<script setup>
import { ref, onMounted } from "vue"
import { useRouter } from "vue-router"
import { useAPIStore } from "@/store/api.js"

import {
  Card,
  CardContent,
  CardHeader,
  CardTitle,
  CardDescription,
} from "@/components/ui/card/index.ts"

import { Separator } from "@/components/ui/separator/index.ts"

import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table/index.ts"

const router = useRouter()
const apiStore = useAPIStore()

const biggestContracts = ref([])
const smallestContracts = ref([])
const entitiesCompeteMoreEarnLess = ref([])
const entitiesMoreContractsAsContracting = ref([])

const cpvQuery = ref("")
const cpvLoading = ref(false)

const cpvResult = ref({
  quantidade_contratos: 0,
  valor_total: 0,
})

const loading = ref(true)

async function searchCPV() {
  if (!cpvQuery.value.trim()) return

  try {
    cpvLoading.value = true

    const response = await apiStore.searchCPV(cpvQuery.value)

    cpvResult.value = response.data ?? {
      quantidade_contratos: 0,
      valor_total: 0,
    }
  } catch (error) {
    console.error(error)
  } finally {
    cpvLoading.value = false
  }
}

function goToEntity(id) {
  router.push(`/entidades/${id}`)
}

function goToContract(id) {
  router.push(`/contracts/${id}`)
}

const formatCurrency = (value) => {
  if (!value) return "0 €"

  return new Intl.NumberFormat("pt-PT", {
    style: "currency",
    currency: "EUR",
  }).format(value)
}

const formatPercentage = (value) => {
  if (!value) return "0%"

  return `${Number(value).toFixed(2)}%`
}

