<template>
  <section class="panel process-panel">
    <div class="panel-header">
      <div>
        <h4 class="panel-title">模型审计工作台</h4>
        <p class="panel-subtitle">参考 TTU 的过程型展示方式，把 AP 估计、样本排名、分数分布和标注前后对照放在同一工作面板中。</p>
      </div>
    </div>

    <div class="workbench-grid">
      <aside class="workbench-sidebar">
        <div class="process-control threshold-control">
          <div class="threshold-head">
            <span>动态阈值</span>
            <strong>{{ thresholdLabel }}</strong>
          </div>
          <label class="threshold-slider" for="audit-threshold">
            <span>低召回</span>
            <input
              id="audit-threshold"
              v-model.number="threshold"
              type="range"
              min="0.2"
              max="0.8"
              step="0.01"
              aria-label="调整模型审计阈值"
            />
            <span>高精度</span>
          </label>
          <div class="threshold-metrics">
            <span>保留 {{ keptCount }}</span>
            <span>过滤 {{ filteredCount }}</span>
          </div>
        </div>
        <div class="process-control">
          <span>边界颜色</span>
          <div class="process-legend">
            <span class="legend-pill is-green">真阳性 TP</span>
            <span class="legend-pill is-red">假阳性 FP</span>
          </div>
        </div>
        <div class="process-control">
          <span>当前类别</span>
          <strong>MetalKey / 代表审计流程</strong>
        </div>

        <div class="rank-table">
          <div class="rank-row rank-head">
            <span>样本</span>
            <span>分数</span>
            <span>判定</span>
          </div>
          <div
            v-for="row in rankedRows"
            :key="row.name"
            class="rank-row"
            :class="{ 'is-muted-row': !row.kept }"
          >
            <span>{{ row.name }}</span>
            <span>{{ row.scoreLabel }}</span>
            <span :class="row.badgeClass">{{ row.decision }}</span>
          </div>
        </div>

        <div class="curve-card">
          <div class="curve-card__title">Precision - Recall Curve</div>
          <svg viewBox="0 0 220 160" class="curve-svg" aria-label="PR 曲线">
            <polyline
              fill="none"
              stroke="#2f7df6"
              stroke-width="3"
              points="12,12 44,12 44,78 60,78 60,92 86,92 86,108 118,108 118,126 152,126 152,140"
            />
            <polyline
              fill="none"
              stroke="#f0b44c"
              stroke-width="2"
              stroke-dasharray="5 4"
              points="12,12 44,18 44,76 60,81 60,91 86,98 86,109 118,113 118,126 152,132 152,140"
            />
            <line x1="12" y1="12" x2="12" y2="148" stroke="#b6c5d5" />
            <line x1="12" y1="148" x2="208" y2="148" stroke="#b6c5d5" />
            <line
              :x1="curveThresholdX"
              y1="14"
              :x2="curveThresholdX"
              y2="148"
              stroke="#1c8a67"
              stroke-width="2"
              stroke-dasharray="4 4"
            />
          </svg>
          <p>当前阈值保留 {{ keptCount }} 个候选，误报 {{ falsePositiveCount }} 个。</p>
        </div>
      </aside>

      <div class="sample-scatter-card">
        <div class="sample-scatter-card__head">
          <strong>样本分数分布</strong>
          <span>横轴表示置信分数，纵向层级表示样本排序</span>
        </div>
        <div class="sample-scatter">
          <div
            v-for="sample in samplePoints"
            :key="sample.id"
            class="sample-dot"
            :class="[sample.type === 'TP' ? 'is-green' : 'is-red', { 'is-below-threshold': sample.score < threshold }]"
            :style="{ left: sample.left, top: sample.top }"
          >
            {{ sample.short }}
          </div>
          <div class="threshold-line" :style="{ left: thresholdLeft }">
            <span>{{ thresholdLabel }}</span>
          </div>
        </div>
        <div class="sample-axis">
          <span>0.20</span>
          <span>0.35</span>
          <span>0.50</span>
          <span>0.65</span>
          <span>0.80</span>
          <span>1.00</span>
        </div>
      </div>

      <div class="compare-column">
        <div class="compare-card">
          <div class="compare-card__head">
            <strong>标注前：机器输出</strong>
            <span>多框重叠，类别混杂，说明该样本在低阈值下产生了明显误报污染。</span>
          </div>
          <div class="image-stage">
            <div class="workbench-placeholder" role="img" aria-label="原始样本 Person3_2 占位画布">
              <strong>Person3_2 / 机器检测画布</strong>
              <span>低阈值下多候选框重叠，先展示检测结构，再进入人工收敛。</span>
            </div>
            <img
              :src="reviewImage"
              alt="原始样本 Person3 证据照片"
              :class="{ 'is-loaded': imageState === 'loaded', 'is-failed': imageState === 'failed' }"
              @load="imageState = 'loaded'"
              @error="imageState = 'failed'"
            />
            <span v-if="imageState === 'loading'" class="workbench-image-state">加载真实图片中</span>
            <span v-else-if="imageState === 'failed'" class="workbench-image-state is-failed">图片未就绪，已使用稳定占位</span>
            <div class="bbox bbox-red" data-label="yellowBag 0.39" style="left: 6%; top: 16%; width: 65%; height: 56%;"></div>
            <div class="bbox bbox-gold" data-label="yellowBalloon 0.40" style="left: 0%; top: 0%; width: 76%; height: 57%;"></div>
            <div class="bbox bbox-blue" data-label="pumpkinNotes 0.53" style="left: 0%; top: 0%; width: 80%; height: 82%;"></div>
          </div>
        </div>

        <div class="compare-card">
          <div class="compare-card__head">
            <strong>标注后：人工确认</strong>
            <span>结合文本描述后，仅保留与线下会合相关的主物证，并将其他候选视为背景噪声。</span>
          </div>
          <div class="image-stage is-clean">
            <div class="workbench-placeholder is-clean" role="img" aria-label="人工修正后的样本 Person3_2 占位画布">
              <strong>Person3_2 / 人工确认画布</strong>
              <span>结合文本语义后，只保留与线下会合相关的关键物证。</span>
            </div>
            <img
              :src="reviewImage"
              alt="人工修正后的 Person3 证据照片"
              :class="{ 'is-loaded': imageState === 'loaded', 'is-failed': imageState === 'failed' }"
              @load="imageState = 'loaded'"
              @error="imageState = 'failed'"
            />
            <div class="bbox bbox-green" data-label="黄色提袋 / 人工确认" style="left: 18%; top: 20%; width: 49%; height: 50%;"></div>
          </div>
          <div class="compare-note">
            <p>文本语义指向“入口处的识别标记”，因此人工复核将视觉结果收敛为单一物证。这一步是后续群体聚类可信的关键前提。</p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, ref } from 'vue'

