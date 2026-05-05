<template>
  <div class="daily-card">
    <div class="flex items-center gap-2 mb-4">
      <svg class="w-4 h-4 text-zhixu-blue/40" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" v-html="icons.volume"></svg>
      <span class="text-xs text-zhixu-blue/50 font-medium tracking-widest uppercase">每日一曲</span>
    </div>
    <div v-if="song" class="flex flex-col flex-1 min-h-0">
      <h3 class="font-serif text-xl text-zhixu-blue font-semibold mb-3">{{ song.title }}</h3>
      <p class="text-zhixu-blue/70 leading-relaxed flex-1 line-clamp-5">{{ song.content }}</p>
      <div class="flex items-center justify-between mt-4 pt-4 border-t border-zhixu-blue/5">
        <span class="text-sm text-zhixu-blue/50 truncate mr-2">{{ song.author || '未知' }}</span>
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
const song = ref<DailyContent | null>(null)
const favorited = ref(false)

async function handleFavorite() {
  if (!song.value) return
  const res = await dailyStore.favorite('song', song.value.id)
  favorited.value = res.favorited
}

onMounted(async () => {
  await dailyStore.fetchSong()
  song.value = dailyStore.song
  if (song.value) {
    favorited.value = await dailyStore.checkFavorite('song', song.value.id)
  }
})
</script>
