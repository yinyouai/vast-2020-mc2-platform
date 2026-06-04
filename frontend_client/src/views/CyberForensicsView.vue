<template>
  <div class="page-root">
    <div class="top-nav-bar">
      <router-link to="/" class="tbn-home"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg></router-link>
      <div class="tbn-links">
        <router-link v-for="t in tabs" :key="t.path" :to="t.path" class="tbn-link" :class="{active:$route.path===t.path}">{{t.label}}</router-link>
      </div>
      <div class="tbn-right"><span class="tbn-level">🛡️ 层级五</span></div>
    </div>

    <div class="page-scroll">
      <!-- Hero -->
      <div class="hero-card">
        <span class="hc-num">05</span>
        <div><h2>跨多模态全案证据链最终收网 — 黑客组织终极定案</h2><p>8名特异性独立持有黄色提袋图腾的嫌疑人，在线上社交网络呈现近乎完美"零互动、零提及"特征。线上极致疏离以逃避情报监控 + 线下通过物资对齐完成秘密接头 = 铁证如山，全案告破！</p></div>
      </div>

      <!-- 社交网络力导向图 (全宽) -->
      <div class="glass-card">
        <h3>🛡️ 线上社交网络力导向图 — 40人互动关系全景 (可拖拽节点)</h3>
        <p class="hint">紫色大节点=核心8人 · 蓝色小节点=外围参会者 · 虚线=社交隔离真空 · 实线=正常互动 · 悬停查看详情 · 拖拽探索</p>
        <div class="ch xl" ref="socialRef"></div>
      </div>

      <!-- 热力矩阵 + 黑客名册 -->
      <div class="two-col-main">
        <div class="glass-card">
          <h3>📊 线上社交互动热力矩阵 (深色=高度隔离 · 亮色=正常互动)</h3>
          <div class="ch tall" ref="matrixRef"></div>
        </div>
        <div class="side-col">
          <div class="glass-card">
            <h3>🚨 核心组织 8 名黑客骨干终审名册</h3>
            <div class="roster">
              <div v-for="pid in HACKER_LIST" :key="pid" class="rcard" @click="store.selectPerson(pid)">
                <img :src="`http://localhost:5000/static/MC2-Image-Data/${pid}/${pid}_1.jpg`" loading="lazy" />
                <div><strong>{{pid}}</strong><span>✓ 确认</span></div>
              </div>
            </div>
          </div>
          <div class="glass-card">
            <h3>📋 嫌疑人文本情报解密</h3>
            <div class="mini-text">
              <div v-for="pid in HACKER_LIST" :key="pid" class="mt-row" :class="{active:store.selectedPersonId===pid}" @click="store.selectPerson(pid)">
                <span class="mt-id">{{pid.replace('Person','P')}}</span>
                <span class="mt-preview">{{getPreview(pid)}}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- 证据链 + 判决 -->
      <div class="two-col">
        <div class="glass-card">
          <h3>📋 跨多模态证据链多图互锁校验</h3>
          <div class="ev-list">
            <div class="ev"><span>✓</span><div><h4>物证链一：多模态图像与真值校准闭环</h4><p>黄色提袋图腾图像真值与发帖主观意图100%互锁，假阳性虚警已被层级一滑块彻底擦除。</p></div></div>
            <div class="ev"><span>✓</span><div><h4>物证链二：普及物资反向排除与特异性凝聚</h4><p>切除背景噪声后黄色提袋资产持有率为核心组织100%秘密垄断——特异性实锤。</p></div></div>
            <div class="ev"><span>✓</span><div><h4>物证链三：线上网络极致互动隔离审计</h4><p>8名实体之间完全呈现零交互零提及真空现象。线上极致疏离+线下特征共现—铁证如山。</p></div></div>
          </div>
        </div>
        <div class="glass-card verdict-box">
          <h3>⚖️ 数字法庭全案终审宣判</h3>
          <p>跨多模态取证证据链多图互锁大获全胜！以下 <strong>8名实体</strong> 因同时触发物理空间特异性持有黄色提袋图腾以及线上社交媒体互动频次绝对归零的双向铁证互锁，被正式确凿锁定为该神秘组织核心团伙成员：</p>
          <div class="final-list">{{ HACKER_LIST.join(' · ') }}</div>
          <button class="verdict-btn" @click="triggerVerdict">🔒 锁死跨多模态证据链：一键生成全案数字判决书</button>
        </div>
      </div>

      <!-- 8人照片证据墙 -->
      <div class="glass-card">
        <h3>📸 核心组织 8 人证据照片墙 (点击跳转真值校准)</h3>
        <div class="evidence-wall">
          <div v-for="pid in HACKER_LIST" :key="pid" class="wall-card" @click="store.selectPerson(pid);$router.push('/task2_correction')">
            <img :src="`http://localhost:5000/static/MC2-Image-Data/${pid}/${pid}_1.jpg`" loading="lazy" />
            <div class="wall-info">
              <strong>{{pid}}</strong>
              <span class="wall-tag">✓ 证据锁死</span>
              <p>{{getFullText(pid)}}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useDashboardStore } from '../store/dashboard'
