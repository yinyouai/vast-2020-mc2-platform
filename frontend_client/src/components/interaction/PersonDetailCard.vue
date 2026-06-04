<template>
  <div class="glass-card detail-card">
    <div class="detail-header">
      <div class="person-identity">
        <img
          :src="photoUrl"
          :alt="personId"
          class="person-avatar-lg"
          @error="onImgError"
        />
        <div class="identity-text">
          <h3 class="person-name">{{ personId }}</h3>
          <span class="badge" :class="statusBadgeClass">{{ statusLabel }}</span>
        </div>
      </div>
      <button class="btn-ghost" @click="$emit('close')" v-if="$attrs.onClose">✕</button>
    </div>

    <!-- 照片画廊 -->
    <div class="detail-section">
      <h5 class="section-title">📷 现场物证照片卷宗</h5>
      <div class="photo-strip">
        <div
          v-for="idx in photoCount"
          :key="idx"
          class="photo-thumb"
          :class="{ active: selectedPhotoIdx === idx }"
          @click="selectedPhotoIdx = idx"
        >
          <img
            :src="`${API_BASE}/static/MC2-Image-Data/${personId}/${personId}_${idx}.jpg`"
            :alt="`${personId}_${idx}`"
            loading="lazy"
          />
        </div>
      </div>
      <div class="photo-preview" v-if="selectedPhotoIdx">
        <img
          :src="`${API_BASE}/static/MC2-Image-Data/${personId}/${personId}_${selectedPhotoIdx}.jpg`"
          :alt="`${personId}_${selectedPhotoIdx} 预览`"
        />
      </div>
    </div>

    <!-- 情报摘要 -->
    <div class="detail-section">
      <h5 class="section-title">📋 情报摘要</h5>
      <div class="info-cards">
        <div class="info-card" v-if="isHacker">
          <span class="info-icon">⚠️</span>
          <div>
            <strong>高危白帽骨干</strong>
            <p>该人员 100% 独立持有秘密接头图腾【黄色提袋】，线上社交呈现极致隔离。</p>
          </div>
        </div>
        <div class="info-card" v-else>
          <span class="info-icon">🔒</span>
          <div>
            <strong>外围无害参会者</strong>
            <p>所有持有物资均为会场免费普及礼品，无任何特异性特征，嫌疑已被反向排除。</p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { HACKER_LIST, isTrueHacker } from '../../constants/forensics'

const props = defineProps({
  personId: { type: String, default: 'Person3' }
})

defineEmits(['close'])

const API_BASE = 'http://localhost:5000'
const selectedPhotoIdx = ref(1)

const photoUrl = computed(() => `${API_BASE}/static/MC2-Image-Data/${props.personId}/${props.personId}_1.jpg`)

const isHacker = computed(() => isTrueHacker(props.personId))

const statusLabel = computed(() => isHacker.value ? '高危白帽骨干' : '外围无害路人')

const statusBadgeClass = computed(() => isHacker.value ? 'badge-purple' : 'badge-default')

const photoCount = computed(() => {
  const num = parseInt(props.personId.replace('Person', ''))
  return num <= 3 ? 6 : num <= 10 ? 5 : 4
})

function onImgError(e) {
  e.target.style.display = 'none'
}
</script>

<style scoped>
.detail-card {
  display: flex;
  flex-direction: column;
  gap: var(--space-lg);
  height: 100%;
  min-height: 0;
  overflow-y: auto;
}

.detail-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.person-identity {
  display: flex;
  align-items: center;
  gap: var(--space-md);
}

.identity-text {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.person-name {
  margin: 0;
  font-size: var(--text-md);
  font-weight: var(--weight-semibold);
  color: var(--text-primary);
}

.detail-section {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.section-title {
  margin: 0;
  font-size: var(--text-xs);
  font-weight: var(--weight-semibold);
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.photo-strip {
  display: flex;
  gap: 6px;
  overflow-x: auto;
  padding-bottom: 4px;
}

.photo-thumb {
  width: 52px;
  height: 52px;
  border-radius: var(--radius-xs);
  overflow: hidden;
  border: 2px solid transparent;
  cursor: pointer;
  transition: all 0.2s var(--ease-out-expo);
  flex-shrink: 0;
}

.photo-thumb img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.photo-thumb:hover {
  border-color: var(--accent-primary);
  transform: translateY(-1px);
}

.photo-thumb.active {
  border-color: var(--accent-primary);
  box-shadow: 0 0 8px rgba(49, 194, 124, 0.3);
}

.photo-preview {
  border-radius: var(--radius-sm);
  overflow: hidden;
  background: var(--bg-secondary);
  max-height: 200px;
}

.photo-preview img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.info-cards {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.info-card {
  display: flex;
  gap: var(--space-sm);
  padding: var(--space-md);
  background: rgba(0, 0, 0, 0.02);
  border-radius: var(--radius-sm);
  font-size: var(--text-xs);
  color: var(--text-secondary);
  line-height: var(--leading-relaxed);
}

.info-card strong {
  color: var(--text-primary);
  display: block;
  margin-bottom: 2px;
}

.info-icon {
  font-size: 16px;
  flex-shrink: 0;
  margin-top: 1px;
}
</style>
