<template>
  <div class="component-wrapper">
    <div class="density-head">
      <div><span>空间偏差</span><h4>检测框中心分布</h4></div>
      <b>{{ visibleCount }} / {{ allCount }}</b>
    </div>
    <p class="component-note">仅显示 score ≥ {{ store.scoreThreshold.toFixed(2) }}；圆点大小映射置信度。</p>
    <div ref="chartRef" class="density-viewport"></div>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import * as echarts from 'echarts'
import { useDashboardStore } from '../../store/dashboard'
import { buildTooltip, chartPalette } from '../../utils/chartTheme'
const store = useDashboardStore()
const chartRef = ref(null)
let chart
const allCount = computed(() => (store.modelAudit.density_points || []).length)
const visibleCount = computed(() => (store.modelAudit.density_points || []).filter((item) => item.score >= store.scoreThreshold).length)
const render = () => {
  if (!chartRef.value) return
  if (!chart) chart = echarts.init(chartRef.value)
  const points = (store.modelAudit.density_points || []).filter((item) => item.score >= store.scoreThreshold).map((item) => ({
    value: [item.x, item.y, item.score], name: `${item.person_id} / ${item.image_id}`, label: item.label
  }))
  chart.setOption({
    tooltip: buildTooltip(({ data }) => `<strong>${data.name}</strong><br/>类别：${data.label}<br/>置信度：${data.value[2].toFixed(3)}`),
    grid: { left: 42, right: 16, top: 12, bottom: 34 },
    xAxis: { type: 'value', name: 'x', axisLabel: { color: chartPalette.muted, fontSize: 10 }, splitLine: { lineStyle: { color: chartPalette.line } } },
    yAxis: { type: 'value', name: 'y', inverse: true, axisLabel: { color: chartPalette.muted, fontSize: 10 }, splitLine: { lineStyle: { color: chartPalette.line } } },
    series: [{ type: 'scatter', data: points, symbolSize: (value) => 4 + value[2] * 12,
      itemStyle: { color: (params) => params.data.value[2] >= 0.55 ? chartPalette.red : chartPalette.accent, opacity: .52 }
    }]
  }, true)
}
watch(() => [store.modelAudit.density_points, store.scoreThreshold], render, { deep: true })
onMounted(() => { render(); window.addEventListener('resize', render) })
onBeforeUnmount(() => { window.removeEventListener('resize', render); chart?.dispose() })
</script>

<style scoped>
.component-wrapper { display: flex; flex-direction: column; min-height: 300px; }
.density-head { display: flex; align-items: flex-start; justify-content: space-between; gap: 12px; }
.density-head span { color: var(--subtle); font-size: .72rem; font-weight: 800; }.density-head h4 { margin: 5px 0 0; font-size: 1rem; }
.density-head b { color: var(--accent); font-size: .86rem; font-variant-numeric: tabular-nums; }
.component-note { margin: 8px 0 10px; color: var(--muted); font-size: .78rem; }.density-viewport { width: 100%; min-height: 230px; flex: 1; }
</style>
