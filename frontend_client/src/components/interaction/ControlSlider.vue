<template>
  <div class="glass-card slider-container">
    <div class="slider-top">
      <label class="slider-label">
        🎛️ 全局动态置信度噪声过滤阀门
        <span class="val-txt">{{ store.scoreThreshold }}</span>
      </label>
      <div class="preset-btns">
        <button
          v-for="p in presets"
          :key="p.value"
          class="preset-btn"
          :class="{ active: Math.abs(store.scoreThreshold - p.value) < 0.01 }"
          @click="store.setScoreThreshold(p.value)"
        >{{ p.label }}</button>
      </div>
    </div>
    <input
      type="range"
      min="0.25"
      max="0.95"
      step="0.05"
      :value="store.scoreThreshold"
      @input="onSliderChange"
      class="apple-slider enhanced-slider"
    />
  </div>
</template>

<script setup>
import { useDashboardStore } from '../../store/dashboard'
const store = useDashboardStore()

const presets = [
  { label: '低噪声', value: 0.25 },
  { label: '中等', value: 0.50 },
  { label: '中等偏高', value: 0.75 },
  { label: '高纯度', value: 0.95 }
]

const onSliderChange = (e) => {
  store.setScoreThreshold(parseFloat(e.target.value))
}
</script>

<style scoped>
.slider-container {
  padding: var(--space-md) var(--space-xl);
  border-left: 4px solid var(--accent-primary);
  flex-shrink: 0;
}

.slider-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: var(--space-sm);
  flex-wrap: wrap;
  gap: var(--space-sm);
}

.slider-label {
  font-size: var(--text-sm);
  color: var(--text-primary);
  font-weight: var(--weight-medium);
}

.val-txt {
  color: var(--accent-primary);
  font-weight: var(--weight-bold);
  font-family: var(--font-mono);
  font-size: var(--text-md);
  margin-left: 6px;
}

.preset-btns {
  display: flex;
  gap: 5px;
}

.preset-btn {
  padding: 3px 10px;
  border-radius: var(--radius-full);
  border: 1px solid rgba(0, 0, 0, 0.08);
  background: rgba(255, 255, 255, 0.5);
  color: var(--text-tertiary);
  font-size: 10px;
  cursor: pointer;
  transition: all 0.2s var(--ease-out-expo);
}

.preset-btn:hover {
  background: rgba(49, 194, 124, 0.06);
}

.preset-btn.active {
  background: var(--accent-primary);
  color: #fff;
  border-color: var(--accent-primary);
}

.enhanced-slider {
  margin-top: 4px;
}
</style>
