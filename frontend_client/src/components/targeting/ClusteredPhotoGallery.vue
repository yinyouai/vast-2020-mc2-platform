<template>
  <div class="glass-card gallery-container">
    <h4 class="舱室标题">🧬 40 人聚类分组照片廊 — 嫌疑社群行为特征可视化</h4>

    <div class="groups-layout">
      <!-- 集团 C: 核心黑客组织 (8 人) -->
      <div class="group-section group-hacker">
        <div class="group-header">
          <span class="group-badge badge-purple">集团 C</span>
          <h5>🎯 核心黑客组织帮派 (8 名成员)</h5>
          <p class="group-desc">孤立方阵 — 行为光谱完全脱离会场主流，不持有任何普及免费礼品，绝对死锁共现</p>
        </div>
        <div class="group-photos">
          <div
            v-for="pid in hackerGroup"
            :key="pid"
            class="group-photo-item is-hacker"
            @click="onClickPerson(pid)"
          >
            <img :src="getPhotoUrl(pid)" :alt="pid" loading="lazy" />
            <div class="photo-overlay">
              <span class="photo-id">{{ pid }}</span>
              <span class="check-icon">✓</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 集团 A: 外围正常参会群体 -->
      <div class="group-section group-normal">
        <div class="group-header">
          <span class="group-badge badge-default">集团 A</span>
          <h5>🔒 外围正常参会群体 (背景噪声)</h5>
          <p class="group-desc">色块死死锚定在【南瓜便签】【眼球玩具】【高危哨子】— 会场普及分发物资</p>
        </div>
        <div class="group-photos">
          <div
            v-for="pid in groupA"
            :key="pid"
            class="group-photo-item"
            @click="onClickPerson(pid)"
          >
            <img :src="getPhotoUrl(pid)" :alt="pid" loading="lazy" />
            <div class="photo-overlay">
              <span class="photo-id">{{ pid }}</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 集团 B: 混合区 -->
      <div class="group-section group-mixed">
        <div class="group-header">
          <span class="group-badge badge-blue">集团 B</span>
          <h5>🔍 混合杂散群体</h5>
          <p class="group-desc">部分持有普及物资，行为特征介于外围与核心之间的过渡区</p>
        </div>
        <div class="group-photos">
          <div
            v-for="pid in groupB"
            :key="pid"
            class="group-photo-item"
            @click="onClickPerson(pid)"
          >
            <img :src="getPhotoUrl(pid)" :alt="pid" loading="lazy" />
            <div class="photo-overlay">
              <span class="photo-id">{{ pid }}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { useDashboardStore } from '../../store/dashboard'
import { HACKER_LIST, TOTAL_PEOPLE } from '../../constants/forensics'

const store = useDashboardStore()
const router = useRouter()

const API_BASE = 'http://localhost:5000'

const hackerGroup = HACKER_LIST

// 基于聚类结果分配人员到各集团 (如果后端有排序数据则优先使用，否则回退到默认分区)
const groupA = computed(() => {
  if (store.orderedSuspects.length > 0) {
    // 后 17 人为外围
    return store.orderedSuspects.slice(-17).filter(p => !HACKER_LIST.includes(p))
  }
  // 默认分区
  return Array.from({ length: 17 }, (_, i) => {
    const num = i + 24
    return `Person${num}`
  })
})

const groupB = computed(() => {
  if (store.orderedSuspects.length > 0) {
    // 中间 15 人为混合区
    const mid = Math.floor(store.orderedSuspects.length * 0.4)
    return store.orderedSuspects.slice(mid, mid + 15).filter(p => !HACKER_LIST.includes(p))
  }
  return Array.from({ length: 15 }, (_, i) => {
    const num = i + 9
    return `Person${num}`
  })
})

function getPhotoUrl(personId) {
  return `${API_BASE}/static/MC2-Image-Data/${personId}/${personId}_1.jpg`
}

function onClickPerson(personId) {
  store.selectPerson(personId)
  router.push('/task2_correction')
}
</script>

<style scoped>
.gallery-container {
  display: flex;
  flex-direction: column;
  min-height: 0;
  overflow-y: auto;
}

.groups-layout {
  display: flex;
  flex-direction: column;
  gap: var(--space-xl);
  margin-top: var(--space-sm);
}

.group-section {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
  padding: var(--space-md);
  border-radius: var(--radius-md);
  border: 1px solid rgba(0, 0, 0, 0.04);
  background: rgba(0, 0, 0, 0.01);
  transition: all 0.3s var(--ease-out-expo);
}

.group-section:hover {
  background: rgba(0, 0, 0, 0.02);
}

.group-hacker {
  border-color: rgba(191, 90, 242, 0.2);
  background: rgba(191, 90, 242, 0.02);
}

.group-header {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: var(--space-sm);
  margin-bottom: var(--space-xs);
}

.group-header h5 {
  margin: 0;
  font-size: var(--text-sm);
  font-weight: var(--weight-semibold);
  color: var(--text-primary);
}

.group-desc {
  width: 100%;
  margin: 2px 0 0;
  font-size: var(--text-xs);
  color: var(--text-tertiary);
  line-height: var(--leading-relaxed);
}

.group-badge {
  font-size: 10px;
  font-weight: var(--weight-bold);
  padding: 2px 8px;
  border-radius: var(--radius-full);
}

.badge-purple {
  background: var(--accent-purple-light);
  color: var(--accent-purple);
}

.badge-default {
  background: rgba(0, 0, 0, 0.05);
  color: var(--text-secondary);
}

.badge-blue {
  background: var(--accent-blue-light);
  color: var(--accent-blue);
}

.group-photos {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.group-photo-item {
  position: relative;
  width: 62px;
  height: 62px;
  border-radius: var(--radius-sm);
  overflow: hidden;
  border: 2.5px solid rgba(0, 0, 0, 0.06);
  cursor: pointer;
  transition: all 0.3s var(--ease-out-expo);
}

.group-photo-item img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.4s var(--ease-out-expo);
}

.group-photo-item:hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-card-hover);
  border-color: var(--accent-primary);
  z-index: 2;
}

.group-photo-item:hover img {
  transform: scale(1.12);
}

.group-photo-item.is-hacker {
  border-color: var(--accent-purple);
  box-shadow: 0 0 10px rgba(191, 90, 242, 0.2);
}

.photo-overlay {
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  padding: 3px 5px;
  background: linear-gradient(transparent, rgba(0, 0, 0, 0.6));
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.photo-id {
  color: #fff;
  font-size: 8px;
  font-weight: var(--weight-medium);
}

.check-icon {
  color: var(--accent-primary);
  font-size: 8px;
  font-weight: var(--weight-bold);
}
</style>
