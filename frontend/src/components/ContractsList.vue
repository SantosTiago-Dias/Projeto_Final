<template>
  <div class="container max-w-5xl mx-auto px-4 py-8">

    <div class="mb-6">
      <h1 class="text-2xl font-medium text-gray-900">Contratos</h1>
      <p class="text-sm text-gray-400 mt-1">{{ contracts.length }} resultados</p>
    </div>

    <p v-if="loading" class="text-gray-400 text-sm">A carregar...</p>

    <div v-else class="flex flex-col gap-3">

      <div
          v-for="contract in contracts"
          :key="contract.chave_contratos"
          class="bg-white border border-gray-100 rounded-xl p-5 flex flex-col gap-4"
      >

        <!-- Title + Value -->
        <div class="flex justify-between items-start gap-4">
          <div class="flex-1 min-w-0">
            <h2 class="text-[15px] font-medium text-gray-900 line-clamp-2 leading-snug" :title="contract.objeto">
              {{ contract.objeto }}
            </h2>
          </div>
          <div class="text-right shrink-0">
            <p class="text-[17px] font-medium text-green-700">Valor Contratual: {{ formatCurrency(contract.valor_contratual) }}</p>
            <p class="text-xs text-gray-400 mt-1">Data de publicação: {{ contract.data_publicacao }}</p>
          </div>
        </div>

        <!-- Adjudicante + Adjudicatário -->
        <div class="grid grid-cols-2 gap-3 border-t border-gray-100 pt-4">
          <div>
            <p class="text-[11px] uppercase tracking-wide text-gray-400 mb-1">Adjudicante</p>
            <p class="text-sm font-medium text-gray-800 line-clamp-2">{{ contract.adjudicante.nome }}</p>
          </div>
          <div>
            <p class="text-[11px] uppercase tracking-wide text-gray-400 mb-1">Adjudicatário</p>
            <div class="text-sm font-medium text-green-700">
              <template v-for="c in contract.concorrentes" :key="c.id">
                <span v-if="c.adjudicatario === 1">{{ c.entidade.nome }}</span>
              </template>
            </div>
          </div>
        </div>

        <!-- Tags + Button -->
        <div class="flex items-center justify-between flex-wrap gap-2">
          <div class="flex gap-2 flex-wrap">
            <span
                class="text-xs px-3 py-1 rounded-full bg-gray-100 text-gray-600 border border-gray-200"
                :title="contract.tipo_contrato.descricao"
            >
              {{ contract.tipo_contrato.tipo }}
            </span>
            <span
                class="text-xs px-3 py-1 rounded-full bg-blue-50 text-blue-700 border border-blue-100"
                :title="contract.tipo_procedimento.descricao"
            >
              {{ contract.tipo_procedimento.tipo }}
            </span>
          </div>
          <Button
              variant="outline"
              size="sm"
              class="text-xs h-8 px-4"
              @click="goToDetails(contract.chave_contratos)"
          >
            Ver detalhes →
          </Button>
        </div>

      </div>
    </div>
    <div class="flex justify-center items-center gap-2 mt-6">
      <button class="px-4 py-1 rounded-md border border-gray-300 bg-white text-gray-700 hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed" @click="changePage(page.current_page - 1)" :disabled="page.current_page === 1">‹ Anterior</button>
      <span class="px-3 py-1 font-medium text-gray-800">Página {{ page.current_page }} de {{ page.last_page }}</span>
      <button class="px-4 py-1 rounded-md border border-gray-300 bg-white text-gray-700 hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed" @click="changePage(page.current_page + 1)" :disabled="page.current_page === page.last_page">Próximo ›</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import { useAPIStore } from "@/store/api.js"
import {Button} from "@/components/ui/button/index.ts";

const router = useRouter()
const apiStore = useAPIStore()
const contracts = ref([])
const page = ref([])
const loading = ref(true)

const changePage = (page) => {
  if (page >= 1 && page <= response.value.meta.last_page) {
    apiStore.getListContracts(page)
  }
}

onMounted(async () => {
  try {
    const response = await apiStore.getListContracts()
    contracts.value = response.data.data
    page.value = response.data.meta
    console.log(contracts.value)
  } catch (err) {
    console.error("Erro ao carregar contratos:", err)
  } finally {
    loading.value = false
  }
})

function formatCurrency(value) {
  return new Intl.NumberFormat("pt-PT", {
    style: "currency",
    currency: "EUR",
  }).format(Number(value))
}

function goToDetails(id) {
  router.push(`/contracts/${id}`)
}
</script>