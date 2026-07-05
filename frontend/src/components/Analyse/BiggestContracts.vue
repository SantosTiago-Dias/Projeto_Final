<template>
  <div class="p-6">
    <Card>
      <CardHeader>
        <CardTitle>Maiores Contratos</CardTitle>
        <CardDescription>Contratos com maior valor adjudicado</CardDescription>
      </CardHeader>

      <Separator />

      <CardContent class="pt-6">
        <AnalyticsTable
            :items="contracts"
            :columns="columns"
            rowKey="chave_contratos"
            :loading="loading"
            :onRowClick="goToContract"
        >
          <template #objeto="{ item }">
            <span class="block truncate max-w-125">
              {{ item.objeto }}
            </span>
          </template>

          <template #valor="{ item }">
            {{ formatCurrency(item.valor_contratual) }}
          </template>
        </AnalyticsTable>
      </CardContent>
    </Card>
  </div>
</template>

<script setup>
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import { useAPIStore } from "@/store/api"

import AnalyticsTable from "@/components/Analyse/AnalyticsTable.vue"

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

import { Separator } from "@/components/ui/separator"
import {toast} from "vue-sonner";

const router = useRouter()
const apiStore = useAPIStore()

const contracts = ref([])
const loading = ref(true)

const columns = [
  { key: "objeto", label: "Contrato" },
  { key: "valor", label: "Valor", class: "text-right", cellClass: "text-right font-semibold text-green-600" },
]

const formatCurrency = (v) =>
    new Intl.NumberFormat("pt-PT", {
      style: "currency",
      currency: "EUR",
    }).format(v)

function goToContract(item) {
  router.push(`/contracts/${item.chave_contratos}`)
}

onMounted(async () => {
  try {
    const res = await apiStore.getAnalyticsBiggestContracts()
    contracts.value = res.data
  }
  catch (error) {
    toast.error("Ocorreu um erro, não foi possivel carregar os dados")
  }
  finally {
    loading.value = false
  }

})
</script>