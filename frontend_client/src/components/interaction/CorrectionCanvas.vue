<template>
  <div class="glass-card canvas-wrapper">
    <div class="canvas-top">
      <h4 class="舱室标题">🔍 多模态证据交叉比对与人类真值校准画布</h4>
      <span class="status-pill" :class="isHacker ? 'pill-danger' : 'pill-safe'">
        {{ isHacker ? '🚨 高度特征冲突' : '🔒 风险表现平稳' }}
      </span>
    </div>

    <div class="canvas-grid">
      <!-- Canvas 视口 -->
      <div class="canvas-viewport">
        <div class="canvas-relative">
          <canvas
            ref="canvasRef"
            @dblclick="executeHumanCorrection"
            @mousemove="trackMouseRadar"
          ></canvas>
          <div
            v-if="hud.show"
            class="canvas-hud"
            :style="{ left: hud.x + 'px', top: hud.y + 'px' }"
          >
            <div class="hud-title">📡 像素级特征审查</div>
            <div class="hud-row">坐标: X:{{ box.bx }}, Y:{{ box.by }}</div>
            <div class="hud-row">机器预测: <span class="text-danger">{{ box.machineLabel }}</span></div>
            <div class="hud-row">置信度: <span class="font-mono">{{ box.score }}%</span></div>
            <div class="hud-tip">💡 双击此区域可强制修改标签</div>
          </div>
        </div>
      </div>

      <!-- 右侧文本面板 -->
      <div class="canvas-text-panel">
        <div class="text-group">
          <h5>📄 嫌疑目标发帖主观配文</h5>
          <blockquote :class="isHacker ? 'quote-conflict' : 'quote-safe'">
            {{ box.caption }}
          </blockquote>
        </div>

        <div class="text-group">
          <h5>📡 画布特征框决策状态</h5>
          <div class="status-card" :class="store.scoreThreshold <= 0.45 ? 'status-err' : 'status-ok'">
            <span class="status-dot"></span>
            <p v-if="store.scoreThreshold <= 0.45">
              <strong>警告：</strong>当前对 <span class="text-purple">{{ store.selectedPersonId }}</span> 发生严重不确定性虚警！图像资产被归类为 {{ box.machineLabel }}。
            </p>
            <p v-else>
              <strong>通过：</strong>低置信度算法虚警已被滑块成功截断，当前资产已归入安全通过区。
            </p>
          </div>
        </div>

        <div class="text-group">
          <h5>🛠️ 多模态交叉取证日志</h5>
          <div class="log-box" v-if="isHacker">
            <div class="log-item log-error">❌ <b>模型噪声：</b>机器单凭像素表面特征，将接头暗号误判为 {{ box.machineLabel }}。</div>
            <div class="log-item log-success">🟩 <b>人类纠偏：</b>核对背景照片+配文，实锤判定该资产本质是 {{ box.humanLabel }}。</div>
          </div>
          <div class="log-box" v-else>
            <div class="log-item log-info">🟩 <b>噪声排除：</b>该成员所有资产均为会场普遍合法免费礼品。</div>
            <div class="log-item log-success">🔒 <b>审查通过：</b>网络交互关系链健康，已执行反向洗白。</div>
          </div>
        </div>

        <div class="truth-anchor">
          <span>🎯 NLP文本提取真实意图: <strong class="text-accent">{{ box.humanLabel }}</strong></span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted, watch, onUnmounted } from 'vue'
import { useDashboardStore } from '../../store/dashboard'
import { HACKER_LIST } from '../../constants/forensics'
import axios from 'axios'

const store = useDashboardStore()
const canvasRef = ref(null)
const hud = reactive({ show: false, x: 0, y: 0 })

const isHacker = computed(() => HACKER_LIST.includes(store.selectedPersonId || 'Person3'))

