<template>
  <div class="daily-card">
    <div class="flex items-center gap-2 mb-4">
      <svg class="w-4 h-4 text-zhixu-gold" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" v-html="icons.star"></svg>
      <span class="text-xs text-zhixu-gold font-medium tracking-widest uppercase">每日一句</span>
    </div>
    <div v-if="quote" class="flex flex-col flex-1 min-h-0">
      <blockquote class="font-serif text-xl sm:text-2xl leading-relaxed text-zhixu-blue/90 italic flex-1 line-clamp-5">
        "{{ quote.content }}"
      </blockquote>
      <div class="flex items-center justify-between mt-4 pt-4 border-t border-zhixu-blue/5">
        <span class="text-sm text-zhixu-blue/50 truncate mr-2">{{ quote.author || '知序' }}</span>
        <button @click="handleFavorite" class="shrink-0 transition" :class="favorited ? 'text-red-400' : 'text-zhixu-blue/20 hover:text-red-300'">
          <svg class="w-5 h-5" :fill="favorited ? 'currentColor' : 'none'" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" v-html="icons.heart"></svg>
        </button>
      </div>
    </div>
    <div v-else class="flex-1 flex items-center justify-center text-zhixu-blue/40">加载中...</div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useDailyStore, type DailyContent } from '../stores/daily'
import { icons } from './icons'

const dailyStore = useDailyStore()
const quote = ref<DailyContent | null>(null)
const favorited = ref(false)

async function handleFavorite() {
  if (!quote.value) return
  const res = await dailyStore.favorite('quote', quote.value.id)
  favorited.value = res.favorited
}

onMounted(async () => {
  await dailyStore.fetchQuote()
  quote.value = dailyStore.quote
  if (quote.value) {
    favorited.value = await dailyStore.checkFavorite('quote', quote.value.id)
  }
})
</script>
