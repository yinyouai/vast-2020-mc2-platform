<template>
  <section class="panel process-panel network-panel">
    <div class="panel-header">
      <div>
        <h4 class="panel-title">预测网络 vs 修正网络</h4>
        <p class="panel-subtitle">公共物品剔除后，噪声边被压缩，黄色提袋路径更清晰。</p>
      </div>
    </div>

    <div class="network-grid">
      <article class="network-card is-before">
        <div class="network-card__head">
          <span>修正前</span>
          <strong>预测网络拥挤</strong>
        </div>
        <svg viewBox="0 0 520 360" class="network-svg" aria-label="预测网络">
          <path v-for="edge in noisyEdges" :key="edge.id" :d="edge.path" class="edge is-noise" />
          <g v-for="node in beforeNodes" :key="node.id" :transform="`translate(${node.x}, ${node.y})`">
            <circle v-if="node.type === 'item'" r="20" class="item-node is-noise-node" />
            <rect v-else x="-25" y="-16" width="50" height="32" rx="12" class="person-node" />
            <text text-anchor="middle" dy="4">{{ node.label }}</text>
          </g>
        </svg>
      </article>

      <article class="network-card is-after">
        <div class="network-card__head">
          <span>修正后</span>
          <strong>核心暗号收敛</strong>
        </div>
        <svg viewBox="0 0 520 360" class="network-svg" aria-label="修正网络">
          <path v-for="edge in cleanEdges" :key="edge.id" :d="edge.path" :class="['edge', edge.main && 'is-main']" />
          <g v-for="node in afterNodes" :key="node.id" :transform="`translate(${node.x}, ${node.y})`">
            <circle v-if="node.type === 'item'" r="24" :class="['item-node', node.main && 'is-main-node']" />
            <rect v-else x="-27" y="-17" width="54" height="34" rx="13" :class="['person-node', node.core && 'is-core']" />
            <text text-anchor="middle" dy="4">{{ node.label }}</text>
          </g>
        </svg>
      </article>
    </div>
  </section>
</template>

<script setup>
const beforeNodes = [
  { id: 'notebook', label: 'Notebook', x: 90, y: 82, type: 'item' },
  { id: 'badge', label: 'Badge', x: 92, y: 180, type: 'item' },
  { id: 'toy', label: 'Toy', x: 102, y: 282, type: 'item' },
  { id: 'bag', label: 'Yellow', x: 430, y: 118, type: 'item' },
  { id: 'p3', label: 'P3', x: 260, y: 78 },
  { id: 'p7', label: 'P7', x: 260, y: 130 },
  { id: 'p9', label: 'P9', x: 260, y: 182 },
  { id: 'p21', label: 'P21', x: 260, y: 234 },
  { id: 'p27', label: 'P27', x: 260, y: 286 }
]

const afterNodes = [
  { id: 'bag', label: 'Yellow Bag', x: 270, y: 180, type: 'item', main: true },
  { id: 'p3', label: 'P3', x: 145, y: 82, core: true },
  { id: 'p7', label: 'P7', x: 376, y: 82, core: true },
  { id: 'p9', label: 'P9', x: 418, y: 180, core: true },
  { id: 'p12', label: 'P12', x: 376, y: 278, core: true },
  { id: 'p32', label: 'P32', x: 145, y: 278, core: true },
  { id: 'noise', label: '公共噪声', x: 78, y: 180, type: 'item' }
]

const noisyEdges = [
  { id: 1, path: 'M90 82 C160 82 190 78 260 78' },
  { id: 2, path: 'M90 82 C160 98 190 130 260 130' },
  { id: 3, path: 'M92 180 C150 160 202 182 260 182' },
  { id: 4, path: 'M102 282 C150 260 205 234 260 234' },
  { id: 5, path: 'M430 118 C370 100 330 78 260 78' },
  { id: 6, path: 'M430 118 C366 160 330 286 260 286' },
  { id: 7, path: 'M92 180 C150 218 198 286 260 286' }
]

const cleanEdges = [
  { id: 1, path: 'M270 180 C225 128 190 96 145 82', main: true },
  { id: 2, path: 'M270 180 C310 126 340 94 376 82', main: true },
  { id: 3, path: 'M270 180 C326 180 370 180 418 180', main: true },
  { id: 4, path: 'M270 180 C310 232 340 266 376 278', main: true },
  { id: 5, path: 'M270 180 C224 232 190 266 145 278', main: true },
  { id: 6, path: 'M78 180 C128 180 172 180 214 180' }
]
</script>

<style scoped>
.network-panel {
  overflow: hidden;
}

.network-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: clamp(16px, 2vw, 24px);
}

.network-card {
  padding: 18px;
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  background:
    radial-gradient(circle at top right, rgba(47, 125, 246, 0.08), transparent 30%),
    linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(247, 251, 255, 0.86));
  box-shadow: var(--shadow-soft);
}

.network-card.is-after {
  background:
    radial-gradient(circle at 78% 20%, rgba(240, 180, 76, 0.14), transparent 30%),
    linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(247, 251, 255, 0.86));
}

.network-card__head span {
  color: var(--subtle);
  font-size: 0.76rem;
  font-weight: 900;
  letter-spacing: 0.08em;
}

.network-card__head strong {
  display: block;
  margin-top: 5px;
  font-size: 1rem;
}

.network-svg {
  width: 100%;
  margin-top: 14px;
  border: 1px solid rgba(53, 89, 138, 0.08);
  border-radius: 22px;
  background:
    radial-gradient(circle at 50% 50%, rgba(47, 125, 246, 0.06), transparent 30%),
    linear-gradient(180deg, #ffffff, #f8fbff);
}

.edge {
  fill: none;
  stroke: rgba(57, 169, 125, 0.34);
  stroke-width: 3;
  stroke-linecap: round;
}

.edge.is-noise {
  stroke: rgba(162, 94, 78, 0.24);
  stroke-width: 2;
}

.edge.is-main {
  stroke: rgba(240, 180, 76, 0.7);
  stroke-width: 4;
}

.person-node {
  fill: rgba(238, 247, 242, 0.92);
  stroke: rgba(57, 169, 125, 0.38);
}

.person-node.is-core {
  fill: rgba(255, 245, 220, 0.94);
  stroke: rgba(240, 180, 76, 0.72);
}

.item-node {
  fill: rgba(229, 245, 239, 0.92);
  stroke: rgba(57, 169, 125, 0.46);
  stroke-width: 2;
}

.item-node.is-noise-node {
  fill: rgba(247, 221, 214, 0.72);
  stroke: rgba(162, 94, 78, 0.5);
}

.item-node.is-main-node {
  fill: rgba(255, 238, 196, 0.98);
  stroke: #f0b44c;
  stroke-width: 3;
  filter: drop-shadow(0 10px 16px rgba(240, 180, 76, 0.24));
}

text {
  fill: var(--text);
  font-size: 0.72rem;
  font-weight: 900;
}

@media (max-width: 1240px) {
  .network-grid {
    grid-template-columns: 1fr;
  }
}
</style>
