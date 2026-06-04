<template>
  <section class="panel process-panel">
    <div class="panel-header">
      <div>
        <h4 class="panel-title">标注前后对照</h4>
        <p class="panel-subtitle">不仅展示最终判断，还展示“模型最初看到了什么、人工最后保留了什么”，让汇报时能清楚讲过程。</p>
      </div>
    </div>

    <div class="cases-grid">
      <article v-for="scene in scenes" :key="scene.id" class="case-card">
        <div class="case-card__text">
          <span>{{ scene.title }}</span>
          <strong>{{ scene.summary }}</strong>
          <p>{{ scene.caption }}</p>
        </div>

        <div class="case-compare">
          <div class="case-view">
            <div class="case-view__title">标注前 / 机器预测</div>
            <div class="case-image" :class="{ 'is-placeholder': imageStates[scene.id] !== 'loaded' }">
              <img
                :src="scene.image"
                :alt="scene.title"
                :class="imageClass(scene.id)"
                loading="lazy"
                @load="markImageLoaded(scene.id)"
                @error="markImageFailed(scene.id)"
              />
              <div class="case-placeholder">
                <strong>{{ scene.placeholderTitle }}</strong>
                <p>{{ scene.placeholderText }}</p>
              </div>
              <span v-if="imageStates[scene.id] === 'loading'" class="case-image-state">加载中</span>
              <span v-else-if="imageStates[scene.id] === 'failed'" class="case-image-state is-failed">图像占位</span>

              <div
                v-for="box in scene.beforeBoxes"
                :key="`before-${box.label}`"
                class="overlay-box"
                :class="box.kind"
                :style="box.style"
              >
                <span class="overlay-box__label">{{ box.label }}</span>
              </div>
            </div>
          </div>

          <div class="case-view">
            <div class="case-view__title">标注后 / 人工修正</div>
            <div class="case-image" :class="{ 'is-placeholder': imageStates[scene.id] !== 'loaded' }">
              <img
                :src="scene.image"
                :alt="`${scene.title} 人工修正`"
                :class="imageClass(scene.id)"
                loading="lazy"
                @load="markImageLoaded(scene.id)"
                @error="markImageFailed(scene.id)"
              />
              <div class="case-placeholder is-clean">
                <strong>{{ scene.placeholderTitle }}</strong>
                <p>人工复核后仅保留主物证。</p>
              </div>

              <div
                v-for="box in scene.afterBoxes"
                :key="`after-${box.label}`"
                class="overlay-box"
                :class="box.kind"
                :style="box.style"
              >
                <span class="overlay-box__label">{{ box.label }}</span>
              </div>
            </div>
          </div>
        </div>

        <div class="case-log">
          <div class="case-log__item">
            <span>机器阶段</span>
            <p>{{ scene.machineNote }}</p>
          </div>
          <div class="case-log__item">
            <span>人工阶段</span>
            <p>{{ scene.humanNote }}</p>
          </div>
        </div>
      </article>
    </div>
  </section>
</template>

<script setup>
import { ref } from 'vue'

const imageStates = ref({})
const imageUrl = (person, imageName) =>
  `http://localhost:5000/static/MC2-Image-Data/${person}/${imageName}`

const scenes = [
  {
    id: 'person3',
    title: '样本 A / Person3_2',
    summary: '从多候选误判收敛为单一关键物证',
    caption: '文本中存在明显的线下会合提示，因此需要把多个候选视觉框收束为一个可追踪物证。',
    image: imageUrl('Person3', 'Person3_1.jpg'),
    placeholderTitle: 'Person3 证据图',
    placeholderText: '真实图加载失败时显示检测结构。',
    beforeBoxes: [
      { label: 'pumpkinNotes 0.53', kind: 'is-blue', style: 'left:8%;top:14%;width:70%;height:58%;' },
      { label: 'yellowBalloon 0.40', kind: 'is-gold', style: 'left:4%;top:10%;width:74%;height:44%;' },
      { label: 'yellowBag 0.39', kind: 'is-red', style: 'left:14%;top:24%;width:58%;height:44%;' }
    ],
    afterBoxes: [
      { label: '人工确认：黄色提袋', kind: 'is-green', style: 'left:24%;top:24%;width:40%;height:42%;' }
    ],
    machineNote: '模型同时给出南瓜便签、黄色气球、黄色提袋等多个高重叠候选，说明低阈值下存在明显类别混淆。',
    humanNote: '结合文本叙事后，仅保留黄色提袋这一线下识别物证，其余框被视为背景噪声或误报。'
  },
  {
    id: 'person27',
    title: '样本 B / Person27_14',
    summary: '从高噪声候选集回退为公共物品',
    caption: '文本明确提到南瓜笔记本，这类物品更像会场通用资产，因此可作为“误报洗白”示例。',
    image: imageUrl('Person27', 'Person27_1.jpg'),
    placeholderTitle: 'Person27 对照图',
    placeholderText: '真实图加载失败时显示公共物品对照结构。',
    beforeBoxes: [
      { label: 'eyeball 0.26', kind: 'is-red', style: 'left:26%;top:40%;width:20%;height:24%;' },
      { label: 'pumpkinNotes 0.40', kind: 'is-blue', style: 'left:21%;top:27%;width:31%;height:34%;' },
      { label: 'yellowBag 0.29', kind: 'is-gold', style: 'left:11%;top:8%;width:52%;height:52%;' }
    ],
    afterBoxes: [
      { label: '人工确认：南瓜笔记本', kind: 'is-green', style: 'left:22%;top:26%;width:34%;height:36%;' }
    ],
    machineNote: '模型把同一区域扩张为多个类别候选，造成了“看起来很复杂”的假象。',
    humanNote: '人工核对文本后，可将其回退为公共笔记本类资产，不再进入核心嫌疑证据链。'
  }
]

