<template>
  <div class="apple-glass-card chart-wrapper">
    <h4 class="舱室标题">📊 组件 8 : 会场普及物资社会持有率与背景噪声削波分析</h4>
    <div class="bar-viewport" ref="barChartRef"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useDashboardStore } from '../../store/dashboard'
import * as echarts from 'echarts'

const store = useDashboardStore()
const barChartRef = ref(null)
let myChart = null

const renderBar = () => {
  if (!barChartRef.value) return
  if (myChart) myChart.dispose()

  myChart = echarts.init(barChartRef.value, 'dark')

  // 赛题真实物资普及率
  const itemsData = [
    { name: '薰衣草骰子', val: 60 }, { name: '参会胸章', val: 60 },
    { name: '通用发夹', val: 47 }, { name: '高危红哨子', val: 45 },
    { name: '南瓜便签', val: 35 }, { name: '秘密黄色提袋', val: 20 }
  ]

  const xData = itemsData.map(d => d.name)
  const yData = itemsData.map(d => {
    // 💡 交互反馈：如果分析师在组件 10 里排除了某个物资，柱子在视觉上瞬间变灰并产生削波塌陷
    const originName = d.name === '薰衣草骰子' ? 'lavenderDie' : d.name === '通用发夹' ? 'hairClip' : d.name === '高危红哨子' ? 'redWhistle' : d.name
    return store.excludedItems.includes(originName) ? 0 : d.val
  })

  myChart.setOption({
    backgroundColor: 'transparent',
    tooltip: { trigger: 'axis', formatter: '{b}: 持有覆盖率 {c}%' },
    grid: { left: '10%', right: '4%', top: '10%', bottom: '15%' },
    xAxis: {
    type: 'category',
    data: xData,
    axisLabel: {
      // 💡 核心大修复：设为 0 代表强行唤醒并显示全量横坐标标签，坚决不允许 ECharts 擅自隐藏！
      interval: 0,

      // 💡 倾斜度优化：将文字轻轻旋转 15~25 度，利用空间几何完美避开碰撞，给长文本留出绝对充足的伸展空间
      rotate: 20,

      // 视觉色彩微调，保持 Apple 视网膜极简灰
      color: '#8E8E93',
      fontSize: 10,
      fontWeight: 500,

      // 动态边界溢出防护：防止旋转后的长文字被图表边缘无情切除
      overflow: 'breakAll'
    },
    axisTick: {
      alignWithLabel: true // 让刻度线与中文标签的几何中心完美对齐
    }
    },
    yAxis: { type: 'value', max: 100, axisLabel: { formatter: '{value}%' }, splitLine: { lineStyle: { color: 'rgba(255,255,255,0.02)' } } },
    series: [{
      type: 'bar', data: yData,
      itemStyle: {
        color: (params) => params.name === '秘密黄色提袋' ? '#BF5AF2' : '#30D158'
      },
      barWidth: '40%'
    }]
  })
}

watch(() => store.excludedItems, renderBar, { deep: true })
onMounted(renderBar)
</script>
<style scoped> .chart-wrapper { display: flex; flex-direction: column; height: 100%; } .bar-viewport { flex: 1; min-height: 200px; } </style>