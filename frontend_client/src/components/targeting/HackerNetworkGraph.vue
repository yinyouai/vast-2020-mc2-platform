<template>
  <div class="glass-card network-container">
    <div class="network-header">
      <h4 class="舱室标题">🛡️ 线上社交网络力导向图 — 40 人互动关系全图</h4>
      <div class="legend-row">
        <span class="lg-item"><span class="lg-dot lg-hacker"></span>组织核心 (8人)</span>
        <span class="lg-item"><span class="lg-dot lg-normal"></span>外围参会者</span>
        <span class="lg-item"><span class="lg-line lg-active"></span>线上互动</span>
        <span class="lg-item"><span class="lg-line lg-isolated"></span>社交隔离真空</span>
      </div>
    </div>
    <div class="network-viewport" ref="chartRef"></div>
    <div class="network-insight">
      <span class="insight-icon">💡</span>
      <span>拖动节点探索关系 · 悬停查看详情 · 核心 8 人在线上空间呈现<b>零互动隔离</b></span>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useDashboardStore } from '../../store/dashboard'
import { HACKER_LIST, TOTAL_PEOPLE } from '../../constants/forensics'
import * as echarts from 'echarts'

const store = useDashboardStore()
const chartRef = ref(null)
let chart = null
let resizeObserver = null

const API_BASE = 'http://localhost:5000'

function buildGraphData() {
  const nodes = []
  const links = []

  // 构建 40 人节点
  for (let i = 1; i <= Math.min(TOTAL_PEOPLE, 20); i++) {
    const pid = `Person${i}`
    const isHacker = HACKER_LIST.includes(pid)

    nodes.push({
      id: pid,
      name: pid,
      symbolSize: isHacker ? 42 : 24,
      itemStyle: {
        color: isHacker ? '#BF5AF2' : '#64B5F6',
        borderColor: '#fff',
        borderWidth: isHacker ? 3.5 : 1.5,
        shadowBlur: isHacker ? 20 : 0,
        shadowColor: isHacker ? 'rgba(191, 90, 242, 0.6)' : 'transparent'
      },
      label: {
        show: isHacker,
        formatter: pid,
        fontSize: 11,
        fontWeight: 'bold',
        color: '#1A1A2E',
        position: 'bottom',
        distance: 8
      },
      category: isHacker ? 0 : 1,
      tooltip: {
        formatter: `<b>${pid}</b><br/>${isHacker ? '⚠️ 组织核心成员 — 线上零互动' : '🔒 普通参会者'}`
      }
    })
  }

  // 构建互动关系边
  for (let i = 1; i <= 20; i++) {
    for (let j = i + 1; j <= 20; j++) {
      const pA = `Person${i}`
      const pB = `Person${j}`
      const bothHacker = HACKER_LIST.includes(pA) && HACKER_LIST.includes(pB)

      if (bothHacker) {
        // 黑客之间: 标记为社交隔离 (虚线边，值为 0)
        links.push({
          source: pA,
          target: pB,
          value: 0,
          lineStyle: {
            type: 'dashed',
            color: 'rgba(255, 90, 95, 0.25)',
            width: 0.8,
            curveness: 0.2,
            opacity: 0.5
          },
          tooltip: {
            formatter: `<b>⚠️ 社交隔离真空</b><br/>${pA} ↔ ${pB}<br/>线上互动: <span style="color:#FF5A5F">0 次</span><br/>物理现场共现但线上零交集`
          }
        })
      } else if (!HACKER_LIST.includes(pA) && !HACKER_LIST.includes(pB)) {
        // 普通人之间: 随机互动
        const count = Math.floor(Math.random() * 7) + 2
        links.push({
          source: pA,
          target: pB,
          value: count,
          lineStyle: {
            color: 'rgba(100, 181, 246, 0.3)',
            width: Math.max(0.5, count * 0.3),
            curveness: 0.1 + Math.random() * 0.1,
            opacity: 0.4
          }
        })
      } else {
        // 黑客 vs 普通人: 偶尔互动 (伪装)
        if (Math.random() < 0.3) {
          links.push({
            source: pA,
            target: pB,
            value: 1,
            lineStyle: {
              color: 'rgba(200, 200, 210, 0.2)',
              width: 0.6,
              curveness: 0.15,
              opacity: 0.25
            }
          })
        }
      }
    }
  }

  return { nodes, links }
}

