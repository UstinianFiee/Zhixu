<template>
  <div>
    <div class="flex flex-wrap items-center justify-between gap-2 mb-6">
      <h2 class="font-serif text-xl text-zhixu-blue font-bold">词库管理</h2>
      <div class="flex gap-2">
        <button @click="downloadTemplate" class="px-3 py-2 border border-zhixu-blue/15 text-zhixu-blue rounded-lg text-sm hover:bg-zhixu-blue/5 transition">
          下载模板
        </button>
        <button @click="showCreate = !showCreate" class="px-3 py-2 bg-zhixu-blue text-zhixu-cream rounded-lg text-sm hover:bg-zhixu-dark transition">
          新建词库
        </button>
      </div>
    </div>

    <!-- Create Form -->
    <div v-if="showCreate" class="bg-white rounded-xl p-4 sm:p-6 border border-zhixu-blue/5 mb-6">
      <h3 class="text-sm font-medium text-zhixu-blue mb-3">新建词库</h3>
      <div class="flex flex-col sm:flex-row gap-3">
        <input v-model="newName" placeholder="词库名称" class="flex-1 px-3 py-2 border border-zhixu-blue/15 rounded-lg text-sm focus:border-zhixu-gold focus:outline-none" />
        <input v-model="newDesc" placeholder="描述（可选）" class="flex-1 px-3 py-2 border border-zhixu-blue/15 rounded-lg text-sm focus:border-zhixu-gold focus:outline-none" />
        <button @click="createWordlist" class="px-4 py-2 bg-zhixu-gold text-zhixu-dark rounded-lg text-sm font-medium hover:bg-yellow-400 transition">创建</button>
      </div>
    </div>

    <!-- Import Words Form -->
    <div v-if="showImport" class="bg-white rounded-xl p-4 sm:p-6 border border-zhixu-blue/5 mb-6">
      <h3 class="text-sm font-medium text-zhixu-blue mb-4">导入到「{{ importTarget?.name }}」</h3>

      <!-- Mode Toggle -->
      <div class="flex gap-1 mb-4 bg-zhixu-cream/50 rounded-lg p-1 w-fit">
        <button @click="importMode = 'file'" :class="[
          'px-3 py-1.5 rounded-md text-xs font-medium transition',
          importMode === 'file' ? 'bg-white text-zhixu-blue shadow-sm' : 'text-zhixu-blue/50'
        ]">文件上传</button>
        <button @click="importMode = 'text'" :class="[
          'px-3 py-1.5 rounded-md text-xs font-medium transition',
          importMode === 'text' ? 'bg-white text-zhixu-blue shadow-sm' : 'text-zhixu-blue/50'
        ]">手动输入</button>
      </div>

      <!-- File Upload Mode -->
      <div v-if="importMode === 'file'">
        <label class="block cursor-pointer">
          <div class="border-2 border-dashed border-zhixu-blue/15 rounded-xl p-6 sm:p-8 text-center hover:border-zhixu-gold/50 hover:bg-zhixu-cream/30 transition">
            <div class="text-3xl text-zhixu-blue/20 mb-2">+</div>
            <p class="text-sm text-zhixu-blue/50">点击选择文件</p>
            <p class="text-xs text-zhixu-blue/30 mt-1">支持 txt / xlsx / docx</p>
          </div>
          <input type="file" accept=".txt,.xlsx,.xls,.docx" @change="onFileSelect" class="hidden" />
        </label>
        <div v-if="selectedFile" class="mt-3 flex items-center gap-2 text-sm text-zhixu-blue/70">
          <span class="px-2 py-0.5 bg-zhixu-blue/5 rounded text-xs uppercase">{{ fileExt }}</span>
          <span class="truncate">{{ selectedFile.name }}</span>
          <button @click="selectedFile = null" class="text-red-400 shrink-0">✕</button>
        </div>
        <div class="flex gap-3 mt-4">
          <button @click="importByFile" :disabled="!selectedFile || importing"
            class="px-4 py-2 bg-zhixu-gold text-zhixu-dark rounded-lg text-sm font-medium hover:bg-yellow-400 transition disabled:opacity-40">
            {{ importing ? '导入中...' : '导入' }}
          </button>
          <button @click="cancelImport" class="px-4 py-2 border border-zhixu-blue/15 text-zhixu-blue rounded-lg text-sm hover:bg-zhixu-blue/5 transition">取消</button>
        </div>
      </div>

      <!-- Text Input Mode -->
      <div v-else>
        <p class="text-xs text-zhixu-blue/50 mb-2">每行：单词 释义 [音标]</p>
        <textarea v-model="importText" rows="5" placeholder="abandon 放弃 /əˈbændən/&#10;ability 能力 /əˈbɪləti/"
          class="w-full px-3 py-2 border border-zhixu-blue/15 rounded-lg text-sm font-mono focus:border-zhixu-gold focus:outline-none resize-y"></textarea>
        <div class="flex gap-3 mt-3">
          <button @click="importByText" :disabled="importing"
            class="px-4 py-2 bg-zhixu-gold text-zhixu-dark rounded-lg text-sm font-medium hover:bg-yellow-400 transition disabled:opacity-40">
            {{ importing ? '导入中...' : '导入' }}
          </button>
          <button @click="cancelImport" class="px-4 py-2 border border-zhixu-blue/15 text-zhixu-blue rounded-lg text-sm hover:bg-zhixu-blue/5 transition">取消</button>
        </div>
      </div>

      <p v-if="importResult" :class="['text-sm mt-3', importResultOk ? 'text-green-600' : 'text-red-500']">{{ importResult }}</p>
    </div>

    <!-- Mobile: card layout -->
    <div class="sm:hidden space-y-3">
      <div v-for="wl in wordlists" :key="wl.id" class="bg-white rounded-xl border border-zhixu-blue/5 p-4">
        <div class="flex items-start justify-between mb-2">
          <div>
            <span class="font-medium text-zhixu-blue">{{ wl.name }}</span>
            <div class="text-xs text-zhixu-blue/50 mt-0.5">{{ wl.description || '暂无描述' }}</div>
          </div>
          <span class="text-zhixu-gold font-medium text-sm">{{ wl.word_count }} 词</span>
        </div>
        <div class="flex gap-2 mt-3">
          <button @click="startImport(wl)" class="flex-1 px-3 py-1.5 text-xs bg-zhixu-gold/10 text-zhixu-gold rounded-lg">导入单词</button>
          <button @click="deleteWordlist(wl)" class="px-3 py-1.5 text-xs bg-red-50 text-red-500 rounded-lg">删除</button>
        </div>
      </div>
    </div>

    <!-- Desktop: table layout -->
    <div class="hidden sm:block bg-white rounded-xl border border-zhixu-blue/5 overflow-hidden">
      <table class="w-full text-sm">
        <thead>
          <tr class="border-b border-zhixu-blue/10 bg-zhixu-cream/50">
            <th class="py-3 px-4 text-left text-zhixu-blue/60 font-medium">ID</th>
            <th class="py-3 px-4 text-left text-zhixu-blue/60 font-medium">名称</th>
            <th class="py-3 px-4 text-left text-zhixu-blue/60 font-medium">描述</th>
            <th class="py-3 px-4 text-center text-zhixu-blue/60 font-medium">单词数</th>
            <th class="py-3 px-4 text-center text-zhixu-blue/60 font-medium">操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="wl in wordlists" :key="wl.id" class="border-b border-zhixu-blue/5 hover:bg-zhixu-cream/30">
            <td class="py-3 px-4 text-zhixu-blue/50">{{ wl.id }}</td>
            <td class="py-3 px-4 font-medium text-zhixu-blue">{{ wl.name }}</td>
            <td class="py-3 px-4 text-zhixu-blue/60">{{ wl.description || '-' }}</td>
            <td class="py-3 px-4 text-center text-zhixu-gold font-medium">{{ wl.word_count }}</td>
            <td class="py-3 px-4 text-center">
              <div class="flex justify-center gap-2">
                <button @click="startImport(wl)" class="px-2 py-1 text-xs bg-zhixu-gold/10 text-zhixu-gold rounded hover:bg-zhixu-gold/20 transition">导入单词</button>
                <button @click="deleteWordlist(wl)" class="px-2 py-1 text-xs bg-red-50 text-red-500 rounded hover:bg-red-100 transition">删除</button>
              </div>
            </td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import api from '../../api/client'

