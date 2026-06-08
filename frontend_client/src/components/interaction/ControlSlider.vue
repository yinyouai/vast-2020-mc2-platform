<template>
  <div class="panel threshold-panel">
    <div class="threshold-copy">
      <span>复核阈值</span>
      <strong>{{ store.scoreThreshold.toFixed(2) }}</strong>
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
    <div class="threshold-scale">
      <span>保留更多</span>
      <span>只看高冲突</span>
    </div>
  </div>
</template>

<script setup>
import { useDashboardStore } from '../../store/dashboard'

const store = useDashboardStore()
</script>

<style scoped>
.threshold-panel {
  display: grid;
  grid-template-columns: auto minmax(180px, 1fr) auto;
  gap: 16px;
  align-items: center;
  padding: 16px 20px;
  border-color: rgba(47, 125, 246, 0.14);
  background:
    linear-gradient(90deg, rgba(47, 125, 246, 0.07), rgba(53, 181, 166, 0.05)),
    rgba(255, 255, 255, 0.1);
  box-shadow: none;
}

.threshold-copy {
  display: grid;
  gap: 3px;
}

.threshold-copy span,
.threshold-scale span {
  color: var(--subtle);
  font-size: 0.76rem;
  font-weight: 900;
  letter-spacing: 0.08em;
}

.threshold-copy strong {
  color: var(--accent);
  font-size: 1.2rem;
  font-variant-numeric: tabular-nums;
}

.threshold-panel input {
  width: 100%;
  accent-color: var(--accent);
}

.threshold-scale {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
  white-space: nowrap;
}

@media (max-width: 760px) {
  .threshold-panel {
    grid-template-columns: 1fr;
  }

  .threshold-scale {
    justify-content: space-between;
  }
}
</style>
