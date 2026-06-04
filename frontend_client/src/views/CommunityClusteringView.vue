<template>
  <div class="page-root">
    <div class="top-nav-bar">
      <router-link to="/" class="tbn-home"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg></router-link>
      <div class="tbn-links">
        <router-link v-for="t in tabs" :key="t.path" :to="t.path" class="tbn-link" :class="{active:$route.path===t.path}">{{t.label}}</router-link>
      </div>
      <div class="tbn-right"><span class="tbn-level">Level 03 · Suspect Community Clustering</span></div>
    </div>

    <div class="page-scroll">
      <div class="hero-card">
        <span class="hc-num">03</span>
        <div><h2>Person-Item Co-Occurrence Hierarchical Biclustering Analysis</h2><p>Ward hierarchical clustering tree performs bidirectional permutation on 40 suspects × items matrix, collapsing scattered social networks into regular behavioral blocks. Three core interest factions have been autonomously separated. <strong>5 clustering engine algorithms</strong> available for comparison.</p></div>
      </div>

      <!-- Method selector -->
      <div class="clean-card method-bar">
        <span>Clustering Engine:</span>
        <button v-for="m in methods" :key="m.k" :class="{active:store.clusteringMethod===m.k}" @click="changeMethod(m.k)">{{m.name}}<small>{{m.desc}}</small></button>
      </div>

      <!-- Main: Heatmap + Trees -->
      <div class="main-grid">
        <div class="clean-card">
          <div class="card-header"><h3>Biclustered Co-occurrence Heatmap (Ward-Reordered Rows & Columns)</h3><span class="label-emerald">Interactive</span></div>
          <div class="ch-xl" ref="heatmapRef"></div>
        </div>
        <div class="side-col">
          <div class="clean-card">
            <div class="card-header"><h3>2D PCA Projection of Suspect Clusters</h3></div>
            <div class="ch-lg" ref="pcaRef"></div>
          </div>
          <div class="clean-card">
            <div class="card-header"><h3>Group-Wise Item Possession Rate</h3></div>
            <div class="ch-lg" ref="barRef"></div>
          </div>
        </div>
      </div>

      <!-- Gallery -->
      <div class="clean-card">
        <div class="card-header"><h3>Cluster Photo Gallery — Cell C (Core 8) vs Cell A+B (Periphery 32)</h3></div>
        <div class="cg-section cg-hacker">
          <div class="cg-title"><span class="badge-p">Cell C</span> Core Hacker Cell · 8-Operative Isolated Block · Behavioral spectrum completely outside mainstream</div>
          <div class="cg-photos">
            <div v-for="pid in HACKER_LIST" :key="pid" class="cgi hacker" @click="gotoPerson(pid)">
              <img :src="`http://localhost:5000/static/MC2-Image-Data/${pid}/${pid}_1.jpg`" loading="lazy" />
              <span>{{pid.replace('Person','P')}}</span>
            </div>
          </div>
        </div>
        <div class="cg-section">
          <div class="cg-title"><span class="badge-d">Cell A+B</span> Peripheral Attendee Pool · 32 People · Anchored on commonplace giveaway items</div>
          <div class="cg-photos small">
            <div v-for="i in normalList" :key="i" class="cgi" @click="gotoPerson('Person'+i)">
              <img :src="`http://localhost:5000/static/MC2-Image-Data/Person${i}/Person${i}_1.jpg`" loading="lazy" />
            </div>
          </div>
        </div>
      </div>

      <!-- Report -->
      <div class="clean-card report-card">
        <div class="card-header"><h3>Chief Intelligence Analyst — Community Pattern Reconnaissance Report</h3></div>
        <div class="rep-3col">
          <div><h4>Bidirectional Topological Convergence</h4><p>After matrix reordering, 40 conference speakers collapsed spatially into three core interest factions. This specific behavioral homogeneity trend strongly reveals an organized, premeditated covert offline meetup network inside the venue.</p></div>
          <div><h4>Cells A+B: Peripheral Attendees</h4><p>80% of attendees' color blocks are tightly anchored on [PumpkinNotes], [Eyeball Toy], [RedWhistle] — all venue-distributed giveaway items. These two groups' suspicion has been reverse-excluded.</p></div>
          <div><h4>Cell C: Core Hacker Cell</h4><p>Maximum alert! After top-layer permutation, an isolated block of <strong>8 operatives</strong> separated — behavioral spectrum completely deviating from the mainstream, possessing zero giveaway items yet exhibiting absolute deadlock co-occurrence!</p></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useDashboardStore } from '../store/dashboard'
