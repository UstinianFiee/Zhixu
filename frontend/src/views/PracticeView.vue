<template>
  <div class="min-h-[calc(100vh-3.5rem)] flex flex-col items-center justify-center px-4 py-8">
    <!-- Session Complete -->
    <div v-if="sessionComplete" class="text-center max-w-md">
      <div class="mb-4">
        <svg class="w-16 h-16 mx-auto text-zhixu-gold" fill="none" stroke="currentColor" stroke-width="1.2" viewBox="0 0 24 24"><path d="M6 9H4.5a2.5 2.5 0 0 1 0-5H6"/><path d="M18 9h1.5a2.5 2.5 0 0 0 0-5H18"/><path d="M4 22h16"/><path d="M10 14.66V17c0 .55-.47.98-.97 1.21C7.85 18.75 7 20 7 22"/><path d="M14 14.66V17c0 .55.47.98.97 1.21C16.15 18.75 17 20 17 22"/><path d="M18 2H6v7a6 6 0 0 0 12 0V2Z"/></svg>
      </div>
      <h2 class="font-serif text-2xl text-zhixu-blue font-bold mb-2">练习完成！</h2>
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
      <div v-if="sessionResult" class="mb-6 p-4 bg-zhixu-gold/10 rounded-xl">
        <p class="text-zhixu-gold font-medium">+{{ sessionResult.points_earned }} 积分</p>
        <p class="text-sm text-zhixu-blue/50 mt-1">总积分: {{ sessionResult.total_points }}</p>
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

    <!-- Practice -->
    <template v-else>
      <div class="w-full max-w-3xl mb-6 flex items-center justify-between">
        <h2 class="font-serif text-lg text-zhixu-blue">打字练习</h2>
        <div class="flex items-center gap-3">
          <span class="text-sm text-zhixu-blue/50">第 {{ practiceStore.stats.total + 1 }} 词</span>
          <button @click="endSession" class="px-4 py-1.5 text-sm border border-zhixu-blue/20 text-zhixu-blue rounded-lg hover:bg-zhixu-blue/5 transition">
            结束练习
          </button>
        </div>
      </div>

      <TypingPractice
        :word="practiceStore.currentWord"
        mode="practice"
        @correct="onCorrect"
        @wrong="onWrong"
      />
    </template>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { usePracticeStore } from '../stores/practice'
import { useAuthStore } from '../stores/auth'
import TypingPractice from '../components/TypingPractice.vue'

const route = useRoute()
const practiceStore = usePracticeStore()
const authStore = useAuthStore()
const sessionComplete = ref(false)
const sessionResult = ref<any>(null)

async function loadWord() {
  await practiceStore.fetchNextWord()
}

async function onCorrect(timeMs: number) {
  if (practiceStore.currentWord) {
    const result = await practiceStore.submitCheck(practiceStore.currentWord.word, practiceStore.currentWord.word, timeMs)
    if (result.points_earned > 0 && authStore.user) {
      authStore.updatePoints(
        authStore.user.total_points + result.points_earned,
        authStore.user.current_level
      )
    }
  }
  // End after 10 words
  if (practiceStore.stats.total >= 10) {
    await endSession()
  } else {
    await loadWord()
  }
}

async function onWrong() {
  if (practiceStore.currentWord) {
    // Record error to backend by sending wrong input
    await practiceStore.submitCheck(practiceStore.currentWord.word, '__wrong__', 0)
  }
}

async function endSession() {
  sessionResult.value = await practiceStore.completeSession()
  if (authStore.user && sessionResult.value) {
    authStore.updatePoints(sessionResult.value.total_points, sessionResult.value.current_level)
  }
  sessionComplete.value = true
}

function restartSession() {
  const wlId = parseInt(route.params.id as string)
  practiceStore.startSession(wlId)
  sessionComplete.value = false
  sessionResult.value = null
  loadWord()
}

onMounted(() => {
  const wlId = parseInt(route.params.id as string)
  practiceStore.startSession(wlId)
  loadWord()
})
</script>
