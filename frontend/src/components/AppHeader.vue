<template>
  <header class="bg-zhixu-blue text-zhixu-cream shadow-lg sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 h-14 flex items-center justify-between">
      <router-link to="/" class="flex items-center gap-2 hover:opacity-80 transition">
        <span class="text-xl font-bold tracking-wider">知序</span>
        <span class="text-xs text-zhixu-gold hidden sm:inline">遣词作序，静揽人间文柔</span>
      </router-link>

      <!-- Desktop nav -->
      <nav class="hidden sm:flex items-center gap-4">
        <router-link to="/" class="nav-link" active-class="nav-link-active">首页</router-link>
        <router-link to="/wordlists" class="nav-link" active-class="nav-link-active">词库</router-link>
        <router-link to="/leaderboard" class="nav-link" active-class="nav-link-active">排行榜</router-link>

        <template v-if="authStore.isLoggedIn">
          <router-link to="/dashboard" class="nav-link" active-class="nav-link-active">看板</router-link>
          <PointsBadge />
          <div class="relative group">
            <button class="flex items-center gap-1 px-2 py-1 rounded hover:bg-white/10 transition">
              <span class="w-7 h-7 rounded-full bg-zhixu-gold/30 flex items-center justify-center text-sm overflow-hidden">
                <img v-if="authStore.user?.avatar_url" :src="authStore.user.avatar_url" class="w-full h-full object-cover" @error="(e: any) => e.target.style.display='none'" />
                <span v-else>{{ (authStore.user?.nickname || authStore.user?.username)?.charAt(0).toUpperCase() }}</span>
              </span>
            </button>
            <div class="absolute right-0 top-full mt-1 w-40 bg-white rounded-lg shadow-xl border opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all">
              <router-link to="/profile" class="block px-4 py-2 text-zhixu-blue hover:bg-zhixu-cream rounded-t-lg text-sm">个人中心</router-link>
              <router-link to="/checkin" class="block px-4 py-2 text-zhixu-blue hover:bg-zhixu-cream text-sm">每日打卡</router-link>
              <router-link to="/favorites" class="block px-4 py-2 text-zhixu-blue hover:bg-zhixu-cream text-sm">我的收藏</router-link>
              <router-link to="/errors" class="block px-4 py-2 text-zhixu-blue hover:bg-zhixu-cream text-sm">错题本</router-link>
              <router-link v-if="authStore.user?.is_admin" to="/admin/wordlists" class="block px-4 py-2 text-zhixu-blue hover:bg-zhixu-cream text-sm">后台管理</router-link>
              <button @click="handleLogout" class="w-full text-left px-4 py-2 text-red-500 hover:bg-red-50 rounded-b-lg text-sm">退出登录</button>
            </div>
          </div>
        </template>
        <template v-else>
          <router-link to="/login" class="px-3 py-1.5 rounded bg-zhixu-gold text-zhixu-dark text-sm font-medium hover:bg-yellow-400 transition">登录</router-link>
        </template>
      </nav>

      <!-- Mobile menu button -->
      <button class="sm:hidden p-2 rounded hover:bg-white/10 transition" @click="mobileOpen = !mobileOpen">
        <svg v-if="!mobileOpen" class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M4 6h16M4 12h16M4 18h16"/></svg>
        <svg v-else class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M18 6 6 18M6 6l12 12"/></svg>
      </button>
    </div>

    <!-- Mobile nav -->
    <Transition name="slide-down">
      <div v-if="mobileOpen" class="sm:hidden border-t border-white/10 bg-zhixu-blue pb-3">
        <router-link v-for="link in mobileLinks" :key="link.to" :to="link.to"
          @click="mobileOpen = false"
          class="block px-4 py-2.5 text-sm text-zhixu-cream/80 hover:text-zhixu-gold hover:bg-white/5 transition">
          {{ link.label }}
        </router-link>
        <template v-if="authStore.isLoggedIn">
          <router-link v-if="authStore.user?.is_admin" to="/admin/wordlists"
            @click="mobileOpen = false"
            class="block px-4 py-2.5 text-sm text-zhixu-gold border-t border-white/10 mt-1 pt-3 hover:bg-white/5 transition">
            后台管理
          </router-link>
          <div class="px-4 py-2 flex items-center gap-2" :class="authStore.user?.is_admin ? '' : 'border-t border-white/10 mt-1 pt-3'">
            <PointsBadge />
            <span class="text-xs text-zhixu-cream/60">{{ authStore.user?.nickname || authStore.user?.username }}</span>
          </div>
          <button @click="handleLogout; mobileOpen = false" class="w-full text-left px-4 py-2.5 text-sm text-red-400 hover:bg-white/5 transition">退出登录</button>
        </template>
        <template v-else>
          <router-link to="/login" @click="mobileOpen = false" class="block px-4 py-2.5 text-sm text-zhixu-gold">登录 / 注册</router-link>
        </template>
      </div>
    </Transition>
  </header>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useAuthStore } from '../stores/auth'
import { useRouter } from 'vue-router'
import PointsBadge from './PointsBadge.vue'

const authStore = useAuthStore()
const router = useRouter()
const mobileOpen = ref(false)

const mobileLinks = [
  { to: '/', label: '首页' },
  { to: '/wordlists', label: '词库' },
  { to: '/leaderboard', label: '排行榜' },
  { to: '/dashboard', label: '学习看板' },
  { to: '/checkin', label: '每日打卡' },
  { to: '/favorites', label: '我的收藏' },
  { to: '/errors', label: '错题本' },
  { to: '/profile', label: '个人中心' },
]

function handleLogout() {
  authStore.logout()
  router.push('/')
}
</script>

<style scoped>
.nav-link {
  @apply px-2 py-1 text-sm text-zhixu-cream/80 hover:text-zhixu-gold transition rounded;
}
.nav-link-active {
  @apply text-zhixu-gold font-medium;
}
.slide-down-enter-active, .slide-down-leave-active {
  transition: all 0.2s ease;
}
.slide-down-enter-from, .slide-down-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>
