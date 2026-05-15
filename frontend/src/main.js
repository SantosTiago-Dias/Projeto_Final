import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import './style.css'
import {createPinia} from "pinia";

const SERVER_BASE_URL = import.meta.env.VITE_BASE_URL;
const WS_BASE_URL = import.meta.env.VITE_WS_URL;
const API_BASE_URL = SERVER_BASE_URL + '/api';
const app = createApp(App)

app.provide('apiBaseURL', API_BASE_URL)
app.provide('wsBaseURL', WS_BASE_URL)

app.use(createPinia())
app.use(router)

app.mount('#app')