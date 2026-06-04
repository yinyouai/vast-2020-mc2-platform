<template>
  <div class="glass-card chart-container">
    <h4 class="舱室标题">📊 人-物资产光谱双向重排层次聚类矩阵</h4>
    <div class="heatmap-viewport" ref="heatmapRef"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick, onUnmounted } from 'vue'
import { useDashboardStore } from '../../store/dashboard'
import { useRouter } from 'vue-router'
import { HACKER_LIST } from '../../constants/forensics'
import * as echarts from 'echarts'

const store = useDashboardStore()
const router = useRouter()
const heatmapRef = ref(null)
let chart = null

function renderHeatmap() {
  if (!heatmapRef.value) return
  if (chart) chart.dispose()

  chart = echarts.init(heatmapRef.value, undefined)

  const xData = store.orderedItems.length > 0
    ? store.orderedItems
    : ['鸟鸣器', '南瓜便签', '眼球玩具', '发夹资产', '薰衣草骰子', '高危哨子', '黄色提袋']

  const yData = store.orderedSuspects.length > 0
    ? store.orderedSuspects
    : Array.from({ length: 40 }, (_, i) => `Person${i + 1}`)

  const countLookup = {}
  if (store.heatmapMatrixData.length > 0) {
    store.heatmapMatrixData.forEach(d => {
      countLookup[`${d.suspect}-${d.item}`] = d.count
    })
  }

  const mappedPoints = []
  for (let y = 0; y < yData.length; y++) {
    for (let x = 0; x < xData.length; x++) {
      let count = 0
      if (store.heatmapMatrixData.length > 0) {
        count = countLookup[`${yData[y]}-${xData[x]}`] || 0
      } else {
        // 回退模拟数据
        if (y < 8 && x >= 5) count = 3
        else if (y >= 8 && y < 25 && x < 4) count = Math.floor(Math.random() * 3) + 1
        else if (y >= 25 && x >= 4 && x < 6) count = 2
      }
      mappedPoints.push([x, y, count])
    }
  }

  chart.setOption({
    backgroundColor: 'transparent',
    tooltip: {
      position: 'top',
      backgroundColor: 'rgba(255,255,255,0.95)',
      borderColor: 'rgba(0,0,0,0.08)',
      textStyle: { color: '#1A1A2E' },
      formatter: (params) => {
        const hackerMark = HACKER_LIST.includes(yData[params.value[1]]) ? ' ⚠️' : ''
        return `<b>取证实体: ${yData[params.value[1]]}${hackerMark}</b><br/>
                <b>特征物资: ${xData[params.value[0]]}</b><br/>
                持有频次: <span style="color:#31C27C">${params.value[2]} 次</span>`
      }
    },
    grid: { left: '12%', right: '4%', top: '4%', bottom: '15%' },
    xAxis: {
      type: 'category', data: xData,
      axisLabel: { rotate: 20, fontSize: 10, color: '#636378' }
    },
    yAxis: {
      type: 'category', data: yData,
      axisLabel: {
        fontSize: 9, color: '#636378',
        formatter: (value) => {
          return HACKER_LIST.includes(value) ? `⚠ ${value}` : value
        }
      }
    },
    visualMap: {
      min: 0, max: 4, calculable: true, orient: 'horizontal', left: 'center', bottom: '0%',
      textStyle: { color: '#636378', fontSize: 10 },
      inRange: { color: ['rgba(0,0,0,0.02)', '#E8F5E9', '#81C784', '#31C27C'] }
    },
    series: [{
      type: 'heatmap',
      data: mappedPoints,
      progressive: 1000,
      itemStyle: {
        borderColor: 'rgba(0,0,0,0.04)',
        borderWidth: 1
      }
    }]
  })

  // 点击级联
  chart.on('click', (params) => {
    if (params.componentType === 'series') {
      const targetSuspect = store.orderedSuspects.length > 0
        ? store.orderedSuspects[params.value[1]]
        : `Person${params.value[1] + 1}`
      store.selectPerson(targetSuspect)
      router.push('/task2_correction')
    }
  })
}

watch(() => [store.heatmapMatrixData, store.orderedSuspects, store.orderedItems],
  () => nextTick(renderHeatmap)
)
onMounted(() => renderHeatmap())
onUnmounted(() => chart?.dispose())
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.heatmap-viewport {
  flex: 1;
  min-height: 380px;
  margin-top: var(--space-sm);
}
</style>
