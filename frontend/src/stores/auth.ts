import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../api/client'

export interface User {
  id: number
  username: string
  nickname: string | null
  email: string
  total_points: number
  current_level: number
  is_admin: boolean
  created_at: string
  avatar_url: string | null
}

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const accessToken = ref<string | null>(null)
  const refreshToken = ref<string | null>(null)

  const isLoggedIn = computed(() => !!accessToken.value)

  function loadFromStorage() {
    const token = localStorage.getItem('zhixu_access_token')
    const userData = localStorage.getItem('zhixu_user')
    const refresh = localStorage.getItem('zhixu_refresh_token')
    if (token && userData) {
      accessToken.value = token
      refreshToken.value = refresh
      user.value = JSON.parse(userData)
    }
  }

  async function login(email: string, password: string) {
    const res = await api.post('/auth/login', { email, password })
    const data = res.data
    accessToken.value = data.access_token
    refreshToken.value = data.refresh_token
    user.value = data.user
    localStorage.setItem('zhixu_access_token', data.access_token)
    localStorage.setItem('zhixu_refresh_token', data.refresh_token)
    localStorage.setItem('zhixu_user', JSON.stringify(data.user))
    return data
  }

  async function register(username: string, email: string, password: string) {
    const res = await api.post('/auth/register', { username, email, password })
    const data = res.data
    accessToken.value = data.access_token
    refreshToken.value = data.refresh_token
    user.value = data.user
    localStorage.setItem('zhixu_access_token', data.access_token)
    localStorage.setItem('zhixu_refresh_token', data.refresh_token)
    localStorage.setItem('zhixu_user', JSON.stringify(data.user))
    return data
  }

  function logout() {
    user.value = null
    accessToken.value = null
    refreshToken.value = null
    localStorage.removeItem('zhixu_access_token')
    localStorage.removeItem('zhixu_refresh_token')
    localStorage.removeItem('zhixu_user')
  }

  function updatePoints(points: number, level: number) {
    if (user.value) {
      user.value.total_points = points
      user.value.current_level = level
      localStorage.setItem('zhixu_user', JSON.stringify(user.value))
    }
  }

  return { user, accessToken, refreshToken, isLoggedIn, loadFromStorage, login, register, logout, updatePoints }
})
