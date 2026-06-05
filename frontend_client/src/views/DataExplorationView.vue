<template>
  <section class="view-grid-layout">
    <div class="page-intro">
      <div>
        <p class="eyebrow">任务 2 / 人工复核</p>
        <h3>把“机器猜测”转化为可追责的人类判断。</h3>
        <div class="intro-pills">
          <span class="data-chip">冲突排序</span>
          <span class="data-chip">人工标签</span>
          <span class="data-chip">状态回灌</span>
        </div>
      </div>
    </div>

    <div class="analysis-grid">
      <article class="analysis-card">
        <span>复核逻辑</span>
        <strong>先处理高冲突，再处理对照样本。</strong>
      </article>
      <article class="analysis-card">
        <span>人工介入</span>
        <strong>每个对象都能确认或修正标签。</strong>
      </article>
      <article class="analysis-card">
        <span>页面联动</span>
        <strong>第三层点击对象会持续进入复核列表。</strong>
      </article>
    </div>

    <ControlSlider />

    <div class="exploration-workspace-grid">
      <ConflictPriorityQueue
        :items="reviewQueue"
        :active-id="activeCaseId"
        :active-item="activeCase"
        @select="selectCase"
        @update-case="updateCase"
      />
      <CorrectionCanvas :case-item="activeCase" />
    </div>

    <ManualReviewComparison :case-item="activeCase" />
  </section>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import ControlSlider from '../components/interaction/ControlSlider.vue'
import ConflictPriorityQueue from '../components/interaction/ConflictPriorityQueue.vue'
import CorrectionCanvas from '../components/interaction/CorrectionCanvas.vue'
import ManualReviewComparison from '../components/process/ManualReviewComparison.vue'
import { useDashboardStore } from '../store/dashboard'

const store = useDashboardStore()
const activeCaseId = ref(store.selectedPersonId || 'Person3')

const reviewCases = ref([
  {
    rank: 'A',
    id: 'Person3',
    source: 'conflict',
    status: 'unreviewed',
    priority: '高',
    risk: 'high',
    conflictScore: 0.92,
    machineLabel: '红帽 / 低置信度',
    humanLabel: '黄色提袋',
    caption: '文本明确提到会场入口处的明亮黄色提袋，机器却倾向红帽，属于强图文冲突。',
    textComment: 'I grabbed the bright yellow bag near the entrance so the team could recognize me quickly.',
    semanticKeywords: ['yellow bag', 'entrance', 'recognize'],
    semanticSignal: '线下识别物',
    semanticConflict: '文本明确指向黄色提袋，但机器预测偏向红帽。',
    verdict: '等待人工复核确认，可手动调整标签后再提交。',
    note: '高冲突'
  },
  {
    rank: 'B',
    id: 'Person27',
    source: 'conflict',
    status: 'unreviewed',
    priority: '高',
    risk: 'high',
    conflictScore: 0.78,
    machineLabel: '南瓜笔记本',
    humanLabel: '公共会场物品',
    caption: '机器框选与文本叙事不一致，更适合作为误报清洗的重要对照。',
    textComment: 'The pumpkin notebook was useful for taking notes during the public talk.',
    semanticKeywords: ['pumpkin notebook', 'notes', 'public talk'],
    semanticSignal: '公共会场资产',
    semanticConflict: '文本更像普通记录场景，不支持核心嫌疑物证。',
    verdict: '等待人工复核确认，可手动调整标签后再提交。',
    note: '高冲突'
  },
  {
    rank: 'C',
    id: 'Person21',
    source: 'compare',
    status: 'unreviewed',
    priority: '低',
    risk: 'low',
    conflictScore: 0.31,
    machineLabel: '普通礼品',
    humanLabel: '背景样本',
    caption: '图像和文本都更接近日常会场活动，冲突强度较低。',
    textComment: 'I stayed near the registration area and picked up a standard event gift.',
    semanticKeywords: ['registration', 'event gift', 'standard'],
    semanticSignal: '背景行为',
    semanticConflict: '文本语义与普通参会行为一致，可作为噪声基线。',
    verdict: '对照样本，可用于校准公共物品分布。',
    note: '对照'
  },
  {
    rank: 'D',
    id: 'Person12',
    source: 'compare',
    status: 'unreviewed',
    priority: '高',
    risk: 'high',
    conflictScore: 0.66,
    machineLabel: '共享暗号物品',
    humanLabel: '黄色提袋',
    caption: '与核心组特征高度接近，物证层面反复出现异常共现。',
    textComment: 'I kept the same yellow bag visible while moving between the side rooms.',
    semanticKeywords: ['same yellow bag', 'visible', 'side rooms'],
    semanticSignal: '稳定共享物证',
    semanticConflict: '文本出现稳定携带和可见性描述，支持继续追踪。',
    verdict: '对照样本，可用于验证核心组收敛。',
    note: '对照'
  }
])

const reviewQueue = computed(() => {
  const staticIds = new Set(reviewCases.value.map((item) => item.id))
  return [
    ...reviewCases.value,
    ...store.cachedReviewTargets.filter((item) => !staticIds.has(item.id))
  ]
})

const activeCase = computed(
  () => reviewQueue.value.find((item) => item.id === activeCaseId.value) || reviewQueue.value[0]
)

const selectCase = (caseId) => {
  activeCaseId.value = caseId
  store.selectPerson(caseId)
}

const updateCase = ({ id, patch }) => {
  const target = reviewCases.value.find((item) => item.id === id)
  const cachedTarget = store.cachedReviewTargets.find((item) => item.id === id)
  const current = target || cachedTarget
  if (!current) return

  const nextPatch = {
    ...patch,
    verdict: buildVerdict({ ...current, ...patch })
  }

  if (target) Object.assign(target, nextPatch)
  else store.updateReviewTarget(id, nextPatch)
}

const buildVerdict = (item) => {
  if (item.status === 'confirmed') return `已确认标签：${item.humanLabel}。`
  if (item.status === 'corrected') return `已修正为：${item.humanLabel}。`
  return '等待人工复核确认，可手动调整标签后再提交。'
}

watch(
  () => store.selectedPersonId,
  (personId) => {
    if (personId) activeCaseId.value = personId
  },
  { immediate: true }
)
</script>

<style scoped>
.view-grid-layout {
  gap: clamp(18px, 2.6vw, 30px);
}

.page-intro {
  min-height: auto;
  padding: clamp(20px, 3vw, 34px);
}

.page-intro h3 {
  max-width: 860px;
  font-size: clamp(1.75rem, 3vw, 3.1rem);
}

.analysis-grid {
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 16px;
  min-height: auto;
}

.analysis-card {
  min-height: 112px;
  padding: 18px 20px;
}

.exploration-workspace-grid {
  display: grid;
  grid-template-columns: minmax(320px, 0.9fr) minmax(0, 1.7fr);
  gap: 18px;
  align-items: start;
  min-height: auto;
}

@media (max-width: 1040px) {
  .exploration-workspace-grid,
  .analysis-grid {
    grid-template-columns: 1fr;
  }
}
</style>