const box = computed(() => {
  const id = store.selectedPersonId || 'Person3'
  if (id === 'Person3') return {
    bx: 80, by: 70, bw: 260, bh: 160, score: '42.15',
    machineLabel: '【高危红哨子误报】', humanLabel: '【黄色接头提袋图腾】',
    caption: '"Excited to secure this customized bright yellow bag at the venue entrance. Very spacious."'
  }
  if (id === 'Person27') return {
    bx: 90, by: 60, bw: 240, bh: 170, score: '40.36',
    machineLabel: '【南瓜便签虚警】', humanLabel: '【笔记本资产】',
    caption: '"Love the neat grid structure of this notebook. Highly recommend for security coding!"'
  }
  const seed = parseInt(id.replace('Person', '')) * 3
  return {
    bx: 100 + (seed % 30), by: 80 + (seed % 20), bw: 220, bh: 150,
    score: (35 + (seed % 15)).toFixed(2),
    machineLabel: HACKER_LIST.includes(id) ? '【日常杂物误报】' : '【免费普及礼品】',
    humanLabel: HACKER_LIST.includes(id) ? '【黄色接头提袋图腾】' : '【会场通用礼品】',
    caption: HACKER_LIST.includes(id)
      ? `Discovered this covert marker in the meeting room. [取证焦点: ${id}]`
      : `Having an awesome tea break at the international cybersecurity union summit. [无害: ${id}]`
  }
})

function renderWorkspace() {
  const canvas = canvasRef.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')
  canvas.width = 460
  canvas.height = 320

  const imgId = store.selectedPersonId === 'Person27' ? '14' : '1'
  const filename = `${store.selectedPersonId || 'Person3'}_${imgId}.jpg`

  const bgImage = new Image()
  bgImage.src = `http://localhost:5000/static/MC2-Image-Data/${store.selectedPersonId || 'Person3'}/${filename}`

  bgImage.onload = () => {
    ctx.drawImage(bgImage, 0, 0, canvas.width, canvas.height)
    drawOverlay(ctx, canvas)
  }
  bgImage.onerror = () => {
    ctx.fillStyle = '#FAFBFC'
    ctx.fillRect(0, 0, canvas.width, canvas.height)
    drawOverlay(ctx, canvas)
  }
}

function drawOverlay(ctx, canvas) {
  ctx.fillStyle = 'rgba(0, 0, 0, 0.6)'
  ctx.font = 'bold 10px monospace'
  ctx.fillText('SAI 可视化取证情报 · 证据覆盖图层', 20, 22)

  const b = box.value
  if (store.scoreThreshold <= 0.45) {
    ctx.strokeStyle = isHacker.value ? '#FF5A5F' : '#636378'
    ctx.lineWidth = isHacker.value ? 3 : 1.5
    ctx.setLineDash([4, 4])
    ctx.strokeRect(b.bx, b.by, b.bw, b.bh)
    ctx.setLineDash([])
    ctx.fillStyle = isHacker.value ? '#FF5A5F' : '#636378'
    ctx.font = 'bold 11px monospace'
    ctx.fillText(`⚠️ ${isHacker.value ? '视觉虚警' : '背景资产'}: ${b.machineLabel}`, b.bx + 6, b.by + 16)
  } else {
    ctx.fillStyle = 'rgba(49, 194, 124, 0.15)'
    ctx.fillRect(b.bx, b.by, b.bw, b.bh)
    ctx.strokeStyle = '#31C27C'
    ctx.lineWidth = 2
    ctx.strokeRect(b.bx, b.by, b.bw, b.bh)
    ctx.fillStyle = '#31C27C'
    ctx.font = 'bold 11px monospace'
    ctx.fillText('🟩 算法缺陷已被滑块滤除通过', b.bx + 6, b.by + 16)
  }
}

function trackMouseRadar(e) {
  const b = box.value
  if (store.scoreThreshold > 0.45) { hud.show = false; return }
  const rect = e.target.getBoundingClientRect()
  const mx = e.clientX - rect.left
  const my = e.clientY - rect.top
  if (mx >= b.bx && mx <= b.bx + b.bw && my >= b.by && my <= b.by + b.bh) {
    hud.show = true
    hud.x = mx + 15
    hud.y = my + 15
  } else {
    hud.show = false
  }
}

async function executeHumanCorrection() {
  const label = prompt('🔧 人在回路取证干预：请输入经过你肉眼校准后的该资产真实分类标签:')
  if (!label) return
  try {
    const res = await axios.post('http://localhost:5000/api/update_label', {
      person_id: store.selectedPersonId,
      image_id: `${store.selectedPersonId}_1`,
      box_id: 0,
      action: 'modify',
      new_label: label
    })
    if (res.data.status === 'success') {
      alert('🎉 级联证词订正成功！真实意图已强行改写，聚类大厅已同步重算！')
      store.fetchHeatmapMatrix()
    }
  } catch (err) { console.error(err) }
}

watch(() => [store.selectedPersonId, store.scoreThreshold], renderWorkspace)
onMounted(renderWorkspace)
</script>

