<template>
  <div class="w-full max-w-3xl mx-auto relative" @keydown="handleKeydown" @click="focusMobileInput" tabindex="0" ref="containerRef">
    <!-- Hidden input for mobile keyboard -->
    <input
      ref="mobileInputRef"
      :value="mobileValue"
      @input="onMobileInput"
      class="absolute opacity-0 h-0 w-0 -z-10"
      autocomplete="off" autocorrect="off" autocapitalize="off" spellcheck="false"
    />
    <!-- Word Display -->
    <div class="text-center mb-8">
      <div v-if="word" class="space-y-4">
        <!-- Phonetic -->
        <div v-if="word.phonetic" class="text-lg text-zhixu-blue/60 font-serif">
          {{ word.phonetic }}
        </div>

        <!-- Word Characters -->
        <div class="flex justify-center gap-1 flex-wrap" :class="{ 'flash-correct': flashCorrect, 'flash-wrong': flashWrong }">
          <span
            v-for="(char, index) in word.word"
            :key="index"
            :class="charClass(index)"
            class="font-mono text-4xl sm:text-5xl tracking-wider transition-colors duration-150"
          >{{ char === ' ' ? ' ' : char }}</span>
        </div>

        <!-- Translation -->
        <div v-if="mode === 'practice'" class="text-zhixu-blue/70 text-lg font-serif mt-4">
          {{ word.translation }}
        </div>
        <div v-else class="text-zhixu-blue/70 text-lg font-serif mt-4">
          {{ word.translation }}
          <div class="text-sm text-zhixu-blue/40 mt-1">（默写模式：请根据释义输入单词）</div>
        </div>

        <!-- Example Sentence -->
        <div v-if="word.example_sentence && showExample" class="text-sm text-zhixu-blue/50 italic mt-2 max-w-lg mx-auto">
          "{{ word.example_sentence }}"
        </div>

        <!-- Speak Button -->
        <button @click="speakWord" class="mt-2 inline-flex items-center gap-1 px-3 py-1 text-sm text-zhixu-blue/50 hover:text-zhixu-gold transition">
          <svg class="w-4 h-4" fill="none" stroke="currentColor" stroke-width="1.5" viewBox="0 0 24 24"><polygon points="11 5 6 9 2 9 2 15 6 15 11 19 11 5"/><path d="M15.54 8.46a5 5 0 0 1 0 7.07"/></svg>
          发音
        </button>
      </div>
      <div v-else class="text-zhixu-blue/40 text-xl py-12">
        加载中...
      </div>
    </div>

    <!-- Input Area (only in dictation mode) -->
    <div v-if="mode === 'dictation'" class="flex justify-center mb-6">
      <input
        ref="inputRef"
        v-model="dictationInput"
        @keydown.enter="checkDictation"
        class="w-80 px-4 py-2 border-2 border-zhixu-blue/20 rounded-lg text-center text-xl font-mono tracking-wider focus:border-zhixu-gold focus:outline-none transition"
        placeholder="输入单词..."
        autofocus
      />
    </div>

    <!-- Stats Bar -->
    <div class="flex justify-center gap-6 text-sm text-zhixu-blue/60">
      <div class="flex items-center gap-1">
        <span class="text-zhixu-gold font-semibold">{{ elapsedTime }}s</span>
        <span>用时</span>
      </div>
      <div class="flex items-center gap-1">
        <span class="text-green-600 font-semibold">{{ correctCount }}</span>
        <span>正确</span>
      </div>
      <div class="flex items-center gap-1">
        <span class="text-red-500 font-semibold">{{ wrongCount }}</span>
        <span>错误</span>
      </div>
      <div class="flex items-center gap-1">
        <span class="text-zhixu-blue font-semibold">{{ currentSpeed }}</span>
        <span>词/分</span>
      </div>
      <div class="flex items-center gap-1">
        <span class="text-zhixu-gold font-semibold">{{ accuracy }}%</span>
        <span>正确率</span>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, onUnmounted, watch, nextTick } from 'vue'

interface Word {
  id: number
  word: string
  translation: string
  phonetic: string | null
  example_sentence: string | null
}

const props = withDefaults(defineProps<{
  word: Word | null
  mode?: 'practice' | 'dictation'
  showExample?: boolean
}>(), {
  mode: 'practice',
  showExample: true,
})

const emit = defineEmits<{
  (e: 'correct', timeMs: number): void
  (e: 'wrong'): void
  (e: 'complete'): void
}>()

