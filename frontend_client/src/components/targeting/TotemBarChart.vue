<template>
  <div class="glass-card chart-wrapper">
    <h4 class="舱室标题">📊 会场普及物资社会持有率与背景噪声削波分析</h4>
    <div class="bar-viewport" ref="barRef"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, onUnmounted } from 'vue'
import { useDashboardStore } from '../../store/dashboard'
import * as echarts from 'echarts'

const store = useDashboardStore()
const barRef = ref(null)
let chart = null

const itemsData = [
  { name: '薰衣草骰子', val: 60, key: 'lavenderDie' },
  { name: '参会胸章', val: 60, key: 'sign' },
  { name: '通用发夹', val: 47, key: 'hairClip' },
  { name: '高危红哨子', val: 45, key: 'redWhistle' },
  { name: '南瓜便签', val: 35, key: 'pumpkinNotes' },
  { name: '秘密黄色提袋', val: 20, key: 'yellowBag' }
]

function renderBar() {
  if (!barRef.value) return
  if (chart) chart.dispose()
  chart = echarts.init(barRef.value, undefined)

  const xData = itemsData.map(d => d.name)
  const yData = itemsData.map(d => store.excludedItems.includes(d.key) ? 0 : d.val)

  chart.setOption({
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'axis',
      formatter: (params) => {
        const item = itemsData[params[0].dataIndex]
        const excluded = store.excludedItems.includes(item.key)
        return `${params[0].name}<br/>持有覆盖率: ${excluded ? '0% (已排除)' : item.val + '%'}`
      }
    },
    grid: { left: '8%', right: '4%', top: '8%', bottom: '18%' },
    xAxis: {
      type: 'category',
      data: xData,
      axisLabel: { interval: 0, rotate: 18, fontSize: 10, color: '#636378' }
    },
    yAxis: {
      type: 'value', max: 100,
      axisLabel: { formatter: '{value}%', fontSize: 10, color: '#636378' },
      splitLine: { lineStyle: { color: 'rgba(0,0,0,0.04)' } }
    },
    series: [{
      type: 'bar',
      data: yData.map((val, i) => ({
        value: val,
        itemStyle: {
          color: i === 5 ? '#BF5AF2' : '#31C27C',
          opacity: val === 0 ? 0.3 : 1
        }
      })),
      barWidth: '40%',
      animationDuration: 500,
      animationEasing: 'cubicOut'
    }]
  })
}

watch(() => store.excludedItems, renderBar, { deep: true })
onMounted(renderBar)
onUnmounted(() => chart?.dispose())
</script>

<style scoped>
.chart-wrapper { display: flex; flex-direction: column; height: 100%; }
.bar-viewport { flex: 1; min-height: 200px; }
</style>
