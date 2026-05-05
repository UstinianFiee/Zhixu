<template>
  <div>
    <!-- Mobile: horizontal tabs -->
    <div class="sm:hidden bg-white border-b border-zhixu-blue/5 px-4 pt-3 pb-0 flex gap-1 overflow-x-auto">
      <router-link v-for="link in navLinks" :key="link.to" :to="link.to"
        class="shrink-0 px-3 py-2 text-sm rounded-t-lg border-b-2 transition"
        active-class="border-zhixu-gold text-zhixu-gold font-medium"
        :class="'border-transparent text-zhixu-blue/50 hover:text-zhixu-blue'">
        {{ link.label }}
      </router-link>
    </div>
    <div class="sm:hidden p-4 bg-zhixu-cream/50 min-h-[calc(100vh-7rem)]">
      <router-view />
    </div>

    <!-- Desktop: sidebar + main -->
    <div class="hidden sm:flex min-h-[calc(100vh-3.5rem)]">
      <aside class="w-48 bg-white border-r border-zhixu-blue/5 p-4">
        <h3 class="font-serif text-sm text-zhixu-blue/50 font-medium mb-4 uppercase tracking-wider">后台管理</h3>
        <nav class="space-y-1">
          <router-link v-for="link in navLinks" :key="link.to" :to="link.to"
            class="block px-3 py-2 rounded-lg text-sm text-zhixu-blue/60 hover:text-zhixu-blue hover:bg-zhixu-cream transition"
            active-class="text-zhixu-gold bg-zhixu-gold/10 font-medium">
            {{ link.label }}
          </router-link>
        </nav>
      </aside>
      <main class="flex-1 p-6 bg-zhixu-cream/50">
        <router-view />
      </main>
    </div>
  </div>
</template>

<script setup lang="ts">
const navLinks = [
  { to: '/admin/wordlists', label: '词库管理' },
  { to: '/admin/content', label: '内容管理' },
  { to: '/admin/users', label: '用户管理' },
]
</script>
