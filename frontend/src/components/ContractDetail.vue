<script setup>
import { onMounted, ref } from "vue"

const contract = ref(null)
const loading = ref(true)

function formatCurrency(value) {
  return new Intl.NumberFormat("pt-PT", {
    style: "currency",
    currency: "EUR",
  }).format(Number(value))
}

function formatBool(value) {
  return value === 1 || value === true ? "Sim" : "Não"
}

onMounted(async () => {
  const id = window.location.pathname.split("/").pop()

  try {
    const res = await fetch(`http://localhost:8000/api/contracts/${id}`)
    contract.value = await res.json()
  } catch (err) {
    console.error(err)
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="container max-w-6xl mx-auto space-y-8">

    <p v-if="loading" class="text-gray-500">A carregar...</p>

    <div v-if="contract" class="space-y-8">

      <!-- HEADER -->
      <div class="space-y-2">
        <h1 class="text-3xl font-bold text-gray-900">
          {{ contract.contrato.objeto }}
        </h1>

        <div class="text-sm text-gray-500">
          ID {{ contract.contrato.id_contrato }}
        </div>
      </div>

      <!-- RESUMO -->
      <section class="bg-white border rounded-xl shadow-sm p-5 space-y-4">

        <div class="grid md:grid-cols-3 gap-4">
          <div>
            <div class="text-xs text-gray-400">Valor</div>
            <div class="text-lg font-bold text-green-600">
              {{ formatCurrency(contract.contrato.valor_contratual) }}
            </div>
          </div>

          <div>
            <div class="text-xs text-gray-400">Publicação</div>
            <div>{{ contract.contrato.data_publicacao }}</div>
          </div>

          <div>
            <div class="text-xs text-gray-400">Celebração</div>
            <div>{{ contract.contrato.data_celebracao }}</div>
          </div>
        </div>

        <div class="text-sm text-gray-700">
          {{ contract.contrato.descricao }}
        </div>

      </section>

      <!-- ENTIDADES -->
      <div class="grid md:grid-cols-2 gap-6">

        <section class="bg-white border rounded-xl p-5">
          <h2 class="font-semibold mb-2">Adjudicante</h2>
          <div>{{ contract.adjudicanteRel?.nome }}</div>
          <div class="text-xs text-gray-400">
            NIF {{ contract.adjudicanteRel?.nif }}
          </div>
        </section>

        <section class="bg-white border rounded-xl p-5">
          <h2 class="font-semibold text-green-700 mb-2">Adjudicatário</h2>
          <div>{{ contract.adjudicatario?.nome }}</div>
          <div class="text-xs text-gray-400">
            NIF {{ contract.adjudicatario?.nif }}
          </div>
        </section>

      </div>

      <!-- CPVs -->
      <section class="bg-white border rounded-xl p-5">
        <div class="text-xs text-gray-400 mb-2">CPVs</div>

        <div v-if="contract.contrato?.cpvs?.length" class="flex flex-wrap gap-2">
          <span
            v-for="(c, i) in contract.contrato.cpvs"
            :key="i"
            class="px-2 py-1 bg-gray-100 rounded text-xs font-mono"
          >
            {{ c.cpv?.codigo }} - {{ c.cpv?.cpv_descricao }}
          </span>
        </div>

        <span v-else class="text-gray-400 text-sm">
          Não aplicável
        </span>
      </section>

      <!-- FLAGS -->
      <section class="flex flex-wrap gap-2">

        <span class="px-2 py-1 text-xs bg-gray-100 rounded">
          Ecológico: {{ formatBool(contract.contrato.contrato_ecologico) }}
        </span>

        <span class="px-2 py-1 text-xs bg-gray-100 rounded">
          Critérios: {{ formatBool(contract.contrato.crit_materiais) }}
        </span>

        <span class="px-2 py-1 text-xs bg-gray-100 rounded">
          Centralizado: {{ formatBool(contract.contrato.procedimento_centralizado) }}
        </span>

      </section>

      <!-- CONCORRENTES (NOVO) -->
      <section   v-if="contract.entidades?.length > 0"
class="bg-white border rounded-xl p-5">

        <h2 class="font-semibold text-gray-900 mb-4">
          Concorrentes
        </h2>

        <div class="space-y-3">

          <div
            v-for="(ent, i) in contract.entidades"
            :key="i"
            class="flex justify-between items-center border-b pb-2 last:border-0"
          >

            <div>
              <div class="font-medium text-gray-800">
                {{ ent.nome }}
              </div>

              <div class="text-xs text-gray-400">
                NIF {{ ent.nif }}
              </div>
            </div>

            <div class="text-xs text-gray-500">
              {{ ent.num_contratos_adjudicatario }} contratos
            </div>

          </div>

        </div>

      </section>

      <!-- OUTROS -->
      <section class="bg-white border rounded-xl p-5 space-y-2 text-sm">

        <div>
          <span class="text-xs text-gray-400">Regime</span><br>
          {{ contract.contrato.regime }}
        </div>

        <div>
          <span class="text-xs text-gray-400">Acordo Quadro</span><br>
          {{ contract.contrato.num_acordos_quadro }} - {{ contract.contrato.desc_acordo_quadro }}
        </div>

        <div>
          <span class="text-xs text-gray-400">Observações</span><br>
          {{ contract.contrato.observacoes }}
        </div>

      </section>

    </div>

    <p v-if="!loading && !contract" class="text-gray-500">
      Contrato não encontrado
    </p>

  </div>
</template>