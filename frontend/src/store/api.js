import { defineStore } from 'pinia'
import axios from 'axios'
import {inject} from "vue";
export const useAPIStore = defineStore('api', () => {
    const API_BASE_URL = inject('apiBaseURL');

    const getListContracts = (params = {}) =>{
        return axios.get(`${API_BASE_URL}/contracts`,{params})
    }

    const getFilterListContracts = () =>{
        return axios.get(`${API_BASE_URL}/contracts/getFilters`)
    }

    const getDetailContracts= (id) =>{
        return axios.get(`${API_BASE_URL}/contracts/${id}`)
    }

    const getListEntity = (params = {}) =>{
        return axios.get(`${API_BASE_URL}/entidades`,{params})
    }

    const getDetailEntity= (id) =>{
        return axios.get(`${API_BASE_URL}/entidades/${id}`)
    }

    const getListContractofEntity = (id) =>{
        return axios.get(`${API_BASE_URL}/entidades/${id}/listContratcs`)
    }

    const getBiggestContracts = () => {
        return axios.get(`${API_BASE_URL}/analytics/biggest-contracts`)
    }

    const getSmallestContracts = () => {
        return axios.get(`${API_BASE_URL}/analytics/smallest-contracts`)
    }

    const getEntitiesCompeteMoreEarnLess = () => {
        return axios.get(`${API_BASE_URL}/analytics/entitiesCompeteMoreEarnLess`)
    }

    const getEntitiesMoreContractsAsContracting = () => {
        return axios.get(`${API_BASE_URL}/analytics/entitiesMoreContractsAsContracting`)
    }

    const searchCPV = (query) => {
        return axios.get(`${API_BASE_URL}/analytics/search-cpv`, {
            params: {query}})
    }


    return {
        getListContracts,
        getFilterListContracts,
        getDetailContracts,
        getListEntity,
        getDetailEntity,
        getListContractofEntity,
        getBiggestContracts,
        getSmallestContracts,
        getEntitiesCompeteMoreEarnLess,
        getEntitiesMoreContractsAsContracting,
        searchCPV,
    }
})