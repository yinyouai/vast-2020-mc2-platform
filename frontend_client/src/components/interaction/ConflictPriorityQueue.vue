<template>
  <div class="panel queue-panel">
    <div class="panel-header">
      <div>
        <h4 class="panel-title">复核对象工作台</h4>
        <p class="panel-subtitle">先选择对象，再点击“开始复核”进行人工确认或修正。</p>
      </div>
      <span class="data-chip">{{ items.length }} 条样本</span>
    </div>

    <section class="current-person-card">
      <span class="section-label">第一部分 / 当前展示</span>
      <div class="current-person-main">
        <strong>{{ activeItem?.id || activeId }}</strong>
        <small>{{ activeItem?.machineLabel }} -> {{ activeItem?.humanLabel }}</small>
      </div>
      <div class="current-actions">
        <span :class="['reviewed-pill', statusTone(activeItem?.status)]">
          {{ statusLabel(activeItem?.status) }}
        </span>
        <button type="button" @click="startReview(activeItem?.id || activeId)">开始复核</button>
      </div>
    </section>

    <section class="queue-section">
      <div class="lane-head">
        <span>第二部分 / 模式识别高冲突</span>
        <strong>{{ conflictItems.length }}</strong>
      </div>
      <article
        v-for="item in conflictItems"
        :key="item.id"
        :class="['queue-card', activeId === item.id && 'is-active']"
      >
        <button type="button" class="queue-select" @click="$emit('select', item.id)">
          <span class="queue-rank">{{ item.rank }}</span>
          <span class="queue-main">
            <strong>{{ item.id }}</strong>
            <small>{{ item.machineLabel }} -> {{ item.humanLabel }}</small>
          </span>
          <span :class="['reviewed-pill', statusTone(item.status)]">{{ statusLabel(item.status) }}</span>
        </button>
        <button type="button" class="review-entry" @click="startReview(item.id)">
          {{ reviewingId === item.id ? '正在复核' : '复核此人' }}
        </button>
        <div v-if="reviewingId === item.id" class="review-controls">
          <select :value="item.humanLabel" @change="updateLabel(item, $event.target.value)">
            <option v-for="label in labelOptions" :key="label" :value="label">{{ label }}</option>
          </select>
          <button type="button" @click="setStatus(item, 'confirmed')">确认正确</button>
          <button type="button" @click="setStatus(item, 'corrected')">提交修正</button>
        </div>
      </article>
    </section>

    <section class="queue-section">
      <div class="lane-head">
        <span>第三部分 / 对比与动态选择</span>
        <strong>{{ dynamicItems.length }}</strong>
      </div>
      <article
        v-for="item in dynamicItems"
        :key="item.id"
        :class="['queue-card', 'is-compare', activeId === item.id && 'is-active']"
      >
        <button type="button" class="queue-select" @click="$emit('select', item.id)">
          <span class="queue-rank">{{ item.rank }}</span>
          <span class="queue-main">
            <strong>{{ item.id }}</strong>
            <small>{{ item.machineLabel }} -> {{ item.humanLabel }}</small>
          </span>
          <span :class="['reviewed-pill', statusTone(item.status)]">{{ statusLabel(item.status) }}</span>
        </button>
        <button type="button" class="review-entry" @click="startReview(item.id)">
          {{ reviewingId === item.id ? '正在复核' : '复核此人' }}
        </button>
        <div v-if="reviewingId === item.id" class="review-controls">
          <select :value="item.humanLabel" @change="updateLabel(item, $event.target.value)">
            <option v-for="label in labelOptions" :key="label" :value="label">{{ label }}</option>
          </select>
          <button type="button" @click="setStatus(item, 'confirmed')">确认正确</button>
          <button type="button" @click="setStatus(item, 'corrected')">提交修正</button>
        </div>
      </article>
    </section>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  items: {
    type: Array,
    default: () => []
  },
  activeId: {
    type: String,
    default: ''
  },
  activeItem: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['select', 'update-case'])
const reviewingId = ref('')

const labelOptions = ['黄色提袋', '公共会场物品', '背景样本', '南瓜笔记本', '红帽', '眼球玩具', '待选择标签']

const conflictItems = computed(() => props.items.filter((item) => item.source === 'conflict'))
const dynamicItems = computed(() => props.items.filter((item) => item.source !== 'conflict'))

const statusLabel = (status) => {
  if (status === 'confirmed') return '已确认'
  if (status === 'corrected') return '已修正'
  return '未复核'
}

const statusTone = (status) => {
  if (status === 'confirmed') return 'is-confirmed'
  if (status === 'corrected') return 'is-corrected'
  return 'is-unreviewed'
}

const startReview = (id) => {
  if (!id) return
  reviewingId.value = id
  emit('select', id)
}

const updateLabel = (item, humanLabel) => {
  emit('update-case', { id: item.id, patch: { humanLabel } })
}

const setStatus = (item, status) => {
  emit('update-case', { id: item.id, patch: { status } })
  reviewingId.value = ''
}
</script>

