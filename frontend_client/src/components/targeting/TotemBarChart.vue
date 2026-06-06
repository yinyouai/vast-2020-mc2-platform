<template>
  <section class="panel">
    <div class="panel-header"><div><span class="section-kicker">覆盖范围</span><h4 class="panel-title">候选拥有者人数</h4>
      <p class="visible-subtitle">目标线为 8 人，已剔除候选会变淡。</p></div></div>
    <div ref="chartRef" class="coverage-chart"></div>
  </section>
</template>
<script setup>
import { onBeforeUnmount,onMounted,ref,watch } from 'vue'
import * as echarts from 'echarts'
import { buildTooltip,chartPalette,splitLine } from '../../utils/chartTheme'
const props=defineProps({items:{type:Array,default:()=>[]}});const emit=defineEmits(['select']);const chartRef=ref(null);let chart
const render=()=>{if(!chartRef.value)return;if(!chart)chart=echarts.init(chartRef.value)
  chart.setOption({tooltip:buildTooltip((params)=>{const item=props.items[params.dataIndex];return `<strong>${item.name}</strong><br/>拥有者 ${item.ownerCount} 人<br/>覆盖率 ${item.coverage}%<br/>${item.role}`}),
    grid:{left:110,right:24,top:16,bottom:34},xAxis:{type:'value',max:12,name:'人数',axisLabel:{color:chartPalette.muted},splitLine},
    yAxis:{type:'category',data:[...props.items].reverse().map((item)=>item.name),axisLabel:{color:chartPalette.muted,fontSize:10},axisLine:{show:false},axisTick:{show:false}},
    series:[{type:'bar',barMaxWidth:18,data:[...props.items].reverse().map((item)=>({value:item.ownerCount,itemStyle:{color:item.role==='最终候选'?chartPalette.gold:chartPalette.accent,opacity:item.excluded?.18:1,borderRadius:[0,4,4,0]}})),
      label:{show:true,position:'right',color:chartPalette.text,fontSize:10},markLine:{symbol:'none',label:{formatter:'目标 8 人',color:chartPalette.gold},lineStyle:{color:chartPalette.gold,type:'dashed'},data:[{xAxis:8}]}}]},true)
  chart.off('click');chart.on('click',(params)=>emit('select',params.name))}
watch(()=>props.items,render,{deep:true});onMounted(()=>{render();window.addEventListener('resize',render)});onBeforeUnmount(()=>{window.removeEventListener('resize',render);chart?.dispose()})
</script>
<style scoped>
.section-kicker{color:var(--subtle);font-size:.7rem;font-weight:800}.visible-subtitle{display:block!important;margin:5px 0 0;color:var(--muted);font-size:.76rem}.coverage-chart{min-height:390px}
</style>
