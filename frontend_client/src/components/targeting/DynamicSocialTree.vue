<template>
  <section class="panel dynamic-network-panel">
    <div class="panel-header">
      <div>
        <h4 class="panel-title">动态树状社交隔离网络</h4>
        <p class="panel-subtitle">外圈紫色节点代表 8 名核心成员，中心普通参会者保持自然互动；黄色提袋把线下物证链收束成最终嫌疑团体。</p>
      </div>
      <button type="button" class="ghost-btn" @click="restartNetwork">重新收束网络</button>
    </div>

    <div class="network-legend" aria-label="网络图图例">
      <span><i class="legend-core"></i>核心组织</span>
      <span><i class="legend-public"></i>普通互动</span>
      <span><i class="legend-totem"></i>黄色提袋</span>
      <span><i class="legend-silent"></i>社交隔离真空</span>
    </div>

    <div class="dynamic-network-layout">
      <div ref="stageRef" class="tree-stage">
        <svg ref="svgRef" viewBox="0 0 920 620" role="img" aria-label="动态树状社交隔离网络"></svg>
      </div>

      <aside class="network-detail-card">
        <span>{{ selectedNode.typeLabel }}</span>
        <strong>{{ selectedNode.label }}</strong>
        <p>{{ selectedNode.note }}</p>

        <div class="detail-metrics">
          <div>
            <small>物证强度</small>
            <b>{{ selectedNode.evidence }}</b>
          </div>
          <div>
            <small>公开互动</small>
            <b>{{ selectedNode.social }}</b>
          </div>
          <div>
            <small>判定状态</small>
            <b>{{ selectedNode.status }}</b>
          </div>
        </div>

        <button
          v-if="selectedNode.personId"
          type="button"
          class="primary-btn"
          @click="store.selectPerson(selectedNode.personId)"
        >
          锁定 {{ selectedNode.personId }}
        </button>
      </aside>
    </div>
  </section>
</template>

<script setup>
import { onBeforeUnmount, onMounted, ref } from 'vue'
import * as d3 from 'd3'
import { useDashboardStore } from '../../store/dashboard'

const store = useDashboardStore()
const svgRef = ref(null)
const stageRef = ref(null)
let simulation

const selectedNode = ref({
  label: '黄色提袋线下识别符号',
  typeLabel: '最终图腾',
  note: '它不是“出现次数最多”的公共物品，而是在过滤公共噪声后仍稳定连接 8 名核心成员的线下会合标记。',
  evidence: '94',
  social: '异常低',
  status: '最终收敛',
  personId: ''
})

const coreNodes = ['Person3', 'Person7', 'Person9', 'Person10', 'Person12', 'Person17', 'Person32', 'Person38']
const publicNodes = ['Person1', 'Person2', 'Person4', 'Person5', 'Person13', 'Person18', 'Person20', 'Person21', 'Person24', 'Person27']