onMounted(async () => {
  try {
    const [
      bigC,
      smallC,
      competeMoreEarnLessE,
      moreContractsE,
    ] = await Promise.all([
      apiStore.getBiggestContracts(),
      apiStore.getSmallestContracts(),
      apiStore.getEntitiesCompeteMoreEarnLess(),
      apiStore.getEntitiesMoreContractsAsContracting(),
    ])

    biggestContracts.value = bigC.data
    smallestContracts.value = smallC.data
    entitiesCompeteMoreEarnLess.value = competeMoreEarnLessE.data
    entitiesMoreContractsAsContracting.value = moreContractsE.data
  } catch (error) {
    console.error("Erro ao carregar dados:", error)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="p-6 overflow-x-hidden">
    <div v-if="loading" class="text-center text-muted-foreground">
      A carregar dados...
    </div>

    <div
        v-else
        class="space-y-6"
    >

      <!-- PESQUISA CPV -->
      <Card>
        <CardHeader>
          <CardTitle>
            Pesquisa CPV
          </CardTitle>

          <CardDescription>
            Pesquisa por código, descrição ou palavras-chave
          </CardDescription>
        </CardHeader>

        <Separator />

        <CardContent class="pt-6">
          <div class="flex flex-col md:flex-row gap-4">
            <input
                v-model="cpvQuery"
                type="text"
                placeholder="Ex: projeto, carros, software..."
                class="flex-1 border rounded-md px-4 py-2 bg-background"
                @keyup.enter="searchCPV"
            >

            <button
                class="bg-primary text-primary-foreground px-6 py-2 rounded-md hover:opacity-90 transition"
                @click="searchCPV"
            >
              Procurar
            </button>
          </div>

          <div
              v-if="cpvLoading"
              class="mt-6 text-muted-foreground"
          >
            A procurar...
          </div>

          <div
              v-else
              class="grid grid-cols-1 md:grid-cols-2 gap-4 mt-6"
          >
            <Card>
              <CardContent class="pt-6">
                <div class="text-sm text-muted-foreground">
                  Quantidade de contratos
                </div>

                <div class="text-3xl font-bold mt-2">
                  {{ cpvResult.quantidade_contratos ?? 0 }}
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardContent class="pt-6">
                <div class="text-sm text-muted-foreground">
                  Valor total
                </div>

                <div class="text-3xl font-bold mt-2 text-green-600">
                  {{ formatCurrency(cpvResult.valor_total) }}
                </div>
              </CardContent>
            </Card>
          </div>
        </CardContent>
      </Card>

      <!-- GRID -->
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6 min-w-0">

        <!-- Maiores Contratos -->
        <Card class="min-w-0 overflow-hidden">
          <CardHeader>
            <CardTitle>Maiores Contratos</CardTitle>

            <CardDescription>
              Contratos com maior valor contratual
            </CardDescription>
          </CardHeader>

          <Separator />

          <CardContent class="pt-6 overflow-hidden">
            <Table class="w-full table-fixed">
              <TableHeader>
                <TableRow>
                  <TableHead class="w-[70%]">
                    Objeto
                  </TableHead>

                  <TableHead class="w-[30%] text-right">
                    Valor
                  </TableHead>
                </TableRow>
              </TableHeader>

              <TableBody>
                <TableRow
                    v-for="c in biggestContracts"
                    :key="c.chave_contratos"
                >
                  <TableCell class="overflow-hidden">
                    <button
                        :title="c.objeto"
                        class="block w-full overflow-hidden text-ellipsis whitespace-nowrap text-left text-primary hover:underline font-medium cursor-pointer"
                        @click="goToContract(c.chave_contratos)"
                    >
                      {{ c.objeto }}
                    </button>
                  </TableCell>

                  <TableCell
                      class="text-right font-semibold text-green-600 whitespace-nowrap"
                  >
                    {{ formatCurrency(c.valor_contratual) }}
                  </TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </CardContent>
        </Card>

        <!-- Menores Contratos -->
        <Card class="min-w-0 overflow-hidden">
          <CardHeader>
            <CardTitle>Menores Contratos</CardTitle>

            <CardDescription>
              Contratos com menor valor contratual
            </CardDescription>
          </CardHeader>

          <Separator />

          <CardContent class="pt-6 overflow-hidden">
            <Table class="w-full table-fixed">
              <TableHeader>
                <TableRow>
                  <TableHead class="w-[70%]">
                    Objeto
                  </TableHead>

                  <TableHead class="w-[30%] text-right">
                    Valor
                  </TableHead>
                </TableRow>
              </TableHeader>

              <TableBody>
                <TableRow
                    v-for="c in smallestContracts"
                    :key="c.chave_contratos"
                >
                  <TableCell class="overflow-hidden">
                    <button
                        :title="c.objeto"
                        class="block w-full overflow-hidden text-ellipsis whitespace-nowrap text-left text-primary hover:underline font-medium cursor-pointer"
                        @click="goToContract(c.chave_contratos)"
                    >
                      {{ c.objeto }}
                    </button>
                  </TableCell>

                  <TableCell
                      class="text-right text-red-500 font-semibold whitespace-nowrap"
                  >
                    {{ formatCurrency(c.valor_contratual) }}
                  </TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </CardContent>
        </Card>

        <!-- Competem Mais e Ganham Menos -->
        <Card class="min-w-0 overflow-hidden">
          <CardHeader>
            <CardTitle>
              Entidades que Competem Mais e Ganham Menos
            </CardTitle>

            <CardDescription>
              Entidades com menor taxa de vitória
            </CardDescription>
          </CardHeader>

          <Separator />

          <CardContent class="pt-6 overflow-hidden">
            <Table class="w-full table-fixed">
              <TableHeader>
                <TableRow>
                  <TableHead class="w-[50%]">
                    Entidade
                  </TableHead>

                  <TableHead class="w-[25%] text-right">
                    Concursos
                  </TableHead>

                  <TableHead class="w-[25%] text-right">
                    Taxa Vitória
                  </TableHead>
                </TableRow>
              </TableHeader>

              <TableBody>
                <TableRow
                    v-for="c in entitiesCompeteMoreEarnLess"
                    :key="c.chave_entidade"
                >
                  <TableCell class="overflow-hidden">
                    <button
                        :title="c.nome"
                        class="block w-full overflow-hidden text-ellipsis whitespace-nowrap text-left text-primary hover:underline font-medium cursor-pointer"
                        @click="goToEntity(c.chave_entidade)"
                    >
                      {{ c.nome }}
                    </button>
                  </TableCell>

                  <TableCell class="text-right whitespace-nowrap">
                    {{ c.total_concursos }}
                  </TableCell>

                  <TableCell class="text-right font-semibold whitespace-nowrap">
                    {{ formatPercentage(c.taxa_vitoria) }}
                  </TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </CardContent>
        </Card>

        <!-- Mais Contratos -->
        <Card class="min-w-0 overflow-hidden">
          <CardHeader>
            <CardTitle>
              Entidades com Mais Contratos
            </CardTitle>

            <CardDescription>
              Ranking de entidades adjudicantes
            </CardDescription>
          </CardHeader>

          <Separator />

          <CardContent class="pt-6 overflow-hidden">
            <Table class="w-full table-fixed">
              <TableHeader>
                <TableRow>
                  <TableHead class="w-[45%]">
                    Entidade
                  </TableHead>

                  <TableHead class="w-[20%] text-right">
                    Nº Contratos
                  </TableHead>

                  <TableHead class="w-[35%] text-right">
                    Valor adjudicado
                  </TableHead>
                </TableRow>
              </TableHeader>

              <TableBody>
                <TableRow
                    v-for="c in entitiesMoreContractsAsContracting"
                    :key="c.adjudicante"
                >
                  <TableCell class="overflow-hidden">
                    <button
                        :title="c.nome"
                        class="block w-full overflow-hidden text-ellipsis whitespace-nowrap text-left text-primary hover:underline font-medium cursor-pointer"
                        @click="goToEntity(c.adjudicante)"
                    >
                      {{ c.nome }}
                    </button>
                  </TableCell>

                  <TableCell class="text-right font-semibold whitespace-nowrap">
                    {{ c.numero_contratos }}
                  </TableCell>

                  <TableCell class="text-right font-semibold whitespace-nowrap">
                    {{ formatCurrency(c.valor_adjudicado) }}
                  </TableCell>
                </TableRow>
              </TableBody>
            </Table>
          </CardContent>
        </Card>

      </div>
    </div>
  </div>
</template>