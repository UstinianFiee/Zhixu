<template>
  <div class="min-h-[calc(100vh-3.5rem)] flex flex-col items-center justify-center px-4 py-8">
    <div v-if="sessionComplete" class="text-center max-w-md">
      <div class="mb-4">
        <svg class="w-16 h-16 mx-auto text-zhixu-gold" fill="none" stroke="currentColor" stroke-width="1.2" viewBox="0 0 24 24"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/></svg>
      </div>
      <h2 class="font-serif text-2xl text-zhixu-blue font-bold mb-2">默写完成！</h2>
      <div class="grid grid-cols-2 gap-4 my-6">
        <div class="bg-white rounded-xl p-4 border border-zhixu-blue/5">
          <div class="text-2xl font-bold text-green-600">{{ practiceStore.stats.correct }}</div>
          <div class="text-xs text-zhixu-blue/50">正确</div>
        </div>
        <div class="bg-white rounded-xl p-4 border border-zhixu-blue/5">
          <div class="text-2xl font-bold text-red-500">{{ practiceStore.stats.wrong }}</div>
          <div class="text-xs text-zhixu-blue/50">错误</div>
        </div>
      </div>
      <div class="flex gap-3 justify-center">
        <button @click="restartSession" class="px-6 py-2.5 bg-zhixu-blue text-zhixu-cream rounded-lg hover:bg-zhixu-dark transition font-medium">
          再来一组
        </button>
        <router-link to="/wordlists" class="px-6 py-2.5 border border-zhixu-blue/20 text-zhixu-blue rounded-lg hover:bg-zhixu-blue/5 transition">
          返回词库
        </router-link>
      </div>
    </div>

    <template v-else>
      <div class="w-full max-w-3xl mb-6 flex items-center justify-between">
        <h2 class="font-serif text-lg text-zhixu-blue">默写检测</h2>
        <div class="flex items-center gap-3">
          <span class="text-sm text-zhixu-blue/50">第 {{ practiceStore.stats.total + 1 }} 词</span>
          <button @click="endSession" class="px-4 py-1.5 text-sm border border-zhixu-blue/20 text-zhixu-blue rounded-lg hover:bg-zhixu-blue/5 transition">
            结束默写
          </button>
        </div>
      </div>

      <!-- Dictation: show only translation, hide word -->
      <div class="w-full max-w-3xl mx-auto" tabindex="0">
        <div class="text-center mb-8">
          <div v-if="practiceStore.currentWord" class="space-y-4">
            <div v-if="practiceStore.currentWord.phonetic" class="text-lg text-zhixu-blue/60 font-serif">
              {{ practiceStore.currentWord.phonetic }}
            </div>
            <div class="font-serif text-2xl text-zhixu-blue/70">
              {{ practiceStore.currentWord.translation }}
            </div>
            <button @click="speakWord" class="mt-2 px-3 py-1 text-sm text-zhixu-blue/50 hover:text-zhixu-gold transition">
              <svg class="w-4 h-4 inline-block mr-1" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/></svg>听发音
            </button>
          </div>
          <div v-else class="text-zhixu-blue/40 text-xl py-12">加载中...</div>
        </div>

        <div class="flex justify-center mb-6">
          <input
            ref="inputRef"
            v-model="dictationInput"
            @keydown.enter="checkDictation"
            class="w-80 px-4 py-2.5 border-2 border-zhixu-blue/20 rounded-lg text-center text-xl font-mono tracking-wider focus:border-zhixu-gold focus:outline-none transition"
            placeholder="输入单词..."
            autofocus
          />
        </div>

        <!-- Show result -->
        <div v-if="showResult" class="text-center mb-6">
          <div v-if="lastCorrect" class="text-green-600 font-medium text-lg">&#10003; 正确！</div>
          <div v-else class="text-red-500">
            <div class="font-medium text-lg">&#10007; 错误</div>
            <div class="text-sm mt-1">正确答案: <span class="font-mono font-bold">{{ practiceStore.currentWord?.word }}</span></div>
          </div>
        </div>

        <div class="flex justify-center gap-6 text-sm text-zhixu-blue/60">
          <div><span class="text-green-600 font-semibold">{{ practiceStore.stats.correct }}</span> 正确</div>
          <div><span class="text-red-500 font-semibold">{{ practiceStore.stats.wrong }}</span> 错误</div>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { usePracticeStore } from '../stores/practice'
import { useAuthStore } from '../stores/auth'

const route = useRoute()
const practiceStore = usePracticeStore()
const authStore = useAuthStore()
const sessionComplete = ref(false)
const dictationInput = ref('')
const showResult = ref(false)
const lastCorrect = ref(false)
const inputRef = ref<HTMLInputElement>()

function speakWord() {
  if (!practiceStore.currentWord) return
  const utterance = new SpeechSynthesisUtterance(practiceStore.currentWord.word)
  utterance.lang = 'en-US'
  utterance.rate = 0.8
  speechSynthesis.speak(utterance)
}

async function checkDictation() {
  if (!practiceStore.currentWord || !dictationInput.value.trim()) return
  const isCorrect = dictationInput.value.trim().toLowerCase() === practiceStore.currentWord.word.toLowerCase()
  lastCorrect.value = isCorrect
  showResult.value = true

  if (isCorrect) {
    const result = await practiceStore.submitCheck(practiceStore.currentWord.word, dictationInput.value.trim(), 3000)
    if (result.points_earned > 0 && authStore.user) {
      authStore.updatePoints(authStore.user.total_points + result.points_earned, authStore.user.current_level)
    }
  } else {
    await practiceStore.submitCheck(practiceStore.currentWord.word, dictationInput.value.trim(), 3000)
  }

  dictationInput.value = ''

  setTimeout(async () => {
    showResult.value = false
    if (practiceStore.stats.total >= 10) {
      const res = await practiceStore.completeSession()
      if (authStore.user && res) {
        authStore.updatePoints(res.total_points, res.current_level)
      }
      sessionComplete.value = true
    } else {
      await practiceStore.fetchNextWord()
      nextTick(() => inputRef.value?.focus())
    }
  }, 1500)
}

async function endSession() {
  const res = await practiceStore.completeSession()
  if (authStore.user && res) {
    authStore.updatePoints(res.total_points, res.current_level)
  }
  sessionComplete.value = true
}

function restartSession() {
  const wlId = parseInt(route.params.id as string)
  practiceStore.startSession(wlId)
  sessionComplete.value = false
  showResult.value = false
  practiceStore.fetchNextWord()
  nextTick(() => inputRef.value?.focus())
}

onMounted(() => {
  const wlId = parseInt(route.params.id as string)
  practiceStore.startSession(wlId)
  practiceStore.fetchNextWord()
  nextTick(() => inputRef.value?.focus())
})
</script>
