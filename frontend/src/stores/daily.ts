import { defineStore } from 'pinia'
import { ref } from 'vue'
import api from '../api/client'

export interface DailyContent {
  id: number
  date: string
  type: string
  title: string
  content: string
  author: string | null
  source_url: string | null
  cover_url: string | null
}

export const useDailyStore = defineStore('daily', () => {
  const quote = ref<DailyContent | null>(null)
  const song = ref<DailyContent | null>(null)
  const article = ref<DailyContent | null>(null)
  const loading = ref(false)

  async function fetchQuote() {
    loading.value = true
    try {
      const res = await api.get('/daily/quote')
      quote.value = res.data
    } finally { loading.value = false }
  }

  async function fetchSong() {
    loading.value = true
    try {
      const res = await api.get('/daily/song')
      song.value = res.data
    } finally { loading.value = false }
  }

  async function fetchArticle() {
    loading.value = true
    try {
      const res = await api.get('/daily/article')
      article.value = res.data
    } finally { loading.value = false }
  }

  async function favorite(type: string, id: number) {
    const res = await api.post(`/content/${type}/${id}/favorite`)
    return res.data
  }

  async function checkFavorite(type: string, id: number): Promise<boolean> {
    try {
      const token = localStorage.getItem('zhixu_access_token')
      if (!token) return false
      const res = await api.get(`/favorites/check/${type}/${id}`)
      return res.data.favorited
    } catch {
      return false
    }
  }

  return { quote, song, article, loading, fetchQuote, fetchSong, fetchArticle, favorite, checkFavorite }
})
