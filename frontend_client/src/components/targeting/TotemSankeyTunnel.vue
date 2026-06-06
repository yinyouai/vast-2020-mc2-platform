<template>
  <div class="panel sankey-panel">
    <div class="panel-header">
      <div>
        <h4 class="panel-title">暗号物证流向</h4>
        <p class="panel-subtitle">仿用 others 的去噪漏斗逻辑：公共物品越多被剔除，背景流越弱，黄色提袋暗号流越突出。</p>
      </div>
      <span class="data-chip">{{ excludedCount }} 已剔除</span>
    </div>

    <div class="sankey-body-layout">
      <div ref="sankeyRef" class="chart-frame sankey-frame" aria-label="暗号物证桑基流向图"></div>

      <aside class="sankey-hud" aria-live="polite">
        <div class="hud-kicker">去噪剥离研判</div>
        <h5>{{ hudState.title }}</h5>
        <p>{{ hudState.summary }}</p>

        <div class="hud-metrics">
          <div>
            <span>背景噪声流</span>
            <strong>{{ flowModel.noiseFlow }}</strong>
          </div>
          <div>
            <span>暗号纯度</span>
            <strong>{{ flowModel.purity }}%</strong>
          </div>
          <div>
            <span>下钻状态</span>
            <strong>{{ canDrill ? '已解锁' : '待过滤' }}</strong>
          </div>
        </div>

        <div class="hud-callout" :class="hudState.tone">
          <strong>{{ hudState.calloutTitle }}</strong>
          <span>{{ hudState.callout }}</span>
        </div>

        <button
          class="primary-btn hud-action"
          type="button"
          :disabled="!canDrill"
          @click="openEvidence"
        >
          查看黄色提袋物证
        </button>
      </aside>
    </div>
  </div>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import * as echarts from 'echarts'
import { useDashboardStore } from '../../store/dashboard'
import { animationTiming, buildTooltip, chartPalette } from '../../utils/chartTheme'

const props = defineProps({
  items: {
    type: Array,
    default: () => []
  }
})

const store = useDashboardStore()
const sankeyRef = ref(null)
let chart

const excludedCount = computed(() => props.items.filter((item) => item.excluded).length)
const totalPublicCount = computed(() => props.items.filter((item) => item.role !== '候选暗号').length)
const canDrill = computed(() => excludedCount.value >= Math.min(3, totalPublicCount.value || 3))

const flowModel = computed(() => {
  const progress = totalPublicCount.value ? excludedCount.value / totalPublicCount.value : 0
  const noiseFlow = Math.max(5, Math.round(52 - progress * 44))
  const falsePositiveFlow = Math.max(3, Math.round(22 - progress * 16))
  const secretFlow = Math.round(24 + progress * 18)
  const purity = Math.min(98, Math.round(42 + progress * 54))

  return { noiseFlow, falsePositiveFlow, secretFlow, purity }
})

const hudState = computed(() => {
  if (!excludedCount.value) {
    return {
      tone: 'is-waiting',
      title: '背景流仍然占主导',
      summary: 'Notebook、Badge、Toy 等公共物品还在流图中占据大流量，黄色提袋信号会被普通参会者的礼品流遮盖。',
      calloutTitle: '当前风险',
      callout: 'Person27 这类普通样本会被公共物品拖入可疑链路，先剔除高覆盖物品再看暗号收敛。'
    }
  }

  if (!canDrill.value) {
    return {
      tone: 'is-progress',
      title: '去噪正在推进',
      summary: `已剔除 ${excludedCount.value} 项公共物品，背景流开始变薄，但暗号物证还没有达到稳定下钻阈值。`,
      calloutTitle: '下一步',
      callout: '继续剔除覆盖率过高的公共物资，直到黄色提袋路径成为主流向。'
    }
  }

  return {
    tone: 'is-success',
    title: '黄色提袋暗号流已收敛',
    summary: '公共礼品流被削弱后，核心嫌疑组到黄色提袋的路径成为主通道，符合 others 中的暗号图腾漏斗结论。',
    calloutTitle: '可下钻',
    callout: '点击桑基图中的“黄色提袋图腾”节点，或使用下方按钮打开第四层物证窗口。'
  }
})

