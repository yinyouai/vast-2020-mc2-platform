<template>
  <section class="panel ranking-chart-panel">
    <div class="panel-header">
      <div>
        <span class="section-kicker">综合评分构成</span>
        <h4 class="panel-title">候选暗号排名</h4>
        <p class="visible-subtitle">
          每段长度是该指标对综合分的实际贡献；全量图片先由模型分析，人工仅覆盖关键误报与漏检。
        </p>
      </div>
      <span class="data-chip live-chip">
        <i></i>数据已同步 · 原始阈值 {{ Number(scoring.score_threshold ?? store.scoreThreshold).toFixed(2) }}
      </span>
    </div>

    <div v-if="dataScope.image_count" class="data-scope">
      <span><b>{{ dataScope.person_count }}</b> 人</span>
      <span><b>{{ dataScope.image_count }}</b> 张全量图片</span>
      <span><b>{{ dataScope.raw_detection_count }}</b> 个原始检测框</span>
      <span><b>{{ dataScope.caption_count }}</b> 条 caption</span>
      <span><b>{{ dataScope.independent_text_count }}</b> 条独立文本</span>
    </div>

    <div ref="chartRef" class="ranking-chart" role="img" aria-label="候选暗号综合评分排名"></div>

    <div v-if="factorDefinitions.length" class="score-method">
      <div class="method-heading">
        <div>
          <span>评分公式</span>
          <strong>{{ scoreFormula }}</strong>
        </div>
        <p>{{ scoring.evidence_source }}；{{ scoring.text_source }}</p>
      </div>
      <div class="factor-grid">
        <article v-for="factor in factorDefinitions" :key="factor.key">
          <i :style="{ background: factor.color }"></i>
          <div>
            <strong>{{ factor.name }} · {{ factor.weight }}%</strong>
            <span>{{ factor.description }}</span>
          </div>
        </article>
      </div>
      <p class="penalty-note">
        拥有者人数不是目标人数时，四项贡献统一乘以
        {{ penaltyPercent }}% 惩罚系数。
      </p>
    </div>

    <div v-if="selectedCandidate" class="candidate-breakdown">
      <div class="breakdown-title">
        <div>
          <span>当前候选计算</span>
          <strong>{{ selectedCandidate.label }}</strong>
        </div>
        <b>综合分 {{ selectedCandidate.score.toFixed(4) }}</b>
      </div>
      <div class="breakdown-grid">
        <article v-for="factor in selectedFactors" :key="factor.key">
          <span>{{ factor.name }}</span>
          <strong>{{ factor.raw }}</strong>
          <small>
            归一化 {{ percent(factor.factor) }} × {{ factor.weight }}%
            <template v-if="factor.penalized"> × {{ penaltyPercent }}%</template>
          </small>
          <b>贡献 {{ factor.contribution.toFixed(4) }}</b>
        </article>
      </div>
    </div>
  </section>
</template>

<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import * as echarts from 'echarts'
import { useDashboardStore } from '../../store/dashboard'
import { buildTooltip, chartPalette, splitLine } from '../../utils/chartTheme'

const store = useDashboardStore()
const chartRef = ref(null)
let chart
let resizeObserver

const rows = computed(() => [...store.candidateRankings].reverse())
const scoring = computed(() => store.candidateScoring || {})
const dataScope = computed(() => scoring.value.data_scope || {})
const selectedCandidate = computed(() =>
  store.candidateRankings.find((item) => item.label === store.selectedCandidateLabel)
  || store.candidateRankings[0]
  || null
)

const factorColors = {
  specificity: 'var(--accent)',
  stability: chartPalette.green,
  visual: '#d99522',
  text: '#8d6ccf'
}
const targetGroupSize = computed(() => Number(scoring.value.target_group_size))
const penaltyPercent = computed(() =>
  Math.round(Number(scoring.value.non_target_penalty) * 100)
)
const factorDefinitions = computed(() =>
  (scoring.value.factors || []).map((item) => ({
    ...item,
    weight: Math.round(Number(item.weight) * 100),
    color: factorColors[item.key] || chartPalette.muted
  }))
)
const scoreFormula = computed(() =>
  factorDefinitions.value
    .map((item) => `${item.name}×${item.weight}%`)
    .join(' + ')
)

