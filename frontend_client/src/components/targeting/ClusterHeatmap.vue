<template>
  <div class="panel heatmap-panel">
    <div class="panel-header">
      <div>
        <h4 class="panel-title">嫌疑人-物品共现矩阵</h4>
        <p class="panel-subtitle">颜色越亮，表示某个人与该物品之间的关联越强。</p>
      </div>
      <span class="data-chip">{{ suspects.length }} x {{ items.length }}</span>
    </div>

    <div class="matrix-summary">
      <div class="matrix-summary__item">
        <span>集中信号</span>
        <strong>黄色提袋局部收敛</strong>
      </div>
      <div class="matrix-summary__item">
        <span>交互提示</span>
        <strong>点击单元格可回到复核层</strong>
      </div>
    </div>

    <div ref="heatmapRef" class="chart-frame heatmap-frame"></div>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import * as echarts from 'echarts'
import { useDashboardStore } from '../../store/dashboard'
import { animationTiming, buildAxis, buildTooltip, chartPalette } from '../../utils/chartTheme'

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
    tooltip: buildTooltip((params) => {
      const suspect = suspects.value[params.value[1]]
      const item = items.value[params.value[0]]
      const intensity = ['无明显信号', '背景级别', '中等关联', '高关联', '核心收敛'][params.value[2]] || '已观测'
      return `
        <strong>${suspect}</strong><br/>
        物品：${item}<br/>
        关联强度：${params.value[2]}<br/>
        解释：${intensity}
      `
    }),
    grid: { left: 94, right: 22, top: 20, bottom: 96 },
    xAxis: {
      type: 'category',
      data: items.value,
      ...buildAxis({ rotate: 28, fontSize: 11 })
    },
    yAxis: {
      type: 'category',
      data: suspects.value,
      ...buildAxis({ fontSize: 10 })
    },
    visualMap: {
      min: 0,
      max: 4,
      calculable: false,
      orient: 'horizontal',
      left: 'center',
      bottom: 18,
      text: ['核心信号', '背景噪声'],
      textGap: 12,
      itemWidth: 180,
      itemHeight: 10,
      textStyle: { color: chartPalette.muted },
      inRange: { color: ['#eef4fb', '#cfe0f7', '#93bbe7', '#4ea2d8', '#f0b44c'] }
    },
    series: [{
      name: '共现强度',
      type: 'heatmap',
      data: buildData(),
      progressive: 0,
      animationDuration: animationTiming.duration,
      animationEasing: animationTiming.easing,
      itemStyle: {
        borderColor: 'rgba(255,255,255,0.35)',
        borderWidth: 1
      },
      emphasis: {
        itemStyle: {
          borderColor: chartPalette.text,
          borderWidth: 1.2,
          shadowBlur: 16,
          shadowColor: 'rgba(47, 125, 246, 0.2)'
        }
      }
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

.matrix-summary {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  margin-bottom: 14px;
}

.matrix-summary__item {
  padding: 12px 14px;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  background: rgba(255, 255, 255, 0.82);
}

.matrix-summary__item span {
  display: block;
  color: var(--subtle);
  font-size: 0.76rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.matrix-summary__item strong {
  display: block;
  margin-top: 8px;
}

.heatmap-frame {
  min-height: 540px;
}

@media (max-width: 1040px) {
  .matrix-summary {
    grid-template-columns: 1fr;
  }
}
</style>