const render = () => {
  if (!sankeyRef.value) return
  if (!chart) chart = echarts.init(sankeyRef.value)

  const { noiseFlow, falsePositiveFlow, secretFlow } = flowModel.value
  const nodes = [
    { name: '40名候选人', itemStyle: { color: chartPalette.accent } },
    { name: '公共礼品背景', itemStyle: { color: '#aebed0' } },
    { name: '误报对照样本', itemStyle: { color: chartPalette.red || '#df6a6a' } },
    { name: '核心嫌疑组', itemStyle: { color: chartPalette.green || '#35b5a6' } },
    { name: '秘密组织暗号', itemStyle: { color: '#c79335' } },
    { name: '黄色提袋图腾', itemStyle: { color: chartPalette.gold || '#f0b44c' } }
  ]

  const links = [
    { source: '40名候选人', target: '公共礼品背景', value: noiseFlow },
    { source: '公共礼品背景', target: '误报对照样本', value: falsePositiveFlow },
    { source: '40名候选人', target: '核心嫌疑组', value: secretFlow },
    { source: '核心嫌疑组', target: '秘密组织暗号', value: secretFlow },
    { source: '秘密组织暗号', target: '黄色提袋图腾', value: secretFlow }
  ]

  chart.setOption({
    backgroundColor: 'transparent',
    tooltip: buildTooltip((params) => {
      if (params.dataType === 'edge') {
        return `<strong>${params.data.source}</strong> -> <strong>${params.data.target}</strong><br/>流量强度：${params.data.value}`
      }
      return `<strong>${params.name}</strong><br/>${params.name === '黄色提袋图腾' ? '达到过滤阈值后可下钻查看物证。' : '过滤流程中的关键节点。'}`
    }),
    series: [{
      type: 'sankey',
      left: 4,
      right: 12,
      top: 10,
      bottom: 12,
      nodeAlign: 'justify',
      nodeWidth: 18,
      nodeGap: 18,
      draggable: false,
      data: nodes,
      links,
      lineStyle: {
        color: 'gradient',
        opacity: 0.5,
        curveness: 0.55
      },
      itemStyle: {
        borderWidth: 1,
        borderColor: 'rgba(255,255,255,0.72)',
        shadowBlur: 10,
        shadowColor: 'rgba(48,78,114,0.12)'
      },
      label: {
        color: '#17324d',
        fontWeight: 800,
        fontSize: 12
      },
      emphasis: { focus: 'adjacency' },
      animationDuration: animationTiming.duration,
      animationEasing: animationTiming.easing
    }]
  })

  chart.off('click')
  chart.on('click', (params) => {
    if (['黄色提袋图腾', '秘密组织暗号'].includes(params.name)) openEvidence()
  })
}

const openEvidence = () => {
  if (canDrill.value) store.isFourthLayerActive = true
}

const resize = () => chart?.resize()

watch(() => [props.items, store.excludedItems], render, { deep: true })
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

.sankey-body-layout {
  display: grid;
  grid-template-columns: minmax(0, 1.2fr) minmax(280px, 0.8fr);
  gap: 16px;
  align-items: stretch;
}

.sankey-frame {
  min-height: 420px;
}

.sankey-hud {
  display: flex;
  flex-direction: column;
  gap: 14px;
  min-height: 420px;
  padding: 16px;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  background:
    radial-gradient(circle at top right, rgba(240, 180, 76, 0.14), transparent 34%),
    linear-gradient(180deg, rgba(255, 255, 255, 0.92), rgba(247, 251, 255, 0.84));
}

.hud-kicker {
  color: var(--subtle);
  font-size: 0.76rem;
  font-weight: 900;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.sankey-hud h5 {
  margin: 0;
  font-size: 1.08rem;
}

.sankey-hud p {
  margin: 0;
  color: var(--muted);
  line-height: 1.68;
}

.hud-metrics {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 10px;
}

.hud-metrics div,
.hud-callout {
  padding: 12px;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  background: rgba(255, 255, 255, 0.78);
}

.hud-metrics span,
.hud-callout span {
  display: block;
  color: var(--subtle);
  font-size: 0.75rem;
  line-height: 1.5;
}

.hud-metrics strong,
.hud-callout strong {
  display: block;
  margin-bottom: 5px;
  color: var(--text);
}

.hud-callout.is-waiting {
  border-color: rgba(223, 106, 106, 0.24);
  background: rgba(223, 106, 106, 0.08);
}

.hud-callout.is-progress {
  border-color: rgba(240, 180, 76, 0.28);
  background: rgba(240, 180, 76, 0.1);
}

.hud-callout.is-success {
  border-color: rgba(57, 169, 125, 0.24);
  background: rgba(57, 169, 125, 0.09);
}

.hud-action {
  margin-top: auto;
}

.hud-action:disabled {
  opacity: 0.48;
  cursor: not-allowed;
  transform: none;
}

@media (max-width: 1180px) {
  .sankey-body-layout {
    grid-template-columns: 1fr;
  }
}
</style>
