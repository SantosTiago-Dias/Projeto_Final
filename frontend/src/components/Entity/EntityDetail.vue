<template>
  <div class="container max-w-5xl py-10 px-4 md:px-0 mx-auto space-y-8">

    <Button @click="$router.back()" variant="ghost" class="flex items-center gap-2 hover:bg-slate-100 -ml-2 text-slate-600 transition-colors">
      <ArrowLeft class="h-4 w-4" />
      <span>Voltar atrás</span>
    </Button>

    <div v-if="loading" class="flex flex-col items-center justify-center py-20 space-y-4">
      <Loader2 class="h-8 w-8 animate-spin text-primary" />
      <p class="text-sm font-medium text-slate-500 tracking-wide animate-pulse">A carregar detalhes da entidade...</p>
    </div>

    <div v-else-if="!entidade" class="flex flex-col items-center justify-center text-center py-16 px-4 bg-white border border-dashed border-slate-200 rounded-2xl shadow-sm transition-all duration-300">
      <div class="p-4 bg-amber-50 rounded-full text-amber-500 mb-4">
        <Building2 class="h-8 w-8" />
      </div>
      <h3 class="text-lg font-semibold text-slate-900">Entidade não encontrada</h3>
    </div>

    <template v-else>
      <header class="space-y-4">
        <div class="flex items-center gap-2">
          <Badge variant="outline" class="uppercase tracking-wider">
            Entidade
          </Badge>
          <Badge v-if="entidade.num_contratos_adjudicante > 0" variant="secondary">
            Adjudicante
          </Badge>
          <Badge v-if="entidade.num_contratos_adjudicatario > 0">
            Adjudicatário
          </Badge>
        </div>

        <h1 class="text-3xl font-extrabold tracking-tight lg:text-4xl text-slate-900 leading-tight">
          {{ entidade.nome }}
        </h1>

        <p class="text-muted-foreground flex items-center gap-2 text-sm">
          <Hash class="h-4 w-4 text-slate-400" />
          <span class="font-medium">NIPC:</span> {{ entidade.nif }}
        </p>
      </header>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
        <Card class="bg-primary/5 border-none shadow-none">
          <CardHeader class="pb-2">
            <CardDescription class="flex items-center gap-2">
              <Euro class="h-4 w-4" /> Total Adjudicado
            </CardDescription>
            <CardTitle class="text-2xl text-primary">
              {{ formatCurrency(entidade.total_adjudicatario) }}
            </CardTitle>
          </CardHeader>
        </Card>

        <Card class="shadow-sm">
          <CardHeader class="pb-2">
            <CardDescription class="flex items-center gap-2">
              <Landmark class="h-4 w-4" /> Total como Adjudicante
            </CardDescription>
            <CardTitle class="text-2xl">
              {{ formatCurrency(entidade.total_adjudicante) }}
            </CardTitle>
          </CardHeader>
        </Card>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">

        <div class="lg:col-span-2 space-y-8">
          <Card class="shadow-sm">
            <CardHeader>
              <CardTitle class="text-lg flex items-center gap-2">
                <MapPinned class="h-5 w-5 text-muted-foreground" />
                Localização
              </CardTitle>
            </CardHeader>
            <CardContent class="space-y-4">
              <div>
                <span class="font-medium block mb-1 text-xs text-slate-400 uppercase tracking-wider">País</span>
                <p class="text-slate-700 font-medium">
                  {{ entidade.pais || 'N/A' }}
                </p>
              </div>
              <Separator />
              <div>
                <span class="font-medium block mb-1 text-xs text-slate-400 uppercase tracking-wider">Distrito</span>
                <p class="text-slate-700 font-medium">
                  {{ entity.distrito || 'N/A' }}
                </p>
              </div>
            </CardContent>
          </Card>

          <Card class="shadow-sm">
            <CardHeader>
              <CardTitle class="text-lg flex items-center gap-2">
                <FileText class="h-5 w-5 text-muted-foreground" />
                Lista de Contratos
              </CardTitle>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Título do contrato</TableHead>
                    <TableHead class="text-right">Valor</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  <TableRow
                      v-for="contract in entityContracts"
                      :key="contract.chave_contratos"
                      class="cursor-pointer hover:bg-muted/50"
                      @click="goToContract(contract.chave_contratos)"
                  >
                    <TableCell>
                      <p class="font-medium text-slate-900 line-clamp-1">
                        {{ contract.objeto ?? 'Sem título' }}
                      </p>
                      <p class="text-xs text-muted-foreground mt-0.5">
                        {{ formatDate(contract.data_publicacao) }}
                      </p>
                    </TableCell>
                    <TableCell class="text-right font-bold text-slate-900">
                      {{ formatCurrency(contract.valor_contratual) }}
                    </TableCell>
                  </TableRow>
                </TableBody>
              </Table>

              <div v-if="entityContracts.length === 0" class="flex flex-col items-center justify-center py-8 text-center text-muted-foreground">
                <FileX class="h-8 w-8 text-slate-300 mb-2" />
                <p class="text-sm">Sem contratos registados.</p>
              </div>
            </CardContent>
          </Card>
        </div>

        <div class="space-y-6">
          <Card class="shadow-sm">
            <CardHeader class="pb-3">
              <CardTitle class="text-sm font-bold uppercase text-muted-foreground tracking-wider">
                Resumo
              </CardTitle>
            </CardHeader>
            <CardContent class="space-y-4 text-sm">
              <div class="flex items-center justify-between">
                <span class="text-slate-600">Total Contratos Adjudicante</span>
                <Badge variant="outline">
                  {{ entidade.num_contratos_adjudicante }}
                </Badge>
              </div>
              <div class="flex items-center justify-between">
                <span class="text-slate-600">Total Contratos Adjudicatário</span>
                <Badge variant="outline">
                  {{ entidade.num_contratos_adjudicatario }}
                </Badge>
              </div>

              <Separator />

              <div class="flex items-center justify-between pt-1">
                <span class="font-semibold text-slate-900">Total Movimentado</span>
                <span class="font-bold text-primary text-base">
                  {{
                    formatCurrency(
                        Number(entidade.total_adjudicante || 0) +
                        Number(entidade.total_adjudicatario || 0)
                    )
                  }}
                </span>
              </div>
            </CardContent>
          </Card>
        </div>

      </div>
    </template>
  </div>
