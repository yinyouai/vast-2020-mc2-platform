<template>
  <div class="glass-card photo-grid-container">
    <h4 class="舱室标题">📸 全场 40 名参会人员图像特征分类阵列 (按置信度分组)</h4>

    <div class="photo-tabs">
      <button
        v-for="tab in filterTabs"
        :key="tab.key"
        class="tab-btn"
        :class="{ active: activeFilter === tab.key }"
        @click="activeFilter = tab.key"
      >
        {{ tab.label }}
        <span class="tab-count">{{ getCount(tab.key) }}</span>
      </button>
    </div>

    <div class="photo-grid-scroll">
      <TransitionGroup name="list-stagger" tag="div" class="photo-grid">
        <div
          v-for="person in filteredPersons"
          :key="person.id"
          class="photo-grid-item"
          :class="getPersonClass(person.id)"
          @click="onPersonClick(person.id)"
          :title="`${person.id} - ${getPersonLabel(person.id)}`"
        >
          <img
            :src="getPhotoUrl(person.id)"
            :alt="person.id"
            loading="lazy"
            @error="onImgError"
          />
          <div class="photo-label">
            <span class="person-id">{{ person.id }}</span>
            <span v-if="isHacker(person.id)" class="hacker-tag">⚠️</span>
          </div>
          <div v-if="isHacker(person.id)" class="hacker-glow"></div>
        </div>
      </TransitionGroup>
    </div>

    <div class="photo-grid-legend">
      <span class="legend-item"><span class="dot dot-hacker"></span> 核心 8 人组织</span>
      <span class="legend-item"><span class="dot dot-high"></span> 高置信度</span>
      <span class="legend-item"><span class="dot dot-mid"></span> 中等置信度</span>
      <span class="legend-item"><span class="dot dot-low"></span> 低置信噪声</span>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useDashboardStore } from '../../store/dashboard'
import { HACKER_LIST, TOTAL_PEOPLE, isTrueHacker } from '../../constants/forensics'

const store = useDashboardStore()
const router = useRouter()

const API_BASE = 'http://localhost:5000'

const activeFilter = ref('all')

const filterTabs = [
  { key: 'all', label: '全部人员' },
  { key: 'hacker', label: '核心组织' },
  { key: 'high', label: '高置信度' },
  { key: 'low', label: '低噪声区' }
]

// 生成 40 人列表
const allPersons = Array.from({ length: TOTAL_PEOPLE }, (_, i) => ({
  id: `Person${i + 1}`,
  index: i
}))

function getConfidenceLevel(personId) {
  // 基于 store 数据和人员编号估算置信度
  const num = parseInt(personId.replace('Person', ''))
  if (HACKER_LIST.includes(personId)) return 'hacker'
  if (num <= 8) return 'high'
  if (num <= 25) return 'mid'
  return 'low'
}

const filteredPersons = computed(() => {
  switch (activeFilter.value) {
    case 'hacker':
      return allPersons.filter(p => HACKER_LIST.includes(p.id))
    case 'high':
      return allPersons.filter(p => getConfidenceLevel(p.id) === 'high')
    case 'low':
      return allPersons.filter(p => getConfidenceLevel(p.id) === 'low')
    default:
      // 按黑客优先 + 编号排序
      return [...allPersons].sort((a, b) => {
        const aHack = HACKER_LIST.includes(a.id) ? 0 : 1
        const bHack = HACKER_LIST.includes(b.id) ? 0 : 1
        if (aHack !== bHack) return aHack - bHack
        return parseInt(a.id.replace('Person', '')) - parseInt(b.id.replace('Person', ''))
      })
  }
})

function getCount(key) {
  switch (key) {
    case 'all': return TOTAL_PEOPLE
    case 'hacker': return HACKER_LIST.length
    case 'high': return 8
    case 'low': return 15
    default: return 0
  }
}

function getPhotoUrl(personId) {
  return `${API_BASE}/static/MC2-Image-Data/${personId}/${personId}_1.jpg`
}

