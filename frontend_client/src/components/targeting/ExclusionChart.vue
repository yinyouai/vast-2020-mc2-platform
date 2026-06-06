<template>
  <section class="panel exclusion-panel">
    <div class="panel-header"><div><span class="section-kicker">反向验证</span><h4 class="panel-title">非成员模型误检</h4>
      <p class="visible-subtitle">这些人员曾被模型预测为 {{ store.activeTotem || '候选物品' }}，但人工校正未确认。</p></div></div>
    <div ref="chartRef" class="exclusion-chart"></div>
  </section>
</template>
<script setup>
import { computed,onBeforeUnmount,onMounted,ref,watch } from 'vue'
import * as echarts from 'echarts'
import { useDashboardStore } from '../../store/dashboard'
import { buildTooltip,chartPalette,splitLine } from '../../utils/chartTheme'
const store=useDashboardStore();const chartRef=ref(null);let chart
const rows=computed(()=>[...(store.analysisSummary?.final?.excluded_nonmembers||[])].reverse())
const render=()=>{if(!chartRef.value)return;if(!chart)chart=echarts.init(chartRef.value)
  chart.setOption({tooltip:buildTooltip(({data,item})=>`<strong>${item?.person_id||data.person_id}</strong><br/>最高分 ${data.value}<br/>图片 ${data.image_id}<br/>人工校正未确认`),
    grid:{left:82,right:24,top:10,bottom:32},xAxis:{type:'value',min:0,max:1,name:'最高置信度',axisLabel:{color:chartPalette.muted},splitLine},
    yAxis:{type:'category',data:rows.value.map((item)=>item.person_id),axisLabel:{color:chartPalette.muted,fontSize:10},axisLine:{show:false},axisTick:{show:false}},
    series:[{type:'bar',barMaxWidth:15,data:rows.value.map((item)=>({value:item.max_score,person_id:item.person_id,image_id:item.image_id,itemStyle:{color:'#cf5656',borderRadius:[0,4,4,0]}})),
      label:{show:true,position:'right',formatter:(params)=>params.value.toFixed(3),color:chartPalette.text,fontSize:10},
      markLine:{symbol:'none',label:{formatter:`当前阈值 ${store.scoreThreshold.toFixed(2)}`,color:chartPalette.accent},lineStyle:{color:chartPalette.accent,type:'dashed'},data:[{xAxis:store.scoreThreshold}]}}]},true)}
watch(()=>[rows.value,store.scoreThreshold],render,{deep:true});onMounted(()=>{render();window.addEventListener('resize',render)});onBeforeUnmount(()=>{window.removeEventListener('resize',render);chart?.dispose()})
</script>
<style scoped>
.section-kicker{color:var(--subtle);font-size:.7rem;font-weight:800}.visible-subtitle{display:block!important;margin:5px 0 0;color:var(--muted);font-size:.76rem}.exclusion-chart{min-height:350px}
</style>
