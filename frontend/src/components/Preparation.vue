<script setup>
import { ref, computed } from 'vue'
import SocketService from '../services/SocketService'
import { state } from '../stores/useGame'

const size = 10
const cells = Array.from({ length: size }, (_, r) =>
  Array.from({ length: size }, (_, c) => String.fromCharCode(65 + r) + (c + 1))
)

const shipDefinitions = {
  carrier: { size: 5, placed: false, coords: [] },
  battleship: { size: 4, placed: false, coords: [] },
  cruiser: { size: 3, placed: false, coords: [] },
  submarine: { size: 3, placed: false, coords: [] },
  destroyer: { size: 2, placed: false, coords: [] }
}

const ships = ref(JSON.parse(JSON.stringify(shipDefinitions)))
const selectedShip = ref('carrier')
const orientation = ref('horizontal') // 'horizontal' | 'vertical' | 'diagonal-down' | 'diagonal-up'

const message = ref('')
const messageType = ref('error')
const snackbar = ref(false)

function showMessage(text, type = 'error') {
  message.value = text
  messageType.value = type
  snackbar.value = true
}

const availableShips = computed(() =>
  Object.keys(ships.value).filter(key => !ships.value[key].placed)
)

const placedCells = computed(() =>
  Object.values(ships.value).flatMap(ship => ship.coords)
)

function coordToIndices(coord) {
  const rowChar = coord.charAt(0)
  const colNum = parseInt(coord.slice(1))
  return { r: rowChar.charCodeAt(0) - 65, c: colNum - 1 }
}

function indicesToCoord(r, c) {
  if (r < 0 || r >= size || c < 0 || c >= size) return null
  return String.fromCharCode(65 + r) + (c + 1)
}

function calcCoords(startCell, shipLength) {
  const { r, c } = coordToIndices(startCell)
  const coords = []
  for (let i = 0; i < shipLength; i++) {
    let nextCoord = null
    if (orientation.value === 'horizontal') nextCoord = indicesToCoord(r, c + i)
    else if (orientation.value === 'vertical') nextCoord = indicesToCoord(r + i, c)
    else if (orientation.value === 'diagonal-down') nextCoord = indicesToCoord(r + i, c + i)
    else if (orientation.value === 'diagonal-up') nextCoord = indicesToCoord(r - i, c + i)
    if (nextCoord) coords.push(nextCoord)
  }
  return coords
}

function placeShip(startCell) {
  const shipKey = selectedShip.value
  const shipLength = ships.value[shipKey].size
  const newCoords = calcCoords(startCell, shipLength)

  if (newCoords.length !== shipLength) {
    showMessage("El barco no cabe en el tablero.")
    return
  }
  const overlap = newCoords.some(coord => placedCells.value.includes(coord))
  if (overlap) {
    showMessage("Se superpone con otro barco.")
    return
  }

  ships.value[shipKey].coords = newCoords
  ships.value[shipKey].placed = true

  const nextShip = availableShips.value.find(s => s !== shipKey)
  if (nextShip) selectedShip.value = nextShip
  else showMessage("¡Todos los barcos colocados! Pulsa 'Flota Lista'.", 'success')
}

function removeShip(cell) {
  const shipKey = Object.keys(ships.value).find(key =>
    ships.value[key].coords.includes(cell)
  )
  if (shipKey) {
    ships.value[shipKey].coords = []
    ships.value[shipKey].placed = false
    selectedShip.value = shipKey
  }
}

function handleCellClick(cell) {
  if (placedCells.value.includes(cell)) removeShip(cell)
  else if (availableShips.value.length > 0) placeShip(cell)
}

const hoverPreview = ref([])
function previewCoords(startCell) {
  if (availableShips.value.length === 0) return
  const shipKey = selectedShip.value
  const shipLength = ships.value[shipKey].size
  hoverPreview.value = calcCoords(startCell, shipLength)
}
function clearPreview() {
  hoverPreview.value = []
}

function cellColor(cell) {
  if (placedCells.value.includes(cell)) return 'success'
  if (hoverPreview.value.includes(cell)) return 'preview'
  return 'grey-lighten-3'
}

