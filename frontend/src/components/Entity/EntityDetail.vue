<template>

  <!-- LOADING -->
  <div
      v-if="loading"
      class="text-center py-10 text-gray-400"
  >
    A carregar...
  </div>

  <!-- ERROR -->
  <div
      v-else-if="error"
      class="text-center py-10 text-red-500"
  >
    {{ error }}
  </div>

  <!-- CONTENT -->
  <div
      v-else-if="entidade"
      class="container max-w-5xl py-10 px-4 md:px-0 mx-auto space-y-8"
  >

    <!-- BACK -->
    <Button>
      <button
          @click="$router.back()"
          class="flex items-center gap-1"
      >
        ← Voltar atrás
      </button>
    </Button>

    <!-- HEADER -->
    <header class="space-y-4">

      <div class="flex items-center gap-2">
        <Badge variant="outline">
          Entidade
        </Badge>

        <Badge
            v-if="entidade.num_contratos_adjudicante > 0"
            variant="secondary"
        >
          Adjudicante
        </Badge>

        <Badge
            v-if="entidade.num_contratos_adjudicatario > 0"
        >
          Adjudicatário
        </Badge>
      </div>

      <h1 class="text-3xl font-extrabold tracking-tight lg:text-4xl text-slate-900 leading-tight">
        {{ entidade.nome }}
      </h1>

      <p class="text-muted-foreground flex items-center gap-2">
        <Hash class="h-4 w-4" />
        NIF: {{ entidade.nif }}
      </p>

    </header>

    <!-- METRICAS -->
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">

      <Card class="bg-primary/5 border-none shadow-none">
        <CardHeader class="pb-2">
          <CardDescription class="flex items-center gap-2">
            <Euro class="h-4 w-4" />
            Total Adjudicado
          </CardDescription>

          <CardTitle class="text-2xl text-primary">
            {{ formatCurrency(entidade.total_adjudicatario) }}
          </CardTitle>
        </CardHeader>
      </Card>

      <Card class="shadow-sm">
        <CardHeader class="pb-2">
          <CardDescription class="flex items-center gap-2">
            <Landmark class="h-4 w-4" />
            Total como Adjudicante
          </CardDescription>

          <CardTitle class="text-2xl">
            {{ formatCurrency(entidade.total_adjudicante) }}
          </CardTitle>
        </CardHeader>
      </Card>

    </div>

    <!-- GRID -->
    <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">

      <!-- MAIN -->
      <div class="lg:col-span-2 space-y-8">

        <!-- LOCALIZACAO -->
        <Card>
          <CardHeader>
            <CardTitle class="text-lg flex items-center gap-2">
              <MapPinned class="h-5 w-5" />
              Localização
            </CardTitle>
          </CardHeader>

          <CardContent class="space-y-4">

            <div>
              <span class="font-medium block mb-1">
                País
              </span>

              <p class="text-muted-foreground">
                {{ entidade.pais || 'N/A' }}
              </p>
            </div>

            <Separator />

            <div>
              <span class="font-medium block mb-1">
                Distrito
              </span>

              <p class="text-muted-foreground">
                {{ entidade.distrito || 'N/A' }}
              </p>
            </div>

          </CardContent>
        </Card>

      </div>

      <!-- SIDEBAR -->
      <div class="space-y-6">

        <!-- RESUMO -->
        <Card>
          <CardHeader class="pb-3">
            <CardTitle class="text-sm font-bold uppercase text-muted-foreground tracking-wider">
              Resumo
            </CardTitle>
          </CardHeader>

          <CardContent class="space-y-4 text-sm">

            <div class="flex items-center justify-between">
              <span>Total Contratos Adjudicante</span>

              <Badge variant="outline">
                {{
                  entidade.num_contratos_adjudicante
                }}
              </Badge>
            </div>
            <div class="flex items-center justify-between">
              <span>Total Contratos Adjudicatário</span>

              <Badge variant="outline">
                {{
                  entidade.num_contratos_adjudicatario
                }}
              </Badge>
            </div>

            <Separator />

            <div class="flex items-center justify-between">
              <span>Total Movimentado</span>

              <span class="font-medium">
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

    <!-- CONTRATOS -->
    <Card>
      <CardHeader>
        <CardTitle class="text-lg flex items-center gap-2">
          <FileText class="h-5 w-5" />
          Lista de Contratos
        </CardTitle>
      </CardHeader>

      <CardContent>

        <div class="bg-white border border-gray-200 rounded-xl overflow-hidden shadow-sm">

          <table class="w-full text-left border-collapse">
            <thead class="bg-gray-50 border-b border-gray-200">
            <tr>
              <th class="px-4 py-3 text-[10px] font-bold text-gray-400 uppercase">
                Título do contrato
              </th>

              <th class="px-4 py-3 text-[10px] font-bold text-gray-400 uppercase text-right">
                Valor
              </th>
            </tr>
            </thead>

            <tbody class="divide-y divide-gray-100">

            <tr
                v-for="contract in entityContracts"
                :key="contract.chave_contratos"
                class="hover:bg-blue-50/50 cursor-pointer"
                @click="goToContract(contract.chave_contratos)"
            >
              <td class="px-4 py-3">
                <p class="text-sm font-medium text-gray-800 line-clamp-1">
                  {{ contract.objeto ?? 'Sem título' }}
                </p>

                <p class="text-[10px] text-gray-400">
                  {{ formatDate(contract.data_publicacao) }}
                </p>
              </td>

              <td class="px-4 py-3 text-right text-sm font-bold text-gray-900">
                {{ formatCurrency(contract.valor_contratual) }}
              </td>
            </tr>

            </tbody>
          </table>

          <div
              v-if="entityContracts.length === 0"
              class="p-8 text-center text-gray-400 text-sm"
          >
            Sem contratos registados.
          </div>

        </div>

      </CardContent>
    </Card>

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

import {
  MapPinned,
  FileText,
  Euro,
  Hash,
  Landmark
} from "lucide-vue-next"

const apiStore = useAPIStore()
const route = useRoute()

const entidade = ref(null)
const entityContracts = ref([])

const loading = ref(true)
const error = ref(null)

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
    error.value = "Não foi possível carregar os detalhes da entidade."
  }
  finally {
    loading.value = false
  }
})
</script>