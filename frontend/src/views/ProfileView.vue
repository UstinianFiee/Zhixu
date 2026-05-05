<template>
  <div class="max-w-3xl mx-auto px-4 py-8">
    <div class="bg-white rounded-2xl shadow-sm border border-zhixu-blue/5 p-6 sm:p-8">
      <!-- Profile Header -->
      <div class="flex items-center gap-4 sm:gap-6 mb-8">
        <div class="relative group cursor-pointer shrink-0" @click="showAvatarInput = !showAvatarInput">
          <!-- Preview or current avatar -->
          <div class="w-20 h-20 rounded-full overflow-hidden border-2 border-zhixu-gold/30">
            <img v-if="previewUrl || authStore.user?.avatar_url"
              :src="previewUrl || authStore.user?.avatar_url"
              class="w-full h-full object-cover"
              @error="(e: any) => e.target.style.display='none'" />
            <div v-else class="w-full h-full bg-zhixu-blue/10 flex items-center justify-center text-3xl font-bold text-zhixu-blue">
              {{ (authStore.user?.nickname || authStore.user?.username || '?').charAt(0).toUpperCase() }}
            </div>
          </div>
          <div class="absolute inset-0 rounded-full bg-black/30 opacity-0 group-hover:opacity-100 transition flex items-center justify-center">
            <svg class="w-6 h-6 text-white" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="M6.827 6.175A2.31 2.31 0 0 1 5.186 7.23c-.38.054-.757.112-1.134.175C2.999 7.58 2.25 8.507 2.25 9.574V18a2.25 2.25 0 0 0 2.25 2.25h15A2.25 2.25 0 0 0 21.75 18V9.574c0-1.067-.75-1.994-1.802-2.169a47.865 47.865 0 0 0-1.134-.175 2.31 2.31 0 0 1-1.64-1.055l-.822-1.316a2.192 2.192 0 0 0-1.736-1.039 48.774 48.774 0 0 0-5.232 0 2.192 2.192 0 0 0-1.736 1.039l-.821 1.316Z"/><path d="M16.5 12.75a4.5 4.5 0 1 1-9 0 4.5 4.5 0 0 1 9 0ZM18.75 10.5h.008v.008h-.008V10.5Z"/></svg>
          </div>
          <!-- Upload progress overlay -->
          <div v-if="uploading" class="absolute inset-0 rounded-full bg-black/50 flex items-center justify-center">
            <svg class="w-8 h-8 animate-spin text-white" fill="none" viewBox="0 0 24 24">
              <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
              <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
            </svg>
          </div>
        </div>
        <div class="flex-1 min-w-0">
          <div v-if="!editingNickname" class="flex items-center gap-2">
            <h2 class="text-2xl font-serif text-zhixu-blue font-bold truncate">{{ authStore.user?.nickname || authStore.user?.username }}</h2>
            <button @click="startEditNickname" class="text-zhixu-blue/30 hover:text-zhixu-gold transition shrink-0">
              <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="m16.862 4.487 1.687-1.688a1.875 1.875 0 1 1 2.652 2.652L10.582 16.07a4.5 4.5 0 0 1-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 0 1 1.13-1.897l8.932-8.931Zm0 0L19.5 7.125"/></svg>
            </button>
          </div>
          <div v-else class="flex items-center gap-2">
            <input v-model="nicknameInput" maxlength="50" placeholder="输入昵称"
              class="px-3 py-1 border border-zhixu-blue/20 rounded-lg text-lg font-serif text-zhixu-blue focus:border-zhixu-gold focus:outline-none"
              @keydown.enter="saveNickname" ref="nicknameRef" />
            <button @click="saveNickname" class="text-sm text-zhixu-gold hover:underline">保存</button>
            <button @click="editingNickname = false" class="text-sm text-zhixu-blue/40 hover:text-zhixu-blue">取消</button>
          </div>
          <p class="text-zhixu-blue/50 text-sm mt-1 truncate">{{ authStore.user?.email }}</p>
          <div class="flex items-center gap-3 mt-2">
            <span class="px-3 py-1 bg-zhixu-gold/10 text-zhixu-gold rounded-full text-sm font-medium">
              Lv.{{ authStore.user?.current_level }} {{ levelTitle }}
            </span>
            <span class="text-sm text-zhixu-blue/60">{{ authStore.user?.total_points }} 积分</span>
          </div>
        </div>
      </div>

      <!-- Avatar input -->
      <div v-if="showAvatarInput" class="mb-6 p-4 bg-zhixu-cream/50 rounded-xl space-y-4">
        <!-- Local upload -->
        <div>
          <p class="text-xs text-zhixu-blue/50 mb-2">上传本地图片</p>
          <label class="inline-flex items-center gap-2 px-4 py-2 bg-white border border-zhixu-blue/15 rounded-lg text-sm cursor-pointer hover:border-zhixu-gold transition">
            <svg class="w-4 h-4 text-zhixu-blue/50" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><path d="M3 16.5v2.25A2.25 2.25 0 0 0 5.25 21h13.5A2.25 2.25 0 0 0 21 18.75V16.5m-13.5-9L12 3m0 0 4.5 4.5M12 3v13.5"/></svg>
            选择图片
            <input type="file" accept="image/*" class="hidden" @change="handleFileSelect" />
          </label>
          <!-- Preview + save -->
          <div v-if="previewUrl" class="mt-3 flex items-center gap-3">
            <img :src="previewUrl" class="w-12 h-12 rounded-full object-cover border border-zhixu-blue/10" />
            <button @click="saveLocalAvatar" :disabled="uploading"
              class="px-4 py-1.5 bg-zhixu-gold text-zhixu-dark rounded-lg text-sm font-medium hover:bg-yellow-400 transition disabled:opacity-40">
              {{ uploading ? '上传中...' : '使用此头像' }}
            </button>
            <button @click="previewUrl = ''" class="text-sm text-zhixu-blue/40 hover:text-zhixu-blue">取消</button>
          </div>
        </div>

        <div class="flex items-center gap-2 text-zhixu-blue/30 text-xs"><span class="flex-1 border-t border-zhixu-blue/10"></span>或<span class="flex-1 border-t border-zhixu-blue/10"></span></div>

        <!-- URL input -->
        <div>
          <p class="text-xs text-zhixu-blue/50 mb-2">输入图片链接</p>
          <div class="flex gap-2">
            <input v-model="avatarUrl" placeholder="https://example.com/avatar.jpg"
              @keydown.enter="saveAvatarUrl"
              class="flex-1 px-3 py-2 border border-zhixu-blue/15 rounded-lg text-sm focus:border-zhixu-gold focus:outline-none" />
            <button @click="saveAvatarUrl" :disabled="savingUrl || !avatarUrl.trim()"
              class="px-4 py-2 bg-zhixu-gold text-zhixu-dark rounded-lg text-sm font-medium hover:bg-yellow-400 transition disabled:opacity-40">
              {{ savingUrl ? '保存中...' : '保存' }}
            </button>
          </div>
          <!-- URL preview -->
          <div v-if="avatarUrl.trim() && avatarUrl.trim().startsWith('http')" class="mt-2 flex items-center gap-2">
            <img :src="avatarUrl.trim()" class="w-10 h-10 rounded-full object-cover border border-zhixu-blue/10"
              @error="(e: any) => e.target.style.display='none'" />
            <span class="text-xs text-zhixu-blue/40">预览</span>
          </div>
        </div>

        <button @click="showAvatarInput = false; previewUrl = ''" class="text-sm text-zhixu-blue/40 hover:text-zhixu-blue">收起</button>

        <!-- Status message -->
        <p v-if="avatarMsg" :class="['text-sm', avatarMsgOk ? 'text-green-600' : 'text-red-500']">{{ avatarMsg }}</p>
      </div>

      <!-- Stats -->
      <div class="grid grid-cols-3 gap-3 sm:gap-4 mb-8">
        <div class="text-center p-3 sm:p-4 bg-zhixu-cream rounded-xl">
          <div class="text-xl sm:text-2xl font-bold text-zhixu-gold">{{ authStore.user?.total_points || 0 }}</div>
          <div class="text-xs text-zhixu-blue/50 mt-1">总积分</div>
        </div>
        <div class="text-center p-3 sm:p-4 bg-zhixu-cream rounded-xl">
          <div class="text-xl sm:text-2xl font-bold text-zhixu-blue">Lv.{{ authStore.user?.current_level || 1 }}</div>
          <div class="text-xs text-zhixu-blue/50 mt-1">等级</div>
        </div>
        <div class="text-center p-3 sm:p-4 bg-zhixu-cream rounded-xl">
          <div class="text-xl sm:text-2xl font-bold text-green-600">{{ pointsRank }}</div>
          <div class="text-xs text-zhixu-blue/50 mt-1">排名</div>
        </div>
      </div>

      <!-- Points History -->
      <h3 class="font-serif text-lg text-zhixu-blue mb-4">积分历史</h3>
      <div class="space-y-2 max-h-64 overflow-y-auto">
        <div v-for="item in history" :key="item.id"
          class="flex items-center justify-between py-2 px-3 rounded-lg hover:bg-zhixu-cream/50 transition">
          <div>
            <span class="text-sm text-zhixu-blue">{{ reasonMap[item.reason] || item.reason }}</span>
            <span class="text-xs text-zhixu-blue/40 ml-2">{{ formatDate(item.created_at) }}</span>
          </div>
          <span :class="item.points_change > 0 ? 'text-green-600' : 'text-red-500'" class="font-medium">
            {{ item.points_change > 0 ? '+' : '' }}{{ item.points_change }}
          </span>
        </div>
        <p v-if="history.length === 0" class="text-center text-zhixu-blue/40 py-4">暂无积分记录</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick, computed } from 'vue'
