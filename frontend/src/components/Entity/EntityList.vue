<template>
  <div class="container max-w-5xl mx-auto px-4 py-8">
    <!-- Header stays the same -->
    <div class="mb-6">
      <h1 class="text-2xl font-medium text-gray-900">Entidades</h1>
    </div>
    <!-- Entity Grid -->
    <div class="flex flex-col gap-3">

      <!-- Filtros -->
      <div class="bg-white border border-gray-200 rounded-xl p-4 mb-6 shadow-sm">

        <div class="grid grid-cols-[repeat(auto-fit,minmax(220px,1fr))] gap-3">

          <!-- Nome -->
          <div>
            <label class="block text-[11px] font-medium text-gray-500 mb-1 uppercase">
              Nome
            </label>

            <input
                type="text"
                v-model="filters.nome"
                placeholder="Pesquisar nome..."
                class="w-full h-9 text-sm border-gray-300 rounded-lg"
            />
          </div>

          <!-- NIF -->
          <div>
            <label class="block text-[11px] font-medium text-gray-500 mb-1 uppercase">
              NIF
            </label>

            <input
                type="text"
                v-model="filters.nif"
                placeholder="Pesquisar NIF..."
                class="w-full h-9 text-sm border-gray-300 rounded-lg"
            />
          </div>

          <!-- Tipo Entidade -->
          <div>
            <label class="block text-[11px] font-medium text-gray-500 mb-1 uppercase">
              Tipo Entidade
            </label>

            <select
                v-model="filters.tipo_entidade"
                class="w-full h-9 text-sm border-gray-300 rounded-lg"
            >
              <option value="">Todos</option>
              <option value="3">Não Residente</option>
              <option value="5">Pessoa Coletiva</option>
              <option value="6">Administração Pública</option>
              <option value="7">Herança Indivisa</option>
              <option value="8">Empresário Nome Individual</option>
              <option value="9">Pessoa Coletiva Irregular</option>
            </select>
          </div>

          <!-- País -->
          <div>
            <label class="block text-[11px] font-medium text-gray-500 mb-1 uppercase">
              Localização
            </label>

            <input
                type="text"
                v-model="filters.pais"
                placeholder="Pesquisar localização..."
                class="w-full h-9 text-sm border-gray-300 rounded-lg"
            />
          </div>


          <!-- Nº Contratos Adjudicatário Min -->
          <div>
            <label class="block text-[11px] font-medium text-gray-500 mb-1 uppercase" title="Número mínimo de contratos ganhos por entidade">
              Nº mín. contratos (adjudicatário)
            </label>

            <input
                type="number"
                min="0"
                v-model="filters.num_contratos_adjudicatario_min"
                class="w-full h-9 text-sm border-black-300 rounded-lg"
            />
          </div>

          <!-- Nº Contratos Adjudicatário Max -->
          <div>
            <label class="block text-[11px] font-medium text-gray-500 mb-1 uppercase" title="Número máximo de contratos ganhos por entidade">
              Nº máx. contratos (adjudicatário)
            </label>

            <input
                type="number"
                min="0"
                v-model="filters.num_contratos_adjudicatario_max"
                class="w-full h-9 text-sm border-black-300 rounded-lg"
            />
          </div>

          <!-- Nº Contratos Adjudicante Min -->
          <div>
            <label class="block text-[11px] font-medium text-gray-500 mb-1 uppercase" title="Número mínimo de contratos lançados por entidade">
              Nº mín. contratos (adjudicatário)
            </label>

            <input
                type="number"
                min="0"
                v-model="filters.num_contratos_adjudicante_min"
                class="w-full h-9 text-sm border-black-300 rounded-lg"
            />
          </div>

          <!-- Nº Contratos Adjudicante Max -->
          <div>
            <label class="block text-[11px] font-medium text-gray-500 mb-1 uppercase" title="Número máximo de contratos lançados por entidade">
              Nº máx. contratos (adjudicatário)
            </label>

            <input
                type="number"
                min="0"
                v-model="filters.num_contratos_adjudicante_max"
                class="w-full h-9 text-sm border-black-300 rounded-lg"
            />
          </div>

          <!-- Botões -->
          <div class="flex items-end gap-2">

            <button
                @click="fetchEntities()"
                class="flex-1 h-9 bg-green-700 text-white text-sm rounded-lg font-medium hover:bg-green-800 transition"
            >
              Filtrar
            </button>

            <button
                @click="resetFilters"
                class="h-9 px-3 text-sm text-gray-500 hover:text-gray-700"
            >
              Limpar
            </button>

          </div>

        </div>
      </div>


      <!-- Loading State -->
      <p v-if="loading" class="text-gray-400 text-sm italic">A carregar entidades...</p>

      <div v-else-if="entities === undefined || entities === null" class="flex flex-col items-center justify-center p-8 bg-white border border-gray-100 rounded-xl transition-all duration-300">
        <p class="text-sm font-medium text-gray-500">Não existem entidades ainda</p>
      </div>

      <div v-else class="contratos-summary" style="margin: 20px 0; font-family: sans-serif; color: #333;">
        <span>A mostrar <strong>{{entities.length}}</strong> de <strong>{{meta.total}}</strong> entidades encontradas</span>
      </div>
      <div
          v-for="entity in entities"
          :key="entity.chave_entidade"
          class="bg-white border border-gray-100 rounded-xl p-5 hover:border-blue-200 transition-colors shadow-sm cursor-pointer"
          @click="openModal(entity)"
      >
        <div class="flex justify-between items-start gap-4">
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 mb-1">
              <span class="text-[10px] font-mono bg-slate-100 text-slate-500 px-1.5 py-0.5 rounded">NIF: {{ entity.nif }}</span>
              <span class="text-[10px] font-medium uppercase text-blue-600 bg-blue-50 px-1.5 py-0.5 rounded">{{ entity.pais }}</span>
            </div>
            <h2 class="text-lg font-semibold text-gray-900 line-clamp-1">{{ entity.nome }}</h2>
          </div>
          <Button variant="outline" size="sm" class="text-xs h-8 px-4" @click.stop="goToDetails(entity.chave_entidade)">Ver Detalhes</Button>
        </div>
      </div>
    </div>

    <!-- PAGINATION -->
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
        >
          «
        </button>

        <!-- Previous Page -->
        <button
            @click="goToPage(meta.current_page - 1)"
            :disabled="meta.current_page === 1"
            class="h-8 w-8 flex items-center justify-center rounded-lg text-sm text-gray-500 hover:bg-gray-100 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
            title="Página anterior"
        >
          ‹
        </button>

        <!-- Page Number Buttons -->
        <template v-for="page in visiblePages" :key="page">
          <span v-if="page === '...'" class="h-8 w-8 flex items-center justify-center text-sm text-gray-400">…</span>
          <button
              v-else
              @click="goToPage(page)"
              :class="[
              'h-8 w-8 flex items-center justify-center rounded-lg text-sm transition-colors font-medium',
              page === meta.current_page
                ? 'bg-blue-600 text-white shadow-sm'
                : 'text-gray-600 hover:bg-gray-100'
            ]"
          >
            {{ page }}
          </button>
        </template>

        <!-- Next Page -->
        <button
            @click="goToPage(meta.current_page + 1)"
            :disabled="meta.current_page === meta.last_page"
            class="h-8 w-8 flex items-center justify-center rounded-lg text-sm text-gray-500 hover:bg-gray-100 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
            title="Próxima página"
        >
          ›
        </button>

        <!-- Last Page -->
        <button
            @click="goToPage(meta.last_page)"
            :disabled="meta.current_page === meta.last_page"
            class="h-8 w-8 flex items-center justify-center rounded-lg text-sm text-gray-500 hover:bg-gray-100 disabled:opacity-30 disabled:cursor-not-allowed transition-colors"
            title="Última página"
        >
          »
        </button>
      </div>
    </div>

    <!-- MODAL OVERLAY -->
    <div v-if="isModalOpen" class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/50 backdrop-blur-sm" @click.self="closeModal">
      <div class="bg-white rounded-2xl shadow-2xl w-full max-w-4xl max-h-[90vh] overflow-hidden flex flex-col">

        <!-- Modal Header -->
        <div class="p-6 border-b border-gray-100 flex justify-between items-center bg-white sticky top-0">
          <div>
            <h2 class="text-xl font-bold text-gray-900">{{ entityDetails?.nome }}</h2>
            <p class="text-sm text-gray-500">NIF: {{ entityDetails?.nif }}</p>
          </div>
          <button @click="closeModal" class="p-2 hover:bg-gray-100 rounded-full text-gray-400">✕</button>
        </div>

        <!-- Modal Body (Scrollable) -->
        <div class="p-6 overflow-y-auto bg-slate-50/50">
          <div v-if="loadingDetails" class="py-10 text-center text-gray-400 italic">A carregar contratos...</div>

          <div v-else>
            <!-- Stats Summary -->
            <div class="grid grid-cols-2 gap-4 mb-8">
              <div class="bg-white border border-gray-200 p-4 rounded-xl">
                <p class="text-[10px] text-gray-400 uppercase font-bold">Como Adjudicante</p>
                <p class="text-2xl font-bold text-slate-800">{{ entityDetails?.num_contratos_adjudicante }}</p>
              </div>
              <div class="bg-white border border-gray-200 p-4 rounded-xl">
                <p class="text-[10px] text-green-600 uppercase font-bold">Como Adjudicatário</p>
                <p class="text-2xl font-bold text-green-700">{{ entityDetails?.num_contratos_adjudicatario }}</p>
              </div>
            </div>

            <!-- Contracts Table -->
            <h3 class="font-semibold text-gray-800 mb-3">Lista de Contratos Recentes</h3>
            <div class="bg-white border border-gray-200 rounded-xl overflow-hidden shadow-sm">
              <table class="w-full text-left border-collapse">
                <thead class="bg-gray-50 border-b border-gray-200">
                <tr>
                  <th class="px-4 py-3 text-[10px] font-bold text-gray-400 uppercase">Titulo do contrato</th>
                  <th class="px-4 py-3 text-[10px] font-bold text-gray-400 uppercase text-right">Valor</th>
                </tr>
                </thead>
                <tbody class="divide-y divide-gray-100">
                <tr v-for="contract in entityContracts" :key="contract.id" class="hover:bg-blue-50/50" @click="goToContract(contract.chave_contratos)">
                  <td class="px-4 py-3">
                    <p class="text-sm font-medium text-gray-800 line-clamp-1">{{ contract.objeto ?? 'Sem título' }}</p>
                    <p class="text-[10px] text-gray-400">{{ formatDate(contract.data_publicacao) }}</p>
                  </td>
                  <td class="px-4 py-3 text-right text-sm font-bold text-gray-900">
                    {{ formatPrice(contract.valor_contratual) }}
                  </td>
                </tr>
                </tbody>
              </table>
              <div v-if="entityContracts.length === 0" class="p-8 text-center text-gray-400 text-sm">
                Sem contratos registados.
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import {ref, computed, onMounted, reactive} from "vue"
import { useAPIStore } from "@/store/api.js"
import { Button } from "@/components/ui/button"
import router from "@/router/index.js";
import { useRoute } from "vue-router";

