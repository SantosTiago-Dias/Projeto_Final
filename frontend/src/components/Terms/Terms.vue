<template>
  <div class="page-wrapper">
    <div class="table-container">
      <!-- Título da Página adicionado aqui -->
      <div class="table-header">
        <h1>Glossário de Termos</h1>
        <p>Consulte os principais conceitos e os seus significados.</p>
      </div>

      <table class="clean-table">
        <thead>
        <tr>
          <th class="term-th">Termo</th>
          <th class="meaning-th">Significado</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="term in terms" :key="term.id">
          <td class="term-cell">{{ decodeText(term.term) }}</td>
          <td class="meaning-cell">{{ decodeText(term.meaning) }}</td>
        </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { useAPIStore } from "@/store/api";
import { onMounted, ref } from "vue";

const apiStore = useAPIStore();
const terms = ref([]);

// Função auxiliar para corrigir caracteres estragados caso a API venha com encoding errado
const decodeText = (str: string) => {
  if (!str) return '';
  try {
    // Tenta decodificar a string se ela estiver em formato "mojibake" (UTF-8 lido como ISO-8859-1)
    return decodeURIComponent(escape(str));
  } catch (e) {
    return str; // Se falhar, devolve o texto original
  }
};

onMounted(async () => {
  let res = await apiStore.getTerms();
  terms.value = res.data;
});
</script>

<style scoped>
.page-wrapper {
  padding: 2.5rem 2rem;
  background-color: #ffffff;
  min-height: 100vh;
}

.table-container {
  max-width: 1000px;
  margin: 0 auto;
}

/* Novos estilos para o Título */
.table-header {
  margin-bottom: 2.5rem;
}

.table-header h1 {
  font-size: 2rem;
  font-weight: 800;
  color: #111111;
  margin: 0 0 0.5rem 0;
  letter-spacing: -0.025em;
}

.table-header p {
  font-size: 1rem;
  color: #64748b;
  margin: 0;
}

.clean-table {
  width: 100%;
  border-collapse: collapse;
  border: none;
}

/* Alinhamento perfeito do Header */
th {
  text-align: left;
  color: #8c8c8c;
  font-size: 0.85rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding-bottom: 1.5rem; /* Espaço antes de começar a lista */
}

.term-th {
  width: 25%;
  padding-left: 0.5rem;
}

.meaning-th {
  width: 75%;
  padding-left: 1rem;
}

/* Alinhamento e espaçamento das células */
td {
  vertical-align: top;
  padding: 1.5rem 0; /* Mais espaçamento vertical para compensar a falta de linhas */
}

.term-cell {
  font-weight: 700;
  color: #111111;
  font-size: 0.95rem;
  padding-left: 0.5rem;
}

.meaning-cell {
  color: #4a5568;
  font-size: 0.95rem;
  line-height: 1.6; /* Melhora a leitura de parágrafos longos */
  padding-left: 1rem;
  padding-right: 2rem;
}

/* Um efeito de transição super suave ao passar o rato (hover) */
tr {
  transition: background-color 0.2s ease;
}

tr:hover td {
  background-color: #f8fafc;
  /* Cria cantos arredondados discretos na linha selecionada */
  &:first-child { border-top-left-radius: 6px; border-bottom-left-radius: 6px; }
  &:last-child { border-top-right-radius: 6px; border-bottom-right-radius: 6px; }
}
</style>