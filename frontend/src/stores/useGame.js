import { reactive } from "vue";
import SocketService from "../services/SocketService";

export const state = reactive({
  currentView: "lobby", // lobby, preparation, game, stats
  roomId: "",
  // Inicializamos me y opponent con estructuras limpias
  me: { name: "", sid: "", ready: false, board: {}, hits: new Set() },
  opponent: { name: "", sid: "", ready: false, board: {}, hits: new Set() },
  started: false,
  currentTurnSid: null,
  logs: [],
  shots: {
    my: { water: new Set(), hit: new Set(), sunk: new Set() },
    opp: { water: new Set(), hit: new Set(), sunk: new Set() }
  },
  history: []
});

export function setupSocketHandlers() {
  const saved = localStorage.getItem("gameHistory");
  if (saved) state.history = JSON.parse(saved);
  
// ----------------------------------------------------------------
// REFACTORIZACIÓN EN "room_update"
// ----------------------------------------------------------------
  SocketService.on("room_update", (payload) => {
    state.roomId = payload.roomId;
    state.me.sid = SocketService.id();
    state.logs.push("Sala actualizada: " + state.roomId);
    
    // 1. Aseguramos que 'players' existe y es un array
    const players = payload.players;

    if (players && Array.isArray(players)) {
      
      // 2. Buscamos al jugador local y al oponente
      const meData = players.find(p => p.sid === state.me.sid);
      const opponentData = players.find(p => p.sid !== state.me.sid);

      // Actualizar datos del jugador local
      if (meData) {
        state.me.name = meData.name || state.me.name;
      }
      
      // Actualizar datos del oponente
      if (opponentData) {
        state.opponent.name = opponentData.name || state.opponent.name || 'Rival';
        state.opponent.sid = opponentData.sid;
      } else {
         // Limpiar estado si el oponente se fue (aunque 'opponent_left' ya lo hace, esto es preventivo)
         state.opponent = { name: "", sid: "", ready: false, board: {}, hits: new Set() };
      }
    }

    state.currentView = "preparation";
  });
// ----------------------------------------------------------------
// FIN REFACTORIZACIÓN
// ----------------------------------------------------------------

  SocketService.on("player_ready", ({ sid }) => {
    if (sid === state.me.sid) state.me.ready = true;
    else state.opponent.ready = true;
    state.logs.push("Jugador listo: " + sid);
  });

  SocketService.on("game_started", ({ turn }) => {
    state.started = true;
    state.currentTurnSid = turn;
    state.logs.push("Partida iniciada");
    state.currentView = "game";
  });

  SocketService.on("fire_result", ({ by, cell, hit, sunk }) => {
    const iShot = by === state.me.sid;
    const label = iShot ? "Tú" : "Rival";
    state.logs.push(`${label} disparó ${cell}: ${hit ? "Tocado" : "Agua"}${sunk ? " (Hundido)" : ""}`);

    if (iShot) {
      if (hit) state.shots.my.hit.add(cell);
      else state.shots.my.water.add(cell);
      if (sunk) state.shots.my.sunk.add(cell);
    } else {
      if (hit) state.shots.opp.hit.add(cell);
      else state.shots.opp.water.add(cell);
      if (sunk) state.shots.opp.sunk.add(cell);
    }
  });

  SocketService.on("turn_changed", ({ turn }) => {
    state.currentTurnSid = turn;
    state.logs.push("Turno cambiado");
  });

  SocketService.on("game_over", ({ winner }) => {
    const result = winner === state.me.sid ? "victoria" : "derrota";
    state.logs.push(result === "victoria" ? "¡Has ganado!" : "Has perdido.");
    state.started = false;

    state.history.push({
      date: new Date().toLocaleString(),
      me: state.me.name || state.me.sid,
      opponent: state.opponent.name || state.opponent.sid,
      result,
      shots: {
        my: {
          water: state.shots.my.water.size,
          hit: state.shots.my.hit.size,
          sunk: state.shots.my.sunk.size
        },
        opp: {
          water: state.shots.opp.water.size,
          hit: state.shots.opp.hit.size,
          sunk: state.shots.opp.sunk.size
        }
      }
    });
    localStorage.setItem("gameHistory", JSON.stringify(state.history));

    state.currentView = "stats";

    state.shots.my = { water: new Set(), hit: new Set(), sunk: new Set() };
    state.shots.opp = { water: new Set(), hit: new Set(), sunk: new Set() };
  });

  SocketService.on("opponent_left", () => {
    state.logs.push("El oponente abandonó la sala.");
    state.started = false;
    state.currentView = "lobby";
    // Limpieza completa del oponente
    state.opponent = { name: "", sid: "", ready: false, board: {}, hits: new Set() };
    // Opcional: limpiar tu estado de listo si quieres forzar a empezar de nuevo
    state.me.ready = false; 
  });

  SocketService.on("error_message", ({ error }) => {
    state.logs.push("Error: " + error);
  });
}