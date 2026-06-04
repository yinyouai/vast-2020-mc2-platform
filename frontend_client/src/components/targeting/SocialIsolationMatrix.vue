<template>
  <div class="panel">
    <div class="panel-header">
      <div>
        <h4 class="panel-title">社交互动隔离矩阵</h4>
        <p class="panel-subtitle">核心组彼此在线上互动极低，符合刻意规避监控的行为模式。</p>
      </div>
    </div>
    <div ref="matrixRef" class="chart-frame matrix-frame"></div>
  </div>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'
import * as echarts from 'echarts'
import { useDashboardStore } from '../../store/dashboard'

const store = useDashboardStore()
const matrixRef = ref(null)
let chart

const people = Array.from({ length: 40 }, (_, i) => `P${i + 1}`)
const coreNumbers = new Set(store.hackerGroup.map((id) => Number(id.replace('Person', ''))))

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
    tooltip: {
      formatter: (params) => `${people[params.value[1]]} x ${people[params.value[0]]}: ${params.value[2]} mentions`
    },
    grid: { left: 54, right: 18, top: 24, bottom: 58 },
    xAxis: {
      type: 'category',
      data: people,
      axisLabel: { color: '#9bb3b6', fontSize: 9 },
      axisLine: { lineStyle: { color: 'rgba(184,211,214,0.14)' } }
    },
    yAxis: {
      type: 'category',
      data: people,
      axisLabel: { color: '#9bb3b6', fontSize: 9 },
      axisLine: { lineStyle: { color: 'rgba(184,211,214,0.14)' } }
    },
    visualMap: {
      min: 0,
      max: 8,
      orient: 'horizontal',
      left: 'center',
      bottom: 12,
      textStyle: { color: '#9bb3b6' },
      inRange: { color: ['#05090b', '#155e63', '#42d6c2', '#f4c95d'] }
    },
    series: [{
      type: 'heatmap',
      data,
      emphasis: { itemStyle: { borderColor: '#edf7f6', borderWidth: 1 } }
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
