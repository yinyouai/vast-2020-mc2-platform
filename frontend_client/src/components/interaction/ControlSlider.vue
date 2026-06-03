<template>
  <div class="apple-glass-card slider-container">
    <div class="flex-control">
      <label>🎛️ 全局动态置信度噪声过滤阀门 (Score Threshold): <span class="val-txt">{{ store.scoreThreshold }}</span></label>
      <input type="range" min="0.25" max="0.95" step="0.05" :value="store.scoreThreshold" @input="onSliderChange" class="apple-slider" />
    </div>
  </div>
</template>

<script setup>
import { useDashboardStore } from '../../store/dashboard'
const store = useDashboardStore()

const onSliderChange = (e) => {
  store.setScoreThreshold(parseFloat(e.target.value)) // 动态驱动全局门限流变
}
</script>

<style scoped>
.slider-container { padding: 14px 24px; border-left: 4px solid var(--accent-truth); }
.flex-control { display: flex; flex-direction: column; gap: 6px; }
label { font-size: 13px; color: #E5E5EA; font-weight: 500; }
.val-txt { color: var(--accent-truth); font-weight: bold; font-family: monospace; font-size: 14px; }
.apple-slider { -webkit-appearance: none; width: 100%; height: 5px; background: rgba(255,255,255,0.1); border-radius: 4px; outline: none; margin-top: 4px; }
.apple-slider::-webkit-slider-thumb { -webkit-appearance: none; width: 14px; height: 14px; background: #FFF; border-radius: 50%; cursor: pointer; box-shadow: 0 2px 6px rgba(0,0,0,0.5); }
</style>