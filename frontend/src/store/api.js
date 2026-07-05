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

    const getAnalyticsBiggestContracts = () => {
        return axios.get(`${API_BASE_URL}/analytics/biggest-contracts`)
    }

    const getAnalyticsSmallestContracts = () => {
        return axios.get(`${API_BASE_URL}/analytics/smallest-contracts`)
    }

    const getAnalyticsEntitiesCompeteMoreEarnLess = () => {
        return axios.get(`${API_BASE_URL}/analytics/entitiesCompeteMoreEarnLess`)
    }

    const getAnalyticsEntitiesMoreContractsAsContracting = () => {
        return axios.get(`${API_BASE_URL}/analytics/entitiesMoreContractsAsContracting`)
    }

    const searchCPV = (query) => {
        return axios.get(`${API_BASE_URL}/analytics/search-cpv`, {
            params: {query}})
    }

    const getAnalyticsTipoContrato = () => {
        return axios.get(`${API_BASE_URL}/analytics/tipoContrato`)
    }

    const getAnalyticsTipoProcedimento = () => {
        return axios.get(`${API_BASE_URL}/analytics/tipoProcedimento`)
    }

    const getTerms = () =>{
        return axios.get(`${API_BASE_URL}/terms`)
    }


    return {
        getListContracts,
        getFilterListContracts,
        getDetailContracts,
        getListEntity,
        getDetailEntity,
        getListContractofEntity,
        getAnalyticsBiggestContracts,
        getAnalyticsSmallestContracts,
        getAnalyticsEntitiesCompeteMoreEarnLess,
        getAnalyticsEntitiesMoreContractsAsContracting,
        searchCPV,
        getAnalyticsTipoContrato,
        getAnalyticsTipoProcedimento,
        getTerms
    }
})