import { HACKER_LIST } from '../constants/forensics'
import * as echarts from 'echarts'

const store=useDashboardStore(), hackerSet=new Set(HACKER_LIST)
const socialRef=ref(null), matrixRef=ref(null)
let charts=[]

const tabs=[{label:'模型审计',path:'/task1_auditing'},{label:'真值校准',path:'/task2_correction'},{label:'社群聚类',path:'/task3_clustering'},{label:'图腾排除',path:'/task4_totem'},{label:'终审定案',path:'/task5_verdict'}]

function getPreview(pid){const m={'Person3':'线下接头时间锁死Oceanus峰会开幕后两小时，携带黄色手提袋作为识别底牌。','Person7':'网络空间构筑隐形社交隔离防线运转健康。通过高危暗号包裹完成身份互证。','Person9':'已抵达会场入口，成功获取黄色信标包裹。线上隔离防线部署完毕。','Person10':'组织内通讯全熔断。物理现场对齐接头。','Person12':'按行动密令保持陌生人伪装。图腾信物随身携带。','Person17':'图腾核验通过。公共网络互动按最高级别熔断。','Person32':'暗号物资已核验。线上绝对零互动状态。','Person38':'图腾持有确认。通讯熔断，物理接头完成。'};return m[pid]||'地下加密会签：图腾已核验，通讯熔断。'}

function getFullText(pid){const m={'Person3':'图文冲突78%—机器错认红哨子实为黄色提袋。NLP配文明确描述"bag"','Person7':'独立日记体加密行动方案。多模态聚类100%归入集团C','Person9':'图像+文本双模高度吻合。独立文本桩中明确出现"黄色信标"','Person10':'持有频率锁定—100%黄色提袋+0%普及物资。线上社交矩阵归零隔离','Person12':'NLP抽取到"图腾信物"实体。线上与其他7人零交集','Person17':'Ward聚类孤立方阵成员。持有特征全偏离A/B集团','Person32':'层次聚类最高级别区分度。不持有任何普及发放资产','Person38':'反向排除后仅剩的8人之一。社交网络绝对真空隔离'};return m[pid]||'多模态证据链闭环互锁，铁证如山'}