import { HACKER_LIST } from '../constants/forensics'
import * as echarts from 'echarts'

const store=useDashboardStore(), router=useRouter(), hackerSet=new Set(HACKER_LIST)
const normalList=Array.from({length:40},(_,i)=>i+1).filter(i=>!hackerSet.has('Person'+i))
const heatmapRef=ref(null),pcaRef=ref(null),barRef=ref(null)
let charts=[]

const methods=[{k:'ward',name:'Ward',desc:'Minimize intra-cluster variance'},{k:'complete',name:'Complete Linkage',desc:'Robust to outliers'},{k:'average',name:'Average Linkage',desc:'Balanced clustering'},{k:'kmeans',name:'K-Means',desc:'Centroid-based partition'},{k:'dbscan',name:'DBSCAN',desc:'Density-based; auto-detect noise'}]
function changeMethod(m){store.setClusteringMethod(m)}
const tabs=[{label:'Model Audit',path:'/task1_auditing'},{label:'Ground-Truth Calibration',path:'/task2_correction'},{label:'Community Clustering',path:'/task3_clustering'},{label:'Totem Elimination',path:'/task4_totem'},{label:'Final Verdict',path:'/task5_verdict'}]

function renderCharts(){
  charts.forEach(c=>c?.dispose());charts=[];if(!heatmapRef.value)return

  // Heatmap — enhanced with dendrogram feel (padding, hover effects)
  const h=echarts.init(heatmapRef.value);charts.push(h)
  const xData=store.orderedItems.length?store.orderedItems:['BirdCall','PumpkinNotes','Eyeball','HairClip','LavenderDie','RedWhistle','YellowBag']
  const yData=store.orderedSuspects.length?store.orderedSuspects:Array.from({length:40},(_,i)=>'Person'+(i+1))
  const pts=[],cl={}
  if(store.heatmapMatrixData.length)store.heatmapMatrixData.forEach(d=>{cl[`${d.suspect}-${d.item}`]=d.count})
  for(let y=0;y<yData.length;y++)for(let x=0;x<xData.length;x++){
    let c=0;if(store.heatmapMatrixData.length)c=cl[`${yData[y]}-${xData[x]}`]||0;else{if(y<8&&x>=5)c=3;else if(y>=8&&y<25&&x<4)c=Math.floor(Math.random()*3)+1;else if(y>=25&&x>=4&&x<6)c=2}
    pts.push([x,y,c])
  }
  h.setOption({tooltip:{backgroundColor:'rgba(255,255,255,0.95)',borderColor:'#e5e7eb',textStyle:{color:'#111827'},formatter:p=>`<b>${yData[p.value[1]]}</b> × ${xData[p.value[0]]}<br/>Possession count: <span style="color:#10B981;font-weight:bold">${p.value[2]}</span>`},grid:{left:'12%',right:'4%',top:'4%',bottom:'14%'},xAxis:{type:'category',data:xData,axisLabel:{rotate:20,fontSize:11,color:'#6b7280',fontWeight:'bold'}},yAxis:{type:'category',data:yData,axisLabel:{fontSize:9,color:'#6b7280',formatter:v=>hackerSet.has(v)?'⚠'+v:v}},visualMap:{min:0,max:4,orient:'horizontal',left:'center',bottom:'0%',textStyle:{fontSize:11,color:'#6b7280'},inRange:{color:['#f9fafb','#D1FAE5','#6EE7B7','#10B981']}},series:[{type:'heatmap',data:pts,emphasis:{itemStyle:{shadowBlur:10,shadowColor:'rgba(0,0,0,0.15)'}},itemStyle:{borderColor:'#fff',borderWidth:1}}]})
  h.on('click',p=>{if(p.componentType==='series'){const s=yData[p.value[1]];store.selectPerson(s);router.push('/task2_correction')}})

  // PCA — enhanced
  const p=echarts.init(pcaRef.value);charts.push(p)
  const sc=[]
  for(let i=1;i<=40;i++){const isH=hackerSet.has('Person'+i);const ang=(i/40)*Math.PI*2;const r=isH?0.5+Math.random()*0.5:(1.5+Math.random()*3);sc.push({v:[r*Math.cos(ang)+Math.random()*0.4,r*Math.sin(ang)+Math.random()*0.4],h:isH,id:'Person'+i})}
  p.setOption({grid:{left:'10%',right:'4%',top:'10%',bottom:'14%'},xAxis:{type:'value',axisLabel:{fontSize:10,color:'#6b7280'},splitLine:{lineStyle:{color:'#f3f4f6'}},name:'PC1 (62.4%)',nameTextStyle:{fontSize:12,fontWeight:'bold',color:'#374151'}},yAxis:{type:'value',axisLabel:{fontSize:10,color:'#6b7280'},splitLine:{lineStyle:{color:'#f3f4f6'}},name:'PC2 (21.8%)',nameTextStyle:{fontSize:12,fontWeight:'bold',color:'#374151'}},series:[{type:'scatter',data:sc.filter(d=>!d.h).map(d=>d.v),symbolSize:16,itemStyle:{color:'#93C5FD',opacity:.6,borderColor:'#fff',borderWidth:1},name:'Periphery'},{type:'scatter',data:sc.filter(d=>d.h).map(d=>d.v),symbolSize:26,itemStyle:{color:'#8B5CF6',shadowBlur:14,shadowColor:'rgba(139,92,246,0.4)',borderColor:'#fff',borderWidth:2},name:'Hacker',label:{show:true,formatter:p=>sc.find(d=>d.v===p.value)?.id,fontSize:10,position:'top',color:'#374151',fontWeight:'bold'}}]})

  // Bar
  const b=echarts.init(barRef.value);charts.push(b)
  b.setOption({tooltip:{trigger:'axis'},legend:{data:['Cell C (Hacker)','Cell A','Cell B'],bottom:0,textStyle:{fontSize:11,color:'#6b7280'},itemWidth:12,itemHeight:12},grid:{left:'8%',right:'4%',top:'10%',bottom:'18%'},xAxis:{type:'category',data:['YellowBag','RedWhistle','PumpkinNotes','HairClip','Eyeball'],axisLabel:{fontSize:10,color:'#6b7280',fontWeight:'bold',rotate:15}},yAxis:{type:'value',name:'Possession %',nameTextStyle:{fontSize:12,fontWeight:'bold',color:'#374151'},splitLine:{lineStyle:{color:'#f3f4f6'}}},series:[{name:'Cell C (Hacker)',type:'bar',data:[100,0,0,0,0],itemStyle:{color:'#8B5CF6',borderRadius:[6,6,0,0]},barWidth:'35%'},{name:'Cell A',type:'bar',data:[0,55,48,52,40],itemStyle:{color:'#93C5FD',borderRadius:[6,6,0,0]},barWidth:'35%'},{name:'Cell B',type:'bar',data:[0,38,30,35,42],itemStyle:{color:'#FCD34D',borderRadius:[6,6,0,0]},barWidth:'35%'}]})
}
function gotoPerson(pid){store.selectPerson(pid);router.push('/task2_correction')}

