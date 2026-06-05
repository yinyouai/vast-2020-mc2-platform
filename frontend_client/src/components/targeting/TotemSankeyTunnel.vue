<template>
  <div class="panel sankey-panel">
    <div class="panel-header">
      <div>
        <h4 class="panel-title">暗号物证流向</h4>
        <p class="panel-subtitle">跟随公共物品剔除状态实时收束。</p>
      </div>
      <span class="data-chip">{{ excludedCount }} 已剔除</span>
    </div>
    <div ref="sankeyRef" class="chart-frame sankey-frame"></div>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import * as echarts from 'echarts'
import { animationTiming, buildTooltip, chartPalette } from '../../utils/chartTheme'

const props = defineProps({
  items: {
    type: Array,
    default: () => []
  }
})

const sankeyRef = ref(null)
let chart

const excludedCount = computed(() => props.items.filter((item) => item.excluded).length)
const publicItems = computed(() => props.items.filter((item) => item.role !== '候选暗号'))
const candidate = computed(() => props.items.find((item) => item.role === '候选暗号') || props.items[props.items.length - 1])

const render = () => {
  if (!sankeyRef.value) return
  if (!chart) chart = echarts.init(sankeyRef.value)

  const publicLinks = publicItems.value.map((item) => ({
    source: '普通参会者',
    target: item.name,
    value: item.excluded ? Math.max(1, Math.round(item.coverage / 12)) : Math.round(item.coverage / 2)
  }))

  const candidateValue = Math.max(6, 8 + excludedCount.value * 2)

  chart.setOption({
    backgroundColor: 'transparent',
    tooltip: buildTooltip((params) => {
      if (params.dataType === 'edge') {
        return `<strong>${params.data.source}</strong> -> <strong>${params.data.target}</strong><br/>流量强度：${params.data.value}`
      }
      return `<strong>${params.name}</strong><br/>过滤流程中的关键节点。`
    }),
    series: [{
      type: 'sankey',
      left: 10,
      right: 10,
      top: 12,
      bottom: 12,
      nodeAlign: 'justify',
      nodeWidth: 18,
      nodeGap: 16,
      draggable: false,
      data: [
        { name: '核心嫌疑组', itemStyle: { color: '#35b5a6' } },
        { name: '普通参会者', itemStyle: { color: '#b5c3d2' } },
        ...publicItems.value.map((item) => ({
          name: item.name,
          itemStyle: { color: item.excluded ? '#c5d0dd' : '#9fb1c4' }
        })),
        { name: candidate.value?.name || 'Yellow Bag', itemStyle: { color: '#f0b44c' } },
        { name: '最终候选组', itemStyle: { color: '#df6a6a' } }
      ],
      links: [
        ...publicLinks,
        { source: '核心嫌疑组', target: candidate.value?.name || 'Yellow Bag', value: candidateValue },
        { source: candidate.value?.name || 'Yellow Bag', target: '最终候选组', value: candidateValue }
      ],
      lineStyle: {
        color: 'gradient',
        opacity: 0.48,
        curveness: 0.52
      },
      itemStyle: {
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.58)'
      },
      label: {
        color: chartPalette.text,
        fontWeight: 800
      },
      emphasis: { focus: 'adjacency' },
      animationDuration: animationTiming.duration,
      animationEasing: animationTiming.easing
    }]
  })
}

const resize = () => chart?.resize()

watch(() => props.items, render, { deep: true })
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
.sankey-panel {
  min-height: 0;
}

.sankey-frame {
  min-height: 420px;
}
</style>
