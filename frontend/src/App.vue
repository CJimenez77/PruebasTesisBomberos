<template>
  <div v-if="$route.meta.public" class="min-h-screen bg-bomberos-bg text-gray-100">
    <router-view />
  </div>

  <div v-else class="flex min-h-screen bg-bomberos-bg text-gray-100 antialiased">
    <!-- Fixed Sidebar -->
    <Sidebar />

    <!-- Main Content Area -->
    <div class="flex-1 flex flex-col min-w-0 overflow-y-auto">
      <Navbar :title="$route.meta.title || 'Sistema de Inventario'" />
      <main class="flex-1">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup>
import Navbar from './components/Navbar.vue'
import Sidebar from './components/Sidebar.vue'
</script>
