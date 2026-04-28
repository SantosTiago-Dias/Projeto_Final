<script setup>
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"

import { Button } from "@/components/ui/button"

const router = useRouter()

const contracts = ref([])
const loading = ref(true)

function formatCurrency(value) {
  return new Intl.NumberFormat("pt-PT", {
    style: "currency",
    currency: "EUR",
  }).format(Number(value))
}

function goToDetails(id) {
  router.push(`/contracts/${id}`)
}

onMounted(async () => {
  try {
    const res = await fetch("http://localhost:8000/api/contracts")
    const data = await res.json()
    contracts.value = data.data
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="container max-w-7xl mx-auto space-y-6">

    <!-- HEADER -->
    <div class="flex items-center justify-between">
      <h1 class="text-2xl font-bold text-gray-900">Contratos</h1>

      <span class="text-sm text-gray-500">
        {{ contracts.length }} resultados
      </span>
    </div>

    <p v-if="loading" class="text-gray-500">
      A carregar...
    </p>

    <div v-else class="space-y-4">

      <div
        v-for="item in contracts"
        :key="item.contrato.chave_contratos"
        class="bg-white border rounded-xl shadow-sm hover:shadow-md transition p-5 space-y-4"
      >

        <div class="flex justify-between gap-4">

          <div class="space-y-1">
            <h2
              class="font-semibold text-gray-900 leading-snug line-clamp-2"
              :title="item.contrato.objeto"
            >
              {{ item.contrato.objeto }}
            </h2>

            <div class="text-xs text-gray-500">
              ID {{ item.contrato.id_contrato }}
            </div>
          </div>

          <div class="text-right">
            <div class="text-green-600 font-bold text-lg">
              {{ formatCurrency(item.contrato.valor_contratual) }}
            </div>
            <div class="text-xs text-gray-400">
              {{ item.contrato.data_publicacao }}
            </div>
          </div>

        </div>

        <div class="grid md:grid-cols-2 gap-4">

          <div>
            <div class="text-xs text-gray-400">Adjudicante</div>
            <div class="font-medium text-gray-800 line-clamp-2">
              {{ item.adjudicanteRel.nome }}
            </div>
          </div>

          <div>
            <div class="text-xs text-gray-400">Adjudicatário</div>
            <div class="font-medium text-green-700 line-clamp-2">
              {{ item.adjudicatario?.nome }}
            </div>
          </div>

        </div>

        <div class="flex flex-wrap gap-2">

          <span class="text-xs px-2 py-1 rounded bg-gray-100 text-gray-700" :title="item.tipo_contrato.descricao">
            {{ item.tipo_contrato.tipo }}
          </span>

          <span class="text-xs px-2 py-1 rounded bg-blue-50 text-blue-700" :title="item.tipo_procedimento.descricao">
            {{ item.tipo_procedimento.tipo }} 
          </span>

        </div>

        <div class="flex justify-end pt-2 border-t">

          <Button
            variant="outline"
            size="sm"
            class="h-8 px-4 text-xs"
            @click="goToDetails(item.contrato.chave_contratos)"
          >
            Ver detalhes
          </Button>

        </div>

      </div>

    </div>
  </div>
</template>