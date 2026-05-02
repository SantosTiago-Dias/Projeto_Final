import { defineStore } from 'pinia'
import axios from 'axios'
import {inject} from "vue";
export const useAPIStore = defineStore('api', () => {
    const API_BASE_URL = inject('apiBaseURL')

    const getListContracts = () =>{
        return axios.get(`${API_BASE_URL}/contracts`)
    }

    const getDetailContracts= (id) =>{
        return axios.get(`${API_BASE_URL}/contracts/${id}`)
    }

    const getListEntity = () =>{
        return axios.get(`${API_BASE_URL}/entidades`)
    }

    const getDetailEntity= (id) =>{
        return axios.get(`${API_BASE_URL}/entidades/${id}`)
    }

    const getListContractofEntity = (id) =>{
        return axios.get(`${API_BASE_URL}/entidades/${id}/listContratcs`)
    }


    return {
        getListContracts,
        getDetailContracts,
        getListEntity,
        getDetailEntity,
        getListContractofEntity
    }
})