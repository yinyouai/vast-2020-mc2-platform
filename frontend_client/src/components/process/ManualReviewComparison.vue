<template>
  <section class="panel comparison-panel">
    <div class="panel-header">
      <div>
        <h4 class="panel-title">标注前后对照</h4>
        <p class="panel-subtitle">与当前复核对象实时同步，展示机器候选和人工标签之间的变化。</p>
      </div>
      <span class="data-chip">{{ caseItem.id }}</span>
    </div>

    <article class="case-card">
      <div class="case-card__text">
        <span>当前样本 / {{ caseItem.id }}</span>
        <strong>{{ caseItem.machineLabel }} -> {{ caseItem.humanLabel }}</strong>
        <p>{{ caseItem.caption }}</p>
      </div>

      <div class="case-compare">
        <div class="case-view">
          <div class="case-view__title">标注前 / 机器预测</div>
          <div class="case-image" :class="{ 'is-placeholder': imageState !== 'loaded', 'is-pending-review': !isReviewed }">
            <img
              :key="imageUrl"
              :src="imageUrl"
              :alt="`${caseItem.id} 机器预测图`"
              :class="{ 'is-loaded': imageState === 'loaded', 'is-failed': imageState === 'failed' }"
              loading="lazy"
              @load="imageState = 'loaded'"
              @error="imageState = 'failed'"
            />
            <div class="case-placeholder">
              <strong>{{ caseItem.id }} 证据图</strong>
              <p>真实图加载失败时显示检测结构。</p>
            </div>
            <div class="overlay-box is-blue" style="left: 10%; top: 18%; width: 66%; height: 52%;">
              <span class="overlay-box__label">{{ caseItem.machineLabel }}</span>
            </div>
            <div class="overlay-box is-red" style="left: 20%; top: 32%; width: 46%; height: 36%;">
              <span class="overlay-box__label">冲突 {{ conflictPercent }}%</span>
            </div>
          </div>
        </div>

        <div class="case-view">
          <div class="case-view__title">{{ afterTitle }}</div>
          <div class="case-image" :class="{ 'is-placeholder': imageState !== 'loaded' }">
            <img
              :key="`after-${imageUrl}`"
              :src="imageUrl"
              :alt="`${caseItem.id} 人工修正图`"
              :class="{ 'is-loaded': imageState === 'loaded', 'is-failed': imageState === 'failed' }"
              loading="lazy"
              @load="imageState = 'loaded'"
              @error="imageState = 'failed'"
            />
            <div class="case-placeholder is-clean">
              <strong>{{ afterPlaceholderTitle }}</strong>
              <p>{{ afterPlaceholderText }}</p>
            </div>
            <div
              v-if="isReviewed"
              class="overlay-box is-green"
              style="left: 24%; top: 24%; width: 42%; height: 42%;"
            >
              <span class="overlay-box__label">{{ afterLabel }}：{{ caseItem.humanLabel }}</span>
            </div>
          </div>
        </div>
      </div>
    </article>
  </section>
</template>

<script setup>
import { computed, ref, watch } from 'vue'

const props = defineProps({
  caseItem: {
    type: Object,
    required: true
  }
})

const imageState = ref('loading')
const imageUrl = computed(
  () => `http://localhost:5000/static/MC2-Image-Data/${props.caseItem.id}/${props.caseItem.id}_1.jpg`
)
const conflictPercent = computed(() => Math.round((props.caseItem.conflictScore || 0) * 100))
const isReviewed = computed(() => ['confirmed', 'corrected'].includes(props.caseItem.status))
const afterTitle = computed(() => isReviewed.value ? '标注后 / 人工结果' : '待标注 / 人工复核')
const afterPlaceholderTitle = computed(() => isReviewed.value ? `${props.caseItem.id} 人工结果` : `${props.caseItem.id} 待人工复核`)
const afterPlaceholderText = computed(() => isReviewed.value ? props.caseItem.humanLabel : '尚未提交人工标注，请先在复核工作台操作。')
const afterLabel = computed(() => props.caseItem.status === 'corrected' ? '人工修正' : '人工确认')

watch(
  () => props.caseItem.id,
  () => {
    imageState.value = 'loading'
  }
)
</script>

<style scoped>
.comparison-panel {
  overflow: hidden;
}

.case-card {
  display: grid;
  grid-template-columns: minmax(220px, 0.36fr) minmax(0, 1fr);
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

.case-card__text span,
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

.case-card__text p {
  display: block !important;
  margin: 0;
  color: var(--muted);
  line-height: 1.7;
}

.case-compare {
  display: grid;
  grid-template-columns: repeat(2, minmax(0, 1fr));
  gap: 12px;
}

.case-image {
  position: relative;
  overflow: hidden;
  margin-top: 8px;
  border: 1px solid rgba(53, 89, 138, 0.12);
  border-radius: 14px;
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

.case-image.is-pending-review img {
  filter: saturate(0.78);
  opacity: 0.58;
}

.case-image.is-placeholder {
  background:
    linear-gradient(rgba(47, 125, 246, 0.06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(47, 125, 246, 0.06) 1px, transparent 1px),
    linear-gradient(180deg, #ffffff, #f7fbff);
  background-size: 48px 48px, 48px 48px, 100% 100%;
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
  display: block !important;
  margin: 0;
  line-height: 1.65;
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

.overlay-box__label {
  position: absolute;
  left: 10px;
  top: -2px;
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

@media (max-width: 1240px) {
  .case-card,
  .case-compare {
    grid-template-columns: 1fr;
  }
}
</style>
