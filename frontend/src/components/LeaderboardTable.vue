<template>
  <div class="overflow-x-auto">
    <table class="w-full text-sm">
      <thead>
        <tr class="border-b border-zhixu-blue/10">
          <th class="py-3 px-4 text-left text-zhixu-blue/50 font-medium rounded-tl-xl">排名</th>
          <th class="py-3 px-4 text-left text-zhixu-blue/50 font-medium">用户</th>
          <th class="py-3 px-4 text-right text-zhixu-blue/50 font-medium rounded-tr-xl">分数</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(entry, i) in entries"
          :key="entry.user_id"
          class="border-b border-zhixu-blue/5 hover:bg-zhixu-gold/5 transition"
          :class="[
            entry.user_id === currentUserId ? 'bg-zhixu-gold/10' : '',
          ]"
        >
          <td class="py-3 px-4" :class="i === entries.length - 1 ? 'rounded-bl-xl' : ''">
            <span v-if="entry.rank === 1" class="inline-flex items-center justify-center w-6 h-6 rounded-full bg-yellow-500/15 text-yellow-600 text-xs font-bold">1</span>
            <span v-else-if="entry.rank === 2" class="inline-flex items-center justify-center w-6 h-6 rounded-full bg-gray-200 text-gray-500 text-xs font-bold">2</span>
            <span v-else-if="entry.rank === 3" class="inline-flex items-center justify-center w-6 h-6 rounded-full bg-amber-500/15 text-amber-600 text-xs font-bold">3</span>
            <span v-else class="text-zhixu-blue/40">{{ entry.rank }}</span>
          </td>
          <td class="py-3 px-4">
            <div class="flex items-center gap-2">
              <span class="w-7 h-7 rounded-full overflow-hidden flex items-center justify-center text-xs font-medium"
                :class="entry.user_id === currentUserId ? 'bg-zhixu-gold/20 text-zhixu-gold' : 'bg-zhixu-blue/10'">
                <img v-if="entry.avatar_url" :src="entry.avatar_url" class="w-full h-full object-cover" @error="(e: any) => e.target.style.display='none'" />
                <span v-else>{{ (entry.nickname || entry.username).charAt(0).toUpperCase() }}</span>
              </span>
              <span class="text-zhixu-blue" :class="{ 'font-semibold text-zhixu-gold': entry.user_id === currentUserId }">
                {{ entry.nickname || entry.username }}
                <span v-if="entry.user_id === currentUserId" class="text-xs text-zhixu-gold ml-1">我</span>
              </span>
            </div>
          </td>
          <td class="py-3 px-4 text-right font-semibold text-zhixu-gold" :class="i === entries.length - 1 ? 'rounded-br-xl' : ''">{{ entry.score }}</td>
        </tr>
        <tr v-if="entries.length === 0">
          <td colspan="3" class="py-8 text-center text-zhixu-blue/40">暂无数据</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
interface Entry {
  rank: number
  user_id: number
  username: string
  nickname: string | null
  avatar_url: string | null
  score: number
}

defineProps<{
  entries: Entry[]
  currentUserId?: number
}>()
</script>
