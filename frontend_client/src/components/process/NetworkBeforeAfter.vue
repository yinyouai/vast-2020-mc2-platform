<template>
  <section class="panel process-panel network-panel">
    <div class="panel-header">
      <div>
        <h4 class="panel-title">预测网络 vs 修正网络</h4>
        <p class="panel-subtitle">公共物品剔除后，噪声边被压缩，黄色提袋路径成为更清晰的核心物证流。</p>
      </div>
      <div class="network-legend">
        <span><i class="legend-dot is-public"></i>公共噪声</span>
        <span><i class="legend-dot is-core"></i>核心路径</span>
        <span><i class="legend-dot is-person"></i>人物节点</span>
      </div>
    </div>

    <div class="network-grid">
      <article class="network-card is-before">
        <div class="network-card__head">
          <span>修正前</span>
          <strong>预测网络拥挤：公共物品把普通样本和核心样本混在一起</strong>
        </div>

        <svg viewBox="0 0 760 430" class="network-svg" aria-label="修正前预测网络">
          <defs>
            <filter id="node-shadow-before" x="-30%" y="-30%" width="160%" height="160%">
              <feDropShadow dx="0" dy="10" stdDeviation="7" flood-color="rgba(48,78,114,0.16)" />
            </filter>
          </defs>

          <g class="zone is-public-zone">
            <rect x="52" y="78" width="190" height="292" rx="28" fill="rgba(223,106,106,0.045)" stroke="rgba(223,106,106,0.14)" stroke-width="1.2" stroke-dasharray="8 8" />
            <text x="147" y="112" text-anchor="middle" fill="#7890ab">公共物品区</text>
          </g>
          <g class="zone is-mixed-zone">
            <rect x="316" y="78" width="212" height="292" rx="28" fill="rgba(47,125,246,0.035)" stroke="rgba(47,125,246,0.1)" stroke-width="1.2" stroke-dasharray="8 8" />
            <text x="422" y="112" text-anchor="middle" fill="#7890ab">混合候选区</text>
          </g>
          <g class="zone is-target-zone">
            <rect x="596" y="130" width="112" height="160" rx="28" fill="rgba(47,125,246,0.035)" stroke="rgba(47,125,246,0.1)" stroke-width="1.2" stroke-dasharray="8 8" />
            <text x="652" y="164" text-anchor="middle" fill="#7890ab">疑似物证</text>
          </g>

          <path v-for="edge in noisyEdges" :key="edge.id" :d="edge.path" fill="none" stroke="rgba(162,94,78,0.34)" stroke-width="2.4" stroke-linecap="round" />
          <path v-for="edge in weakEdges" :key="edge.id" :d="edge.path" fill="none" stroke="rgba(120,144,171,0.36)" stroke-width="2" stroke-dasharray="5 5" stroke-linecap="round" />

          <g v-for="node in beforeNodes" :key="node.id" :transform="`translate(${node.x}, ${node.y})`" filter="url(#node-shadow-before)">
            <rect
              v-if="node.type !== 'item'"
              x="-36"
              y="-20"
              width="72"
              height="40"
              rx="14"
              :class="['person-node', node.noise && 'is-noise-person']"
              :fill="node.noise ? 'rgba(247,221,214,0.92)' : 'rgba(238,247,242,0.98)'"
              :stroke="node.noise ? 'rgba(223,106,106,0.44)' : 'rgba(57,169,125,0.46)'"
              stroke-width="1.6"
            />
            <circle
              v-else
              r="34"
              :class="['item-node', node.main ? 'is-main-node' : 'is-public-node']"
              :fill="node.main ? 'rgba(255,238,196,0.98)' : 'rgba(247,221,214,0.9)'"
              :stroke="node.main ? '#f0b44c' : 'rgba(162,94,78,0.45)'"
              :stroke-width="node.main ? 3 : 2.2"
            />
            <text text-anchor="middle" dy="5" fill="#17324d" :class="{ 'is-long-label': node.long }">{{ node.label }}</text>
          </g>
        </svg>

        <div class="network-caption">
          <strong>问题</strong>
          <span>公共礼品边过多，P21/P27 等对照样本被拉进候选区，黄色提袋路径被噪声遮住。</span>
        </div>
      </article>

      <article class="network-card is-after">
        <div class="network-card__head">
          <span>修正后</span>
          <strong>暗号路径收敛：公共噪声沉降，黄色提袋连接核心嫌疑组</strong>
        </div>

        <svg viewBox="0 0 760 430" class="network-svg" aria-label="修正后网络">
          <defs>
            <filter id="node-shadow-after" x="-30%" y="-30%" width="160%" height="160%">
              <feDropShadow dx="0" dy="10" stdDeviation="7" flood-color="rgba(48,78,114,0.16)" />
            </filter>
            <radialGradient id="yellow-bag-fill" cx="40%" cy="30%" r="70%">
              <stop offset="0%" stop-color="#fff8df" />
              <stop offset="100%" stop-color="#f0b44c" />
            </radialGradient>
          </defs>

          <g class="zone is-core-zone">
            <rect x="72" y="68" width="446" height="318" rx="32" fill="rgba(240,180,76,0.065)" stroke="rgba(240,180,76,0.24)" stroke-width="1.2" stroke-dasharray="8 8" />
            <text x="295" y="104" text-anchor="middle" fill="#7890ab">核心嫌疑组收敛区</text>
          </g>
          <g class="zone is-target-zone">
            <rect x="584" y="116" width="138" height="194" rx="30" fill="rgba(47,125,246,0.035)" stroke="rgba(47,125,246,0.1)" stroke-width="1.2" stroke-dasharray="8 8" />
            <text x="653" y="148" text-anchor="middle" fill="#7890ab">暗号物证</text>
          </g>

          <path v-for="edge in cleanEdges" :key="edge.id" :d="edge.path" fill="none" stroke="rgba(240,180,76,0.78)" stroke-width="4.2" stroke-linecap="round" />
          <path d="M112 216 C168 216 210 216 256 216" fill="none" stroke="rgba(120,144,171,0.36)" stroke-width="2" stroke-dasharray="5 5" stroke-linecap="round" />

          <g transform="translate(112, 216)" filter="url(#node-shadow-after)">
            <circle r="34" class="item-node is-muted-node" fill="rgba(229,236,246,0.92)" stroke="rgba(120,144,171,0.5)" stroke-width="2.2" />
            <text text-anchor="middle" dy="5" fill="#17324d" class="is-long-label">公共噪声</text>
          </g>

          <g v-for="node in afterNodes" :key="node.id" :transform="`translate(${node.x}, ${node.y})`" filter="url(#node-shadow-after)">
            <rect x="-35" y="-20" width="70" height="40" rx="14" class="person-node is-core" fill="rgba(255,245,220,0.98)" stroke="rgba(240,180,76,0.8)" stroke-width="2" />
            <text text-anchor="middle" dy="5" fill="#17324d">{{ node.label }}</text>
          </g>

          <g transform="translate(654, 230)" filter="url(#node-shadow-after)">
            <circle r="42" class="item-node is-totem-node" fill="url(#yellow-bag-fill)" stroke="#f0b44c" stroke-width="3" />
            <text text-anchor="middle" dy="0" fill="#17324d">Yellow</text>
            <text text-anchor="middle" dy="16" fill="#17324d">Bag</text>
          </g>
        </svg>

        <div class="network-caption is-success">
          <strong>结果</strong>
          <span>过滤后主路径集中到黄色提袋，公共噪声只保留为弱背景，视觉结构更接近最终证据链。</span>
        </div>
      </article>
    </div>
  </section>
