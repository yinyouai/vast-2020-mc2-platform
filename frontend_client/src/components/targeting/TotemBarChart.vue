<template>
  <div class="panel">
    <div class="panel-header">
      <div>
        <h4 class="panel-title">物品覆盖率分布</h4>
        <p class="panel-subtitle">覆盖率越高，作为关键物证的判别力通常越弱。</p>
      </div>
    </div>
    <div ref="barRef" class="chart-frame small-chart"></div>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import * as echarts from 'echarts'
import { useDashboardStore } from '../../store/dashboard'
import { animationTiming, buildAxis, buildTooltip, chartPalette, splitLine } from '../../utils/chartTheme'

const store = useDashboardStore()
const barRef = ref(null)
let chart

const items = ['Notebook', 'Badge', 'Toy', 'Red Hat', 'Yellow Bag']
const values = [60, 48, 44, 41, 20]

const averageCoverage = computed(() => Math.round(values.reduce((sum, value) => sum + value, 0) / values.length))

const render = () => {
  if (!barRef.value) return
  if (!chart) chart = echarts.init(barRef.value)
  chart.setOption({
    backgroundColor: 'transparent',
    tooltip: buildTooltip((params) => {
      const excluded = store.excludedItems.includes(params.name)
      return `
        <strong>${params.name}</strong><br/>
        覆盖率：${params.value}%<br/>
        当前状态：${excluded ? '已从背景基线中剔除' : '仍作为背景噪声保留'}
      `
    }),
    grid: { left: 54, right: 24, top: 24, bottom: 46 },
    xAxis: {
      type: 'category',
      data: items,
      ...buildAxis()
    },
    yAxis: {
      type: 'value',
      axisLabel: { color: chartPalette.muted, formatter: '{value}%' },
      splitLine
    },
    series: [{
      type: 'bar',
      barWidth: 32,
      data: values.map((value, index) => {
        const name = items[index]
        const excluded = store.excludedItems.includes(name)
        const gradientStops = name === 'Yellow Bag'
          ? ['#f6cd75', '#f0b44c']
          : excluded
            ? ['#9fb1c4', '#c5d0dd']
            : ['#6da3ff', '#58c9b2']
        return {
          value,
          itemStyle: {
            borderRadius: [10, 10, 4, 4],
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: gradientStops[0] },
              { offset: 1, color: gradientStops[1] }
            ]),
            opacity: excluded ? 0.58 : 1
          }
        }
      }),
      label: {
        show: true,
        position: 'top',
        color: chartPalette.text,
        formatter: '{c}%'
      },
      markLine: {
        symbol: 'none',
        label: {
          color: chartPalette.gold,
          formatter: `平均 ${averageCoverage.value}%`
        },
        lineStyle: {
          color: chartPalette.gold,
          type: 'dashed'
        },
        data: [{ yAxis: averageCoverage.value }]
      },
      animationDuration: animationTiming.duration,
      animationEasing: animationTiming.easing,
      animationDelay: animationTiming.delay
    }]
  })
}

const resize = () => chart?.resize()

watch(() => store.excludedItems, render, { deep: true })
onMounted(() => {
  render()
  window.addEventListener('resize', resize)
})
onBeforeUnmount(() => {
  window.removeEventListener('resize', resize)
  chart?.dispose()
})
</script>

<style scoped>
.small-chart {
  min-height: 260px;
}
</style>
