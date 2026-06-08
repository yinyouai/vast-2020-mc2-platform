<template>
  <section class="view-grid-layout review-page">
    <div class="page-intro">
      <div><p class="eyebrow">任务 2 / 人在回路复核</p><h3>只复核最需要人工判断的样本，其余图片继续由模型参与评分。</h3>
        <div class="intro-pills"><span class="data-chip">模型命中 {{ counts.modelHits }}</span><span class="data-chip">建议人工复核 {{ counts.pending }}</span><span class="data-chip">人工修正 {{ counts.corrected }}</span></div></div>
    </div>
    <div v-if="store.correctionMessage" class="save-feedback" role="status">{{ store.correctionMessage }}</div>
    <section class="review-scope">
      <div>
        <span>当前核验候选</span>
        <strong>{{ store.reviewCandidateLabel || store.activeTotem }}</strong>
        <small>
          全量图片都会进入后续评分；这里只抽取最不确定、最冲突或最可能漏检的图片供人工纠偏。
        </small>
      </div>
      <div class="candidate-switcher" role="group" aria-label="选择要人工核验的候选物品">
        <button
          v-for="candidate in store.candidateRankings"
          :key="candidate.label"
          type="button"
          :class="{ active: candidate.label === store.reviewCandidateLabel }"
          @click="changeCandidate(candidate.label)"
        >
          {{ candidate.label }}
          <small>{{ candidate.owner_count }} 人</small>
        </button>
      </div>
    </section>
    <section class="review-policy">
      <div class="batch-copy">
        <span>最小人工复核集</span>
        <strong>每位候选拥有者仅推荐 1 张最高优先图片</strong>
        <small>
          当前建议人工判断 {{ counts.pending }} 张；其余
          {{ Math.max(0, (store.reviewQueueMeta.total_search_images || 0) - (store.reviewQueueMeta.returned_search_images || 0)) }}
          张不要求逐图复核，但模型结果仍进入最终候选评分。
        </small>
      </div>
      <div class="policy-stats">
        <span><b>{{ store.reviewQueueMeta.returned_search_images || 0 }}</b>张候选图</span>
        <span><b>{{ store.reviewQueueMeta.total_search_images || 0 }}</b>张模型持续分析</span>
      </div>
    </section>
    <PersonReviewRadar
      :people="store.reviewPriorities"
      :summary="store.reviewPrioritySummary"
      :scoring="store.reviewPriorityScoring"
      :updated-at="store.reviewPrioritiesUpdatedAt"
      @select-person="selectPriorityPerson"
    />
    <ConflictPriorityQueue :items="store.reviewQueue" :active-id="activeCaseId" :busy-id="store.correctionInFlight"
      @select="selectCase" @update-case="updateCase" />
    <CorrectionCanvas :case-item="activeCase" @submit-review="updateCase" />
    <ManualReviewComparison :case-item="activeCase" />
  </section>
</template>

<script setup>
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import ConflictPriorityQueue from '../components/interaction/ConflictPriorityQueue.vue'
import CorrectionCanvas from '../components/interaction/CorrectionCanvas.vue'
import ManualReviewComparison from '../components/process/ManualReviewComparison.vue'
import PersonReviewRadar from '../components/interaction/PersonReviewRadar.vue'
import { useDashboardStore } from '../store/dashboard'
const store=useDashboardStore()
const activeCaseId=ref('')
const rawRecommendedCase=ref(null)
let refreshTimer
const activeCase=computed(()=>store.reviewQueue.find((item)=>item.id===activeCaseId.value)||rawRecommendedCase.value||store.reviewQueue[0]||null)
const counts=computed(()=>({
  modelHits:store.reviewQueue.filter((item)=>['model_hit','weak_model_hit','verified'].includes(item.review_kind)&&item.box_id>=0&&item.status!=='rejected').length,
  pending:store.reviewQueue.filter((item)=>item.status==='unreviewed').length,
  corrected:store.reviewQueue.filter((item)=>['confirmed','added','rejected','dismissed'].includes(item.status)).length
}))
const selectCase=(id)=>{activeCaseId.value=id;const item=store.reviewQueue.find((entry)=>entry.id===id);if(item)store.selectReviewTarget(item)}
const selectPriorityPerson=(person)=>{
  rawRecommendedCase.value=person.recommended_case
  activeCaseId.value=person.recommended_case_id
  store.selectReviewTarget(person.recommended_case)
}
const updateCase=async({id,patch})=>{
  const item=store.reviewQueue.find((entry)=>entry.id===id)
    || (rawRecommendedCase.value?.id===id ? rawRecommendedCase.value : null)
  if(item)await store.submitCorrection(item,patch)
}
const changeCandidate=async(label)=>{
  rawRecommendedCase.value=null
  activeCaseId.value=''
  await store.setReviewCandidate(label)
}
watch(()=>store.reviewQueue,(items)=>{if(items.length&&!items.some((item)=>item.id===activeCaseId.value))selectCase(items[0].id)},{immediate:true,deep:true})
onMounted(()=>{store.fetchReviewPriorities();refreshTimer=window.setInterval(()=>store.fetchReviewPriorities(),10000)})
onBeforeUnmount(()=>window.clearInterval(refreshTimer))
</script>

<style scoped>
.review-page{gap:20px}.save-feedback{padding:10px 13px;border: none;border-radius: 12px;color: var(--success);background: rgba(16, 185, 129, 0.1);font-size:.78rem;font-weight:700}
.review-scope{display:grid;grid-template-columns:minmax(220px,.35fr) minmax(0,1.65fr);align-items:center;gap:18px}.review-scope>div:first-child span,.review-scope>div:first-child strong,.review-scope>div:first-child small{display:block}.review-scope>div:first-child span{color:var(--subtle);font-size:.68rem;font-weight:800}.review-scope>div:first-child strong{margin:5px 0;font-size:1.08rem}.review-scope>div:first-child small{color:var(--muted);font-size:.7rem;line-height:1.5}
.candidate-switcher{display:flex;gap:7px;overflow-x:auto;padding:3px}.candidate-switcher button{flex:0 0 auto;min-height:48px;padding:7px 10px;border: none;border-radius: 12px;color:var(--muted);background: transparent;font-size:.7rem;font-weight:800}.candidate-switcher button small{display:block;margin-top:3px;color:var(--subtle);font-size:.6rem}.candidate-switcher button.active{border-color:var(--accent);color:var(--accent);background: rgba(255, 255, 255, 0.02);box-shadow: none;align-items:center;justify-content:space-between;gap:18px}.batch-copy span,.batch-copy strong,.batch-copy small{display:block}.batch-copy span{color:var(--subtle);font-size:.68rem;font-weight:800}.batch-copy strong{margin:4px 0;font-size:.9rem}.batch-copy small{max-width:760px;color:var(--muted);font-size:.68rem;line-height:1.5}.policy-stats{display:flex;gap:8px}.policy-stats span{min-width:112px;padding:10px;border: none;border-radius: 12px;color:var(--muted);background: rgba(255, 255, 255, 0.02);font-size:.68rem}.policy-stats b{display:block;margin-bottom:4px;color:var(--text);font-size:1.05rem}
@media(max-width:800px){.review-scope{grid-template-columns:1fr}}
@media(max-width:950px){.review-policy{align-items:stretch;flex-direction:column}.policy-stats{flex-wrap:wrap}}
</style>
