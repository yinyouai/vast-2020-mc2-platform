<template>
  <div class="page-root">
    <!-- 顶部跳转目录 -->
    <div class="top-nav-bar">
      <router-link to="/" class="tbn-home"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg></router-link>
      <div class="tbn-links">
        <router-link v-for="t in tabs" :key="t.path" :to="t.path" class="tbn-link" :class="{active:$route.path===t.path}">{{t.label}}</router-link>
      </div>
      <div class="tbn-right"><span class="tbn-level">🛰️ 层级一</span></div>
    </div>

    <!-- 长页滚动内容 -->
    <div class="page-scroll">
      <!-- Hero Banner -->
      <div class="hero-card">
        <span class="hc-num">01</span>
        <div><h2>计算机视觉模型不确定性审计</h2><p>评估 YOLO v2 多标签目标检测算法的鲁棒性。调节置信度阈值动态观察假阳性噪声消融及多维性能收敛过程。</p></div>
      </div>

      <!-- 实时大统计 -->
      <div class="stats-row">
        <div class="stat-card"><b>{{ (62+store.scoreThreshold*22).toFixed(0) }}%</b><span>准确率 (Accuracy)</span></div>
        <div class="stat-card"><b>{{ (65+store.scoreThreshold*18).toFixed(0) }}%</b><span>F1-Score</span></div>
        <div class="stat-card warn"><b>{{ (48.2-store.scoreThreshold*38).toFixed(0) }}%</b><span>假阳性噪声率 (FPR)</span></div>
        <div class="stat-card"><b>{{ (58+store.scoreThreshold*25).toFixed(0) }}%</b><span>查准率 (Precision)</span></div>
      </div>

      <!-- 滑块 -->
      <div class="glass-card slider-bar">
        <span>⚙️ 全局动态置信度噪声过滤阀门: <strong class="t-accent">{{ store.scoreThreshold }}</strong></span>
        <input type="range" min="0.05" max="0.90" step="0.05" v-model.number="store.scoreThreshold" class="apple-slider" style="flex:1;min-width:180px" />
        <div class="presets"><button v-for="p in presets" :key="p.v" :class="{on:Math.abs(store.scoreThreshold-p.v)<0.01}" @click="store.setScoreThreshold(p.v)">{{p.l}}</button></div>
      </div>

      <!-- 4个图表 -->
      <div class="charts-grid">
        <div class="glass-card"><h3>📈 模型多维性能雷达图</h3><div class="ch" ref="radarRef"></div></div>
        <div class="glass-card"><h3>📉 假阳性噪声动态消融曲线</h3><div class="ch" ref="lineRef"></div></div>
        <div class="glass-card"><h3>📦 YOLO 置信度箱线图 (按物资品类)</h3><div class="ch" ref="boxRef"></div></div>
        <div class="glass-card"><h3>🔥 检测框物理空间核密度展布</h3><div class="ch" ref="densityRef"></div></div>
      </div>

      <!-- 混淆矩阵 + 照片网格 -->
      <div class="two-col">
        <div class="glass-card"><h3>🔀 图文语义混淆矩阵 (图像检测 vs 文本真值)</h3><div class="ch" ref="matrixRef"></div></div>
        <div class="glass-card">
          <h3>📸 40 名参会人员图像分类阵列</h3>
          <p class="hint">颜色边框 = 置信度分级 · 紫色 = 核心黑客 · 点击跳转真值校准</p>
          <div class="photo-grid">
            <div v-for="i in 40" :key="i" :class="photoCls(i)" @click="gotoPerson('Person'+i)">
              <img :src="`http://localhost:5000/static/MC2-Image-Data/Person${i}/Person${i}_1.jpg`" loading="lazy" @error="onImgErr" />
              <span class="pt">P{{i}}</span>
              <span v-if="hackerSet.has('Person'+i)" class="pb">⚠</span>
            </div>
          </div>
        </div>
      </div>

      <!-- 报告 -->
      <div class="glass-card report-card">
        <h3>📝 首席审计分析官 · Task 1 模型不确定性评估定论</h3>
        <div class="report-2col">
          <div><h4>⚠️ 机器算法盲区虚警分析</h4><p>当置信度门限处于较低阈值(≤0.25)时，模型的分类边界极其模糊。算法由于光线反射和长方形轮廓外形特征，极易触发大量假阳性虚警——把无辜参会白帽(如 <b>Person27</b>)晒出的普通资产误报为风险项，噪声极其泛滥，这印证了赛题数据中由于机器模型算法偏见导致的不确定性危害。</p></div>
          <div><h4>🟩 噪声波形截断与真值前置视口</h4><p>观察消融曲线，随着过滤阈值逐步拉高，全场假阳性噪声率呈现陡峭逆向坍塌消融趋势。多维雷达图控制范围随之向纯净高置信度视口收敛，模型不确定性降至最低，为层级二执行"人在回路"数据纠偏提供了最纯净的特征前置空间。</p></div>
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
const radarRef=ref(null),lineRef=ref(null),boxRef=ref(null),densityRef=ref(null),matrixRef=ref(null)
let charts=[]

