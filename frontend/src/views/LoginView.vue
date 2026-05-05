<template>
  <div class="min-h-[calc(100vh-3.5rem)] flex items-center justify-center px-4">
    <div class="w-full max-w-md bg-white rounded-2xl shadow-lg p-8 border border-zhixu-blue/5">
      <h2 class="font-serif text-2xl text-zhixu-blue font-bold text-center mb-6">登录知序</h2>
      <form @submit.prevent="handleLogin" class="space-y-4">
        <div>
          <label class="block text-sm text-zhixu-blue/70 mb-1">邮箱</label>
          <input v-model="email" type="email" required
            class="w-full px-4 py-2.5 border border-zhixu-blue/15 rounded-lg focus:border-zhixu-gold focus:outline-none transition" />
        </div>
        <div>
          <label class="block text-sm text-zhixu-blue/70 mb-1">密码</label>
          <input v-model="password" type="password" required
            class="w-full px-4 py-2.5 border border-zhixu-blue/15 rounded-lg focus:border-zhixu-gold focus:outline-none transition" />
        </div>
        <p v-if="error" class="text-red-500 text-sm">{{ error }}</p>
        <button type="submit" :disabled="loading"
          class="w-full py-2.5 bg-zhixu-blue text-zhixu-cream rounded-lg hover:bg-zhixu-dark transition font-medium disabled:opacity-50">
          {{ loading ? '登录中...' : '登录' }}
        </button>
      </form>
      <p class="text-center text-sm text-zhixu-blue/50 mt-4">
        还没有账号？<router-link to="/register" class="text-zhixu-gold hover:underline">注册</router-link>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const route = useRoute()
const authStore = useAuthStore()
const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function handleLogin() {
  error.value = ''
  loading.value = true
  try {
    await authStore.login(email.value, password.value)
    const redirect = route.query.redirect as string || '/'
    router.push(redirect)
  } catch (e: any) {
    error.value = e.response?.data?.detail || '登录失败'
  } finally {
    loading.value = false
  }
}
</script>
