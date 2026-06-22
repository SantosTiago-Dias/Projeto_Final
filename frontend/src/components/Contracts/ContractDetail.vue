<template>
  <div class="container max-w-5xl py-10 px-4 md:px-0 mx-auto space-y-8">

    <Button @click="$router.back()" variant="ghost" class="flex items-center gap-2 hover:bg-slate-100 -ml-2 text-slate-600 transition-colors">
      <ArrowLeft class="h-4 w-4" />
      <span>Voltar atrás</span>
    </Button>

    <div v-if="loading" class="flex flex-col items-center justify-center py-20 space-y-4">
      <Loader2 class="h-8 w-8 animate-spin text-primary" />
      <p class="text-sm font-medium text-slate-500 tracking-wide animate-pulse">A carregar detalhes do contrato...</p>
    </div>

    <div v-else-if="!contract" class="flex flex-col items-center justify-center text-center py-16 px-4 bg-white border border-dashed border-slate-200 rounded-2xl shadow-sm transition-all duration-300">
      <div class="p-4 bg-amber-50 rounded-full text-amber-500 mb-4">
        <FileSearch2 class="h-8 w-8" />
      </div>
      <h3 class="text-lg font-semibold text-slate-900">Contrato não encontrado</h3>
    </div>

    <template v-else>
      <header class="space-y-4">
        <div class="flex items-center gap-2">
          <Badge variant="outline" class="uppercase tracking-wider"
                 :title="contract.tipo_contrato?.descricao ?? 'Sem descrição'">
            {{ contract.tipo_contrato?.tipo ?? 'Não disponível' }}
          </Badge>
          <Badge v-if="contract?.procedimento_centralizado === 1" variant="secondary">
            Procedimento Centralizado
          </Badge>
        </div>
        <h1 class="text-3xl font-extrabold tracking-tight lg:text-4xl text-slate-900 leading-tight">
          {{ contract.objeto }}
        </h1>
      </header>

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
            <CardTitle class="text-xl">{{ formatDate(contract?.data_publicacao) }}</CardTitle>
          </CardHeader>
        </Card>

        <Card class="shadow-sm">
          <CardHeader class="pb-2">
            <CardDescription class="flex items-center gap-2">
              <Calendar class="h-4 w-4" /> Celebração
            </CardDescription>
            <CardTitle class="text-xl">{{ formatDate(contract?.data_celebracao) }}</CardTitle>
          </CardHeader>
        </Card>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
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
                  <TableRow
                      v-if="contract.adjudicante"
                      class="cursor-pointer hover:bg-muted/50"
                      @click="goToEntity(contract.adjudicante.chave_entidade)"
                  >
                    <TableCell class="font-medium text-blue-700">{{ contract.adjudicante.nome }}</TableCell>
                    <TableCell>{{ contract.adjudicante.nif }}</TableCell>
                    <TableCell class="text-right"><Badge variant="outline">Adjudicante</Badge></TableCell>
                  </TableRow>
                  <TableRow
                      v-for="c in contract.concorrentes"
                      :key="c.id"
                      class="cursor-pointer hover:bg-muted/50"
                      @click="goToEntity(c.entidade.chave_entidade)"
                  >
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

        <div class="space-y-6">
          <Card>
            <CardHeader class="pb-3">
              <CardTitle class="text-sm font-bold uppercase text-muted-foreground tracking-wider">CPV Códigos</CardTitle>
            </CardHeader>
            <CardContent>
              <CPVList :cpvs="contract.cpvs" />
            </CardContent>
          </Card>

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

      <footer v-if="contract.observacoes" class="pt-6 border-t">
        <h4 class="text-sm font-semibold mb-2 italic text-muted-foreground text-center">Observações</h4>
        <p class="text-sm text-muted-foreground text-center max-w-2xl mx-auto">
          {{ contract.observacoes }}
        </p>
      </footer>
    </template>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue"
import { useAPIStore } from "@/store/api.js"
import { useRoute, useRouter } from "vue-router"

import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/card/index.ts"
import { Badge } from "@/components/ui/badge/index.ts"
import { Button } from "@/components/ui/button/index.ts"
import { Separator } from "@/components/ui/separator/index.ts"
import { Table, TableBody, TableCell, TableHead, TableHeader, TableRow } from "@/components/ui/table/index.ts"

import { Pin, Calendar, Euro, FileText, Users, ArrowLeft, Loader2, FileSearch2 } from "lucide-vue-next"
import CPVList from "@/components/ui/CPV/CPV.vue"

const apiStore = useAPIStore()
const route = useRoute()
const router = useRouter()

const contract = ref(null)
const loading = ref(true)
const error = ref(null)

const formatCurrency = (value) => {
  if (!value) return "---"
  return new Intl.NumberFormat("pt-PT", { style: "currency", currency: "EUR" }).format(Number(value))
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

  if (!id) {
    error.value = "ID do contrato não encontrado na rota."
    loading.value = false
    return
  }

  try {
    const res = await apiStore.getDetailContracts(id)
    contract.value = res.data
  } catch (err) {
    contract.value =null
  } finally {
    loading.value = false
  }
})
</script>