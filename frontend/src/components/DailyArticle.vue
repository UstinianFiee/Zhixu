<template>
  <div class="daily-card">
    <div class="flex items-center gap-2 mb-4">
      <svg class="w-4 h-4 text-zhixu-blue/40" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" v-html="icons.book"></svg>
      <span class="text-xs text-zhixu-blue/50 font-medium tracking-widest uppercase">每日一文</span>
    </div>
    <div v-if="article" class="flex flex-col flex-1 min-h-0">
      <h3 class="font-serif text-xl text-zhixu-blue font-semibold mb-3">{{ article.title }}</h3>
      <div class="text-zhixu-blue/70 leading-relaxed whitespace-pre-line flex-1 line-clamp-5">{{ article.content }}</div>
      <div class="flex items-center justify-between mt-4 pt-4 border-t border-zhixu-blue/5">
        <span class="text-sm text-zhixu-blue/50 truncate mr-2">{{ article.author || '未知' }}</span>
        <div class="flex gap-3 items-center shrink-0">
          <button @click="showModal = true" class="text-sm text-zhixu-gold hover:underline">
            阅读全文
          </button>
          <button @click="handleFavorite" class="transition" :class="favorited ? 'text-red-400' : 'text-zhixu-blue/20 hover:text-red-300'">
            <svg class="w-5 h-5" :fill="favorited ? 'currentColor' : 'none'" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24" v-html="icons.heart"></svg>
          </button>
        </div>
      </div>
    </div>
    <div v-else class="flex-1 flex items-center justify-center text-zhixu-blue/40">加载中...</div>

    <!-- Modal -->
    <Teleport to="body">
      <Transition name="fade">
        <div v-if="showModal" class="fixed inset-0 z-50 flex items-center justify-center p-4" @click.self="showModal = false">
          <div class="fixed inset-0 bg-black/40 backdrop-blur-sm"></div>
          <div class="relative bg-white rounded-2xl shadow-xl max-w-2xl w-full max-h-[80vh] overflow-y-auto p-8 z-10">
            <button @click="showModal = false" class="absolute top-4 right-4 text-zhixu-blue/30 hover:text-zhixu-blue transition">
              <svg class="w-6 h-6" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="M18 6 6 18M6 6l12 12"/></svg>
            </button>
            <h2 class="font-serif text-2xl text-zhixu-blue font-bold mb-2">{{ article?.title }}</h2>
            <div class="text-sm text-zhixu-blue/50 mb-6">{{ article?.author || '未知' }}</div>
            <div class="text-zhixu-blue/80 leading-loose whitespace-pre-line text-base">{{ article?.content }}</div>
          </div>
        </div>
      </Transition>
    </Teleport>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useDailyStore, type DailyContent } from '../stores/daily'
import { icons } from './icons'

const dailyStore = useDailyStore()
const article = ref<DailyContent | null>(null)
const favorited = ref(false)
const showModal = ref(false)

async function handleFavorite() {
  if (!article.value) return
  const res = await dailyStore.favorite('article', article.value.id)
  favorited.value = res.favorited
}

onMounted(async () => {
  await dailyStore.fetchArticle()
  article.value = dailyStore.article
  if (article.value) {
    favorited.value = await dailyStore.checkFavorite('article', article.value.id)
  }
})
</script>
