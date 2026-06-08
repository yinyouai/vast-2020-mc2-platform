<template>
  <section class="panel provenance-panel">
    <div class="panel-header"><div><span class="section-kicker">可追溯链</span><h4 class="panel-title">结论形成过程</h4></div></div>
    <div class="provenance-flow">
      <article v-for="(stage,index) in stages" :key="stage.id"><span>{{ String(index+1).padStart(2,'0') }}</span>
        <div><strong>{{ stage.name }}</strong><small>{{ descriptions[index] }}</small></div></article>
    </div>
    <div v-if="final" class="final-statement"><span>最终判定</span><strong>{{ final.totem }}</strong><p>{{ final.group.join('、') }}</p></div>
  </section>
</template>
<script setup>
import { computed } from 'vue'
import { useDashboardStore } from '../../store/dashboard'
const store=useDashboardStore();const stages=computed(()=>store.analysisSummary?.stages||[]);const final=computed(()=>store.analysisSummary?.final)
const descriptions=['测量类别缺失、置信度与阈值代价','确认模型命中、补录漏检、驳回误报','重建校正后人物—物品结构','比较人数、稳定性、图片与文本贡献','逐人核对图片并反向排除非成员']
</script>
<style scoped>
.section-kicker{color:var(--subtle);font-size:.7rem;font-weight:800}.provenance-flow{display:grid;gap:8px}.provenance-flow article{display:grid;grid-template-columns:38px 1fr;align-items:center;gap:10px;padding:9px;border-left:3px solid var(--accent);background: var(--surface-3)}.provenance-flow article>span{display:grid;place-items:center;width:34px;height:34px;border-radius: 12px;color:var(--accent);background: var(--surface-glow);font-weight:900}.provenance-flow strong,.provenance-flow small{display:block}.provenance-flow small{margin-top:3px;color:var(--muted);font-size:.7rem}
.final-statement{margin-top:12px;padding:14px;border: none;border-radius: 12px;background: rgba(245, 158, 11, 0.1)}.final-statement span{color: var(--warning);font-size:.7rem;font-weight:800}.final-statement strong{display:block;margin:5px 0;font-size:1.3rem}.final-statement p{display:block!important;margin:0;color:var(--muted);font-size:.72rem;line-height:1.5}
</style>
