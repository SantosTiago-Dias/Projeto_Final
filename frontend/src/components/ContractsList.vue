<script setup>
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"

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
  <div class="container space-y-6">
    <h1 class="text-2xl font-bold">Contratos</h1>

    <p v-if="loading">A carregar...</p>

    <Table v-else class="w-full text-sm table-fixed">

      <TableHeader class="bg-gray-50 border-b">
        <TableRow>
          <TableHead class="w-[28%]">Objeto</TableHead>
          <TableHead class="w-[22%]">Adjudicante</TableHead>
          <TableHead class="w-[12%] text-center">Tipo Contrato</TableHead>
          <TableHead class="w-[15%] text-center">Tipo Procedimento</TableHead>
          <TableHead class="w-[10%] text-center">Data Assinatura</TableHead>
          <TableHead class="w-[8%] text-center">Valor</TableHead>
          <TableHead class="w-[5%] text-center"></TableHead>
        </TableRow>
      </TableHeader>

      <TableBody>
        <TableRow v-for="item in contracts" :key="item.contrato.chave_contratos"
          class="border-b hover:bg-gray-50 transition-colors">

          <TableCell class="px-2 py-2">
            <div class="truncate font-semibold text-gray-900" :title="item.contrato.objeto">
              {{ item.contrato.objeto }}
            </div>
          </TableCell>

          <TableCell class="px-2 py-2">
            <div class="whitespace-normal break-words leading-relaxed text-gray-700" :title="item.adjudicanteRel.nome">
              {{ item.adjudicanteRel.nome }}
            </div>
          </TableCell>

          <TableCell class="text-center px-2 py-2">
            <span class="truncate block text-xs bg-gray-100 px-2 py-1 rounded-md" :title="item.tipo_contrato.tipo">
              {{ item.tipo_contrato.tipo }}
            </span>
          </TableCell>

          <TableCell class="text-center px-2 py-2">
            <span class="truncate block text-xs bg-blue-50 text-blue-700 px-2 py-1 rounded-md"
              :title="item.tipo_procedimento.tipo">
              {{ item.tipo_procedimento.tipo }}
            </span>
          </TableCell>

          <TableCell class="text-center px-2 py-2 text-gray-600">
            <div class="truncate">
              {{ item.data.data }}
            </div>
          </TableCell>

          <TableCell class="text-center px-2 py-2 font-semibold text-green-600">
            {{ formatCurrency(item.contrato.valor_contratual) }}
          </TableCell>

          <TableCell class="text-center px-2 py-2">
            <Button variant="outline" size="sm" class="h-7 px-2 text-xs"
              @click="goToDetails(item.contrato.chave_contratos)">
              Detalhes
            </Button>
          </TableCell>

        </TableRow>
      </TableBody>

    </Table>
  </div>
</template>