const imageState = ref('loading')
const reviewImage = 'http://localhost:5000/static/MC2-Image-Data/Person3/Person3_1.jpg'
const threshold = ref(0.25)

const rankedSamples = [
  { name: 'Person18_8', score: 0.668, type: 'TP' },
  { name: 'Person9_2', score: 0.664, type: 'TP' },
  { name: 'Person32_22', score: 0.594, type: 'TP' },
  { name: 'Person30_17', score: 0.569, type: 'TP' },
  { name: 'Person23_11', score: 0.563, type: 'FP' },
  { name: 'Person27_14', score: 0.552, type: 'FP' }
]

const samplePoints = [
  { id: 1, short: 'P18', score: 0.668, type: 'TP', left: '72%', top: '10%' },
  { id: 2, short: 'P09', score: 0.664, type: 'TP', left: '69%', top: '22%' },
  { id: 3, short: 'P32', score: 0.594, type: 'TP', left: '58%', top: '31%' },
  { id: 4, short: 'P30', score: 0.569, type: 'TP', left: '52%', top: '46%' },
  { id: 5, short: 'P23', score: 0.563, type: 'FP', left: '44%', top: '40%' },
  { id: 6, short: 'P27', score: 0.552, type: 'FP', left: '47%', top: '58%' },
  { id: 7, short: 'P08', score: 0.418, type: 'TP', left: '38%', top: '72%' },
  { id: 8, short: 'P16', score: 0.326, type: 'FP', left: '29%', top: '84%' },
  { id: 9, short: 'P21', score: 0.506, type: 'TP', left: '63%', top: '79%' },
  { id: 10, short: 'P37', score: 0.708, type: 'FP', left: '77%', top: '88%' }
]

