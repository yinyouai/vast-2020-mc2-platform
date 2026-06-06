<template>
  <section class="panel network-panel">
    <div class="panel-header">
      <div><span class="section-kicker">物品—人员关系</span><h4 class="panel-title">最终 8 人证据网络</h4>
        <p class="visible-subtitle">边宽表示图片出现次数；金色描边表示存在直接文本支持。</p></div>
      <div class="network-legend"><span><i class="hit"></i>模型检出</span><span><i class="miss"></i>人工补标</span></div>
    </div>
    <div ref="chartRef" class="network-chart"></div>
  </section>
</template>
<script setup>
import { onBeforeUnmount,onMounted,ref,watch } from 'vue'
import * as echarts from 'echarts'
import { useDashboardStore } from '../../store/dashboard'
import { buildTooltip,chartPalette } from '../../utils/chartTheme'
const store=useDashboardStore();const chartRef=ref(null);let chart
const render=()=>{if(!chartRef.value)return;if(!chart)chart=echarts.init(chartRef.value)
  const center={id:store.activeTotem,name:store.activeTotem,symbolSize:86,itemStyle:{color:chartPalette.gold,borderColor:'#fff',borderWidth:3},label:{fontWeight:800}}
  const people=store.finalEvidence.map((item)=>({id:item.person_id,name:item.person_id,symbolSize:38+item.occurrence_count*4,value:item,
    itemStyle:{color:item.raw_detected?chartPalette.green:chartPalette.accent,borderColor:item.text_snippets.length?chartPalette.gold:'#fff',borderWidth:item.text_snippets.length?4:2}}))
  const links=store.finalEvidence.map((item)=>({source:store.activeTotem,target:item.person_id,value:item.occurrence_count,lineStyle:{width:1.5+item.occurrence_count*.9,color:item.raw_detected?chartPalette.green:chartPalette.accent,opacity:.5}}))
  chart.setOption({tooltip:buildTooltip((params)=>{if(params.dataType==='edge')return `${params.data.target}：${params.data.value} 张图片`
      if(params.data.id===store.activeTotem)return `<strong>${store.activeTotem}</strong><br/>最终暗号物品`
      const item=params.data.value;return `<strong>${item.person_id}</strong><br/>图片 ${item.occurrence_count} 张<br/>${item.raw_detected?`模型最高 ${item.raw_max_score}`:'模型漏检'}<br/>文本 ${item.text_snippets.length} 条`}),
    series:[{type:'graph',layout:'circular',circular:{rotateLabel:true},roam:true,data:[center,...people],links,
      label:{show:true,position:'right',color:chartPalette.text,fontSize:10},lineStyle:{curveness:.08},emphasis:{focus:'adjacency',lineStyle:{opacity:1}}}]},true)
  chart.off('click');chart.on('click',(params)=>{if(params.dataType==='node'&&params.data.id!==store.activeTotem)store.selectPerson(params.data.id)})}
watch(()=>[store.finalEvidence,store.activeTotem],render,{deep:true});onMounted(()=>{render();window.addEventListener('resize',render)});onBeforeUnmount(()=>{window.removeEventListener('resize',render);chart?.dispose()})
</script>
<style scoped>
.section-kicker{color:var(--subtle);font-size:.7rem;font-weight:800}.visible-subtitle{display:block!important;margin:5px 0 0;color:var(--muted);font-size:.76rem}.network-legend{display:flex;gap:10px;color:var(--muted);font-size:.7rem}.network-legend span{display:flex;align-items:center;gap:5px}.network-legend i{width:10px;height:10px;border-radius:50%}.hit{background:#24956f}.miss{background:#2f7df6}.network-chart{min-height:460px}
</style>