</template>

<script setup>
const beforeNodes = [
  { id: 'notebook', label: 'Notebook', x: 146, y: 150, type: 'item', long: true },
  { id: 'badge', label: 'Badge', x: 146, y: 224, type: 'item' },
  { id: 'toy', label: 'Toy', x: 146, y: 298, type: 'item' },
  { id: 'p3', label: 'P3', x: 420, y: 138 },
  { id: 'p7', label: 'P7', x: 420, y: 190 },
  { id: 'p9', label: 'P9', x: 420, y: 242 },
  { id: 'p21', label: 'P21', x: 420, y: 294, noise: true },
  { id: 'p27', label: 'P27', x: 420, y: 346, noise: true },
  { id: 'yellow', label: 'Yellow', x: 652, y: 216, type: 'item', main: true }
]

const afterNodes = [
  { id: 'p3', label: 'P3', x: 244, y: 142 },
  { id: 'p7', label: 'P7', x: 352, y: 142 },
  { id: 'p9', label: 'P9', x: 454, y: 158 },
  { id: 'p10', label: 'P10', x: 244, y: 244 },
  { id: 'p12', label: 'P12', x: 352, y: 244 },
  { id: 'p17', label: 'P17', x: 454, y: 260 },
  { id: 'p32', label: 'P32', x: 298, y: 332 },
  { id: 'p38', label: 'P38', x: 406, y: 332 }
]

const noisyEdges = [
  { id: 1, path: 'M180 150 C248 142 316 138 384 138' },
  { id: 2, path: 'M180 150 C250 164 316 184 384 190' },
  { id: 3, path: 'M180 224 C250 224 316 236 384 242' },
  { id: 4, path: 'M180 298 C250 292 316 288 384 294' },
  { id: 5, path: 'M180 224 C250 260 316 330 384 346' }
]

const weakEdges = [
  { id: 1, path: 'M456 138 C530 146 582 178 618 216' },
  { id: 2, path: 'M456 346 C532 318 586 266 618 216' }
]

const cleanEdges = [
  { id: 1, path: 'M279 142 C420 146 526 196 612 230' },
  { id: 2, path: 'M387 142 C486 154 558 204 612 230' },
  { id: 3, path: 'M489 158 C548 176 586 210 612 230' },
  { id: 4, path: 'M279 244 C420 242 522 232 612 230' },
  { id: 5, path: 'M387 244 C488 244 560 236 612 230' },
  { id: 6, path: 'M489 260 C552 258 588 240 612 230' },
  { id: 7, path: 'M333 332 C456 314 548 262 612 230' },
  { id: 8, path: 'M441 332 C520 306 586 254 612 230' }
]
</script>

