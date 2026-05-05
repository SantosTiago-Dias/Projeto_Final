<template>
  <div class="container max-w-5xl mx-auto px-4 py-8">

    <!-- Header -->
    <div class="mb-6">
      <h1 class="text-2xl font-medium text-gray-900">Contratos</h1>
      <p v-if="meta" class="text-sm text-gray-400 mt-1">{{ meta.total }} resultados encontrados</p>
    </div>

    <!-- Filtros -->
    <div class="bg-white border border-gray-100 rounded-xl p-6 mb-6 shadow-sm">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">

        <div>
          <label class="block text-xs font-medium text-gray-500 mb-1 uppercase">Tipo de Contrato</label>
          <select v-model="filters.tipo_contrato" class="w-full text-sm border-gray-300 rounded-lg">
            <option :value="null">Todos</option>
            <option v-for="tipoContrato in listTipoContratos" :key="tipoContrato.id" :value="tipoContrato.id">
              {{ tipoContrato.tipo }}
            </option>
          </select>
        </div>

        <div>
          <label class="block text-xs font-medium text-gray-500 mb-1 uppercase">Tipo de Procedimento</label>
          <select v-model="filters.tipo_procedimento" class="w-full text-sm border-gray-300 rounded-lg">
            <option :value="null">Todos</option>
            <option v-for="tipoProcedimento in listTipoProcedimento" :key="tipoProcedimento.id" :value="tipoProcedimento.id">
              {{ tipoProcedimento.tipo }}
            </option>
          </select>
        </div>

        <div>
          <label class="block text-xs font-medium text-gray-500 mb-1 uppercase">CPV</label>
          <input type="text" v-model="filters.cpvs" class="w-full text-sm border-gray-300 rounded-lg" placeholder="Insira uma palavra sobre o tema que quer procurar" />
        </div>

        <div>
          <label class="block text-xs font-medium text-gray-500 mb-1 uppercase">Valor Mínimo (€)</label>
          <input type="number" v-model="filters.valor_contratual" min="0" class="w-full text-sm border-gray-300 rounded-lg" />
        </div>

        <div>
          <label class="block text-xs font-medium text-gray-500 mb-1 uppercase">Data Início</label>
          <input type="date" v-model="filters.data_publicacao_inicio" class="w-full text-sm border-gray-300 rounded-lg" />
        </div>

        <div>
          <label class="block text-xs font-medium text-gray-500 mb-1 uppercase">Data Fim</label>
          <input type="date" v-model="filters.data_publicacao_fim" class="w-full text-sm border-gray-300 rounded-lg" />
        </div>

        <div class="flex items-end gap-2">
          <button @click="fetchContracts()" class="flex-1 bg-green-700 text-white py-2 rounded-lg text-sm font-medium hover:bg-green-800 transition">
            Filtrar
          </button>
          <button @click="resetFilters" class="px-4 py-2 text-gray-400 hover:text-gray-600 text-sm">Limpar</button>
        </div>

      </div>
    </div>

    <!-- Loading State -->
    <p v-if="loading" class="text-gray-400 text-sm italic">A carregar contratos...</p>

    <!-- Contract List -->
    <div v-else class="flex flex-col gap-3">
      <div
          v-for="contract in contracts"
          :key="contract.chave_contratos"
          class="bg-white border border-gray-100 rounded-xl p-5 hover:border-green-200 transition-colors shadow-sm cursor-pointer"
          @click="openModal(contract)"
      >
        <div class="flex justify-between items-start gap-4">
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 mb-1">
              <span class="text-[10px] font-medium uppercase text-blue-600 bg-blue-50 px-1.5 py-0.5 rounded">
                {{ contract.tipo_procedimento?.tipo }}
              </span>
              <span class="text-[10px] font-mono bg-slate-100 text-slate-500 px-1.5 py-0.5 rounded">
                {{ formatDate(contract.data_publicacao) }}
              </span>
            </div>
            <h2 class="text-[15px] font-semibold text-gray-900 line-clamp-1">{{ contract.objeto }}</h2>
          </div>
          <div class="text-right shrink-0">
            <p class="text-base font-bold text-green-700">{{ formatCurrency(contract.valor_contratual) }}</p>
            <Button variant="outline" size="sm" class="text-xs h-8 px-4 mt-1">Ver Detalhes</Button>
          </div>
        </div>
      </div>
    </div>

    <!-- Pagination -->
    <div v-if="meta && meta.last_page > 1" class="mt-6 flex items-center justify-between gap-4">
      <p class="text-sm text-gray-400">
        Página {{ meta.current_page }} de {{ meta.last_page }}
      </p>
      <div class="flex items-center gap-1">
        <!-- First Page -->
        <button
            @click="goToPage(1)"
            :disabled="meta.current_page === 1"
            class="h-8 w-8 flex items-center justify-center rounded-lg text-sm text-gray-500 hover:bg-gray-100 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
            title="Primeira página"
        >«</button>

        <!-- Previous Page -->
        <button
            @click="goToPage(meta.current_page - 1)"
            :disabled="meta.current_page === 1"
            class="h-8 w-8 flex items-center justify-center rounded-lg text-sm text-gray-500 hover:bg-gray-100 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
            title="Página anterior"
        >‹</button>

        <!-- Page Numbers -->
        <template v-for="p in visiblePages" :key="p">
          <span v-if="p === '...'" class="h-8 w-8 flex items-center justify-center text-sm text-gray-400">…</span>
          <button
              v-else
              @click="goToPage(p)"
              :class="[
              'h-8 w-8 flex items-center justify-center rounded-lg text-sm transition-colors font-medium',
              p === meta.current_page
                ? 'bg-green-700 text-white shadow-sm'
                : 'text-gray-600 hover:bg-gray-100'
            ]"
          >{{ p }}</button>
        </template>

        <!-- Next Page -->
        <button
            @click="goToPage(meta.current_page + 1)"
            :disabled="meta.current_page === meta.last_page"
            class="h-8 w-8 flex items-center justify-center rounded-lg text-sm text-gray-500 hover:bg-gray-100 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
            title="Próxima página"
        >›</button>

        <!-- Last Page -->
        <button
            @click="goToPage(meta.last_page)"
            :disabled="meta.current_page === meta.last_page"
            class="h-8 w-8 flex items-center justify-center rounded-lg text-sm text-gray-500 hover:bg-gray-100 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
            title="Última página"
        >»</button>
      </div>
    </div>

    <!-- MODAL OVERLAY -->
    <div v-if="isModalOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm" @click.self="closeModal">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-4xl max-h-[90vh] overflow-hidden flex flex-col">

        <!-- Modal Header -->
        <div class="p-6 border-b border-gray-100 flex justify-between items-center bg-white sticky top-0">
          <div>
            <h2 class="text-xl font-bold text-gray-900 line-clamp-2">{{ selectedContract?.objeto }}</h2>
            <p class="text-sm text-gray-500 mt-0.5">{{ formatDate(selectedContract?.data_publicacao) }}</p>
          </div>
          <button @click="closeModal" class="p-2 hover:bg-gray-100 rounded-full text-gray-400 ml-4 shrink-0">✕</button>
        </div>

        <!-- Modal Body -->
        <div class="p-6 overflow-y-auto bg-slate-50/50">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">

            <!-- Left Column -->
            <div class="space-y-4">
              <div class="bg-white border border-gray-200 p-4 rounded-xl">
                <p class="text-[10px] text-gray-400 uppercase font-bold mb-1">Valor Contratual</p>
                <p class="text-2xl font-bold text-green-700">{{ formatCurrency(selectedContract?.valor_contratual) }}</p>
              </div>

              <div class="bg-white border border-gray-200 p-4 rounded-xl space-y-3">
                <div>
                  <p class="text-[10px] text-gray-400 uppercase font-bold">Adjudicante</p>
                  <p class="text-sm font-medium text-gray-800 mt-0.5">{{ selectedContract?.adjudicante?.nome }}</p>
                </div>
                <div>
                  <p class="text-[10px] text-green-600 uppercase font-bold">Adjudicatário</p>
                  <div class="text-sm font-medium text-green-700 mt-0.5">
                    <span v-for="c in selectedContract?.concorrentes?.filter(x => x.adjudicatario === 1)" :key="c.id">
                      {{ c.entidade.nome }}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Right Column -->
            <div class="space-y-4">
              <div class="bg-white border border-gray-200 p-4 rounded-xl space-y-3">
                <div>
                  <p class="text-[10px] text-gray-400 uppercase font-bold">Tipo de Procedimento</p>
                  <p class="text-sm font-medium text-gray-800 mt-0.5">{{ selectedContract?.tipo_procedimento?.tipo }}</p>
                </div>
                <div>
                  <p class="text-[10px] text-gray-400 uppercase font-bold">Prazo de Execução</p>
                  <p class="text-sm font-medium text-gray-800 mt-0.5">{{ selectedContract?.prazo_execucao }} dias</p>
                </div>
              </div>

              <div class="bg-white border border-gray-200 p-4 rounded-xl">
                <p class="text-[10px] text-gray-400 uppercase font-bold mb-2">CPVs</p>
                <ul class="space-y-1">
                  <li v-for="c in selectedContract?.cpvs" :key="c.codigo" class="text-xs text-gray-600">
                    <strong>{{ c.codigo }}</strong>: {{ c.cpv_descricao }}
                  </li>
                </ul>
              </div>

              <div class="flex justify-end pt-1">
                <Button variant="outline" size="sm" @click="goToDetails(selectedContract.chave_contratos)">
                  Página Completa →
                </Button>
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, reactive } from "vue"
import { useRouter } from "vue-router"
import { useAPIStore } from "@/store/api.js"
import { Button } from "@/components/ui/button/index.ts"

