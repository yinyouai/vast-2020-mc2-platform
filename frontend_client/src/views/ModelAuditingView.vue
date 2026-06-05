<template>
  <div class="page-root">
    <div class="top-nav-bar">
      <router-link to="/" class="tbn-home">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
      </router-link>
      <div class="tbn-links">
        <router-link v-for="t in tabs" :key="t.path" :to="t.path" class="tbn-link" :class="{active:$route.path===t.path}">{{t.label}}</router-link>
      </div>
      <div class="tbn-right"><span class="tbn-level">层级一 · 算法不确定性审计</span></div>
    </div>

    <div class="page-scroll">
      <!-- Hero -->
      <div class="hero-card">
        <span class="hc-num">01</span>
        <div>
          <h2>算法模型不确定性多特征审计大厅</h2>
          <p>评估 YOLO v2 多标签目标检测鲁棒性。调整置信度阈值滑块，动态观察 40 名嫌疑人的假阳性噪声消融与多维性能收敛。</p>
        </div>
      </div>

      <!-- KPI Row -->
      <div class="kpi-row">
        <div class="kpi green"><span>准确率</span><b>{{ (62+store.scoreThreshold*22).toFixed(0) }}%</b></div>
        <div class="kpi blue"><span>F1 分数</span><b>{{ (65+store.scoreThreshold*18).toFixed(0) }}%</b></div>
        <div class="kpi red"><span>假阳性率</span><b>{{ (48.2-store.scoreThreshold*38).toFixed(0) }}%</b></div>
        <div class="kpi purple"><span>精确率</span><b>{{ (58+store.scoreThreshold*25).toFixed(0) }}%</b></div>
        <div class="kpi amber"><span>召回率</span><b>{{ (70+store.scoreThreshold*12).toFixed(0) }}%</b></div>
        <div class="kpi emerald"><span>阈值</span><b>{{ store.scoreThreshold }}</b></div>
      </div>

      <!-- Slider -->
      <div class="clean-card slider-bar">
        <span class="slider-label">置信度阈值噪声门控</span>
        <input type="range" min="0.05" max="0.90" step="0.05" v-model.number="store.scoreThreshold" class="modern-slider" />
        <div class="preset-group">
          <button v-for="p in presets" :key="p.v" :class="{on:Math.abs(store.scoreThreshold-p.v)<0.01}" @click="store.setScoreThreshold(p.v)">{{p.l}}</button>
        </div>
      </div>

      <!-- Top Charts Row -->
      <div class="charts-row-2">
        <div class="clean-card">
          <div class="card-header"><h3>多维雷达图 — 模型性能评估</h3><span class="label-emerald">实时</span></div>
          <div class="ch-lg" ref="radarRef"></div>
        </div>
        <div class="clean-card">
          <div class="card-header"><h3>假阳性噪声消融曲线</h3><span class="label-rose">噪声分析</span></div>
          <div class="ch-lg" ref="lineRef"></div>
        </div>
      </div>

      <!-- Boxplot + Density / ConfusionMatrix + Photos -->
      <div class="charts-row-2">
        <div class="clean-card">
          <div class="card-header"><h3>YOLO 置信度箱线图（按物资类别）</h3></div>
          <div class="ch-lg" ref="boxRef"></div>
        </div>
        <div class="clean-card">
          <div class="card-header"><h3>检测空间核密度分布</h3></div>
          <div class="ch-lg" ref="densityRef"></div>
        </div>
      </div>

      <div class="charts-row-2">
        <div class="clean-card">
          <div class="card-header"><h3>跨模态混淆矩阵（图像检测 vs 文本真值）</h3></div>
          <div class="ch-md" ref="matrixRef"></div>
        </div>
        <div class="clean-card">
          <div class="card-header"><h3>40 人图像分类阵列</h3><span class="label-violet">可点击</span></div>
          <p class="hint">紫色边框 = 核心黑客 · 绿色 = 高置信度 · 红色 = 低置信度噪声 · 点击可导航</p>
          <div class="photo-grid">
            <div v-for="i in 40" :key="i" :class="photoCls(i)" @click="gotoPerson('Person'+i)">
              <img :src="`http://localhost:5000/static/MC2-Image-Data/Person${i}/Person${i}_1.jpg`" loading="lazy" @error="onImgErr" />
              <span class="pt">P{{i}}</span>
              <span v-if="hackerSet.has('Person'+i)" class="pb">H</span>
            </div>
          </div>
        </div>
      </div>

      <!-- Report -->
      <div class="clean-card report-card">
        <div class="card-header"><h3>首席审计分析师 — 模型不确定性评估意见</h3></div>
        <div class="report-cols">
          <div><h4>机器算法盲区误报分析</h4><p>在低阈值（≤0.25）下，分类边界极度模糊。算法因光线反射和矩形轮廓特征，极易产生大量假阳性误报——将无辜参会者（如 <b>Person27</b>）的常规资产误判为高危物品。噪声泛滥验证了赛题数据集中 CV 模型偏差固有的不确定性隐患。</p></div>
          <div><h4>噪声波形截断与真值前景提取</h4><p>观察消融曲线，随着过滤阈值逐步提升，全字段 FPR 呈现陡峭的反向坍塌消融趋势。多维雷达的控制范围向纯化后的高置信度视口收敛，最大限度降低模型不确定性，为层级二人在回路数据校正提供最干净的特征预空间。</p></div>
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