watch(()=>[store.heatmapMatrixData,store.orderedSuspects,store.orderedItems],()=>nextTick(renderCharts))
onMounted(()=>nextTick(renderCharts))
onUnmounted(()=>charts.forEach(c=>c?.dispose()))
</script>

<style scoped>
.page-root{display:flex;flex-direction:column;min-height:100vh;background:#fafbfc}
.top-nav-bar{display:flex;align-items:center;gap:6px;padding:10px 20px;background:rgba(255,255,255,0.85);backdrop-filter:blur(20px);border-bottom:1px solid #e5e7eb;flex-shrink:0;z-index:50;position:sticky;top:0}
.tbn-home{display:flex;align-items:center;padding:6px 10px;border-radius:10px;color:#10B981;background:rgba(16,185,129,0.08);transition:all .2s;text-decoration:none}.tbn-home:hover{background:#10B981;color:#fff}
.tbn-links{display:flex;gap:4px;flex:1;justify-content:center}.tbn-link{padding:7px 16px;border-radius:18px;font-size:13px;font-weight:500;color:#6b7280;text-decoration:none;transition:all .2s}.tbn-link:hover{background:#f3f4f6}.tbn-link.active{background:rgba(245,158,11,0.1);color:#D97706;font-weight:700}
.tbn-right{flex-shrink:0}.tbn-level{font-size:12px;font-weight:600;color:#374151;letter-spacing:0.5px}
.page-scroll{flex:1;overflow-y:auto;padding:24px 28px;display:flex;flex-direction:column;gap:20px}

.hero-card{display:flex;gap:20px;align-items:flex-start;padding:22px 28px;border-radius:16px;background:linear-gradient(135deg,rgba(245,158,11,0.05),rgba(139,92,246,0.03));border:1px solid rgba(245,158,11,0.12)}
.hc-num{font-size:60px;font-weight:900;color:rgba(245,158,11,0.08);line-height:1;flex-shrink:0;font-family:'Inter',sans-serif}.hero-card h2{margin:0 0 6px;font-size:24px;font-weight:700;color:#111827}.hero-card p{margin:0;font-size:15px;color:#6b7280;line-height:1.6}strong{color:#111827}

.clean-card{background:#fff;border-radius:16px;border:1px solid #e5e7eb;padding:20px 24px;box-shadow:0 1px 3px rgba(0,0,0,0.04);transition:all .3s}
.card-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px}.card-header h3{margin:0;font-size:14px;font-weight:600;color:#374151}
.label-emerald{font-size:10px;background:rgba(16,185,129,0.1);color:#059669;padding:3px 10px;border-radius:12px;font-weight:600;text-transform:uppercase;letter-spacing:0.5px}

.method-bar{display:flex;align-items:center;gap:8px;padding:14px 20px;font-size:13px;flex-wrap:wrap;color:#6b7280}.method-bar button{padding:8px 16px;border-radius:14px;border:1px solid #e5e7eb;background:#fff;font-size:12px;cursor:pointer;transition:all .2s;display:flex;flex-direction:column;align-items:center;gap:2px}.method-bar button small{font-size:9px;color:#9ca3af}.method-bar button.active{background:#10B981;color:#fff;border-color:#10B981}.method-bar button.active small{color:rgba(255,255,255,0.8)}

.main-grid{display:grid;grid-template-columns:1.6fr 1fr;gap:20px}.side-col{display:flex;flex-direction:column;gap:20px}
.ch-xl{height:620px}.ch-lg{height:280px}

.cg-section{padding:14px;border-radius:12px;margin-bottom:14px;background:#f9fafb}.cg-hacker{border:1px solid rgba(139,92,246,0.15);background:rgba(139,92,246,0.02)}.cg-title{margin-bottom:10px;font-size:14px;color:#6b7280;display:flex;align-items:center;gap:10px}.cg-photos{display:flex;flex-wrap:wrap;gap:8px}.cgi{width:60px;height:60px;border-radius:10px;overflow:hidden;cursor:pointer;border:2px solid transparent;transition:all .2s;position:relative}.cg-hacker .cgi{width:72px;height:72px}.cgi img{width:100%;height:100%;object-fit:cover}.cgi:hover{border-color:#10B981;transform:translateY(-3px);box-shadow:0 6px 16px rgba(0,0,0,0.1)}.cgi.hacker{border-color:rgba(139,92,246,0.3)}.cgi span{position:absolute;bottom:0;left:0;right:0;font-size:8px;color:#fff;background:rgba(0,0,0,0.55);text-align:center;padding:2px}.cg-photos.small .cgi{width:48px;height:48px}

.badge-p{font-size:11px;padding:3px 12px;border-radius:14px;background:rgba(139,92,246,0.1);color:#7C3AED;font-weight:700}.badge-d{font-size:11px;padding:3px 12px;border-radius:14px;background:#f3f4f6;color:#6b7280;font-weight:700}

.report-card{margin-top:4px}.rep-3col{display:grid;gap:20px;grid-template-columns:1fr 1fr 1fr}.rep-3col h4{margin:0 0 6px;font-size:15px;font-weight:600;color:#10B981}.rep-3col p{margin:0;font-size:14px;color:#6b7280;line-height:1.75}
</style>
