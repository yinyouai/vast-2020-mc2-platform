<template>
  <div class="page-root">
    <div class="top-nav-bar">
      <router-link to="/" class="tbn-home"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg></router-link>
      <div class="tbn-links">
        <router-link v-for="t in tabs" :key="t.path" :to="t.path" class="tbn-link" :class="{active:$route.path===t.path}">{{t.label}}</router-link>
      </div>
      <div class="tbn-right"><span class="tbn-level">🔮 层级四</span></div>
    </div>

    <div class="page-scroll">
      <div class="hero-card">
        <span class="hc-num">04</span>
        <div><h2>秘密图腾反向排除 & 力导向网络图分析</h2><p>会场免费分发物资形成极强背景噪声。利用反向排除漏斗一键切除高持有率大众资产，逼迫核心黑客组织线下接头暗号图腾在流向图与力导向图中显现！已排除 <strong class="t-purple">{{store.excludedItems.length}}/4</strong> 项。</p></div>
      </div>

      <!-- 排除控制 + 桑基图 -->
      <div class="two-col">
        <div class="glass-card">
          <h3>⚙️ 反向排除漏斗控制台</h3>
          <p class="hint">勾选放逐会场免费分发的高覆盖率物资，每一个勾选都是向真相逼近一步</p>
          <div class="ex-list">
            <label v-for="item in excludeItems" :key="item.id" class="ex-chip" :class="{on:store.excludedItems.includes(item.id)}" @click="toggle(item.id)">
              <span class="ex-box">{{store.excludedItems.includes(item.id)?'✕':''}}</span>
              <span class="ex-name">{{item.cnName}}</span>
              <span class="ex-cov">覆盖{{item.coverage}}%</span>
            </label>
          </div>
          <div class="ex-result" :class="{done:store.excludedItems.length>=3}">
            <span v-if="store.excludedItems.length>=3">🎉 去噪纯度达标！秘密图腾已锁定——点击下方网络图中「黄色提袋」节点查看物证</span>
            <span v-else>⚠️ 请继续勾选放逐普及物资 (至少排除3项以解锁深度下钻)</span>
          </div>
        </div>
        <div class="glass-card">
          <h3>📊 物资持有率削波对比 (排除后归零)</h3>
          <div class="ch" ref="barRef"></div>
        </div>
      </div>

      <!-- 桑基图 + 力导向网络图 -->
      <div class="two-col-main">
        <div class="glass-card">
          <h3>🔮 资产漏斗流向图 (桑基拓扑传导)</h3>
          <div class="ch" ref="sankeyRef"></div>
          <div class="sankey-msg">{{sankeyMsg}}</div>
        </div>
        <div class="glass-card">
          <h3>🔮 人-物关联力导向网络图 (40人 + 物资节点)</h3>
          <div class="ch xl" ref="networkRef"></div>
        </div>
      </div>

      <!-- 报告 -->
      <div class="glass-card report-card">
        <h3>📡 去噪剥离研判报告</h3>
        <div v-if="store.excludedItems.length===0" class="rep-status warn"><p>❌ <b>背景干扰过高(未去噪)：</b>全网发帖资产里充斥着海量会场泛滥礼品噪声。普通参会白帽(Person27)的笔记本与真正黑客的黄色提袋在光谱中交织共现，无法分辨无辜路人与高危团伙！请开始勾选放逐普及物资。</p></div>
        <div v-else-if="store.excludedItems.length<3" class="rep-status progress"><p>⏳ <b>反向排除进行中(纯度提升)：</b>已排除{{store.excludedItems.length}}项背景物资。大量无辜参会人员行为光谱向正常背景收敛。请继续放逐更多普及物资！</p></div>
        <div v-else class="rep-status done"><p>🎉 <b>地下接头暗号图腾完全破译！</b>当会场大众礼品被反向切除后，整个全景社交资产流以100%极高数学纯度全部收敛汇聚指向唯一的<strong>【秘密黄色接头提袋】</strong>！8名黑客被锁死。</p></div>
      </div>
    </div>

    <Teleport to="body">
      <transition name="fade">
        <div v-if="store.isFourthLayerActive" class="full-overlay" @click.self="store.isFourthLayerActive=false">
          <div class="full-modal">
            <div class="fm-h"><h3>🛸 像素级物证链级联钻取: 黄色提袋图腾</h3><button @click="store.isFourthLayerActive=false">✕ 关闭</button></div>
            <div class="fm-b">
              <div class="fm-img"><img src="http://localhost:5000/static/MC2-Image-Data/Person3/Person3_1.jpg"/></div>
              <div class="fm-log">
                <div class="b">🟩 <b>特异性实锤：</b>全场40人中除8人组织外其余32人对此资产持有率为绝对零共现！</div>
                <div class="b">🟩 <b>图文矛盾闭环：</b>YOLO严重错认后人类真值校准以100%数学纯度凝结为秘密图腾。</div>
                <button @click="store.isFourthLayerActive=false;$router.push('/task5_verdict')" class="btn-go">证据锁死：前往层级五核对社交隔离网</button>
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
import { useRouter } from 'vue-router'
import { useDashboardStore } from '../store/dashboard'
import { HACKER_LIST, EXCLUDABLE_ITEMS } from '../constants/forensics'
import * as echarts from 'echarts'

