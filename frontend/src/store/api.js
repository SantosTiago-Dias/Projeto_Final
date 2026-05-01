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


    return {
        getListContracts,
        getDetailContracts
    }
})