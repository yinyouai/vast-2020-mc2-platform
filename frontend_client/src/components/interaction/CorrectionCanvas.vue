<template>
  <div class="panel correction-panel">
    <div class="panel-header">
      <div>
        <h4 class="panel-title">证据复核画布</h4>
        <p class="panel-subtitle">当前对象：{{ caseItem.id }}；人工修正：{{ caseItem.humanLabel }}</p>
      </div>
      <span :class="['risk-pill', caseItem.risk === 'high' ? 'risk-high' : 'risk-low']">
        {{ statusLabel }}
      </span>
    </div>

    <div class="canvas-layout">
      <div class="canvas-stage">
        <img
          :key="imageUrl"
          :src="imageUrl"
          :alt="`${caseItem.id} 复核证据图`"
          :class="{ 'is-loaded': imageState === 'loaded', 'is-failed': imageState === 'failed' }"
          @load="imageState = 'loaded'"
          @error="imageState = 'failed'"
        />
        <canvas ref="canvasRef" width="720" height="460" aria-label="证据复核画布"></canvas>
        <strong v-if="imageState === 'loading'" class="canvas-image-state">加载 {{ caseItem.id }} 图片</strong>
        <strong v-else-if="imageState === 'failed'" class="canvas-image-state is-failed">图片未就绪，已保留标注画布</strong>
      </div>

      <div class="evidence-side">
        <article class="evidence-block">
          <span>机器预测</span>
          <strong>{{ caseItem.machineLabel }}</strong>
          <small>冲突强度 {{ conflictPercent }}%</small>
        </article>
        <article class="evidence-block">
          <span>文本语义</span>
          <blockquote>{{ caseItem.textComment || caseItem.caption }}</blockquote>
        </article>
        <TextSemanticAnalysis :case-item="caseItem" />
        <article class="evidence-block">
          <span>人工判定</span>
          <p>{{ caseItem.verdict }}</p>
        </article>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, nextTick, onMounted, ref, watch } from 'vue'
import TextSemanticAnalysis from './TextSemanticAnalysis.vue'

const props = defineProps({
  caseItem: {
    type: Object,
    required: true
  }
})

const canvasRef = ref(null)
const imageState = ref('loading')
const conflictPercent = computed(() => Math.round((props.caseItem.conflictScore || 0) * 100))
const imageUrl = computed(
  () => `http://localhost:5000/static/MC2-Image-Data/${props.caseItem.id}/${props.caseItem.id}_1.jpg`
)
const statusLabel = computed(() => {
  if (props.caseItem.status === 'confirmed') return '已确认'
  if (props.caseItem.status === 'corrected') return '已修正'
  return '未复核'
})

const draw = () => {
  const canvas = canvasRef.value
  if (!canvas || !props.caseItem) return
  const ctx = canvas.getContext('2d')
  const item = props.caseItem
  const accent = item.risk === 'high' ? '#df6a6a' : '#39a97d'

  ctx.clearRect(0, 0, canvas.width, canvas.height)

  if (imageState.value === 'failed') {
    const gradient = ctx.createLinearGradient(0, 0, canvas.width, canvas.height)
    gradient.addColorStop(0, '#f5f9ff')
    gradient.addColorStop(1, '#eaf1fb')
    ctx.fillStyle = gradient
    ctx.fillRect(0, 0, canvas.width, canvas.height)

    ctx.fillStyle = 'rgba(47, 125, 246, 0.06)'
    for (let x = 0; x < canvas.width; x += 48) ctx.fillRect(x, 0, 1, canvas.height)
    for (let y = 0; y < canvas.height; y += 48) ctx.fillRect(0, y, canvas.width, 1)
  }

  ctx.fillStyle = '#17324d'
  ctx.font = '700 18px Microsoft YaHei UI, sans-serif'
  ctx.fillText(`${item.id} / 图文冲突复核`, 28, 38)
  ctx.fillStyle = '#56708f'
  ctx.font = '13px Microsoft YaHei UI, sans-serif'
  ctx.fillText(`队列 ${item.rank} · ${item.note} · 冲突强度 ${conflictPercent.value}%`, 28, 62)

  const box = { x: 142, y: 128, w: 372, h: 208 }
  ctx.save()
  ctx.shadowBlur = 24
  ctx.shadowColor = `${accent}55`
  ctx.setLineDash(item.status === 'unreviewed' ? [10, 8] : [])
  ctx.strokeStyle = accent
  ctx.lineWidth = 4
  ctx.strokeRect(box.x, box.y, box.w, box.h)
  ctx.restore()

  ctx.fillStyle = item.status === 'unreviewed' ? 'rgba(223,106,106,0.10)' : 'rgba(57,169,125,0.10)'
  ctx.fillRect(box.x, box.y, box.w, box.h)

  ctx.fillStyle = '#17324d'
  ctx.font = '700 15px Microsoft YaHei UI, sans-serif'
  ctx.fillText(item.humanLabel, box.x + 18, box.y + 34)
  ctx.fillStyle = '#56708f'
  ctx.font = '13px Microsoft YaHei UI, sans-serif'
  ctx.fillText(`机器标签：${item.machineLabel}`, box.x + 18, box.y + 62)
  ctx.fillText(`人工结论：${statusLabel.value}`, box.x + 18, box.y + 88)

  ctx.fillStyle = 'rgba(240, 180, 76, 0.16)'
  ctx.fillRect(548, 112, 126, 76)
  ctx.strokeStyle = 'rgba(240, 180, 76, 0.48)'
  ctx.lineWidth = 1.5
  ctx.strokeRect(548, 112, 126, 76)
  ctx.fillStyle = '#a56e1d'
  ctx.font = '700 12px Microsoft YaHei UI, sans-serif'
  ctx.fillText('复核状态', 562, 140)
  ctx.fillStyle = '#17324d'
  ctx.font = '12px Microsoft YaHei UI, sans-serif'
  ctx.fillText(statusLabel.value, 562, 164)
}