const thresholdLabel = computed(() => threshold.value.toFixed(2))

const rankedRows = computed(() =>
  rankedSamples.map((row) => {
    const kept = row.score >= threshold.value

    return {
      ...row,
      kept,
      scoreLabel: row.score.toFixed(3),
      decision: kept ? row.type : '过滤',
      badgeClass: kept ? (row.type === 'TP' ? 'is-green' : 'is-red') : 'is-filtered'
    }
  })
)

const keptCount = computed(() => rankedRows.value.filter((row) => row.kept).length)
const filteredCount = computed(() => rankedRows.value.length - keptCount.value)
const falsePositiveCount = computed(
  () => rankedRows.value.filter((row) => row.kept && row.type === 'FP').length
)
const thresholdLeft = computed(() => `${((threshold.value - 0.2) / 0.8) * 100}%`)
const curveThresholdX = computed(() => 12 + ((threshold.value - 0.2) / 0.8) * 196)
</script>

<style scoped>
.process-panel {
  overflow: hidden;
  padding: clamp(22px, 3vw, 34px);
}

.workbench-grid {
  display: grid;
  grid-template-columns: minmax(260px, 300px) minmax(420px, 1fr) minmax(330px, 450px);
  gap: clamp(18px, 2.2vw, 28px);
  align-items: stretch;
}

.workbench-sidebar,
.compare-column {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.process-control,
.curve-card,
.sample-scatter-card,
.compare-card {
  padding: 16px;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.92), rgba(247, 251, 255, 0.82)),
    rgba(255, 255, 255, 0.82);
  transition:
    transform var(--motion-medium) var(--ease-spring),
    border-color var(--motion-medium) ease,
    box-shadow var(--motion-medium) ease;
}

.process-control:hover,
.curve-card:hover,
.sample-scatter-card:hover,
.compare-card:hover {
  transform: translateY(-3px);
  border-color: rgba(47, 125, 246, 0.18);
  box-shadow: var(--shadow-soft);
}

.process-control span,
.curve-card__title,
.compare-card__head span,
.sample-scatter-card__head span {
  display: block;
  color: var(--subtle);
  font-size: 0.8rem;
  line-height: 1.55;
}

.process-control strong,
.sample-scatter-card__head strong,
.compare-card__head strong {
  display: block;
  margin-top: 6px;
  font-size: 1rem;
}

.threshold-control {
  background:
    radial-gradient(circle at 86% 18%, rgba(47, 125, 246, 0.12), transparent 28%),
    linear-gradient(180deg, rgba(255, 255, 255, 0.94), rgba(247, 251, 255, 0.86));
}

.threshold-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 12px;
}

.threshold-head strong {
  margin-top: 0;
  font-size: 1.35rem;
  font-variant-numeric: tabular-nums;
}

.threshold-slider {
  display: grid;
  grid-template-columns: auto minmax(0, 1fr) auto;
  gap: 10px;
  align-items: center;
  margin-top: 14px;
  color: var(--subtle);
  font-size: 0.72rem;
  font-weight: 800;
}

.threshold-slider input {
  width: 100%;
  height: 32px;
  accent-color: var(--accent);
  cursor: pointer;
}

.threshold-slider input:focus-visible {
  outline: 3px solid rgba(47, 125, 246, 0.2);
  outline-offset: 3px;
  border-radius: 999px;
}

