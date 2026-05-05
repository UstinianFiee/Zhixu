<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <h2 class="font-serif text-2xl text-zhixu-blue font-bold mb-6">学习看板</h2>

    <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 mb-8">
      <div class="bg-white rounded-xl p-5 border border-zhixu-blue/5 text-center">
        <div class="text-3xl font-bold text-zhixu-gold">{{ stats.totalPoints }}</div>
        <div class="text-xs text-zhixu-blue/50 mt-1">总积分</div>
      </div>
      <div class="bg-white rounded-xl p-5 border border-zhixu-blue/5 text-center">
        <div class="text-3xl font-bold text-green-600">{{ stats.totalCorrect }}</div>
        <div class="text-xs text-zhixu-blue/50 mt-1">正确单词</div>
      </div>
      <div class="bg-white rounded-xl p-5 border border-zhixu-blue/5 text-center">
        <div class="text-3xl font-bold text-zhixu-blue">{{ stats.avgSpeed }}</div>
        <div class="text-xs text-zhixu-blue/50 mt-1">平均速度 (词/分)</div>
      </div>
      <div class="bg-white rounded-xl p-5 border border-zhixu-blue/5 text-center">
        <div class="text-3xl font-bold text-red-400">{{ stats.totalWrong }}</div>
        <div class="text-xs text-zhixu-blue/50 mt-1">错误次数</div>
      </div>
    </div>

    <!-- Today -->
    <div class="bg-white rounded-xl p-6 border border-zhixu-blue/5 mb-8">
      <h3 class="font-serif text-lg text-zhixu-blue mb-3">今日学习</h3>
      <div class="flex items-center gap-6">
        <div>
          <div class="text-2xl font-bold text-green-600">{{ stats.todayCorrect }}</div>
          <div class="text-xs text-zhixu-blue/50">今日正确</div>
        </div>
        <div>
          <div class="text-2xl font-bold text-zhixu-blue">{{ stats.totalRecords }}</div>
          <div class="text-xs text-zhixu-blue/50">总练习次数</div>
        </div>
      </div>
    </div>

    <!-- Level Progress -->
    <div class="bg-white rounded-xl p-6 border border-zhixu-blue/5 mb-8">
      <div class="flex items-center justify-between mb-3">
        <span class="font-serif text-lg text-zhixu-blue">Lv.{{ authStore.user?.current_level }} {{ levelTitle }}</span>
        <span class="text-sm text-zhixu-blue/50">{{ authStore.user?.total_points }} / {{ nextLevelPoints > 0 ? nextLevelPoints : 'MAX' }} 积分</span>
      </div>
      <div class="h-3 bg-zhixu-cream rounded-full overflow-hidden">
        <div class="h-full bg-gradient-to-r from-zhixu-blue to-zhixu-gold rounded-full transition-all duration-500"
          :style="{ width: progressPercent + '%' }"></div>
      </div>
    </div>

    <!-- Level Reference -->
    <div class="bg-white rounded-xl p-6 border border-zhixu-blue/5">
      <h3 class="font-serif text-lg text-zhixu-blue mb-4">等级体系</h3>
      <div class="grid grid-cols-2 sm:grid-cols-5 gap-3">
        <div v-for="lv in levels" :key="lv.level"
          class="text-center p-3 rounded-lg transition"
          :class="authStore.user && authStore.user.current_level >= lv.level ? 'bg-zhixu-gold/10 text-zhixu-gold' : 'bg-zhixu-cream/50 text-zhixu-blue/30'">
          <div class="font-bold">Lv.{{ lv.level }}</div>
          <div class="text-xs mt-1">{{ lv.title }}</div>
          <div class="text-xs opacity-60">{{ lv.points }}分</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, reactive } from 'vue'
import { useAuthStore } from '../stores/auth'
import api from '../api/client'

const authStore = useAuthStore()

const stats = reactive({
  totalPoints: 0,
  totalCorrect: 0,
  totalWrong: 0,
  avgSpeed: 0,
  todayCorrect: 0,
  totalRecords: 0,
})

const levels = [
  { level: 1, title: '文艺学徒', points: 0 },
  { level: 2, title: '单词小生', points: 200 },
  { level: 3, title: '笔墨行者', points: 500 },
  { level: 4, title: '浮光阅者', points: 1000 },
  { level: 5, title: '英文探路者', points: 2000 },
  { level: 6, title: '星夜记忆者', points: 3500 },
  { level: 7, title: '轻文艺学士', points: 5500 },
  { level: 8, title: '键盘诗人', points: 8000 },
  { level: 9, title: '安宁守护者', points: 12000 },
  { level: 10, title: '独行大师', points: 18000 },
]

const LEVEL_TITLES: Record<number, string> = Object.fromEntries(levels.map(l => [l.level, l.title]))
const levelTitle = computed(() => LEVEL_TITLES[authStore.user?.current_level || 1] || '')

const nextLevelPoints = computed(() => {
  const next = levels.find(l => l.level === (authStore.user?.current_level || 1) + 1)
  return next ? next.points : -1
})

const prevLevelPoints = computed(() => {
  const current = levels.find(l => l.level === (authStore.user?.current_level || 1))
  return current ? current.points : 0
})

const progressPercent = computed(() => {
  if (nextLevelPoints.value < 0) return 100
  const range = nextLevelPoints.value - prevLevelPoints.value
  const current = (authStore.user?.total_points || 0) - prevLevelPoints.value
  return Math.min(100, Math.max(0, (current / range) * 100))
})

onMounted(async () => {
  try {
    const res = await api.get('/words/dashboard')
    const data = res.data
    stats.totalPoints = data.total_points || 0
    stats.totalCorrect = data.correct_count || 0
    stats.totalWrong = data.wrong_count || 0
    stats.avgSpeed = data.avg_speed || 0
    stats.todayCorrect = data.today_correct || 0
    stats.totalRecords = data.total_records || 0
  } catch {}
})
</script>