<style scoped>
.network-panel {
  overflow: hidden;
}

.network-legend {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 14px;
  flex-wrap: wrap;
  color: var(--subtle);
  font-size: 0.78rem;
  font-weight: 800;
}

.network-legend span {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  white-space: nowrap;
}

.legend-dot {
  width: 10px;
  height: 10px;
  border-radius: 999px;
}

.legend-dot.is-public { background: #df6a6a; }
.legend-dot.is-core { background: #f0b44c; }
.legend-dot.is-person { background: #39a97d; }

.network-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 18px;
}

.network-card {
  display: flex;
  flex-direction: column;
  gap: 14px;
  padding: 18px;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background:
    radial-gradient(circle at 88% 14%, rgba(47, 125, 246, 0.08), transparent 28%),
    linear-gradient(180deg, rgba(255, 255, 255, 0.96), rgba(247, 251, 255, 0.86));
  box-shadow: var(--shadow-soft);
}

.network-card.is-after {
  background:
    radial-gradient(circle at 80% 18%, rgba(240, 180, 76, 0.16), transparent 34%),
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
  margin-top: 6px;
  font-size: 1rem;
  line-height: 1.45;
}

.network-svg {
  display: block;
  width: 100%;
  min-height: 360px;
  border: 1px solid rgba(53, 89, 138, 0.08);
  border-radius: 18px;
  background:
    linear-gradient(rgba(47, 125, 246, 0.045) 1px, transparent 1px),
    linear-gradient(90deg, rgba(47, 125, 246, 0.045) 1px, transparent 1px),
    linear-gradient(180deg, #ffffff, #f8fbff);
  background-size: 100% 48px, 48px 100%, 100% 100%;
}

.zone rect {
  fill: rgba(47, 125, 246, 0.035);
  stroke: rgba(47, 125, 246, 0.1);
  stroke-width: 1.2;
  stroke-dasharray: 8 8;
}

.zone text {
  fill: var(--subtle);
  font-size: 0.78rem;
  font-weight: 900;
  letter-spacing: 0.06em;
}

.is-public-zone rect {
  fill: rgba(223, 106, 106, 0.045);
  stroke: rgba(223, 106, 106, 0.14);
}

.is-core-zone rect {
  fill: rgba(240, 180, 76, 0.065);
  stroke: rgba(240, 180, 76, 0.24);
}

.edge {
  fill: none;
  stroke-linecap: round;
}

.edge.is-noise {
  stroke: rgba(162, 94, 78, 0.34);
  stroke-width: 2.4;
}

.edge.is-weak,
.edge.is-muted {
  stroke: rgba(120, 144, 171, 0.36);
  stroke-width: 2;
  stroke-dasharray: 5 5;
}

.edge.is-main {
  stroke: rgba(240, 180, 76, 0.78);
  stroke-width: 4.2;
}

.person-node {
  fill: rgba(238, 247, 242, 0.98);
  stroke: rgba(57, 169, 125, 0.46);
  stroke-width: 1.6;
}

.person-node.is-noise-person {
  fill: rgba(247, 221, 214, 0.92);
  stroke: rgba(223, 106, 106, 0.44);
}

.person-node.is-core {
  fill: rgba(255, 245, 220, 0.98);
  stroke: rgba(240, 180, 76, 0.8);
  stroke-width: 2;
}

.item-node {
  stroke-width: 2.2;
}

.item-node.is-public-node {
  fill: rgba(247, 221, 214, 0.9);
  stroke: rgba(162, 94, 78, 0.45);
}

.item-node.is-main-node {
  fill: rgba(255, 238, 196, 0.98);
  stroke: #f0b44c;
  stroke-width: 3;
}

.item-node.is-muted-node {
  fill: rgba(229, 236, 246, 0.92);
  stroke: rgba(120, 144, 171, 0.5);
}

.item-node.is-totem-node {
  fill: url(#yellow-bag-fill);
  stroke: #f0b44c;
  stroke-width: 3;
}

text {
  fill: var(--text);
  font-size: 0.82rem;
  font-weight: 900;
  pointer-events: none;
}

text.is-long-label {
  font-size: 0.76rem;
}

.network-caption {
  display: flex;
  gap: 8px;
  align-items: flex-start;
  padding: 12px 14px;
  border: 1px solid rgba(223, 106, 106, 0.18);
  border-radius: var(--radius-sm);
  color: var(--muted);
  background: rgba(223, 106, 106, 0.06);
  line-height: 1.6;
}

.network-caption strong {
  color: #b44e4e;
  white-space: nowrap;
}

.network-caption.is-success {
  border-color: rgba(57, 169, 125, 0.2);
  background: rgba(57, 169, 125, 0.08);
}

.network-caption.is-success strong {
  color: #25795a;
}
</style>