function getPersonClass(personId) {
  const cls = []
  const level = getConfidenceLevel(personId)
  if (level === 'hacker') cls.push('is-hacker')
  else if (level === 'high') cls.push('high-conf')
  else if (level === 'low') cls.push('low-conf')
  return cls
}

function getPersonLabel(personId) {
  if (isTrueHacker(personId)) return '核心组织成员'
  const level = getConfidenceLevel(personId)
  if (level === 'high') return '高置信度'
  if (level === 'mid') return '中等置信度'
  return '低置信噪声区'
}

function isHacker(personId) {
  return HACKER_LIST.includes(personId)
}

function onPersonClick(personId) {
  store.selectPerson(personId)
  router.push('/task2_correction')
}

function onImgError(e) {
  e.target.style.display = 'none'
}
</script>

<style scoped>
.photo-grid-container {
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.photo-tabs {
  display: flex;
  gap: 6px;
  margin-bottom: var(--space-md);
  flex-wrap: wrap;
}

.tab-btn {
  padding: 6px 14px;
  border-radius: var(--radius-full);
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: rgba(255, 255, 255, 0.5);
  color: var(--text-secondary);
  font-size: var(--text-xs);
  font-weight: var(--weight-medium);
  cursor: pointer;
  transition: all 0.25s var(--ease-out-expo);
  display: flex;
  align-items: center;
  gap: 5px;
}

.tab-btn:hover {
  background: rgba(49, 194, 124, 0.06);
  border-color: rgba(49, 194, 124, 0.2);
}

.tab-btn.active {
  background: var(--accent-primary);
  color: #fff;
  border-color: var(--accent-primary);
  box-shadow: 0 2px 8px rgba(49, 194, 124, 0.3);
}

.tab-count {
  font-size: 10px;
  padding: 1px 6px;
  border-radius: var(--radius-full);
  background: rgba(0, 0, 0, 0.06);
}

.tab-btn.active .tab-count {
  background: rgba(255, 255, 255, 0.25);
}

.photo-grid-scroll {
  flex: 1;
  overflow-y: auto;
  min-height: 0;
}

.photo-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(72px, 1fr));
  gap: var(--space-sm);
  padding: 2px;
}

.photo-grid-item {
  position: relative;
  border-radius: var(--radius-sm);
  overflow: hidden;
  aspect-ratio: 1;
  border: 2.5px solid rgba(0, 0, 0, 0.06);
  transition: all 0.35s var(--ease-out-expo);
  cursor: pointer;
  background: var(--bg-secondary);
}

.photo-grid-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s var(--ease-out-expo);
}

.photo-grid-item:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-card-hover);
  z-index: 2;
}

.photo-grid-item:hover img {
  transform: scale(1.1);
}

.photo-grid-item.high-conf {
  border-color: var(--accent-primary);
}

.photo-grid-item.low-conf {
  border-color: rgba(255, 90, 95, 0.3);
  opacity: 0.8;
}

.photo-grid-item.is-hacker {
  border-color: var(--accent-purple);
  box-shadow: 0 0 12px rgba(191, 90, 242, 0.25);
  animation: breath-glow 3s infinite;
}

.photo-label {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 3px 5px;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.65));
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 4px;
}

.person-id {
  color: #fff;
  font-size: 8px;
  font-weight: var(--weight-semibold);
  white-space: nowrap;
}

.hacker-tag {
  font-size: 8px;
}

.hacker-glow {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border-radius: inherit;
  box-shadow: inset 0 0 12px rgba(191, 90, 242, 0.15);
  pointer-events: none;
}

/* 图例 */
.photo-grid-legend {
  display: flex;
  gap: var(--space-lg);
  padding-top: var(--space-md);
  border-top: 1px solid rgba(0, 0, 0, 0.04);
  margin-top: var(--space-sm);
  flex-wrap: wrap;
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 10px;
  color: var(--text-tertiary);
}

.dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
}

.dot-hacker { background: var(--accent-purple); box-shadow: 0 0 4px var(--accent-purple); }
.dot-high { background: var(--accent-primary); }
.dot-mid { background: var(--text-tertiary); }
.dot-low { background: var(--accent-danger); opacity: 0.5; }
</style>