const component = (row, key) => Number(row.score_components?.[key] || 0)
const factor = (row, key) => Number(row.score_factors?.[key] || 0)
const percent = (value) => `${Math.round(Number(value || 0) * 100)}%`

const rawFactorValue = (row, key) => {
  if (key === 'specificity') return `${row.owner_count} 人 / 目标 ${targetGroupSize.value} 人`
  if (key === 'stability') return `${Math.round(row.stable_owner_ratio * row.owner_count)} / ${row.owner_count} 人稳定`
  if (key === 'visual') {
    return `${row.evidence_image_count} 张组内支持 / ${row.non_owner_raw_detection_image_count} 张组外命中（全量 ${row.evaluated_image_count} 张已分析）`
  }
  return `${row.text_support_count} / ${row.owner_count} 人，${row.text_evidence_count} 条直接文本`
}

const selectedFactors = computed(() => {
  if (!selectedCandidate.value) return []
  const row = selectedCandidate.value
  return factorDefinitions.value.map((definition) => ({
    ...definition,
    raw: rawFactorValue(row, definition.key),
    factor: factor(row, definition.key),
    contribution: component(row, definition.key),
    penalized: Number(row.score_components?.penalty ?? 1) < 1
  }))
})

const render = async () => {
  if (!chartRef.value) return
  await nextTick()
  if (!chart) chart = echarts.init(chartRef.value)
  const compact = chartRef.value.clientWidth < 520

  const makeSeries = (definition) => ({
    name: `${definition.name} ${definition.weight}%`,
    type: 'bar',
    stack: 'score',
    barMaxWidth: 22,
    data: rows.value.map((row) => ({
      value: component(row, definition.key),
      itemStyle: {
        color: definition.color,
        opacity: store.excludedItems.includes(row.label) ? .2 : 1,
        borderColor: row.label === store.selectedCandidateLabel ? '#17324d' : 'transparent',
        borderWidth: row.label === store.selectedCandidateLabel ? 1 : 0
      }
    }))
  })

  chart.setOption({
    tooltip: {
      ...buildTooltip((params) => {
        const list = Array.isArray(params) ? params : []
        const row = rows.value[params[0]?.dataIndex]
        if (!row) return ''
        const details = factorDefinitions.value.map((definition) =>
          `${definition.name}：${rawFactorValue(row, definition.key)} → 贡献 ${component(row, definition.key).toFixed(4)}`
        )
        return `<strong>${row.label}</strong><br/>综合分 ${row.score.toFixed(4)}<br/>${details.join('<br/>')}`
      }),
      trigger: 'axis'
    },
    legend: {
      top: 0,
      type: 'scroll',
      data: factorDefinitions.value.map((item) => `${item.name} ${item.weight}%`),
      textStyle: { color: chartPalette.muted, fontSize: compact ? 9 : 11 }
    },
    grid: {
      left: compact ? 104 : 116,
      right: compact ? 24 : 48,
      top: compact ? 58 : 42,
      bottom: 36
    },
    xAxis: {
      type: 'value',
      max: 1,
      name: '综合分',
      axisLabel: { color: chartPalette.muted },
      splitLine
    },
    yAxis: {
      type: 'category',
      data: rows.value.map((row) => row.label),
      axisLabel: {
        color: (value) => value === store.selectedCandidateLabel ? chartPalette.accent : chartPalette.muted,
        fontWeight: (value) => value === store.selectedCandidateLabel ? 800 : 500,
        fontSize: compact ? 9 : 10
      },
      axisTick: { show: false },
      axisLine: { show: false }
    },
    series: factorDefinitions.value.map(makeSeries)
  }, true)

  chart.off('click')
  chart.on('click', (params) => store.selectCandidate(params.name))
  chart.resize()
}

watch(
  () => [store.candidateRankings, store.selectedCandidateLabel, store.excludedItems, store.candidateScoring],
  render,
  { deep: true }
)