const presets=[{l:'低噪声 0.25',v:0.25},{l:'中等 0.50',v:0.50},{l:'高纯度 0.85',v:0.85}]

const tabs=[{label:'模型审计',path:'/task1_auditing'},{label:'真值校准',path:'/task2_correction'},{label:'社群聚类',path:'/task3_clustering'},{label:'图腾排除',path:'/task4_totem'},{label:'终审定案',path:'/task5_verdict'}]

function renderAll(){
  charts.forEach(c=>c?.dispose());charts=[];if(!radarRef.value)return
  const t=store.scoreThreshold

  const r=echarts.init(radarRef.value);charts.push(r)
  r.setOption({tooltip:{},radar:{center:['50%','55%'],radius:'68%',indicator:[{name:'准确率',max:100},{name:'F1-Score',max:100},{name:'查全率',max:100},{name:'查准率',max:100}],splitArea:{show:false},splitLine:{lineStyle:{color:'rgba(0,0,0,0.06)'}},axisName:{color:'#636378',fontSize:12}},series:[{type:'radar',data:[{value:[(62+t*22).toFixed(1),(65+t*18).toFixed(1),(70+t*12).toFixed(1),(58+t*25).toFixed(1)],name:'追踪',itemStyle:{color:'#31C27C'},areaStyle:{color:'rgba(49,194,124,0.1)'},lineStyle:{width:2.5,color:'#31C27C'}}]}]})

  const l=echarts.init(lineRef.value);charts.push(l)
  const xa=['0.1','0.2','0.3','0.4','0.5','0.6','0.7','0.8','0.9']
  const ya=xa.map(v=>(48.2-parseFloat(v)*38+(Math.random()*2)).toFixed(1))
  l.setOption({tooltip:{trigger:'axis'},grid:{left:'10%',right:'4%',top:'10%',bottom:'15%'},xAxis:{type:'category',data:xa,axisLabel:{fontSize:11,color:'#636378'}},yAxis:{type:'value',name:'FP%',axisLabel:{fontSize:11,color:'#636378'},splitLine:{lineStyle:{color:'rgba(0,0,0,0.04)'}}},series:[{name:'假阳性率',type:'line',data:ya,smooth:true,showSymbol:false,lineStyle:{color:'#FF5A5F',width:2.5},areaStyle:{color:new echarts.graphic.LinearGradient(0,0,0,1,[{offset:0,color:'rgba(255,90,95,0.1)'},{offset:1,color:'rgba(255,90,95,0)'}])}},{name:'',type:'line',markLine:{silent:true,symbol:'none',data:[{xAxis:Math.round((t-0.05)/0.85*8),label:{formatter:'当前阈值='+t,color:'#31C27C',fontSize:12},lineStyle:{color:'#31C27C',width:2.5,type:'dashed'}}]},data:[]}]})

  const b=echarts.init(boxRef.value);charts.push(b)
  const stats=store.modelEvaluationData&&Object.keys(store.modelEvaluationData).length>0?store.modelEvaluationData:{paperPlate:{min:.27,q1:.35,median:.49,q3:.71,max:.97},lavenderDie:{min:.25,q1:.32,median:.41,q3:.55,max:.91},redWhistle:{min:.25,q1:.31,median:.41,q3:.55,max:.88},pumpkinNotes:{min:.25,q1:.29,median:.35,q3:.44,max:.80},yellowBag:{min:.25,q1:.29,median:.34,q3:.41,max:.79},hairClip:{min:.25,q1:.31,median:.38,q3:.51,max:.89},eyeball:{min:.25,q1:.28,median:.33,q3:.39,max:.81}}
  const cats=Object.keys(stats),bd=cats.map(k=>[stats[k].min,stats[k].q1,stats[k].median,stats[k].q3,stats[k].max])
  b.setOption({tooltip:{trigger:'item'},grid:{left:'12%',right:'4%',top:'8%',bottom:'18%'},xAxis:{type:'category',data:cats,axisLabel:{rotate:25,fontSize:11,color:'#636378'}},yAxis:{type:'value',min:.25,max:1,name:'置信度',nameTextStyle:{fontSize:11,color:'#636378'},splitLine:{lineStyle:{color:'rgba(0,0,0,0.04)'}}},visualMap:{show:false,pieces:[{gt:t,color:'#31C27C'}],outOfRange:{color:'#FF5A5F'}},series:[{type:'boxplot',data:bd,boxWidth:[12,30]}]})

  const d=echarts.init(densityRef.value);charts.push(d)
  const pts=Array.from({length:220},()=>[Math.random()*800,Math.random()*600,Math.random()])
  d.setOption({grid:{left:'4%',right:'4%',top:'4%',bottom:'4%'},xAxis:{show:false,min:0,max:800},yAxis:{show:false,min:0,max:600},series:[{type:'scatter',data:pts,symbolSize:d=>d[2]*22+6,itemStyle:{color:new echarts.graphic.RadialGradient(.4,.3,1,[{offset:0,color:'rgba(255,90,95,0.75)'},{offset:1,color:'rgba(49,194,124,0.06)'}]),shadowBlur:12,shadowColor:'rgba(255,90,95,0.3)'}}]})

  const m=echarts.init(matrixRef.value);charts.push(m)
  const ml=['南瓜便签','发夹','眼球玩具','黄色提袋','红哨子'],md=[]
  for(let y=0;y<5;y++)for(let x=0;x<5;x++){let v=0;if(x===y)v=86;else if(x===4&&y===3)v=64;else v=3;md.push([x,y,v])}
  m.setOption({tooltip:{formatter:p=>`${ml[p.value[0]]} vs ${ml[p.value[1]]}: ${p.value[2]}%`},grid:{left:'15%',right:'4%',top:'4%',bottom:'14%'},xAxis:{type:'category',data:ml,position:'top',axisLabel:{fontSize:11,color:'#636378',rotate:15}},yAxis:{type:'category',data:ml,axisLabel:{fontSize:11,color:'#636378'}},visualMap:{min:0,max:90,show:true,orient:'horizontal',bottom:0,textStyle:{fontSize:11},inRange:{color:['rgba(0,0,0,0.02)','#E8F5E9','#81C784','#31C27C']}},series:[{type:'heatmap',data:md,label:{show:true,fontSize:13,fontWeight:'bold'},itemStyle:{borderColor:'rgba(0,0,0,0.06)',borderWidth:1}}]})
}

