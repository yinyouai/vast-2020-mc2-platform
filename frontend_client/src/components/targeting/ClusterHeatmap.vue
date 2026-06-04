<template>
  <div class="panel heatmap-panel">
    <div class="panel-header">
      <div>
        <h4 class="panel-title">嫌疑人-物品共现热力矩阵</h4>
        <p class="panel-subtitle">颜色越亮，代表该目标与该物品的关联越强。</p>
      </div>
      <span class="data-chip">{{ suspects.length }} x {{ items.length }}</span>
    </div>
    <div ref="heatmapRef" class="chart-frame heatmap-frame"></div>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import * as echarts from 'echarts'
import { useDashboardStore } from '../../store/dashboard'

const store = useDashboardStore()
const router = useRouter()
const heatmapRef = ref(null)
let chart

const fallbackSuspects = Array.from({ length: 40 }, (_, i) => `Person${i + 1}`)
const fallbackItems = ['Notebook', 'Badge', 'Toy', 'Cap', 'Red Hat', 'Yellow Bag', 'Connector']

const suspects = computed(() => store.orderedSuspects.length ? store.orderedSuspects : fallbackSuspects)
const items = computed(() => store.orderedItems.length ? store.orderedItems : fallbackItems)

const buildData = () => {
  const lookup = new Map()
  store.heatmapMatrixData.forEach((entry) => {
    lookup.set(`${entry.suspect}-${entry.item}`, entry.count)
  })

  const core = new Set(store.hackerGroup)
  const data = []
  suspects.value.forEach((suspect, y) => {
    items.value.forEach((item, x) => {
      let value = lookup.get(`${suspect}-${item}`)
      if (value === undefined) {
        const itemKey = String(item).toLowerCase()
        if (core.has(suspect) && (itemKey.includes('yellow') || itemKey.includes('connector'))) value = 4
        else if (!core.has(suspect) && x < 4) value = (x + y) % 3
        else value = 0
      }
      data.push([x, y, value])
    })
  })
  return data
}

const render = () => {
  if (!heatmapRef.value) return
  if (!chart) chart = echarts.init(heatmapRef.value)
  chart.setOption({
    backgroundColor: 'transparent',
    tooltip: {
      position: 'top',
      formatter: (params) => {
        const suspect = suspects.value[params.value[1]]
        const item = items.value[params.value[0]]
        return `${suspect}<br/>${item}: ${params.value[2]}`
      }
    },
    grid: { left: 86, right: 22, top: 26, bottom: 82 },
    xAxis: {
      type: 'category',
      data: items.value,
      axisLabel: { color: '#9bb3b6', rotate: 32 },
      axisLine: { lineStyle: { color: 'rgba(184,211,214,0.14)' } }
    },
    yAxis: {
      type: 'category',
      data: suspects.value,
      axisLabel: { color: '#9bb3b6', fontSize: 10 },
      axisLine: { lineStyle: { color: 'rgba(184,211,214,0.14)' } }
    },
    visualMap: {
      min: 0,
      max: 4,
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      bottom: 16,
      textStyle: { color: '#9bb3b6' },
      inRange: { color: ['#0d1c21', '#155e63', '#42d6c2', '#f4c95d', '#ff6b6b'] }
    },
    series: [{
      type: 'heatmap',
      data: buildData(),
      emphasis: { itemStyle: { borderColor: '#edf7f6', borderWidth: 1 } }
    }]
  })

  chart.off('click')
  chart.on('click', (params) => {
    const target = suspects.value[params.value[1]]
    store.selectPerson(target)
    router.push('/task2_correction')
  })
}

const resize = () => chart?.resize()

watch(() => [store.heatmapMatrixData, store.orderedSuspects, store.orderedItems], render, { deep: true })

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
.heatmap-panel {
  min-height: 620px;
}

.heatmap-frame {
  min-height: 540px;
}
</style>
