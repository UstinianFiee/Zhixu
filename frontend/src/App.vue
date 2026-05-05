<template>
  <div class="min-h-screen flex flex-col overflow-x-hidden">
    <AppHeader />
    <main class="flex-1">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<script setup lang="ts">
import AppHeader from './components/AppHeader.vue'
import { useAuthStore } from './stores/auth'

const authStore = useAuthStore()
authStore.loadFromStorage()
</script>
