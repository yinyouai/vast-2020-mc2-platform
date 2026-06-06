<template>
  <section class="panel delta-panel">
    <div class="panel-header">
      <div><span class="section-kicker">校正影响</span><h4 class="panel-title">原始预测与校正拥有者</h4>
        <p class="visible-subtitle">比较同一候选在两层数据中的人员覆盖变化。</p></div>
    </div>
    <div ref="chartRef" class="delta-chart"></div>
  </section>
</template>
<script setup>
import { computed,onBeforeUnmount,onMounted,ref,watch } from 'vue'
import * as echarts from 'echarts'
import { useDashboardStore } from '../../store/dashboard'
import { buildTooltip,chartPalette,splitLine } from '../../utils/chartTheme'
const store=useDashboardStore();const chartRef=ref(null);let chart
const ownerCounts=(cells=[])=>{const map=new Map();cells.forEach((cell)=>{if(!map.has(cell.item))map.set(cell.item,new Set());map.get(cell.item).add(cell.suspect)});return new Map([...map].map(([key,set])=>[key,set.size]))}
const rows=computed(()=>{const raw=ownerCounts(store.rawMatrixSnapshot.cells);const corrected=ownerCounts(store.correctedMatrixSnapshot.cells)
  return store.candidateRankings.map((item)=>({label:item.label,raw:raw.get(item.label)||0,corrected:corrected.get(item.label)||0})).reverse()})
const render=()=>{if(!chartRef.value)return;if(!chart)chart=echarts.init(chartRef.value)
  chart.setOption({color:['#9cb5cf',chartPalette.green],tooltip:{...buildTooltip(),trigger:'axis'},legend:{top:0,textStyle:{color:chartPalette.muted},data:['原始预测','人工校正']},
    grid:{left:116,right:22,top:40,bottom:28},xAxis:{type:'value',name:'拥有者人数',axisLabel:{color:chartPalette.muted},splitLine},
    yAxis:{type:'category',data:rows.value.map((row)=>row.label),axisLabel:{color:(value)=>value===store.selectedCandidateLabel?chartPalette.accent:chartPalette.muted,fontSize:10},axisTick:{show:false},axisLine:{show:false}},
    series:[{name:'原始预测',type:'bar',barMaxWidth:12,data:rows.value.map((row)=>row.raw),itemStyle:{borderRadius:[0,4,4,0]}},
      {name:'人工校正',type:'bar',barMaxWidth:12,data:rows.value.map((row)=>row.corrected),itemStyle:{borderRadius:[0,4,4,0]}}]},true)
  chart.off('click');chart.on('click',(params)=>store.selectCandidate(params.name))}
watch(()=>[rows.value,store.selectedCandidateLabel],render,{deep:true})
onMounted(()=>{render();window.addEventListener('resize',render)});onBeforeUnmount(()=>{window.removeEventListener('resize',render);chart?.dispose()})
</script>
<style scoped>
.section-kicker{color:var(--subtle);font-size:.7rem;font-weight:800}.visible-subtitle{display:block!important;margin:5px 0 0;color:var(--muted);font-size:.76rem}.delta-chart{min-height:350px}
</style>
