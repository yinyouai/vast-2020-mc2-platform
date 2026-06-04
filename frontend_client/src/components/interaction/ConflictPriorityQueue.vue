<template>
  <div class="panel queue-panel">
    <div class="panel-header">
      <div>
        <h4 class="panel-title">冲突优先队列</h4>
        <p class="panel-subtitle">按照风险等级、语义冲突强度和物证特异性进行排序。</p>
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
  { rank: 'A', id: 'Person3', score: '高', risk: 'high', summary: '模型倾向于识别成红帽，但文本明确指向黄色提袋，属于高优先级图文冲突样本。' },
  { rank: 'B', id: 'Person27', score: '高', risk: 'high', summary: '机器框选结果与文本叙事不一致，更适合作为误报清洗的重要对照。' },
  { rank: 'C', id: 'Person21', score: '低', risk: 'low', summary: '更像普通会场参与者，可作为背景样本辅助判断公共物品分布。' },
  { rank: 'D', id: 'Person12', score: '高', risk: 'high', summary: '与核心组特征高度接近，且在物证层面反复出现异常共现。' }
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
  background: rgba(255, 255, 255, 0.82);
}

.queue-card:hover,
.queue-card.is-active {
  border-color: rgba(47, 125, 246, 0.24);
  background: rgba(47, 125, 246, 0.08);
}

  .queue-rank {
  display: grid;
  place-items: center;
  width: 42px;
  height: 42px;
  border-radius: 10px;
  color: var(--accent);
  background: rgba(47, 125, 246, 0.09);
  font-weight: 900;
}

.queue-main strong,
.queue-main small {
  display: block;
}

.queue-main small {
  margin-top: 5px;
  color: var(--muted);
  line-height: 1.5;
}
</style>