const router = useRouter()
const apiStore = useAPIStore()

// List state
const contracts = ref([])
const meta = ref(null)
const loading = ref(true)
const listTipoContratos = ref([])
const listTipoProcedimento = ref([])

// Modal state
const isModalOpen = ref(false)
const selectedContract = ref(null)

const filters = reactive({
  tipo_contrato: null,
  tipo_procedimento: null,
  data_publicacao_inicio: '',
  data_publicacao_fim: '',
  valor_contratual: null,
  prazo_execucao: null,
  cpvs: '',
  contrato_ecologico: null,
  procedimento_centralizado: null
})

const fetchContracts = async (pageNumber = 1) => {
  loading.value = true
  try {
    const queryParams = Object.fromEntries(
        Object.entries(filters).filter(([_, v]) => v !== '' && v !== null)
    )
    const response = await apiStore.getListContracts({ page: pageNumber, ...queryParams })
    contracts.value = response.data.data
    meta.value = response.data.meta
  } catch (err) {
    console.error("Falha ao carregar dados:", err)
  } finally {
    loading.value = false
  }
}

const goToPage = (page) => {
  if (page < 1 || page > meta.value.last_page) return
  window.scrollTo({ top: 0, behavior: 'smooth' })
  fetchContracts(page)
}

const visiblePages = computed(() => {
  if (!meta.value) return []
  const { current_page: current, last_page: last } = meta.value
  const delta = 1
  const range = []
  for (let i = Math.max(2, current - delta); i <= Math.min(last - 1, current + delta); i++) {
    range.push(i)
  }
  const pages = [1]
  if (range[0] > 2) pages.push('...')
  pages.push(...range)
  if (range[range.length - 1] < last - 1) pages.push('...')
  if (last > 1) pages.push(last)
  return pages
})

const openModal = (contract) => {
  selectedContract.value = contract
  isModalOpen.value = true
}

const closeModal = () => {
  isModalOpen.value = false
  selectedContract.value = null
}

const resetFilters = () => {
  Object.keys(filters).forEach(key => filters[key] = (key.includes('data') || key === 'cpvs') ? '' : null)
  fetchContracts(1)
}

const goToDetails = (id) => {
  router.push(`/contracts/${id}`)
}

const formatCurrency = (v) => new Intl.NumberFormat("pt-PT", { style: "currency", currency: "EUR" }).format(v)
const formatDate = (date) => new Date(date).toLocaleDateString('pt-PT')

onMounted(async () => {
  fetchContracts()
  const res = await apiStore.getFilterListContracts()
  listTipoContratos.value = res.data.TipoContrato
  listTipoProcedimento.value = res.data.TipoProcedimento
})
</script>