<template>
  <div class="panel">
    <div class="panel-header">
      <div>
        <h4 class="panel-title">社交互动隔离矩阵</h4>
        <p class="panel-subtitle">核心群体在线上呈现出异常低互动状态，这符合刻意规避公开联系的行为模式。</p>
      </div>
      <span class="data-chip">40 x 40 提及关系</span>
    </div>
    <div ref="matrixRef" class="chart-frame matrix-frame"></div>
  </div>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'
import * as echarts from 'echarts'
import { useDashboardStore } from '../../store/dashboard'
import { animationTiming, buildAxis, buildTooltip, chartPalette } from '../../utils/chartTheme'

const store = useDashboardStore()
const matrixRef = ref(null)
let chart

const people = Array.from({ length: 40 }, (_, i) => `P${i + 1}`)
const coreNumbers = new Set(store.hackerGroup.filter((id) => id !== 'Person27').map((id) => Number(id.replace('Person', ''))))

const data = []
for (let y = 0; y < 40; y += 1) {
  for (let x = 0; x < 40; x += 1) {
    const isCorePair = coreNumbers.has(x + 1) && coreNumbers.has(y + 1)
    const value = x === y ? 0 : (isCorePair ? 0 : ((x * y + x + y) % 8))
    data.push([x, y, value])
  }
}

const render = () => {
  if (!matrixRef.value) return
  if (!chart) chart = echarts.init(matrixRef.value)
  chart.setOption({
    backgroundColor: 'transparent',
    tooltip: buildTooltip((params) => {
      const isCorePair = coreNumbers.has(params.value[0] + 1) && coreNumbers.has(params.value[1] + 1)
      return `
        <strong>${people[params.value[1]]}</strong> x <strong>${people[params.value[0]]}</strong><br/>
        提及次数：${params.value[2]}<br/>
        模式解释：${isCorePair ? '核心组内部出现异常沉默' : '普通公开互动'}
      `
    }),
    grid: { left: 62, right: 18, top: 20, bottom: 62 },
    xAxis: {
      type: 'category',
      data: people,
      ...buildAxis({ fontSize: 9, interval: 1 })
    },
    yAxis: {
      type: 'category',
      data: people,
      ...buildAxis({ fontSize: 9, interval: 1 })
    },
    visualMap: {
      min: 0,
      max: 8,
      orient: 'horizontal',
      left: 'center',
      bottom: 12,
      text: ['公开互动高', '接近沉默'],
      textStyle: { color: chartPalette.muted },
      inRange: { color: ['#f4f8fd', '#dce8f6', '#a2c4eb', '#5d98dd', '#f0b44c'] }
    },
    series: [{
      type: 'heatmap',
      data,
      progressive: 0,
      animationDuration: animationTiming.duration,
      animationEasing: animationTiming.easing,
      itemStyle: {
        borderColor: 'rgba(255,255,255,0.35)',
        borderWidth: 1
      },
      emphasis: {
        itemStyle: {
          borderColor: chartPalette.text,
          borderWidth: 1
        }
      }
    }]
  })
}

const resize = () => chart?.resize()
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
.matrix-frame {
  min-height: 590px;
}
</style>
