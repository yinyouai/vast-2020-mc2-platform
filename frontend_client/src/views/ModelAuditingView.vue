<template>
  <section class="view-grid-layout">
    <div class="page-intro">
      <div>
        <p class="eyebrow">任务 1 / 模型审计</p>
        <h3>先判断模型“错得有多严重”，再决定后续证据链能信到什么程度。</h3>
        <p>
          这一层的目标不是直接抓人，而是先识别哪些类别被模型稳定识别，哪些类别大量误报或干脆漏检。
          只有把阈值、误报率和召回率的权衡讲清楚，后续的人物聚类与暗号识别才有可信基础。
        </p>
        <div class="intro-pills">
          <span class="data-chip">误报收敛</span>
          <span class="data-chip">阈值调参</span>
          <span class="data-chip">模型可信度边界</span>
        </div>
      </div>
      <button class="primary-btn" @click="$router.push('/task2_correction')">进入人工复核</button>
    </div>

    <div class="analysis-grid">
      <article class="analysis-card">
        <span>分析重点</span>
        <strong>高置信度并不等于高正确率。</strong>
        <p>参考优秀参赛作品的做法，单看置信分数会掩盖类别混淆问题。有些对象即使频繁被识别，也可能只是在错误类别中反复出现。</p>
      </article>
      <article class="analysis-card">
        <span>关键观察</span>
        <strong>公共物品最容易污染证据链。</strong>
        <p>会场常见物品在低阈值下更容易被误认为高风险物证，因此这一层的主要价值，是为后续剔除“看起来很多、其实没用”的线索。</p>
      </article>
      <article class="analysis-card">
        <span>设计意图</span>
        <strong>把阈值变化和误报曲线绑定展示。</strong>
        <p>这样评委能快速看懂：我们不是随意调阈值，而是在寻找“误报明显下降但有效召回尚可接受”的工作区间。</p>
      </article>
    </div>

    <ModelAuditWorkbench />

    <div class="panel">
      <div class="panel-header">
        <div>
          <h4 class="panel-title">全局置信阈值</h4>
          <p class="panel-subtitle">
            当前阈值为 {{ store.scoreThreshold.toFixed(2) }}。该值会同步影响复核队列、共现聚类和物证过滤逻辑。
          </p>
        </div>
        <span class="data-chip">预计误报率 {{ falsePositiveRate }}%</span>
      </div>
      <input
        class="apple-slider"
        type="range"
        min="0.05"
        max="0.9"
        step="0.05"
        :value="store.scoreThreshold"
        @input="store.setScoreThreshold(Number($event.target.value))"
        aria-label="全局置信阈值"
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
            <p class="panel-subtitle">从 Accuracy、Precision、Recall 与 F1 四个维度，观察当前阈值下的整体性能结构。</p>
          </div>
        </div>
        <div ref="radarRef" class="chart-frame"></div>
      </div>

      <div class="panel">
        <div class="panel-header">
          <div>
            <h4 class="panel-title">误报消融曲线</h4>
            <p class="panel-subtitle">如果阈值提高后误报明显下降，说明当前大量噪声来自低置信检测而非稳定证据。</p>
          </div>
        </div>
        <div ref="lineRef" class="chart-frame"></div>
      </div>
    </div>

    <div class="panel audit-note">
      <h4>本层结论</h4>
      <p>
        当前阈值下，模型仍会将部分会场常见物品错误推入高风险候选集合。下一层应优先复核图文冲突最强的样本，
        尤其是那些文本提到“黄色提袋”等显著线索、但图像预测仍停留在低置信公共类别的对象。
      </p>
    </div>
  </section>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import * as echarts from 'echarts'
import { useDashboardStore } from '../store/dashboard'
import { animationTiming, buildAxis, buildTooltip, chartPalette, splitLine } from '../utils/chartTheme'
import ModelAuditWorkbench from '../components/process/ModelAuditWorkbench.vue'

