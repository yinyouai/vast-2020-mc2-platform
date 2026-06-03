<template>
  <div class="apple-glass-card component-wrapper">
    <h4 class="舱室标题">🛰️ 组件 2 : 多模态图文语义指鹿为马混淆判定矩阵</h4>
    <div class="matrix-layout">
      <div class="matrix-grid">
        <div class="matrix-row header">
          <div class="cell title">图像 \ 文本</div>
          <div v-for="v in vocab" :key="v" class="cell font-lbl">{{ v }}</div>
        </div>
        <div v-for="img in vocab" :key="img" class="matrix-row">
          <div class="cell font-lbl row-title">{{ img }}</div>
          <div v-for="txt in vocab" :key="txt" class="cell data-cell" :class="getCellClass(img, txt)">
            {{ getConfusionValue(img, txt) }}%
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
const vocab = ["pumpkinNotes", "hairClip", "eyeball", "yellowBag", "redWhistle"]

const getConfusionValue = (img, txt) => {
  if (img === txt) return 86
  if (img === 'redWhistle' && txt === 'yellowBag') return 64 // 赛题预埋核心错位特征
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
.cell { height: 32px; display: flex; align-items: center; justify-content: center; font-size: 11px; border-radius: 6px; background: rgba(255,255,255,0.02); color: #E5E5EA; }
.font-lbl { color: #AEAED2; font-weight: 500; }
.row-title { justify-content: flex-end; padding-right: 8px; }

.is-diagonal { background: rgba(48, 209, 88, 0.2) !important; color: #30D158; border: 1px solid rgba(48, 209, 88, 0.1); }
.is-trap { background: rgba(255, 90, 95, 0.25) !important; color: #FF5A5F; font-weight: bold; border: 1px solid rgba(255, 90, 95, 0.2); }
.data-cell:not(.header):hover { transform: scale(1.05); z-index: 10; box-shadow: 0 4px 12px rgba(0,0,0,0.5); cursor: pointer; }
</style>