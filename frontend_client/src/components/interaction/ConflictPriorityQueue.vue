<template>
  <div class="panel queue-panel">
    <div class="panel-header">
      <div>
        <h4 class="panel-title">冲突优先队列</h4>
        <p class="panel-subtitle">按风险、语义冲突和物证特异性排序。</p>
      </div>
    </div>

    <button
      v-for="item in queue"
      :key="item.id"
      :class="['queue-card', store.selectedPersonId === item.id && 'is-active']"
      @click="store.selectPerson(item.id)"
    >
      <span class="queue-rank">{{ item.rank }}</span>
      <span class="queue-main">
        <strong>{{ item.id }}</strong>
        <small>{{ item.summary }}</small>
      </span>
      <span :class="['risk-pill', item.risk === 'high' ? 'risk-high' : 'risk-low']">
        {{ item.score }}
      </span>
    </button>
  </div>
</template>

<script setup>
import { useDashboardStore } from '../../store/dashboard'

const store = useDashboardStore()

const queue = [
  { rank: 'A', id: 'Person3', score: '高', risk: 'high', summary: '机器标为普通红帽，文本指向黄色接头包。' },
  { rank: 'B', id: 'Person27', score: '中', risk: 'high', summary: '机器框和文本标签不一致，需要人工排除。' },
  { rank: 'C', id: 'Person21', score: '低', risk: 'low', summary: '典型会场背景样本，用作安全参照。' },
  { rank: 'D', id: 'Person12', score: '高', risk: 'high', summary: '核心组候选，物证出现频次异常。' }
]
</script>

<style scoped>
.queue-panel {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.queue-card {
  display: grid;
  grid-template-columns: 42px minmax(0, 1fr) auto;
  align-items: center;
  gap: 12px;
  width: 100%;
  min-height: 74px;
  padding: 12px;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  color: var(--text);
  text-align: left;
  background: rgba(255, 255, 255, 0.03);
}

.queue-card:hover,
.queue-card.is-active {
  border-color: rgba(66, 214, 194, 0.45);
  background: rgba(66, 214, 194, 0.08);
}

.queue-rank {
  display: grid;
  place-items: center;
  width: 42px;
  height: 42px;
  border-radius: 6px;
  color: var(--accent);
  background: rgba(66, 214, 194, 0.09);
  font-weight: 900;
}

.queue-main strong,
.queue-main small {
  display: block;
}

.queue-main small {
  margin-top: 5px;
  color: var(--muted);
  line-height: 1.4;
}
</style>
