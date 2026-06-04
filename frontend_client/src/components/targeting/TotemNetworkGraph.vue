<template>
  <div class="glass-card network-container">
    <div class="network-header">
      <h4 class="舱室标题">🔮 人-物关联力导向网络图 (40 人 + 7 种物资)</h4>
      <div class="network-legend">
        <span class="net-legend-item"><span class="n-dot n-dot-hacker"></span>核心 8 人</span>
        <span class="net-legend-item"><span class="n-dot n-dot-person"></span>普通参会者</span>
        <span class="net-legend-item"><span class="n-dot n-dot-item"></span>物资品类</span>
      </div>
    </div>
    <div class="network-viewport" ref="chartRef"></div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, onUnmounted, nextTick } from 'vue'
import { useDashboardStore } from '../../store/dashboard'
import { HACKER_LIST, TOTAL_PEOPLE, ITEM_METADATA } from '../../constants/forensics'
import * as echarts from 'echarts'

const store = useDashboardStore()
const chartRef = ref(null)
let chart = null
let resizeObserver = null

const API_BASE = 'http://localhost:5000'

// 构建力导向图数据
function buildGraphData() {
  const nodes = []
  const links = []

  // 40 个人物节点
  for (let i = 1; i <= TOTAL_PEOPLE; i++) {
    const pid = `Person${i}`
    const isHacker = HACKER_LIST.includes(pid)
    const clusterGroup = isHacker ? 'C' : (i <= 8 ? 'B' : 'A')

    nodes.push({
      id: pid,
      name: pid,
      category: isHacker ? 'hacker' : 'person',
      symbolSize: isHacker ? 36 : 22,
      itemStyle: {
        color: isHacker ? '#BF5AF2' : (i <= 8 ? '#FF9F0A' : '#C0C0C0'),
        borderColor: isHacker ? '#fff' : 'rgba(255,255,255,0.6)',
        borderWidth: isHacker ? 3 : 1,
        shadowBlur: isHacker ? 15 : 0,
        shadowColor: isHacker ? 'rgba(191, 90, 242, 0.5)' : 'transparent'
      },
      label: {
        show: isHacker,
        formatter: pid,
        fontSize: 10,
        fontWeight: 'bold',
        color: '#1A1A2E'
      },
      tooltip: {
        formatter: `<b>${pid}</b><br/>${isHacker ? '⚠️ 核心组织成员' : '普通参会者'}`
      },
      // 力导向参数
      fixed: false,
      draggable: true
    })
  }

  // 7 种物资节点
  const itemKeys = Object.keys(ITEM_METADATA)
  const excludedSet = new Set(store.excludedItems)
  const filteredItems = itemKeys.filter(k => !excludedSet.has(k))

  for (const key of filteredItems) {
    const meta = ITEM_METADATA[key]
    const isTotem = meta.isSecretTotem

    nodes.push({
      id: key,
      name: meta.cnName,
      category: isTotem ? 'totem' : 'item',
      symbolSize: isTotem ? 38 : 28,
      itemStyle: {
        color: meta.color,
        borderColor: isTotem ? '#fff' : 'rgba(255,255,255,0.5)',
        borderWidth: isTotem ? 3 : 1.5,
        shadowBlur: isTotem ? 18 : 0,
        shadowColor: isTotem ? 'rgba(191, 90, 242, 0.5)' : 'transparent'
      },
      label: {
        show: true,
        formatter: meta.cnName.substring(0, 6),
        fontSize: 9,
        color: '#1A1A2E'
      },
      tooltip: {
        formatter: `<b>${meta.cnName}</b><br/>覆盖率: ${meta.coverage}%${meta.isSecretTotem ? '<br/>🔮 秘密接头图腾' : ''}`
      }
    })
  }

  // 人-物 持有关系边
  for (let i = 1; i <= TOTAL_PEOPLE; i++) {
    const pid = `Person${i}`
    const isHacker = HACKER_LIST.includes(pid)

    for (const key of filteredItems) {
      const meta = ITEM_METADATA[key]

      // 模拟持有关系: 黑客 100% 持有黄色提袋
      let hasItem = false
      if (meta.isSecretTotem) {
        hasItem = isHacker // 仅黑客持有秘密图腾
      } else {
        // 普通物品: 根据覆盖率随机分配
        const seed = (i * Object.keys(ITEM_METADATA).indexOf(key) * 7) % 100
        hasItem = seed < meta.coverage && !isHacker
      }

      if (hasItem) {
        links.push({
          source: pid,
          target: key,
          value: 1,
          lineStyle: {
            color: meta.isSecretTotem ? '#BF5AF2' : 'rgba(180, 180, 190, 0.3)',
            width: meta.isSecretTotem ? 2.5 : 0.8,
            curveness: 0.15,
            opacity: meta.isSecretTotem ? 0.7 : 0.3
          }
        })
      }
    }
  }

  return { nodes, links }
}

