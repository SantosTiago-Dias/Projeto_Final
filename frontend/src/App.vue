<script setup>
</script>

<template>
  <nav class="max-w-full p-5 shadow-md flex flex-col sm:flex-row sm:justify-between sm:items-center gap-4">
    <div class="nav-container">
      <!-- Logo -->
      <div class="logo">
        <router-link to="/">DB_FAIR</router-link>
      </div>
    </div>
  </nav>
  <main>
    <RouterView :key="$route.fullPath" />
  </main>
</template>

<style scoped></style>