const containerRef = ref<HTMLElement>()
const inputRef = ref<HTMLInputElement>()
const mobileInputRef = ref<HTMLInputElement>()
const mobileValue = ref('')
const currentIndex = ref(0)
const wordStartTime = ref(0)
const correctCount = ref(0)
const wrongCount = ref(0)
const sessionStart = ref(Date.now())
const flashCorrect = ref(false)
const flashWrong = ref(false)
const timerInterval = ref<number>()
const elapsedTime = ref(0)
const dictationInput = ref('')

const currentSpeed = computed(() => {
  const minutes = (Date.now() - sessionStart.value) / 60000
  if (minutes < 0.05) return 0
  return Math.round(correctCount.value / minutes)
})

const accuracy = computed(() => {
  const total = correctCount.value + wrongCount.value
  if (total === 0) return 100
  return Math.round((correctCount.value / total) * 100)
})

function charClass(index: number) {
  if (index < currentIndex.value) return 'text-green-600'
  if (index === currentIndex.value) return 'text-zhixu-gold underline underline-offset-8 decoration-2'
  return 'text-zhixu-blue/25'
}

function speakWord() {
  if (!props.word) return
  const utterance = new SpeechSynthesisUtterance(props.word.word)
  utterance.lang = 'en-US'
  utterance.rate = 0.8
  speechSynthesis.speak(utterance)
}

function handleKeydown(e: KeyboardEvent) {
  if (props.mode === 'dictation') return
  if (!props.word || e.ctrlKey || e.altKey || e.metaKey) return
  if (e.key === 'Backspace') return

  const expected = props.word.word[currentIndex.value]
  if (!expected) return

  if (e.key === expected || e.key === expected.toLowerCase()) {
    currentIndex.value++
    flash('correct')

    if (currentIndex.value >= props.word.word.length) {
      const timeMs = Date.now() - wordStartTime.value
      correctCount.value++
      emit('correct', timeMs)
      resetWord()
    }
  } else {
    flash('wrong')
    wrongCount.value++
    emit('wrong')
  }
}

function focusMobileInput() {
  mobileInputRef.value?.focus()
}

function onMobileInput(e: Event) {
  if (props.mode === 'dictation') return
  if (!props.word) return
  const input = e.target as HTMLInputElement
  const typed = input.value
  if (!typed) return

  // Process each new character
  for (let i = 0; i < typed.length; i++) {
    const ch = typed[i]
    const expected = props.word.word[currentIndex.value]
    if (!expected) break

    if (ch === expected || ch.toLowerCase() === expected.toLowerCase()) {
      currentIndex.value++
      flash('correct')
      if (currentIndex.value >= props.word.word.length) {
        const timeMs = Date.now() - wordStartTime.value
        correctCount.value++
        emit('correct', timeMs)
        resetWord()
        break
      }
    } else {
      flash('wrong')
      wrongCount.value++
      emit('wrong')
    }
  }

  // Clear input for next character
  input.value = ''
  mobileValue.value = ''
}

function checkDictation() {
  if (!props.word || !dictationInput.value.trim()) return
  const isCorrect = dictationInput.value.trim().toLowerCase() === props.word.word.toLowerCase()
  if (isCorrect) {
    correctCount.value++
    flash('correct')
    const timeMs = Date.now() - wordStartTime.value
    emit('correct', timeMs)
  } else {
    wrongCount.value++
    flash('wrong')
    emit('wrong')
  }
  dictationInput.value = ''
  resetWord()
}

function flash(type: 'correct' | 'wrong') {
  if (type === 'correct') {
    flashCorrect.value = true
    setTimeout(() => { flashCorrect.value = false }, 300)
  } else {
    flashWrong.value = true
    setTimeout(() => { flashWrong.value = false }, 300)
  }
}

function resetWord() {
  currentIndex.value = 0
  wordStartTime.value = Date.now()
  dictationInput.value = ''
  mobileValue.value = ''
  nextTick(() => {
    containerRef.value?.focus()
    inputRef?.value?.focus()
    mobileInputRef?.value?.focus()
  })
}

watch(() => props.word, () => {
  resetWord()
})

onMounted(() => {
  sessionStart.value = Date.now()
  wordStartTime.value = Date.now()
  containerRef.value?.focus()
  mobileInputRef.value?.focus()
  timerInterval.value = window.setInterval(() => {
    elapsedTime.value = Math.floor((Date.now() - sessionStart.value) / 1000)
  }, 1000)
})

onUnmounted(() => {
  if (timerInterval.value) clearInterval(timerInterval.value)
})
</script>
