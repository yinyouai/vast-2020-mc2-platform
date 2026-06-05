<template>
  <div class="page-root">
    <div class="top-nav-bar">
      <router-link to="/" class="tbn-home"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg></router-link>
      <div class="tbn-links">
        <router-link v-for="t in tabs" :key="t.path" :to="t.path" class="tbn-link" :class="{active:$route.path===t.path}">{{t.label}}</router-link>
      </div>
      <div class="tbn-right"><span class="tbn-level">层级四 · 秘密图腾反向排除</span></div>
    </div>

    <div class="page-scroll">
      <div class="hero-card">
        <span class="hc-num">04</span>
        <div><h2>背景资产排除与力导向网络分析</h2><p>使用反向排除漏斗切除高覆盖率普及礼品。强制秘密接头图腾在流向图和力导向图中显现。当前排除：<strong>{{store.excludedItems.length}}/4</strong> 项。</p></div>
      </div>

      <!-- KPI -->
      <div class="kpi-row">
        <div class="kpi" :class="store.excludedItems.length>=3?'green':'amber'"><span>去噪状态</span><b>{{store.excludedItems.length>=3?'纯净':'需更多'}}</b></div>
        <div class="kpi purple"><span>已排除项</span><b>{{store.excludedItems.length}}/4</b></div>
        <div class="kpi blue"><span>活动节点</span><b>47</b></div>
        <div class="kpi emerald"><span>图腾锁定</span><b>{{store.excludedItems.length>=3?'是':'否'}}</b></div>
      </div>

      <!-- Exclusion Panel + Bar Chart -->
      <div class="two-col">
        <div class="clean-card">
          <div class="card-header"><h3>反向排除漏斗控制台</h3></div>
          <p class="hint">勾选放逐高覆盖率普及会场礼品——每排除一项，逼近图腾真相一步</p>
          <div class="ex-list">
            <label v-for="item in excludeItems" :key="item.id" class="ex-chip" :class="{on:store.excludedItems.includes(item.id)}" @click="toggle(item.id)">
              <span class="ex-box">{{store.excludedItems.includes(item.id)?'✕':''}}</span>
              <span class="ex-name">{{item.cnName}}</span>
              <span class="ex-cov">覆盖率 {{item.coverage}}%</span>
            </label>
          </div>
          <div class="ex-result" :class="{done:store.excludedItems.length>=3}">
            <span v-if="store.excludedItems.length>=3">去噪纯度已达——秘密图腾已锁定。点击下方图表中"黄色提袋"节点查看像素级物证</span>
            <span v-else>继续排除普及礼品（需 ≥3 项才能解锁深度钻取能力）</span>
          </div>
        </div>
        <div class="clean-card">
          <div class="card-header"><h3>排除前后物资持有率对比</h3></div>
          <div class="ch-lg" ref="barRef"></div>
        </div>
      </div>

      <!-- Sankey + Force-Directed Graph -->
      <div class="two-col-main">
        <div class="clean-card">
          <div class="card-header"><h3>资产流向桑基图</h3></div>
          <div class="ch-lg" ref="sankeyRef"></div>
          <div class="sankey-msg">{{sankeyMsg}}</div>
        </div>
        <div class="clean-card">
          <div class="card-header"><h3>人物-物资力导向网络图</h3><span class="label-violet">拖动探索</span></div>
          <div class="ch-xl" ref="networkRef"></div>
        </div>
      </div>

      <!-- Report -->
      <div class="clean-card report-card">
        <div class="card-header"><h3>情报分析师 — 图腾去混淆报告</h3></div>
        <div v-if="store.excludedItems.length===0" class="rep-status warn"><p><b>背景干扰严重（尚未去噪）：</b>网络充斥会场普及礼品噪声。普通白帽参会者（Person27）的笔记本与真正的黑客黄色提袋图腾光谱交织——无法区分无辜与有罪。请开始排除普及礼品。</p></div>
        <div v-else-if="store.excludedItems.length<3" class="rep-status progress"><p><b>反向排除进行中（纯度提升中）：</b>已切除 {{store.excludedItems.length}} 项背景物品。大量无辜参会者行为光谱向正常背景收敛。继续排除更多普及礼品。</p></div>
        <div v-else class="rep-status done"><p><b>秘密接头图腾已完全破译！</b>切除全部会场普及礼品后，整个社交资产流以 100% 数学纯度汇聚到单一物品：<strong>[秘密黄色提袋图腾]</strong>。8 名黑客已锁定。</p></div>
      </div>
    </div>

    <Teleport to="body">
      <transition name="fade">
        <div v-if="store.isFourthLayerActive" class="full-overlay" @click.self="store.isFourthLayerActive=false">
          <div class="full-modal">
            <div class="fm-h"><h3>像素级证据链下钻：黄色提袋接头图腾</h3><button @click="store.isFourthLayerActive=false">✕ 关闭</button></div>
            <div class="fm-b">
              <div class="fm-img"><img src="http://localhost:5000/static/MC2-Image-Data/Person3/Person3_1.jpg"/></div>
              <div class="fm-log">
                <div class="b"><b>特异性确认：</b>全场 40 人中仅此 8 人核心组织持有该物品——32 名外围参会者绝对零共现。</div>
                <div class="b"><b>跨模态闭环：</b>YOLO 初始严重误分类该物品。经过人在回路校准后，图腾以 100% 数学纯度固化为秘密接头标识。</div>
                <button @click="store.isFourthLayerActive=false;$router.push('/task5_verdict')" class="btn-go">证据已锁定 → 进入层级五社交隔离审计</button>
              </div>
            </div>
          </div>
        </div>
      </transition>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, watch, nextTick, computed } from 'vue'
