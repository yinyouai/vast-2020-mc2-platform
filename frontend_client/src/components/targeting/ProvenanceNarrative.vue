<template>
  <aside class="panel verdict-panel">
    <div class="panel-header">
      <div>
        <h4 class="panel-title">证据叙事与最终判定</h4>
        <p class="panel-subtitle">将模型、人工复核、物证过滤和社交矩阵合并。</p>
      </div>
    </div>

    <div class="verdict-list">
      <div class="verdict-item high">
        <span>核心名单</span>
        <strong>{{ coreList }}</strong>
        <p>这些目标在特殊物证上共同收敛，同时缺乏自然社交联系。</p>
      </div>

      <div class="verdict-item">
        <span>排除样本</span>
        <strong>Person27</strong>
        <p>其物品更符合公共会场资产，适合作为误报纠偏样本。</p>
      </div>

      <div class="verdict-item high">
        <span>最终结论</span>
        <strong>黄色接头包是线下会合暗号</strong>
        <p>公共物品被剔除后，该物证仍稳定连接核心嫌疑组，是最强定案线索。</p>
      </div>
    </div>

    <div ref="radarRef" class="chart-frame radar-frame"></div>
  </aside>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import * as echarts from 'echarts'
import { useDashboardStore } from '../../store/dashboard'

const store = useDashboardStore()
const radarRef = ref(null)
let chart

const coreList = computed(() => store.hackerGroup.filter((id) => id !== 'Person27').join(', '))

const render = () => {
  if (!radarRef.value) return
  if (!chart) chart = echarts.init(radarRef.value)
  chart.setOption({
    backgroundColor: 'transparent',
    radar: {
      radius: '64%',
      indicator: [
        { name: '物证特异性', max: 100 },
        { name: '社交隔离', max: 100 },
        { name: '图文一致', max: 100 },
        { name: '误报排除', max: 100 }
      ],
      axisName: { color: '#9bb3b6' },
      splitLine: { lineStyle: { color: 'rgba(184,211,214,0.12)' } },
      axisLine: { lineStyle: { color: 'rgba(184,211,214,0.12)' } },
      splitArea: { areaStyle: { color: ['rgba(66,214,194,0.03)', 'rgba(255,255,255,0.015)'] } }
    },
    series: [{
      type: 'radar',
      data: [{
        value: [94, 91, 86, 82],
        itemStyle: { color: '#f4c95d' },
        areaStyle: { color: 'rgba(244,201,93,0.18)' },
        lineStyle: { width: 2 }
      }]
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
  border-radius: var(--radius);
  background: rgba(255, 255, 255, 0.035);
}

.verdict-item.high {
  border-color: rgba(244, 201, 93, 0.34);
  background: rgba(244, 201, 93, 0.08);
}

.verdict-item span {
  color: var(--subtle);
  font-size: 0.78rem;
  font-weight: 800;
}

.verdict-item strong {
  display: block;
  margin: 8px 0;
}

.verdict-item p {
  margin: 0;
  color: var(--muted);
  line-height: 1.55;
}

.radar-frame {
  min-height: 300px;
  margin-top: auto;
}
</style>
