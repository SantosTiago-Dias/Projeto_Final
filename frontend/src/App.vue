<script setup>
import { FileText, Building2, LayoutDashboard, Search } from "lucide-vue-next";
import { RouterLink, RouterView } from "vue-router";
import {onMounted, onUnmounted} from "vue";

onMounted(() => {
  try {
    const ws = new WebSocket("ws://localhost:3000/");
    ws.onmessage = ({data}) => {
      this.message =  data;
      console.log(this.message);
    }
  } catch(err) {
    console.log(err);
  }
})
</script>

<template>
  <div class="flex min-h-screen w-full bg-[#f8fafc]">
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
          <FileText :size="20" class="text-blue-600" />
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
      </nav>
    </aside>

    <!-- Main Content Area -->
    <div class="flex flex-col flex-1 md:ml-64">
      <!-- Header -->
      <header class="h-16 border-b bg-white/80 backdrop-blur-md sticky top-0 z-10 flex items-center justify-between px-8">
        <div class="flex items-center gap-2 text-sm font-medium text-slate-500">
          <span>Portal</span>
          <span class="text-slate-300">/</span>
          <span class="text-slate-900">Contratos</span>
        </div>

        <div class="flex items-center gap-4">
          <div class="relative hidden sm:block">
            <Search class="absolute left-2.5 top-2.5 h-4 w-4 text-slate-400" />
            <input
                type="search"
                placeholder="Pesquisar contratos..."
                class="pl-9 h-9 w-64 rounded-md border border-slate-200 bg-slate-50 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500/20 transition-all"
            />
          </div>
        </div>
      </header>

      <!-- View Wrapper -->
      <main class="p-8 max-w-7xl">
        <RouterView :key="$route.fullPath" />
      </main>
    </div>
  </div>
</template>