<template>
  <aside class="panel verdict-panel">
    <div class="panel-header">
      <div>
        <h4 class="panel-title">证据叙事与最终判定</h4>
        <p class="panel-subtitle">把模型审计、人工修正、物证过滤和社交隔离整合为一条完整结论链。</p>
      </div>
    </div>

    <div class="verdict-list">
      <div class="verdict-item high">
        <span>核心名单</span>
        <strong>{{ coreList }}</strong>
        <p>这些目标在同一稀有物证上高度收敛，同时缺少自然的公开社交联系。</p>
      </div>

      <div class="verdict-item">
        <span>排除样本</span>
        <strong>Person27</strong>
        <p>其物品分布更接近普通会场资产，也缺少与核心群体一致的结构性异常，因此更像误报对照样本。</p>
      </div>

      <div class="verdict-item high">
        <span>最终结论</span>
        <strong>黄色提袋承担了线下会合识别符号的角色。</strong>
        <p>在高覆盖公共物品被剔除后，该物证仍稳定连接核心嫌疑群体，是当前最有说服力的线下协同信号。</p>
      </div>
    </div>

    <div class="verdict-radar-head">
      <div>
        <span>置信读数</span>
        <strong>多源取证信号收敛</strong>
      </div>
      <p>雷达图面积越大，说明该群体同时满足物证特异性、社交隔离、图文一致性和误报排除等多个条件。</p>
    </div>

    <div ref="radarRef" class="chart-frame radar-frame"></div>
  </aside>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import * as echarts from 'echarts'
import { useDashboardStore } from '../../store/dashboard'
import { animationTiming, buildTooltip, chartPalette } from '../../utils/chartTheme'

const store = useDashboardStore()
const radarRef = ref(null)
let chart

const coreList = computed(() => store.hackerGroup.filter((id) => id !== 'Person27').join(', '))

const render = () => {
  if (!radarRef.value) return
  if (!chart) chart = echarts.init(radarRef.value)
  chart.setOption({
    backgroundColor: 'transparent',
    tooltip: buildTooltip((params) => `
      <strong>${params.name || '核心群体'}</strong><br/>
      物证特异性：${params.value[0]}<br/>
      社交隔离度：${params.value[1]}<br/>
      图文一致性：${params.value[2]}<br/>
      误报排除度：${params.value[3]}
    `),
    legend: {
      right: 0,
      top: 0,
      textStyle: { color: chartPalette.muted }
    },
    radar: {
      radius: '63%',
      center: ['50%', '58%'],
      indicator: [
        { name: '物证特异性', max: 100 },
        { name: '社交隔离度', max: 100 },
        { name: '图文一致性', max: 100 },
        { name: '误报排除度', max: 100 }
      ],
      axisName: {
        color: chartPalette.muted,
        fontSize: 11
      },
      splitLine: {
        lineStyle: {
          color: 'rgba(86, 112, 143, 0.14)'
        }
      },
      axisLine: {
        lineStyle: {
          color: 'rgba(86, 112, 143, 0.18)'
        }
      },
      splitArea: {
        areaStyle: {
          color: ['rgba(47,125,246,0.02)', 'rgba(53,181,166,0.03)']
        }
      }
    },
    series: [{
      name: '核心嫌疑群体',
      type: 'radar',
      symbol: 'circle',
      symbolSize: 7,
      data: [{
        value: [94, 91, 86, 82],
        name: '核心嫌疑群体',
        itemStyle: { color: chartPalette.gold },
        areaStyle: {
          color: 'rgba(240, 180, 76, 0.22)'
        },
        lineStyle: {
          width: 3,
          color: chartPalette.gold
        }
      }],
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
.verdict-panel {
  display: flex;
  flex-direction: column;
}

.verdict-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.verdict-item {
  padding: 14px;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  background: rgba(255, 255, 255, 0.82);
}

.verdict-item.high {
  border-color: rgba(240, 180, 76, 0.32);
  background: rgba(240, 180, 76, 0.1);
}

.verdict-item span,
.verdict-radar-head span {
  color: var(--subtle);
  font-size: 0.78rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.verdict-item strong,
.verdict-radar-head strong {
  display: block;
  margin: 8px 0;
}

.verdict-item p,
.verdict-radar-head p {
  margin: 0;
  color: var(--muted);
  line-height: 1.7;
}

.verdict-radar-head {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(0, 0.9fr);
  gap: 14px;
  padding: 14px;
  margin-top: 14px;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  background: rgba(255, 255, 255, 0.78);
}

.radar-frame {
  min-height: 320px;
  margin-top: auto;
}

@media (max-width: 1040px) {
  .verdict-radar-head {
    grid-template-columns: 1fr;
  }
}
</style>