.threshold-metrics {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 12px;
}

.threshold-metrics span {
  display: inline-flex;
  min-height: 28px;
  align-items: center;
  padding: 0 10px;
  border-radius: 999px;
  color: var(--text);
  background: rgba(47, 125, 246, 0.08);
  font-size: 0.74rem;
  font-weight: 900;
}

.process-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 10px;
}

.legend-pill {
  display: inline-flex;
  align-items: center;
  padding: 6px 10px;
  border-radius: 999px;
  font-size: 0.78rem;
  font-weight: 700;
}

.is-green {
  color: #1c8a67;
}

.is-red {
  color: #c55353;
}

.is-filtered {
  color: var(--subtle);
}

.legend-pill.is-green {
  background: rgba(57, 169, 125, 0.12);
}

.legend-pill.is-red {
  background: rgba(223, 106, 106, 0.12);
}

.rank-table {
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  overflow: hidden;
  background: rgba(255, 255, 255, 0.88);
}

.rank-row {
  display: grid;
  grid-template-columns: 1.6fr 0.8fr 0.7fr;
  gap: 8px;
  padding: 10px 12px;
  font-size: 0.84rem;
  border-top: 1px solid rgba(53, 89, 138, 0.08);
}

.rank-row:first-child {
  border-top: 0;
}

.rank-head {
  color: var(--subtle);
  font-weight: 700;
  background: rgba(47, 125, 246, 0.05);
}

.rank-row.is-muted-row {
  color: var(--subtle);
  background: rgba(245, 248, 252, 0.72);
}

.curve-card p,
.compare-note p {
  margin: 10px 0 0;
  color: var(--muted);
  line-height: 1.7;
}

