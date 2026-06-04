<template>
  <div class="glass-card matrix-wrapper">
    <h4 class="舱室标题">🛡️ 黑客网络隐形社交零提及与通讯隔离真值矩阵</h4>
    <div class="matrix-viewport" ref="chartRef"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useDashboardStore } from '../../store/dashboard'
import { HACKER_LIST } from '../../constants/forensics'
import * as echarts from 'echarts'

const store = useDashboardStore()
const chartRef = ref(null)
let chart = null

onMounted(() => {
  if (!chartRef.value) return
  chart = echarts.init(chartRef.value, undefined)

  const size = 16
  const axisData = Array.from({ length: size }, (_, i) => `P${i + 1}`)

  const matrixPoints = []
  for (let y = 0; y < size; y++) {
    for (let x = 0; x < size; x++) {
      const pX = `Person${x + 1}`
      const pY = `Person${y + 1}`
      let count = x === y ? 0 : Math.floor(Math.random() * 7) + 2
      if (HACKER_LIST.includes(pX) && HACKER_LIST.includes(pY)) {
        count = 0
      }
      matrixPoints.push([x, y, count])
    }
  }

  chart.setOption({
    backgroundColor: 'transparent',
    tooltip: {
      backgroundColor: 'rgba(255,255,255,0.95)',
      borderColor: 'rgba(0,0,0,0.1)',
      textStyle: { color: '#1A1A2E' },
      formatter: (params) => {
        const uX = `Person${params.value[0] + 1}`
        const uY = `Person${params.value[1] + 1}`
        const bothHacker = HACKER_LIST.includes(uX) && HACKER_LIST.includes(uY) && uX !== uY
        if (bothHacker) {
          return `<b>⚠️ 社交隔离真空</b><br/>${uX} ↔ ${uY}<br/>线上互动: <span style="color:#FF5A5F">0 次</span><br/>物理共现但线上零交集！`
        }
        return `<b>外围网络参照</b><br/>${uX} ↔ ${uY}<br/>互动: <span style="color:#31C27C">${params.value[2]} 次</span>`
      }
    },
    grid: { left: '8%', right: '4%', top: '4%', bottom: '12%' },
    xAxis: {
      type: 'category', data: axisData,
      axisLabel: { fontSize: 9, rotate: 25, color: '#636378' }
    },
    yAxis: {
      type: 'category', data: axisData,
      axisLabel: { fontSize: 9, color: '#636378' }
    },
    visualMap: {
      min: 0, max: 8, show: true, orient: 'horizontal', left: 'center', bottom: 0,
      text: ['高频互动', '社交隔离'],
      textStyle: { color: '#636378', fontSize: 10 },
      inRange: { color: ['#0A0A0E', '#1A237E', '#42A5F5', '#E8F5E9'] }
    },
    series: [{
      type: 'heatmap',
      data: matrixPoints,
      itemStyle: { borderColor: 'rgba(0,0,0,0.08)', borderWidth: 1 }
    }]
  })

  chart.on('click', (params) => {
    if (params.componentType === 'series') {
      const clickedX = `Person${params.value[0] + 1}`
      const clickedY = `Person${params.value[1] + 1}`
      const targetId = HACKER_LIST.includes(clickedX) ? clickedX : clickedY
      store.selectPerson(targetId)
    }
  })
})

onUnmounted(() => chart?.dispose())
</script>

<style scoped>
.matrix-wrapper { display: flex; flex-direction: column; height: 100%; }
.matrix-viewport { flex: 1; min-height: 400px; margin-top: var(--space-sm); }
</style>
