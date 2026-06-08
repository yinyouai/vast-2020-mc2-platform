<template>
  <section class="panel exclusion-panel">
    <div class="panel-header">
      <div class="header-copy">
        <span class="section-kicker">反向验证</span>
        <h4 class="panel-title">非成员模型误检</h4>
        <p class="visible-subtitle">
          这些人员曾被模型预测为 {{ store.activeTotem || '候选物品' }}，但人工校正未确认。
        </p>
      </div>
      <span class="result-count">{{ rows.length }} 人未确认</span>
    </div>

    <div class="chart-note">
      <span class="threshold-key"></span>
      虚线为当前置信度阈值 {{ store.scoreThreshold.toFixed(2) }}
    </div>
    <div
      ref="chartRef"
      class="exclusion-chart"
      :style="{ height: `${chartHeight}px` }"
      role="img"
      :aria-label="`非成员模型误检分布，共 ${rows.length} 人，当前阈值 ${store.scoreThreshold.toFixed(2)}`"
    ></div>
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

const rows = computed(() => [...(store.analysisSummary?.final?.excluded_nonmembers || [])].reverse())
const chartHeight = computed(() => Math.max(340, rows.value.length * 42 + 84))

const render = async () => {
  if (!chartRef.value) return
  await nextTick()
  if (!chart) chart = echarts.init(chartRef.value)

  const compact = chartRef.value.clientWidth < 520
  chart.setOption({
    animationDuration: 280,
    tooltip: buildTooltip(({ data, item }) =>
      `<strong>${item?.person_id || data.person_id}</strong><br/>最高分 ${Number(data.value).toFixed(3)}<br/>图片 ${data.image_id}<br/>人工校正未确认`
    ),
    grid: {
      left: compact ? 76 : 94,
      right: compact ? 42 : 58,
      top: 18,
      bottom: 52,
      containLabel: false
    },
    xAxis: {
      type: 'value',
      min: 0,
      max: 1,
      interval: 0.2,
      name: '模型最高置信度',
      nameLocation: 'middle',
      nameGap: 34,
      nameTextStyle: { color: chartPalette.muted, fontSize: 11, fontWeight: 700 },
      axisLabel: {
        color: chartPalette.muted,
        fontSize: 10,
        formatter: (value) => Number(value).toFixed(1)
      },
      axisLine: { show: false },
      axisTick: { show: false },
      splitLine
    },
    yAxis: {
      type: 'category',
      data: rows.value.map((item) => item.person_id),
      axisLabel: {
        color: chartPalette.muted,
        fontSize: compact ? 9 : 10,
        margin: 10,
        width: compact ? 58 : 72,
        overflow: 'truncate'
      },
      axisLine: { show: false },
      axisTick: { show: false }
    },
    series: [{
      type: 'bar',
      barWidth: compact ? 17 : 19,
      data: rows.value.map((item) => ({
        value: item.max_score,
        person_id: item.person_id,
        image_id: item.image_id,
        itemStyle: {
          color: 'var(--danger)',
          borderRadius: [0, 5, 5, 0]
        }
      })),
      label: {
        show: true,
        position: 'right',
        distance: 7,
        formatter: (params) => Number(params.value).toFixed(3),
        color: chartPalette.text,
        fontSize: compact ? 9 : 10,
        fontWeight: 700
      },
      markLine: {
        silent: true,
        symbol: 'none',
        label: {
          show: false
        },
        lineStyle: {
          color: chartPalette.accent,
          width: 2,
          type: 'dashed'
        },
        data: [{ xAxis: store.scoreThreshold }]
      }
    }]
  }, true)
  chart.resize()
}

watch(
  () => [rows.value, store.scoreThreshold, store.activeTotem],
  render,
  { deep: true }
)

onMounted(() => {
  render()
  resizeObserver = new ResizeObserver(() => {
    chart?.resize()
    render()
  })
  resizeObserver.observe(chartRef.value)
})

onBeforeUnmount(() => {
  resizeObserver?.disconnect()
  chart?.dispose()
})
</script>

<style scoped>
.exclusion-panel {
  min-width: 0;
}

.panel-header {
  align-items: flex-start;
  flex-wrap: wrap;
  margin-bottom: 12px;
}

.header-copy {
  min-width: 240px;
  flex: 1;
}

.section-kicker {
  display: block;
  margin-bottom: 4px;
  color: var(--subtle);
  font-size: .7rem;
  font-weight: 800;
}

.panel-title {
  line-height: 1.35;
}

.visible-subtitle {
  display: block !important;
  max-width: 620px;
  margin: 6px 0 0;
  color: var(--muted);
  font-size: .76rem;
  line-height: 1.6;
}

.result-count {
  flex: 0 0 auto;
  padding: 6px 10px;
  border: none;
  border-radius: 12px;
  color: #a64141;
  background: rgba(207, 86, 86, .08);
  font-size: .68rem;
  font-weight: 800;
}

.chart-note {
  display: flex;
  align-items: center;
  gap: 7px;
  min-height: 28px;
  padding: 5px 9px;
  border-radius: 12px;
  color: var(--muted);
  background: var(--surface-3);
  font-size: .68rem;
  font-weight: 700;
}

.threshold-key {
  width: 20px;
  border-top: 2px dashed var(--accent);
}

.exclusion-chart {
  width: 100%;
  min-height: 340px;
}

@media (max-width: 560px) {
  .header-copy {
    min-width: 100%;
  }

  .result-count {
    margin-top: 2px;
  }

  .exclusion-chart {
    margin-top: 2px;
  }
}
</style>