const apiStore = useAPIStore()

// List State
const entities = ref([])
const meta = ref(null)
const loading = ref(true)
const route = useRoute()

// Modal State
const isModalOpen = ref(false)
const loadingDetails = ref(false)
const selectedEntity = ref(null)
const entityContracts = ref([])
const entityDetails = ref({})

const fetchEntities = async (page = 1) => {
  loading.value = true

  try {
    const queryParams = {}

    Object.entries(filters).forEach(([key, value]) => {
      if (value !== '' && value !== null && value !== undefined) {
        queryParams[key] = value
      }
    })
    
    const response = await apiStore.getListEntity({
      page,
      ...queryParams
    })

    entities.value = response.data.data
    meta.value = response.data.meta

  } catch (err) {
    console.error("Falha ao carregar entidades:", err)
    entities.value = null
  } finally {
    loading.value = false
  }
}

const goToPage = (page) => {
  if (page < 1 || page > meta.value.last_page) return
  window.scrollTo({ top: 0, behavior: 'smooth' })
  fetchEntities(page)
}

// Builds the visible page range with ellipsis, e.g. 1 … 4 5 6 … 20
const visiblePages = computed(() => {
  if (!meta.value) return []
  const { current_page: current, last_page: last } = meta.value
  const pages = []
  const delta = 1 // pages on each side of current

  const range = []
  for (let i = Math.max(2, current - delta); i <= Math.min(last - 1, current + delta); i++) {
    range.push(i)
  }

  pages.push(1)
  if (range[0] > 2) pages.push('...')
  pages.push(...range)
  if (range[range.length - 1] < last - 1) pages.push('...')
  if (last > 1) pages.push(last)

  return pages
})

