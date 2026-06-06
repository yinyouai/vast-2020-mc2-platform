<template>
  <section class="view-grid-layout cluster-page">
    <div class="page-intro">
      <div><p class="eyebrow">任务 3 / 群体聚类</p><h3>同时观察矩阵形态、校正变化和候选稳定性。</h3>
        <div class="intro-pills"><span class="data-chip">Ward 重排</span><span class="data-chip">原始 / 校正对照</span><span class="data-chip">候选结构空间</span></div></div>
    </div>

    <section class="cluster-control panel">
      <div class="source-copy"><span>当前数据层</span><strong>{{ store.matrixDataSource === 'raw' ? '原始预测矩阵' : '人工校正矩阵' }}</strong>
        <small>{{ currentCells }} 个非零单元 · {{ currentTotal }} 次共现</small></div>
      <div class="segmented" role="group" aria-label="矩阵数据层">
        <button :class="{active:store.matrixDataSource==='raw'}" @click="store.setMatrixDataSource('raw')">原始预测</button>
        <button :class="{active:store.matrixDataSource==='corrected'}" @click="store.setMatrixDataSource('corrected')">人工校正</button>
      </div>
      <div class="selected-signal"><span>当前候选</span><strong>{{ store.selectedCandidateLabel || store.activeTotem }}</strong>
        <button @click="$router.push('/task4_totem')">进入候选评分</button></div>
    </section>

    <div class="cluster-overview-grid"><ClusterSignalMap/><MatrixDeltaBars/></div>
    <ClusterHeatmap/>
  </section>
</template>
<script setup>
import { computed } from 'vue'
import { useDashboardStore } from '../store/dashboard'
import ClusterHeatmap from '../components/targeting/ClusterHeatmap.vue'
import ClusterSignalMap from '../components/targeting/ClusterSignalMap.vue'
import MatrixDeltaBars from '../components/targeting/MatrixDeltaBars.vue'
const store=useDashboardStore()
const currentCells=computed(()=>store.heatmapMatrixData.length)
const currentTotal=computed(()=>store.heatmapMatrixData.reduce((sum,item)=>sum+item.count,0))
</script>
<style scoped>
.cluster-page{gap:22px}.cluster-control{display:grid;grid-template-columns:1fr auto 1fr;align-items:center;gap:18px}.source-copy span,.source-copy strong,.source-copy small,.selected-signal span,.selected-signal strong{display:block}
.source-copy span,.selected-signal span{color:var(--subtle);font-size:.7rem;font-weight:800}.source-copy strong,.selected-signal strong{margin:5px 0;font-size:1.05rem}.source-copy small{color:var(--muted)}
.segmented{display:flex;padding:4px;border:1px solid var(--border);border-radius:8px;background:#eef3f8}.segmented button{min-height:38px;padding:0 14px;border-radius:6px;background:transparent;font-size:.78rem;font-weight:800}.segmented button.active{color:var(--accent);background:#fff;box-shadow:var(--shadow-soft)}
.selected-signal{text-align:right}.selected-signal button{min-height:34px;padding:0 10px;border:1px solid var(--border);border-radius:6px;color:var(--accent);background:#fff;font-size:.72rem;font-weight:800}
.cluster-overview-grid{display:grid;grid-template-columns:1fr 1fr;gap:18px}
@media(max-width:1000px){.cluster-control{grid-template-columns:1fr}.selected-signal{text-align:left}.cluster-overview-grid{grid-template-columns:1fr}}
</style>
