<template>
  <section class="view-grid-layout totem-page">
    <div class="page-intro"><div><p class="eyebrow">任务 4 / 暗号物品筛选</p><h3>让候选经过人数、稳定性、图片和文本四道检验。</h3>
      <div class="intro-pills"><span class="data-chip">9 个候选</span><span class="data-chip">4 项评分</span><span class="data-chip">规则流动图</span></div></div></div>
    <div class="totem-workspace">
      <TotemEliminationPanel :items="totemItems" :selected="store.selectedCandidateLabel"
        @toggle="store.toggleItemExclusion" @select="store.selectCandidate" @auto-exclude="excludeNonmatching" @clear="store.setExcludedItems([])" />
      <CandidateRankingChart/>
    </div>
    <div class="totem-secondary"><TotemBarChart :items="totemItems" @select="store.selectCandidate"/><TotemFlow/></div>
    <section v-if="selectedCandidate" class="panel candidate-inspector">
      <div class="candidate-identity"><span>当前候选</span><strong>{{ selectedCandidate.label }}</strong>
        <b :class="{winner:selectedCandidate.label===store.activeTotem}">{{ selectedCandidate.label===store.activeTotem?'最终暗号':'对照候选' }}</b></div>
      <div class="candidate-metrics">
        <article><span>拥有者</span><b>{{ selectedCandidate.owner_count }} 人</b></article><article><span>最少出现</span><b>{{ selectedCandidate.min_occurrence }} 次</b></article>
        <article><span>稳定率</span><b>{{ percent(selectedCandidate.stable_owner_ratio) }}</b></article><article><span>人工核验图片</span><b>{{ selectedCandidate.verified_image_count }} 张</b></article>
        <article><span>模型命中图片</span><b>{{ selectedCandidate.raw_detection_image_count }} 张</b></article><article><span>直接文本</span><b>{{ selectedCandidate.text_support_count }} 人 / {{ selectedCandidate.text_evidence_count }} 条</b></article>
        <article><span>综合分</span><b>{{ selectedCandidate.score.toFixed(4) }}</b></article>
      </div>
      <div class="candidate-owners"><span v-for="person in selectedCandidate.owners" :key="person">{{ person }}</span></div>
    </section>
  </section>
</template>
<script setup>
import { computed } from 'vue'
import { useDashboardStore } from '../store/dashboard'
import TotemEliminationPanel from '../components/targeting/TotemEliminationPanel.vue'
import TotemBarChart from '../components/targeting/TotemBarChart.vue'
import CandidateRankingChart from '../components/targeting/CandidateRankingChart.vue'
import TotemFlow from '../components/targeting/TotemFlow.vue'
const store=useDashboardStore();const percent=(value=0)=>`${Math.round(value*100)}%`
const selectedCandidate=computed(()=>store.candidateRankings.find((item)=>item.label===store.selectedCandidateLabel)||store.candidateRankings[0])
const totemItems=computed(()=>store.candidateRankings.map((item)=>({name:item.label,coverage:Math.round(item.coverage*100),ownerCount:item.owner_count,minOccurrence:item.min_occurrence,
  stability:item.stable_owner_ratio,score:item.score,role:item.label===store.activeTotem?'最终候选':item.exact_target_size?'人数匹配但不稳定':'人数不匹配',excluded:store.excludedItems.includes(item.label)})))
const excludeNonmatching=()=>store.setExcludedItems(store.candidateRankings.filter((item)=>!item.exact_target_size).map((item)=>item.label))
</script>
<style scoped>
.totem-page{gap:22px}.totem-workspace{display:grid;grid-template-columns:minmax(300px,.62fr) minmax(0,1.38fr);gap:18px}.totem-secondary{display:grid;grid-template-columns:minmax(360px,.8fr) minmax(0,1.2fr);gap:18px}
.candidate-inspector{display:grid;grid-template-columns:220px 1fr;gap:18px}.candidate-identity span,.candidate-identity strong{display:block}.candidate-identity span{color:var(--subtle);font-size:.7rem;font-weight:800}.candidate-identity strong{margin:7px 0;font-size:1.55rem}.candidate-identity>b{display:inline-flex;padding:6px 9px;border-radius: 12px;color:var(--muted);background: var(--surface-3);font-size:.7rem}.candidate-identity>b.winner{color: var(--warning);background: rgba(245, 158, 11, 0.15)}
.candidate-metrics{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:8px}.candidate-metrics article{padding:10px;border: none;border-radius: 12px;background: var(--surface-2)}.candidate-metrics span,.candidate-metrics b{display:block}.candidate-metrics span{color:var(--subtle);font-size:.68rem}.candidate-metrics b{margin-top:5px;font-size:.9rem;font-variant-numeric:tabular-nums}
.candidate-owners{grid-column:1/-1;display:flex;flex-wrap:wrap;gap:6px}.candidate-owners span{padding:6px 8px;border: none;border-radius: 12px;color:var(--muted);background: var(--surface);font-size:.72rem}
@media(max-width:1050px){.totem-workspace,.totem-secondary{grid-template-columns:1fr}.candidate-inspector{grid-template-columns:1fr}.candidate-metrics{grid-template-columns:repeat(3,1fr)}}
</style>
