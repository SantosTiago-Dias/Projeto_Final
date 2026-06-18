<script setup>
import { FileText, Building2, FolderKanban, Search, ChevronDown  } from "lucide-vue-next";
import { RouterLink, RouterView, useRouter,useRoute } from "vue-router";
import { Toaster } from "vue-sonner";
import { useWebSocket } from "@/composable/newDataWS.js";
import {inject} from "vue";
import { ref } from "vue"
let ws = inject('wsBaseURL');
useWebSocket(ws);


const router = useRouter()
const route = useRoute()
const search = ref("")

const searchContracts = () => {

  if (!search.value.trim()) return

  router.push({
    path: "/",
    query: {
      objeto: search.value
    }
  })
}

const open = ref(false)

function toggleDropdown() {
  open.value = !open.value
}

function goTo(path) {
  router.push(path)
  open.value = true
}

const isActive = (path) => route.path.startsWith(path)
</script>

<template>

  <div class="flex min-h-screen w-full bg-[#f8fafc]">

    <Toaster richColors position="bottom-right" />

    <!-- Sidebar -->
    <aside class="hidden w-64 border-r bg-white md:flex flex-col fixed h-full">
      <div class="p-6 border-b">
        <router-link to="/" class="text-xl font-bold tracking-tight text-slate-900">
          DB_FAIR
        </router-link>
      </div>

      <nav class="flex-1 px-4 py-6 space-y-1">
        <router-link
            to="/"
            class="flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium text-slate-600 transition-all hover:bg-slate-50 hover:text-slate-900 group"
            active-class="bg-blue-50 text-blue-700 font-semibold shadow-sm"
        >
          <FileText :size="20" class="text-slate-400 group-hover:text-slate-900" />
          Contratos
        </router-link>


        <router-link
            to="/entidades"
            class="flex items-center gap-3 rounded-lg px-3 py-2.5 text-sm font-medium text-slate-600 transition-all hover:bg-slate-50 hover:text-slate-900 group"
            active-class="bg-blue-50 text-blue-700 font-semibold"
        >
          <Building2 :size="20" class="text-slate-400 group-hover:text-slate-900" />
          Entidades
        </router-link>
        <div class="relative">

          <!-- BOTÃO PRINCIPAL -->
          <button
              @click="toggleDropdown"
              class="flex w-full items-center justify-between gap-3 rounded-lg px-3 py-2.5 text-sm font-medium text-slate-600 transition-all hover:bg-slate-50 hover:text-slate-900"
              :class="{ 'bg-blue-50 text-blue-700 font-semibold': isActive('/analyses') }"
          >
            <div class="flex items-center gap-3">
              <FolderKanban :size="20" />
              Análises
            </div>

            <ChevronDown
                :size="16"
                class="transition-transform"
                :class="{ 'rotate-180': open }"
            />
          </button>

          <!-- DROPDOWN -->
          <div
              v-if="open"
              class="ml-8 mt-2 space-y-1"
          >
            <button
                @click="goTo('/analyses/cpv')"
                class="block w-full text-left rounded-md px-3 py-2 text-sm hover:bg-slate-100"
            >
              Pesquisa CPV
            </button>

            <button
                @click="goTo('/analyses/biggest-contracts')"
                class="block w-full text-left rounded-md px-3 py-2 text-sm hover:bg-slate-100"
            >
              Maiores Contratos
            </button>

            <button
                @click="goTo('/analyses/smallest-contracts')"
                class="block w-full text-left rounded-md px-3 py-2 text-sm hover:bg-slate-100"
            >
              Menores Contratos
            </button>

            <button
                @click="goTo('/analyses/compete-more-earn-less')"
                class="block w-full text-left rounded-md px-3 py-2 text-sm hover:bg-slate-100"
            >
              Tentam mais e ganham menos
            </button>

            <button
                @click="goTo('/analyses/more-contracts')"
                class="block w-full text-left rounded-md px-3 py-2 text-sm hover:bg-slate-100"
            >
              Quem mais faz contratos
            </button>
            <button
                @click="goTo('/analyses/contracts-graphs')"
                class="block w-full text-left rounded-md px-3 py-2 text-sm hover:bg-slate-100"
            >
              Detalhes sobre contratos
            </button>
          </div>

        </div>
      </nav>
    </aside>

    <!-- Main -->
    <div class="flex flex-col flex-1 md:ml-64">
      <!-- Header -->
      <header class="h-16 border-b bg-white/80 backdrop-blur-md sticky top-0 z-10 flex items-center justify-between px-8">
        <div class="flex items-center gap-2 text-sm font-medium text-slate-500">
          <span>Portal</span>
        </div>

        <div class="flex items-center gap-4">
          <div class="relative hidden sm:block">
            <Search class="absolute left-2.5 top-2.5 h-4 w-4 text-slate-400" />
            <input
                v-model="search"
                @keyup.enter="searchContracts"
                type="search"
                placeholder="Pesquisar contratos..."
                class="pl-9 h-9 w-64 rounded-md border border-slate-200 bg-slate-50 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all"
            />
          </div>
        </div>
      </header>

      <!-- View -->
      <main class="p-8 max-w-7xl">
        <RouterView :key="$route.fullPath" />
      </main>
    </div>
  </div>
</template>