function renderChart() {
  if (!chartRef.value) return
  if (chart) chart.dispose()

  chart = echarts.init(chartRef.value, undefined) // 浅色主题

  const { nodes, links } = buildGraphData()

  const option = {
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: 'rgba(0, 0, 0, 0.08)',
      textStyle: { color: '#1A1A2E', fontSize: 12 },
      formatter: (params) => {
        if (params.dataType === 'node') {
          return params.data.tooltip?.formatter || params.name
        }
        return `${params.data.source} → ${params.data.target}`
      }
    },
    legend: {
      show: true,
      bottom: 0,
      textStyle: { fontSize: 11, color: '#636378' },
      data: [
        { name: '核心组织成员', icon: 'circle' },
        { name: '普通参会者', icon: 'circle' },
        { name: '物资品类', icon: 'roundRect' }
      ]
    },
    series: [{
      type: 'graph',
      layout: 'force',
      roam: true,
      draggable: true,
      force: {
        repulsion: 350,
        gravity: 0.06,
        edgeLength: [60, 200],
        layoutAnimation: true,
        friction: 0.6
      },
      data: nodes,
      links: links,
      categories: [
        { name: '核心组织成员', itemStyle: { color: '#BF5AF2' } },
        { name: '普通参会者', itemStyle: { color: '#C0C0C0' } },
        { name: '物资品类', itemStyle: { color: '#6495ED' } }
      ],
      emphasis: {
        focus: 'adjacency',
        lineStyle: { width: 6 },
        itemStyle: { shadowBlur: 20 }
      },
      lineStyle: {
        opacity: 0.3,
        curveness: 0.15
      },
      label: {
        show: true,
        position: 'bottom',
        fontSize: 10,
        color: '#1A1A2E'
      }
    }]
  }

  chart.setOption(option)

  // 点击事件: 下钻
  chart.on('click', (params) => {
    if (params.dataType === 'node') {
      const id = params.data.id || params.name
      if (id && id.startsWith('Person')) {
        store.selectPerson(id)
      } else if (id === 'yellowBag' || params.name?.includes('黄色提袋')) {
        if (store.excludedItems.length >= 3) {
          store.isFourthLayerActive = true
        }
      }
    }
  })

  // 响应大小变化
  resizeObserver = new ResizeObserver(() => {
    chart?.resize()
  })
  resizeObserver.observe(chartRef.value)
}

watch(() => store.excludedItems, () => nextTick(renderChart), { deep: true })

onMounted(() => renderChart())

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
  align-items: center;
  flex-wrap: wrap;
  gap: var(--space-sm);
}

.network-legend {
  display: flex;
  gap: var(--space-md);
  flex-wrap: wrap;
}

.net-legend-item {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 10px;
  color: var(--text-tertiary);
}

.n-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.n-dot-hacker {
  background: var(--accent-purple);
  box-shadow: 0 0 6px rgba(191, 90, 242, 0.4);
}

.n-dot-person {
  background: #C0C0C0;
  border: 1px solid rgba(0, 0, 0, 0.1);
}

.n-dot-item {
  width: 10px;
  height: 10px;
  border-radius: 3px;
  background: #6495ED;
}

.network-viewport {
  flex: 1;
  min-height: 380px;
  margin-top: var(--space-sm);
}
</style>
