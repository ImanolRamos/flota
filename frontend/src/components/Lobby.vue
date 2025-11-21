<script setup>
import { ref } from 'vue'
import SocketService from '../services/SocketService'
import { state } from '../stores/useGame'

const roomId = ref('')
const name = ref('')

function createRoom() {
  SocketService.emit("create_room", { roomId: roomId.value, name: name.value || "Jugador" })
}
function joinRoom() {
  SocketService.emit("join_room", { roomId: roomId.value, name: name.value || "Jugador" })
}
</script>

<template>
  <v-card class="pa-4">
    <v-card-title>Lobby</v-card-title>
    <v-card-text>
      <v-text-field v-model="name" label="Tu nombre" />
      <v-text-field v-model="roomId" label="ID de sala" />
      <v-btn color="success" @click="createRoom">Crear sala</v-btn>
      <v-btn color="info" @click="joinRoom">Unirse</v-btn>
    </v-card-text>
  </v-card>
</template>
