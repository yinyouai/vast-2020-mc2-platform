<template>
  <div class="chart-container">
    <div class="component-head">
      <div><span>原始模型层</span><h4>高频类别置信度分布</h4></div>
      <b>阈值 {{ store.scoreThreshold.toFixed(2) }}</b>
    </div>
    <div ref="chartRef" class="box-viewport"></div>
  </div>
</template>

<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import * as echarts from 'echarts'
import { useDashboardStore } from '../../store/dashboard'
import { buildTooltip, chartPalette, splitLine } from '../../utils/chartTheme'
const store = useDashboardStore()
const chartRef = ref(null)
let chart
const rows = computed(() => Object.entries(store.modelEvaluationData || {}).map(([label, stats]) => ({ label, ...stats }))
  .sort((a, b) => b.count - a.count).slice(0, 12).reverse())
const render = () => {
  if (!chartRef.value) return
  if (!chart) chart = echarts.init(chartRef.value)
  chart.setOption({
    tooltip: buildTooltip((params) => {
      const row = rows.value[params.dataIndex]
      return `<strong>${row.label}</strong><br/>样本 ${row.count}<br/>Min ${row.min.toFixed(3)} / Median ${row.median.toFixed(3)} / Max ${row.max.toFixed(3)}`
    }),
    grid: { left: 118, right: 22, top: 16, bottom: 38 },
    xAxis: { type: 'value', min: 0, max: 1, name: '置信度', axisLabel: { color: chartPalette.muted, formatter: (value) => value.toFixed(1) }, splitLine },
    yAxis: { type: 'category', data: rows.value.map((row) => row.label), axisLabel: { color: chartPalette.muted, width: 104, overflow: 'truncate', fontSize: 11 }, axisLine: { show: false }, axisTick: { show: false } },
    series: [{ type: 'boxplot', data: rows.value.map((row) => [row.min, row.q1, row.median, row.q3, row.max]),
      itemStyle: { color: 'rgba(47,125,246,.12)', borderColor: chartPalette.accent, borderWidth: 1.5 }, boxWidth: [8, 18],
      markLine: { symbol: 'none', label: { formatter: `当前 ${store.scoreThreshold.toFixed(2)}`, color: chartPalette.red, position: 'insideEndTop' },
        lineStyle: { color: chartPalette.red, width: 2, type: 'dashed' }, data: [{ xAxis: store.scoreThreshold }] }
    }]
  }, true)
}
watch(() => [store.modelEvaluationData, store.scoreThreshold], () => nextTick(render), { deep: true })
onMounted(() => { render(); window.addEventListener('resize', render) })
onBeforeUnmount(() => { window.removeEventListener('resize', render); chart?.dispose() })
</script>

<style scoped>
.chart-container { display: flex; min-height: 620px; flex-direction: column; }
.component-head { display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; }
.component-head span { color: var(--subtle); font-size: .72rem; font-weight: 800; }.component-head h4 { margin: 5px 0 0; font-size: 1rem; }
.component-head b { color: var(--accent); font-size: .82rem; font-variant-numeric: tabular-nums; }.box-viewport { min-height: 540px; flex: 1; margin-top: 10px; }
</style>
