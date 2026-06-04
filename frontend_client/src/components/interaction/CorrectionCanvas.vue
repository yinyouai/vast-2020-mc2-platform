<template>
  <div class="panel correction-panel">
    <div class="panel-header">
      <div>
        <h4 class="panel-title">证据复核画布</h4>
        <p class="panel-subtitle">当前目标 {{ store.selectedPersonId }}，人工标签：{{ evidence.humanLabel }}</p>
      </div>
      <span :class="['risk-pill', isCoreSuspect ? 'risk-high' : 'risk-low']">
        {{ isCoreSuspect ? '需重点复核' : '安全参照' }}
      </span>
    </div>

    <div class="canvas-layout">
      <div class="canvas-stage">
        <canvas ref="canvasRef" width="720" height="460" aria-label="证据画布"></canvas>
      </div>

      <div class="evidence-side">
        <div class="evidence-block">
          <span>机器预测</span>
          <strong>{{ evidence.machineLabel }}</strong>
          <p>置信度 {{ evidence.score }}%。低阈值时会显示为风险框，高阈值时仅保留人工确认信息。</p>
        </div>
        <div class="evidence-block">
          <span>文本语义</span>
          <blockquote>{{ evidence.caption }}</blockquote>
        </div>
        <div class="evidence-block">
          <span>复核判断</span>
          <p>{{ evidence.verdict }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, ref, watch } from 'vue'
import { useDashboardStore } from '../../store/dashboard'

const store = useDashboardStore()
const canvasRef = ref(null)

const isCoreSuspect = computed(() => store.hackerGroup.includes(store.selectedPersonId))

const evidence = computed(() => {
  const id = store.selectedPersonId || 'Person3'
  if (id === 'Person3') {
    return {
      machineLabel: 'red hat / low confidence',
      humanLabel: 'yellow connector bag',
      score: 42,
      caption: 'Secured the bright yellow bag at the venue entrance. It is the marker we agreed on.',
      verdict: '机器标签与文本语义冲突，人工复核后应锁定为黄色接头包暗号。',
      color: '#ff6b6b'
    }
  }
  if (id === 'Person27') {
    return {
      machineLabel: 'souvenir notebook',
      humanLabel: 'public conference item',
      score: 40,
      caption: 'This notebook is useful for taking notes during the talks.',
      verdict: '文本语义与会场普通物品一致，建议作为误报样本排除。',
      color: '#f4c95d'
    }
  }
  return {
    machineLabel: isCoreSuspect.value ? 'shared covert object' : 'public giveaway',
    humanLabel: isCoreSuspect.value ? 'yellow connector bag' : 'background item',
    score: isCoreSuspect.value ? 47 : 36,
    caption: isCoreSuspect.value
      ? `${id} mentions an offline marker without direct online coordination.`
      : `${id} only shows routine conference activity.`,
    verdict: isCoreSuspect.value
      ? '目标具备核心组物证特征，应继续送入后续聚类和社交隔离验证。'
      : '该目标更接近正常参会者，保留为背景基线。',
    color: isCoreSuspect.value ? '#ff6b6b' : '#6ee7a8'
  }
})

const draw = () => {
  const canvas = canvasRef.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')
  ctx.clearRect(0, 0, canvas.width, canvas.height)

  const gradient = ctx.createLinearGradient(0, 0, canvas.width, canvas.height)
  gradient.addColorStop(0, '#10252a')
  gradient.addColorStop(1, '#071013')
  ctx.fillStyle = gradient
  ctx.fillRect(0, 0, canvas.width, canvas.height)

  ctx.strokeStyle = 'rgba(184, 211, 214, 0.12)'
  for (let x = 40; x < canvas.width; x += 40) {
    ctx.beginPath()
    ctx.moveTo(x, 0)
    ctx.lineTo(x, canvas.height)
    ctx.stroke()
  }
  for (let y = 40; y < canvas.height; y += 40) {
    ctx.beginPath()
    ctx.moveTo(0, y)
    ctx.lineTo(canvas.width, y)
    ctx.stroke()
  }

  ctx.fillStyle = '#edf7f6'
  ctx.font = '700 16px Inter, sans-serif'
  ctx.fillText(`${store.selectedPersonId} / Evidence frame`, 28, 34)

  const box = { x: 155, y: 118, w: 355, h: 210 }
  if (store.scoreThreshold <= 0.45) {
    ctx.setLineDash([8, 8])
    ctx.strokeStyle = evidence.value.color
    ctx.lineWidth = 4
    ctx.strokeRect(box.x, box.y, box.w, box.h)
    ctx.setLineDash([])
    ctx.fillStyle = 'rgba(255,107,107,0.12)'
    ctx.fillRect(box.x, box.y, box.w, box.h)
  } else {
    ctx.strokeStyle = '#6ee7a8'
    ctx.lineWidth = 3
    ctx.strokeRect(box.x, box.y, box.w, box.h)
    ctx.fillStyle = 'rgba(110,231,168,0.10)'
    ctx.fillRect(box.x, box.y, box.w, box.h)
  }

  ctx.fillStyle = '#edf7f6'
  ctx.font = '700 14px Inter, sans-serif'
  ctx.fillText(evidence.value.humanLabel, box.x + 16, box.y + 30)
  ctx.fillStyle = '#9bb3b6'
  ctx.font = '13px Inter, sans-serif'
  ctx.fillText(`Machine: ${evidence.value.machineLabel}`, box.x + 16, box.y + 54)
}

watch(() => [store.selectedPersonId, store.scoreThreshold], draw)
onMounted(draw)
</script>

<style scoped>
.correction-panel {
  min-height: 0;
}

.canvas-layout {
  display: grid;
  grid-template-columns: minmax(0, 1.35fr) minmax(280px, 0.8fr);
  gap: 18px;
}

.canvas-stage {
  display: grid;
  place-items: center;
  overflow: hidden;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: #05090b;
}

canvas {
  width: 100%;
  max-width: 720px;
  height: auto;
  display: block;
}

.evidence-side {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.evidence-block {
  padding: 14px;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: rgba(255, 255, 255, 0.035);
}

.evidence-block span {
  display: block;
  margin-bottom: 8px;
  color: var(--subtle);
  font-size: 0.78rem;
  font-weight: 800;
  text-transform: uppercase;
}

.evidence-block strong {
  display: block;
  margin-bottom: 8px;
}

.evidence-block p,
blockquote {
  margin: 0;
  color: var(--muted);
  line-height: 1.55;
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