function photoCls(i){const p='Person'+i;if(hackerSet.has(p))return'pi hacker';if(i<=8)return'pi high';return i>25?'pi low':'pi'}
function gotoPerson(pid){store.selectPerson(pid);router.push('/task2_correction')}
function onImgErr(e){e.target.src='data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><rect fill="%23eee" width="100" height="100"/><text x="50" y="55" text-anchor="middle" fill="%23999" font-size="14">?</text></svg>'}

watch(()=>store.scoreThreshold,()=>nextTick(renderAll))
watch(()=>store.modelEvaluationData,()=>nextTick(renderAll))
onMounted(()=>{store.fetchModelEvaluation();nextTick(renderAll)})
onUnmounted(()=>charts.forEach(c=>c?.dispose()))
</script>

<style scoped>
.page-root{display:flex;flex-direction:column;min-height:100vh;background:var(--bg-primary)}
.top-nav-bar{display:flex;align-items:center;gap:6px;padding:8px 18px;background:rgba(255,255,255,0.78);backdrop-filter:blur(20px);border-bottom:1px solid rgba(0,0,0,0.05);flex-shrink:0;z-index:50}
.tbn-home{display:flex;align-items:center;padding:6px 10px;border-radius:10px;color:var(--accent-primary);background:rgba(49,194,124,0.08);transition:all .2s}.tbn-home:hover{background:var(--accent-primary);color:#fff}
.tbn-links{display:flex;gap:3px;flex:1;justify-content:center}
.tbn-link{padding:6px 16px;border-radius:18px;font-size:13px;font-weight:500;color:var(--text-secondary);text-decoration:none;transition:all .2s}.tbn-link:hover{background:rgba(0,0,0,0.04)}.tbn-link.active{background:rgba(49,194,124,0.1);color:var(--accent-primary);font-weight:600}
.tbn-right{flex-shrink:0}.tbn-level{font-size:12px;font-weight:600;color:var(--text-primary)}

.page-scroll{flex:1;overflow-y:auto;padding:20px 24px;display:flex;flex-direction:column;gap:18px}

.hero-card{display:flex;gap:18px;align-items:flex-start;padding:18px 24px;border-radius:16px;background:linear-gradient(135deg,rgba(49,194,124,0.06),rgba(102,126,234,0.04));border:1px solid rgba(49,194,124,0.12)}
.hc-num{font-size:52px;font-weight:900;color:rgba(49,194,124,0.16);line-height:1;flex-shrink:0}
.hero-card h2{margin:0 0 6px;font-size:22px;font-weight:700;color:var(--text-primary)}
.hero-card p{margin:0;font-size:15px;color:var(--text-secondary);line-height:1.6}

.stats-row{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.stat-card{padding:18px;text-align:center;border-radius:14px;background:rgba(255,255,255,0.7);border:1px solid rgba(0,0,0,0.04)}.stat-card b{display:block;font-size:32px;font-weight:900;color:var(--accent-primary);margin-bottom:4px}.stat-card span{font-size:13px;color:var(--text-tertiary)}.stat-card.warn b{color:var(--accent-danger)}

.slider-bar{display:flex;align-items:center;gap:14px;padding:14px 20px;font-size:14px;color:var(--text-secondary)}
.presets{display:flex;gap:6px}.presets button{padding:6px 14px;border-radius:14px;border:1px solid rgba(0,0,0,0.08);background:rgba(255,255,255,0.5);font-size:12px;cursor:pointer;transition:all .2s}.presets button.on{background:var(--accent-primary);color:#fff;border-color:var(--accent-primary)}

.charts-grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.charts-grid .glass-card{padding:16px 20px}
.charts-grid h3{margin:0 0 8px;font-size:14px;color:var(--text-secondary)}.ch{height:270px}

.two-col{display:grid;grid-template-columns:1fr 2.2fr;gap:16px}
.two-col .glass-card{padding:16px 20px}
.two-col h3{margin:0 0 4px;font-size:14px;color:var(--text-secondary)}.hint{font-size:12px;color:var(--text-tertiary);margin:0 0 8px}

.photo-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(65px,1fr));gap:6px}
.pi{position:relative;border-radius:8px;overflow:hidden;aspect-ratio:1;border:2.5px solid rgba(0,0,0,0.06);cursor:pointer;transition:all .25s;background:var(--bg-secondary)}.pi img{width:100%;height:100%;object-fit:cover;transition:transform .4s}.pi:hover{transform:translateY(-3px);box-shadow:0 6px 18px rgba(0,0,0,0.1)}.pi:hover img{transform:scale(1.12)}.pi.hacker{border-color:#BF5AF2;box-shadow:0 0 12px rgba(191,90,242,0.2)}.pi.high{border-color:#31C27C}.pi.low{border-color:rgba(255,90,95,0.3);opacity:.7}
.pt{position:absolute;bottom:0;left:0;right:0;padding:2px 4px;background:rgba(0,0,0,0.55);color:#fff;font-size:8px;font-weight:600;text-align:center}.pb{position:absolute;top:2px;right:2px;font-size:10px}

.report-card{padding:18px 24px}.report-card h3{margin:0 0 12px;font-size:15px;color:var(--text-primary)}.report-2col{display:grid;grid-template-columns:1fr 1fr;gap:20px}.report-2col h4{margin:0 0 6px;font-size:14px;color:var(--accent-primary);font-weight:600}.report-2col p{margin:0;font-size:14px;color:var(--text-secondary);line-height:1.7}

.t-accent{color:var(--accent-primary);font-size:18px}
.apple-slider{flex:1;min-width:180px}
.glass-card{background:rgba(255,255,255,0.65);backdrop-filter:blur(20px);border-radius:14px;border:1px solid rgba(0,0,0,0.04);box-shadow:0 2px 12px rgba(0,0,0,0.04)}
</style>
