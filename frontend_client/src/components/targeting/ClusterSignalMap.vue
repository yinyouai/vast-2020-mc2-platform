<template>
  <section class="panel signal-map-panel">
    <div class="panel-header">
      <div><span class="section-kicker">候选结构空间</span><h4 class="panel-title">人数与稳定性分布</h4>
        <p class="visible-subtitle">越接近 8 人且越靠上，越符合稳定暗号物品特征。</p></div>
      <span class="data-chip">点大小 = 图片证据</span>
    </div>
    <div ref="chartRef" class="signal-chart"></div>
  </section>
</template>
<script setup>
import { onBeforeUnmount,onMounted,ref,watch } from 'vue'
import * as echarts from 'echarts'
import { useDashboardStore } from '../../store/dashboard'
import { buildTooltip,chartPalette,splitLine } from '../../utils/chartTheme'
const store=useDashboardStore();const chartRef=ref(null);let chart
const render=()=>{
  if(!chartRef.value)return;if(!chart)chart=echarts.init(chartRef.value)
  const data=store.candidateRankings.map((item)=>({
    name:item.label,value:[item.owner_count,item.stable_owner_ratio,item.evidence_image_count,item.score],
    itemStyle:{color:item.label===store.activeTotem?chartPalette.gold:item.exact_target_size?chartPalette.accent:chartPalette.cyan,
      borderColor:item.label===store.selectedCandidateLabel?'#17324d':'#fff',borderWidth:item.label===store.selectedCandidateLabel?3:1}
  }))
  chart.setOption({
    tooltip:buildTooltip(({data:item})=>`<strong>${item.name}</strong><br/>拥有者 ${item.value[0]} 人<br/>稳定率 ${Math.round(item.value[1]*100)}%<br/>证据图 ${item.value[2]}<br/>综合分 ${item.value[3].toFixed(4)}`),
    grid:{left:52,right:20,top:18,bottom:42},
    xAxis:{type:'value',min:6,max:11,interval:1,name:'拥有者人数',axisLabel:{color:chartPalette.muted},splitLine,
      axisLine:{lineStyle:{color:chartPalette.lineStrong}}},
    yAxis:{type:'value',min:0,max:1,name:'稳定率',axisLabel:{color:chartPalette.muted,formatter:(v)=>`${Math.round(v*100)}%`},splitLine},
    series:[{type:'scatter',data,symbolSize:(value)=>Math.max(16,Math.min(46,14+value[2]*1.2)),
      label:{show:true,position:'top',formatter:'{b}',color:chartPalette.text,fontSize:10},
      markLine:{silent:true,symbol:'none',lineStyle:{color:chartPalette.gold,type:'dashed'},label:{color:chartPalette.gold},
        data:[{xAxis:8,name:'目标 8 人'},{yAxis:1,name:'全部稳定'}]}
    }]
  },true)
  chart.off('click');chart.on('click',(params)=>store.selectCandidate(params.name))
}
watch(()=>[store.candidateRankings,store.selectedCandidateLabel],render,{deep:true})
onMounted(()=>{render();window.addEventListener('resize',render)})
onBeforeUnmount(()=>{window.removeEventListener('resize',render);chart?.dispose()})
</script>
<style scoped>
.section-kicker{color:var(--subtle);font-size:.7rem;font-weight:800}.visible-subtitle{display:block!important;margin:5px 0 0;color:var(--muted);font-size:.76rem}.signal-chart{min-height:350px}
</style>
