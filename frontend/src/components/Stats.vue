<script setup>
import { state } from '../stores/useGame'
import SocketService from '../services/SocketService'

// Reiniciar: volver al lobby y limpiar estado
function newGame() {
  state.currentView = "lobby"
  state.roomId = ""
  state.me.ready = false
  state.opponent = { name: "", sid: "", ready: false, board: {}, hits: new Set() }
  state.logs = []
  state.started = false
  state.currentTurnSid = null
  state.shots.my = { water: new Set(), hit: new Set(), sunk: new Set() }
  state.shots.opp = { water: new Set(), hit: new Set(), sunk: new Set() }
}
</script>

<template>
  <v-card class="pa-4 stats-card">
    <v-card-title class="d-flex align-center justify-space-between">
      <span>Historial de partidas</span>
      <v-btn color="primary" @click="newGame">Nuevo juego</v-btn>
    </v-card-title>

    <v-card-text>
      <v-table class="stats-table">
        <thead>
          <tr>
            <th>Fecha</th>
            <th>Jugador</th>
            <th>Oponente</th>
            <th>Resultado</th>
            <th>Mis disparos (agua/tocado/hundido)</th>
            <th>Rival (agua/tocado/hundido)</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(game, i) in state.history" :key="i">
            <td>{{ game.date }}</td>
            <td>{{ game.me }}</td>
            <td>{{ game.opponent }}</td>
            <td>
              <v-chip :color="game.result === 'victoria' ? 'green' : 'red'" dark>
                {{ game.result }}
              </v-chip>
            </td>
            <td>{{ game.shots.my.water }}/{{ game.shots.my.hit }}/{{ game.shots.my.sunk }}</td>
            <td>{{ game.shots.opp.water }}/{{ game.shots.opp.hit }}/{{ game.shots.opp.sunk }}</td>
          </tr>
        </tbody>
      </v-table>
    </v-card-text>
  </v-card>
</template>

<style scoped>
/* Estilo futurista coherente con Game.vue */
.stats-card {
  background: radial-gradient(circle at top, #0a1124, #060812 70%);
  border: 1px solid rgba(0, 180, 255, 0.2);
  border-radius: 14px;
  box-shadow: 0 4px 25px rgba(0,150,255,0.25);
  color: #d9eaff;
}

.v-card-title {
  font-weight: bold;
  font-size: 1.3rem;
  color: #cfe9ff;
  text-shadow: 0 0 6px rgba(0,150,255,0.6);
}

.stats-table {
  background: rgba(0, 30, 60, 0.4);
  border-radius: 10px;
  overflow: hidden;
}

.stats-table th {
  color: #9ecfff;
  font-weight: bold;
  background: rgba(0, 60, 120, 0.4);
}

.stats-table td {
  color: #d9eaff;
  background: rgba(0, 20, 40, 0.4);
  padding: 6px 10px;
}

.v-chip {
  font-weight: bold;
  text-transform: capitalize;
  box-shadow: 0 0 10px rgba(255,255,255,0.4);
}
</style>