const buildGraph = () => {
  const nodes = [
    {
      id: 'yellowBag',
      label: '黄色提袋',
      type: 'totem',
      orbit: 0,
      size: 26,
      typeLabel: '最终图腾',
      evidence: '94',
      social: '异常低',
      status: '最终收敛',
      note: '过滤笔记本、胸牌、玩具等公共物品后，黄色提袋仍然把核心组稳定串联起来。'
    },
    {
      id: 'publicHub',
      label: '公开会场',
      type: 'publicHub',
      orbit: 126,
      size: 17,
      typeLabel: '普通社交场',
      evidence: '28',
      social: '自然',
      status: '背景基线',
      note: '普通参会者之间存在自然公开互动，因此不应被误判为刻意隔离。'
    },
    ...coreNodes.map((id, index) => ({
      id,
      label: id,
      personId: id,
      type: 'core',
      orbit: 238,
      size: id === 'Person3' ? 22 : 19,
      angleHint: (Math.PI * 2 * index) / coreNodes.length,
      typeLabel: '核心组织节点',
      evidence: id === 'Person3' ? '98' : '90',
      social: '近乎沉默',
      status: '核心保留',
      note: `${id} 与黄色提袋或同源物证共同收敛，但公开社交网络中没有形成自然互动链。`
    })),
    ...publicNodes.map((id, index) => ({
      id,
      label: id,
      personId: id,
      type: id === 'Person27' ? 'washed' : 'public',
      orbit: id === 'Person27' ? 188 : 120,
      size: id === 'Person27' ? 16 : 13,
      angleHint: (Math.PI * 2 * index) / publicNodes.length,
      typeLabel: id === 'Person27' ? '误报洗白节点' : '普通参会者',
      evidence: id === 'Person27' ? '41' : '22',
      social: id === 'Person27' ? '普通' : '自然',
      status: id === 'Person27' ? '排除' : '背景',
      note: id === 'Person27'
        ? 'Person27 更像公共物品误报样本，适合作为反向排除对照。'
        : `${id} 保持普通公开互动，用于衬托核心组的社交隔离。`
    }))
  ]

  const links = [
    ...coreNodes.map((id) => ({ source: 'yellowBag', target: id, type: 'totem', strength: 0.82 })),
    ...publicNodes.map((id) => ({ source: 'publicHub', target: id, type: id === 'Person27' ? 'washed' : 'public', strength: 0.24 })),
    { source: 'Person3', target: 'Person7', type: 'silent', strength: 0.08 },
    { source: 'Person7', target: 'Person10', type: 'silent', strength: 0.08 },
    { source: 'Person10', target: 'Person12', type: 'silent', strength: 0.08 },
    { source: 'Person12', target: 'Person17', type: 'silent', strength: 0.08 },
    { source: 'Person17', target: 'Person32', type: 'silent', strength: 0.08 },
    { source: 'Person32', target: 'Person38', type: 'silent', strength: 0.08 },
    { source: 'Person1', target: 'Person13', type: 'public', strength: 0.2 },
    { source: 'Person4', target: 'Person21', type: 'public', strength: 0.2 },
    { source: 'Person18', target: 'Person24', type: 'public', strength: 0.2 },
    { source: 'Person20', target: 'Person27', type: 'washed', strength: 0.18 }
  ]

  return { nodes, links }
}