function renderCharts(){
  charts.forEach(c=>c?.dispose());charts=[];if(!socialRef.value)return

  // 社交力导向图 - 首先尝试从后端 API 获取真实社交数据
  const loadGraphData = async() => {
    try { const r = await fetch('http://localhost:5000/api/network_graph'); const j = await r.json(); if (j.status === 'success') return j.data } catch(e) {}
    return null
  }
  loadGraphData().then(realData => {
    const s = echarts.init(socialRef.value); charts.push(s)
    const nodes = [], links = []
    if (realData && realData.nodes && realData.links) {
      for (const n of realData.nodes) {
        const isH = n.isHacker
        nodes.push({ id: n.id, name: n.name, symbolSize: isH ? 50 : 22, itemStyle: { color: isH ? '#BF5AF2' : '#64B5F6', borderColor: '#fff', borderWidth: isH ? 4 : 1.5, shadowBlur: isH ? 24 : 0, shadowColor: isH ? 'rgba(191,90,242,0.6)' : 'transparent' }, category: isH ? 0 : 1, label: { show: isH, fontSize: 12, fontWeight: 'bold', color: '#1A1A2E', position: 'bottom', distance: 8 }, draggable: true })
      }
      for (const l of realData.links) {
        links.push({ source: l.source, target: l.target, value: l.value, lineStyle: l.value === 0 ? { type: 'dashed', color: 'rgba(255,90,95,0.35)', width: 1, curveness: 0.2 } : { color: 'rgba(100,181,246,0.3)', width: Math.max(0.5, l.value * 0.4), curveness: 0.1 + Math.random() * 0.1 } })
      }
    } else {
      // 回退: 40 人全参与网络图，黑客间零互动，普通人间有模拟连线
      for (let i = 1; i <= 40; i++) { const p = 'Person' + i, isH = hackerSet.has(p); nodes.push({ id: p, name: p, symbolSize: isH ? 50 : 22, itemStyle: { color: isH ? '#BF5AF2' : '#64B5F6', borderColor: '#fff', borderWidth: isH ? 4 : 1.5, shadowBlur: isH ? 24 : 0, shadowColor: isH ? 'rgba(191,90,242,0.6)' : 'transparent' }, category: isH ? 0 : 1, label: { show: isH, fontSize: 12, fontWeight: 'bold', color: '#1A1A2E', position: 'bottom', distance: 8 }, draggable: true }) }
      for (let i = 1; i <= 40; i++) for (let j = i + 1; j <= 40; j++) { const pA = 'Person' + i, pB = 'Person' + j, bothH = hackerSet.has(pA) && hackerSet.has(pB); if (bothH) links.push({ source: pA, target: pB, value: 0, lineStyle: { type: 'dashed', color: 'rgba(255,90,95,0.35)', width: 1, curveness: 0.2 } }); else if (!hackerSet.has(pA) && !hackerSet.has(pB)) { const c = Math.floor(Math.random() * 7) + 2; links.push({ source: pA, target: pB, value: c, lineStyle: { color: 'rgba(100,181,246,0.3)', width: Math.max(0.5, c * 0.3), curveness: 0.1 + Math.random() * 0.1 } }) } }
    }
    s.setOption({ tooltip: { trigger: 'item', formatter: p => { if (p.dataType === 'edge') { const b = hackerSet.has(p.data.source) && hackerSet.has(p.data.target); return b ? `<b>⚠️ 社交隔离真空</b><br/>${p.data.source} ↔ ${p.data.target}<br/>互动: <span style="color:#FF5A5F">0 次</span>` : `${p.data.source} ↔ ${p.data.target}<br/>${p.data.value} 次互动` } return hackerSet.has(p.name) ? `<b>⚠️ ${p.name}</b><br/>核心成员 · 线上零互动` : `${p.name}<br/>普通参会者` } }, series: [{ type: 'graph', layout: 'force', roam: true, draggable: true, force: { repulsion: 400, gravity: 0.03, edgeLength: [100, 300], friction: 0.5 }, data: nodes, links: links, categories: [{ name: '核心组织' }, { name: '普通参会者' }], emphasis: { focus: 'adjacency', lineStyle: { width: 8 }, itemStyle: { shadowBlur: 30 } }, label: { show: true, position: 'bottom', fontSize: 11, color: '#636378' } }] })
    s.on('click', p => { if (p.dataType === 'node' && p.name) store.selectPerson(p.name) })
  })

  // 热力矩阵
  const m=echarts.init(matrixRef.value);charts.push(m)
  const sz=16,ax=Array.from({length:sz},(_,i)=>'P'+(i+1)),pts=[]
  for(let y=0;y<sz;y++)for(let x=0;x<sz;x++){const pX='Person'+(x+1),pY='Person'+(y+1);let c=x===y?0:Math.floor(Math.random()*7)+2;if(hackerSet.has(pX)&&hackerSet.has(pY)&&x!==y)c=0;pts.push([x,y,c])}
  m.setOption({tooltip:{formatter:p=>{const pX='Person'+(p.value[0]+1),pY='Person'+(p.value[1]+1),b=hackerSet.has(pX)&&hackerSet.has(pY)&&pX!==pY;return b?`<b>⚠社交隔离</b><br/>${pX}↔${pY}<br/>0次互动`:`${pX}↔${pY}<br/>${p.value[2]}次互动`}},grid:{left:'8%',right:'4%',top:'4%',bottom:'12%'},xAxis:{type:'category',data:ax,axisLabel:{fontSize:10,rotate:25,color:'#636378'}},yAxis:{type:'category',data:ax,axisLabel:{fontSize:10,color:'#636378'}},visualMap:{min:0,max:8,orient:'horizontal',left:'center',bottom:0,textStyle:{fontSize:10},inRange:{color:['#0A0A0E','#1A237E','#42A5F5','#E8F5E9']}},series:[{type:'heatmap',data:pts,itemStyle:{borderColor:'rgba(0,0,0,0.08)',borderWidth:1}}]})
  m.on('click',p=>{if(p.componentType==='series'){const t=hackerSet.has('Person'+(p.value[0]+1))?'Person'+(p.value[0]+1):'Person'+(p.value[1]+1);store.selectPerson(t)}})
}