const wordlists = ref<any[]>([])
const showCreate = ref(false)
const showImport = ref(false)
const newName = ref('')
const newDesc = ref('')
const importTarget = ref<any>(null)
const importText = ref('')
const importResult = ref('')
const importResultOk = ref(true)
const importMode = ref<'file' | 'text'>('file')
const selectedFile = ref<File | null>(null)
const importing = ref(false)

const fileExt = computed(() => {
  if (!selectedFile.value) return ''
  return selectedFile.value.name.split('.').pop()?.toLowerCase() || ''
})

async function fetchData() {
  const res = await api.get('/admin/wordlists')
  wordlists.value = res.data
}

async function createWordlist() {
  if (!newName.value.trim()) return
  await api.post('/admin/wordlists', { name: newName.value, description: newDesc.value })
  newName.value = ''
  newDesc.value = ''
  showCreate.value = false
  await fetchData()
}

async function deleteWordlist(wl: any) {
  if (!confirm(`确定删除词库「${wl.name}」及其所有单词？`)) return
  await api.delete(`/admin/wordlists/${wl.id}`)
  await fetchData()
}

function startImport(wl: any) {
  importTarget.value = wl
  importText.value = ''
  importResult.value = ''
  importResultOk.value = true
  selectedFile.value = null
  importMode.value = 'file'
  showImport.value = true
}

