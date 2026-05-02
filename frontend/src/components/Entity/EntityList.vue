<template>
  <div class="container max-w-5xl mx-auto px-4 py-8">
    <!-- Header -->
    <div class="mb-6">
      <h1 class="text-2xl font-medium text-gray-900">Entidades</h1>
      <p v-if="meta" class="text-sm text-gray-400 mt-1">{{ meta.total }} resultados</p>
    </div>

    <!-- Loading State -->
    <p v-if="loading" class="text-gray-400 text-sm italic">A carregar entidades...</p>

    <!-- Entity Grid/List -->
    <div v-else class="flex flex-col gap-3">
      <div
          v-for="entity in entities"
          :key="entity.id_entidade"
          class="bg-white border border-gray-100 rounded-xl p-5 hover:border-blue-200 transition-colors shadow-sm"
      >
        <div class="flex justify-between items-start gap-4">
          <!-- Info Section -->
          <div class="flex-1 min-w-0">
            <div class="flex items-center gap-2 mb-1">
               <span class="text-[10px] font-mono bg-slate-100 text-slate-500 px-1.5 py-0.5 rounded">
                 NIF: {{ entity.nif }}
               </span>
              <span class="text-[10px] font-medium uppercase text-blue-600 bg-blue-50 px-1.5 py-0.5 rounded">
                 {{ entity.pais }}
               </span>
            </div>
            <h2 class="text-lg font-semibold text-gray-900 line-clamp-1">
              {{ entity.nome }}
            </h2>
          </div>

          <!-- Quick Action -->
          <Button
              variant="outline"
              size="sm"
              class="text-xs h-8 px-4"
              @click="goToEntityDetails(entity.id_entidade)"
          >
            Ver perfil →
          </Button>
        </div>

        <!-- Stats Grid -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 border-t border-gray-100 pt-4 mt-4">
          <div>
            <p class="text-[11px] uppercase tracking-wide text-gray-400 mb-1">Como Adjudicante</p>
            <p class="text-sm font-bold text-gray-800">
              {{ entity.num_contratos_adjudicante }} <span class="font-normal text-gray-500">contratos</span>
            </p>
          </div>
          <div>
            <p class="text-[11px] uppercase tracking-wide text-gray-400 mb-1">Como Adjudicatário</p>
            <p class="text-sm font-bold text-green-700">
              {{ entity.num_contratos_adjudicatario }} <span class="font-normal text-gray-500">contratos</span>
            </p>
          </div>
        </div>
      </div>
    </div>

    <!-- Pagination -->
    <div class="flex justify-center items-center gap-2 mt-6">
      <button class="px-4 py-1 rounded-md border border-gray-300 bg-white text-gray-700 hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed" @click="changePage(meta.current_page - 1)" :disabled="meta.current_page === 1">‹ Anterior</button>
      <span class="px-3 py-1 font-medium text-gray-800">Página {{ meta.current_page }} de {{ meta.last_page }}</span>
      <button class="px-4 py-1 rounded-md border border-gray-300 bg-white text-gray-700 hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed" @click="changePage(meta.current_page + 1)" :disabled="meta.current_page === meta.last_page">Próximo ›</button>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import { useAPIStore } from "@/store/api.js"
import { Button } from "@/components/ui/button"

const router = useRouter()
const apiStore = useAPIStore()

const entities = ref([])
const meta = ref(null)
const loading = ref(true)
const currentPage = ref(1)

const fetchEntities = async () => {
  loading.value = true
  try {
    const response = await apiStore.getListEntity()
    entities.value = response.data.data
    meta.value = response.data.meta
  } catch (err) {
    console.error("Erro ao carregar entidades:", err)
  } finally {
    loading.value = false
  }
}

const changePage = (page) => {
  if (page >= 1 && page <= meta.last_page) {
    apiStore.getListEntity(page)
  }
}

const goToEntityDetails = (id) => {
  router.push(`/entidades/${id}`)
}

onMounted(() => fetchEntities())
</script>