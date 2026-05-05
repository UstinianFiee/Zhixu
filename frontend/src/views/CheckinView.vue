<template>
  <div class="max-w-2xl mx-auto px-4 py-8">
    <h2 class="font-serif text-2xl text-zhixu-blue font-bold mb-6">每日打卡</h2>

    <!-- Checkin Status -->
    <div class="bg-white rounded-2xl shadow-sm border border-zhixu-blue/5 p-8 mb-6 text-center">
      <div class="mb-4">
        <svg class="w-16 h-16 mx-auto transition" fill="none" stroke="currentColor" stroke-width="1.2" viewBox="0 0 24 24"
          :class="checkedIn ? 'text-zhixu-gold' : 'text-zhixu-blue/30'">
          <path d="M9 12l2 2 4-4"/><circle cx="12" cy="12" r="10"/>
        </svg>
      </div>
      <div v-if="checkedIn" class="text-zhixu-gold font-serif text-xl mb-2">今日已打卡</div>
      <div v-else class="text-zhixu-blue/60 font-serif text-xl mb-2">今日尚未打卡</div>
      <div class="text-sm text-zhixu-blue/50 mb-4">连续打卡 <span class="text-zhixu-gold font-bold text-lg">{{ streakDays }}</span> 天</div>
      <button v-if="!checkedIn" @click="handleCheckin" :disabled="loading"
        class="px-8 py-3 bg-zhixu-blue text-zhixu-cream rounded-xl hover:bg-zhixu-dark transition font-medium disabled:opacity-50">
        {{ loading ? '打卡中...' : '立即打卡' }}
      </button>
      <p v-if="toast" class="text-sm text-zhixu-gold mt-3">{{ toast }}</p>
    </div>

    <!-- Calendar -->
    <div class="bg-white rounded-2xl shadow-sm border border-zhixu-blue/5 p-6">
      <div class="flex items-center justify-between mb-4">
        <button @click="changeMonth(-1)" class="p-1 text-zhixu-blue/40 hover:text-zhixu-blue transition">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M15 19l-7-7 7-7"/></svg>
        </button>
        <span class="font-serif text-lg text-zhixu-blue">{{ currentYear }}年{{ currentMonth + 1 }}月</span>
        <button @click="changeMonth(1)" class="p-1 text-zhixu-blue/40 hover:text-zhixu-blue transition">
          <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><path d="M9 5l7 7-7 7"/></svg>
        </button>
      </div>

      <!-- Week headers -->
      <div class="grid grid-cols-7 gap-1 mb-2">
        <div v-for="d in weekDays" :key="d" class="text-center text-xs text-zhixu-blue/40 py-1">{{ d }}</div>
      </div>

      <!-- Calendar days -->
      <div class="grid grid-cols-7 gap-1">
        <div v-for="(day, i) in calendarDays" :key="i"
          class="aspect-square flex items-center justify-center text-sm rounded-lg transition"
          :class="dayClass(day)">
          {{ day || '' }}
        </div>
      </div>

      <div class="flex items-center gap-4 mt-4 justify-center text-xs text-zhixu-blue/40">
        <span class="flex items-center gap-1"><span class="w-3 h-3 rounded-full bg-zhixu-gold"></span> 已打卡</span>
        <span class="flex items-center gap-1"><span class="w-3 h-3 rounded-full bg-zhixu-gold ring-2 ring-zhixu-gold/30"></span> 今天</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import api from '../api/client'
import { useAuthStore } from '../stores/auth'

const authStore = useAuthStore()
const checkedIn = ref(false)
const streakDays = ref(0)
const loading = ref(false)
const toast = ref('')
const checkinDates = ref<Set<string>>(new Set())

const now = new Date()
const currentYear = ref(now.getFullYear())
const currentMonth = ref(now.getMonth())
const weekDays = ['日', '一', '二', '三', '四', '五', '六']

const calendarDays = computed(() => {
  const firstDay = new Date(currentYear.value, currentMonth.value, 1).getDay()
  const daysInMonth = new Date(currentYear.value, currentMonth.value + 1, 0).getDate()
  const days: (number | null)[] = []
  for (let i = 0; i < firstDay; i++) days.push(null)
  for (let i = 1; i <= daysInMonth; i++) days.push(i)
  return days
})

function dateKey(day: number) {
  const m = String(currentMonth.value + 1).padStart(2, '0')
  const d = String(day).padStart(2, '0')
  return `${currentYear.value}-${m}-${d}`
}

function isToday(day: number) {
  const t = new Date()
  return day === t.getDate() && currentMonth.value === t.getMonth() && currentYear.value === t.getFullYear()
}

function dayClass(day: number | null) {
  if (!day) return ''
  const checked = checkinDates.value.has(dateKey(day))
  const today = isToday(day)
  if (checked && today) return 'bg-zhixu-gold text-white font-bold ring-2 ring-zhixu-gold/30'
  if (checked) return 'bg-zhixu-gold/15 text-zhixu-gold font-medium'
  if (today) return 'ring-2 ring-zhixu-blue/20 text-zhixu-blue'
  return 'text-zhixu-blue/50'
}

function changeMonth(delta: number) {
  let m = currentMonth.value + delta
  let y = currentYear.value
  if (m > 11) { m = 0; y++ }
  if (m < 0) { m = 11; y-- }
  currentMonth.value = m
  currentYear.value = y
  fetchMonthData()
}

async function fetchStatus() {
  try {
    const res = await api.get('/checkin/status')
    checkedIn.value = res.data.checked_in_today
    streakDays.value = res.data.streak_days
  } catch {}
}

async function fetchMonthData() {
  try {
    const res = await api.get('/checkin/month', {
      params: { year: currentYear.value, month: currentMonth.value + 1 }
    })
    checkinDates.value = new Set(res.data.dates)
  } catch {}
}

async function handleCheckin() {
  if (checkedIn.value || loading.value) return
  loading.value = true
  try {
    const res = await api.post('/checkin')
    checkedIn.value = true
    streakDays.value = res.data.streak_days
    checkinDates.value.add(dateKey(new Date().getDate()))
    if (res.data.points_earned && authStore.user) {
      authStore.updatePoints(authStore.user.total_points + res.data.points_earned, authStore.user.current_level)
    }
    toast.value = res.data.message || '打卡成功！'
  } catch (e: any) {
    toast.value = e?.response?.data?.detail || '打卡失败，请重试'
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchStatus()
  fetchMonthData()
})
</script>
