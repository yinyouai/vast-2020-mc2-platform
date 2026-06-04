<template>
  <div class="glass-card component-wrapper">
    <h4 class="舱室标题">🛰️ 原始 YOLO v2 检测框物理空间核密度展布</h4>
    <div class="density-viewport" ref="densityChartRef"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import * as echarts from 'echarts'

const densityChartRef = ref(null)
let chart = null

onMounted(() => {
  if (!densityChartRef.value) return
  chart = echarts.init(densityChartRef.value, undefined)

  const points = Array.from({ length: 180 }, () => [
    Math.random() * 800,
    Math.random() * 600,
    Math.random()
  ])

  chart.setOption({
    backgroundColor: 'transparent',
    grid: { left: '4%', right: '4%', top: '4%', bottom: '4%' },
    xAxis: { show: false, min: 0, max: 800 },
    yAxis: { show: false, min: 0, max: 600 },
    series: [{
      type: 'scatter',
      data: points,
      symbolSize: (data) => data[2] * 20 + 5,
      itemStyle: {
        color: new echarts.graphic.RadialGradient(0.4, 0.3, 1, [
          { offset: 0, color: 'rgba(255, 90, 95, 0.7)' },
          { offset: 1, color: 'rgba(49, 194, 124, 0.08)' }
        ]),
        shadowBlur: 10,
        shadowColor: 'rgba(255, 90, 95, 0.3)'
      }
    }]
  })
})

onUnmounted(() => chart?.dispose())
</script>

<style scoped>
.component-wrapper { display: flex; flex-direction: column; height: 100%; }
.density-viewport { width: 100%; height: 160px; }
</style>
