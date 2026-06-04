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
        <div class="process-control">
          <span>阈值</span>
          <strong>0.20</strong>
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
          <div v-for="row in rankedSamples" :key="row.name" class="rank-row">
            <span>{{ row.name }}</span>
            <span>{{ row.score }}</span>
            <span :class="row.type === 'TP' ? 'is-green' : 'is-red'">{{ row.type }}</span>
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
          </svg>
          <p>AP 估计值：20.97%。通过人工确认 TP / FP 后，曲线会实时更新，帮助我们判断该类别是否值得继续信任。</p>
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
            :class="sample.type === 'TP' ? 'is-green' : 'is-red'"
            :style="{ left: sample.left, top: sample.top }"
          >
            {{ sample.short }}
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
            <div class="bbox bbox-red" style="left: 6%; top: 16%; width: 65%; height: 56%;">
              yellowBag 0.39
            </div>
            <div class="bbox bbox-gold" style="left: 0%; top: 0%; width: 76%; height: 57%;">
              yellowBalloon 0.40
            </div>
            <div class="bbox bbox-blue" style="left: 0%; top: 0%; width: 80%; height: 82%;">
              pumpkinNotes 0.53
            </div>
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
            <div class="bbox bbox-green" style="left: 18%; top: 20%; width: 49%; height: 50%;">
              黄色提袋 / 人工确认
            </div>
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
const rankedSamples = [
  { name: 'Person18_8', score: '0.668', type: 'TP' },
  { name: 'Person9_2', score: '0.664', type: 'TP' },
  { name: 'Person32_22', score: '0.594', type: 'TP' },
  { name: 'Person30_17', score: '0.569', type: 'TP' },
  { name: 'Person23_11', score: '0.563', type: 'FP' },
  { name: 'Person27_14', score: '0.552', type: 'FP' }
]

const samplePoints = [
  { id: 1, short: 'P18', type: 'TP', left: '72%', top: '10%' },
  { id: 2, short: 'P09', type: 'TP', left: '69%', top: '22%' },
  { id: 3, short: 'P32', type: 'TP', left: '58%', top: '31%' },
  { id: 4, short: 'P30', type: 'TP', left: '52%', top: '46%' },
  { id: 5, short: 'P23', type: 'FP', left: '44%', top: '40%' },
  { id: 6, short: 'P27', type: 'FP', left: '47%', top: '58%' },
  { id: 7, short: 'P08', type: 'TP', left: '38%', top: '72%' },
  { id: 8, short: 'P16', type: 'FP', left: '29%', top: '84%' },
  { id: 9, short: 'P21', type: 'TP', left: '63%', top: '79%' },
  { id: 10, short: 'P37', type: 'FP', left: '77%', top: '88%' }
]
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

.sample-dot.is-green {
  background: linear-gradient(135deg, #39a97d, #70c9a7);
}

.sample-dot.is-red {
  background: linear-gradient(135deg, #df6a6a, #f0a2a2);
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

.bbox {
  position: absolute;
  border: 3px solid;
  border-radius: 12px;
  padding: 6px 8px;
  font-size: 0.72rem;
  font-weight: 800;
  background: rgba(255, 255, 255, 0.7);
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