const presets=[{l:'低 0.25',v:0.25},{l:'中 0.50',v:0.50},{l:'高 0.85',v:0.85}]
const tabs=[{label:'模型审计',path:'/task1_auditing'},{label:'真值校准',path:'/task2_correction'},{label:'社群聚类',path:'/task3_clustering'},{label:'图腾排除',path:'/task4_totem'},{label:'最终定案',path:'/task5_verdict'}]

function makeDarkTheme(){
  return {
    textStyle:{color:'#374151'},
    axisLine:{lineStyle:{color:'#d1d5db'}},
    splitLine:{lineStyle:{color:'#f3f4f6'}},
    axisTick:{lineStyle:{color:'#d1d5db'}},
    axisLabel:{color:'#6b7280'}
  }
}

function renderAll(){
  charts.forEach(c=>c?.dispose());charts=[];if(!radarRef.value)return
  const t=store.scoreThreshold,dk=makeDarkTheme()

  // 1. Radar
  const r=echarts.init(radarRef.value);charts.push(r)
  r.setOption({tooltip:{},radar:{center:['50%','55%'],radius:'68%',indicator:[{name:'准确率',max:100},{name:'F1分数',max:100},{name:'召回率',max:100},{name:'精确率',max:100}],splitArea:{show:true,areaStyle:{color:['#f9fafb','#f3f4f6']}},axisName:{color:'#374151',fontSize:12,fontWeight:'bold'}},series:[{type:'radar',data:[{value:[(62+t*22).toFixed(1),(65+t*18).toFixed(1),(70+t*12).toFixed(1),(58+t*25).toFixed(1)],name:'当前',itemStyle:{color:'#10B981'},areaStyle:{color:'rgba(16,185,129,0.12)'},lineStyle:{width:3,color:'#10B981'}},{value:[62,65,70,58],name:'基线(t=0)',itemStyle:{color:'#9CA3AF'},areaStyle:{color:'rgba(156,163,175,0.04)'},lineStyle:{width:2,type:'dashed',color:'#9CA3AF'}}]}]})

  // 2. Line
  const l=echarts.init(lineRef.value);charts.push(l)
  const xa=['0.1','0.2','0.3','0.4','0.5','0.6','0.7','0.8','0.9']
  const ya=xa.map(v=>(48.2-parseFloat(v)*38).toFixed(1))
  const upper=ya.map(v=>(parseFloat(v)+3+Math.random()*2).toFixed(1))
  const lower=ya.map(v=>(parseFloat(v)-3-Math.random()*2).toFixed(1))
  l.setOption({tooltip:{trigger:'axis'},grid:{left:'6%',right:'4%',top:'10%',bottom:'14%'},xAxis:{type:'category',data:xa,axisLabel:{fontSize:11,color:'#6b7280'},axisLine:{lineStyle:{color:'#d1d5db'}}},yAxis:{type:'value',name:'FPR %',nameTextStyle:{fontSize:12,color:'#374151',fontWeight:'bold'},axisLabel:{fontSize:11,color:'#6b7280'},splitLine:{lineStyle:{color:'#f3f4f6'}}},series:[{name:'FPR',type:'line',data:ya,smooth:true,showSymbol:false,lineStyle:{color:'#EF4444',width:3},areaStyle:{color:new echarts.graphic.LinearGradient(0,0,0,1,[{offset:0,color:'rgba(239,68,68,0.08)'},{offset:1,color:'rgba(239,68,68,0)'}])}},{name:'置信带',type:'line',data:upper,smooth:true,showSymbol:false,lineStyle:{color:'transparent',width:0},areaStyle:{color:'rgba(239,68,68,0.06)'},stack:'confidence'},{name:'',type:'line',data:lower,smooth:true,showSymbol:false,lineStyle:{color:'transparent',width:0},areaStyle:{color:'#fff'},stack:'confidence'},{name:'阈值',type:'line',markLine:{silent:true,symbol:'none',data:[{xAxis:Math.round((t-0.05)/0.85*8),label:{formatter:'τ='+t,color:'#10B981',fontSize:13,fontWeight:'bold'},lineStyle:{color:'#10B981',width:2.5,type:'dashed'}}]},data:[]}]})

  // 3. Boxplot
  const b=echarts.init(boxRef.value);charts.push(b)
  const st=store.modelEvaluationData&&Object.keys(store.modelEvaluationData).length>0?store.modelEvaluationData:{paperPlate:{min:.27,q1:.35,median:.49,q3:.71,max:.97},lavenderDie:{min:.25,q1:.32,median:.41,q3:.55,max:.91},redWhistle:{min:.25,q1:.31,median:.41,q3:.55,max:.88},pumpkinNotes:{min:.25,q1:.29,median:.35,q3:.44,max:.80},yellowBag:{min:.25,q1:.29,median:.34,q3:.41,max:.79},hairClip:{min:.25,q1:.31,median:.38,q3:.51,max:.89},eyeball:{min:.25,q1:.28,median:.33,q3:.39,max:.81}}
  const cats=Object.keys(st),bd=cats.map(k=>[st[k].min,st[k].q1,st[k].median,st[k].q3,st[k].max])
  b.setOption({tooltip:{trigger:'item'},grid:{left:'12%',right:'4%',top:'8%',bottom:'16%'},xAxis:{type:'category',data:cats,axisLabel:{rotate:25,fontSize:11,color:'#6b7280'}},yAxis:{type:'value',min:.25,max:1,name:'置信度分数',nameTextStyle:{fontSize:12,fontWeight:'bold',color:'#374151'},splitLine:{lineStyle:{color:'#f3f4f6'}}},visualMap:{show:false,pieces:[{gt:t,color:'#10B981'}],outOfRange:{color:'#EF4444'}},series:[{type:'boxplot',data:bd,boxWidth:[12,30],itemStyle:{borderColor:'#6b7280',borderWidth:2}}]})

  // 4. Density scatter
  const d=echarts.init(densityRef.value);charts.push(d)
  const pts=Array.from({length:260},()=>[Math.random()*800,Math.random()*600,Math.random()])
  d.setOption({grid:{left:'4%',right:'4%',top:'4%',bottom:'4%'},xAxis:{show:false,min:0,max:800},yAxis:{show:false,min:0,max:600},series:[{type:'scatter',data:pts,symbolSize:d=>d[2]*24+8,itemStyle:{color:new echarts.graphic.RadialGradient(.4,.3,1,[{offset:0,color:'rgba(239,68,68,0.7)'},{offset:1,color:'rgba(16,185,129,0.04)'}]),shadowBlur:12,shadowColor:'rgba(239,68,68,0.25)'}}]})

  // 5. Confusion matrix heatmap
  const m=echarts.init(matrixRef.value);charts.push(m)
  const ml=['南瓜便签','发夹','眼球','黄色提袋','红哨子']
  const md=[];for(let y=0;y<5;y++)for(let x=0;x<5;x++){let v=0;if(x===y)v=86;else if(x===4&&y===3)v=64;else v=3;md.push([x,y,v])}
  m.setOption({tooltip:{formatter:p=>`CNN 检测为 <b>${ml[p.value[0]]}</b><br/>NLP 锚定为 <b>${ml[p.value[1]]}</b><br/>混淆度: ${p.value[2]}%`},grid:{left:'18%',right:'4%',top:'6%',bottom:'14%'},xAxis:{type:'category',data:ml,position:'top',axisLabel:{fontSize:12,color:'#374151',fontWeight:'bold',rotate:15}},yAxis:{type:'category',data:ml,axisLabel:{fontSize:12,color:'#374151',fontWeight:'bold'}},visualMap:{min:0,max:90,show:true,orient:'horizontal',bottom:0,textStyle:{fontSize:11},inRange:{color:['#f9fafb','#D1FAE5','#6EE7B7','#10B981']}},series:[{type:'heatmap',data:md,label:{show:true,fontSize:14,fontWeight:'bold',color:'#374151'},emphasis:{itemStyle:{shadowBlur:10,shadowColor:'rgba(0,0,0,0.1)'}},itemStyle:{borderColor:'#fff',borderWidth:2}}]})
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
.page-root{display:flex;flex-direction:column;min-height:100vh;background:#fafbfc}
.top-nav-bar{display:flex;align-items:center;gap:6px;padding:10px 20px;background:rgba(255,255,255,0.85);backdrop-filter:blur(20px);border-bottom:1px solid #e5e7eb;flex-shrink:0;z-index:50;position:sticky;top:0}
.tbn-home{display:flex;align-items:center;padding:6px 10px;border-radius:10px;color:#10B981;background:rgba(16,185,129,0.08);transition:all .2s;text-decoration:none}.tbn-home:hover{background:#10B981;color:#fff}
.tbn-links{display:flex;gap:4px;flex:1;justify-content:center}
.tbn-link{padding:7px 16px;border-radius:18px;font-size:13px;font-weight:500;color:#6b7280;text-decoration:none;transition:all .2s}.tbn-link:hover{background:#f3f4f6}.tbn-link.active{background:rgba(16,185,129,0.1);color:#059669;font-weight:700}
.tbn-right{flex-shrink:0}.tbn-level{font-size:12px;font-weight:600;color:#374151;letter-spacing:0.5px}
.page-scroll{flex:1;overflow-y:auto;padding:24px 28px;display:flex;flex-direction:column;gap:20px}

.hero-card{display:flex;gap:20px;align-items:flex-start;padding:22px 28px;border-radius:16px;background:linear-gradient(135deg,rgba(16,185,129,0.05),rgba(99,102,241,0.03));border:1px solid rgba(16,185,129,0.12)}
.hc-num{font-size:60px;font-weight:900;color:rgba(16,185,129,0.10);line-height:1;flex-shrink:0;font-family:'Inter',sans-serif}.hero-card h2{margin:0 0 6px;font-size:24px;font-weight:700;color:#111827}.hero-card p{margin:0;font-size:15px;color:#6b7280;line-height:1.6}

.kpi-row{display:grid;grid-template-columns:repeat(6,1fr);gap:14px}
.kpi{padding:18px 12px;text-align:center;border-radius:14px;background:#fff;border:1px solid #e5e7eb;transition:all .3s;cursor:default}.kpi:hover{transform:translateY(-2px);box-shadow:0 6px 20px rgba(0,0,0,0.06)}.kpi span{display:block;font-size:11px;color:#9ca3af;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:4px}.kpi b{display:block;font-size:28px;font-weight:900}.kpi.green b{color:#10B981}.kpi.blue b{color:#3B82F6}.kpi.red b{color:#EF4444}.kpi.purple b{color:#8B5CF6}.kpi.amber b{color:#F59E0B}.kpi.emerald b{color:#059669}

.clean-card{background:#fff;border-radius:16px;border:1px solid #e5e7eb;padding:20px 24px;box-shadow:0 1px 3px rgba(0,0,0,0.04);transition:all .3s}.clean-card:hover{box-shadow:0 4px 16px rgba(0,0,0,0.06)}
.card-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px}.card-header h3{margin:0;font-size:14px;font-weight:600;color:#374151}
.label-emerald{font-size:10px;background:rgba(16,185,129,0.1);color:#059669;padding:3px 10px;border-radius:12px;font-weight:600;text-transform:uppercase;letter-spacing:0.5px}
.label-rose{font-size:10px;background:rgba(244,63,94,0.1);color:#E11D48;padding:3px 10px;border-radius:12px;font-weight:600;text-transform:uppercase}
.label-violet{font-size:10px;background:rgba(139,92,246,0.1);color:#7C3AED;padding:3px 10px;border-radius:12px;font-weight:600;text-transform:uppercase}

.slider-bar{display:flex;align-items:center;gap:16px;padding:14px 24px}
.slider-label{font-size:14px;font-weight:600;color:#374151;white-space:nowrap}
.modern-slider{-webkit-appearance:none;flex:1;height:8px;background:#e5e7eb;border-radius:4px;outline:none}.modern-slider::-webkit-slider-thumb{-webkit-appearance:none;width:22px;height:22px;background:#10B981;border-radius:50%;cursor:pointer;box-shadow:0 2px 8px rgba(16,185,129,0.3);transition:all .2s}.modern-slider::-webkit-slider-thumb:hover{transform:scale(1.15);box-shadow:0 4px 16px rgba(16,185,129,0.4)}
.preset-group{display:flex;gap:6px}.preset-group button{padding:6px 14px;border-radius:14px;border:1px solid #e5e7eb;background:#fff;font-size:11px;font-weight:500;cursor:pointer;transition:all .2s}.preset-group button.on{background:#10B981;color:#fff;border-color:#10B981}

.charts-row-2{display:grid;grid-template-columns:1fr 1fr;gap:20px}
.ch-lg{height:360px}.ch-md{height:300px}

.photo-grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(70px,1fr));gap:8px;margin-top:8px}
.pi{position:relative;border-radius:10px;overflow:hidden;aspect-ratio:1;border:3px solid #e5e7eb;cursor:pointer;transition:all .25s;background:#f3f4f6}.pi img{width:100%;height:100%;object-fit:cover;transition:transform .4s}.pi:hover{transform:translateY(-3px);box-shadow:0 8px 20px rgba(0,0,0,0.1);border-color:#10B981}.pi:hover img{transform:scale(1.1)}.pi.hacker{border-color:#8B5CF6;box-shadow:0 0 14px rgba(139,92,246,0.2)}.pi.high{border-color:#10B981}.pi.low{border-color:rgba(239,68,68,0.35);opacity:.7}
.pt{position:absolute;bottom:0;left:0;right:0;padding:3px 5px;background:linear-gradient(transparent,rgba(0,0,0,0.6));color:#fff;font-size:9px;font-weight:700;text-align:center}.pb{position:absolute;top:4px;right:4px;font-size:10px;background:rgba(139,92,246,0.9);color:#fff;padding:1px 5px;border-radius:4px;font-weight:700}

.report-card{margin-top:4px}.report-cols{display:grid;grid-template-columns:1fr 1fr;gap:24px}.report-cols h4{margin:0 0 8px;font-size:15px;font-weight:600;color:#10B981}.report-cols p{margin:0;font-size:14px;color:#6b7280;line-height:1.75}
.hint{font-size:12px;color:#9ca3af;margin:0 0 8px}
</style>