<style scoped>
.queue-panel {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.current-person-card {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto;
  gap: 8px 12px;
  align-items: center;
  padding: 14px;
  border: 1px solid rgba(47, 125, 246, 0.22);
  border-radius: var(--radius);
  background:
    radial-gradient(circle at 92% 10%, rgba(47, 125, 246, 0.16), transparent 28%),
    rgba(47, 125, 246, 0.08);
}

.section-label {
  grid-column: 1 / -1;
  color: var(--subtle);
  font-size: 0.76rem;
  font-weight: 900;
  letter-spacing: 0.08em;
}

.current-person-main {
  min-width: 0;
}

.current-person-main strong,
.current-person-main small {
  display: block;
}

.current-person-main strong {
  font-size: 1.2rem;
}

.current-person-main small {
  margin-top: 6px;
  color: var(--muted);
  line-height: 1.5;
}

.current-actions {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-end;
  gap: 8px;
}

.current-actions button,
.review-entry,
.review-controls button {
  min-height: 34px;
  border: 1px solid var(--border);
  border-radius: 999px;
  color: var(--text);
  background: rgba(255, 255, 255, 0.88);
  font-size: 0.78rem;
  font-weight: 900;
  cursor: pointer;
}

.current-actions button,
.review-entry {
  padding: 0 12px;
}

.queue-section {
  display: flex;
  min-width: 0;
  flex-direction: column;
  gap: 8px;
}

.lane-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  min-height: 34px;
  padding: 0 4px;
}

.lane-head span {
  color: var(--subtle);
  font-size: 0.78rem;
  font-weight: 900;
  letter-spacing: 0.08em;
}

.lane-head strong {
  display: grid;
  place-items: center;
  min-width: 30px;
  height: 30px;
  border-radius: 999px;
  color: var(--accent);
  background: rgba(47, 125, 246, 0.1);
  font-size: 0.82rem;
}

.queue-card {
  display: grid;
  gap: 8px;
  width: 100%;
  padding: 10px;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  color: var(--text);
  background: rgba(255, 255, 255, 0.82);
  transition:
    transform var(--motion-fast) var(--ease-spring),
    border-color var(--motion-fast) ease,
    box-shadow var(--motion-fast) ease,
    background var(--motion-fast) ease;
}

.queue-card:hover,
.queue-card.is-active {
  transform: translateY(-2px);
  border-color: rgba(47, 125, 246, 0.28);
  background: rgba(47, 125, 246, 0.08);
  box-shadow: var(--shadow-soft);
}

.queue-select {
  display: grid;
  grid-template-columns: 34px minmax(0, 1fr) auto;
  align-items: center;
  gap: 9px;
  width: 100%;
  padding: 0;
  border: 0;
  color: inherit;
  text-align: left;
  background: transparent;
  cursor: pointer;
}

.queue-select:focus-visible,
.current-actions button:focus-visible,
.review-entry:focus-visible,
.review-controls button:focus-visible,
.review-controls select:focus-visible {
  outline: 3px solid rgba(47, 125, 246, 0.22);
  outline-offset: 3px;
}

.queue-rank {
  display: grid;
  place-items: center;
  width: 34px;
  height: 34px;
  border-radius: 12px;
  color: var(--accent);
  background: rgba(47, 125, 246, 0.1);
  font-weight: 900;
}

.queue-main {
  min-width: 0;
}

.queue-main strong,
.queue-main small {
  display: block;
}

.queue-main small {
  margin-top: 5px;
  overflow: hidden;
  color: var(--muted);
  line-height: 1.45;
  text-overflow: ellipsis;
}

.reviewed-pill {
  display: inline-flex;
  align-items: center;
  min-height: 30px;
  padding: 0 10px;
  border-radius: 999px;
  font-size: 0.76rem;
  font-weight: 900;
  white-space: nowrap;
}

.reviewed-pill.is-unreviewed {
  color: #9a6818;
  background: rgba(240, 180, 76, 0.14);
}

.reviewed-pill.is-confirmed {
  color: #1c8a67;
  background: rgba(57, 169, 125, 0.12);
}

.reviewed-pill.is-corrected {
  color: #1d58b1;
  background: rgba(47, 125, 246, 0.12);
}

.review-controls {
  display: grid;
  grid-template-columns: minmax(0, 1fr) auto auto;
  gap: 7px;
  padding-top: 8px;
  border-top: 1px solid rgba(53, 89, 138, 0.08);
}

.review-controls select,
.review-controls button {
  padding: 0 10px;
}

.review-controls select {
  min-height: 34px;
  border: 1px solid var(--border);
  border-radius: 999px;
  color: var(--text);
  background: rgba(255, 255, 255, 0.88);
  font-size: 0.78rem;
  font-weight: 900;
}

@media (max-width: 720px) {
  .current-person-card,
  .queue-select,
  .review-controls {
    grid-template-columns: 1fr;
  }
}
</style>
