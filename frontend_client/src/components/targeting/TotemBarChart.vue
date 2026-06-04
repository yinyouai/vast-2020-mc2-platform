<template>
  <div class="panel">
    <div class="panel-header">
      <div>
        <h4 class="panel-title">物品覆盖率</h4>
        <p class="panel-subtitle">公共物品越高，作为定案证据的价值越低。</p>
      </div>
    </div>
    <div ref="barRef" class="chart-frame small-chart"></div>
  </div>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref, watch } from 'vue'
import * as echarts from 'echarts'
import { useDashboardStore } from '../../store/dashboard'

const store = useDashboardStore()
const barRef = ref(null)
let chart

const items = ['Notebook', 'Badge', 'Toy', 'Red Hat', 'Yellow Bag']
const values = [60, 48, 44, 41, 20]

const render = () => {
  if (!barRef.value) return
  if (!chart) chart = echarts.init(barRef.value)
  chart.setOption({
    backgroundColor: 'transparent',
    grid: { left: 48, right: 18, top: 18, bottom: 34 },
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      data: items,
      axisLabel: { color: '#9bb3b6' },
      axisLine: { lineStyle: { color: 'rgba(184,211,214,0.14)' } }
    },
    yAxis: {
      type: 'value',
      axisLabel: { color: '#9bb3b6', formatter: '{value}%' },
      splitLine: { lineStyle: { color: 'rgba(184,211,214,0.12)' } }
    },
    series: [{
      type: 'bar',
      data: values.map((value, index) => ({
        value,
        itemStyle: {
          color: store.excludedItems.includes(items[index])
            ? '#70878b'
            : (items[index] === 'Yellow Bag' ? '#f4c95d' : '#42d6c2')
        }
      })),
      barWidth: 28
    }]
  })
}

const resize = () => chart?.resize()

watch(() => store.excludedItems, render, { deep: true })
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
.small-chart {
  min-height: 260px;
}
</style>
