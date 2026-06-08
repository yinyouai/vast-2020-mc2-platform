<template>
  <div class="component-wrapper coverage-card">
    <div class="coverage-head">
      <div><span class="component-kicker">类别可见性</span><h4>训练类别覆盖</h4></div>
      <strong>{{ coveragePercent }}%</strong>
    </div>
    <div class="coverage-visual">
      <div ref="chartRef" class="coverage-ring" aria-label="训练类别覆盖环形图"></div>
      <div class="coverage-facts">
        <article><b>{{ audit.detected_class_count || 0 }}</b><span>已输出类别</span></article>
        <article><b>{{ audit.missing_class_count || 0 }}</b><span>完全缺失</span></article>
        <article><b>{{ audit.training_class_count || 0 }}</b><span>训练类别</span></article>
      </div>
    </div>
    <div class="class-map" aria-label="训练类别状态图">
      <button v-for="item in classStates" :key="item.label"
        :class="['class-cell', item.detected ? 'is-detected' : 'is-missing']"
        :title="`${item.label}：${item.detected ? '模型有输出' : '模型未输出'}`"
        :aria-label="`${item.label} ${item.detected ? '已输出' : '缺失'}`"></button>
    </div>
    <div class="coverage-legend">
      <span><i class="detected"></i>模型有输出</span>
      <span><i class="missing"></i>训练存在但未输出</span>
    </div>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import * as echarts from 'echarts'
import { useDashboardStore } from '../../store/dashboard'
import { chartPalette } from '../../utils/chartTheme'

const store = useDashboardStore()
const chartRef = ref(null)
let chart
const audit = computed(() => store.modelAudit || {})
const classStates = computed(() => [
  ...Object.keys(store.modelEvaluationData || {}).map((label) => ({ label, detected: true })),
  ...(audit.value.missing_classes || []).map((label) => ({ label, detected: false }))
].sort((a, b) => a.label.localeCompare(b.label)))
const coveragePercent = computed(() => {
  const total = audit.value.training_class_count || 0
  return total ? Math.round((audit.value.detected_class_count / total) * 100) : 0
})
const render = () => {
  if (!chartRef.value) return
  if (!chart) chart = echarts.init(chartRef.value)
  chart.setOption({
    series: [{ type: 'pie', radius: ['68%', '88%'], silent: true, label: { show: false }, data: [
      { value: audit.value.detected_class_count || 0, itemStyle: { color: chartPalette.accent } },
      { value: audit.value.missing_class_count || 0, itemStyle: { color: '#e4eaf1' } }
    ] }],
    graphic: [
      { type: 'text', left: 'center', top: '36%', style: { text: `${coveragePercent.value}%`, fill: chartPalette.text, font: '700 25px Segoe UI' } },
      { type: 'text', left: 'center', top: '56%', style: { text: '覆盖率', fill: chartPalette.muted, font: '12px Microsoft YaHei UI' } }
    ]
  })
}
watch(() => [audit.value.detected_class_count, audit.value.missing_class_count], render)
onMounted(() => { render(); window.addEventListener('resize', render) })
onBeforeUnmount(() => { window.removeEventListener('resize', render); chart?.dispose() })
</script>

<style scoped>
.coverage-card { min-height: 300px; }
.coverage-head { display: flex; align-items: flex-start; justify-content: space-between; gap: 16px; }
.coverage-head h4 { margin: 4px 0 0; font-size: 1rem; }.coverage-head > strong { color: var(--accent); font-size: 1.65rem; font-variant-numeric: tabular-nums; }
.component-kicker { color: var(--subtle); font-size: .72rem; font-weight: 800; }
.coverage-visual { display: grid; grid-template-columns: 148px 1fr; align-items: center; gap: 16px; margin: 12px 0; }
.coverage-ring { width: 148px; height: 148px; }.coverage-facts { display: grid; gap: 7px; }
.coverage-facts article { display: flex; align-items: baseline; justify-content: space-between; padding: 8px 10px; border-bottom: 1px solid var(--border); }
.coverage-facts b { font-size: 1.08rem; font-variant-numeric: tabular-nums; }.coverage-facts span { color: var(--muted); font-size: .78rem; }
.class-map { display: grid; grid-template-columns: repeat(11, minmax(0,1fr)); gap: 5px; }
.class-cell { min-height: 14px; height: 14px; padding: 0; border-radius: 12px; cursor: help; }
.class-cell.is-detected { background: var(--accent); }.class-cell.is-missing { background: #dfe6ee; border: none; }
.coverage-legend { display: flex; flex-wrap: wrap; gap: 14px; margin-top: 10px; color: var(--muted); font-size: .72rem; }
.coverage-legend span { display: inline-flex; align-items: center; gap: 6px; }.coverage-legend i { width: 9px; height: 9px; border-radius: 12px; }
.coverage-legend .detected { background: var(--accent); }.coverage-legend .missing { background: #dfe6ee; border: none; }
</style>
