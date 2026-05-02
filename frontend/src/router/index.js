import { createRouter, createWebHistory } from 'vue-router'
import ContractsList from '../components/Contracts/ContractsList.vue'
import ContractDetail from '../components/Contracts/ContractDetail.vue'
import EntityList from "@/components/Entity/EntityList.vue";

const routes = [
  {
    path: '/',
    name: 'contracts-list',
    component: ContractsList
  },
  {
    path: '/contracts/:id',
    name: 'contract-detail',
    component: ContractDetail,
    props: true
  },
  {
    path: '/entidades',
    name: 'entity-list',
    component: EntityList
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router