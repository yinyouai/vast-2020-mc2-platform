<template>
  <div class="panel heatmap-panel">
    <div class="panel-header">
      <div>
        <span class="section-kicker">Ward 双向重排</span>
        <h4 class="panel-title">人物 × 物品共现矩阵</h4>
        <p class="panel-subtitle">当前数据层：{{ store.matrixDataSource === 'raw' ? '原始预测' : '人工校正' }}；颜色表示实际出现次数。</p>
      </div>
      <span class="data-chip">{{ suspects.length }} × {{ items.length }}</span>
    </div>

    <div class="matrix-summary">
      <div class="matrix-summary__item">
        <span>集中信号</span>
        <strong>{{ store.activeTotem || '等待分析' }} / {{ store.hackerGroup.length }} 人</strong>
      </div>
      <div class="matrix-summary__item">
        <span>交互提示</span>
        <strong>点击单元格可回到复核层</strong>
      </div>
    </div>

    <div ref="heatmapRef" class="chart-frame heatmap-frame"></div>
    <div class="heatmap-legend" aria-label="热力图颜色图例">
      <span>背景噪声</span>
      <i v-for="color in legendColors" :key="color" :style="{ background: color }"></i>
      <span>核心信号</span>
    </div>
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

const legendColors = ['#eef4fb', '#cfe0f7', '#93bbe7', '#4ea2d8', '#f0b44c']

const suspects = computed(() => store.orderedSuspects)
const items = computed(() => store.orderedItems)

const buildData = () => {
  const lookup = new Map()
  store.heatmapMatrixData.forEach((entry) => {
    lookup.set(`${entry.suspect}-${entry.item}`, entry.count)
  })

  const data = []
  suspects.value.forEach((suspect, y) => {
    items.value.forEach((item, x) => {
      const value = lookup.get(`${suspect}-${item}`) || 0
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
        ...buildAxis({ rotate: 32, fontSize: 10 }),
        axisLabel: {
          color: (value) => value === store.selectedCandidateLabel ? chartPalette.accent : chartPalette.muted,
          fontWeight: (value) => value === store.selectedCandidateLabel ? 800 : 500,
          rotate: 32,
          interval: 0,
          fontSize: 10
        }
    },
    yAxis: {
      type: 'category',
      data: suspects.value,
        ...buildAxis({ fontSize: 10 }),
        axisLabel: {
          color: (value) => value === store.selectedPersonId
            ? chartPalette.accent
            : store.hackerGroup.includes(value) ? chartPalette.green : chartPalette.muted,
          fontWeight: (value) => value === store.selectedPersonId || store.hackerGroup.includes(value) ? 800 : 500,
          fontSize: 10
        }
    },
    visualMap: {
      show: false,
      min: 0,
      max: Math.min(8, Math.max(1, ...store.heatmapMatrixData.map((item) => item.count))),
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
    const itemName = items.value[params.value[0]]
    store.selectCandidate(itemName)
    const reviewItem = store.reviewQueue.find((item) =>
      item.person_id === target && item.corrected_label === itemName
    )
    if (reviewItem) store.selectReviewTarget(reviewItem)
    else store.selectPerson(target)
    router.push('/task2_correction')
  })
}

const resize = () => chart?.resize()

watch(
  () => [
    store.heatmapMatrixData,
    store.orderedSuspects,
    store.orderedItems,
    store.selectedCandidateLabel,
    store.selectedPersonId,
    store.hackerGroup
  ],
  render,
  { deep: true }
)

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
.section-kicker{display:block;margin-bottom:5px;color:var(--subtle);font-size:.7rem;font-weight:800}

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

.heatmap-legend {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  margin-top: 10px;
  color: var(--subtle);
  font-size: 0.78rem;
  font-weight: 800;
}

.heatmap-legend i {
  width: 30px;
  height: 10px;
  border: 1px solid rgba(53, 89, 138, 0.1);
  border-radius: 999px;
}

@media (max-width: 1040px) {
  .matrix-summary {
    grid-template-columns: 1fr;
  }
}
</style>
