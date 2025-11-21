<script setup>
import { state } from '../stores/useGame'
import SocketService from '../services/SocketService'

const size = 10
const cells = Array.from({ length: size }, (_, r) =>
  Array.from({ length: size }, (_, c) => String.fromCharCode(65 + r) + (c + 1))
)

function fire(cell) {
  if (!state.started) return
  if (state.currentTurnSid !== SocketService.id()) return
  SocketService.emit("fire", { roomId: state.roomId, cell })
}

function cellColor(cell) {
  // Agua disparada por mí
  if (state.logs.some(l => l.includes(`disparó ${cell}: Agua`))) return 'blue'
  // Tocado
  if (state.logs.some(l => l.includes(`disparó ${cell}: Tocado`))) return 'red'
  // Hundido
  if (state.logs.some(l => l.includes(`Hundido`) && l.includes(cell))) return 'black'
  return 'grey'
}
</script>

<template>
  <v-container>
    <v-row v-for="row in cells" :key="row[0]" no-gutters>
      <v-col v-for="cell in row" :key="cell" cols="1">
        <v-btn
          :color="cellColor(cell)"
          @click="fire(cell)"
          size="small"
        >
          {{ cell }}
        </v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>