function ready() {
  if (availableShips.value.length > 0) {
    showMessage("Debes colocar todos los barcos.")
    return
  }
  const finalBoard = {}
  Object.entries(ships.value).forEach(([key, ship]) => {
    finalBoard[key] = ship.coords
  })
  state.me.board = finalBoard
  SocketService.emit("place_ships", { roomId: state.roomId, board: finalBoard })
}
</script>

<template>
  <v-card class="pa-4">
    <v-card-title>Preparación</v-card-title>
    <v-card-text>
      <v-select v-model="selectedShip" :items="availableShips" label="Barco" />
      <v-btn-toggle v-model="orientation" mandatory class="mb-4">
        <v-btn value="horizontal"><v-icon>mdi-arrow-right</v-icon></v-btn>
        <v-btn value="vertical"><v-icon>mdi-arrow-down</v-icon></v-btn>
        <v-btn value="diagonal-down"><v-icon>mdi-arrow-bottom-right</v-icon></v-btn>
        <v-btn value="diagonal-up"><v-icon>mdi-arrow-top-right</v-icon></v-btn>
      </v-btn-toggle>

      <div class="board-grid">
        <div v-for="row in cells" :key="row[0]" class="d-flex">
          <v-btn
            v-for="cell in row"
            :key="cell"
            :color="cellColor(cell)"
            @click="handleCellClick(cell)"
            @mouseenter="previewCoords(cell)"
            @mouseleave="clearPreview"
            size="x-small"
            tile
            class="board-cell"
          >
            {{ cell.slice(1) }}
          </v-btn>
        </div>
      </div>

      <v-btn :disabled="availableShips.length > 0" @click="ready" color="teal">Flota Lista</v-btn>
    </v-card-text>

    <v-snackbar v-model="snackbar" :timeout="3000" :color="messageType">
      {{ message }}
    </v-snackbar>
  </v-card>
</template>
<style scoped>
.board-grid {
  display: flex;
  flex-direction: column;
  border: 3px solid #2196f3;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 6px 18px rgba(33, 150, 243, 0.3);
  background: linear-gradient(180deg, #0d1b2a 0%, #1b263b 100%);
  padding: 8px;
}

.board-cell {
  min-width: 40px !important;
  max-width: 40px !important;
  height: 40px !important;
  margin: 2px;
  padding: 0;
  font-size: 0.75rem;
  font-weight: bold;
  border-radius: 6px !important;
  transition: all 0.25s ease;
  color: #e3f2fd;
}

/* Agua */
.board-cell.grey-lighten-3 {
  background-color: #37474f !important;
}

/* Barco colocado */
.board-cell.success {
  background-color: #43a047 !important;
  border: 2px solid #66bb6a !important;
  box-shadow: 0 0 8px rgba(102, 187, 106, 0.8);
  color: white;
}

/* Fantasma en hover */
.board-cell.preview {
  background-color: rgba(96, 125, 139, 0.6) !important;
  border: 2px dashed #90a4ae !important;
  animation: pulsePreview 1s infinite alternate;
}

/* Animación fantasma */
@keyframes pulsePreview {
  from { background-color: rgba(96, 125, 139, 0.4); }
  to   { background-color: rgba(96, 125, 139, 0.8); }
}

/* Botones de orientación */
.v-btn-toggle {
  background: rgba(255, 255, 255, 0.05);
  border-radius: 8px;
  padding: 4px;
  box-shadow: 0 2px 6px rgba(33, 150, 243, 0.3);
}

.v-btn-toggle .v-btn {
  color: #bbdefb;
  transition: background-color 0.3s ease, transform 0.2s ease;
}

.v-btn-toggle .v-btn.v-btn--active {
  background-color: #2196f3 !important;
  color: white !important;
  transform: scale(1.1);
  box-shadow: 0 0 10px rgba(33, 150, 243, 0.6);
}

/* Snackbar */
.v-snackbar {
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
  font-weight: bold;
}
</style>
