<template>
  <div>
    <h2 class="font-serif text-xl text-zhixu-blue font-bold mb-6">用户管理</h2>

    <!-- Reset Password Modal -->
    <div v-if="resetTarget" class="fixed inset-0 z-50 flex items-center justify-center p-4" @click.self="resetTarget = null">
      <div class="fixed inset-0 bg-black/30 backdrop-blur-sm"></div>
      <div class="relative bg-white rounded-2xl shadow-xl w-full max-w-sm p-6 z-10">
        <h3 class="font-medium text-zhixu-blue mb-4">重置密码 - {{ resetTarget.username }}</h3>
        <input v-model="newPassword" type="password" placeholder="输入新密码" class="w-full px-3 py-2 border border-zhixu-blue/15 rounded-lg text-sm focus:border-zhixu-gold focus:outline-none mb-4" />
        <div class="flex gap-3">
          <button @click="confirmResetPassword" class="flex-1 px-4 py-2 bg-zhixu-gold text-zhixu-dark rounded-lg text-sm font-medium hover:bg-yellow-400 transition">确认重置</button>
          <button @click="resetTarget = null" class="px-4 py-2 border border-zhixu-blue/15 text-zhixu-blue rounded-lg text-sm hover:bg-zhixu-blue/5 transition">取消</button>
        </div>
      </div>
    </div>

    <!-- Mobile: card layout -->
    <div class="sm:hidden space-y-3">
      <div v-for="user in users" :key="user.id" class="bg-white rounded-xl border border-zhixu-blue/5 p-4">
        <div class="flex items-start justify-between mb-3">
          <div>
            <div class="flex items-center gap-2">
              <span class="font-medium text-zhixu-blue">{{ user.username }}</span>
              <button @click="toggleRole(user)"
                class="px-2 py-0.5 rounded-full text-xs font-medium transition"
                :class="user.is_admin ? 'bg-zhixu-gold/10 text-zhixu-gold' : 'bg-zhixu-blue/5 text-zhixu-blue/50'">
                {{ user.is_admin ? '管理员' : '普通' }}
              </button>
            </div>
            <div class="text-xs text-zhixu-blue/50 mt-0.5">{{ user.email }}</div>
          </div>
          <div class="flex gap-1">
            <button @click="resetTarget = user; newPassword = ''" class="px-2 py-1 text-xs bg-zhixu-gold/10 text-zhixu-gold rounded">改密</button>
            <button @click="deleteUser(user)" class="px-2 py-1 text-xs bg-red-50 text-red-500 rounded">删除</button>
          </div>
        </div>
        <div class="flex gap-4 text-xs text-zhixu-blue/50">
          <span>积分 <span class="text-zhixu-gold font-medium">{{ user.total_points }}</span></span>
          <span>Lv.{{ user.current_level }}</span>
          <span>{{ formatDate(user.created_at) }}</span>
        </div>
      </div>
    </div>

    <!-- Desktop: table layout -->
    <div class="hidden sm:block bg-white rounded-xl border border-zhixu-blue/5 overflow-x-auto">
      <table class="w-full text-sm">
        <thead>
          <tr class="border-b border-zhixu-blue/10 bg-zhixu-cream/50">
            <th class="py-3 px-4 text-left text-zhixu-blue/60 font-medium">ID</th>
            <th class="py-3 px-4 text-left text-zhixu-blue/60 font-medium">用户名</th>
            <th class="py-3 px-4 text-left text-zhixu-blue/60 font-medium">邮箱</th>
            <th class="py-3 px-4 text-center text-zhixu-blue/60 font-medium">积分</th>
            <th class="py-3 px-4 text-center text-zhixu-blue/60 font-medium">等级</th>
            <th class="py-3 px-4 text-center text-zhixu-blue/60 font-medium">身份</th>
            <th class="py-3 px-4 text-center text-zhixu-blue/60 font-medium">注册时间</th>
            <th class="py-3 px-4 text-center text-zhixu-blue/60 font-medium">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in users" :key="user.id" class="border-b border-zhixu-blue/5 hover:bg-zhixu-cream/30">
            <td class="py-3 px-4 text-zhixu-blue/50">{{ user.id }}</td>
            <td class="py-3 px-4 font-medium text-zhixu-blue">{{ user.username }}</td>
            <td class="py-3 px-4 text-zhixu-blue/60">{{ user.email }}</td>
            <td class="py-3 px-4 text-center text-zhixu-gold font-medium">{{ user.total_points }}</td>
            <td class="py-3 px-4 text-center text-zhixu-blue/50">Lv.{{ user.current_level }}</td>
            <td class="py-3 px-4 text-center">
              <button @click="toggleRole(user)"
                class="px-2 py-0.5 rounded-full text-xs font-medium transition"
                :class="user.is_admin ? 'bg-zhixu-gold/10 text-zhixu-gold hover:bg-zhixu-gold/20' : 'bg-zhixu-blue/5 text-zhixu-blue/50 hover:bg-zhixu-blue/10'">
                {{ user.is_admin ? '管理员' : '普通用户' }}
              </button>
            </td>
            <td class="py-3 px-4 text-center text-zhixu-blue/40 text-xs">{{ formatDate(user.created_at) }}</td>
            <td class="py-3 px-4 text-center">
              <div class="flex justify-center gap-1">
                <button @click="resetTarget = user; newPassword = ''" class="px-2 py-1 text-xs bg-zhixu-gold/10 text-zhixu-gold rounded hover:bg-zhixu-gold/20 transition">改密</button>
                <button @click="deleteUser(user)" class="px-2 py-1 text-xs bg-red-50 text-red-500 rounded hover:bg-red-100 transition">删除</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import api from '../../api/client'

const users = ref<any[]>([])
const resetTarget = ref<any>(null)
const newPassword = ref('')

function formatDate(d: string) {
  return new Date(d).toLocaleString('zh-CN', { year: 'numeric', month: 'short', day: 'numeric' })
}

async function fetchData() {
  const res = await api.get('/admin/users')
  users.value = res.data
}

async function toggleRole(user: any) {
  const newRole = !user.is_admin
  const label = newRole ? '管理员' : '普通用户'
  if (!confirm(`将「${user.username}」的身份切换为${label}？`)) return
  await api.put(`/admin/users/${user.id}/role`, { is_admin: newRole })
  await fetchData()
}

async function confirmResetPassword() {
  if (!resetTarget.value || !newPassword.value.trim()) return
  await api.put(`/admin/users/${resetTarget.value.id}/password`, { password: newPassword.value })
  resetTarget.value = null
  newPassword.value = ''
}

async function deleteUser(user: any) {
  if (!confirm(`确定删除用户「${user.username}」？此操作不可撤销。`)) return
  await api.delete(`/admin/users/${user.id}`)
  await fetchData()
}

onMounted(fetchData)
</script>
