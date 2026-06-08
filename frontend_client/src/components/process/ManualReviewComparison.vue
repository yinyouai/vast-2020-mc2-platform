<template>
  <section v-if="caseItem" class="audit-trace">
    <div class="trace-step raw"><span>01</span><div><b>原始预测保留</b><small>{{ caseItem.predicted_label }} / box {{ caseItem.box_id }}</small></div></div>
    <i></i>
    <div class="trace-step human"><span>02</span><div><b>人工校正记录</b><small>{{ caseItem.corrected_label }} / {{ statusLabel }}</small></div></div>
    <i></i>
    <div class="trace-step inference"><span>03</span><div><b>重新计算</b><small>{{ caseItem.status === 'rejected' ? '从校正矩阵排除' : '计入候选与证据评分' }}</small></div></div>
  </section>
</template>
<script setup>
import { computed } from 'vue'
const props=defineProps({caseItem:{type:Object,default:null}})
const statusLabel=computed(()=>({confirmed:'模型命中',added:'人工补标',rejected:'误报驳回',unreviewed:'待复核',dismissed:'该图未确认'}[props.caseItem?.status]||''))
</script>
<style scoped>
.audit-trace { display:grid; grid-template-columns:1fr 40px 1fr 40px 1fr; align-items:center; gap:8px; padding:14px 0; border-top: 1px solid rgba(255, 255, 255, 0.05); background: transparent; }
.audit-trace > i { height:1px; background:var(--border-strong); }.trace-step { display:flex; align-items:center; gap:10px; min-width:0; }.trace-step > span { display:grid; place-items:center; width:34px;height:34px;border-radius: 12px;font-weight:900 }
.trace-step b,.trace-step small{display:block}.trace-step small{margin-top:3px;color:var(--muted);font-size:.72rem}.raw>span{color:var(--accent);background:#ebf3ff}.human>span{color: var(--success);background: rgba(16, 185, 129, 0.1)}.inference>span{color: var(--warning);background: rgba(245, 158, 11, 0.15)}
@media(max-width:760px){.audit-trace { display:grid; grid-template-columns:1fr 40px 1fr 40px 1fr; align-items:center; gap:8px; padding:14px 0; border-top: 1px solid rgba(255, 255, 255, 0.05); background: transparent; }.audit-trace>i{width:1px;height:20px;margin-left:16px}}
</style>
