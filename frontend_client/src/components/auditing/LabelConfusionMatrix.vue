<template>
  <div class="glass-card component-wrapper">
    <h4 class="舱室标题">🛰️ 多模态图文语义指鹿为马混淆判定矩阵</h4>
    <div class="matrix-layout">
      <div class="matrix-grid">
        <div class="matrix-row header">
          <div class="cell title">图像 \ 文本</div>
          <div v-for="v in vocab" :key="v" class="cell font-lbl">{{ v }}</div>
        </div>
        <div v-for="img in vocab" :key="img" class="matrix-row">
          <div class="cell font-lbl row-title">{{ img }}</div>
          <div
            v-for="txt in vocab"
            :key="txt"
            class="cell data-cell"
            :class="getCellClass(img, txt)"
          >
            {{ getConfusionValue(img, txt) }}%
          </div>
        </div>
      </div>
    </div>
    <div class="matrix-legend">
      <span class="legend-item"><span class="lg-block diag"></span> 对角匹配 (86%)</span>
      <span class="legend-item"><span class="lg-block trap"></span> 高危混淆 (64%) — redWhistle→yellowBag</span>
    </div>
  </div>
</template>

<script setup>
const vocab = ['pumpkinNotes', 'hairClip', 'eyeball', 'yellowBag', 'redWhistle']

const getConfusionValue = (img, txt) => {
  if (img === txt) return 86
  if (img === 'redWhistle' && txt === 'yellowBag') return 64
  return 3
}

const getCellClass = (img, txt) => {
  if (img === txt) return 'is-diagonal'
  if (img === 'redWhistle' && txt === 'yellowBag') return 'is-trap'
  return ''
}
</script>

<style scoped>
.component-wrapper { display: flex; flex-direction: column; height: 100%; }
.matrix-layout { flex: 1; display: flex; align-items: center; justify-content: center; }
.matrix-grid { display: flex; flex-direction: column; gap: 4px; width: 100%; }
.matrix-row { display: grid; grid-template-columns: 1.2fr repeat(5, 1fr); gap: 4px; }

.cell {
  height: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 11px;
  border-radius: var(--radius-xs);
  background: rgba(0, 0, 0, 0.02);
  color: var(--text-primary);
  transition: all 0.2s var(--ease-out-expo);
}

.font-lbl { color: var(--text-secondary); font-weight: var(--weight-medium); }
.row-title { justify-content: flex-end; padding-right: 8px; }

.is-diagonal {
  background: rgba(49, 194, 124, 0.12) !important;
  color: var(--accent-primary-dark);
  border: 1px solid rgba(49, 194, 124, 0.15);
  font-weight: var(--weight-semibold);
}

.is-trap {
  background: rgba(255, 90, 95, 0.12) !important;
  color: var(--accent-danger);
  font-weight: var(--weight-bold);
  border: 1px solid rgba(255, 90, 95, 0.2);
}

.data-cell:not(.header):hover {
  transform: scale(1.06);
  z-index: 10;
  box-shadow: var(--shadow-sm);
  cursor: pointer;
}

.matrix-legend {
  display: flex;
  gap: var(--space-lg);
  margin-top: var(--space-sm);
  padding-top: var(--space-sm);
  border-top: 1px solid rgba(0, 0, 0, 0.04);
}

.legend-item {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 10px;
  color: var(--text-tertiary);
}

.lg-block {
  width: 12px;
  height: 12px;
  border-radius: 3px;
}

.diag { background: rgba(49, 194, 124, 0.2); border: 1px solid rgba(49, 194, 124, 0.3); }
.trap { background: rgba(255, 90, 95, 0.2); border: 1px solid rgba(255, 90, 95, 0.3); }
</style>
