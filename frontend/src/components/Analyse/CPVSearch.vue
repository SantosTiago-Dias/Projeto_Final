<template>
  <Card>
    <CardHeader>
      <CardTitle>Pesquisa por palavras chave</CardTitle>

      <CardDescription>
        Aqui é possível pesquisar contratos utilizando palavras simples como 'carros', 'software' ou 'obras'.
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
        />

        <button
            class="bg-primary text-primary-foreground px-6 py-2 rounded-md hover:opacity-90 transition"
            @click="searchCPV"
        >
          Procurar
        </button>
      </div>

      <div v-if="cpvLoading" class="mt-6 text-muted-foreground">
        A procurar...
      </div>

      <div v-else class="space-y-4 mt-6">
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Card>
            <CardContent class="pt-6">
              <div class="text-sm text-muted-foreground">
                Total de contratos encontrados
              </div>
              <div class="text-3xl font-bold mt-2">
                {{ cpvResult.quantidade_contratos }}
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardContent class="pt-6">
              <div class="text-sm text-muted-foreground">
                Dinheiro total envolvido
              </div>
              <div class="text-3xl font-bold mt-2 text-green-600">
                {{ formatCurrency(cpvResult.valor_total) }}
              </div>
            </CardContent>
          </Card>
        </div>

        <div
            v-if="cpvResult.quantidade_contratos > 0"
            class="flex justify-end"
        >
          <button
              class="bg-primary text-primary-foreground px-6 py-2 rounded-md hover:opacity-90 transition"
              @click="goToContractsByCPV"
          >
            Ver contratos encontrados
          </button>
        </div>
      </div>
    </CardContent>
  </Card>
</template>

<script setup >
import { ref } from "vue"
import { useRouter } from "vue-router"
import { useAPIStore } from "@/store/api"

import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card"

import { Separator } from "@/components/ui/separator"
import { toast } from "vue-sonner";


const router = useRouter()
const apiStore = useAPIStore()

const cpvQuery = ref("")
const cpvLoading = ref(false)

const cpvResult = ref({
  quantidade_contratos: 0,
  valor_total: 0,
})

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
    toast.error("Ocorreu um erro, não foi possivel carregar os dados")
  } finally {
    cpvLoading.value = false
  }
}

function formatCurrency(value) {
  if (!value) return "0 €"

  return new Intl.NumberFormat("pt-PT", {
    style: "currency",
    currency: "EUR",
  }).format(value)
}

function goToContractsByCPV() {
  router.push({
    path: "/",
    query: {
      cpvs: cpvQuery.value,
    },
  })
}
</script>