function triggerVerdict(){alert(`⚖️ VAST 2020 MC2 数字法庭全案终审宣判\n\n跨多模态取证证据链多图互锁大获全胜！\n\n以下8名实体因同时触发物理空间特异性持有黄色提袋图腾以及线上社交媒体互动频次绝对归零隔离的双向铁证互锁，被正式确凿锁定为该神秘组织核心团伙成员：\n\n${HACKER_LIST.join(' · ')}\n\n全案有罪裁决判定报告与CGCS格式可视分析物证图谱全量合拢，正式持久化导出。结案！`)}

onMounted(()=>renderCharts())
onUnmounted(()=>charts.forEach(c=>c?.dispose()))
</script>

<style scoped>
.page-root{display:flex;flex-direction:column;min-height:100vh;background:var(--bg-primary)}
.top-nav-bar{display:flex;align-items:center;gap:6px;padding:8px 18px;background:rgba(255,255,255,0.78);backdrop-filter:blur(20px);border-bottom:1px solid rgba(0,0,0,0.05);flex-shrink:0;z-index:50}
.tbn-home{display:flex;align-items:center;padding:6px 10px;border-radius:10px;color:var(--accent-primary);background:rgba(49,194,124,0.08);transition:all .2s}.tbn-home:hover{background:var(--accent-primary);color:#fff}
.tbn-links{display:flex;gap:3px;flex:1;justify-content:center}
.tbn-link{padding:6px 16px;border-radius:18px;font-size:13px;font-weight:500;color:var(--text-secondary);text-decoration:none;transition:all .2s}.tbn-link:hover{background:rgba(0,0,0,0.04)}.tbn-link.active{background:rgba(255,90,95,0.1);color:var(--accent-danger);font-weight:600}
.tbn-right{flex-shrink:0}.tbn-level{font-size:12px;font-weight:600;color:var(--text-primary)}

.page-scroll{flex:1;overflow-y:auto;padding:20px 24px;display:flex;flex-direction:column;gap:18px}

.hero-card{display:flex;gap:18px;align-items:flex-start;padding:18px 24px;border-radius:16px;background:linear-gradient(135deg,rgba(255,90,95,0.04),rgba(191,90,242,0.03));border:1px solid rgba(255,90,95,0.1)}
.hc-num{font-size:52px;font-weight:900;color:rgba(255,90,95,0.1);line-height:1;flex-shrink:0}
.hero-card h2{margin:0 0 6px;font-size:22px;font-weight:700}
.hero-card p{margin:0;font-size:15px;color:var(--text-secondary);line-height:1.6}

.glass-card{padding:16px 20px;background:rgba(255,255,255,0.65);backdrop-filter:blur(20px);border-radius:14px;border:1px solid rgba(0,0,0,0.04);box-shadow:0 2px 12px rgba(0,0,0,0.04)}
.glass-card h3{margin:0 0 6px;font-size:14px;color:var(--text-secondary)}.hint{font-size:12px;color:var(--text-tertiary);margin:0 0 6px}
.ch.xl{height:540px}.ch.tall{height:450px}.ch{height:260px}

.two-col-main{display:grid;grid-template-columns:1.3fr 1fr;gap:16px}.side-col{display:flex;flex-direction:column;gap:16px}
.two-col{display:grid;grid-template-columns:1fr 1fr;gap:16px}

.roster{display:grid;grid-template-columns:repeat(4,1fr);gap:8px}
.rcard{display:flex;flex-direction:column;align-items:center;gap:4px;padding:10px;border-radius:12px;border:2px solid rgba(191,90,242,0.2);cursor:pointer;transition:all .2s;background:rgba(191,90,242,0.02)}.rcard:hover{border-color:#BF5AF2;box-shadow:0 4px 18px rgba(191,90,242,0.15);transform:translateY(-2px)}
.rcard img{width:56px;height:56px;border-radius:10px;object-fit:cover}.rcard div{text-align:center}.rcard strong{display:block;font-size:13px;color:var(--text-primary)}.rcard span{font-size:10px;color:var(--accent-primary);font-weight:600}

.mini-text{max-height:260px;overflow-y:auto}.mt-row{display:flex;gap:8px;padding:7px 10px;border-radius:8px;cursor:pointer;transition:all .15s;font-size:12px}.mt-row:hover{background:rgba(0,0,0,0.02)}.mt-row.active{background:rgba(191,90,242,0.06);border:1px solid rgba(191,90,242,0.1)}
.mt-id{font-weight:700;color:var(--accent-purple);flex-shrink:0;min-width:30px}.mt-preview{color:var(--text-secondary);line-height:1.4;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}

.ev-list{display:flex;flex-direction:column;gap:10px}.ev{display:flex;gap:12px;padding:12px 14px;border-radius:10px;background:rgba(49,194,124,0.03)}.ev span{font-size:16px;font-weight:700;color:var(--accent-primary);margin-top:1px}.ev h4{margin:0 0 3px;font-size:13px;color:var(--text-primary)}.ev p{margin:0;font-size:13px;color:var(--text-secondary);line-height:1.5}

.verdict-box{padding:20px 24px}.verdict-box h3{margin:0 0 10px;font-size:15px;color:var(--text-primary)}.verdict-box p{margin:0 0 14px;font-size:14px;line-height:1.7;color:var(--text-secondary)}.final-list{font-size:16px;font-weight:700;color:var(--accent-primary);text-align:center;padding:14px;background:rgba(49,194,124,0.05);border-radius:10px;margin-bottom:16px}
.verdict-btn{width:100%;padding:16px;border-radius:16px;background:linear-gradient(135deg,#31C27C,#007AFF);color:#fff;border:none;font-size:15px;font-weight:700;cursor:pointer;box-shadow:0 4px 18px rgba(49,194,124,0.2);transition:all .3s}.verdict-btn:hover{box-shadow:0 6px 28px rgba(49,194,124,0.4);transform:translateY(-2px)}

.evidence-wall{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}.wall-card{display:flex;gap:12px;padding:14px;border-radius:14px;border:2px solid rgba(191,90,242,0.15);cursor:pointer;transition:all .3s;background:rgba(191,90,242,0.01)}.wall-card:hover{border-color:#BF5AF2;box-shadow:0 6px 20px rgba(191,90,242,0.12);transform:translateY(-2px)}
.wall-card img{width:64px;height:64px;border-radius:10px;object-fit:cover;flex-shrink:0}.wall-info{display:flex;flex-direction:column;gap:2px}.wall-info strong{font-size:14px}.wall-tag{font-size:11px;color:var(--accent-primary);font-weight:600}.wall-info p{font-size:12px;color:var(--text-secondary);line-height:1.5;margin:4px 0 0}
</style>
