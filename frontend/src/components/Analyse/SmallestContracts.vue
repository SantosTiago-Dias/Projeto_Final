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

const router = useRouter()
const apiStore = useAPIStore()

const contracts = ref([])
const loading = ref(true)

const columns = [
  { key: "objeto", label: "Contrato" },
  { key: "valor", label: "Valor", class: "text-right", cellClass: "text-right font-semibold text-red-600" },
]

function goToContract(item) {
  router.push(`/contracts/${item.chave_contratos}`)
}

const formatCurrency = (v) =>
    new Intl.NumberFormat("pt-PT", {
      style: "currency",
      currency: "EUR",
    }).format(v)

onMounted(async () => {
  const res = await apiStore.getSmallestContracts()
  contracts.value = res.data
  loading.value = false
})
</script>

<template>
  <div class="p-6">
    <Card>
      <CardHeader>
        <CardTitle>Contratos de Menor Valor</CardTitle>
        <CardDescription>Contratos com menor valor adjudicado</CardDescription>
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
            <span class="block truncate max-w-[500px]">
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