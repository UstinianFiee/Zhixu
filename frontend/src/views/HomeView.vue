<template>
  <div class="min-h-[calc(100vh-3.5rem)] bg-gradient-to-b from-zhixu-cream to-zhixu-light overflow-x-hidden">
    <!-- Hero Section -->
    <div class="text-center py-12 sm:py-16 px-4 animate-fade-in">
      <h1 class="font-serif text-3xl sm:text-4xl text-zhixu-blue font-bold mb-3 animate-slide-up">知序</h1>
      <p class="text-zhixu-blue/60 text-sm sm:text-base tracking-widest animate-slide-up-delay">遣词作序，静揽人间文柔</p>
      <div class="mt-6 flex justify-center gap-4 animate-slide-up-delay-2">
        <router-link to="/wordlists" class="px-6 py-2.5 bg-zhixu-blue text-zhixu-cream rounded-lg hover:bg-zhixu-dark transition font-medium">
          开始学习
        </router-link>
        <router-link v-if="!authStore.isLoggedIn" to="/register" class="px-6 py-2.5 border border-zhixu-blue/20 text-zhixu-blue rounded-lg hover:bg-zhixu-blue/5 transition">
          注册账号
        </router-link>
      </div>
    </div>

    <!-- Daily Content Cards -->
    <div class="max-w-6xl mx-auto px-4 pb-16">
      <div class="grid grid-cols-1 md:grid-cols-3 gap-6 items-stretch">
        <div class="animate-card" style="animation-delay: 0.1s">
          <DailyQuote />
        </div>
        <div class="animate-card" style="animation-delay: 0.2s">
          <DailySong />
        </div>
        <div class="animate-card" style="animation-delay: 0.3s">
          <DailyArticle />
        </div>
      </div>

      <!-- Quick Actions -->
      <div class="mt-12 grid grid-cols-2 sm:grid-cols-5 gap-4">
        <router-link to="/wordlists" class="animate-card group bg-white/60 backdrop-blur rounded-xl p-5 text-center hover:bg-white hover:shadow-md transition border border-zhixu-blue/5" style="animation-delay: 0.4s">
          <svg class="w-6 h-6 mx-auto mb-2 text-zhixu-blue/40 group-hover:text-zhixu-gold transition" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" v-html="icons.book"></svg>
          <div class="text-sm font-medium text-zhixu-blue group-hover:text-zhixu-gold transition">词库练习</div>
        </router-link>
        <router-link to="/leaderboard" class="animate-card group bg-white/60 backdrop-blur rounded-xl p-5 text-center hover:bg-white hover:shadow-md transition border border-zhixu-blue/5" style="animation-delay: 0.45s">
          <svg class="w-6 h-6 mx-auto mb-2 text-zhixu-blue/40 group-hover:text-zhixu-gold transition" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" v-html="icons.trophy"></svg>
          <div class="text-sm font-medium text-zhixu-blue group-hover:text-zhixu-gold transition">排行榜</div>
        </router-link>
        <router-link to="/dashboard" class="animate-card group bg-white/60 backdrop-blur rounded-xl p-5 text-center hover:bg-white hover:shadow-md transition border border-zhixu-blue/5" style="animation-delay: 0.5s">
          <svg class="w-6 h-6 mx-auto mb-2 text-zhixu-blue/40 group-hover:text-zhixu-gold transition" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" v-html="icons.chart"></svg>
          <div class="text-sm font-medium text-zhixu-blue group-hover:text-zhixu-gold transition">学习看板</div>
        </router-link>
        <router-link to="/errors" class="animate-card group bg-white/60 backdrop-blur rounded-xl p-5 text-center hover:bg-white hover:shadow-md transition border border-zhixu-blue/5" style="animation-delay: 0.55s">
          <svg class="w-6 h-6 mx-auto mb-2 text-zhixu-blue/40 group-hover:text-zhixu-gold transition" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" v-html="icons.target"></svg>
          <div class="text-sm font-medium text-zhixu-blue group-hover:text-zhixu-gold transition">错题本</div>
        </router-link>
        <router-link :to="authStore.isLoggedIn ? '/checkin' : '/login'"
          class="animate-card group bg-white/60 backdrop-blur rounded-xl p-5 text-center hover:bg-white hover:shadow-md transition border border-zhixu-blue/5"
          :class="{ 'ring-2 ring-zhixu-gold bg-zhixu-gold/5': checkedIn }" style="animation-delay: 0.6s">
          <svg class="w-6 h-6 mx-auto mb-2 transition" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"
            :class="checkedIn ? 'text-zhixu-gold' : 'text-zhixu-blue/40 group-hover:text-zhixu-gold'">
            <path d="M9 12l2 2 4-4"/><circle cx="12" cy="12" r="10"/>
          </svg>
          <div class="text-sm font-medium transition" :class="checkedIn ? 'text-zhixu-gold' : 'text-zhixu-blue group-hover:text-zhixu-gold'">
            <template v-if="checkedIn">已打卡 {{ streakDays }}天</template>
            <template v-else>每日打卡</template>
          </div>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import DailyQuote from '../components/DailyQuote.vue'
import DailySong from '../components/DailySong.vue'
import DailyArticle from '../components/DailyArticle.vue'
import { useAuthStore } from '../stores/auth'
import { icons } from '../components/icons'
import api from '../api/client'

const authStore = useAuthStore()
const checkedIn = ref(false)
const streakDays = ref(0)

async function checkStatus() {
  if (!authStore.isLoggedIn) return
  try {
    const res = await api.get('/checkin/status')
    checkedIn.value = res.data.checked_in_today
    streakDays.value = res.data.streak_days
  } catch {}
}

onMounted(checkStatus)
</script>

<style scoped>
.animate-fade-in { animation: fadeIn 0.8s ease-out; }
.animate-slide-up { animation: slideUp 0.6s ease-out both; }
.animate-slide-up-delay { animation: slideUp 0.6s ease-out 0.15s both; }
.animate-slide-up-delay-2 { animation: slideUp 0.6s ease-out 0.3s both; }
.animate-card { animation: cardAppear 0.5s ease-out both; }
@keyframes fadeIn { from { opacity: 0; } to { opacity: 1; } }
@keyframes slideUp { from { opacity: 0; transform: translateY(16px); } to { opacity: 1; transform: translateY(0); } }
@keyframes cardAppear { from { opacity: 0; transform: translateY(20px) scale(0.98); } to { opacity: 1; transform: translateY(0) scale(1); } }
</style>
