<script setup>
import { onMounted, ref, computed } from "vue"
import { useAPIStore } from "@/store/api.js"
import { useRoute } from "vue-router"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card/index.ts"
import { Badge } from "@/components/ui/badge/index.ts"
import { Separator } from "@/components/ui/separator/index.ts"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table/index.ts"
import { Pin,  Calendar, Euro, FileText, Users } from "lucide-vue-next"
import CPVList from "@/components/ui/CPV/CPV.vue";
import {Button} from "@/components/ui/button/index.ts";
import router from "@/router/index.js";

const apiStore = useAPIStore()
const route = useRoute()

const contract = ref(null)
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

function goToEntity(id) {
  router.push(`/entidades/${id}`)
}


onMounted(async () => {

  const id = route.params.id

  try {
    const res = await apiStore.getDetailContracts(id)
    contract.value = res.data
  } catch (err) {
    error.value = "Não foi possível carregar os detalhes do contrato."
    console.error(err)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <!-- LOADING -->
  <div v-if="loading" class="text-center py-10 text-gray-400">
    A carregar...
  </div>

  <!-- ERROR -->
  <div v-else-if="error" class="text-center py-10 text-red-500">
    {{ error }}
  </div>

  <!-- CONTENT SAFE -->
  <div v-else-if="contract" class="container max-w-5xl py-10 px-4 md:px-0 mx-auto space-y-8">
    
      <!-- HEADER -->
    <Button>
      <button
          @click="$router.back()"
          class="flex items-center gap-1"
      >
        ← Voltar atrás
      </button>
    </Button>
      <header class="space-y-4">
        <div class="flex items-center gap-2">
          <Badge variant="outline" class="uppercase tracking-wider">Contrato Público</Badge>
          <Badge v-if="contract?.procedimento_centralizado === 1" variant="secondary">Procedimento Centralizado</Badge>
        </div>
        <h1 class="text-3xl font-extrabold tracking-tight lg:text-4xl text-slate-900 leading-tight">
          {{ contract.objeto }}
        </h1>
      </header>

      <!-- KEY METRICS -->
      <div class="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card class="bg-primary/5 border-none shadow-none">
          <CardHeader class="pb-2">
            <CardDescription class="flex items-center gap-2">
              <Euro class="h-4 w-4" /> Valor Contratual
            </CardDescription>
            <CardTitle class="text-2xl text-primary">{{ formatCurrency(contract.valor_contratual) }}</CardTitle>
          </CardHeader>
        </Card>

        <Card class="shadow-sm">
          <CardHeader class="pb-2">
            <CardDescription class="flex items-center gap-2">
              <Calendar class="h-4 w-4" /> Publicação
            </CardDescription>
            <CardTitle class="text-xl">{{ formatDate(contract.data_publicacao) }}</CardTitle>
          </CardHeader>
        </Card>

        <Card class="shadow-sm">
          <CardHeader class="pb-2">
            <CardDescription class="flex items-center gap-2">
              <Calendar class="h-4 w-4" /> Celebração
            </CardDescription>
            <CardTitle class="text-xl">{{ formatDate(contract.data_celebracao) }}</CardTitle>
          </CardHeader>
        </Card>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
        <!-- MAIN INFO -->
        <div class="lg:col-span-2 space-y-8">
          <section>
            <h3 class="text-lg font-semibold mb-3 flex items-center gap-2">
              <FileText class="h-5 w-5 text-muted-foreground" />
              Descrição do Objeto
            </h3>
            <p class="text-slate-600 leading-relaxed bg-slate-50 p-4 rounded-lg border">
              {{ contract.descricao || 'Sem descrição disponível.' }}
            </p>
          </section>

          <!-- CONCORRENTES TABLE -->
          <Card>
            <CardHeader>
              <CardTitle class="text-lg flex items-center gap-2">
                <Users class="h-5 w-5" /> Entidades Envolvidas
              </CardTitle>
            </CardHeader>
            <CardContent>
              <Table>
                <TableHeader>
                  <TableRow>
                    <TableHead>Entidade</TableHead>
                    <TableHead>NIF</TableHead>
                    <TableHead class="text-right">Papel</TableHead>
                  </TableRow>
                </TableHeader>
                <TableBody>
                  <!-- Adjudicante -->
                  <TableRow @click="goToEntity(contract.adjudicante.chave_entidade)">
                    <TableCell class="font-medium text-blue-700">{{ contract.adjudicante.nome }}</TableCell>
                    <TableCell>{{ contract.adjudicante.nif }}</TableCell>
                    <TableCell class="text-right"><Badge variant="outline">Adjudicante</Badge></TableCell>
                  </TableRow>
                  <!-- Concorrentes -->
                  <TableRow v-for="c in contract.concorrentes" :key="c.id" @click="goToEntity(c.entidade.chave_entidade)">
                    <TableCell class="font-medium">{{ c.entidade.nome }}</TableCell>
                    <TableCell>{{ c.entidade.nif }}</TableCell>
                    <TableCell class="text-right">
                      <Badge :variant="c.adjudicatario ? 'default' : 'secondary'">
                        {{ c.adjudicatario ? 'Adjudicatário' : 'Concorrente' }}
                      </Badge>
                    </TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            </CardContent>
          </Card>

          <section>
            <h3 class="text-lg font-semibold mb-3 flex items-center gap-2">
              <Pin class="h-5 w-5 text-muted-foreground" />
              Local de Execução
            </h3>
            <p class="text-slate-600 leading-relaxed bg-slate-50 p-4 rounded-lg border">
              {{ contract.local_execucao || 'Sem local de execução disponível.' }}
            </p>
          </section>
        </div>

        <!-- SIDEBAR INFO -->
        <div class="space-y-6">
          <!-- CPVs -->
          <Card>
            <CardHeader class="pb-3">
              <CardTitle class="text-sm font-bold uppercase text-muted-foreground tracking-wider">CPV Códigos</CardTitle>
            </CardHeader>
            <CardContent class="flex flex-wrap gap-2">
              <div class="rounded-xl border bg-card text-card-foreground shadow-sm p-6">
                <CPVList :cpvs="contract.cpvs" />
              </div>
            </CardContent>
          </Card>

          <!-- DETAILS LIST -->
          <Card>
            <CardHeader class="pb-3">
              <CardTitle class="text-sm font-bold uppercase text-muted-foreground tracking-wider">Detalhes Adicionais</CardTitle>
            </CardHeader>
            <CardContent class="space-y-4 text-sm">
              <div>
                <span class="font-medium block mb-1">Regime</span>
                <span class="text-muted-foreground">{{ contract.regime }}</span>
              </div>
              <Separator />
              <div class="grid grid-cols-2 gap-2">
                <div>
                  <span class="font-medium block mb-1 text-xs">Ecológico</span>
                  <Badge :variant="contract.contrato_ecologico ? 'default' : 'outline'">
                    {{ contract.contrato_ecologico ? 'Sim' : 'Não' }}
                  </Badge>
                </div>
                <div>
                  <span class="font-medium block mb-1 text-xs">Acordo Quadro</span>
                  <Badge variant="outline">{{ contract.num_acordos_quadro || 'Não' }}</Badge>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>

      <!-- FOOTER INFO -->
      <footer v-if="contract.observacoes" class="pt-6 border-t">
        <h4 class="text-sm font-semibold mb-2 italic text-muted-foreground text-center">Observações</h4>
        <p class="text-sm text-muted-foreground text-center max-w-2xl mx-auto">
          {{ contract.observacoes }}
        </p>
      </footer>
    </div>
</template>