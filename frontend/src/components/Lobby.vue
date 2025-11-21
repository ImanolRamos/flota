<script setup>
import { ref, onMounted } from 'vue'
import SocketService from '../services/SocketService'
import { state } from '../stores/useGame'

const roomId = ref('')
const name = ref('')
const hasSavedName = ref(false)

// Al montar, comprobar si hay nombre guardado
onMounted(() => {
  const savedName = localStorage.getItem("playerName")
  if (savedName) {
    name.value = savedName
    state.me.name = savedName
    hasSavedName.value = true
  }
})

function createRoom() {
  if (!hasSavedName.value) {
    state.me.name = name.value || "Jugador"
    localStorage.setItem("playerName", state.me.name)
    hasSavedName.value = true
  }
  SocketService.emit("create_room", { roomId: roomId.value, name: state.me.name })
}

function joinRoom() {
  if (!hasSavedName.value) {
    state.me.name = name.value || "Jugador"
    localStorage.setItem("playerName", state.me.name)
    hasSavedName.value = true
  }
  SocketService.emit("join_room", { roomId: roomId.value, name: state.me.name })
}

function logout() {
  localStorage.removeItem("playerName")
  name.value = ""
  state.me.name = ""
  hasSavedName.value = false
}
</script>

<template>
  <v-card class="pa-6 lobby-card">
    <v-card-title class="lobby-title">⚓️ Lobby de Batalla Naval</v-card-title>
    <v-card-text>
      <!-- Si ya existe nombre guardado, mostrarlo bloqueado -->
      <v-text-field
        v-if="hasSavedName"
        v-model="name"
        label="Tu nombre"
        readonly
        class="mb-4"
      />
      <!-- Si no existe, permitir elegirlo -->
      <v-text-field
        v-else
        v-model="name"
        label="Tu nombre"
        class="mb-4"
      />

      <v-text-field v-model="roomId" label="ID de sala" class="mb-4" />

      <div class="d-flex flex-wrap gap-4">
        <v-btn color="success" @click="createRoom" class="lobby-btn">Crear sala</v-btn>
        <v-btn color="info" @click="joinRoom" class="lobby-btn">Unirse</v-btn>
        <v-btn v-if="hasSavedName" color="error" @click="logout" class="lobby-btn">Logout</v-btn>
      </div>
    </v-card-text>
  </v-card>
</template>

<style scoped>
.lobby-card {
  background: radial-gradient(circle at top, #0a1124, #060812 70%);
  border: 1px solid rgba(0, 180, 255, 0.3);
  border-radius: 16px;
  box-shadow: 0 4px 25px rgba(0,150,255,0.25);
  color: #d9eaff;
}
.lobby-title {
  font-weight: bold;
  font-size: 1.4rem;
  color: #cfe9ff;
  text-shadow: 0 0 8px rgba(0,150,255,0.7);
}
.lobby-btn {
  font-weight: bold;
  border-radius: 10px;
  box-shadow: 0 0 12px rgba(0,180,255,0.6);
  transition: transform .2s, box-shadow .2s;
}
.lobby-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 0 18px rgba(0,220,255,0.9);
}
</style>
