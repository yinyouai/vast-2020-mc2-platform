<template>
  <section class="panel evidence-matrix-panel">
    <div class="panel-header"><div><span class="section-kicker">逐人完整性</span><h4 class="panel-title">成员证据矩阵</h4>
      <p class="visible-subtitle">颜色越深，表示该维度证据越完整。</p></div></div>
    <div ref="chartRef" class="matrix-chart"></div>
  </section>
</template>
<script setup>
import { onBeforeUnmount,onMounted,ref,watch } from 'vue'
import * as echarts from 'echarts'
import { useDashboardStore } from '../../store/dashboard'
import { buildTooltip,chartPalette } from '../../utils/chartTheme'
const store=useDashboardStore();const chartRef=ref(null);let chart
const dimensions=['图片数量','模型检出率','文本支持','重复稳定性']
const render=()=>{if(!chartRef.value)return;if(!chart)chart=echarts.init(chartRef.value)
  const data=[];store.finalEvidence.forEach((item,y)=>{const values=[
    {score:Math.min(1,item.occurrence_count/5),display:`${item.occurrence_count} 张`},
    {score:item.image_ids.length?item.raw_detection_images.length/item.image_ids.length:0,display:`${item.raw_detection_images.length}/${item.image_ids.length}`},
    {score:item.text_snippets.length?1:0,display:`${item.text_snippets.length} 条`},
    {score:item.occurrence_count>=2?1:item.occurrence_count/2,display:item.occurrence_count>=2?'通过':'不足'}
  ];values.forEach((value,x)=>data.push({value:[x,y,value.score],display:value.display,person:item.person_id,dimension:dimensions[x]}))})
  chart.setOption({tooltip:buildTooltip(({data:item})=>`<strong>${item.person}</strong><br/>${item.dimension}：${item.display}`),
    grid:{left:82,right:16,top:14,bottom:52},xAxis:{type:'category',data:dimensions,axisLabel:{color:chartPalette.muted,rotate:25,fontSize:10},axisTick:{show:false}},
    yAxis:{type:'category',data:store.finalEvidence.map((item)=>item.person_id),axisLabel:{color:(value)=>value===store.selectedPersonId?chartPalette.accent:chartPalette.muted,fontWeight:(value)=>value===store.selectedPersonId?800:500,fontSize:10},axisTick:{show:false}},
    visualMap:{show:false,min:0,max:1,inRange:{color:['#edf2f7','#cfe0f7','#73a9e8','var(--success)']}},
    series:[{type:'heatmap',data,label:{show:true,formatter:(params)=>params.data.display,color:'#17324d',fontSize:9},itemStyle:{borderColor: 'var(--border)',borderWidth:3,borderRadius:4},emphasis:{itemStyle:{borderColor:'#17324d',borderWidth:2}}}]},true)
  chart.off('click');chart.on('click',(params)=>store.selectPerson(params.data.person))}
watch(()=>[store.finalEvidence,store.selectedPersonId],render,{deep:true});onMounted(()=>{render();window.addEventListener('resize',render)});onBeforeUnmount(()=>{window.removeEventListener('resize',render);chart?.dispose()})
</script>
<style scoped>
.section-kicker{color:var(--subtle);font-size:.7rem;font-weight:800}.visible-subtitle{display:block!important;margin:5px 0 0;color:var(--muted);font-size:.76rem}.matrix-chart{min-height:460px}
</style>