const paintNetwork = () => {
  if (!svgRef.value) return

  const width = 920
  const height = 620
  const graph = buildGraph()
  const svg = d3.select(svgRef.value)
  svg.selectAll('*').remove()

  const defs = svg.append('defs')
  const glow = defs.append('filter').attr('id', 'networkGlow').attr('x', '-40%').attr('y', '-40%').attr('width', '180%').attr('height', '180%')
  glow.append('feGaussianBlur').attr('stdDeviation', 6).attr('result', 'coloredBlur')
  const merge = glow.append('feMerge')
  merge.append('feMergeNode').attr('in', 'coloredBlur')
  merge.append('feMergeNode').attr('in', 'SourceGraphic')

  svg.append('circle')
    .attr('class', 'orbit-ring')
    .attr('cx', width / 2)
    .attr('cy', height / 2)
    .attr('r', 238)
    .attr('fill', 'none')
    .attr('stroke', 'rgba(198, 83, 255, 0.16)')
    .attr('stroke-width', 2)
    .attr('stroke-dasharray', '8 10')

  svg.append('circle')
    .attr('class', 'orbit-ring')
    .attr('cx', width / 2)
    .attr('cy', height / 2)
    .attr('r', 126)
    .attr('fill', 'none')
    .attr('stroke', 'rgba(47, 125, 246, 0.12)')
    .attr('stroke-width', 2)

  const linkLayer = svg.append('g').attr('class', 'link-layer')
  const nodeLayer = svg.append('g').attr('class', 'node-layer')

  const link = linkLayer
    .selectAll('line')
    .data(graph.links)
    .join('line')
    .attr('stroke', (d) => {
      if (d.type === 'totem') return 'rgba(240, 180, 76, 0.74)'
      if (d.type === 'silent') return 'rgba(223, 106, 106, 0.34)'
      if (d.type === 'washed') return 'rgba(57, 169, 125, 0.28)'
      return 'rgba(93, 152, 221, 0.24)'
    })
    .attr('stroke-width', (d) => (d.type === 'totem' ? 3.4 : d.type === 'silent' ? 1.4 : 1.8))
    .attr('stroke-dasharray', (d) => (d.type === 'silent' ? '5 8' : null))
    .attr('stroke-linecap', 'round')

  const node = nodeLayer
    .selectAll('g')
    .data(graph.nodes)
    .join('g')
    .attr('class', (d) => `tree-node is-${d.type}`)
    .attr('tabindex', 0)
    .attr('role', 'button')
    .attr('aria-label', (d) => `查看 ${d.label}`)
    .call(dragBehavior())

  node.append('circle')
    .attr('r', (d) => d.size + 9)
    .attr('fill', (d) => {
      if (d.type === 'totem') return 'rgba(240, 180, 76, 0.16)'
      if (d.type === 'core') return 'rgba(198, 83, 255, 0.18)'
      if (d.type === 'washed') return 'rgba(57, 169, 125, 0.13)'
      return 'rgba(47, 125, 246, 0.1)'
    })
    .attr('filter', (d) => (d.type === 'core' || d.type === 'totem' ? 'url(#networkGlow)' : null))

  node.append('circle')
    .attr('r', (d) => d.size)
    .attr('fill', (d) => {
      if (d.type === 'totem') return '#f0b44c'
      if (d.type === 'core') return '#c653ff'
      if (d.type === 'washed') return '#39a97d'
      if (d.type === 'publicHub') return '#35b5a6'
      return '#5d98dd'
    })
    .attr('stroke', '#ffffff')
    .attr('stroke-width', 3)

  node.append('text')
    .attr('text-anchor', 'middle')
    .attr('dy', (d) => d.size + 21)
    .attr('fill', '#17324d')
    .attr('font-size', (d) => (d.type === 'totem' ? 14 : 12))
    .attr('font-weight', 900)
    .text((d) => d.label)

  node
    .on('click', (_event, d) => chooseNode(d))
    .on('keydown', (event, d) => {
      if (event.key === 'Enter' || event.key === ' ') {
        event.preventDefault()
        chooseNode(d)
      }
    })
    .on('mouseenter', (_event, d) => focusNode(d, node, link))
    .on('mouseleave', () => resetFocus(node, link))

  simulation = d3.forceSimulation(graph.nodes)
    .force('link', d3.forceLink(graph.links).id((d) => d.id).distance((d) => (d.type === 'totem' ? 168 : 96)).strength((d) => d.strength))
    .force('charge', d3.forceManyBody().strength((d) => (d.type === 'totem' ? -620 : d.type === 'core' ? -170 : -90)))
    .force('center', d3.forceCenter(width / 2, height / 2))
    .force('radial', d3.forceRadial((d) => d.orbit, width / 2, height / 2).strength((d) => (d.type === 'totem' ? 0.2 : 0.72)))
    .force('collide', d3.forceCollide((d) => d.size + 18))
    .alpha(0.96)
    .on('tick', () => {
      link
        .attr('x1', (d) => d.source.x)
        .attr('y1', (d) => d.source.y)
        .attr('x2', (d) => d.target.x)
        .attr('y2', (d) => d.target.y)

      node.attr('transform', (d) => `translate(${d.x},${d.y})`)
    })
}

const chooseNode = (node) => {
  selectedNode.value = {
    label: node.label,
    typeLabel: node.typeLabel,
    note: node.note,
    evidence: node.evidence,
    social: node.social,
    status: node.status,
    personId: node.personId || ''
  }
  if (node.personId) store.selectPerson(node.personId)
}

const focusNode = (target, nodeSelection, linkSelection) => {
  const adjacent = new Set([target.id])
  linkSelection.each((link) => {
    const sourceId = typeof link.source === 'string' ? link.source : link.source.id
    const targetId = typeof link.target === 'string' ? link.target : link.target.id
    if (sourceId === target.id || targetId === target.id) {
      adjacent.add(sourceId)
      adjacent.add(targetId)
    }
  })

  nodeSelection.transition().duration(180).style('opacity', (node) => (adjacent.has(node.id) ? 1 : 0.26))
  linkSelection.transition().duration(180).style('opacity', (link) => {
    const sourceId = typeof link.source === 'string' ? link.source : link.source.id
    const targetId = typeof link.target === 'string' ? link.target : link.target.id
    return sourceId === target.id || targetId === target.id ? 1 : 0.14
  })
}

const resetFocus = (nodeSelection, linkSelection) => {
  nodeSelection.transition().duration(180).style('opacity', 1)
  linkSelection.transition().duration(180).style('opacity', 1)
}

const dragBehavior = () =>
  d3.drag()
    .on('start', (event, d) => {
      if (!event.active) simulation?.alphaTarget(0.28).restart()
      d.fx = d.x
      d.fy = d.y
    })
    .on('drag', (event, d) => {
      d.fx = event.x
      d.fy = event.y
    })
    .on('end', (event, d) => {
      if (!event.active) simulation?.alphaTarget(0)
      if (d.type !== 'totem') {
        d.fx = null
        d.fy = null
      }
    })

