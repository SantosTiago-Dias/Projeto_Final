<template>
  <div class="container max-w-5xl mx-auto px-4 py-8">
    <!-- Header stays the same -->
    <div class="mb-6">
      <h1 class="text-2xl font-medium text-gray-900">Entidades</h1>
      <p v-if="meta" class="text-sm text-gray-400 mt-1">{{ meta.total }} resultados</p>
    </div>

    <!-- Loading State -->
    <p v-if="loading" class="text-gray-400 text-sm italic">A carregar entidades...</p>

    <!-- Entity Grid -->
    <div v-else class="flex flex-col gap-3">
      <div
          v-for="entity in entities"
          :key="entity.id_entidade"
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
          <Button variant="outline" size="sm" class="text-xs h-8 px-4">Ver Detalhes</Button>
        </div>
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
            <h3 class="font-semibold text-gray-800 mb-3">Lista de Contratos</h3>
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
import { ref, onMounted } from "vue"
import { useAPIStore } from "@/store/api.js"
import { Button } from "@/components/ui/button"
import router from "@/router/index.js";
import {useRoute} from "vue-router";

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
const entityDetails = ref([])

const fetchEntities = async () => {
  loading.value = true
  try {
    const response = await apiStore.getListEntity()
    entities.value = response.data.data
    meta.value = response.data.meta

  } catch (err) { console.error(err) }
  finally { loading.value = false }
}

const openModal = async (entity) => {
  selectedEntity.value = entity
  isModalOpen.value = true
  loadingDetails.value = true
  console.log(entity)
  try {
    // We use the ID from the clicked entity to fetch its specific contracts
    const [ resEntityDetails,resEntityContracts] = await Promise.all([
        apiStore.getDetailEntity(entity.id_entidade),
        apiStore.getListContractofEntity(entity.id_entidade)
    ])
    entityDetails.value = resEntityDetails.data
    entityContracts.value = resEntityContracts.data.data
  } catch (err) {
    console.error("Erro ao carregar contratos:", err)
  } finally {
    loadingDetails.value = false
  }
}

const closeModal = () => {
  isModalOpen.value = false
  selectedEntity.value = null
  entityContracts.value = []
}

const goToContract = (id) => {
  router.push(`/contracts/${id}`)
}

// Helpers
const formatPrice = (val) => new Intl.NumberFormat('pt-PT', { style: 'currency', currency: 'EUR' }).format(val)
const formatDate = (date) => new Date(date).toLocaleDateString('pt-PT')

onMounted(() => fetchEntities())
</script>