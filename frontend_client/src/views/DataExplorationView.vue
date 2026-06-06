<template>
  <section class="view-grid-layout review-page">
    <div class="page-intro">
      <div><p class="eyebrow">任务 2 / 人在回路复核</p><h3>系统已完成首轮校正，分析师仍可逐条推翻或恢复。</h3>
        <div class="intro-pills"><span class="data-chip">人工补标 {{ counts.added }}</span><span class="data-chip">模型命中 {{ counts.confirmed }}</span><span class="data-chip">误报驳回 {{ counts.rejected }}</span></div></div>
    </div>
    <div v-if="store.correctionMessage" class="save-feedback" role="status">{{ store.correctionMessage }}</div>
    <ConflictPriorityQueue :items="store.reviewQueue" :active-id="activeCaseId" :busy-id="store.correctionInFlight"
      @select="selectCase" @update-case="updateCase" />
    <CorrectionCanvas :case-item="activeCase" @submit-review="updateCase" />
    <ManualReviewComparison :case-item="activeCase" />
  </section>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import ConflictPriorityQueue from '../components/interaction/ConflictPriorityQueue.vue'
import CorrectionCanvas from '../components/interaction/CorrectionCanvas.vue'
import ManualReviewComparison from '../components/process/ManualReviewComparison.vue'
import { useDashboardStore } from '../store/dashboard'
const store=useDashboardStore()
const activeCaseId=ref('')
const activeCase=computed(()=>store.reviewQueue.find((item)=>item.id===activeCaseId.value)||store.reviewQueue[0]||null)
const counts=computed(()=>({confirmed:store.reviewQueue.filter((item)=>item.status==='confirmed').length,added:store.reviewQueue.filter((item)=>item.status==='added').length,rejected:store.reviewQueue.filter((item)=>['rejected','unreviewed'].includes(item.status)).length}))
const selectCase=(id)=>{activeCaseId.value=id;const item=store.reviewQueue.find((entry)=>entry.id===id);if(item)store.selectReviewTarget(item)}
const updateCase=async({id,patch})=>{const item=store.reviewQueue.find((entry)=>entry.id===id);if(item)await store.submitCorrection(item,patch)}
watch(()=>store.reviewQueue,(items)=>{if(items.length&&!items.some((item)=>item.id===activeCaseId.value))selectCase(items[0].id)},{immediate:true,deep:true})
</script>

<style scoped>
.review-page{gap:20px}.save-feedback{padding:10px 13px;border:1px solid #bfe2d4;border-radius:7px;color:#187553;background:#effaf5;font-size:.78rem;font-weight:700}
</style>
