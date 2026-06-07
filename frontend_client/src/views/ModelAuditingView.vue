<template>
  <section class="view-grid-layout audit-page">
    <div class="page-intro">
      <div>
        <p class="eyebrow">任务 1 / 原始模型审计</p>
        <h3>先把模型的盲区和阈值代价量出来。</h3>
        <div class="intro-pills"><span class="data-chip">类别覆盖</span><span class="data-chip">置信度分布</span><span class="data-chip">阈值联动</span></div>
      </div>
      <div class="audit-status">
        <span>当前审计范围</span><strong>全部 {{ audit.detected_class_count || 0 }} 类</strong><small>{{ audit.total_predictions || 0 }} 个原始检测框</small>
      </div>
    </div>

    <section class="audit-command panel">
      <div class="threshold-copy">
        <span class="section-kicker">全局工作阈值</span>
        <strong>{{ store.scoreThreshold.toFixed(2) }}</strong>
        <p>同步过滤箱线图工作点、检测框散点、人员级指标和第三页原始矩阵。</p>
      </div>
      <div class="threshold-control">
        <input type="range" min=".25" max=".75" step=".05" :value="store.scoreThreshold"
          aria-label="原始预测置信度阈值" @input="store.setScoreThreshold($event.target.value)" />
        <div class="threshold-ticks"><span v-for="tick in thresholdTicks" :key="tick">{{ tick.toFixed(2) }}</span></div>
      </div>
      <div class="threshold-impact">
        <article><span>检测保留率</span><b>{{ percent(currentPoint.retention_rate) }}</b></article>
        <article><span>类别覆盖率</span><b>{{ percent(currentPoint.class_coverage) }}</b></article>
        <article><span>人员覆盖率</span><b>{{ percent(currentPoint.person_coverage) }}</b></article>
        <article><span>保留检测框</span><b>{{ currentPoint.retained_predictions || 0 }}</b></article>
      </div>
    </section>

    <section class="audit-main-grid">
      <ModelEvaluation />
      <div class="audit-side-stack">
        <LabelConfusionMatrix />
        <DetectionDensityMap />
      </div>
    </section>

    <section class="panel threshold-chart-panel">
      <div class="panel-header">
        <div><span class="section-kicker">全类别阈值审计</span><h4 class="panel-title">阈值变化如何影响全部模型输出</h4>
          <p class="visible-subtitle">折线衡量全类别保留与覆盖情况，柱形表示剩余检测框数量；红色工作线对应上方滑块。</p></div>
      </div>
      <div ref="curveRef" class="threshold-chart"></div>
    </section>
  </section>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import * as echarts from 'echarts'
import { useDashboardStore } from '../store/dashboard'
import { buildTooltip, chartPalette, splitLine } from '../utils/chartTheme'
import ModelEvaluation from '../components/auditing/ModelEvaluation.vue'
import LabelConfusionMatrix from '../components/auditing/LabelConfusionMatrix.vue'
import DetectionDensityMap from '../components/auditing/DetectionDensityMap.vue'
const store = useDashboardStore()
const curveRef = ref(null)
let chart
const audit = computed(() => store.modelAudit || {})
const thresholdTicks = [.25, .35, .45, .55, .65, .75]
const rows = computed(() => audit.value.threshold_curve || [])
const currentPoint = computed(() => rows.value.reduce((best, row) =>
  Math.abs(row.threshold - store.scoreThreshold) < Math.abs((best?.threshold ?? 99) - store.scoreThreshold) ? row : best, rows.value[0] || {}))
