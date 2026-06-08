<template>
  <section class="view-grid-layout verdict-page">
    <section v-if="final" class="verdict-hero">
      <div class="verdict-copy"><span class="eyebrow">任务 5 / 最终定案</span><h3>{{ final.totem }}</h3>
        <p>由 {{ final.group.length }} 位成员稳定共享，共核验 {{ winner?.evidence_image_count || 0 }} 张图片。</p>
        <div class="member-line"><span v-for="person in final.group" :key="person">{{ person }}</span></div></div>
      <div class="score-ring" :style="{ '--score': `${Math.round(final.score*100)*3.6}deg` }"><div><strong>{{ Math.round(final.score*100) }}</strong><span>综合分</span></div></div>
      <div class="verdict-kpis"><article><span>人数</span><b>{{ winner?.owner_count }}/8</b></article><article><span>最少出现</span><b>{{ winner?.min_occurrence }} 张</b></article>
        <article><span>稳定拥有者</span><b>{{ percent(winner?.stable_owner_ratio) }}</b></article><article><span>文本支持</span><b>{{ winner?.text_support_count }} 人</b></article></div>
    </section>
    <div class="final-visual-grid"><GroupEvidenceNetwork/><FinalEvidenceMatrix/></div>
    <EvidencePhotoGallery/>
    <div class="final-bottom-grid"><ExclusionChart/><ProvenanceNarrative/></div>
  </section>
</template>
<script setup>
import { computed } from 'vue'
import { useDashboardStore } from '../store/dashboard'
import GroupEvidenceNetwork from '../components/targeting/GroupEvidenceNetwork.vue'
import FinalEvidenceMatrix from '../components/targeting/FinalEvidenceMatrix.vue'
import EvidencePhotoGallery from '../components/targeting/EvidencePhotoGallery.vue'
import ExclusionChart from '../components/targeting/ExclusionChart.vue'
import ProvenanceNarrative from '../components/targeting/ProvenanceNarrative.vue'
const store=useDashboardStore();const final=computed(()=>store.analysisSummary?.final);const winner=computed(()=>store.candidateRankings.find((item)=>item.label===store.activeTotem));const percent=(value=0)=>`${Math.round(value*100)}%`
</script>
<style scoped>
.verdict-page{gap:22px}.verdict-hero{display:grid;grid-template-columns:minmax(0,1fr) 150px minmax(360px,.8fr);align-items:center;gap:24px;padding:28px;border: none;border-radius: 12px;background: var(--surface-2);box-shadow: none;font-size:2.3rem}.verdict-copy p{display:block!important;margin:0;color:var(--muted)}.member-line{display:flex;flex-wrap:wrap;gap:5px;margin-top:13px}.member-line span{padding:5px 7px;border: none;border-radius: 12px;background: var(--surface);font-size:.7rem}
.score-ring{display:grid;place-items:center;width:132px;aspect-ratio:1;border-radius:50%;background:conic-gradient(#d99522 var(--score),#e5ebf1 0);position:relative}.score-ring:after{content:"";position:absolute;inset:12px;border-radius:50%;background: var(--surface)}.score-ring div{position:relative;z-index:1;text-align:center}.score-ring strong,.score-ring span{display:block}.score-ring strong{font-size:2rem}.score-ring span{color:var(--muted);font-size:.7rem}
.verdict-kpis{display:grid;grid-template-columns:1fr 1fr;gap:8px}.verdict-kpis article{padding:11px;border: none;border-radius: 12px;background: var(--surface-2)}.verdict-kpis span,.verdict-kpis b{display:block}.verdict-kpis span{color:var(--subtle);font-size:.68rem}.verdict-kpis b{margin-top:5px;font-size:1rem}
.final-visual-grid{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(430px,.8fr);gap:18px}.final-bottom-grid{display:grid;grid-template-columns:minmax(0,1.2fr) minmax(330px,.8fr);gap:18px}
@media(max-width:1150px){.verdict-hero{grid-template-columns:1fr 130px}.verdict-kpis{grid-column:1/-1}.final-visual-grid,.final-bottom-grid{grid-template-columns:1fr}}
@media(max-width:700px){.verdict-hero{grid-template-columns:1fr}.score-ring{width:116px}.verdict-kpis{grid-template-columns:1fr 1fr}}
</style>
