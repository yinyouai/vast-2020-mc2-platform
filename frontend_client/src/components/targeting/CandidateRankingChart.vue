<template>
  <section class="panel ranking-chart-panel">
    <div class="panel-header">
      <div><span class="section-kicker">综合评分构成</span><h4 class="panel-title">候选暗号排名</h4>
        <p class="visible-subtitle">颜色拆分人数特异性、稳定性、图片和文本贡献。</p></div>
      <span class="data-chip">点击选择候选</span>
    </div>
    <div ref="chartRef" class="ranking-chart"></div>
  </section>
</template>
<script setup>
import { computed,onBeforeUnmount,onMounted,ref,watch } from 'vue'
import * as echarts from 'echarts'
import { useDashboardStore } from '../../store/dashboard'
import { buildTooltip,chartPalette,splitLine } from '../../utils/chartTheme'
const store=useDashboardStore();const chartRef=ref(null);let chart
const rows=computed(()=>[...store.candidateRankings].reverse())
const component=(row,key)=>row.score_components?.[key]||0
const render=()=>{if(!chartRef.value)return;if(!chart)chart=echarts.init(chartRef.value)
  const makeSeries=(name,key,color)=>({name,type:'bar',stack:'score',barMaxWidth:22,data:rows.value.map((row)=>({
    value:component(row,key),itemStyle:{color,opacity:store.excludedItems.includes(row.label)?.2:1,
      borderColor:row.label===store.selectedCandidateLabel?'#17324d':'transparent',borderWidth:row.label===store.selectedCandidateLabel?1:0}
  }))})
  chart.setOption({tooltip:{...buildTooltip((params)=>{const list=Array.isArray(params)?params:[];const row=rows.value[params[0]?.dataIndex]
      return `<strong>${row?.label}</strong><br/>综合分 ${row?.score.toFixed(4)}<br/>拥有者 ${row?.owner_count} 人 · 最少 ${row?.min_occurrence} 次<br/>${list.map((item)=>`${item.marker}${item.seriesName} ${(item.value*100).toFixed(1)}`).join('<br/>')}`}),trigger:'axis'},
    legend:{top:0,data:['人数特异性','重复稳定性','图片证据','文本支持'],textStyle:{color:chartPalette.muted,fontSize:11}},
    grid:{left:116,right:48,top:42,bottom:30},xAxis:{type:'value',max:1,name:'综合分',axisLabel:{color:chartPalette.muted},splitLine},
    yAxis:{type:'category',data:rows.value.map((row)=>row.label),axisLabel:{color:(value)=>value===store.selectedCandidateLabel?chartPalette.accent:chartPalette.muted,fontWeight:(value)=>value===store.selectedCandidateLabel?800:500,fontSize:10},axisTick:{show:false},axisLine:{show:false}},
    series:[makeSeries('人数特异性','specificity','#2f7df6'),makeSeries('重复稳定性','stability','#24956f'),makeSeries('图片证据','visual','#d99522'),makeSeries('文本支持','text','#8d6ccf')]},true)
  chart.off('click');chart.on('click',(params)=>store.selectCandidate(params.name))}
watch(()=>[store.candidateRankings,store.selectedCandidateLabel,store.excludedItems],render,{deep:true})
onMounted(()=>{render();window.addEventListener('resize',render)});onBeforeUnmount(()=>{window.removeEventListener('resize',render);chart?.dispose()})
</script>
<style scoped>
.section-kicker{color:var(--subtle);font-size:.7rem;font-weight:800}.visible-subtitle{display:block!important;margin:5px 0 0;color:var(--muted);font-size:.76rem}.ranking-chart{min-height:420px}
</style>