import { useAuthStore } from '../stores/auth'
import api from '../api/client'

const authStore = useAuthStore()
const history = ref<any[]>([])
const pointsRank = ref('-')
const editingNickname = ref(false)
const nicknameInput = ref('')
const nicknameRef = ref<HTMLInputElement>()
const showAvatarInput = ref(false)
const avatarUrl = ref('')
const previewUrl = ref('')
const uploading = ref(false)
const savingUrl = ref(false)
const avatarMsg = ref('')
const avatarMsgOk = ref(true)

const LEVEL_TITLES: Record<number, string> = {
  1: '文艺学徒', 2: '单词小生', 3: '笔墨行者', 4: '浮光阅者', 5: '英文探路者',
  6: '星夜记忆者', 7: '轻文艺学士', 8: '键盘诗人', 9: '安宁守护者', 10: '独行大师'
}

const reasonMap: Record<string, string> = {
  new_user_register: '新用户注册奖励',
  word_practice: '单词练习',
  session_complete: '完成一组练习',
  favorite_content: '收藏内容',
  daily_checkin: '每日打卡',
  read_article: '阅读文章',
  streak_bonus: '连续正确奖励',
  demo_init: '示范账号初始化',
}

const levelTitle = computed(() => LEVEL_TITLES[authStore.user?.current_level || 1] || '')

