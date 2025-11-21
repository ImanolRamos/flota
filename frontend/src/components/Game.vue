<script setup>
import { computed } from 'vue'
import { state } from '../stores/useGame'
import SocketService from '../services/SocketService'

const size = 10
const cells = Array.from({ length: size }, (_, r) =>
  Array.from({ length: size }, (_, c) => String.fromCharCode(65 + r) + (c + 1))
)

// Disparo al tablero enemigo
function fire(cell) {
  if (!state.started) return
  if (state.currentTurnSid !== SocketService.id()) return
  SocketService.emit("fire", { roomId: state.roomId, cell })
}

// Colores del tablero enemigo basados en sets de disparos propios
function enemyCellColor(cell) {
  if (state.shots?.my?.sunk?.has(cell)) return 'black'
  if (state.shots?.my?.hit?.has(cell)) return 'red'
  if (state.shots?.my?.water?.has(cell)) return 'blue'
  return 'grey-lighten-3'
}

// Colores del tablero propio: verde si hay barco, rojo si el rival lo ha tocado
function myCellColor(cell) {
  const hasShip = Object.values(state.me.board || {}).some(list => list?.includes(cell))
  const gotHit = state.shots?.opp?.hit?.has(cell)
  if (gotHit) return 'red'
  if (hasShip) return 'success'
  return 'grey-lighten-3'
}

const isMyTurn = computed(() => state.currentTurnSid === state.me.sid)
</script>

<template>
  <v-card class="pa-4">
    <v-card-title class="d-flex align-center justify-space-between">
        <div>
            <span>Partida en curso</span>
            <div class="players">
            <strong>{{ state.me.name || 'Yo' }}</strong>
            vs
            <strong>{{ state.opponent.name || 'Rival' }}</strong>
            </div>
        </div>
        <v-chip :color="isMyTurn ? 'green' : 'grey'">
            Turno: {{ isMyTurn ? 'Tu turno' : 'Turno del rival' }}
        </v-chip>
    </v-card-title>

    <v-card-text>
      <v-row>
        <!-- Tablero propio -->
        <v-col cols="12" md="6">
          <h4 class="mb-2">Tu tablero</h4>
          <div class="board-grid">
            <div v-for="row in cells" :key="row[0]" class="d-flex">
              <v-btn
                v-for="cell in row"
                :key="cell"
                :color="myCellColor(cell)"
                size="x-small"
                tile
                class="board-cell"
                :disabled="true"
              >
                {{ cell.slice(1) }}
              </v-btn>
            </div>
          </div>
        </v-col>

        <!-- Tablero enemigo -->
        <v-col cols="12" md="6">
          <h4 class="mb-2">Tablero enemigo</h4>
          <div class="board-grid">
            <div v-for="row in cells" :key="row[0]" class="d-flex">
              <v-btn
                v-for="cell in row"
                :key="cell"
                :color="enemyCellColor(cell)"
                @click="fire(cell)"
                :disabled="!isMyTurn"
                size="x-small"
                tile
                class="board-cell"
              >
                {{ cell.slice(1) }}
              </v-btn>
            </div>
          </div>
        </v-col>
      </v-row>

      <!-- Leyenda -->
      <v-row class="mt-4">
        <v-col cols="12">
          <div class="legend">
            <div class="legend-item">
              <span class="legend-swatch swatch-grey"></span> Sin disparar / agua propia
            </div>
            <div class="legend-item">
              <span class="legend-swatch swatch-green"></span> Barco propio
            </div>
            <div class="legend-item">
              <span class="legend-swatch swatch-blue"></span> Agua en enemigo
            </div>
            <div class="legend-item">
              <span class="legend-swatch swatch-red"></span> Tocado
            </div>
            <div class="legend-item">
              <span class="legend-swatch swatch-black"></span> Hundido (celda final)
            </div>
          </div>
        </v-col>
      </v-row>

      <!-- Logs -->
      <v-card class="mt-4" variant="tonal">
        <v-card-title>Eventos</v-card-title>
        <v-card-text>
          <v-list density="compact">
            <v-list-item v-for="(l,i) in state.logs" :key="i">{{ l }}</v-list-item>
          </v-list>
        </v-card-text>
      </v-card>
    </v-card-text>
  </v-card>
</template>
<style scoped>

/* ============================================================
   BATTLESHIP NEO-WAVE THEME
   Estilo futurista, brillante, con animaciones sutiles
   ============================================================ */