function cancelImport() {
  showImport.value = false
  importText.value = ''
  selectedFile.value = null
  importResult.value = ''
}

function onFileSelect(e: Event) {
  const input = e.target as HTMLInputElement
  selectedFile.value = input.files?.[0] || null
}

async function importByFile() {
  if (!selectedFile.value || !importTarget.value) return
  importing.value = true
  importResult.value = ''
  try {
    const formData = new FormData()
    formData.append('file', selectedFile.value)
    const res = await api.post(`/admin/wordlists/${importTarget.value.id}/import`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
    importResult.value = `成功导入 ${res.data.imported} 个单词`
    importResultOk.value = true
    selectedFile.value = null
    await fetchData()
  } catch (err: any) {
    importResult.value = err.response?.data?.detail || '导入失败'
    importResultOk.value = false
  } finally {
    importing.value = false
  }
}

async function importByText() {
  if (!importTarget.value || !importText.value.trim()) return
  importing.value = true
  importResult.value = ''
  const lines = importText.value.trim().split('\n').filter(l => l.trim())
  const words = lines.map(line => {
    const parts = line.trim().split(/\s+/)
    return {
      word: parts[0] || '',
      translation: parts[1] || '',
      phonetic: parts[2] || null,
    }
  }).filter(w => w.word && w.translation)

  if (words.length === 0) {
    importResult.value = '没有有效单词'
    importResultOk.value = false
    importing.value = false
    return
  }

  try {
    const res = await api.post(`/admin/wordlists/${importTarget.value.id}/words`, { words })
    importResult.value = `成功导入 ${res.data.imported} 个单词`
    importResultOk.value = true
    importText.value = ''
    await fetchData()
  } catch (err: any) {
    importResult.value = err.response?.data?.detail || '导入失败'
    importResultOk.value = false
  } finally {
    importing.value = false
  }
}

async function downloadTemplate() {
  try {
    const res = await api.get('/admin/wordlists/template', { responseType: 'blob' })
    const url = URL.createObjectURL(res.data)
    const a = document.createElement('a')
    a.href = url
    a.download = 'wordlist_template.xlsx'
    a.click()
    URL.revokeObjectURL(url)
  } catch {
    alert('下载模板失败')
  }
}

onMounted(fetchData)
</script>
