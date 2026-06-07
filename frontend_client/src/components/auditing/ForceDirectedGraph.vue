<template>
  <section class="panel force-graph-panel">
    <div class="panel-header">
      <div>
        <span class="section-kicker">实体关系网络 (Force-Directed Layout)</span>
        <h4 class="panel-title">人员 - 图像 - 物品 关联拓扑</h4>
        <p class="visible-subtitle">展示当前阈值下模型检测到的所有物品分类关系。<span style="color:var(--accent)">人员</span> 连接 <span style="color:var(--green)">图片</span>，图片连接 <span style="color:var(--gold)">物体类别</span>。</p>
      </div>
    </div>
    <div ref="chartRef" class="force-chart"></div>
  </section>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import * as echarts from 'echarts'
import { useDashboardStore } from '../../store/dashboard'
import { chartPalette } from '../../utils/chartTheme'

const store = useDashboardStore()
const chartRef = ref(null)
let chart

const graphData = computed(() => store.modelAudit?.force_graph || { nodes: [], links: [] })

const render = () => {
  if (!chartRef.value) return
  if (!chart) chart = echarts.init(chartRef.value)

  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{b}'
    },
    legend: {
      data: ['人物', '图像', '物体类别'],
      top: 10,
      left: 'center'
    },
    series: [
      {
        type: 'graph',
        layout: 'force',
        roam: true,
        label: {
          show: true,
          position: 'right',
          formatter: '{b}',
          fontSize: 10,
          color: chartPalette.muted
        },
        draggable: true,
        categories: [
          { name: '人物', itemStyle: { color: chartPalette.accent } },
          { name: '图像', itemStyle: { color: chartPalette.green } },
          { name: '物体类别', itemStyle: { color: chartPalette.gold } }
        ],
        force: {
          repulsion: 150,
          edgeLength: [30, 80],
          gravity: 0.1
        },
        data: graphData.value.nodes.map(n => ({
          ...n,
          label: {
            show: n.category === 0 || n.category === 2 // Only show labels for Person and Object Category
          }
        })),
        links: graphData.value.links,
        lineStyle: {
          color: 'source',
          curveness: 0.2,
          opacity: 0.5
        }
      }
    ]
  }

  chart.setOption(option)
}

watch(() => graphData.value, render, { deep: true })
onMounted(() => { render(); window.addEventListener('resize', render) })
onBeforeUnmount(() => { window.removeEventListener('resize', render); chart?.dispose() })
</script>

<style scoped>
.force-graph-panel {
  display: flex;
  flex-direction: column;
}
.force-chart {
  min-height: 500px;
  flex: 1;
}
</style>
