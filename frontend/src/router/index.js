import { createRouter, createWebHistory } from 'vue-router'
import ContractsList from '../components/Contracts/ContractsList.vue'
import ContractDetail from '../components/Contracts/ContractDetail.vue'
import EntityList from "@/components/Entity/EntityList.vue";
import EntityDetail from "@/components/Entity/EntityDetail.vue";
import CPVSearch from "@/components/Analyse/CPVSearch.vue"
import BiggestContracts from "@/components/Analyse/BiggestContracts.vue"
import SmallestContracts from "@/components/Analyse/SmallestContracts.vue"
import EntitiesCompeteMoreEarnLess from "@/components/Analyse/EntitiesCompeteMoreEarnLess.vue"
import EntitiesMoreContracts from "@/components/Analyse/EntitiesMoreContracts.vue"
import GraphsContractType from "@/components/Analyse/GraphsContractType.vue";
import Terms from "@/components/Terms/Terms.vue";

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
  },
    {
        path: '/entidades/:id',
        name: 'entity-detail',
        component: EntityDetail,
        props: true
    },
    {
        path: '/analyses/cpv',
        name: 'cpv-analysis',
        component: CPVSearch
    },

    {
        path: '/analyses/biggest-contracts',
        name: 'biggest-contracts',
        component: BiggestContracts
    },

    {
        path: '/analyses/smallest-contracts',
        name: 'smallest-contracts',
        component: SmallestContracts
    },

    {
        path: '/analyses/compete-more-earn-less',
        name: 'compete-more-earn-less',
        component: EntitiesCompeteMoreEarnLess
    },

    {
        path: '/analyses/more-contracts',
        name: 'more-contracts',
        component: EntitiesMoreContracts
    },
    {
        path: '/analyses/contracts-graphs',
        name: 'contracts-graphs',
        component: GraphsContractType
    },
    {
        path: '/terms',
        name: 'termos',
        component: Terms
    },
    {
        path: '/:pathMatch(.*)*',
        redirect: '/'
    }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router