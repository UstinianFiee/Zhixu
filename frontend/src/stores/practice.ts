import { defineStore } from 'pinia'
import { ref, reactive } from 'vue'
import api from '../api/client'

export interface Word {
  id: number
  word: string
  translation: string
  phonetic: string | null
  example_sentence: string | null
}

export const usePracticeStore = defineStore('practice', () => {
  const sessionId = ref('')
  const wordlistId = ref(0)
  const currentWord = ref<Word | null>(null)
  const stats = reactive({
    total: 0,
    correct: 0,
    wrong: 0,
    startTime: 0,
    words: [] as string[],
  })
  const loading = ref(false)

  function startSession(wlId: number) {
    sessionId.value = 'session-' + Date.now() + '-' + Math.random().toString(36).slice(2, 8)
    wordlistId.value = wlId
    stats.total = 0
    stats.correct = 0
    stats.wrong = 0
    stats.startTime = Date.now()
    stats.words = []
  }

  async function fetchNextWord() {
    loading.value = true
    try {
      const res = await api.post('/words/practice', {
        wordlist_id: wordlistId.value,
        session_id: sessionId.value,
      })
      currentWord.value = res.data
    } finally {
      loading.value = false
    }
  }

  async function submitCheck(word: string, userInput: string, timeMs: number) {
    const res = await api.post('/words/check', {
      word,
      user_input: userInput,
      time_spent_ms: timeMs,
      session_id: sessionId.value,
    })
    const result = res.data
    stats.total++
    if (result.is_correct) {
      stats.correct++
    } else {
      stats.wrong++
    }
    stats.words.push(word)
    return result
  }

  async function completeSession() {
    const duration = Date.now() - stats.startTime
    const avgSpeed = stats.total > 0 ? Math.round(stats.total / (duration / 60000)) : 0
    const res = await api.post('/sessions/complete', {
      session_id: sessionId.value,
      stats: {
        total: stats.total,
        correct: stats.correct,
        wrong: stats.wrong,
        avg_speed: avgSpeed,
        duration_ms: duration,
      },
    })
    return res.data
  }

  return { sessionId, wordlistId, currentWord, stats, loading, startSession, fetchNextWord, submitCheck, completeSession }
})
