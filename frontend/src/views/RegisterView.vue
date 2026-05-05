<template>
  <div class="min-h-[calc(100vh-3.5rem)] flex items-center justify-center px-4">
    <div class="w-full max-w-md bg-white rounded-2xl shadow-lg p-8 border border-zhixu-blue/5">
      <h2 class="font-serif text-2xl text-zhixu-blue font-bold text-center mb-6">注册知序</h2>
      <form @submit.prevent="handleRegister" class="space-y-4">
        <div>
          <label class="block text-sm text-zhixu-blue/70 mb-1">用户名</label>
          <input v-model="username" type="text" required minlength="2" maxlength="50"
            class="w-full px-4 py-2.5 border border-zhixu-blue/15 rounded-lg focus:border-zhixu-gold focus:outline-none transition" />
        </div>
        <div>
          <label class="block text-sm text-zhixu-blue/70 mb-1">邮箱</label>
          <input v-model="email" type="email" required
            class="w-full px-4 py-2.5 border border-zhixu-blue/15 rounded-lg focus:border-zhixu-gold focus:outline-none transition" />
        </div>
        <div>
          <label class="block text-sm text-zhixu-blue/70 mb-1">密码</label>
          <input v-model="password" type="password" required minlength="6"
            class="w-full px-4 py-2.5 border border-zhixu-blue/15 rounded-lg focus:border-zhixu-gold focus:outline-none transition" />
        </div>
        <div>
          <label class="block text-sm text-zhixu-blue/70 mb-1">确认密码</label>
          <input v-model="confirmPassword" type="password" required
            class="w-full px-4 py-2.5 border border-zhixu-blue/15 rounded-lg focus:border-zhixu-gold focus:outline-none transition" />
        </div>
        <p v-if="error" class="text-red-500 text-sm">{{ error }}</p>
        <button type="submit" :disabled="loading"
          class="w-full py-2.5 bg-zhixu-blue text-zhixu-cream rounded-lg hover:bg-zhixu-dark transition font-medium disabled:opacity-50">
          {{ loading ? '注册中...' : '注册（+50积分奖励）' }}
        </button>
      </form>
      <p class="text-center text-sm text-zhixu-blue/50 mt-4">
        已有账号？<router-link to="/login" class="text-zhixu-gold hover:underline">登录</router-link>
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const username = ref('')
const email = ref('')
const password = ref('')
const confirmPassword = ref('')
const error = ref('')
const loading = ref(false)

async function handleRegister() {
  error.value = ''
  if (password.value !== confirmPassword.value) {
    error.value = '两次密码不一致'
    return
  }
  loading.value = true
  try {
    await authStore.register(username.value, email.value, password.value)
    router.push('/')
  } catch (e: any) {
    error.value = e.response?.data?.detail || '注册失败'
  } finally {
    loading.value = false
  }
}
</script>
