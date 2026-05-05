<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <h2 class="font-serif text-2xl text-zhixu-blue font-bold mb-6">排行榜</h2>

    <!-- Tabs -->
    <div class="flex gap-2 mb-6 overflow-x-auto pb-2">
      <button v-for="tab in tabs" :key="tab.key"
        @click="activeTab = tab.key; fetchData()"
        class="px-4 py-2 rounded-lg text-sm font-medium whitespace-nowrap transition"
        :class="activeTab === tab.key ? 'bg-zhixu-blue text-zhixu-cream' : 'bg-white text-zhixu-blue/60 hover:text-zhixu-blue border border-zhixu-blue/10'">
        {{ tab.label }}
      </button>
    </div>

    <!-- My Rank -->
    <div v-if="myRank" class="mb-4 bg-zhixu-gold/10 rounded-xl p-4 flex items-center justify-between">
      <span class="text-sm text-zhixu-blue/70">我的排名</span>
      <span class="text-xl font-bold text-zhixu-gold">#{{ myRank }}</span>
    </div>

    <!-- Table -->
    <div class="bg-white rounded-2xl shadow-sm border border-zhixu-blue/5">
      <LeaderboardTable :entries="entries" :current-user-id="authStore.user?.id" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '../api/client'
import { useAuthStore } from '../stores/auth'
import LeaderboardTable from '../components/LeaderboardTable.vue'

interface Entry {
  rank: number
  user_id: number
  username: string
  avatar_url: string | null
  score: number
}

const authStore = useAuthStore()
const activeTab = ref('total')
const entries = ref<Entry[]>([])
const myRank = ref<number | null>(null)

const tabs = [
  { key: 'total', label: '总榜' },
  { key: 'month', label: '月榜' },
  { key: 'week', label: '周榜' },
  { key: 'daily', label: '今日之星' },
  { key: 'speed', label: '速度之王' },
  { key: 'mistake', label: '错题攻克' },
]

async function fetchData() {
  try {
    const res = await api.get(`/leaderboard/${activeTab.value}`)
    entries.value = res.data.entries
    myRank.value = res.data.my_rank
  } catch {}
}

onMounted(fetchData)
</script>