watch(
  () => props.caseItem,
  () => nextTick(draw),
  { deep: true }
)
watch(
  () => props.caseItem.id,
  () => {
    imageState.value = 'loading'
  }
)
watch(imageState, () => nextTick(draw))
onMounted(draw)
</script>

<style scoped>
.correction-panel {
  min-height: 0;
  align-self: start;
}

.canvas-layout {
  display: grid;
  grid-template-columns: minmax(0, 1.25fr) minmax(250px, 0.82fr);
  gap: 14px;
  align-items: start;
}

.canvas-stage {
  position: relative;
  display: block;
  overflow: hidden;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background:
    linear-gradient(rgba(47, 125, 246, 0.06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(47, 125, 246, 0.06) 1px, transparent 1px),
    #f9fbff;
  background-size: 48px 48px, 48px 48px, 100% 100%;
  aspect-ratio: 720 / 460;
}

.canvas-stage > img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0;
  transition: opacity var(--motion-medium) ease;
}

.canvas-stage > img.is-loaded {
  opacity: 1;
}

.canvas-stage > img.is-failed {
  display: none;
}

canvas {
  position: relative;
  z-index: 2;
  display: block;
  width: 100%;
  max-width: 720px;
  height: auto;
}

.canvas-image-state {
  position: absolute;
  left: 50%;
  top: 50%;
  z-index: 3;
  transform: translate(-50%, -50%);
  display: inline-flex;
  align-items: center;
  min-height: 34px;
  padding: 0 14px;
  border: 1px solid var(--border);
  border-radius: 999px;
  color: var(--muted);
  background: rgba(255, 255, 255, 0.9);
  box-shadow: var(--shadow-soft);
  font-size: 0.82rem;
}

.canvas-image-state.is-failed {
  color: #9a6818;
  border-color: rgba(240, 180, 76, 0.28);
  background: rgba(255, 247, 219, 0.92);
}

.evidence-side {
  display: grid;
  grid-template-columns: 1fr;
  gap: 10px;
}

.evidence-block {
  padding: 12px;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  background: rgba(255, 255, 255, 0.86);
}

.evidence-block span {
  display: block;
  margin-bottom: 8px;
  color: var(--subtle);
  font-size: 0.78rem;
  font-weight: 900;
  letter-spacing: 0.08em;
}

.evidence-block strong {
  display: block;
  margin-bottom: 8px;
}

.evidence-block small {
  color: var(--muted);
  font-weight: 800;
}

.evidence-block p,
blockquote {
  display: block !important;
  margin: 0;
  color: var(--muted);
  line-height: 1.7;
}

blockquote {
  padding-left: 12px;
  border-left: 3px solid var(--accent);
}

@media (max-width: 1180px) {
  .canvas-layout {
    grid-template-columns: 1fr;
  }
}
</style>
