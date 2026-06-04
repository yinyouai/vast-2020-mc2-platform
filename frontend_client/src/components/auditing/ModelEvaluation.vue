<template>
  <div class="glass-card chart-container">
    <h4 class="舱室标题">🛰️ 原始 YOLO v2 物资识别质量与置信度展布审计</h4>
    <div class="box-viewport" ref="boxChartRef"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick, onUnmounted } from 'vue'
import { useDashboardStore } from '../../store/dashboard'
import * as echarts from 'echarts'

const store = useDashboardStore()
const boxChartRef = ref(null)
let myChart = null

const renderChart = () => {
  if (!boxChartRef.value) return
  if (myChart) myChart.dispose()

  myChart = echarts.init(boxChartRef.value, undefined)

  const defaultStats = store.modelEvaluationData && Object.keys(store.modelEvaluationData).length > 0
    ? store.modelEvaluationData
    : {
        paperPlate: { min: 0.27, q1: 0.35, median: 0.49, q3: 0.71, max: 0.97 },
        lavenderDie: { min: 0.25, q1: 0.32, median: 0.41, q3: 0.55, max: 0.91 },
        redWhistle: { min: 0.25, q1: 0.31, median: 0.41, q3: 0.55, max: 0.88 },
        pumpkinNotes: { min: 0.25, q1: 0.29, median: 0.35, q3: 0.44, max: 0.80 },
        yellowBag: { min: 0.25, q1: 0.29, median: 0.34, q3: 0.41, max: 0.79 },
        hairClip: { min: 0.25, q1: 0.31, median: 0.38, q3: 0.51, max: 0.89 },
        eyeball: { min: 0.25, q1: 0.28, median: 0.33, q3: 0.39, max: 0.81 }
      }

  const categories = Object.keys(defaultStats)
  const boxData = categories.map(k => [
    defaultStats[k].min, defaultStats[k].q1, defaultStats[k].median,
    defaultStats[k].q3, defaultStats[k].max
  ])

  myChart.setOption({
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(255,255,255,0.95)',
      borderColor: 'rgba(0,0,0,0.08)',
      textStyle: { color: '#1A1A2E' },
      formatter: (params) => {
        if (params.componentSubtype === 'boxplot') {
          return `📦 <b>物资品类: ${params.name}</b><br/>
                  最大: ${params.value[5]}<br/>
                  Q3: ${params.value[4]}<br/>
                  中位数: ${params.value[3]}<br/>
                  Q1: ${params.value[2]}<br/>
                  最小: ${params.value[1]}`
        }
      }
    },
    grid: { left: '10%', right: '4%', top: '10%', bottom: '18%' },
    xAxis: {
      type: 'category', data: categories,
      axisLabel: { rotate: 25, color: '#636378', fontSize: 11, fontWeight: 500 }
    },
    yAxis: {
      type: 'value', min: 0.25, max: 1.0,
      name: 'YOLO 置信度', nameTextStyle: { color: '#636378', fontSize: 11 },
      axisLabel: { color: '#636378' },
      splitLine: { lineStyle: { color: 'rgba(0,0,0,0.05)' } }
    },
    visualMap: {
      show: false,
      pieces: [{ gt: store.scoreThreshold, color: '#31C27C' }],
      outOfRange: { color: '#FF5A5F' }
    },
    series: [{
      type: 'boxplot',
      data: boxData,
      itemStyle: { borderWidth: 1.5, stroke: '#636378' },
      boxWidth: [10, 30]
    }]
  })
}

watch(() => [store.modelEvaluationData, store.scoreThreshold], () => nextTick(renderChart))
onMounted(() => { renderChart() })
onUnmounted(() => myChart?.dispose())
</script>

<style scoped>
.chart-container { width: 100%; height: 100%; display: flex; flex-direction: column; }
.box-viewport { flex: 1; min-height: 330px; margin-top: var(--space-sm); }
</style>
