<template>
  <section class="panel process-panel">
    <div class="panel-header">
      <div>
        <h4 class="panel-title">预测网络 vs 修正网络</h4>
        <p class="panel-subtitle">参考 TTU 的前后对照网络视角：左侧展示预测阶段的噪声网络，右侧展示经过人工复核与物证过滤后的收敛网络。</p>
      </div>
    </div>

    <div class="network-grid">
      <article class="network-card">
        <div class="network-card__head">
          <strong>修正前：预测网络</strong>
          <span>公共物品和误报边过多，网络结构拥挤且解释性差。</span>
        </div>
        <svg viewBox="0 0 520 520" class="network-svg" aria-label="预测网络">
          <g v-for="edge in predictedEdges" :key="edge.id">
            <line
              :x1="edge.x1"
              :y1="edge.y1"
              :x2="edge.x2"
              :y2="edge.y2"
              stroke="rgba(162,94,78,0.28)"
              :stroke-width="edge.width"
            />
          </g>
          <g v-for="person in peopleNodes" :key="person.id">
            <rect :x="person.x - 22" :y="person.y - 10" width="44" height="20" rx="4" fill="#eef3f8" stroke="#9db0c3" />
            <text :x="person.x" :y="person.y + 4" text-anchor="middle" font-size="10" fill="#17324d">{{ person.label }}</text>
          </g>
          <g v-for="item in predictedItems" :key="item.id">
            <circle :cx="item.x" :cy="item.y" r="7" fill="#f7ddd6" stroke="#bf7d68" stroke-width="2" />
            <text :x="item.x" :y="item.y - 14" text-anchor="middle" font-size="10" fill="#7d5446">{{ item.label }}</text>
          </g>
        </svg>
      </article>

      <article class="network-card">
        <div class="network-card__head">
          <strong>修正后：收敛网络</strong>
          <span>误报边被压缩，黄色提袋及其相关物证与核心组之间的关系更加清晰。</span>
        </div>
        <svg viewBox="0 0 520 520" class="network-svg" aria-label="修正网络">
          <g v-for="edge in correctedEdges" :key="edge.id">
            <line
              :x1="edge.x1"
              :y1="edge.y1"
              :x2="edge.x2"
              :y2="edge.y2"
              :stroke="edge.highlight ? 'rgba(223,106,106,0.72)' : 'rgba(57,169,125,0.34)'"
              :stroke-width="edge.width"
            />
          </g>
          <g v-for="person in peopleNodes" :key="person.id">
            <rect
              :x="person.x - 22"
              :y="person.y - 10"
              width="44"
              height="20"
              rx="4"
              :fill="person.highlight ? '#fff0ef' : '#eef7f2'"
              :stroke="person.highlight ? '#df6a6a' : '#7ab998'"
            />
            <text :x="person.x" :y="person.y + 4" text-anchor="middle" font-size="10" fill="#17324d">{{ person.label }}</text>
          </g>
          <g v-for="item in correctedItems" :key="item.id">
            <circle
              :cx="item.x"
              :cy="item.y"
              r="7"
              :fill="item.highlight ? '#fde8c4' : '#e5f5ef'"
              :stroke="item.highlight ? '#f0b44c' : '#39a97d'"
              stroke-width="2"
            />
            <text :x="item.x" :y="item.y - 14" text-anchor="middle" font-size="10" fill="#17324d">{{ item.label }}</text>
          </g>
        </svg>
      </article>
    </div>
  </section>
</template>

<script setup>
const peopleNodes = [
  { id: 'p3', label: 'P3', x: 260, y: 120, highlight: true },
  { id: 'p7', label: 'P7', x: 260, y: 170, highlight: true },
  { id: 'p9', label: 'P9', x: 260, y: 220, highlight: true },
  { id: 'p12', label: 'P12', x: 260, y: 270, highlight: true },
  { id: 'p21', label: 'P21', x: 260, y: 320, highlight: false },
  { id: 'p27', label: 'P27', x: 260, y: 370, highlight: false },
  { id: 'p32', label: 'P32', x: 260, y: 420, highlight: true }
]

