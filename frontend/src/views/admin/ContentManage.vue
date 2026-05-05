<template>
  <div>
    <div class="flex items-center justify-between mb-6">
      <h2 class="font-serif text-xl text-zhixu-blue font-bold">内容管理</h2>
      <button @click="showCreate = !showCreate" class="px-4 py-2 bg-zhixu-blue text-zhixu-cream rounded-lg text-sm hover:bg-zhixu-dark transition">
        发布内容
      </button>
    </div>

    <!-- Create Form -->
    <div v-if="showCreate" class="bg-white rounded-xl p-4 sm:p-6 border border-zhixu-blue/5 mb-6 space-y-3">
      <h3 class="text-sm font-medium text-zhixu-blue">发布内容</h3>
      <div class="flex flex-col sm:flex-row gap-3">
        <select v-model="formData.type" class="px-3 py-2 border border-zhixu-blue/15 rounded-lg text-sm focus:border-zhixu-gold focus:outline-none">
          <option value="quote">每日一句</option>
          <option value="song">每日一曲</option>
          <option value="article">每日一文</option>
        </select>
        <input v-model="formData.date" type="date" class="px-3 py-2 border border-zhixu-blue/15 rounded-lg text-sm focus:border-zhixu-gold focus:outline-none" />
      </div>
      <input v-model="formData.title" placeholder="标题" class="w-full px-3 py-2 border border-zhixu-blue/15 rounded-lg text-sm focus:border-zhixu-gold focus:outline-none" />
      <textarea v-model="formData.content" placeholder="内容" rows="4" class="w-full px-3 py-2 border border-zhixu-blue/15 rounded-lg text-sm focus:border-zhixu-gold focus:outline-none resize-y"></textarea>
      <input v-model="formData.author" placeholder="作者" class="w-full px-3 py-2 border border-zhixu-blue/15 rounded-lg text-sm focus:border-zhixu-gold focus:outline-none" />
      <div class="flex gap-3">
        <button @click="saveContent" class="px-4 py-2 bg-zhixu-gold text-zhixu-dark rounded-lg text-sm font-medium hover:bg-yellow-400 transition">发布</button>
        <button @click="showCreate = false" class="px-4 py-2 border border-zhixu-blue/15 text-zhixu-blue rounded-lg text-sm hover:bg-zhixu-blue/5 transition">取消</button>
      </div>
    </div>

    <!-- Filter -->
    <div class="flex gap-2 mb-4 overflow-x-auto pb-1">
      <button v-for="f in filters" :key="f.value" @click="activeFilter = f.value"
        class="shrink-0 px-3 py-1.5 rounded-full text-xs font-medium transition"
        :class="activeFilter === f.value ? 'bg-zhixu-blue text-zhixu-cream' : 'bg-white border border-zhixu-blue/10 text-zhixu-blue/60 hover:border-zhixu-gold'">
        {{ f.label }}
      </button>
    </div>

    <!-- Content List -->
    <div class="space-y-3">
      <div v-for="item in filteredContents" :key="item.id" class="bg-white rounded-xl border border-zhixu-blue/5 overflow-hidden">
        <div class="p-4 sm:p-5">
          <div class="flex items-start justify-between gap-2">
            <div class="flex-1 min-w-0">
              <div class="flex items-center gap-2 mb-1">
                <span class="text-xs px-2 py-0.5 rounded-full" :class="typeClass(item.type)">{{ typeLabel(item.type) }}</span>
                <span class="text-xs text-zhixu-blue/40">{{ item.date }}</span>
              </div>
              <h4 class="font-medium text-zhixu-blue">{{ item.title }}</h4>
              <p class="text-sm text-zhixu-blue/60 mt-1 line-clamp-2">{{ item.content }}</p>
              <span v-if="item.author" class="text-xs text-zhixu-blue/40 mt-1">—— {{ item.author }}</span>
            </div>
            <div class="flex gap-1 shrink-0">
              <button @click="startEdit(item)" class="px-2 py-1 text-xs bg-zhixu-gold/10 text-zhixu-gold rounded hover:bg-zhixu-gold/20 transition">编辑</button>
              <button @click="deleteContent(item)" class="px-2 py-1 text-xs bg-red-50 text-red-500 rounded hover:bg-red-100 transition">删除</button>
            </div>
          </div>
        </div>
        <!-- Inline Edit Form -->
        <div v-if="editing === item.id" class="border-t border-zhixu-blue/5 p-4 sm:p-5 space-y-3 bg-zhixu-cream/30">
          <div class="flex flex-col sm:flex-row gap-3">
            <select v-model="editData.type" class="px-3 py-2 border border-zhixu-blue/15 rounded-lg text-sm focus:border-zhixu-gold focus:outline-none bg-white">
              <option value="quote">每日一句</option>
              <option value="song">每日一曲</option>
              <option value="article">每日一文</option>
            </select>
            <input v-model="editData.date" type="date" class="px-3 py-2 border border-zhixu-blue/15 rounded-lg text-sm focus:border-zhixu-gold focus:outline-none bg-white" />
          </div>
          <input v-model="editData.title" placeholder="标题" class="w-full px-3 py-2 border border-zhixu-blue/15 rounded-lg text-sm focus:border-zhixu-gold focus:outline-none bg-white" />
          <textarea v-model="editData.content" placeholder="内容" rows="4" class="w-full px-3 py-2 border border-zhixu-blue/15 rounded-lg text-sm focus:border-zhixu-gold focus:outline-none resize-y bg-white"></textarea>
          <input v-model="editData.author" placeholder="作者" class="w-full px-3 py-2 border border-zhixu-blue/15 rounded-lg text-sm focus:border-zhixu-gold focus:outline-none bg-white" />
          <div class="flex gap-3">
            <button @click="saveEdit" class="px-4 py-2 bg-zhixu-gold text-zhixu-dark rounded-lg text-sm font-medium hover:bg-yellow-400 transition">保存</button>
            <button @click="editing = null" class="px-4 py-2 border border-zhixu-blue/15 text-zhixu-blue rounded-lg text-sm hover:bg-zhixu-blue/5 transition">取消</button>
          </div>
        </div>
      </div>
      <p v-if="filteredContents.length === 0" class="text-center text-zhixu-blue/40 py-8">暂无内容</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, computed, onMounted } from 'vue'
