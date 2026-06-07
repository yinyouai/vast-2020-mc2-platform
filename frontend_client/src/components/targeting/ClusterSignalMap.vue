<template>
  <section class="panel signal-map-panel">
    <div class="panel-header">
      <div>
        <span class="section-kicker">候选结构空间</span>
        <h4 class="panel-title">人数与稳定性分布</h4>
        <p class="visible-subtitle">
          越接近 8 人且越靠上，越符合稳定暗号物品特征；圆点大小只表示可追溯的人工核验图片。
        </p>
      </div>
      <div class="legend" aria-label="图表图例">
        <span><i class="legend-dot exact"></i>恰好 8 人</span>
        <span><i class="legend-dot winner"></i>当前结论</span>
      </div>
    </div>

    <div class="plot-shell">
      <svg
        class="distribution-plot"
        viewBox="0 0 720 390"
        role="img"
        aria-labelledby="distribution-title distribution-description"
      >
        <title id="distribution-title">候选物品人数与稳定率分布</title>
        <desc id="distribution-description">横轴为拥有者人数，纵轴为稳定率，圆点越大代表人工核验图片越多。</desc>

        <rect x="86" y="28" width="586" height="286" rx="10" class="plot-background" />
        <rect :x="xPosition(8) - 52" y="28" width="104" height="286" rx="8" class="target-band" />

        <g v-for="tick in stabilityTicks" :key="`y-${tick}`">
          <line x1="86" x2="672" :y1="yPosition(tick)" :y2="yPosition(tick)" class="grid-line" />
          <text x="72" :y="yPosition(tick) + 4" text-anchor="end" class="axis-label">{{ Math.round(tick * 100) }}%</text>
        </g>

        <g v-for="count in ownerTicks" :key="`x-${count}`">
          <line :x1="xPosition(count)" :x2="xPosition(count)" y1="28" y2="314" class="grid-line vertical" />
          <text :x="xPosition(count)" y="338" text-anchor="middle" class="axis-label">{{ count }} 人</text>
        </g>

        <text x="379" y="374" text-anchor="middle" class="axis-title">拥有者人数</text>
        <text transform="translate(20 172) rotate(-90)" text-anchor="middle" class="axis-title">稳定拥有比例</text>
        <text :x="xPosition(8)" y="48" text-anchor="middle" class="target-label">目标人数 8</text>

        <g
          v-for="point in plotPoints"
          :key="point.label"
          :class="[
            'candidate-point',
            point.exact_target_size && 'is-exact',
            point.label === store.activeTotem && 'is-winner',
            point.label === store.selectedCandidateLabel && 'is-selected'
          ]"
          role="button"
          tabindex="0"
          :aria-label="`${point.label}，${point.owner_count} 人，稳定率 ${Math.round(point.stable_owner_ratio * 100)}%`"
          @click="selectCandidate(point)"
          @keydown.enter.prevent="selectCandidate(point)"
          @keydown.space.prevent="selectCandidate(point)"
        >
          <circle
            :cx="point.plotX"
            :cy="point.plotY"
            :r="point.radius + 7"
            class="point-hit-area"
          />
          <circle :cx="point.plotX" :cy="point.plotY" :r="point.radius" class="point-circle" />
          <text
            :x="point.plotX"
            :y="point.plotY - point.radius - 9"
            text-anchor="middle"
            class="point-label"
          >{{ point.label }}</text>
        </g>
      </svg>
    </div>

    <div class="candidate-index" aria-label="候选物品索引">
      <button
        v-for="candidate in store.candidateRankings"
        :key="candidate.label"
        type="button"
        :class="{ active: candidate.label === store.selectedCandidateLabel }"
        @click="selectCandidate(candidate)"
      >
        <i :class="{ winner: candidate.label === store.activeTotem }"></i>
        {{ candidate.label }}
      </button>
    </div>

    <div v-if="selectedCandidate" class="selected-candidate" role="status">
      <div class="selected-main">
        <span>当前联动候选</span>
        <strong>{{ selectedCandidate.label }}</strong>
      </div>
      <div><span>拥有者</span><strong>{{ selectedCandidate.owner_count }} 人</strong></div>
      <div><span>稳定率</span><strong>{{ Math.round(selectedCandidate.stable_owner_ratio * 100) }}%</strong></div>
      <div><span>人工核验</span><strong>{{ selectedCandidate.verified_image_count }} 张</strong></div>
      <div><span>模型命中</span><strong>{{ selectedCandidate.raw_detection_image_count }} 张</strong></div>
    </div>
  </section>
</template>

<script setup>
import { computed } from 'vue'
import { useDashboardStore } from '../../store/dashboard'

const store = useDashboardStore()
const ownerTicks = [8, 9, 10]
const stabilityTicks = [0, 0.25, 0.5, 0.75, 1]

const xPosition = (ownerCount) => 142 + (ownerCount - 8) * 238
const yPosition = (stability) => 296 - stability * 238

const selectedCandidate = computed(() =>
  store.candidateRankings.find((item) => item.label === store.selectedCandidateLabel)
  || store.candidateRankings[0]
  || null
)