const predictedItems = [
  { id: 'notebook', label: 'Notebook', x: 90, y: 120 },
  { id: 'badge', label: 'Badge', x: 120, y: 210 },
  { id: 'toy', label: 'Toy', x: 88, y: 300 },
  { id: 'yellowbag', label: 'YellowBag', x: 430, y: 150 },
  { id: 'eyeball', label: 'Eyeball', x: 425, y: 240 },
  { id: 'cloud', label: 'CloudSign', x: 440, y: 330 },
  { id: 'redwhistle', label: 'RedWhistle', x: 410, y: 410 }
]

const correctedItems = [
  { id: 'yellowbag', label: 'YellowBag', x: 430, y: 150, highlight: true },
  { id: 'hairclip', label: 'HairClip', x: 418, y: 260, highlight: false },
  { id: 'notebook', label: 'Notebook', x: 106, y: 150, highlight: false },
  { id: 'badge', label: 'Badge', x: 88, y: 260, highlight: false }
]

const predictedEdges = [
  { id: 1, x1: 90, y1: 120, x2: 260, y2: 120, width: 1.4 },
  { id: 2, x1: 90, y1: 120, x2: 260, y2: 170, width: 1.3 },
  { id: 3, x1: 120, y1: 210, x2: 260, y2: 220, width: 1.2 },
  { id: 4, x1: 88, y1: 300, x2: 260, y2: 270, width: 1.2 },
  { id: 5, x1: 430, y1: 150, x2: 260, y2: 120, width: 2.1 },
  { id: 6, x1: 425, y1: 240, x2: 260, y2: 170, width: 1.4 },
  { id: 7, x1: 440, y1: 330, x2: 260, y2: 320, width: 1.4 },
  { id: 8, x1: 410, y1: 410, x2: 260, y2: 370, width: 1.5 },
  { id: 9, x1: 430, y1: 150, x2: 260, y2: 420, width: 2.3 },
  { id: 10, x1: 120, y1: 210, x2: 260, y2: 370, width: 1.3 }
]

const correctedEdges = [
  { id: 1, x1: 430, y1: 150, x2: 260, y2: 120, width: 3.2, highlight: true },
  { id: 2, x1: 430, y1: 150, x2: 260, y2: 170, width: 3, highlight: true },
  { id: 3, x1: 430, y1: 150, x2: 260, y2: 220, width: 2.8, highlight: true },
  { id: 4, x1: 430, y1: 150, x2: 260, y2: 270, width: 2.6, highlight: true },
  { id: 5, x1: 430, y1: 150, x2: 260, y2: 420, width: 2.8, highlight: true },
  { id: 6, x1: 106, y1: 150, x2: 260, y2: 370, width: 1.2, highlight: false },
  { id: 7, x1: 88, y1: 260, x2: 260, y2: 320, width: 1.1, highlight: false },
  { id: 8, x1: 418, y1: 260, x2: 260, y2: 220, width: 1.2, highlight: false }
]
</script>

<style scoped>
.process-panel {
  overflow: hidden;
}

.network-grid {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: clamp(18px, 2.4vw, 30px);
}

.network-card {
  padding: clamp(16px, 2.2vw, 24px);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  background:
    radial-gradient(circle at top right, rgba(240, 180, 76, 0.08), transparent 30%),
    linear-gradient(180deg, rgba(255, 255, 255, 0.94), rgba(247, 251, 255, 0.84));
  box-shadow: var(--shadow-soft);
  transition:
    transform var(--motion-medium) var(--ease-spring),
    border-color var(--motion-medium) ease,
    box-shadow var(--motion-medium) ease;
}

.network-card:hover {
  transform: translateY(-5px);
  border-color: rgba(47, 125, 246, 0.18);
  box-shadow: var(--shadow-stage);
}

.network-card__head strong {
  display: block;
  margin-bottom: 6px;
  font-size: 1rem;
}

.network-card__head span {
  display: block;
  color: var(--muted);
  font-size: 0.84rem;
  line-height: 1.65;
}

.network-svg {
  width: 100%;
  margin-top: 12px;
  background: linear-gradient(180deg, #ffffff, #f8fbff);
  border-radius: 22px;
}

@media (max-width: 1240px) {
  .network-grid {
    grid-template-columns: 1fr;
  }
}
</style>
