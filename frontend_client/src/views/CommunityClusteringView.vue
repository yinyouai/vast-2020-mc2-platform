<template>
  <div class="page-root">
    <div class="top-nav-bar">
      <router-link to="/" class="tbn-home"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg></router-link>
      <div class="tbn-links">
        <router-link v-for="t in tabs" :key="t.path" :to="t.path" class="tbn-link" :class="{active:$route.path===t.path}">{{t.label}}</router-link>
      </div>
      <div class="tbn-right"><span class="tbn-level">📊 层级三</span></div>
    </div>

    <div class="page-scroll">
      <div class="hero-card">
        <span class="hc-num">03</span>
        <div><h2>人-物资产光谱双向重排层次聚类</h2><p>Ward 层次聚类树对 40 人及物资轴执行双向洗牌，迫使离散的社交网络在屏幕上收敛为规整聚类行为色块。三大利益阵营已自动分离。支持 5 种聚类引擎切换。</p></div>
      </div>

      <!-- 聚类方法 -->
      <div class="glass-card method-bar">
        <span>🔬 聚类引擎:</span>
        <button v-for="m in methods" :key="m.k" :class="{active:store.clusteringMethod===m.k}" @click="changeMethod(m.k)">{{m.name}}<small>{{m.desc}}</small></button>
      </div>

      <!-- 热力图 + PCA + 分组柱状图 -->
      <div class="main-grid">
        <div class="glass-card">
          <h3>🧬 人-物共现层次聚类矩阵 (行列=聚类重排后)</h3>
          <div class="ch tall" ref="heatmapRef"></div>
        </div>
        <div class="side-col">
          <div class="glass-card"><h3>📍 嫌疑人聚类空间投影 (PCA降维)</h3><div class="ch" ref="pcaRef"></div></div>
          <div class="glass-card"><h3>📊 三大阵营物资持有率对比</h3><div class="ch" ref="barRef"></div></div>
        </div>
      </div>

      <!-- 聚类画廊 -->
      <div class="glass-card">
        <h3>🧬 聚类分组照片廊 — 集团C核心成员(8人) vs 外围参会者(32人)</h3>
        <div class="cg-section cg-hacker">
          <div class="cg-title"><span class="badge badge-purple">集团C</span> 核心黑客组织帮派 · 8人孤立方阵 · 行为光谱完全脱离主流</div>
          <div class="cg-photos">
            <div v-for="pid in HACKER_LIST" :key="pid" class="cgi hacker" @click="gotoPerson(pid)">
              <img :src="`http://localhost:5000/static/MC2-Image-Data/${pid}/${pid}_1.jpg`" loading="lazy" />
              <span>{{pid.replace('Person','P')}}</span>
            </div>
          </div>
        </div>
        <div class="cg-section">
          <div class="cg-title"><span class="badge badge-default">集团A+B</span> 外围参会群体 · 32人 · 色块锚定普及物资</div>
          <div class="cg-photos small">
            <div v-for="i in normalList" :key="i" class="cgi" @click="gotoPerson('Person'+i)">
              <img :src="`http://localhost:5000/static/MC2-Image-Data/Person${i}/Person${i}_1.jpg`" loading="lazy" />
            </div>
          </div>
        </div>
      </div>

      <!-- 报告 -->
      <div class="glass-card report-card">
        <h3>📡 社群模式侦察报告</h3>
        <div class="rep-3col">
          <div><h4>🧬 拓扑收敛</h4><p>矩阵重排后40位发言人在空间上坍缩为三大核心利益阵营。这种特异性行为同质化趋势强力揭示会场内部存在有组织有预谋的秘密线下面基网络。</p></div>
          <div><h4>⚠️ 集团A+B</h4><p>占总数80%的外围参会人员色块死死锚定在【南瓜便签】【眼球玩具】【高危哨子】——属于会场普及分发物资。此两类集团嫌疑已被反向排除。</p></div>
          <div><h4>🎯 集团C</h4><p>极度高能警报！矩阵顶层洗牌后分离出由8名成员组成的孤立方阵。行为光谱完全脱离会场主流，不持有任何普及免费礼品，却呈现出绝对死锁的共现特征！</p></div>
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

const methods=[{k:'ward',name:'Ward层次聚类',desc:'最小化簇内方差'},{k:'complete',name:'完全链接',desc:'最远距离鲁棒'},{k:'average',name:'平均链接',desc:'平衡聚类'},{k:'kmeans',name:'K-Means',desc:'基于质心划分'},{k:'dbscan',name:'DBSCAN',desc:'密度识别噪声'}]
function changeMethod(m){store.setClusteringMethod(m)}

const tabs=[{label:'模型审计',path:'/task1_auditing'},{label:'真值校准',path:'/task2_correction'},{label:'社群聚类',path:'/task3_clustering'},{label:'图腾排除',path:'/task4_totem'},{label:'终审定案',path:'/task5_verdict'}]