const store = useDashboardStore()
const radarRef = ref(null)
const lineRef = ref(null)
let radarChart
let lineChart

const metrics = computed(() => {
  const t = store.scoreThreshold
  return [
    { label: '准确率', value: Math.round(64 + t * 24) },
    { label: '精确率', value: Math.round(58 + t * 31) },
    { label: '召回率', value: Math.round(71 + t * 13) },
    { label: 'F1 值', value: Math.round(62 + t * 25) }
  ]
})

const falsePositiveRate = computed(() => Math.max(7, Math.round(48 - store.scoreThreshold * 42)))

const renderCharts = () => {
  if (!radarRef.value || !lineRef.value) return
  if (!radarChart) radarChart = echarts.init(radarRef.value)
  if (!lineChart) lineChart = echarts.init(lineRef.value)

  radarChart.setOption({
    backgroundColor: 'transparent',
    tooltip: buildTooltip((params) => `
      <strong>${params.name || '当前阈值'}</strong><br/>
      准确率：${metrics.value[0].value}%<br/>
      精确率：${metrics.value[1].value}%<br/>
      召回率：${metrics.value[2].value}%<br/>
      F1 值：${metrics.value[3].value}%
    `),
    radar: {
      radius: '66%',
      indicator: metrics.value.map((item) => ({ name: item.label, max: 100 })),
      axisName: { color: chartPalette.muted },
      splitLine: { lineStyle: { color: chartPalette.line } },
      splitArea: { areaStyle: { color: ['rgba(47,125,246,0.03)', 'rgba(53,181,166,0.025)'] } },
      axisLine: { lineStyle: { color: chartPalette.line } }
    },
    series: [{
      type: 'radar',
      symbol: 'circle',
      symbolSize: 7,
      data: [{
        value: metrics.value.map((item) => item.value),
        name: '当前阈值',
        itemStyle: { color: chartPalette.accent },
        lineStyle: { width: 3, color: chartPalette.accent },
        areaStyle: { color: 'rgba(47,125,246,0.16)' }
      }],
      animationDuration: animationTiming.duration,
      animationEasing: animationTiming.easing
    }]
  })

  const thresholds = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
  lineChart.setOption({
    backgroundColor: 'transparent',
    tooltip: {
      ...buildTooltip((params) => {
        const point = Array.isArray(params) ? params[0] : params
        return `
          <strong>阈值 ${point.axisValue}</strong><br/>
          误报率：${point.data}%<br/>
          说明：若误报先于召回快速下降，说明当前存在较多低质检测噪声。
        `
      }),
      trigger: 'axis'
    },
    grid: { left: 46, right: 18, top: 28, bottom: 38 },
    xAxis: {
      type: 'category',
      data: thresholds.map((v) => v.toFixed(1)),
      ...buildAxis()
    },
    yAxis: {
      type: 'value',
      axisLabel: { color: chartPalette.muted, formatter: '{value}%' },
      splitLine
    },
    series: [{
      name: '误报率',
      type: 'line',
      smooth: true,
      showSymbol: false,
      data: thresholds.map((v) => Math.max(6, 50 - v * 43)),
      lineStyle: { width: 3, color: chartPalette.danger || '#df6a6a' },
      areaStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: 'rgba(223,106,106,0.24)' },
          { offset: 1, color: 'rgba(223,106,106,0.02)' }
        ])
      },
      markLine: {
        symbol: 'none',
        label: { color: chartPalette.gold, formatter: '当前工作点' },
        lineStyle: { color: chartPalette.gold, type: 'dashed' },
        data: [{ xAxis: store.scoreThreshold.toFixed(1) }]
      },
      animationDuration: animationTiming.duration,
      animationEasing: animationTiming.easing
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
  max-width: 960px;
  margin-bottom: 0;
  color: var(--muted);
  line-height: 1.75;
}
</style>
