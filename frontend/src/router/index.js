import { createRouter, createWebHistory } from 'vue-router'
import ContractsList from '../components/ContractsList.vue'
import ContractDetail from '../components/ContractDetail.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: ContractsList
  },
  {
    path: '/contracts/:id',
    name: 'contract-detail',
    component: ContractDetail,
    props: true
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router