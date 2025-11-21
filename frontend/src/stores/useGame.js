import { reactive } from "vue";
import SocketService from "../services/SocketService";

export const state = reactive({
  roomId: "",
  me: { name: "", sid: "", ready: false, board: {}, hits: new Set() },
  opponent: { name: "", sid: "", ready: false, board: {}, hits: new Set() },
  started: false,
  currentTurnSid: null,
  logs: [],
  shots: {
    my: { water: new Set(), hit: new Set(), sunk: new Set() },
    opp: { water: new Set(), hit: new Set(), sunk: new Set() }
  }
});

export function setupSocketHandlers() {
  SocketService.on("room_update", ({ roomId }) => {
    state.roomId = roomId;
    state.me.sid = SocketService.id();
    state.logs.push("Sala actualizada: " + roomId);
  });

  SocketService.on("player_ready", ({ sid }) => {
    if (sid === state.me.sid) state.me.ready = true;
    else state.opponent.ready = true;
    state.logs.push("Jugador listo: " + sid);
  });

  SocketService.on("game_started", ({ turn }) => {
    state.started = true;
    state.currentTurnSid = turn;
    state.logs.push("Partida iniciada");
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
    state.logs.push(winner === state.me.sid ? "¡Has ganado!" : "Has perdido.");
    state.started = false;
  });

  SocketService.on("opponent_left", () => {
    state.logs.push("El oponente abandonó la sala.");
    state.started = false;
  });

  SocketService.on("error_message", ({ error }) => {
    state.logs.push("Error: " + error);
  });
}