const store=useDashboardStore(), router=useRouter(), hackerSet=new Set(HACKER_LIST)
const excludeItems=EXCLUDABLE_ITEMS
const barRef=ref(null),sankeyRef=ref(null),networkRef=ref(null)
let charts=[]

const tabs=[{label:'模型审计',path:'/task1_auditing'},{label:'真值校准',path:'/task2_correction'},{label:'社群聚类',path:'/task3_clustering'},{label:'图腾排除',path:'/task4_totem'},{label:'终审定案',path:'/task5_verdict'}]
function toggle(id){const c=[...store.excludedItems];const i=c.indexOf(id);if(i>-1)c.splice(i,1);else c.push(id);store.excludedItems=c;store.fetchHeatmapMatrix()}

const sankeyMsg=computed(()=>{if(store.excludedItems.length===0)return'❌ 噪声过高——线索模糊——请开始排除';if(store.excludedItems.length<3)return`⏳ 排除进行中(${store.excludedItems.length}/4)——光谱逐收敛`;return'🎉 铁证图腾锁死——100%纯度指向黄色提袋'})

function renderAll(){
  charts.forEach(c=>c?.dispose());charts=[];if(!barRef.value)return

  const bar=echarts.init(barRef.value);charts.push(bar)
  const bi=[{n:'薰衣草骰子',v:60,k:'lavenderDie'},{n:'参会胸章',v:60,k:'sign'},{n:'通用发夹',v:47,k:'hairClip'},{n:'高危红哨子',v:45,k:'redWhistle'},{n:'南瓜便签',v:35,k:'pumpkinNotes'},{n:'秘密黄色提袋',v:20,k:'yellowBag'}]
  bar.setOption({tooltip:{trigger:'axis'},grid:{left:'8%',right:'4%',top:'6%',bottom:'15%'},xAxis:{type:'category',data:bi.map(d=>d.n),axisLabel:{rotate:15,fontSize:10}},yAxis:{type:'value',max:100},series:[{type:'bar',data:bi.map((d,i)=>({value:store.excludedItems.includes(d.k)?0:d.v,itemStyle:{color:i===5?'#BF5AF2':'#31C27C',opacity:store.excludedItems.includes(d.k)?.3:1}})),barWidth:'38%'}]})

  const sank=echarts.init(sankeyRef.value);charts.push(sank)
  const excl=store.excludedItems.length,nf=excl>=3?5:excl===0?50:25,sf=35
  sank.setOption({tooltip:{trigger:'item'},series:[{type:'sankey',layout:'none',emphasis:{focus:'adjacency'},data:[{name:'40名候选人',itemStyle:{color:'#64B5F6'}},{name:'免费礼品背景',itemStyle:{color:'#BDBDBD'}},{name:'秘密组织暗号',itemStyle:{color:'#BF5AF2'}},{name:'💛黄色提袋',itemStyle:{color:'#FFD54F'}}],links:[{source:'40名候选人',target:'免费礼品背景',value:nf},{source:'40名候选人',target:'秘密组织暗号',value:sf},{source:'秘密组织暗号',target:'💛黄色提袋',value:sf}],nodeWidth:18,nodeGap:18,label:{fontSize:12,color:'#1A1A2E'},lineStyle:{color:'source',curveness:.5}}]})
  sank.on('click',p=>{if((p.name||'').includes('黄色提袋')||p.name==='秘密组织暗号'){if(store.excludedItems.length>=3)store.isFourthLayerActive=true;else alert('请先排除≥3项普及物资')}})

  // 力导向网络图
  const net=echarts.init(networkRef.value);charts.push(net)
  const nodes=[],links=[]
  for(let i=1;i<=40;i++){const p='Person'+i,isH=hackerSet.has(p);nodes.push({id:p,name:p,symbolSize:isH?42:22,category:isH?0:1,itemStyle:{color:isH?'#BF5AF2':'#64B5F6',borderColor:'#fff',borderWidth:isH?3:1,shadowBlur:isH?16:0,shadowColor:isH?'rgba(191,90,242,0.5)':'transparent'},label:{show:isH,fontSize:11,fontWeight:'bold',color:'#1A1A2E',position:'bottom',distance:5},draggable:true})}
  const exSet=new Set(store.excludedItems)
  const its=[{id:'yellowBag',n:'💛黄色提袋',c:'#BF5AF2',t:true},{id:'redWhistle',n:'红哨子',c:'#FF5A5F'},{id:'pumpkinNotes',n:'南瓜便签',c:'#FF8C00'},{id:'hairClip',n:'发夹',c:'#FF9F0A'},{id:'eyeball',n:'眼球玩具',c:'#00BFFF'},{id:'lavenderDie',n:'薰衣草骰子',c:'#9370DB'},{id:'paperPlate',n:'纸盘',c:'#A9A9A9'}]
  its.filter(it=>!exSet.has(it.id)).forEach(it=>{nodes.push({id:it.id,name:it.n,symbolSize:it.t?40:28,category:it.t?2:3,itemStyle:{color:it.c,borderColor:'#fff',borderWidth:it.t?3:1.5,shadowBlur:it.t?16:0,shadowColor:it.t?'rgba(191,90,242,0.5)':'transparent'},label:{show:true,fontSize:10,color:'#1A1A2E'},draggable:false})})
  for(let i=1;i<=40;i++){const p='Person'+i,isH=hackerSet.has(p);its.filter(it=>!exSet.has(it.id)).forEach((it,idx)=>{let has=false;if(it.t)has=isH;else has=((i*(idx+1)*7)%100)<(it.id==='lavenderDie'?60:it.id==='redWhistle'?45:it.id==='hairClip'?47:35)&&!isH;if(has)links.push({source:p,target:it.id,lineStyle:{color:it.t?'rgba(191,90,242,0.55)':'rgba(180,190,200,0.2)',width:it.t?2.8:.8,curveness:.1}})})}
  net.setOption({tooltip:{trigger:'item',formatter:p=>p.dataType==='node'?`<b>${p.name}</b>`:p.data.source+'→'+p.data.target},legend:{show:true,bottom:5,textStyle:{fontSize:10},data:['黑客(8人)','普通参会者','秘密图腾','普通物资']},series:[{type:'graph',layout:'force',roam:true,draggable:true,force:{repulsion:400,gravity:.05,edgeLength:[60,200],layoutAnimation:true,friction:.5},data:nodes,links:links,categories:[{name:'黑客(8人)',itemStyle:{color:'#BF5AF2'}},{name:'普通参会者',itemStyle:{color:'#64B5F6'}},{name:'秘密图腾',itemStyle:{color:'#BF5AF2'}},{name:'普通物资',itemStyle:{color:'#6495ED'}}],emphasis:{focus:'adjacency',lineStyle:{width:6},itemStyle:{shadowBlur:20}},label:{show:true,position:'bottom',fontSize:11,color:'#636378'}}]})
}

