<template>
  <div class="panel correction-panel">
    <div class="panel-header">
      <div>
        <h4 class="panel-title">证据复核画布</h4>
        <p class="panel-subtitle">当前对象：{{ store.selectedPersonId }}。人工修正标签：{{ evidence.humanLabel }}</p>
      </div>
      <span :class="['risk-pill', isCoreSuspect ? 'risk-high' : 'risk-low']">
        {{ isCoreSuspect ? '重点复核' : '背景参考' }}
      </span>
    </div>

    <div class="canvas-layout">
      <div class="canvas-stage">
        <canvas ref="canvasRef" width="720" height="460" aria-label="证据复核画布"></canvas>
      </div>

      <div class="evidence-side">
        <div class="evidence-block">
          <span>机器预测</span>
          <strong>{{ evidence.machineLabel }}</strong>
          <p>当前置信度 {{ evidence.score }}%。阈值较低时会保留更多可疑框，阈值提高后则更强调稳定候选。</p>
        </div>
        <div class="evidence-block">
          <span>文本语义</span>
          <blockquote>{{ evidence.caption }}</blockquote>
        </div>
        <div class="evidence-block">
          <span>人工判定</span>
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
      machineLabel: '红帽 / 低置信度',
      humanLabel: '黄色提袋',
      score: 42,
      caption: '在会场入口拿到了明亮的黄色提袋，那是我们约定好的识别标记。',
      verdict: '机器标签与文本叙事存在明显冲突，人工复核后应将该样本修正为“黄色提袋”线索。',
      color: '#df6a6a'
    }
  }
  if (id === 'Person27') {
    return {
      machineLabel: '纪念笔记本',
      humanLabel: '公共会场物品',
      score: 40,
      caption: '这个笔记本适合在会场记录讲座内容。',
      verdict: '文本语义与普通会场资产一致，因此更适合作为误报剔除样本，而非核心嫌疑证据。',
      color: '#f0b44c'
    }
  }
  return {
    machineLabel: isCoreSuspect.value ? '共享暗号物品' : '普通会场礼品',
    humanLabel: isCoreSuspect.value ? '黄色提袋' : '背景物品',
    score: isCoreSuspect.value ? 47 : 36,
    caption: isCoreSuspect.value
      ? `${id} 在文本中提到了线下识别标记，但没有表现出明显公开协作。`
      : `${id} 的文本内容更接近日常会场活动。`,
    verdict: isCoreSuspect.value
      ? '该对象具备核心组物证特征，应继续送入聚类层和社交隔离层验证。'
      : '该对象更像普通参会者，适合作为背景基线保留。'
      ,
    color: isCoreSuspect.value ? '#df6a6a' : '#39a97d'
  }
})

const draw = () => {
  const canvas = canvasRef.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')
  ctx.clearRect(0, 0, canvas.width, canvas.height)

  const gradient = ctx.createLinearGradient(0, 0, canvas.width, canvas.height)
  gradient.addColorStop(0, '#f5f9ff')
  gradient.addColorStop(1, '#eaf1fb')
  ctx.fillStyle = gradient
  ctx.fillRect(0, 0, canvas.width, canvas.height)

  ctx.fillStyle = 'rgba(47, 125, 246, 0.06)'
  for (let x = 0; x < canvas.width; x += 48) {
    ctx.fillRect(x, 0, 1, canvas.height)
  }
  for (let y = 0; y < canvas.height; y += 48) {
    ctx.fillRect(0, y, canvas.width, 1)
  }

  ctx.fillStyle = '#17324d'
  ctx.font = '700 16px Microsoft YaHei UI, sans-serif'
  ctx.fillText(`${store.selectedPersonId} / 复核画面`, 28, 34)
  ctx.fillStyle = '#56708f'
  ctx.font = '12px Microsoft YaHei UI, sans-serif'
  ctx.fillText('将机器框选结果与文本叙事进行交叉校验。', 28, 54)

  const box = { x: 155, y: 118, w: 355, h: 210 }
  const highlighted = store.scoreThreshold <= 0.45
  ctx.save()
  ctx.shadowBlur = 24
  ctx.shadowColor = `${evidence.value.color}55`
  ctx.setLineDash(highlighted ? [10, 8] : [])
  ctx.strokeStyle = highlighted ? evidence.value.color : '#39a97d'
  ctx.lineWidth = 4
  ctx.strokeRect(box.x, box.y, box.w, box.h)
  ctx.restore()
  ctx.setLineDash([])

  ctx.fillStyle = highlighted ? 'rgba(223,106,106,0.10)' : 'rgba(57,169,125,0.1)'
  ctx.fillRect(box.x, box.y, box.w, box.h)

  ctx.fillStyle = '#17324d'
  ctx.font = '700 14px Microsoft YaHei UI, sans-serif'
  ctx.fillText(evidence.value.humanLabel, box.x + 16, box.y + 30)
  ctx.fillStyle = '#56708f'
  ctx.font = '13px Microsoft YaHei UI, sans-serif'
  ctx.fillText(`机器标签：${evidence.value.machineLabel}`, box.x + 16, box.y + 54)
  ctx.fillText(`当前分值：${evidence.value.score}%`, box.x + 16, box.y + 76)

  ctx.fillStyle = 'rgba(240, 180, 76, 0.16)'
  ctx.fillRect(540, 96, 126, 72)
  ctx.strokeStyle = 'rgba(240, 180, 76, 0.5)'
  ctx.lineWidth = 1.5
  ctx.strokeRect(540, 96, 126, 72)
  ctx.fillStyle = '#a56e1d'
  ctx.font = '700 12px Microsoft YaHei UI, sans-serif'
  ctx.fillText('人工校正', 554, 122)
  ctx.fillStyle = '#17324d'
  ctx.font = '12px Microsoft YaHei UI, sans-serif'
  ctx.fillText('当前线索状态：', 554, 144)
  ctx.fillText(highlighted ? '仍需进一步确认' : '已较为稳定', 554, 160)
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
  background: #f9fbff;
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
  border-radius: var(--radius-sm);
  background: rgba(255, 255, 255, 0.86);
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
