<template>
  <div class="min-h-screen bg-slate-50 text-slate-800 font-sans">
    <main class="max-w-7xl mx-auto p-8">
      <div class="mb-6">
        <h1 class="text-2xl font-bold text-slate-900">Contratos</h1>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 gap-8">

        <div class="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm hover:shadow-md transition duration-300">
          <div class="mb-4">
            <h3 class="text-lg font-semibold text-slate-800">Tipo de Contratos</h3>
            <p class="text-xs text-slate-400" >Distribuição da quantidade pelos os varios tipos de contrato</p>
          </div>
          <div class="chart-container">
            <Doughnut v-if="chartData1" :data="chartData1" :options="chartOptions" />
          </div>
        </div>

        <div class="bg-white p-6 rounded-2xl border border-slate-100 shadow-sm hover:shadow-md transition duration-300">
          <div class="mb-4">
            <h3 class="text-lg font-semibold text-slate-800">Tipo de Procedimento</h3>
            <p class="text-xs text-slate-400" title="Os procedimentos de contratação pública em Portugal são definidos pelo Código dos Contratos Públicos (CCP), que rege a escolha de fornecedores de forma transparente e concorrencial. Os tipos de procedimentos variam essencialmente em função do valor estimado do contrato e da natureza da aquisição.">
              Distribuição da quantidade pelos os varios tipos de procedimento</p>
          </div>
          <div class="chart-container">
            <Doughnut v-if="chartData2" :data="chartData2" :options="chartOptions" />
          </div>
        </div>

      </div>
    </main>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { Chart as ChartJS, ArcElement, Tooltip, Legend } from 'chart.js'
import { Doughnut } from 'vue-chartjs'
import { useAPIStore } from "@/store/api.js";

ChartJS.register(ArcElement, Tooltip, Legend) // ← move outside onMounted

const apiStore = useAPIStore()

// ← declare refs outside onMounted so the template can access them
const chartData1 = ref(null)
const chartData2 = ref(null)

const chartOptions = ref({
  responsive: true,
  maintainAspectRatio: false
})

//generate news colors
const generateColors = (count) => {
  const hueStep = 360 / count
  return Array.from({ length: count }, (_, i) => `hsl(${i * hueStep}, 70%, 60%)`)
}

const generateChart = (name,dataset,labels) => {
  return  {
    labels: labels,
    datasets: [
      {
        label: name,
        backgroundColor: generateColors(labels.length),
        borderRadius: 8,
        data: dataset.data.map(item => item.contratos)
      }
    ]
  }
}

onMounted(async () => {

  const tipo_contrato = await apiStore.getAnalyticsTipoContrato()
  console.log(tipo_contrato)
  let labels = tipo_contrato.data.map(item => item.tipo_contrato.tipo)
  chartData1.value = generateChart("Tipo contrato", tipo_contrato,labels)

  /*const tipo_procedimento = await apiStore.getAnalyticsTipoProcedimento()
  labels = tipo_procedimento.data.map(item => item.tipo_procedimento.tipo)
  chartData2.value = generateChart("Tipo procedimento", tipo_procedimento,labels)*/
})
</script>

<style scoped>
.chart-container {
  position: relative;
  width: 400px;
  height: 400px;
}
</style>