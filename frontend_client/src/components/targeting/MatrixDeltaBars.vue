<template>
  <section class="panel delta-panel">
    <div class="panel-header">
      <div><span class="section-kicker">校正影响</span><h4 class="panel-title">原始预测与校正拥有者</h4>
        <p class="visible-subtitle">比较同一候选在两层数据中的人员覆盖变化。</p></div>
      <div class="series-legend" aria-label="前后对比图例">
        <span><i class="raw"></i>原始预测</span>
        <span><i class="corrected"></i>人工校正</span>
      </div>
    </div>
    <div ref="chartRef" class="delta-chart"></div>
    <div v-if="selectedRow" class="comparison-detail">
      <header>
        <div><span>当前联动候选</span><strong>{{ selectedRow.label }}</strong></div>
        <div class="delta-value" :class="{positive:selectedRow.delta>0,negative:selectedRow.delta<0}">
          {{ selectedRow.delta > 0 ? '+' : '' }}{{ selectedRow.delta }} 人
        </div>
      </header>
      <div class="owner-columns">
        <section>
          <div><span>校正前</span><b>{{ selectedRow.rawOwners.length }} 人</b></div>
          <p v-if="selectedRow.rawOwners.length">
            <button v-for="person in selectedRow.rawOwners" :key="`raw-${person}`" type="button" @click="selectPerson(person)">{{ person }}</button>
          </p>
          <small v-else>原始模型未形成拥有者记录</small>
        </section>
        <section>
          <div><span>校正后</span><b>{{ selectedRow.correctedOwners.length }} 人</b></div>
          <p v-if="selectedRow.correctedOwners.length">
            <button v-for="person in selectedRow.correctedOwners" :key="`corrected-${person}`" type="button" @click="selectPerson(person)">{{ person }}</button>
          </p>
          <small v-else>人工校正层未保留该候选</small>
        </section>
      </div>
    </div>
  </section>
</template>
<script setup>
import { computed,onBeforeUnmount,onMounted,ref,watch } from 'vue'
import * as echarts from 'echarts'
import { useDashboardStore } from '../../store/dashboard'
import { buildTooltip,chartPalette,splitLine } from '../../utils/chartTheme'
const store=useDashboardStore();const chartRef=ref(null);let chart;let resizeObserver
const ownerSets=(cells=[])=>{const map=new Map();cells.forEach((cell)=>{if(!map.has(cell.item))map.set(cell.item,new Set());map.get(cell.item).add(cell.suspect)});return map}
const personNumber=(person='')=>Number(person.replace('Person',''))||999
const rows=computed(()=>{
  const raw=ownerSets(store.rawMatrixSnapshot.cells);const corrected=ownerSets(store.correctedMatrixSnapshot.cells)
  return store.candidateRankings.map((item)=>{
    const rawOwners=[...(raw.get(item.label)||[])].sort((a,b)=>personNumber(a)-personNumber(b))
    const correctedOwners=[...(corrected.get(item.label)||[])].sort((a,b)=>personNumber(a)-personNumber(b))
    return {label:item.label,raw:rawOwners.length,corrected:correctedOwners.length,delta:correctedOwners.length-rawOwners.length,rawOwners,correctedOwners}
  }).reverse()
})
const selectedRow=computed(()=>rows.value.find((row)=>row.label===store.selectedCandidateLabel)||rows.value.at(-1)||null)
const render=()=>{if(!chartRef.value)return;if(!chart)chart=echarts.init(chartRef.value)
  const series=[
    {name:'原始预测',type:'bar',barMaxWidth:12,data:rows.value.map((row)=>row.raw),itemStyle:{color:'#9cb5cf',borderRadius:[0,4,4,0]}},
    {name:'人工校正',type:'bar',barMaxWidth:12,data:rows.value.map((row)=>row.corrected),itemStyle:{color:chartPalette.green,borderRadius:[0,4,4,0]}}
  ]
  chart.setOption({color:['#9cb5cf',chartPalette.green],tooltip:{...buildTooltip(),trigger:'axis'},legend:{show:false},
    grid:{left:116,right:22,top:40,bottom:28},xAxis:{type:'value',name:'拥有者人数',axisLabel:{color:chartPalette.muted},splitLine},
    yAxis:{type:'category',data:rows.value.map((row)=>row.label),axisLabel:{color:(value)=>value===store.selectedCandidateLabel?chartPalette.accent:chartPalette.muted,fontSize:10},axisTick:{show:false},axisLine:{show:false}},
    series},true)
  chart.off('click');chart.on('click',(params)=>{const row=rows.value[params.dataIndex];if(row)store.selectCandidate(row.label)})}
const selectPerson=(person)=>store.selectPerson(person)
watch(()=>[rows.value,store.selectedCandidateLabel],render,{deep:true})
onMounted(()=>{
  render()
  resizeObserver=new ResizeObserver(()=>chart?.resize())
  if(chartRef.value)resizeObserver.observe(chartRef.value)
})
onBeforeUnmount(()=>{resizeObserver?.disconnect();chart?.dispose()})
</script>
<style scoped>
.delta-panel{display:flex;flex-direction:column;min-width:0;overflow:hidden}.delta-panel .panel-header{flex-wrap:wrap}.delta-panel .panel-header>div:first-child{min-width:220px;flex:1}
.section-kicker{color:var(--subtle);font-size:.7rem;font-weight:800}.visible-subtitle{display:block!important;margin:5px 0 0;color:var(--muted);font-size:.76rem;line-height:1.55}.delta-chart{width:100%;min-width:0;min-height:370px}
.series-legend{display:flex;flex-wrap:wrap;gap:12px;color:var(--muted);font-size:.68rem;font-weight:800}.series-legend span{display:flex;align-items:center;gap:6px}.series-legend i{width:16px;height:7px;border-radius:3px}.series-legend i.raw{background:#9cb5cf}.series-legend i.corrected{background:var(--success)}
.comparison-detail{margin-top:8px;padding:12px;border: none;border-radius: 12px;background: var(--surface)}.comparison-detail>header{display:flex;align-items:center;justify-content:space-between;gap:10px}.comparison-detail header span,.comparison-detail header strong{display:block}.comparison-detail header span{color:var(--subtle);font-size:.65rem;font-weight:800}.comparison-detail header strong{margin-top:4px;font-size:.9rem}.delta-value{padding:5px 8px;border-radius: 12px;color:var(--muted);background: var(--surface-3);font-size:.75rem;font-weight:900}.delta-value.positive{color: var(--success);background: rgba(16, 185, 129, 0.1)}.delta-value.negative{color:var(--danger);background: rgba(244, 63, 94, 0.1)}
.owner-columns{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:10px}.owner-columns section{min-width:0;padding:9px;border: none;border-radius: 12px;background: var(--surface)}.owner-columns section>div{display:flex;align-items:center;justify-content:space-between;gap:8px}.owner-columns span{color:var(--muted);font-size:.7rem;font-weight:800}.owner-columns b{font-size:.72rem}.owner-columns p{display:flex!important;flex-wrap:wrap;gap:5px;margin:8px 0 0}.owner-columns button{min-height:28px;padding:0 7px;border: none;border-radius: 12px;color:var(--text);background: var(--surface-3);font-size:.65rem;font-weight:700}.owner-columns button:hover,.owner-columns button:focus-visible{border-color:var(--accent);color:var(--accent)}.owner-columns small{display:block;margin-top:8px;color:var(--subtle);font-size:.68rem}
@media(max-width:650px){.owner-columns{grid-template-columns:1fr}.delta-chart{min-height:330px}}
</style>
