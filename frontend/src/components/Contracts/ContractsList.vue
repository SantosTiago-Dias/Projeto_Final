<template>
  <div class="container max-w-5xl mx-auto px-4 py-8">

    <div class="mb-8">
      <h1 class="text-2xl font-medium text-gray-900">Contratos</h1>
      <p class="text-sm text-gray-400 mt-1">{{ page.total || 0 }} resultados encontrados</p>
    </div>

    <!-- Filtros -->
    <div class="bg-white border border-gray-200 rounded-xl p-6 mb-8 shadow-sm">
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
          <input type="text" v-model="filters.cpvs" class="w-full text-sm border-gray-300 rounded-lg focus:ring-green-500" placeholder="Insira uma palavra sobre o tema que quer procurar" />
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

    <!-- Lista de Contratos -->
    <div v-if="loading" class="text-center py-10 text-gray-400">A carregar...</div>

    <div v-else class="flex flex-col gap-4">
      <div
          v-for="contract in contracts"
          :key="contract.chave_contratos"
          class="bg-white border border-gray-100 rounded-xl overflow-hidden transition-all duration-300"
          :class="{'ring-2 ring-green-500 shadow-lg': contract._isOpen}"
      >
        <!-- Header do Card -->
        <div
            class="p-5 cursor-pointer flex justify-between items-start gap-4 hover:bg-gray-50 transition"
            @click="toggleContract(contract)"
        >
          <div class="flex-1">
            <h2 class="text-[15px] font-medium text-gray-900 leading-snug">
              {{ contract.objeto }}
            </h2>
            <div class="flex gap-2 mt-2">
              <span class="text-[10px] px-2 py-0.5 rounded bg-blue-50 text-blue-700 border border-blue-100 uppercase font-bold">
                {{ contract.tipo_procedimento.tipo }}
              </span>
            </div>
          </div>
          <div class="text-right shrink-0">
            <p class="text-[16px] font-bold text-green-700">{{ formatCurrency(contract.valor_contratual) }}</p>
            <p class="text-[10px] text-gray-400 uppercase mt-1">{{ contract._isOpen ? 'Fechar ▲' : 'Abrir ▼' }}</p>
          </div>
        </div>

        <!-- Conteúdo Expansível -->
        <div v-show="contract._isOpen" class="px-5 pb-5 pt-2 border-t border-gray-50 bg-gray-50/50">
          <div class="grid grid-cols-1 md:grid-cols-2 gap-6">

            <div class="space-y-3">
              <div>
                <p class="text-[11px] uppercase tracking-wide text-gray-400">Adjudicante</p>
                <p class="text-sm font-medium text-gray-800">{{ contract.adjudicante.nome }}</p>
              </div>
              <div>
                <p class="text-[11px] uppercase tracking-wide text-gray-400">Adjudicatário</p>
                <div class="text-sm font-medium text-green-700">
                  <span v-for="c in contract.concorrentes.filter(x => x.adjudicatario === 1)" :key="c.id">
                    {{ c.entidade.nome }}
                  </span>
                </div>
              </div>
            </div>

            <div class="space-y-3">
              <div>
                <p class="text-[11px] uppercase tracking-wide text-gray-400">Detalhes Adicionais</p>
                <ul class="text-xs space-y-1 text-gray-600 mt-1">
                  <li><strong>Prazo de Execução:</strong> {{ contract.prazo_execucao }} dias</li>
                  <li><strong>Data Publicação:</strong> {{ contract.data_publicacao }}</li>
                </ul>
              </div>
              <div>
                <p class="text-[11px] uppercase tracking-wide text-gray-400">CPVs</p>
                <ul class="text-xs space-y-1 text-gray-600 mt-1" v-for="c in contract.cpvs" :key="c.codigo">
                  <li class="relative group cursor-default">
                    <strong>{{ c.codigo }}</strong>: {{ c.cpv_descricao }}
                    <span class="absolute bottom-full left-0 mb-1 hidden group-hover:block bg-gray-800 text-white text-xs rounded px-2 py-1 z-10 max-w-xs">
                      {{ c.descricao }}
                    </span>
                  </li>
                </ul>
              </div>
              <div class="flex justify-end gap-2 pt-2">
                <Button variant="outline" size="sm" @click.stop="goToDetails(contract.chave_contratos)">
                  Página Completa →
                </Button>
              </div>
            </div>

          </div>
        </div>
      </div>
    </div>

    <!-- Paginação -->
    <div class="flex justify-center items-center gap-2 mt-8">
      <button class="px-3 py-1 border rounded disabled:opacity-50"
              @click="fetchContracts(page.current_page - 1)"
              :disabled="page.current_page === 1">‹ Anterior</button>
      <span class="text-sm font-medium">Página {{ page.current_page }} de {{ page.last_page }}</span>
      <button class="px-3 py-1 border rounded disabled:opacity-50"
              @click="fetchContracts(page.current_page + 1)"
              :disabled="page.current_page === page.last_page">Próximo ›</button>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from "vue"
import { useRouter } from "vue-router"
import { useAPIStore } from "@/store/api.js"
import { Button } from "@/components/ui/button/index.ts"

const router = useRouter()
const apiStore = useAPIStore()

const contracts = ref([])
const page = ref({ current_page: 1, last_page: 1 })
const loading = ref(true)
const listTipoContratos = ref([])
const listTipoProcedimento = ref([])

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

    contracts.value = response.data.data.map(item => ({
      ...item,
      _isOpen: false
    }))

    page.value = response.data.meta
  } catch (err) {
    console.error("Falha ao carregar dados:", err)
  } finally {
    loading.value = false
  }
}

const toggleContract = (contract) => {
  contract._isOpen = !contract._isOpen
}

const resetFilters = () => {
  Object.keys(filters).forEach(key => filters[key] = (key.includes('data') || key === 'cpvs') ? '' : null)
  fetchContracts(1)
}

onMounted(async () => {
  fetchContracts()

  let res = await apiStore.getFilterListContracts()
  listTipoContratos.value = res.data.TipoContrato
  listTipoProcedimento.value = res.data.TipoProcedimento
})

function formatCurrency(v) {
  return new Intl.NumberFormat("pt-PT", { style: "currency", currency: "EUR" }).format(v)
}

function goToDetails(id) {
  router.push(`/contracts/${id}`)
}
</script>