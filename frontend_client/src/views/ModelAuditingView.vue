<template>
  <section class="view-grid-layout">
    <div class="page-intro">
      <div>
        <p class="eyebrow">Task 1 / Model Audit</p>
        <h3>先把机器误报从证据链里剥离出来</h3>
        <p>
          这一层用于观察目标检测模型在不同置信度阈值下的稳定性。阈值越低，背景物品越容易被错误归入风险标签；阈值提升后，误报曲线下降，后续人工复核会更干净。
        </p>
      </div>
      <button class="primary-btn" @click="$router.push('/task2_correction')">进入人工复核</button>
    </div>

    <div class="panel">
      <div class="panel-header">
        <div>
          <h4 class="panel-title">全局置信度阈值</h4>
          <p class="panel-subtitle">当前阈值 {{ store.scoreThreshold.toFixed(2) }}，影响后续矩阵和物证过滤。</p>
        </div>
        <span class="data-chip">FP 预计 {{ falsePositiveRate }}%</span>
      </div>
      <input
        class="apple-slider"
        type="range"
        min="0.05"
        max="0.9"
        step="0.05"
        :value="store.scoreThreshold"
        @input="store.setScoreThreshold(Number($event.target.value))"
        aria-label="全局置信度阈值"
      />
    </div>

    <div class="metric-grid">
      <div v-for="metric in metrics" :key="metric.label" class="metric-card">
        <span>{{ metric.label }}</span>
        <strong>{{ metric.value }}%</strong>
      </div>
    </div>

    <div class="split-grid">
      <div class="panel">
        <div class="panel-header">
          <div>
            <h4 class="panel-title">模型质量雷达</h4>
            <p class="panel-subtitle">准确率、精确率、召回率和 F1 的综合视图。</p>
          </div>
        </div>
        <div ref="radarRef" class="chart-frame"></div>
      </div>

      <div class="panel">
        <div class="panel-header">
          <div>
            <h4 class="panel-title">误报消融曲线</h4>
            <p class="panel-subtitle">低置信噪声随阈值提升快速收敛。</p>
          </div>
        </div>
        <div ref="lineRef" class="chart-frame"></div>
      </div>
    </div>

    <div class="panel audit-note">
      <h4>审计结论</h4>
      <p>
        当前阈值下，模型仍可能把会场常见物品误判为高风险物证。建议在第 2 层优先复核 Person3 与 Person27 的图文冲突样本，再进入群体共现聚类。
      </p>
    </div>
  </section>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import * as echarts from 'echarts'
import { useDashboardStore } from '../store/dashboard'

const store = useDashboardStore()
const radarRef = ref(null)
const lineRef = ref(null)
let radarChart
let lineChart

const metrics = computed(() => {
  const t = store.scoreThreshold
  return [
    { label: 'Accuracy', value: Math.round(64 + t * 24) },
    { label: 'Precision', value: Math.round(58 + t * 31) },
    { label: 'Recall', value: Math.round(71 + t * 13) },
    { label: 'F1 Score', value: Math.round(62 + t * 25) }
  ]
})

const falsePositiveRate = computed(() => Math.max(7, Math.round(48 - store.scoreThreshold * 42)))

const axisColor = '#70878b'
const gridColor = 'rgba(184, 211, 214, 0.12)'

const renderCharts = () => {
  if (!radarRef.value || !lineRef.value) return
  if (!radarChart) radarChart = echarts.init(radarRef.value)
  if (!lineChart) lineChart = echarts.init(lineRef.value)

  radarChart.setOption({
    backgroundColor: 'transparent',
    tooltip: {},
    radar: {
      radius: '68%',
      indicator: metrics.value.map((item) => ({ name: item.label, max: 100 })),
      axisName: { color: axisColor },
      splitLine: { lineStyle: { color: gridColor } },
      splitArea: { areaStyle: { color: ['rgba(66,214,194,0.03)', 'rgba(255,255,255,0.015)'] } },
      axisLine: { lineStyle: { color: gridColor } }
    },
    series: [{
      type: 'radar',
      data: [{
        value: metrics.value.map((item) => item.value),
        name: '当前阈值',
        symbolSize: 5,
        itemStyle: { color: '#42d6c2' },
        lineStyle: { width: 2 },
        areaStyle: { color: 'rgba(66,214,194,0.16)' }
      }]
    }]
  })

  const thresholds = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
  lineChart.setOption({
    backgroundColor: 'transparent',
    tooltip: { trigger: 'axis' },
    grid: { left: 46, right: 18, top: 28, bottom: 38 },
    xAxis: {
      type: 'category',
      data: thresholds.map((v) => v.toFixed(1)),
      axisLabel: { color: axisColor },
      axisLine: { lineStyle: { color: gridColor } }
    },
    yAxis: {
      type: 'value',
      axisLabel: { color: axisColor, formatter: '{value}%' },
      splitLine: { lineStyle: { color: gridColor } }
    },
    series: [{
      name: 'False Positive Rate',
      type: 'line',
      smooth: true,
      showSymbol: false,
      data: thresholds.map((v) => Math.max(6, 50 - v * 43)),
      lineStyle: { width: 3, color: '#ff6b6b' },
      areaStyle: { color: 'rgba(255,107,107,0.12)' },
      markLine: {
        symbol: 'none',
        label: { color: '#f4c95d', formatter: '当前' },
        lineStyle: { color: '#f4c95d', type: 'dashed' },
        data: [{ xAxis: store.scoreThreshold.toFixed(1) }]
      }
    }]
  })
}

const resizeCharts = () => {
  radarChart?.resize()
  lineChart?.resize()
}

watch(() => store.scoreThreshold, renderCharts)

onMounted(() => {
  renderCharts()
  window.addEventListener('resize', resizeCharts)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', resizeCharts)
  radarChart?.dispose()
  lineChart?.dispose()
})
</script>

<style scoped>
.audit-note h4 {
  margin-bottom: 8px;
}

.audit-note p {
  max-width: 900px;
  margin-bottom: 0;
  color: var(--muted);
  line-height: 1.65;
}
</style>
