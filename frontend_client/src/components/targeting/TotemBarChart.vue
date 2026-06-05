<template>
  <div class="panel">
    <div class="panel-header">
      <div>
        <h4 class="panel-title">物品覆盖率分布</h4>
        <p class="panel-subtitle">已剔除物品会淡化，候选暗号保持高亮。</p>
      </div>
    </div>
    <div ref="barRef" class="chart-frame small-chart"></div>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import * as echarts from 'echarts'
import { animationTiming, buildAxis, buildTooltip, chartPalette, splitLine } from '../../utils/chartTheme'

const props = defineProps({
  items: {
    type: Array,
    default: () => []
  }
})

const barRef = ref(null)
let chart

const averageCoverage = computed(() => {
  if (!props.items.length) return 0
  return Math.round(props.items.reduce((sum, item) => sum + item.coverage, 0) / props.items.length)
})

const render = () => {
  if (!barRef.value) return
  if (!chart) chart = echarts.init(barRef.value)

  chart.setOption({
    backgroundColor: 'transparent',
    tooltip: buildTooltip((params) => {
      const target = props.items.find((item) => item.name === params.name)
      return `
        <strong>${params.name}</strong><br/>
        覆盖率：${params.value}%<br/>
        状态：${target?.excluded ? '已剔除' : target?.role || '保留'}
      `
    }),
    grid: { left: 54, right: 24, top: 24, bottom: 46 },
    xAxis: {
      type: 'category',
      data: props.items.map((item) => item.name),
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
      data: props.items.map((item) => {
        const gradientStops = item.role === '候选暗号'
          ? ['#f6cd75', '#f0b44c']
          : item.excluded
            ? ['#9fb1c4', '#c5d0dd']
            : ['#6da3ff', '#58c9b2']

        return {
          value: item.coverage,
          itemStyle: {
            borderRadius: [10, 10, 4, 4],
            color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
              { offset: 0, color: gradientStops[0] },
              { offset: 1, color: gradientStops[1] }
            ]),
            opacity: item.excluded ? 0.48 : 1
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
        lineStyle: { color: chartPalette.gold, type: 'dashed' },
        data: [{ yAxis: averageCoverage.value }]
      },
      animationDuration: animationTiming.duration,
      animationEasing: animationTiming.easing,
      animationDelay: animationTiming.delay
    }]
  })
}

const resize = () => chart?.resize()

watch(() => props.items, render, { deep: true })
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