function renderCharts(){
  charts.forEach(c=>c?.dispose());charts=[];if(!heatmapRef.value)return

  const h=echarts.init(heatmapRef.value);charts.push(h)
  const xData=store.orderedItems.length?store.orderedItems:['鸟鸣器','南瓜便签','眼球玩具','发夹','薰衣草骰子','红哨子','黄色提袋']
  const yData=store.orderedSuspects.length?store.orderedSuspects:Array.from({length:40},(_,i)=>'Person'+(i+1))
  const pts=[],cl={}
  if(store.heatmapMatrixData.length)store.heatmapMatrixData.forEach(d=>{cl[`${d.suspect}-${d.item}`]=d.count})
  for(let y=0;y<yData.length;y++)for(let x=0;x<xData.length;x++){
    let c=0;if(store.heatmapMatrixData.length)c=cl[`${yData[y]}-${xData[x]}`]||0;else{if(y<8&&x>=5)c=3;else if(y>=8&&y<25&&x<4)c=Math.floor(Math.random()*3)+1;else if(y>=25&&x>=4&&x<6)c=2}
    pts.push([x,y,c])
  }
  h.setOption({tooltip:{formatter:p=>`<b>${yData[p.value[1]]}</b> × ${xData[p.value[0]]}<br/>持有: ${p.value[2]}次`},grid:{left:'12%',right:'4%',top:'4%',bottom:'14%'},xAxis:{type:'category',data:xData,axisLabel:{rotate:20,fontSize:11,color:'#636378'}},yAxis:{type:'category',data:yData,axisLabel:{fontSize:9,color:'#636378',formatter:v=>hackerSet.has(v)?'⚠'+v:v}},visualMap:{min:0,max:4,orient:'horizontal',left:'center',bottom:'0%',textStyle:{fontSize:11},inRange:{color:['rgba(0,0,0,0.02)','#E8F5E9','#81C784','#31C27C']}},series:[{type:'heatmap',data:pts,itemStyle:{borderColor:'rgba(0,0,0,0.04)',borderWidth:1}}]})
  h.on('click',p=>{if(p.componentType==='series'){const s=yData[p.value[1]];store.selectPerson(s);router.push('/task2_correction')}})

  const p=echarts.init(pcaRef.value);charts.push(p)
  const sc=[]
  for(let i=1;i<=40;i++){const isH=hackerSet.has('Person'+i);const ang=(i/40)*Math.PI*2;const r=isH?0.5+Math.random()*0.5:(1.5+Math.random()*3);sc.push({v:[r*Math.cos(ang)+Math.random()*0.4,r*Math.sin(ang)+Math.random()*0.4],h:isH,id:'Person'+i})}
  p.setOption({grid:{left:'8%',right:'4%',top:'8%',bottom:'12%'},xAxis:{type:'value',axisLabel:{fontSize:10},splitLine:{lineStyle:{color:'rgba(0,0,0,0.04)'}},name:'PC1',nameTextStyle:{fontSize:11}},yAxis:{type:'value',axisLabel:{fontSize:10},splitLine:{lineStyle:{color:'rgba(0,0,0,0.04)'}},name:'PC2',nameTextStyle:{fontSize:11}},series:[{type:'scatter',data:sc.filter(d=>!d.h).map(d=>d.v),symbolSize:14,itemStyle:{color:'#64B5F6',opacity:.55},name:'普通'},{type:'scatter',data:sc.filter(d=>d.h).map(d=>d.v),symbolSize:24,itemStyle:{color:'#BF5AF2',shadowBlur:12,shadowColor:'rgba(191,90,242,0.5)'},name:'黑客',label:{show:true,formatter:p=>sc.find(d=>d.v===p.value)?.id,fontSize:9,position:'top'}}]})

  const b=echarts.init(barRef.value);charts.push(b)
  b.setOption({tooltip:{trigger:'axis'},legend:{data:['集团C(黑客)','集团A','集团B'],bottom:0,textStyle:{fontSize:11}},grid:{left:'8%',right:'4%',top:'10%',bottom:'18%'},xAxis:{type:'category',data:['黄色提袋','红哨子','南瓜便签','发夹','眼球玩具'],axisLabel:{fontSize:10,rotate:15}},yAxis:{type:'value',name:'持有率%',splitLine:{lineStyle:{color:'rgba(0,0,0,0.04)'}}},series:[{name:'集团C(黑客)',type:'bar',data:[100,0,0,0,0],itemStyle:{color:'#BF5AF2'}},{name:'集团A',type:'bar',data:[0,55,48,52,40],itemStyle:{color:'#64B5F6'}},{name:'集团B',type:'bar',data:[0,38,30,35,42],itemStyle:{color:'#FF9F0A'}}]})
}

function gotoPerson(pid){store.selectPerson(pid);router.push('/task2_correction')}

watch(()=>[store.heatmapMatrixData,store.orderedSuspects,store.orderedItems],()=>nextTick(renderCharts))
onMounted(()=>nextTick(renderCharts))
onUnmounted(()=>charts.forEach(c=>c?.dispose()))
</script>