<style scoped>
.canvas-wrapper {
  display: flex;
  flex-direction: column;
  height: 100%;
}

.canvas-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.status-pill {
  font-size: var(--text-xs);
  font-weight: var(--weight-semibold);
  padding: 4px 10px;
  border-radius: var(--radius-full);
}

.pill-danger {
  background: var(--accent-danger-light);
  color: var(--accent-danger);
}
.pill-safe {
  background: rgba(0,0,0,0.03);
  color: var(--text-secondary);
}

.canvas-grid {
  display: grid;
  grid-template-columns: 1.3fr 1fr;
  gap: var(--space-lg);
  flex: 1;
  margin-top: var(--space-sm);
  min-height: 0;
}

.canvas-viewport {
  background: var(--bg-canvas);
  border-radius: var(--radius-sm);
  overflow: hidden;
  display: flex;
  justify-content: center;
  align-items: center;
  border: 1px solid rgba(0,0,0,0.04);
  position: relative;
}

.canvas-relative {
  position: relative;
  width: 460px;
  height: 320px;
}

canvas { display: block; }

.canvas-hud {
  position: absolute;
  pointer-events: none;
  background: rgba(255,255,255,0.95);
  backdrop-filter: blur(15px);
  border: 1px solid rgba(0,0,0,0.1);
  border-radius: var(--radius-sm);
  padding: var(--space-sm);
  display: flex;
  flex-direction: column;
  gap: 3px;
  box-shadow: var(--shadow-dropdown);
  z-index: 200;
  width: 220px;
  font-size: 10px;
}

.hud-title {
  font-size: 11px;
  font-weight: var(--weight-bold);
  color: var(--accent-purple);
  border-bottom: 1px solid rgba(0,0,0,0.05);
  padding-bottom: 4px;
}

.hud-row {
  color: var(--text-secondary);
  display: flex;
  justify-content: space-between;
}

.hud-tip {
  color: var(--accent-primary);
  font-size: 9px;
  border-top: 1px solid rgba(0,0,0,0.04);
  padding-top: 4px;
  margin-top: 2px;
}

.canvas-text-panel {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
  background: rgba(0,0,0,0.01);
  padding: var(--space-md);
  border-radius: var(--radius-sm);
  overflow-y: auto;
}

.text-group h5 {
  margin: 0 0 6px;
  font-size: var(--text-xs);
  color: var(--text-secondary);
  font-weight: var(--weight-medium);
}

blockquote {
  margin: 0;
  padding: var(--space-md);
  border-radius: var(--radius-sm);
  font-size: var(--text-xs);
  line-height: var(--leading-relaxed);
  font-style: italic;
}

.quote-conflict {
  border-left: 4px solid var(--accent-danger);
  background: rgba(255, 90, 95, 0.02);
  color: var(--text-primary);
}

.quote-safe {
  border-left: 4px solid var(--text-tertiary);
  background: rgba(0,0,0,0.02);
  color: var(--text-secondary);
}

.status-card {
  padding: var(--space-sm) var(--space-md);
  border-radius: var(--radius-sm);
  font-size: var(--text-xs);
  line-height: var(--leading-normal);
  display: flex;
  align-items: flex-start;
  gap: var(--space-sm);
}

.status-card p { margin: 0; }

.status-err {
  background: rgba(255, 90, 95, 0.04);
  border: 1px solid rgba(255, 90, 95, 0.1);
}

.status-ok {
  background: rgba(49, 194, 124, 0.04);
  border: 1px solid rgba(49, 194, 124, 0.1);
}

.status-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  margin-top: 4px;
  flex-shrink: 0;
}

.status-err .status-dot { background: var(--accent-danger); }
.status-ok .status-dot { background: var(--accent-primary); }

.log-item {
  font-size: var(--text-xs);
  line-height: var(--leading-normal);
  padding: 4px 8px;
  border-radius: 4px;
  margin-bottom: 4px;
}

.log-error { background: rgba(255,90,95,0.04); color: #FF453A; }
.log-info { background: rgba(0,0,0,0.02); color: var(--text-secondary); }
.log-success { background: rgba(49,194,124,0.04); color: var(--accent-primary-dark); }

.truth-anchor {
  font-size: var(--text-xs);
  color: var(--text-secondary);
  border-top: 1px solid rgba(0,0,0,0.04);
  padding-top: var(--space-sm);
  margin-top: auto;
}
</style>
