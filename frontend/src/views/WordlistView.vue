<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <h2 class="font-serif text-2xl text-zhixu-blue font-bold mb-6">词库列表</h2>
    <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
      <div v-for="wl in wordlists" :key="wl.id"
        class="bg-white rounded-2xl shadow-sm border border-zhixu-blue/5 p-6 hover:shadow-md transition group">
        <div class="flex items-start justify-between mb-3">
          <h3 class="font-sans text-xl text-zhixu-blue font-semibold group-hover:text-zhixu-gold transition">
            {{ wl.name }}
          </h3>
          <span class="text-xs px-2 py-1 bg-zhixu-gold/10 text-zhixu-gold rounded-full">
            {{ wl.word_count }} 词
          </span>
        </div>
        <p class="text-sm text-zhixu-blue/60 mb-4">{{ wl.description }}</p>
        <div class="flex gap-2">
          <router-link :to="`/wordlists/${wl.id}/practice`"
            class="flex-1 text-center py-2 bg-zhixu-blue text-zhixu-cream rounded-lg text-sm font-medium hover:bg-zhixu-dark transition">
            打字练习
          </router-link>
          <router-link :to="`/wordlists/${wl.id}/dictation`"
            class="flex-1 text-center py-2 border border-zhixu-blue/20 text-zhixu-blue rounded-lg text-sm font-medium hover:bg-zhixu-blue/5 transition">
            默写模式
          </router-link>
        </div>
      </div>
    </div>
    <p v-if="wordlists.length === 0 && !loading" class="text-center text-zhixu-blue/40 py-12">暂无词库</p>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '../api/client'

interface WordList {
  id: number
  name: string
  description: string | null
  word_count: number
  is_preset: boolean
}

const wordlists = ref<WordList[]>([])
const loading = ref(true)

onMounted(async () => {
  try {
    const res = await api.get('/wordlists')
    wordlists.value = res.data
  } finally {
    loading.value = false
  }
})
</script>
