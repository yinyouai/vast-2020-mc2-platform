<template>
  <div class="panel">
    <div class="panel-header">
      <div>
        <h4 class="panel-title">暗号物证流向</h4>
        <p class="panel-subtitle">过滤后，核心嫌疑组在黄色接头包上汇聚。</p>
      </div>
    </div>
    <div ref="sankeyRef" class="chart-frame sankey-frame"></div>
  </div>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'
import * as echarts from 'echarts'

const sankeyRef = ref(null)
let chart

const render = () => {
  if (!sankeyRef.value) return
  if (!chart) chart = echarts.init(sankeyRef.value)
  chart.setOption({
    backgroundColor: 'transparent',
    tooltip: { trigger: 'item' },
    series: [{
      type: 'sankey',
      left: 28,
      right: 28,
      top: 24,
      bottom: 24,
      nodeWidth: 14,
      nodeGap: 16,
      data: [
        { name: 'Core Suspects' },
        { name: 'Background Attendees' },
        { name: 'Notebook' },
        { name: 'Badge' },
        { name: 'Yellow Bag' },
        { name: 'Final Candidate Group' }
      ],
      links: [
        { source: 'Background Attendees', target: 'Notebook', value: 24 },
        { source: 'Background Attendees', target: 'Badge', value: 19 },
        { source: 'Core Suspects', target: 'Yellow Bag', value: 8 },
        { source: 'Yellow Bag', target: 'Final Candidate Group', value: 8 }
      ],
      lineStyle: { color: 'gradient', opacity: 0.35 },
      itemStyle: { borderColor: 'rgba(237,247,246,0.38)' },
      label: { color: '#edf7f6' },
      emphasis: { focus: 'adjacency' }
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
