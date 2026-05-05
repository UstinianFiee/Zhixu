<template>
  <router-link to="/profile" class="flex items-center gap-1 px-2 py-1 rounded bg-white/10 hover:bg-white/20 transition text-sm">
    <span class="text-zhixu-gold">Lv.{{ authStore.user?.current_level || 1 }}</span>
    <span class="text-zhixu-cream/90">{{ authStore.user?.total_points || 0 }}分</span>
  </router-link>
</template>

<script setup lang="ts">
import { useAuthStore } from '../stores/auth'
const authStore = useAuthStore()
</script>