const percent = (value = 0) => `${Math.round(value * 100)}%`
const render = () => {
  if (!curveRef.value) return
  if (!chart) chart = echarts.init(curveRef.value)
  chart.setOption({
    color: [chartPalette.accent, chartPalette.green, chartPalette.gold, chartPalette.muted],
    tooltip: { ...buildTooltip(), trigger: 'axis' },
    legend: { top: 4, left: 6, itemWidth: 18, itemHeight: 8, textStyle: { color: chartPalette.muted, fontSize: 11 },
      data: ['检测保留率', '类别覆盖率', '人员覆盖率', '保留检测框'] },
    grid: { left: 56, right: 58, top: 58, bottom: 42 },
    xAxis: { type: 'category', name: '阈值', data: rows.value.map((row) => row.threshold.toFixed(2)),
      axisLabel: { color: chartPalette.muted }, axisLine: { lineStyle: { color: chartPalette.lineStrong } }, axisTick: { show: false } },
    yAxis: [
      { type: 'value', min: 0, max: 1, name: '全局比例', axisLabel: { color: chartPalette.muted, formatter: (value) => `${Math.round(value * 100)}%` }, splitLine },
      { type: 'value', min: 0, name: '检测框数量', axisLabel: { color: chartPalette.muted }, splitLine: { show: false } }
    ],
    series: [
      { name: '检测保留率', type: 'line', smooth: .25, symbolSize: 8, data: rows.value.map((row) => row.retention_rate) },
      { name: '类别覆盖率', type: 'line', smooth: .25, symbolSize: 8, data: rows.value.map((row) => row.class_coverage) },
      { name: '人员覆盖率', type: 'line', smooth: .25, symbolSize: 8, data: rows.value.map((row) => row.person_coverage),
        markLine: { symbol: 'none', label: { formatter: `工作点 ${store.scoreThreshold.toFixed(2)}`, color: chartPalette.red },
          lineStyle: { color: chartPalette.red, type: 'dashed', width: 2 }, data: [{ xAxis: currentPoint.value.threshold?.toFixed(2) }] } },
      { name: '保留检测框', type: 'bar', yAxisIndex: 1, barMaxWidth: 28, data: rows.value.map((row) => row.retained_predictions),
        itemStyle: { color: 'rgba(86,112,143,.18)', borderColor: chartPalette.muted, borderWidth: 1, borderRadius: [4,4,0,0] } }
    ]
  }, true)
}
watch(() => [rows.value, store.scoreThreshold], render, { deep: true })
onMounted(() => { render(); window.addEventListener('resize', render) })
onBeforeUnmount(() => { window.removeEventListener('resize', render); chart?.dispose() })
</script>

<style scoped>
.audit-page { gap: 24px; }.audit-status { position: relative; z-index: 1; min-width: 190px; padding: 16px; border: 1px solid var(--border); border-radius: 12px; background: rgba(255,255,255,.82); }
.audit-status span,.audit-status small { display:block; color:var(--subtle); font-size:.72rem; }.audit-status strong { display:block; margin:7px 0; font-size:1.25rem; }
.audit-command { display:grid; grid-template-columns: 190px minmax(280px,1fr) minmax(420px,1.2fr); align-items:center; gap:24px; }
.section-kicker { color:var(--subtle); font-size:.72rem; font-weight:800; }.threshold-copy strong { display:block; margin:5px 0; color:var(--accent); font-size:2.2rem; font-variant-numeric:tabular-nums; }
.threshold-copy p,.visible-subtitle { display:block!important; margin:0; color:var(--muted); font-size:.8rem; line-height:1.55; }.threshold-control input { width:100%; }
.threshold-ticks { display:flex; justify-content:space-between; margin-top:7px; color:var(--subtle); font-size:.68rem; font-variant-numeric:tabular-nums; }
.threshold-impact { display:grid; grid-template-columns:repeat(4,minmax(0,1fr)); gap:8px; }.threshold-impact article { padding:11px; border:1px solid var(--border); border-radius:8px; background:#f8fbff; }
.threshold-impact span,.threshold-impact b { display:block; }.threshold-impact span { color:var(--subtle); font-size:.7rem; }.threshold-impact b { margin-top:6px; font-size:1.06rem; font-variant-numeric:tabular-nums; }
.audit-main-grid { display:grid; grid-template-columns:minmax(520px,1.35fr) minmax(330px,.75fr); gap:18px; }.audit-side-stack { display:grid; gap:18px; }
.audit-main-grid > *, .audit-side-stack > * { padding:var(--panel-padding); border:1px solid var(--border); border-radius:var(--radius); background:#fff; box-shadow:var(--shadow); }
  .threshold-chart { min-height:380px; }
@media(max-width:1180px){.audit-command{grid-template-columns:1fr 1fr}.threshold-impact{grid-column:1/-1}.audit-main-grid{grid-template-columns:1fr}}
@media(max-width:700px){.audit-command{grid-template-columns:1fr}.threshold-impact{grid-template-columns:repeat(2,1fr)}}
</style>
