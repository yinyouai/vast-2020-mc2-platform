<template>
  <div class="panel">
    <div class="panel-header">
      <div>
        <h4 class="panel-title">暗号物证流向</h4>
        <p class="panel-subtitle">当公共物品被过滤后，核心嫌疑组会向黄色提袋这一条路径收敛。</p>
      </div>
    </div>
    <div ref="sankeyRef" class="chart-frame sankey-frame"></div>
  </div>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'
import * as echarts from 'echarts'
import { animationTiming, buildTooltip, chartPalette } from '../../utils/chartTheme'

const sankeyRef = ref(null)
let chart

const render = () => {
  if (!sankeyRef.value) return
  if (!chart) chart = echarts.init(sankeyRef.value)
  chart.setOption({
    backgroundColor: 'transparent',
    tooltip: buildTooltip((params) => {
      if (params.dataType === 'edge') {
        return `<strong>${params.data.source}</strong> -> <strong>${params.data.target}</strong><br/>流量强度：${params.data.value}`
      }
      return `<strong>${params.name}</strong><br/>表示过滤流程中的一个关键节点。`
    }),
    series: [{
      type: 'sankey',
      left: 10,
      right: 10,
      top: 10,
      bottom: 10,
      nodeAlign: 'justify',
      nodeWidth: 16,
      nodeGap: 18,
      draggable: false,
      data: [
        { name: '核心嫌疑组', itemStyle: { color: '#58c9b2' } },
        { name: '普通参会者', itemStyle: { color: '#b5c3d2' } },
        { name: '笔记本', itemStyle: { color: '#c4d3e1' } },
        { name: '胸牌', itemStyle: { color: '#d1dce7' } },
        { name: '黄色提袋', itemStyle: { color: '#f0b44c' } },
        { name: '最终候选组', itemStyle: { color: '#df6a6a' } }
      ],
      links: [
        { source: '普通参会者', target: '笔记本', value: 24 },
        { source: '普通参会者', target: '胸牌', value: 19 },
        { source: '核心嫌疑组', target: '黄色提袋', value: 8 },
        { source: '黄色提袋', target: '最终候选组', value: 8 }
      ],
      lineStyle: {
        color: 'gradient',
        opacity: 0.5,
        curveness: 0.5
      },
      itemStyle: {
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.5)'
      },
      label: {
        color: chartPalette.text,
        fontWeight: 700
      },
      emphasis: {
        focus: 'adjacency'
      },
      animationDuration: animationTiming.duration,
      animationEasing: animationTiming.easing
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
.sankey-frame {
  min-height: 420px;
}
</style>