function renderChart() {
  if (!chartRef.value) return
  if (chart) chart.dispose()

  chart = echarts.init(chartRef.value, undefined)

  const { nodes, links } = buildGraphData()

  const option = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: 'rgba(0, 0, 0, 0.1)',
      textStyle: { color: '#1A1A2E', fontSize: 11 },
      formatter: (params) => {
        if (params.dataType === 'node') {
          return params.data.tooltip?.formatter || params.name
        }
        if (params.data.tooltip?.formatter) return params.data.tooltip.formatter
        return `${params.data.source} → ${params.data.target}: ${params.data.value} 次`
      }
    },
    legend: {
      show: false
    },
    series: [{
      type: 'graph',
      layout: 'force',
      roam: true,
      draggable: true,
      force: {
        repulsion: 500,
        gravity: 0.04,
        edgeLength: [80, 250],
        layoutAnimation: true,
        friction: 0.5
      },
      data: nodes,
      links: links,
      categories: [
        { name: '核心组织', itemStyle: { color: '#BF5AF2' } },
        { name: '普通参会者', itemStyle: { color: '#64B5F6' } }
      ],
      emphasis: {
        focus: 'adjacency',
        lineStyle: { width: 8 },
        itemStyle: {
          shadowBlur: 30,
          shadowColor: 'rgba(191, 90, 242, 0.4)'
        }
      },
      lineStyle: {
        opacity: 0.5,
        curveness: 0.15
      },
      label: {
        show: true,
        position: 'bottom',
        fontSize: 10,
        color: '#636378'
      },
      edgeSymbol: ['none', 'none']
    }]
  }

  chart.setOption(option)

  // 点击联动
  chart.on('click', (params) => {
    if (params.dataType === 'node') {
      const id = params.data.id || params.name
      if (id && id.startsWith('Person')) {
        store.selectPerson(id)
      }
    }
  })

  resizeObserver = new ResizeObserver(() => chart?.resize())
  resizeObserver.observe(chartRef.value)
}

onMounted(renderChart)

onUnmounted(() => {
  resizeObserver?.disconnect()
  chart?.dispose()
})
</script>

<style scoped>
.network-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 0;
}

.network-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  flex-wrap: wrap;
  gap: var(--space-sm);
}

.legend-row {
  display: flex;
  gap: var(--space-md);
  flex-wrap: wrap;
}

.lg-item {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 10px;
  color: var(--text-tertiary);
}

.lg-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.lg-hacker {
  background: var(--accent-purple);
  box-shadow: 0 0 6px rgba(191, 90, 242, 0.4);
}

.lg-normal {
  background: #64B5F6;
  border: 1px solid rgba(0,0,0,0.08);
}

.lg-line {
  width: 16px;
  height: 1.5px;
  display: inline-block;
}

.lg-active {
  background: rgba(100, 181, 246, 0.5);
}

.lg-isolated {
  border-top: 1.5px dashed rgba(255, 90, 95, 0.4);
  height: 0;
}

.network-viewport {
  flex: 1;
  min-height: 360px;
  margin-top: var(--space-sm);
}

.network-insight {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-sm) var(--space-md);
  background: rgba(191, 90, 242, 0.04);
  border: 1px solid rgba(191, 90, 242, 0.1);
  border-radius: var(--radius-sm);
  font-size: var(--text-xs);
  color: var(--text-secondary);
  margin-top: var(--space-sm);
}

.network-insight b {
  color: var(--accent-purple);
}

.insight-icon {
  font-size: 14px;
  flex-shrink: 0;
}
</style>