const restartNetwork = () => {
  simulation?.alpha(0.9).restart()
}

onMounted(paintNetwork)

onBeforeUnmount(() => {
  simulation?.stop()
})
</script>

<style scoped>
.dynamic-network-panel {
  overflow: hidden;
  padding: clamp(22px, 3vw, 34px);
}

.network-legend {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 18px;
}

.network-legend span {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  min-height: 34px;
  padding: 0 12px;
  border: 1px solid var(--border);
  border-radius: 999px;
  color: var(--muted);
  background: rgba(255, 255, 255, 0.74);
  font-size: 0.82rem;
  font-weight: 800;
}

.network-legend i {
  width: 10px;
  height: 10px;
  border-radius: 999px;
}

.legend-core {
  background: #c653ff;
}

.legend-public {
  background: #5d98dd;
}

.legend-totem {
  background: #f0b44c;
}

.legend-silent {
  background: #df6a6a;
}

.dynamic-network-layout {
  display: grid;
  grid-template-columns: minmax(0, 1fr) minmax(300px, 0.38fr);
  gap: clamp(18px, 2.2vw, 28px);
  align-items: stretch;
}

.tree-stage {
  min-height: clamp(520px, 62dvh, 720px);
  overflow: hidden;
  border: 1px solid rgba(53, 89, 138, 0.12);
  border-radius: var(--radius-xl);
  background:
    radial-gradient(circle at center, rgba(240, 180, 76, 0.12), transparent 16%),
    radial-gradient(circle at 24% 30%, rgba(198, 83, 255, 0.1), transparent 18%),
    radial-gradient(circle at 78% 68%, rgba(53, 181, 166, 0.12), transparent 22%),
    linear-gradient(180deg, #ffffff, #f7fbff);
  box-shadow: inset 0 1px 0 rgba(255, 255, 255, 0.9);
}

.tree-stage svg {
  width: 100%;
  height: 100%;
  min-height: inherit;
}

.network-detail-card {
  display: flex;
  flex-direction: column;
  gap: 14px;
  padding: 18px;
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  background:
    radial-gradient(circle at top right, rgba(240, 180, 76, 0.12), transparent 26%),
    rgba(255, 255, 255, 0.82);
}

.network-detail-card span {
  color: var(--subtle);
  font-size: 0.78rem;
  font-weight: 900;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.network-detail-card strong {
  font-family: "Source Han Serif SC", "Songti SC", "STSong", serif;
  font-size: clamp(1.35rem, 2vw, 2rem);
  line-height: 1.2;
}

.network-detail-card p {
  margin: 0;
  color: var(--muted);
  line-height: 1.75;
}

.detail-metrics {
  display: grid;
  grid-template-columns: 1fr;
  gap: 10px;
  margin-top: auto;
}

.detail-metrics div {
  padding: 12px;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  background: rgba(255, 255, 255, 0.76);
}

.detail-metrics small,
.detail-metrics b {
  display: block;
}

.detail-metrics small {
  color: var(--subtle);
  font-size: 0.78rem;
}

.detail-metrics b {
  margin-top: 6px;
  color: var(--text);
  font-size: 1.15rem;
}

:deep(.tree-node) {
  cursor: grab;
  outline: none;
}

:deep(.tree-node:focus-visible circle:last-of-type) {
  stroke: #17324d;
  stroke-width: 4;
}

:deep(.tree-node:active) {
  cursor: grabbing;
}

:deep(.tree-node.is-core circle:first-child),
:deep(.tree-node.is-totem circle:first-child) {
  animation: node-pulse 2.6s ease-in-out infinite;
}

:deep(.orbit-ring) {
  animation: orbit-spin 18s linear infinite;
  transform-origin: 460px 310px;
}

@keyframes node-pulse {
  0%,
  100% {
    opacity: 0.68;
    transform: scale(1);
  }
  50% {
    opacity: 1;
    transform: scale(1.08);
  }
}

@keyframes orbit-spin {
  to {
    transform: rotate(360deg);
  }
}

@media (max-width: 1180px) {
  .dynamic-network-layout {
    grid-template-columns: 1fr;
  }

  .detail-metrics {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
}

@media (max-width: 760px) {
  .panel-header {
    flex-direction: column;
  }

  .detail-metrics {
    grid-template-columns: 1fr;
  }
}
</style>
