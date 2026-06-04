<template>
  <div class="glass-card roster-container">
    <h4 class="舱室标题">🚨 核心组织 8 名黑客骨干终审照片名册</h4>
    <div class="roster-grid">
      <div
        v-for="pid in HACKER_LIST"
        :key="pid"
        class="roster-card"
        :class="{ active: store.selectedPersonId === pid }"
        @click="store.selectPerson(pid)"
      >
        <div class="roster-photo-wrap">
          <img :src="getPhotoUrl(pid)" :alt="pid" loading="lazy" />
          <div class="verified-badge" title="证据链已闭环确认">✓ 已确认</div>
        </div>
        <div class="roster-info">
          <span class="roster-id">{{ pid }}</span>
          <span class="roster-evidence">{{ getEvidence(pid) }}</span>
        </div>
        <div class="roster-glow"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useDashboardStore } from '../../store/dashboard'
import { HACKER_LIST } from '../../constants/forensics'

const store = useDashboardStore()
const API_BASE = 'http://localhost:5000'

function getPhotoUrl(personId) {
  return `${API_BASE}/static/MC2-Image-Data/${personId}/${personId}_1.jpg`
}

function getEvidence(personId) {
  const map = {
    'Person3': '持有接头图腾+图文冲突78%',
    'Person7': '线上零互动+加密行动记录',
    'Person9': '黄色信标+网络隔离防线',
    'Person10': '绝对零互动+物理接头',
    'Person12': '加密协议+网络陌生人伪装',
    'Person17': '图腾核验+通讯熔断',
    'Person32': '暗号物资+绝对隔离',
    'Person38': '图腾持有+网络真空'
  }
  return map[personId] || '铁证互锁已确认'
}
</script>

<style scoped>
.roster-container {
  display: flex;
  flex-direction: column;
  min-height: 0;
}

.roster-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: var(--space-md);
  margin-top: var(--space-sm);
  flex: 1;
  overflow-y: auto;
}

.roster-card {
  position: relative;
  display: flex;
  flex-direction: column;
  border-radius: var(--radius-md);
  overflow: hidden;
  border: 3px solid var(--accent-purple);
  cursor: pointer;
  transition: all 0.35s var(--ease-out-expo);
  background: #fff;
  box-shadow: var(--shadow-card);
  animation: breath-glow 3s infinite;
}

.roster-card:hover {
  transform: translateY(-3px);
  box-shadow: var(--shadow-card-hover), 0 0 20px rgba(191, 90, 242, 0.3);
}

.roster-card.active {
  border-color: var(--accent-primary);
  box-shadow: 0 0 24px rgba(49, 194, 124, 0.3);
  animation: none;
}

.roster-photo-wrap {
  position: relative;
  aspect-ratio: 1;
  overflow: hidden;
}

.roster-photo-wrap img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.5s var(--ease-out-expo);
}

.roster-card:hover .roster-photo-wrap img {
  transform: scale(1.08);
}

.verified-badge {
  position: absolute;
  top: 6px;
  right: 6px;
  padding: 2px 8px;
  background: var(--accent-primary);
  color: #fff;
  font-size: 9px;
  font-weight: var(--weight-bold);
  border-radius: var(--radius-full);
  box-shadow: 0 2px 6px rgba(49, 194, 124, 0.4);
}

.roster-info {
  padding: var(--space-sm);
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.roster-id {
  font-size: var(--text-sm);
  font-weight: var(--weight-bold);
  color: var(--text-primary);
}

.roster-evidence {
  font-size: 9px;
  color: var(--text-tertiary);
  line-height: var(--leading-tight);
}

.roster-glow {
  position: absolute;
  inset: 0;
  border-radius: inherit;
  pointer-events: none;
  box-shadow: inset 0 0 16px rgba(191, 90, 242, 0.08);
}

@media (max-width: 768px) {
  .roster-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
</style>
