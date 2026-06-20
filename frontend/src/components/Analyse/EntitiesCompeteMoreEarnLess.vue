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

const entities = ref([])
const loading = ref(true)

function goToEntity(item) {
  router.push(`/entidades/${item.chave_entidade}`)
}

const formatPercent = (v) => {
  if (v === null || v === undefined) return "0%"
  return `${Number(v).toFixed(2)}%`
}

onMounted(async () => {
  try {
    const response = await apiStore.getAnalyticsEntitiesCompeteMoreEarnLess()
    entities.value = response.data
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="p-6">
    <Card>
      <CardHeader>
        <CardTitle>
          Entidades que mais tentam e menos ganham
        </CardTitle>

        <CardDescription>
          Entidades com maior esforço em concursos mas menor taxa de sucesso.
        </CardDescription>
      </CardHeader>

      <Separator />

      <CardContent class="pt-6">
        <AnalyticsTable
            :items="entities"
            :columns="[
            { key: 'nome', label: 'Entidade' },
            { key: 'concursos', label: 'Concursos', class: 'text-right', cellClass: 'text-right font-semibold' },
            { key: 'taxa', label: 'Taxa de vitória', class: 'text-right', cellClass: 'text-right font-semibold text-red-600' }
          ]"
            rowKey="chave_entidade"
            :loading="loading"
            :onRowClick="goToEntity"
        >
          <template #concursos="{ item }">
            {{ item.total_concursos }}
          </template>

          <template #taxa="{ item }">
            {{ formatPercent(item.taxa_vitoria) }}
          </template>
        </AnalyticsTable>
      </CardContent>
    </Card>
  </div>
</template>