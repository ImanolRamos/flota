<template>
  <div class="battle-wrapper">
    <v-card class="battle-card pa-3" elevation="10">

      <!-- ENCABEZADO DE COLUMNAS -->
      <div class="header-row">
        <div class="corner"></div>
        <div v-for="letter in letters" :key="letter" class="header-cell">
          {{ letter }}
        </div>
      </div>

      <!-- TABLERO COMPLETO -->
      <div class="board-grid">
        <template v-for="row in rows" :key="row">
          <!-- Etiqueta de fila -->
          <div class="row-label">{{ row }}</div>

          <!-- Celdas -->
          <div
            v-for="col in cols"
            :key="`${row}-${col}`"
            class="game-cell"
            :class="getCellClass(row, col)"
            @click="handleCellClick(row, col)"
          >
            <v-icon v-if="boardState[row][col] === 'AGUA'" class="splash-icon">
              mdi-close-circle-outline
            </v-icon>
            <v-icon v-else-if="boardState[row][col] === 'IMPACTO'" class="hit-icon">
              mdi-fire
            </v-icon>
          </div>
        </template>
      </div>

    </v-card>
  </div>
</template>

<script setup>
import { ref, computed } from "vue";

const SIZE = 10;

const rows = computed(() => Array.from({ length: SIZE }, (_, i) => i + 1));
const letters = computed(() =>
  Array.from({ length: SIZE }, (_, i) => String.fromCharCode(65 + i))
);
const cols = computed(() => Array.from({ length: SIZE }, (_, i) => i));

/* ====== DEMO BOARD ====== */
const initialBoard = {};
rows.value.forEach((row) => {
  initialBoard[row] = Array(SIZE).fill("VACIO");
});
initialBoard[2][1] = "BARCO";
initialBoard[3][1] = "BARCO";

const boardState = ref(initialBoard);

/* ====== CLASSES ====== */
const getCellClass = (row, col) => {
  const state = boardState.value[row][col];
  return {
    "cell-vacio": state === "VACIO",
    "cell-barco": state === "BARCO",
    "cell-agua": state === "AGUA",
    "cell-impacto": state === "IMPACTO",
  };
};

/* ====== HANDLE CLICK ====== */
const handleCellClick = (row, colIndex) => {
  const current = boardState.value[row][colIndex];
  if (navigator.vibrate) navigator.vibrate(40);

  if (current === "VACIO") boardState.value[row][colIndex] = "AGUA";
  else if (current === "BARCO") boardState.value[row][colIndex] = "IMPACTO";
};
</script>

<style scoped>
/* ======================================================
   WRAPPER
   ====================================================== */
.battle-wrapper {
  width: 100%;
  display: flex;
  justify-content: center;
}

/* ======================================================
   CARD
   ====================================================== */
.battle-card {
  background: radial-gradient(circle at center, #112030 0%, #0a1520 100%);
  border: 2px solid rgba(0, 180, 255, 0.3);
  border-radius: 16px;
  color: #e0f4ff;
  padding: 12px;
}

/* ======================================================
   ENCABEZADOS
   ====================================================== */
.header-row {
  display: grid;
  grid-template-columns: 40px repeat(10, 1fr);
  margin-bottom: 4px;
}

.corner {
  width: 40px;
}

.header-cell {
  text-align: center;
  font-weight: bold;
  color: #66d3ff;
}

/* ======================================================
   TABLERO
   ====================================================== */
.board-grid {
  display: grid;
  grid-template-columns: 40px repeat(10, 1fr);
  gap: 2px;
  width: 100%;
  margin: 0 auto;
}

.row-label {
  display: flex;
  justify-content: center;
  align-items: center;
  font-weight: bold;
  color: #66d3ff;
}

.game-cell {
  border: 1px solid rgba(120, 160, 190, 0.4);
  background-color: rgba(255, 255, 255, 0.05);
  display: flex;
  justify-content: center;
  align-items: center;
  aspect-ratio: 1 / 1;   /* cuadradas */
  transition: background-color 0.2s, transform 0.1s;
}

.game-cell:hover {
  background-color: rgba(255, 255, 255, 0.15);
  transform: scale(1.05);
}

/* ======================================================
   ESTADOS
   ====================================================== */
.cell-vacio { background-color: rgba(255, 255, 255, 0.05); }
.cell-barco { background-color: rgba(120, 120, 120, 0.45); }
.cell-agua  { background-color: rgba(90, 170, 255, 0.25); }
.cell-impacto { background-color: rgba(255, 90, 90, 0.35); }

/* ======================================================
   ICONOS
   ====================================================== */
.splash-icon { color: #8ecbff; }
.hit-icon { color: red; }

/* ======================================================
   RESPONSIVE
   ====================================================== */
@media (max-width: 600px) {
  .header-row, .board-grid {
    grid-template-columns: 30px repeat(10, 1fr);
    max-width: 95vmin;
  }
  .corner, .row-label {
    font-size: 0.7rem;
  }
}
</style>
