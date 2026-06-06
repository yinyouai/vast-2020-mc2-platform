<template>
  <section class="panel flow-panel">
    <div class="panel-header">
      <div><span class="section-kicker">规则淘汰路径</span><h4 class="panel-title">候选暗号流动图</h4>
        <p class="visible-subtitle">候选依次经过人数条件和重复出现条件。</p></div>
      <div class="flow-stats"><b>{{ visibleCandidates.length }}</b><span>当前可见候选</span></div>
    </div>
    <div ref="chartRef" class="flow-chart"></div>
  </section>
</template>
<script setup>
import { computed,onBeforeUnmount,onMounted,ref,watch } from 'vue'
import * as echarts from 'echarts'
import { useDashboardStore } from '../../store/dashboard'
import { buildTooltip,chartPalette } from '../../utils/chartTheme'
const store=useDashboardStore();const chartRef=ref(null);let chart
const visibleCandidates=computed(()=>store.candidateRankings.filter((item)=>!store.excludedItems.includes(item.label)))
const buildGraph=()=>{const nodes=[];const links=[];const add=(name,color)=>{if(!nodes.some((node)=>node.name===name))nodes.push({name,itemStyle:{color}})}
  visibleCandidates.value.forEach((item)=>{add(item.label,item.label===store.activeTotem?chartPalette.gold:'#8fa8c2')
    const sizeGate=item.exact_target_size?'人数恰好 8':'人数不匹配';add(sizeGate,item.exact_target_size?chartPalette.accent:'#c7d1dc');links.push({source:item.label,target:sizeGate,value:1})
    if(item.exact_target_size){const stable=item.min_occurrence>=2?'每人至少 2 次':'仅单次出现';add(stable,item.min_occurrence>=2?chartPalette.green:'#d9a95f');links.push({source:sizeGate,target:stable,value:1})
      const result=item.min_occurrence>=2?'最终暗号':'稳定性淘汰';add(result,item.min_occurrence>=2?chartPalette.gold:'#d6dde5');links.push({source:stable,target:result,value:1})
    }else{add('覆盖范围淘汰','#d6dde5');links.push({source:sizeGate,target:'覆盖范围淘汰',value:1})}});return{nodes,links}}
const render=()=>{if(!chartRef.value)return;if(!chart)chart=echarts.init(chartRef.value);const graph=buildGraph()
  chart.setOption({tooltip:buildTooltip((params)=>params.dataType==='edge'?`${params.data.source} → ${params.data.target}`:`<strong>${params.name}</strong>`),
    series:[{type:'sankey',data:graph.nodes,links:graph.links,left:8,right:12,top:12,bottom:14,nodeWidth:16,nodeGap:10,draggable:false,
      emphasis:{focus:'adjacency'},lineStyle:{color:'gradient',curveness:.5,opacity:.36},label:{color:chartPalette.text,fontSize:10}}]},true)
  chart.off('click');chart.on('click',(params)=>{if(store.candidateRankings.some((item)=>item.label===params.name))store.selectCandidate(params.name)})}
watch(()=>[store.candidateRankings,store.excludedItems],render,{deep:true});onMounted(()=>{render();window.addEventListener('resize',render)});onBeforeUnmount(()=>{window.removeEventListener('resize',render);chart?.dispose()})
</script>
<style scoped>
.section-kicker{color:var(--subtle);font-size:.7rem;font-weight:800}.visible-subtitle{display:block!important;margin:5px 0 0;color:var(--muted);font-size:.76rem}.flow-stats{text-align:right}.flow-stats b,.flow-stats span{display:block}.flow-stats b{font-size:1.4rem;color:var(--accent)}.flow-stats span{color:var(--muted);font-size:.7rem}.flow-chart{min-height:390px}
</style>
