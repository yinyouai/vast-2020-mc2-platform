<template>
  <article class="semantic-card">
    <div class="semantic-head">
      <span>文本语义分析</span>
      <strong>{{ caseItem.semanticSignal || '待判读语义' }}</strong>
    </div>

    <div class="keyword-row">
      <span v-for="keyword in keywords" :key="keyword">{{ keyword }}</span>
    </div>

    <div class="semantic-grid">
      <div>
        <span>图文冲突</span>
        <p>{{ caseItem.semanticConflict || '暂无冲突描述，等待人工复核补充。' }}</p>
      </div>
      <div>
        <span>复核建议</span>
        <p>{{ suggestion }}</p>
      </div>
    </div>
  </article>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  caseItem: {
    type: Object,
    required: true
  }
})

const keywords = computed(() => props.caseItem.semanticKeywords?.length
  ? props.caseItem.semanticKeywords
  : ['待抽取关键词']
)

const suggestion = computed(() => {
  if (props.caseItem.status === 'confirmed') return '当前人工标签已确认，可回灌到后续聚类与证据链。'
  if (props.caseItem.status === 'corrected') return '当前标签已被修正，应优先同步更新标注前后对照。'
  return '建议先核对文本评论中的物品、地点和行动描述，再决定确认或修正标签。'
})
</script>

<style scoped>
.semantic-card {
  display: grid;
  gap: 10px;
  padding: 12px;
  border: none;
  border-radius: var(--radius-sm);
  background:
    radial-gradient(circle at top right, rgba(47, 125, 246, 0.1), transparent 28%),
    rgba(255, 255, 255, 0.1);
}

.semantic-head span,
.semantic-grid span {
  display: block;
  color: var(--subtle);
  font-size: 0.76rem;
  font-weight: 900;
  letter-spacing: 0.08em;
}

.semantic-head strong {
  display: block;
  margin-top: 6px;
}

.keyword-row {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}

.keyword-row span {
  display: inline-flex;
  align-items: center;
  min-height: 24px;
  padding: 0 8px;
  border-radius: 12px;
  color: #1d58b1;
  background: rgba(47, 125, 246, 0.1);
  font-size: 0.76rem;
  font-weight: 900;
}

.semantic-grid {
  display: grid;
  gap: 10px;
}

.semantic-grid div {
  padding: 10px;
  border: none;
  border-radius: 12px;
  background: rgba(247, 250, 255, 0.72);
}

.semantic-grid p {
  display: block !important;
  margin: 6px 0 0;
  color: var(--muted);
  line-height: 1.5;
  font-size: 0.86rem;
}
</style>
