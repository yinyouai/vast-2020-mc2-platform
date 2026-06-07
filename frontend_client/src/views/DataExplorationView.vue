<template>
  <section class="view-grid-layout review-page">
    <div class="page-intro">
      <div><p class="eyebrow">任务 2 / 人在回路复核</p><h3>选择候选物品，逐张确认模型命中或寻找漏检证据。</h3>
        <div class="intro-pills"><span class="data-chip">已核验 {{ counts.verified }}</span><span class="data-chip">待人工判断 {{ counts.pending }}</span><span class="data-chip">已排除 {{ counts.excluded }}</span></div></div>
    </div>
    <div v-if="store.correctionMessage" class="save-feedback" role="status">{{ store.correctionMessage }}</div>
    <section class="review-scope panel">
      <div>
        <span>当前核验候选</span>
        <strong>{{ store.reviewCandidateLabel || store.activeTotem }}</strong>
        <small>
          队列动态包含人工核验图片、阈值 {{ store.scoreThreshold.toFixed(2) }} 下的模型命中，以及候选拥有者的待查图片。
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
    <section class="batch-control panel">
      <div class="batch-copy">
        <span>渐进式核验</span>
        <strong>
          {{ store.reviewQueueMode === 'focused' ? `智能批次 ${store.reviewQueueMeta.batch || 1} / ${store.reviewQueueMeta.max_batch || 1}` : '全部图片模式' }}
        </strong>
        <small>
          当前显示 {{ store.reviewQueueMeta.returned_items || store.reviewQueue.length }} 条；
          待搜索图片总量 {{ store.reviewQueueMeta.total_search_images || 0 }} 张。
          智能批次每位拥有者只取 3 张高优先图片。
        </small>
      </div>
      <div class="mode-switch" role="group" aria-label="人工核验队列范围">
        <button :class="{ active: store.reviewQueueMode === 'focused' }" @click="store.setReviewQueueMode('focused')">智能批次</button>
        <button :class="{ active: store.reviewQueueMode === 'all' }" @click="store.setReviewQueueMode('all')">查看全部</button>
      </div>
      <div v-if="store.reviewQueueMode === 'focused'" class="batch-actions">
        <button
          :disabled="(store.reviewQueueMeta.batch || 1) <= 1"
          @click="store.setReviewQueueBatch((store.reviewQueueMeta.batch || 1) - 1)"
        >上一批</button>
        <span>{{ store.reviewQueueMeta.returned_search_images || 0 }} 张搜索图</span>
        <button
          :disabled="(store.reviewQueueMeta.batch || 1) >= (store.reviewQueueMeta.max_batch || 1)"
          @click="store.setReviewQueueBatch((store.reviewQueueMeta.batch || 1) + 1)"
        >下一批</button>
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
  verified:store.reviewQueue.filter((item)=>['confirmed','added'].includes(item.status)).length,
  pending:store.reviewQueue.filter((item)=>item.status==='unreviewed').length,
  excluded:store.reviewQueue.filter((item)=>['rejected','dismissed'].includes(item.status)).length
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
.review-page{gap:20px}.save-feedback{padding:10px 13px;border:1px solid #bfe2d4;border-radius:7px;color:#187553;background:#effaf5;font-size:.78rem;font-weight:700}
.review-scope{display:grid;grid-template-columns:minmax(220px,.35fr) minmax(0,1.65fr);align-items:center;gap:18px}.review-scope>div:first-child span,.review-scope>div:first-child strong,.review-scope>div:first-child small{display:block}.review-scope>div:first-child span{color:var(--subtle);font-size:.68rem;font-weight:800}.review-scope>div:first-child strong{margin:5px 0;font-size:1.08rem}.review-scope>div:first-child small{color:var(--muted);font-size:.7rem;line-height:1.5}
.candidate-switcher{display:flex;gap:7px;overflow-x:auto;padding:3px}.candidate-switcher button{flex:0 0 auto;min-height:48px;padding:7px 10px;border:1px solid var(--border);border-radius:7px;color:var(--muted);background:#fff;font-size:.7rem;font-weight:800}.candidate-switcher button small{display:block;margin-top:3px;color:var(--subtle);font-size:.6rem}.candidate-switcher button.active{border-color:var(--accent);color:var(--accent);background:#f1f6ff;box-shadow:0 0 0 2px rgba(47,125,246,.1)}
.batch-control{display:grid;grid-template-columns:minmax(260px,1fr) auto auto;align-items:center;gap:14px}.batch-copy span,.batch-copy strong,.batch-copy small{display:block}.batch-copy span{color:var(--subtle);font-size:.68rem;font-weight:800}.batch-copy strong{margin:4px 0;font-size:.9rem}.batch-copy small{color:var(--muted);font-size:.68rem;line-height:1.5}.mode-switch{display:flex;padding:3px;border:1px solid var(--border);border-radius:7px;background:#eef3f8}.mode-switch button,.batch-actions button{min-height:36px;padding:0 11px;border-radius:5px;color:var(--muted);background:transparent;font-size:.7rem;font-weight:800}.mode-switch button.active{color:var(--accent);background:#fff;box-shadow:var(--shadow-soft)}.batch-actions{display:flex;align-items:center;gap:8px}.batch-actions button{border:1px solid var(--border);background:#fff}.batch-actions button:disabled{opacity:.42}.batch-actions span{color:var(--muted);font-size:.68rem;white-space:nowrap}
@media(max-width:800px){.review-scope{grid-template-columns:1fr}}
@media(max-width:950px){.batch-control{grid-template-columns:1fr}.mode-switch{width:max-content}}
</style>