onMounted(() => {
  render()
  resizeObserver = new ResizeObserver(() => chart?.resize())
  resizeObserver.observe(chartRef.value)
})

onBeforeUnmount(() => {
  resizeObserver?.disconnect()
  chart?.dispose()
})
</script>

<style scoped>
.ranking-chart-panel {
  min-width: 0;
}

.panel-header {
  align-items: flex-start;
  flex-wrap: wrap;
}

.section-kicker {
  color: var(--subtle);
  font-size: .7rem;
  font-weight: 800;
}

.visible-subtitle {
  display: block !important;
  margin: 5px 0 0;
  color: var(--muted);
  font-size: .76rem;
  line-height: 1.55;
}

.live-chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.live-chip i {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--success);
  box-shadow: none;
}

.ranking-chart {
  width: 100%;
  min-height: 420px;
}

.data-scope {
  display: flex;
  flex-wrap: wrap;
  gap: 7px;
  margin: -4px 0 10px;
}

.data-scope span {
  padding: 5px 8px;
  border: none;
  border-radius: 12px;
  color: var(--muted);
  background: var(--surface-3);
  font-size: .62rem;
}

.data-scope b {
  color: var(--text);
  font-variant-numeric: tabular-nums;
}

.score-method,
.candidate-breakdown {
  margin-top: 14px;
  padding: 14px;
  border: none;
  border-radius: 12px;
  background: var(--surface-3);
}

.method-heading,
.breakdown-title {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 14px;
}

.method-heading span,
.breakdown-title span {
  display: block;
  color: var(--subtle);
  font-size: .65rem;
  font-weight: 800;
}

.method-heading strong,
.breakdown-title strong {
  display: block;
  margin-top: 4px;
  color: var(--text);
  font-size: .78rem;
  line-height: 1.5;
}

.method-heading p {
  max-width: 250px;
  margin: 0;
  color: var(--muted);
  font-size: .65rem;
  line-height: 1.5;
  text-align: right;
}

.factor-grid,
.breakdown-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 8px;
  margin-top: 12px;
}

.factor-grid article {
  display: flex;
  gap: 9px;
  min-width: 0;
  padding: 9px;
  border-radius: 12px;
  background: var(--surface);
}

.factor-grid i {
  flex: 0 0 auto;
  width: 8px;
  height: 28px;
  border-radius: 12px;
}

.factor-grid strong,
.factor-grid span {
  display: block;
}

.factor-grid strong {
  color: var(--text);
  font-size: .69rem;
}

.factor-grid span {
  margin-top: 3px;
  color: var(--muted);
  font-size: .62rem;
  line-height: 1.45;
}

.penalty-note {
  margin: 10px 0 0;
  color: var(--muted);
  font-size: .64rem;
  line-height: 1.5;
}

.breakdown-title > b {
  padding: 6px 9px;
  border-radius: 12px;
  color: var(--accent);
  background: var(--surface-glow);
  font-size: .7rem;
}

.breakdown-grid article {
  min-width: 0;
  padding: 9px;
  border: none;
  border-radius: 12px;
  background: var(--surface);
}

.breakdown-grid span,
.breakdown-grid strong,
.breakdown-grid small,
.breakdown-grid b {
  display: block;
}

.breakdown-grid span {
  color: var(--subtle);
  font-size: .62rem;
  font-weight: 800;
}

.breakdown-grid strong {
  margin-top: 5px;
  font-size: .74rem;
}

.breakdown-grid small {
  margin-top: 5px;
  color: var(--muted);
  font-size: .6rem;
  line-height: 1.4;
}

.breakdown-grid b {
  margin-top: 6px;
  color: var(--accent);
  font-size: .68rem;
  font-variant-numeric: tabular-nums;
}

@media (max-width: 620px) {
  .method-heading {
    display: block;
  }

  .method-heading p {
    max-width: none;
    margin-top: 7px;
    text-align: left;
  }

  .factor-grid,
  .breakdown-grid {
    grid-template-columns: 1fr;
  }
}
</style>