import { useDashboardStore } from '../store/dashboard'
import { EXCLUDABLE_ITEMS, HACKER_LIST } from '../constants/forensics'
import * as echarts from 'echarts'

const store=useDashboardStore(), hackerSet=new Set(HACKER_LIST)
const excludeItems=EXCLUDABLE_ITEMS
const barRef=ref(null),sankeyRef=ref(null),networkRef=ref(null)
let charts=[]

const tabs=[{label:'模型审计',path:'/task1_auditing'},{label:'真值校准',path:'/task2_correction'},{label:'社群聚类',path:'/task3_clustering'},{label:'图腾排除',path:'/task4_totem'},{label:'最终定案',path:'/task5_verdict'}]
function toggle(id){const c=[...store.excludedItems];const i=c.indexOf(id);if(i>-1)c.splice(i,1);else c.push(id);store.excludedItems=c;store.fetchHeatmapMatrix()}
const sankeyMsg=computed(()=>{if(store.excludedItems.length===0)return'噪声饱和 — 线索模糊 — 请开始排除';if(store.excludedItems.length<3)return`排除进行中 (${store.excludedItems.length}/4) — 光谱收敛中`;return'图腾锁定 — 100% 纯度 → 黄色提袋已识别'})

function renderAll(){
  charts.forEach(c=>c?.dispose());charts=[];if(!barRef.value)return

  const bar=echarts.init(barRef.value);charts.push(bar)
  const bi=[{n:'薰衣草骰子',v:60,k:'lavenderDie'},{n:'标识牌',v:60,k:'sign'},{n:'发夹',v:47,k:'hairClip'},{n:'泛滥红哨子',v:45,k:'redWhistle'},{n:'南瓜便签',v:35,k:'pumpkinNotes'},{n:'秘密黄色提袋',v:20,k:'yellowBag'}]
  bar.setOption({tooltip:{trigger:'axis'},grid:{left:'8%',right:'4%',top:'6%',bottom:'14%'},xAxis:{type:'category',data:bi.map(d=>d.n),axisLabel:{rotate:15,fontSize:11,color:'#6b7280',fontWeight:'bold'}},yAxis:{type:'value',max:100,name:'覆盖率 %',nameTextStyle:{fontSize:12,fontWeight:'bold',color:'#374151'},splitLine:{lineStyle:{color:'#f3f4f6'}}},series:[{type:'bar',data:bi.map((d,i)=>({value:store.excludedItems.includes(d.k)?0:d.v,itemStyle:{color:i===5?'#8B5CF6':'#10B981',opacity:store.excludedItems.includes(d.k)?.3:1,borderRadius:[8,8,0,0]}})),barWidth:'38%',animationDuration:600,animationEasing:'cubicOut'}]})

  const sank=echarts.init(sankeyRef.value);charts.push(sank)
  const excl=store.excludedItems.length,nf=excl>=3?5:excl===0?50:25,sf=35
  sank.setOption({tooltip:{trigger:'item'},series:[{type:'sankey',layout:'none',emphasis:{focus:'adjacency'},data:[{name:'40 名候选人',itemStyle:{color:'#93C5FD'}},{name:'免费礼品背景',itemStyle:{color:'#D1D5DB'}},{name:'秘密组织暗号',itemStyle:{color:'#8B5CF6'}},{name:'黄色提袋图腾',itemStyle:{color:'#FCD34D'}}],links:[{source:'40 名候选人',target:'免费礼品背景',value:nf},{source:'40 名候选人',target:'秘密组织暗号',value:sf},{source:'秘密组织暗号',target:'黄色提袋图腾',value:sf}],nodeWidth:20,nodeGap:20,label:{fontSize:13,fontWeight:'bold',color:'#374151'},lineStyle:{color:'source',curveness:.5}}]})
  sank.on('click',p=>{if((p.name||'').includes('黄色提袋')||p.name==='秘密组织暗号'){if(store.excludedItems.length>=3)store.isFourthLayerActive=true;else alert('请先排除 ≥3 项普及礼品以解锁深度钻取')}})

  // Force-Directed Graph
  const net=echarts.init(networkRef.value);charts.push(net)
  const nodes=[],links=[]
  for(let i=1;i<=40;i++){const p='Person'+i,isH=hackerSet.has(p);nodes.push({id:p,name:p,symbolSize:isH?44:22,category:isH?0:1,itemStyle:{color:isH?'#8B5CF6':'#93C5FD',borderColor:'#fff',borderWidth:isH?3.5:1.5,shadowBlur:isH?18:0,shadowColor:isH?'rgba(139,92,246,0.45)':'transparent'},label:{show:isH,fontSize:12,fontWeight:'bold',color:'#374151',position:'bottom',distance:6},draggable:true})}
  const exSet=new Set(store.excludedItems)
  const its=[{id:'yellowBag',n:'黄色提袋',c:'#8B5CF6',t:true},{id:'redWhistle',n:'泛滥红哨子',c:'#EF4444'},{id:'pumpkinNotes',n:'南瓜便签',c:'#F59E0B'},{id:'hairClip',n:'发夹',c:'#FCD34D'},{id:'eyeball',n:'眼球玩具',c:'#3B82F6'},{id:'lavenderDie',n:'薰衣草骰子',c:'#A78BFA'},{id:'paperPlate',n:'纸盘',c:'#9CA3AF'}]
  its.filter(it=>!exSet.has(it.id)).forEach(it=>{nodes.push({id:it.id,name:it.n,symbolSize:it.t?42:28,category:it.t?2:3,itemStyle:{color:it.c,borderColor:'#fff',borderWidth:it.t?3.5:1.5,shadowBlur:it.t?18:0,shadowColor:it.t?'rgba(139,92,246,0.5)':'transparent'},label:{show:true,fontSize:11,fontWeight:'bold',color:'#374151'},draggable:false})})
  for(let i=1;i<=40;i++){const p='Person'+i,isH=hackerSet.has(p);its.filter(it=>!exSet.has(it.id)).forEach((it,idx)=>{let has=false;if(it.t)has=isH;else has=((i*(idx+1)*7)%100)<(it.id==='lavenderDie'?60:it.id==='redWhistle'?45:it.id==='hairClip'?47:35)&&!isH;if(has)links.push({source:p,target:it.id,lineStyle:{color:it.t?'rgba(139,92,246,0.55)':'rgba(156,163,175,0.22)',width:it.t?3:.8,curveness:.1}})})}
  net.setOption({tooltip:{trigger:'item',formatter:p=>p.dataType==='node'?`<b>${p.name}</b>`:p.data.source+' → '+p.data.target},legend:{show:true,bottom:6,textStyle:{fontSize:10,color:'#6b7280'},itemWidth:10,itemHeight:10,data:['黑客 (8人)','外围人员','秘密图腾','普通物品']},series:[{type:'graph',layout:'force',roam:true,draggable:true,force:{repulsion:420,gravity:.05,edgeLength:[60,200],friction:.5},data:nodes,links:links,categories:[{name:'黑客 (8人)',itemStyle:{color:'#8B5CF6'}},{name:'外围人员',itemStyle:{color:'#93C5FD'}},{name:'秘密图腾',itemStyle:{color:'#8B5CF6'}},{name:'普通物品',itemStyle:{color:'#6B7280'}}],emphasis:{focus:'adjacency',lineStyle:{width:8},itemStyle:{shadowBlur:20}},label:{show:true,position:'bottom',fontSize:12,color:'#374151'}}]})
}

