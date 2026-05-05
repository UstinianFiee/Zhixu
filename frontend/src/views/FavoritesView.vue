<template>
  <div class="max-w-4xl mx-auto px-4 py-8">
    <h2 class="font-serif text-2xl text-zhixu-blue font-bold mb-6">我的收藏</h2>
    <div v-if="favorites.length > 0" class="space-y-4">
      <div v-for="item in favorites" :key="item.id"
        class="bg-white rounded-2xl shadow-sm border border-zhixu-blue/5 p-6 hover:shadow-md transition cursor-pointer"
        @click="toggleExpand(item.id)">
        <div class="flex items-start justify-between mb-2">
          <div class="flex items-center gap-2 min-w-0">
            <span class="text-xs px-2 py-0.5 rounded-full shrink-0"
              :class="typeClass(item.content_type)">
              {{ typeLabel(item.content_type) }}
            </span>
            <h3 class="font-serif text-lg text-zhixu-blue font-semibold truncate">{{ item.title }}</h3>
          </div>
          <button @click.stop="removeFavorite(item)" class="text-red-400 hover:text-red-500 transition shrink-0 ml-2" title="取消收藏">
            <svg class="w-5 h-5" fill="currentColor" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
          </button>
        </div>
        <p class="text-zhixu-blue/70 leading-relaxed whitespace-pre-line"
          :class="{ 'line-clamp-3': !expandedIds[item.id] && item.content.length > 200 }">{{ item.content }}</p>
        <div class="flex items-center justify-between mt-3">
          <span class="text-sm text-zhixu-blue/40">{{ item.author || '' }}</span>
          <div class="flex items-center gap-3">
            <span v-if="item.content.length > 200" class="text-xs text-zhixu-gold">
              {{ expandedIds[item.id] ? '收起' : '展开全文' }}
            </span>
            <span class="text-xs text-zhixu-blue/30">{{ formatDate(item.created_at) }}</span>
          </div>
        </div>
      </div>
    </div>
    <div v-else-if="!loading" class="text-center py-16 text-zhixu-blue/40">
      <svg class="w-12 h-12 mx-auto mb-3 text-zhixu-blue/20" fill="none" stroke="currentColor" stroke-width="1.2" viewBox="0 0 24 24"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"/></svg>
      <p>还没有收藏内容</p>
      <p class="text-sm mt-1">在首页点击心形图标即可收藏</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '../api/client'

interface FavoriteItem {
  id: number
  content_type: string
  content_id: number
  created_at: string
  title: string
  content: string
  author: string | null
}

const favorites = ref<FavoriteItem[]>([])
const loading = ref(true)
const expandedIds = ref<Record<number, boolean>>({})

function toggleExpand(id: number) {
  expandedIds.value[id] = !expandedIds.value[id]
}

function typeLabel(t: string) {
  return { quote: '金句', song: '音乐', article: '文章' }[t] || t
}

function typeClass(t: string) {
  if (t === 'quote') return 'bg-zhixu-gold/10 text-zhixu-gold'
  if (t === 'song') return 'bg-purple-50 text-purple-500'
  return 'bg-green-50 text-green-600'
}

function formatDate(d: string) {
  if (!d) return ''
  return new Date(d).toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' })
}

async function removeFavorite(item: FavoriteItem) {
  await api.post(`/content/${item.content_type}/${item.content_id}/favorite`)
  favorites.value = favorites.value.filter(f => f.id !== item.id)
}

onMounted(async () => {
  try {
    const res = await api.get('/favorites')
    favorites.value = res.data
  } catch {}
  loading.value = false
})
</script>