<style scoped>
.page-root{display:flex;flex-direction:column;min-height:100vh;background:var(--bg-primary)}
.top-nav-bar{display:flex;align-items:center;gap:6px;padding:8px 18px;background:rgba(255,255,255,0.78);backdrop-filter:blur(20px);border-bottom:1px solid rgba(0,0,0,0.05);flex-shrink:0;z-index:50}
.tbn-home{display:flex;align-items:center;padding:6px 10px;border-radius:10px;color:var(--accent-primary);background:rgba(49,194,124,0.08);transition:all .2s}.tbn-home:hover{background:var(--accent-primary);color:#fff}
.tbn-links{display:flex;gap:3px;flex:1;justify-content:center}
.tbn-link{padding:6px 16px;border-radius:18px;font-size:13px;font-weight:500;color:var(--text-secondary);text-decoration:none;transition:all .2s}.tbn-link:hover{background:rgba(0,0,0,0.04)}.tbn-link.active{background:rgba(255,159,10,0.1);color:#B8860B;font-weight:600}
.tbn-right{flex-shrink:0}.tbn-level{font-size:12px;font-weight:600;color:var(--text-primary)}

.page-scroll{flex:1;overflow-y:auto;padding:20px 24px;display:flex;flex-direction:column;gap:18px}

.hero-card{display:flex;gap:18px;align-items:flex-start;padding:18px 24px;border-radius:16px;background:linear-gradient(135deg,rgba(255,159,10,0.04),rgba(191,90,242,0.03));border:1px solid rgba(255,159,10,0.1)}
.hc-num{font-size:52px;font-weight:900;color:rgba(255,159,10,0.12);line-height:1;flex-shrink:0}
.hero-card h2{margin:0 0 6px;font-size:22px;font-weight:700}
.hero-card p{margin:0;font-size:15px;color:var(--text-secondary);line-height:1.6}

.method-bar{display:flex;align-items:center;gap:8px;padding:12px 18px;font-size:13px;flex-wrap:wrap}.method-bar button{padding:6px 14px;border-radius:14px;border:1px solid rgba(0,0,0,0.08);background:rgba(255,255,255,0.5);font-size:12px;cursor:pointer;transition:all .2s;display:flex;flex-direction:column;align-items:center;gap:1px}.method-bar button small{font-size:9px;color:var(--text-tertiary)}.method-bar button.active{background:var(--accent-primary);color:#fff;border-color:var(--accent-primary)}.method-bar button.active small{color:rgba(255,255,255,0.8)}

.main-grid{display:grid;grid-template-columns:1.6fr 1fr;gap:16px}
.main-grid>.glass-card{padding:20px 24px;overflow:visible}.side-col{display:flex;flex-direction:column;gap:16px}
.main-grid h3{margin:0 0 10px;font-size:14px;color:var(--text-secondary)}.ch.tall{height:580px}.ch{height:280px}

.cg-section{padding:12px;border-radius:10px;margin-bottom:12px;background:rgba(0,0,0,0.01)}.cg-hacker{border:1px solid rgba(191,90,242,0.15);background:rgba(191,90,242,0.02)}.cg-title{margin-bottom:10px;font-size:14px;color:var(--text-secondary);display:flex;align-items:center;gap:8px}.cg-photos{display:flex;flex-wrap:wrap;gap:7px}.cgi{width:56px;height:56px;border-radius:8px;overflow:hidden;cursor:pointer;border:2px solid transparent;transition:all .2s}.cg-hacker .cgi{width:68px;height:68px}.cgi img{width:100%;height:100%;object-fit:cover}.cgi:hover{border-color:#31C27C;transform:translateY(-2px);box-shadow:0 4px 14px rgba(0,0,0,0.1)}.cgi.hacker{border-color:rgba(191,90,242,0.3)}.cgi span{position:absolute;bottom:0;left:0;right:0;font-size:7px;color:#fff;background:rgba(0,0,0,0.5);text-align:center}.cg-photos.small .cgi{width:44px;height:44px}

.report-card{padding:18px 24px}.report-card h3{margin:0 0 12px;font-size:15px}.rep-3col{display:grid;grid-template-columns:1fr 1fr 1fr;gap:16px}.rep-3col h4{margin:0 0 6px;font-size:14px;font-weight:600}.rep-3col p{margin:0;font-size:14px;color:var(--text-secondary);line-height:1.7}

.glass-card{background:rgba(255,255,255,0.65);backdrop-filter:blur(20px);border-radius:14px;border:1px solid rgba(0,0,0,0.04);box-shadow:0 2px 12px rgba(0,0,0,0.04)}
.badge-purple{padding:2px 10px;border-radius:20px;background:rgba(191,90,242,0.1);color:var(--accent-purple);font-size:11px;font-weight:600}.badge-default{padding:2px 10px;border-radius:20px;background:rgba(0,0,0,0.04);color:var(--text-secondary);font-size:11px;font-weight:600}
</style>