const plotPoints = computed(() => {
  const collisionGroups = new Map()
  store.candidateRankings.forEach((item) => {
    const key = `${item.owner_count}:${item.stable_owner_ratio}`
    if (!collisionGroups.has(key)) collisionGroups.set(key, [])
    collisionGroups.get(key).push(item)
  })

  return store.candidateRankings.map((item) => {
    const group = collisionGroups.get(`${item.owner_count}:${item.stable_owner_ratio}`)
    const index = group.findIndex((candidate) => candidate.label === item.label)
    const centeredIndex = index - (group.length - 1) / 2
    const radius = Math.max(10, Math.min(24, 10 + Math.sqrt(item.verified_image_count) * 2.7))
    return {
      ...item,
      plotX: xPosition(item.owner_count) + centeredIndex * 34,
      plotY: yPosition(item.stable_owner_ratio) + (index % 2 ? 8 : -8),
      radius
    }
  })
})

const selectCandidate = (candidate) => {
  store.selectCandidate(candidate.label)
}
</script>

<style scoped>
.signal-map-panel{min-width:0;overflow:hidden}.signal-map-panel .panel-header{align-items:flex-start;flex-wrap:wrap}.signal-map-panel .panel-header>div:first-child{min-width:240px;flex:1}
.section-kicker{color:var(--subtle);font-size:.7rem;font-weight:800}.visible-subtitle{display:block!important;max-width:620px;margin:5px 0 0;color:var(--muted);font-size:.76rem;line-height:1.55}
.legend{display:flex;flex-wrap:wrap;gap:12px;color:var(--muted);font-size:.68rem;font-weight:800}.legend span{display:flex;align-items:center;gap:6px}.legend-dot{width:9px;height:9px;border-radius:50%;background:#dbe6f2}.legend-dot.exact{background:#2f7df6}.legend-dot.winner{background:#d99522}
.plot-shell{width:100%;overflow-x:auto;border:1px solid var(--border);border-radius:9px;background:#f9fbfd}.distribution-plot{display:block;width:100%;min-width:590px;height:auto;min-height:320px}.plot-background{fill:#fff}.target-band{fill:rgba(47,125,246,.06);stroke:rgba(47,125,246,.16);stroke-dasharray:5 5}.grid-line{stroke:rgba(53,89,138,.12);stroke-dasharray:4 5}.grid-line.vertical{stroke-dasharray:2 6}.axis-label{fill:#7890ab;font-size:11px;font-weight:700}.axis-title{fill:#56708f;font-size:12px;font-weight:800}.target-label{fill:#2f7df6;font-size:10px;font-weight:900}
.candidate-point{cursor:pointer;outline:none}.point-hit-area{fill:transparent}.point-circle{fill:#35a8c8;stroke:#fff;stroke-width:3;filter:drop-shadow(0 5px 7px rgba(48,78,114,.18));transition:fill 160ms ease,stroke 160ms ease,transform 160ms ease;transform-box:fill-box;transform-origin:center}.candidate-point.is-exact .point-circle{fill:#2f7df6}.candidate-point.is-winner .point-circle{fill:#d99522}.candidate-point.is-selected .point-circle{stroke:#17324d;stroke-width:4;transform:scale(1.12)}.candidate-point:hover .point-circle,.candidate-point:focus-visible .point-circle{stroke:#17324d;transform:scale(1.12)}.point-label{fill:#17324d;font-size:10px;font-weight:900;opacity:0;pointer-events:none}.candidate-point:hover .point-label,.candidate-point:focus-visible .point-label,.candidate-point.is-selected .point-label,.candidate-point.is-winner .point-label{opacity:1}
.candidate-index{display:flex;flex-wrap:wrap;gap:6px;margin-top:10px}.candidate-index button{display:inline-flex;align-items:center;gap:6px;min-height:34px;padding:0 9px;border:1px solid var(--border);border-radius:6px;color:var(--muted);background:#fff;font-size:.67rem;font-weight:800}.candidate-index button:hover,.candidate-index button:focus-visible,.candidate-index button.active{border-color:var(--accent);color:var(--accent);background:#f2f7ff}.candidate-index i{width:7px;height:7px;border-radius:50%;background:#35a8c8}.candidate-index i.winner{background:#d99522}
.selected-candidate{display:grid;grid-template-columns:1.4fr repeat(3,1fr);gap:8px;margin-top:12px}.selected-candidate>div{min-width:0;padding:10px 11px;border:1px solid var(--border);border-radius:7px;background:#f7f9fc}.selected-candidate span,.selected-candidate strong{display:block}.selected-candidate span{color:var(--subtle);font-size:.64rem;font-weight:800}.selected-candidate strong{overflow:hidden;margin-top:5px;font-size:.8rem;text-overflow:ellipsis;white-space:nowrap}.selected-main{border-color:rgba(47,125,246,.22)!important;background:#f2f7ff!important}.selected-main strong{color:var(--accent)}
@media(max-width:760px){.distribution-plot{width:590px}.selected-candidate{grid-template-columns:repeat(2,1fr)}.selected-main{grid-column:1/-1}}
@media(prefers-reduced-motion:reduce){.point-circle{transition:none}}
</style>