</template>
<script setup>
import { onMounted, ref } from "vue"
import { useAPIStore } from "@/store/api.js"
import { useRoute } from "vue-router"

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle
} from "@/components/ui/card/index.ts"

import { Badge } from "@/components/ui/badge/index.ts"
import { Separator } from "@/components/ui/separator/index.ts"
import { Button } from "@/components/ui/button/index.ts"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table/index.ts"
import {
  ArrowLeft,
  MapPinned,
  FileText,
  Euro,
  Hash,
  Landmark,
  Loader2,
  FileX,
  Building2,
  AlertCircle
} from "lucide-vue-next"

const apiStore = useAPIStore()
const route = useRoute()

const entidade = ref(null)
const entityContracts = ref([])

const loading = ref(true)

const formatCurrency = (value) => {
  if (!value) return "---"

  return new Intl.NumberFormat("pt-PT", {
    style: "currency",
    currency: "EUR",
  }).format(Number(value))
}

const formatDate = (date) => {
  if (!date) return "---"

  return new Date(date).toLocaleDateString("pt-PT")
}

const goToContract = (id) => {
  window.location.href = `/contracts/${id}`
}

onMounted(async () => {
  try {
    const id = route.params.id

    const [entityRes, contractsRes] = await Promise.all([
      apiStore.getDetailEntity(id),
      apiStore.getListContractofEntity(id)
    ])

    entidade.value = entityRes.data
    entityContracts.value = contractsRes.data.data
  }
  catch (err) {
    console.error(err)
    entidade.value = null
  }
  finally {
    loading.value = false
  }
})
</script>