/* Contenedor general */
.v-card {
  background: radial-gradient(circle at top, #0a1124, #060812 70%);
  border: 1px solid rgba(0, 180, 255, 0.2);
  border-radius: 14px;
  box-shadow: 0 4px 25px rgba(0,150,255,0.25);
  color: #d9eaff;
}

/* Título */
.v-card-title {
  font-weight: bold;
  font-size: 1.3rem;
  color: #cfe9ff;
  text-shadow: 0 0 6px rgba(0,150,255,0.6);
}

/* Chip de turno */
.v-chip {
  font-weight: bold;
  color: white !important;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(255,255,255,0.4);
  animation: turnPulse 2s infinite ease-in-out;
}

@keyframes turnPulse {
  0% { transform: scale(1); box-shadow: 0 0 8px rgba(0,150,255,0.3); }
  50% { transform: scale(1.07); box-shadow: 0 0 14px rgba(0,180,255,0.8); }
  100% { transform: scale(1); box-shadow: 0 0 8px rgba(0,150,255,0.3); }
}

/* =========================
   TABLEROS
   ========================= */
.board-grid {
  display: flex;
  flex-direction: column;
  border: 3px solid rgba(0,180,255,0.5);
  background: rgba(0, 30, 60, 0.4);
  backdrop-filter: blur(6px);
  border-radius: 10px;
  padding: 8px;
  box-shadow: 0 0 20px rgba(0,150,255,0.4);
}

/* Celdas */
.board-cell {
  min-width: 42px !important;
  max-width: 42px !important;
  height: 42px !important;
  margin: 2px;
  padding: 0;
  border-radius: 8px !important;
  font-size: 0.75rem;
  font-weight: bold;
  transition: transform .15s, box-shadow .2s;
  color: white !important;
  border: 1px solid rgba(255,255,255,0.12);
}

/* Hover ataque */
.board-cell:not(:disabled):hover {
  transform: scale(1.08);
  box-shadow: 0 0 12px rgba(0,180,255,0.8);
}

/* ======== COLORES DE ESTADO ======== */
.board-cell.success { 
  background: linear-gradient(135deg, #1ea35f, #0c6938); 
  box-shadow: 0 0 10px #1ea35f;
}

.board-cell.red { 
  background: linear-gradient(135deg, #ff4141, #9e0c0c);
  box-shadow: 0 0 12px rgba(255,0,0,0.9);
  animation: hitBlink 0.6s infinite alternate;
}

@keyframes hitBlink {
  from { filter: brightness(1); }
  to { filter: brightness(1.4); }
}

.board-cell.blue { 
  background: linear-gradient(135deg, #4db8ff, #006bb3); 
  box-shadow: 0 0 10px rgba(88,179,255,0.8);
}

.board-cell.black { 
  background: linear-gradient(135deg, #000, #333);
  box-shadow: 0 0 14px rgba(255,255,255,0.4);
}

.board-cell.grey-lighten-3 { 
  background: rgba(255,255,255,0.10) !important; 
}

/* =========================
   LEYENDA
   ========================= */
.legend {
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
  background: rgba(0,20,40,0.7);
  border: 1px solid rgba(0,180,255,0.4);
  border-radius: 12px;
  padding: 15px 20px;
  backdrop-filter: blur(5px);
  box-shadow: 0 4px 12px rgba(0,100,200,0.2);
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #d9eaff;
  font-size: 0.9rem;
}

.legend-swatch {
  width: 20px;
  height: 20px;
  border-radius: 4px;
  border: 1px solid rgba(255,255,255,0.3);
}

/* Colores leyenda */
.swatch-grey { background: rgba(255,255,255,0.15); }
.swatch-green { background: #1ea35f; }
.swatch-blue { background: #4db8ff; }
.swatch-red { background: #ff4141; }
.swatch-black { background: black; }

/* =========================
   LOGS
   ========================= */
.v-card.variant-tonal {
  background: rgba(0, 25, 50, 0.6) !important;
  border: 1px solid rgba(0,180,255,0.3);
}

.v-list-item {
  color: #cfe9ff !important;
  background: rgba(0, 40, 80, 0.4);
  margin-bottom: 4px;
  border-radius: 6px;
  font-family: Consolas, monospace;
  transition: transform .15s;
}

.v-list-item:hover {
  transform: translateX(5px);
  background: rgba(0,150,255,0.25);
}
.players {
  font-size: 0.9rem;
  color: #bbdefb;
  margin-top: 4px;
}
.players strong {
  color: #fff;
  text-shadow: 0 0 6px rgba(0,150,255,0.6);
}

/* =========================
   RESPONSIVE
   ========================= */
@media (max-width: 600px) {
  .board-cell {
    min-width: 32px !important;
    max-width: 32px !important;
    height: 32px !important;
    font-size: 0.6rem;
  }
}


</style>