.curve-svg {
  width: 100%;
  height: 160px;
  margin-top: 8px;
  background: linear-gradient(180deg, #ffffff, #f7faff);
  border-radius: 10px;
}

.sample-scatter-card {
  display: flex;
  flex-direction: column;
}

.sample-scatter {
  position: relative;
  flex: 1;
  min-height: clamp(500px, 52dvh, 680px);
  margin-top: 12px;
  border-radius: 16px;
  background:
    linear-gradient(rgba(47, 125, 246, 0.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(47, 125, 246, 0.05) 1px, transparent 1px),
    linear-gradient(180deg, #ffffff, #f7fbff);
  background-size: 100% 72px, 14.28% 100%, 100% 100%;
  overflow: hidden;
}

.sample-dot {
  position: absolute;
  display: grid;
  place-items: center;
  width: 42px;
  height: 28px;
  border-radius: 8px;
  font-size: 0.74rem;
  font-weight: 800;
  color: #ffffff;
  transform: translate(-50%, -50%);
  box-shadow: var(--shadow-soft);
  transition:
    transform var(--motion-fast) var(--ease-spring),
    box-shadow var(--motion-fast) ease;
}

.sample-dot:hover {
  transform: translate(-50%, -50%) scale(1.08);
  box-shadow: 0 14px 24px rgba(48, 78, 114, 0.16);
}

.sample-dot.is-below-threshold {
  opacity: 0.26;
  filter: grayscale(0.4);
}

.sample-dot.is-green {
  background: linear-gradient(135deg, #39a97d, #70c9a7);
}

.sample-dot.is-red {
  background: linear-gradient(135deg, #df6a6a, #f0a2a2);
}

.threshold-line {
  position: absolute;
  top: 0;
  bottom: 0;
  z-index: 2;
  width: 2px;
  background: linear-gradient(180deg, rgba(28, 138, 103, 0), rgba(28, 138, 103, 0.88), rgba(28, 138, 103, 0));
  transform: translateX(-50%);
  transition: left var(--motion-fast) var(--ease-spring);
}

.threshold-line span {
  position: absolute;
  top: 12px;
  left: 8px;
  padding: 5px 9px;
  border: 1px solid rgba(57, 169, 125, 0.24);
  border-radius: 999px;
  color: #1c8a67;
  background: rgba(255, 255, 255, 0.92);
  box-shadow: var(--shadow-soft);
  font-size: 0.72rem;
  font-weight: 900;
  font-variant-numeric: tabular-nums;
}

.sample-axis {
  display: grid;
  grid-template-columns: repeat(6, 1fr);
  margin-top: 10px;
  color: var(--subtle);
  font-size: 0.78rem;
}

.compare-card__head {
  margin-bottom: 12px;
}

.image-stage {
  position: relative;
  overflow: hidden;
  border-radius: 14px;
  background:
    linear-gradient(rgba(47, 125, 246, 0.06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(47, 125, 246, 0.06) 1px, transparent 1px),
    linear-gradient(180deg, #ffffff, #f8fbff);
  background-size: 100% 46px, 46px 100%, 100% 100%;
  border: 1px solid rgba(53, 89, 138, 0.12);
  min-height: 220px;
}

.workbench-placeholder {
  position: relative;
  z-index: 1;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  min-height: 270px;
  padding: 18px;
  color: var(--muted);
}

.workbench-placeholder.is-clean {
  background: radial-gradient(circle at top right, rgba(57, 169, 125, 0.1), transparent 30%);
}

.workbench-placeholder strong {
  margin-bottom: 8px;
  color: var(--text);
  font-size: 1rem;
}

.workbench-placeholder span {
  max-width: 260px;
  line-height: 1.65;
  font-size: 0.84rem;
}

.image-stage img {
  position: absolute;
  inset: 0;
  z-index: 2;
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0;
  transition: opacity var(--motion-medium) ease;
}

.image-stage img.is-loaded {
  opacity: 1;
}

.image-stage img.is-failed {
  display: none;
}

.workbench-image-state {
  position: absolute;
  left: 14px;
  top: 14px;
  z-index: 4;
  display: inline-flex;
  align-items: center;
  min-height: 30px;
  padding: 0 11px;
  border: 1px solid var(--border);
  border-radius: 999px;
  color: var(--muted);
  background: rgba(255, 255, 255, 0.9);
  box-shadow: var(--shadow-soft);
  font-size: 0.74rem;
  font-weight: 900;
}

.workbench-image-state::before {
  content: "";
  width: 8px;
  height: 8px;
  margin-right: 6px;
  border: 2px solid rgba(47, 125, 246, 0.18);
  border-top-color: var(--accent);
  border-radius: 999px;
  animation: workbench-spin 760ms linear infinite;
}

.workbench-image-state.is-failed {
  color: #9a6818;
  border-color: rgba(240, 180, 76, 0.24);
  background: rgba(255, 247, 219, 0.92);
}

.workbench-image-state.is-failed::before {
  display: none;
}

.bbox {
  position: absolute;
  z-index: 3;
  border: 3px solid;
  border-radius: 12px;
  font-size: 0;
  font-weight: 800;
  color: transparent;
  background: transparent;
  box-shadow: none;
  pointer-events: none;
}

.bbox::before {
  content: attr(data-label);
  position: absolute;
  left: 10px;
  top: -10px;
  transform: translateY(-100%);
  display: inline-flex;
  align-items: center;
  padding: 5px 9px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.9);
  box-shadow: var(--shadow-soft);
  white-space: nowrap;
  font-size: 0.72rem;
  color: currentColor;
}

@keyframes workbench-spin {
  to {
    transform: rotate(360deg);
  }
}

.bbox-red {
  border-color: #df6a6a;
  color: #b44e4e;
}

.bbox-gold {
  border-color: #f0b44c;
  color: #a56e1d;
}

.bbox-blue {
  border-color: #2f7df6;
  color: #1d58b1;
}

.bbox-green {
  border-color: #39a97d;
  color: #25795a;
}

@media (max-width: 1320px) {
  .workbench-grid {
    grid-template-columns: 1fr;
  }
}
</style>
