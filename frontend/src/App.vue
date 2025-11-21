<script setup>
import { state, setupSocketHandlers } from './stores/useGame'
import SocketService from './services/SocketService'
import { onMounted } from 'vue'
import Lobby from './components/Lobby.vue'
import Preparation from './components/Preparation.vue'
import Game from './components/Game.vue'

onMounted(() => {
  setupSocketHandlers()
  SocketService.connect()
})
</script>

<template>
  <v-app>
    <v-main>
      <v-container>
        <Lobby v-if="!state.roomId" />
        <Preparation v-else-if="!state.started" />
        <Game v-else />
      </v-container>
    </v-main>
  </v-app>
</template>