scenes.forEach((scene) => {
  imageStates.value[scene.id] = 'loading'
})

const markImageLoaded = (sceneId) => {
  imageStates.value = { ...imageStates.value, [sceneId]: 'loaded' }
}

const markImageFailed = (sceneId) => {
  imageStates.value = { ...imageStates.value, [sceneId]: 'failed' }
}

const imageClass = (sceneId) => {
  const state = imageStates.value[sceneId] || 'loading'
  return {
    'is-loaded': state === 'loaded',
    'is-failed': state === 'failed'
  }
}
</script>

<style scoped>
.process-panel {
  overflow: hidden;
}

.cases-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: clamp(22px, 3vw, 34px);
}

.case-card {
  display: grid;
  grid-template-columns: minmax(240px, 0.42fr) minmax(0, 1fr);
  gap: clamp(18px, 2.4vw, 30px);
  align-items: center;
  padding: clamp(18px, 2.6vw, 30px);
  border: 1px solid var(--border);
  border-radius: var(--radius-xl);
  background:
    radial-gradient(circle at top left, rgba(47, 125, 246, 0.08), transparent 28%),
    linear-gradient(180deg, rgba(255, 255, 255, 0.94), rgba(247, 251, 255, 0.84));
  box-shadow: var(--shadow-soft);
}

.case-card__text {
  align-self: stretch;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.case-card__text span,
.case-log__item span,
.case-view__title {
  display: block;
  color: var(--subtle);
  font-size: 0.8rem;
  font-weight: 800;
  letter-spacing: 0.06em;
}

.case-card__text strong {
  display: block;
  margin: 8px 0;
  font-size: 1.04rem;
}

.case-card__text p,
.case-log__item p {
  margin: 0;
  color: var(--muted);
  line-height: 1.7;
}

.case-compare {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  margin-top: 0;
}

.case-image {
  position: relative;
  overflow: hidden;
  margin-top: 8px;
  border-radius: 14px;
  border: 1px solid rgba(53, 89, 138, 0.12);
  background: linear-gradient(180deg, #ffffff, #f6faff);
  aspect-ratio: 4 / 3;
}

.case-image img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
  opacity: 0;
  transition: opacity var(--motion-medium) ease;
}

.case-image img.is-loaded {
  opacity: 1;
}

.case-image img.is-failed {
  display: none;
}

.case-image.is-placeholder {
  background:
    linear-gradient(rgba(47, 125, 246, 0.06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(47, 125, 246, 0.06) 1px, transparent 1px),
    linear-gradient(180deg, #ffffff, #f7fbff);
  background-size: 100% 48px, 48px 100%, 100% 100%;
}

.case-placeholder {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: 16px;
  color: var(--muted);
}

.case-placeholder strong {
  margin-bottom: 8px;
  color: var(--text);
  font-size: 1rem;
}

.case-placeholder p {
  margin: 0;
  line-height: 1.65;
}

.case-image-state {
  position: absolute;
  left: 10px;
  top: 10px;
  z-index: 4;
  display: inline-flex;
  align-items: center;
  min-height: 28px;
  padding: 0 10px;
  border: 1px solid var(--border);
  border-radius: 999px;
  color: var(--muted);
  background: rgba(255, 255, 255, 0.9);
  box-shadow: var(--shadow-soft);
  font-size: 0.74rem;
  font-weight: 900;
}

.case-image-state::before {
  content: "";
  width: 8px;
  height: 8px;
  margin-right: 6px;
  border: 2px solid rgba(47, 125, 246, 0.18);
  border-top-color: var(--accent);
  border-radius: 999px;
  animation: case-spin 760ms linear infinite;
}

.case-image-state.is-failed {
  color: #9a6818;
  border-color: rgba(240, 180, 76, 0.24);
  background: rgba(255, 247, 219, 0.92);
}

.case-image-state.is-failed::before {
  display: none;
}

.case-placeholder.is-clean {
  background: radial-gradient(circle at top right, rgba(57, 169, 125, 0.08), transparent 28%);
}

.overlay-box {
  position: absolute;
  z-index: 3;
  border: 3px solid;
  border-radius: 12px;
  background: transparent;
}

@keyframes case-spin {
  to {
    transform: rotate(360deg);
  }
}

.overlay-box__label {
  position: absolute;
  top: -2px;
  left: 10px;
  transform: translateY(-100%);
  display: inline-flex;
  align-items: center;
  padding: 4px 8px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.96);
  box-shadow: 0 6px 14px rgba(48, 78, 114, 0.08);
  white-space: nowrap;
  font-size: 0.72rem;
  font-weight: 800;
}

.overlay-box.is-blue {
  border-color: #2f7df6;
}

.overlay-box.is-blue .overlay-box__label {
  color: #1d58b1;
}

.overlay-box.is-gold {
  border-color: #f0b44c;
}

.overlay-box.is-gold .overlay-box__label {
  color: #9a6818;
}

.overlay-box.is-red {
  border-color: #df6a6a;
}

.overlay-box.is-red .overlay-box__label {
  color: #b44e4e;
}

.overlay-box.is-green {
  border-color: #39a97d;
}

.overlay-box.is-green .overlay-box__label {
  color: #1c8a67;
}

.case-log {
  grid-column: 2;
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
  margin-top: -8px;
}

.case-log__item {
  padding: 12px;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  background: rgba(247, 250, 255, 0.86);
}

@media (max-width: 1240px) {
  .case-card {
    grid-template-columns: 1fr;
  }

  .case-log {
    grid-column: auto;
    margin-top: 0;
  }
}

@media (max-width: 760px) {
  .cases-grid,
  .case-compare,
  .case-log {
    grid-template-columns: 1fr;
  }
}
</style>
