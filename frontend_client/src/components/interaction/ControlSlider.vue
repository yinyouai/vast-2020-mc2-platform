<template>
  <div class="panel threshold-panel">
    <div class="panel-header">
      <div>
        <h4 class="panel-title">复核阈值</h4>
        <p class="panel-subtitle">提高阈值会隐藏低置信框，帮助分析者把注意力集中到真正值得复核的冲突样本上。</p>
      </div>
      <span class="threshold-chip">{{ store.scoreThreshold.toFixed(2) }}</span>
    </div>
    <input
      type="range"
      min="0.25"
      max="0.95"
      step="0.05"
      :value="store.scoreThreshold"
      @input="store.setScoreThreshold(Number($event.target.value))"
      aria-label="复核阈值"
    />
  </div>
</template>

<script setup>
import { useDashboardStore } from '../../store/dashboard'

const store = useDashboardStore()
</script>

<style scoped>
.threshold-panel {
  box-shadow: none;
}
</style>