function formatDate(d: string) {
  return new Date(d).toLocaleString('zh-CN', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })
}

function startEditNickname() {
  nicknameInput.value = authStore.user?.nickname || authStore.user?.username || ''
  editingNickname.value = true
  nextTick(() => nicknameRef.value?.focus())
}

async function saveNickname() {
  if (!nicknameInput.value.trim()) return
  try {
    const res = await api.put('/auth/profile', { nickname: nicknameInput.value.trim() })
    authStore.user = res.data
    localStorage.setItem('zhixu_user', JSON.stringify(res.data))
    editingNickname.value = false
  } catch {}
}

function handleFileSelect(e: Event) {
  const file = (e.target as HTMLInputElement).files?.[0]
  if (!file) return
  avatarMsg.value = ''

  // Compress and preview
  const reader = new FileReader()
  reader.onload = () => {
    const img = new Image()
    img.onload = () => {
      const canvas = document.createElement('canvas')
      const size = 128
      canvas.width = size
      canvas.height = size
      const ctx = canvas.getContext('2d')!
      // Center crop
      const min = Math.min(img.width, img.height)
      const sx = (img.width - min) / 2
      const sy = (img.height - min) / 2
      ctx.drawImage(img, sx, sy, min, min, 0, 0, size, size)
      previewUrl.value = canvas.toDataURL('image/jpeg', 0.8)
    }
    img.src = reader.result as string
  }
  reader.readAsDataURL(file)
}

async function saveLocalAvatar() {
  if (!previewUrl.value) return
  uploading.value = true
  avatarMsg.value = ''
  try {
    const res = await api.put('/auth/profile', { avatar_url: previewUrl.value })
    authStore.user = res.data
    localStorage.setItem('zhixu_user', JSON.stringify(res.data))
    previewUrl.value = ''
    showAvatarInput.value = false
    avatarMsg.value = '头像更新成功'
    avatarMsgOk.value = true
  } catch (err: any) {
    avatarMsg.value = err.response?.data?.detail || '上传失败'
    avatarMsgOk.value = false
  } finally {
    uploading.value = false
  }
}

async function saveAvatarUrl() {
  if (!avatarUrl.value.trim()) return
  savingUrl.value = true
  avatarMsg.value = ''
  try {
    const res = await api.put('/auth/profile', { avatar_url: avatarUrl.value.trim() })
    authStore.user = res.data
    localStorage.setItem('zhixu_user', JSON.stringify(res.data))
    showAvatarInput.value = false
    avatarUrl.value = ''
    avatarMsg.value = '头像更新成功'
    avatarMsgOk.value = true
  } catch (err: any) {
    avatarMsg.value = err.response?.data?.detail || '保存失败'
    avatarMsgOk.value = false
  } finally {
    savingUrl.value = false
  }
}

onMounted(async () => {
  try {
    const res = await api.get('/points/history')
    history.value = res.data.items
    const rankRes = await api.get('/points/rank/me')
    pointsRank.value = '#' + rankRes.data.rank
  } catch {}
})
</script>
