<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <h2 class="font-serif text-2xl text-zhixu-blue font-bold mb-6">错题本</h2>
    <div v-if="errors.length > 0" class="bg-white rounded-2xl shadow-sm border border-zhixu-blue/5 overflow-hidden">
      <table class="w-full text-sm">
        <thead>
          <tr class="border-b border-zhixu-blue/10 bg-zhixu-cream/50">
            <th class="py-3 px-4 text-left text-zhixu-blue/60 font-medium">单词</th>
            <th class="py-3 px-4 text-left text-zhixu-blue/60 font-medium">释义</th>
            <th class="py-3 px-4 text-center text-zhixu-blue/60 font-medium">错误次数</th>
            <th class="py-3 px-4 text-center text-zhixu-blue/60 font-medium">最近练习</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="item in errors" :key="item.word" class="border-b border-zhixu-blue/5 hover:bg-zhixu-cream/30 transition">
            <td class="py-3 px-4 font-mono text-zhixu-blue font-medium">{{ item.word }}</td>
            <td class="py-3 px-4 text-zhixu-blue/70">{{ item.translation }}</td>
            <td class="py-3 px-4 text-center">
              <span class="px-2 py-0.5 bg-red-50 text-red-500 rounded-full text-xs font-medium">{{ item.error_count }}</span>
            </td>
            <td class="py-3 px-4 text-center text-zhixu-blue/40 text-xs">{{ formatDate(item.last_attempt) }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else-if="!loading" class="text-center py-16 text-zhixu-blue/40">
      <svg class="w-12 h-12 mx-auto mb-3 text-zhixu-blue/20" fill="none" stroke="currentColor" stroke-width="1.2" viewBox="0 0 24 24"><path d="M22 10v6M2 10l10-5 10 5-10 5z"/><path d="M6 12v5c3 3 6.5 3 12 0v-5"/></svg>
      <p>还没有错题，继续保持！</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '../api/client'

interface ErrorEntry {
  word: string
  translation: string
  error_count: number
  last_attempt: string
}

const errors = ref<ErrorEntry[]>([])
const loading = ref(true)

function formatDate(d: string) {
  if (!d) return ''
  return new Date(d).toLocaleString('zh-CN', { month: 'short', day: 'numeric' })
}

onMounted(async () => {
  try {
    const res = await api.get('/words/errors')
    errors.value = res.data
  } catch {}
  loading.value = false
})
</script>
