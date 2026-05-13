<script setup>
import { ref, onMounted } from "vue"
import { useAPIStore } from "@/store/api.js"

const apiStore = useAPIStore()

const biggestContracts = ref([])
const smallestContracts = ref([])
const entitiesCompeteMoreEarnLess = ref([])
const entitiesMoreContractsAsContracting = ref([])

onMounted(async () => {
  const bigC = await apiStore.getBiggestContracts()
  biggestContracts.value = bigC.data
  const smallC = await apiStore.getSmallestContracts()
  smallestContracts.value = smallC.data
  const competeMoreEarnLessE = await apiStore.getEntitiesCompeteMoreEarnLess()
  entitiesCompeteMoreEarnLess.value = competeMoreEarnLessE.data
  const moreContractsE = await apiStore.getEntitiesMoreContractsAsContracting()
  entitiesMoreContractsAsContracting.value = moreContractsE.data
})
</script>

<template>
  <div v-for="c in biggestContracts" :key="c.chave_contratos">
    {{ c.valor_contratual }}
  </div>

  <div v-for="c in smallestContracts" :key="c.chave_contratos">
    {{ c.valor_contratual }}
  </div>

  <div v-for="c in entitiesCompeteMoreEarnLess" :key="c.nome">
    {{ c.taxa_vitoria }}
  </div>

  <div v-for="c in entitiesMoreContractsAsContracting" :key="c.nome">
    {{ c.numero_contratos }}
  </div>
</template>