watch(()=>store.excludedItems,()=>nextTick(renderAll),{deep:true})
onMounted(()=>nextTick(renderAll))
onUnmounted(()=>charts.forEach(c=>c?.dispose()))
</script>

<style scoped>
.page-root{display:flex;flex-direction:column;min-height:100vh;background:var(--bg-primary)}
.top-nav-bar{display:flex;align-items:center;gap:6px;padding:8px 18px;background:rgba(255,255,255,0.78);backdrop-filter:blur(20px);border-bottom:1px solid rgba(0,0,0,0.05);flex-shrink:0;z-index:50}
.tbn-home{display:flex;align-items:center;padding:6px 10px;border-radius:10px;color:var(--accent-primary);background:rgba(49,194,124,0.08);transition:all .2s}.tbn-home:hover{background:var(--accent-primary);color:#fff}
.tbn-links{display:flex;gap:3px;flex:1;justify-content:center}
.tbn-link{padding:6px 16px;border-radius:18px;font-size:13px;font-weight:500;color:var(--text-secondary);text-decoration:none;transition:all .2s}.tbn-link:hover{background:rgba(0,0,0,0.04)}.tbn-link.active{background:rgba(191,90,242,0.1);color:var(--accent-purple);font-weight:600}
.tbn-right{flex-shrink:0}.tbn-level{font-size:12px;font-weight:600;color:var(--text-primary)}

.page-scroll{flex:1;overflow-y:auto;padding:20px 24px;display:flex;flex-direction:column;gap:18px}

.hero-card{display:flex;gap:18px;align-items:flex-start;padding:18px 24px;border-radius:16px;background:linear-gradient(135deg,rgba(191,90,242,0.04),rgba(102,126,234,0.03));border:1px solid rgba(191,90,242,0.1)}
.hc-num{font-size:52px;font-weight:900;color:rgba(191,90,242,0.12);line-height:1;flex-shrink:0}
.hero-card h2{margin:0 0 6px;font-size:22px;font-weight:700}
.hero-card p{margin:0;font-size:15px;color:var(--text-secondary);line-height:1.6}
.t-purple{color:var(--accent-purple);font-size:20px}

.two-col{display:grid;grid-template-columns:1fr 1fr;gap:16px}.glass-card{padding:16px 20px;background:rgba(255,255,255,0.65);backdrop-filter:blur(20px);border-radius:14px;border:1px solid rgba(0,0,0,0.04);box-shadow:0 2px 12px rgba(0,0,0,0.04)}
.two-col h3,.two-col-main h3{margin:0 0 8px;font-size:14px;color:var(--text-secondary)}.hint{font-size:13px;color:var(--text-tertiary);margin:0 0 10px}
.ch{height:270px}.ch.xl{height:540px}

.two-col-main{display:grid;grid-template-columns:1fr 1.6fr;gap:16px;flex:1;min-height:0}
.two-col-main .glass-card{overflow:hidden}

.ex-list{display:flex;flex-direction:column;gap:7px;margin-bottom:12px}
.ex-chip{display:flex;align-items:center;gap:10px;padding:10px 14px;border-radius:20px;border:1px solid rgba(0,0,0,0.06);cursor:pointer;transition:all .2s;font-size:14px}.ex-chip.on{background:rgba(255,90,95,0.05);border-color:rgba(255,90,95,0.25);color:#FF5A5F}
.ex-box{width:22px;height:22px;border-radius:50%;border:2px solid rgba(0,0,0,0.12);display:flex;align-items:center;justify-content:center;font-weight:700;flex-shrink:0}.ex-chip.on .ex-box{background:#FF5A5F;border-color:#FF5A5F;color:#fff}
.ex-name{flex:1;font-weight:500}.ex-cov{font-size:11px;opacity:.6;font-family:monospace}
.ex-result{padding:10px 14px;border-radius:10px;font-size:13px;background:rgba(255,159,10,0.04);border:1px solid rgba(255,159,10,0.1);line-height:1.5}.ex-result.done{background:rgba(49,194,124,0.05);border-color:rgba(49,194,124,0.1);color:var(--accent-primary-dark)}

.sankey-msg{font-size:12px;color:var(--text-secondary);padding:6px 10px;background:rgba(0,0,0,0.015);border-radius:6px;margin-top:6px}

.report-card{padding:18px 24px}.report-card h3{margin:0 0 10px;font-size:15px}
.rep-status{padding:14px 18px;border-radius:10px;font-size:14px;line-height:1.7}.rep-status.warn{background:rgba(255,90,95,0.03);border:1px solid rgba(255,90,95,0.08)}.rep-status.progress{background:rgba(255,159,10,0.03);border:1px solid rgba(255,159,10,0.08)}.rep-status.done{background:rgba(49,194,124,0.03);border:1px solid rgba(49,194,124,0.08)}.rep-status p{margin:0}

.full-overlay{position:fixed;inset:0;z-index:999;background:rgba(245,246,250,0.94);backdrop-filter:blur(20px);display:flex;align-items:center;justify-content:center;padding:40px}
.full-modal{width:100%;max-width:1050px;max-height:600px;height:100%;background:#fff;border-radius:18px;border:2px solid rgba(191,90,242,0.2);padding:24px;display:flex;flex-direction:column;box-shadow:0 20px 60px rgba(0,0,0,0.15)}
.fm-h{display:flex;justify-content:space-between;align-items:center;border-bottom:1px solid rgba(0,0,0,0.06);padding-bottom:12px;margin-bottom:16px}.fm-h h3{margin:0;font-size:16px}.fm-h button{padding:8px 16px;border-radius:16px;border:1px solid rgba(0,0,0,0.1);background:transparent;cursor:pointer;font-size:13px}
.fm-b{display:grid;grid-template-columns:1.2fr 1fr;gap:20px;flex:1;min-height:0}
.fm-img{background:var(--bg-secondary);border-radius:10px;overflow:hidden;display:flex;align-items:center;justify-content:center}.fm-img img{width:100%}
.fm-log{display:flex;flex-direction:column;gap:14px;font-size:14px;line-height:1.7}.b{padding:10px 14px;background:rgba(0,0,0,0.02);border-radius:8px}
.btn-go{padding:14px;border-radius:16px;background:linear-gradient(135deg,#BF5AF2,#651fff);color:#fff;border:none;font-size:14px;font-weight:700;cursor:pointer;margin-top:auto}
</style>