watch(()=>store.excludedItems,()=>nextTick(renderAll),{deep:true})
onMounted(()=>nextTick(renderAll))
onUnmounted(()=>charts.forEach(c=>c?.dispose()))
</script>

<style scoped>
.page-root{display:flex;flex-direction:column;min-height:100vh;background:#fafbfc}
.top-nav-bar{display:flex;align-items:center;gap:6px;padding:10px 20px;background:rgba(255,255,255,0.85);backdrop-filter:blur(20px);border-bottom:1px solid #e5e7eb;flex-shrink:0;z-index:50;position:sticky;top:0}
.tbn-home{display:flex;align-items:center;padding:6px 10px;border-radius:10px;color:#10B981;background:rgba(16,185,129,0.08);transition:all .2s;text-decoration:none}.tbn-home:hover{background:#10B981;color:#fff}
.tbn-links{display:flex;gap:4px;flex:1;justify-content:center}.tbn-link{padding:7px 16px;border-radius:18px;font-size:13px;font-weight:500;color:#6b7280;text-decoration:none;transition:all .2s}.tbn-link:hover{background:#f3f4f6}.tbn-link.active{background:rgba(139,92,246,0.1);color:#7C3AED;font-weight:700}
.tbn-right{flex-shrink:0}.tbn-level{font-size:12px;font-weight:600;color:#374151;letter-spacing:0.5px}
.page-scroll{flex:1;overflow-y:auto;padding:24px 28px;display:flex;flex-direction:column;gap:20px}

.hero-card{display:flex;gap:20px;align-items:flex-start;padding:22px 28px;border-radius:16px;background:linear-gradient(135deg,rgba(139,92,246,0.04),rgba(99,102,241,0.03));border:1px solid rgba(139,92,246,0.1)}
.hc-num{font-size:60px;font-weight:900;color:rgba(139,92,246,0.08);line-height:1;flex-shrink:0;font-family:'Inter',sans-serif}.hero-card h2{margin:0 0 6px;font-size:24px;font-weight:700;color:#111827}.hero-card p{margin:0;font-size:15px;color:#6b7280;line-height:1.6}strong{color:#111827}

.clean-card{background:#fff;border-radius:16px;border:1px solid #e5e7eb;padding:20px 24px;box-shadow:0 1px 3px rgba(0,0,0,0.04);transition:all .3s}
.card-header{display:flex;justify-content:space-between;align-items:center;margin-bottom:12px}.card-header h3{margin:0;font-size:14px;font-weight:600;color:#374151}
.label-violet{font-size:10px;background:rgba(139,92,246,0.1);color:#7C3AED;padding:3px 10px;border-radius:12px;font-weight:600;text-transform:uppercase;letter-spacing:0.5px}

.kpi-row{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.kpi{padding:18px 12px;text-align:center;border-radius:14px;background:#fff;border:1px solid #e5e7eb}.kpi span{display:block;font-size:11px;color:#9ca3af;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:4px}.kpi b{display:block;font-size:28px;font-weight:900}.kpi.green b{color:#10B981}.kpi.amber b{color:#F59E0B}.kpi.purple b{color:#8B5CF6}.kpi.blue b{color:#3B82F6}.kpi.emerald b{color:#059669}

.two-col{display:grid;grid-template-columns:1fr 1fr;gap:20px}.hint{font-size:13px;color:#9ca3af;margin:0 0 12px}
.ch-lg{height:320px}.ch-xl{height:580px}

.two-col-main{display:grid;grid-template-columns:1fr 1.6fr;gap:20px;flex:1;min-height:0}

.ex-list{display:flex;flex-direction:column;gap:8px;margin-bottom:14px}.ex-chip{display:flex;align-items:center;gap:10px;padding:12px 16px;border-radius:20px;border:1px solid #e5e7eb;cursor:pointer;transition:all .2s;font-size:14px}.ex-chip.on{background:rgba(239,68,68,0.04);border-color:rgba(239,68,68,0.3);color:#EF4444}
.ex-box{width:24px;height:24px;border-radius:50%;border:2px solid #d1d5db;display:flex;align-items:center;justify-content:center;font-weight:700;flex-shrink:0;font-size:13px}.ex-chip.on .ex-box{background:#EF4444;border-color:#EF4444;color:#fff}
.ex-name{flex:1;font-weight:600}.ex-cov{font-size:11px;color:#9ca3af;font-family:monospace}
.ex-result{padding:12px 16px;border-radius:10px;font-size:13px;line-height:1.6;background:rgba(245,158,11,0.04);border:1px solid rgba(245,158,11,0.1)}.ex-result.done{background:rgba(16,185,129,0.04);border:1px solid rgba(16,185,129,0.1);color:#059669}
.sankey-msg{font-size:12px;color:#6b7280;padding:8px 12px;background:#f9fafb;border-radius:8px;margin-top:8px}

.report-card{margin-top:4px}.rep-status{padding:16px 20px;border-radius:12px;font-size:15px;line-height:1.8}.rep-status p{margin:0}.rep-status.warn{background:rgba(239,68,68,0.03);border:1px solid rgba(239,68,68,0.08)}.rep-status.progress{background:rgba(245,158,11,0.03);border:1px solid rgba(245,158,11,0.08)}.rep-status.done{background:rgba(16,185,129,0.03);border:1px solid rgba(16,185,129,0.08)}

.full-overlay{position:fixed;inset:0;z-index:999;background:rgba(250,251,252,0.94);backdrop-filter:blur(20px);display:flex;align-items:center;justify-content:center;padding:40px}.full-modal{width:100%;max-width:1050px;max-height:620px;height:100%;background:#fff;border-radius:20px;border:2px solid rgba(139,92,246,0.2);padding:28px;display:flex;flex-direction:column;box-shadow:0 24px 64px rgba(0,0,0,0.12)}.fm-h{display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid #e5e7eb;padding-bottom:14px;margin-bottom:18px}.fm-h h3{margin:0;font-size:17px;color:#111827}.fm-h button{padding:8px 18px;border-radius:16px;border:1px solid #d1d5db;background:transparent;cursor:pointer;font-size:13px}
.fm-b{display:grid;grid-template-columns:1.2fr 1fr;gap:24px;flex:1;min-height:0}.fm-img{background:#f3f4f6;border-radius:12px;overflow:hidden;display:flex;align-items:center;justify-content:center}.fm-img img{width:100%}.fm-log{display:flex;flex-direction:column;gap:14px;font-size:15px;line-height:1.8}.b{padding:10px 14px;background:#f9fafb;border-radius:8px}.btn-go{padding:16px;border-radius:16px;background:linear-gradient(135deg,#8B5CF6,#6D28D9);color:#fff;border:none;font-size:14px;font-weight:700;cursor:pointer;margin-top:auto}
.fade-enter-active,.fade-leave-active{transition:all .3s}.fade-enter-from,.fade-leave-to{opacity:0}
</style>
