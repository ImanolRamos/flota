<template>
  <v-card class="mx-auto pa-2" :width="cellSize * 10 + 60" elevation="10">
    <v-row no-gutters class="text-center font-weight-bold">
      <v-col class="pa-1" style="width: 30px;"></v-col> <v-col
        v-for="letter in letters"
        :key="letter"
        class="pa-1"
        :style="{ width: cellSize + 'px' }"
      >
        {{ letter }}
      </v-col>
    </v-row>

    <v-row
      v-for="row in rows"
      :key="row"
      no-gutters
      class="text-center"
    >
      <v-col class="pa-1 font-weight-bold" style="width: 30px;">
        {{ row }}
      </v-col>
      
      <v-col
        v-for="col in cols"
        :key="`${row}-${col}`"
        class="game-cell"
        :class="getCellClass(row, col)"
        :style="{ width: cellSize + 'px', height: cellSize + 'px' }"
        @click="handleCellClick(row, col)"
      >
        <v-icon v-if="boardState[row][col] === 'AGUA'" color="blue-lighten-2" size="small">
          mdi-close-circle-outline
        </v-icon>
        <v-icon v-else-if="boardState[row][col] === 'IMPACTO'" color="red-darken-3" size="small">
          mdi-fire
        </v-icon>
      </v-col>
    </v-row>
  </v-card>
</template>

<script setup>
import { ref, computed } from 'vue';

// --- Configuración y Datos Base ---

const SIZE = 10;
const cellSize = 35; // Tamaño fijo en píxeles para cada celda

// Generar las etiquetas de fila (1 a 10)
const rows = computed(() => Array.from({ length: SIZE }, (_, i) => i + 1));
// Generar las etiquetas de columna (A a J)
const letters = computed(() => 
  Array.from({ length: SIZE }, (_, i) => String.fromCharCode(65 + i))
);
// Array simple de índices de columna para el v-for
const cols = computed(() => Array.from({ length: SIZE }, (_, i) => i));

// --- Estado del Tablero (Simulación) ---

// Estado de un tablero de 10x10. 
// Valores posibles: 'VACIO', 'BARCO', 'AGUA', 'IMPACTO'
// Usamos un objeto simple donde la clave es el número de fila.
const initialBoard = {};
rows.value.forEach(row => {
  // Inicializamos todas las columnas de la fila como 'VACIO'
  initialBoard[row] = Array(SIZE).fill('VACIO');
});

// Simulamos un barco para la prueba (Impacto en B2, B3)
initialBoard[2][1] = 'BARCO';
initialBoard[3][1] = 'BARCO';

// Estado reactivo del tablero
const boardState = ref(initialBoard);

// --- Lógica y Estilos ---

const getCellClass = (row, col) => {
  const state = boardState.value[row][col];
  return {
    'cell-vacio': state === 'VACIO',
    'cell-barco': state === 'BARCO', // Solo visible en tu propio tablero
    'cell-agua': state === 'AGUA',
    'cell-impacto': state === 'IMPACTO',
    'cursor-pointer': true, // Para indicar que se puede hacer clic (si es el turno de ataque)
  };
};

const handleCellClick = (row, colIndex) => {
  const colLetter = letters.value[colIndex];
  console.log(`Disparo a la celda: ${colLetter}${row}`);
  
  // Lógica de simulación: Cambiar el estado para probar
  const currentState = boardState.value[row][colIndex];
  
  if (currentState === 'VACIO') {
    boardState.value[row][colIndex] = 'AGUA';
  } else if (currentState === 'BARCO') {
    boardState.value[row][colIndex] = 'IMPACTO';
  }
};

</script>

<style scoped>
.game-cell {
  border: 1px solid #ccc;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background-color 0.2s;
}

.cursor-pointer:hover {
  background-color: #e0e0e0; /* Gris claro al pasar el ratón */
}

/* Estilos de estado (puedes ajustarlos a tu gusto) */
.cell-vacio {
  background-color: #f5f5f5; /* Casi blanco */
}
.cell-barco {
  /* En el tablero propio, los barcos se pueden mostrar */
  background-color: #aaa; 
}
.cell-agua {
  background-color: #c9e9ff; /* Azul muy claro */
}
.cell-impacto {
  background-color: #ffcccc; /* Rojo muy claro */
}
</style>