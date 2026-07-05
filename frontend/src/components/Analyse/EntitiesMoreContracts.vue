<template>
  <div class="p-6">
    <Card>
      <CardHeader>
        <CardTitle>Entidades que mais contratam</CardTitle>
        <CardDescription>Top entidades por número de contratos</CardDescription>
      </CardHeader>

      <Separator />

      <CardContent class="pt-6">
        <AnalyticsTable
            :items="entities"
            :columns="columns"
            rowKey="adjudicante"
            :loading="loading"
            :onRowClick="goToEntity"
        >
          <template #valor="{ item }">
            {{ formatCurrency(item.valor_adjudicado) }}
          </template>

          <template #numero="{ item }">
            {{ item.numero_contratos }}
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

const entities = ref([])
const loading = ref(true)

const columns = [
  { key: "nome", label: "Entidade" },
  { key: "numero", label: "Contratos", class: "text-right", cellClass: "text-right font-semibold" },
  { key: "valor", label: "Valor", class: "text-right", cellClass: "text-right font-semibold text-green-600" },
]

function goToEntity(item) {
  router.push(`/entidades/${item.adjudicante}`)
}

const formatCurrency = (v) =>
    new Intl.NumberFormat("pt-PT", {
      style: "currency",
      currency: "EUR",
    }).format(v)

onMounted(async () => {
  try
  {
    const res = await apiStore.getAnalyticsEntitiesMoreContractsAsContracting()
    entities.value = res.data
  }catch (error) {
    toast.error("Ocorreu um erro, não foi possivel carregar os dados")
  }
  finally {
    loading.value = false
  }
})
</script>