import api from '../../api/client'

const contents = ref<any[]>([])
const showCreate = ref(false)
const editing = ref<number | null>(null)
const activeFilter = ref('all')

const filters = [
  { label: '全部', value: 'all' },
  { label: '金句', value: 'quote' },
  { label: '歌曲', value: 'song' },
  { label: '文章', value: 'article' },
]

const formData = reactive({
  date: new Date().toISOString().slice(0, 10),
  type: 'quote',
  title: '',
  content: '',
  author: '',
})

const editData = reactive({
  date: '',
  type: 'quote',
  title: '',
  content: '',
  author: '',
})

const filteredContents = computed(() => {
  if (activeFilter.value === 'all') return contents.value
  return contents.value.filter(c => c.type === activeFilter.value)
})

function typeLabel(t: string) {
  return { quote: '金句', song: '歌曲', article: '文章' }[t] || t
}
function typeClass(t: string) {
  return { quote: 'bg-zhixu-gold/10 text-zhixu-gold', song: 'bg-blue-50 text-blue-500', article: 'bg-green-50 text-green-600' }[t] || ''
}

function startEdit(item: any) {
  editing.value = item.id
  editData.date = item.date
  editData.type = item.type
  editData.title = item.title
  editData.content = item.content
  editData.author = item.author || ''
}

async function fetchData() {
  const res = await api.get('/admin/content')
  contents.value = res.data
}

async function saveContent() {
  if (!formData.title.trim() || !formData.content.trim()) return
  await api.post('/admin/content', { ...formData })
  formData.title = ''
  formData.content = ''
  formData.author = ''
  showCreate.value = false
  await fetchData()
}

async function saveEdit() {
  if (!editData.title.trim() || !editData.content.trim()) return
  await api.put(`/admin/content/${editing.value}`, { ...editData })
  editing.value = null
  await fetchData()
}

async function deleteContent(item: any) {
  if (!confirm(`确定删除「${item.title}」？`)) return
  await api.delete(`/admin/content/${item.id}`)
  await fetchData()
}

onMounted(fetchData)
</script>
