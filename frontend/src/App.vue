<script setup>
import { state, setupSocketHandlers } from './stores/useGame'
import SocketService from './services/SocketService'
import { onMounted } from 'vue'
import Lobby from './components/Lobby.vue'
import Preparation from './components/Preparation.vue'
import Game from './components/Game.vue'
import Stats from './components/Stats.vue'

onMounted(() => {
  setupSocketHandlers()
  SocketService.connect()
})
</script>
<template>
  <v-app>
    <v-main>
      <v-container>
        <Lobby v-if="state.currentView === 'lobby'" />
        <Preparation v-else-if="state.currentView === 'preparation'" />
        <Game v-else-if="state.currentView === 'game'" />
        <Stats v-else-if="state.currentView === 'stats'" />
      </v-container>
    </v-main>
  </v-app>
</template>