const openModal = async (entity) => {
  selectedEntity.value = entity
  isModalOpen.value = true
  loadingDetails.value = true
  try {
    const [resEntityDetails, resEntityContracts] = await Promise.all([
      apiStore.getDetailEntity(entity.chave_entidade),
      apiStore.getListContractofEntity(entity.chave_entidade)
    ])

    entityDetails.value = resEntityDetails.data
    entityContracts.value = resEntityContracts.data.data
        .sort((a, b) => new Date(b.data_publicacao) - new Date(a.data_publicacao))
        .slice(0, 5)
  } catch (err) {
    console.error("Erro ao carregar entidades:", err)
  } finally {
    loadingDetails.value = false
  }
}

const closeModal = () => {
  isModalOpen.value = false
  selectedEntity.value = null
  entityContracts.value = []
}

const goToContract = (chave_contrato) => {
  router.push(`/contracts/${chave_contrato}`)
}

function goToDetails(id) {
  router.push(`/entidades/${id}`)
}

const filters = reactive( {
        nome: '',
        nif: '',
        tipo_entidade: '',
        pais: '',
        num_contratos_adjudicatario_min: null,
        num_contratos_adjudicatario_max: null,
        num_contratos_adjudicante_min: null,
        num_contratos_adjudicante_max: null,
}
)

const resetFilters = () => {
  Object.keys(filters).forEach(key => {
    if (typeof filters[key] === 'number') {
      filters[key] = null
    } else {
      filters[key] = ''
    }
  })

  fetchEntities(1)
}

// Helpers
const formatPrice = (val) => new Intl.NumberFormat('pt-PT', { style: 'currency', currency: 'EUR' }).format(val)
const formatDate = (date) => new Date(date).toLocaleDateString('pt-PT')

onMounted(() => fetchEntities())
</script>