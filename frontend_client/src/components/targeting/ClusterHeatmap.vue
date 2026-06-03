<template>
  <div class="apple-glass-card chart-container">
    <h4 class="舱室标题">📊 组件 7 : “人-物”资产光谱双向重排层次聚类矩阵 (动态洗牌架构)</h4>
    <div class="heatmap-canvas-lens" ref="heatmapViewportRef"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, nextTick } from 'vue'
import { useDashboardStore } from '../../store/dashboard'
// 💡 修复核心：引入现代路由跳转控制器
import { useRouter } from 'vue-router'
import * as echarts from 'echarts'

const store = useDashboardStore()
const router = useRouter()
const heatmapViewportRef = ref(null)
let myChart = null

const recomputeHeatmap = () => {
  if (!heatmapViewportRef.value) return
  if (myChart) myChart.dispose()

  myChart = echarts.init(heatmapViewportRef.value, 'dark')

  const xAxisData = store.orderedItems && store.orderedItems.length > 0
    ? store.orderedItems
    : ["【鸟鸣器】", "【南瓜便签】", "【眼球玩具】", "【发夹资产】", "【薰衣草骰子】", "【高危哨子】", "【黄色提袋】"]

  const yAxisData = store.orderedSuspects && store.orderedSuspects.length > 0
    ? store.orderedSuspects
    : Array.from({ length: 40 }, (_, i) => `嫌疑目标 P${i+1}`)

  const mappedPoints = []
  const countLookup = {}

  if (store.heatmapMatrixData && store.heatmapMatrixData.length > 0) {
    store.heatmapMatrixData.forEach(d => {
      countLookup[`${d.suspect}-${d.item}`] = d.count
    })
  }

  for (let yIdx = 0; yIdx < yAxisData.length; yIdx++) {
    for (let xIdx = 0; xIdx < xAxisData.length; xIdx++) {
      let count = 0
      if (store.heatmapMatrixData && store.heatmapMatrixData.length > 0) {
        const suspectKey = store.orderedSuspects[yIdx]
        const itemKey = store.orderedItems[xIdx]
        count = countLookup[`${suspectKey}-${itemKey}`] || 0
      } else {
        if (yIdx < 8 && xIdx === 6) count = 3
        else if (yIdx >= 8 && yIdx < 25 && xIdx < 4) count = Math.floor(Math.random() * 3) + 1
        else if (yIdx >= 25 && xIdx >= 4 && xIdx < 6) count = 2
      }
      mappedPoints.push([xIdx, yIdx, count])
    }
  }

  myChart.setOption({
    backgroundColor: 'transparent',
    tooltip: {
      position: 'top',
      backgroundColor: 'rgba(10,10,14,0.9)',
      borderColor: 'rgba(255,255,255,0.1)',
      formatter: (params) => {
        return `👤 <b>取证实体轴: ${yAxisData[params.value[1]]}</b><br/>
                📦 <b>特征物资轴: ${xAxisData[params.value[0]]}</b><br/>
                🔢 <b>去噪后持有频次: <span style="color:#30D158">${params.value[2]} 次</span></b>`
      }
    },
    grid: { left: '10%', right: '4%', top: '4%', bottom: '15%' },
    xAxis: {
      type: 'category',
      data: xAxisData,
      axisLabel: { rotate: 25, fontSize: 10, color: '#8E8E93' }
    },
    yAxis: {
      type: 'category',
      data: yAxisData,
      axisLabel: { fontSize: 9, color: '#8E8E93' }
    },
    visualMap: {
      min: 0, max: 4, calculable: true, orient: 'horizontal', left: 'center', bottom: '0%',
      textStyle: { color: '#8E8E93', fontSize: 11 },
      inRange: { color: ['rgba(255,255,255,0.01)', '#1A1A2E', '#BF5AF2', '#30D158'] }
    },
    series: [{
      name: '光谱矩阵',
      type: 'heatmap',
      data: mappedPoints,
      progressive: 1000
    }]
  })

  // 💡 级联钻取流变完美修复！
  myChart.on('click', (params) => {
    if (params.componentType === 'series') {
      // 1. 获取点击行所在的嫌疑人 ID 真实字符串
      const targetSuspect = store.orderedSuspects.length > 0
        ? store.orderedSuspects[params.value[1]]
        : `Person${params.value[1] + 1}`

      // 2. 强力向全局状态网络广播更新
      store.selectPerson(targetSuspect)

      // 3. 🚨 核心修复：执行自动化路由跃迁，命令视口瞬间下钻跳转至层级二多模态交叉工作台！
      router.push('/task2_correction')
    }
  })
}

watch(() => [store.heatmapMatrixData, store.orderedSuspects, store.orderedItems], () => nextTick(recomputeHeatmap))
onMounted(() => { recomputeHeatmap() })
</script>

<style scoped>
.chart-container { width: 100%; height: 100%; display: flex; flex-direction: column; }
.heatmap-canvas-lens { flex: 1; min-height: 420px; margin-top: 10px; }
</style>