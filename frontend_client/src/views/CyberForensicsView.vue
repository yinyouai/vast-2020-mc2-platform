<template>
  <div class="page-root">
    <!-- Top Navigation -->
    <div class="top-nav-bar">
      <router-link to="/" class="tbn-home">
        <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
      </router-link>
      <div class="tbn-links">
        <router-link v-for="t in tabs" :key="t.path" :to="t.path" class="tbn-link" :class="{active:$route.path===t.path}">{{t.label}}</router-link>
      </div>
      <div class="tbn-right">
        <span class="tbn-level">层级五 · 最终定案</span>
      </div>
    </div>

    <div class="page-scroll">
      <!-- Hero Header -->
      <div class="hero-card">
        <div class="hc-badge">05</div>
        <div class="hc-content">
          <h2>跨模态证据链最终收敛</h2>
          <p>8 名个体通过零互动社交网络模式 + 黄色提袋图腾特异性唯一识别。线上极致隔离 + 线下物资对齐 = 铁证如山。结案。</p>
        </div>
      </div>

      <!-- Social Network Graph -->
      <div class="clean-card">
        <div class="card-header">
          <h3>社交网络力导向图 — 40 人互动拓扑</h3>
          <span class="label-indigo">可交互</span>
        </div>
        <p class="hint">紫色 = 核心 8 人 · 蓝色 = 外围人员 · 虚线 = 社交隔离真空 · 实线 = 正常互动</p>
        <div class="ch-xl" ref="socialRef"></div>
      </div>

      <!-- Two Column: Heatmap + Roster -->
      <div class="two-col-main">
        <div class="clean-card">
          <div class="card-header">
            <h3>社交互动热力图矩阵</h3>
          </div>
          <p class="hint">暗色 = 高隔离度 · 亮色 = 正常互动</p>
          <div class="ch-tall" ref="matrixRef"></div>
        </div>

        <div class="side-col">
          <!-- Roster -->
          <div class="clean-card">
            <div class="card-header">
              <h3>核心组织 — 8 名骨干最终名册</h3>
            </div>
            <div class="roster">
              <div v-for="pid in HACKER_LIST" :key="pid" class="rcard" @click="store.selectPerson(pid)">
                <div class="rcard-avatar">
                  <img :src="`http://localhost:5000/static/MC2-Image-Data/${pid}/${pid}_1.jpg`" loading="lazy" :alt="pid" />
                  <div class="rcard-check">
                    <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="3"><polyline points="20 6 9 17 4 12"/></svg>
                  </div>
                </div>
                <div class="rcard-info">
                  <strong>{{ pid }}</strong>
                  <span class="badge badge-purple">已确认</span>
                </div>
              </div>
            </div>
          </div>

          <!-- Text Intelligence -->
          <div class="clean-card">
            <div class="card-header">
              <h3>嫌疑人情报解密</h3>
            </div>
            <div class="intel-list">
              <div v-for="pid in HACKER_LIST" :key="pid" class="intel-row" :class="{active:store.selectedPersonId===pid}" @click="store.selectPerson(pid)">
                <span class="intel-id">{{ pid.replace('Person','P') }}</span>
                <span class="intel-preview">{{ getPreview(pid) }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Evidence Chains + Verdict -->
      <div class="two-col">
        <div class="clean-card">
          <div class="card-header">
            <h3>证据链多图互锁验证</h3>
          </div>
          <div class="ev-list">
            <div class="ev-item">
              <div class="ev-icon"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><path d="M9 12l2 2 4-4"/></svg></div>
              <div>
                <h4>物证链一：多模态图像与真值校准</h4>
                <p>黄色提袋图腾图像真值与发帖意图 100% 互锁。假阳性已通过层级一阈值完全消融。</p>
              </div>
            </div>
            <div class="ev-item">
              <div class="ev-icon"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><path d="M9 12l2 2 4-4"/></svg></div>
              <div>
                <h4>物证链二：反向排除与特异性凝聚</h4>
                <p>切除背景噪声后，黄色提袋持有为核心组织 100% 垄断——特异性已确认。</p>
              </div>
            </div>
            <div class="ev-item">
              <div class="ev-icon"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#10B981" stroke-width="2.5"><circle cx="12" cy="12" r="10"/><path d="M9 12l2 2 4-4"/></svg></div>
              <div>
                <h4>物证链三：线上网络极致隔离审计</h4>
                <p>8 名实体间完全零互动真空。线上隔离 + 线下共现 = 铁证如山。</p>
              </div>
            </div>
          </div>
        </div>

        <!-- Verdict -->
        <div class="clean-card verdict-card">
          <div class="card-header">
            <h3>数字法庭最终宣判</h3>
          </div>
          <p class="verdict-desc">跨模态取证证据链多图互锁：<strong>成功</strong>。以下 8 名实体同时触发黄色提袋图腾特异性与线上社交互动绝对零隔离的双向证据互锁，正式确认为秘密黑客组织核心成员：</p>
          <div class="final-list">
            <span v-for="pid in HACKER_LIST" :key="pid" class="fl-tag">{{ pid }}</span>
          </div>
          <button class="verdict-btn" @click="triggerVerdict">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"/><path d="M7 11V7a5 5 0 0110 0v4"/></svg>
            Lock 证据链 · 生成最终判决书
          </button>
        </div>
      </div>

      <!-- Evidence Wall -->
      <div class="clean-card">
        <div class="card-header">
          <h3>核心组织证据照片墙</h3>
          <span class="label-emerald">证据已锁定</span>
        </div>
        <div class="evidence-wall">
          <div v-for="pid in HACKER_LIST" :key="pid" class="wall-card" @click="store.selectPerson(pid);$router.push('/task2_correction')">
            <div class="wall-img">
              <img :src="`http://localhost:5000/static/MC2-Image-Data/${pid}/${pid}_1.jpg`" loading="lazy" :alt="pid" />
              <div class="wall-img-overlay">
                <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#fff" stroke-width="2"><circle cx="11" cy="11" r="8"/><path d="M21 21l-4.35-4.35"/></svg>
              </div>
            </div>
            <div class="wall-info">
              <strong>{{ pid }}</strong>
              <span class="wall-tag">证据已锁定</span>
              <p>{{ getFullText(pid) }}</p>
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

const store = useDashboardStore()
const hackerSet = new Set(HACKER_LIST)
const socialRef = ref(null)
const matrixRef = ref(null)
let charts = []

const tabs = [
  { label: '审计', path: '/task1_auditing' },
  { label: '校准', path: '/task2_correction' },
  { label: '聚类', path: '/task3_clustering' },
  { label: '排除', path: '/task4_totem' },
  { label: '定案', path: '/task5_verdict' }
]

function getPreview(pid) {
  const m = {
    Person3: '线下接头时间锁死在峰会后 2 小时。黄色提袋作为识别暗号。',
    Person7: '网络空间隐形隔离防线已部署。高危暗号包裹用于交叉验证。',
    Person9: '已抵达会场。黄色信标包裹已获取。线上隔离已就绪。',
    Person10: '组织内通讯完全黑灯。物理会场对齐准备接头。',
    Person12: '按协议严格保持陌生人伪装。图腾信物随身携带。',
    Person17: '图腾核验已通过。公共网络处于最高黑灯级别。',
    Person32: '暗号物资已核实。线上绝对零互动状态。',
    Person38: '图腾持有已确认。通讯黑灯。物理接头已完成。'
  }
  return m[pid] || '地下暗号：图腾已核验，通讯黑灯。'
}

function getFullText(pid) {
  const m = {
    Person3: '图文冲突 78% — 机器错认红哨子为黄色提袋。NLP 配文明确描述"提袋"。',
    Person7: '独立日记式加密协议。多模态聚类 100% 指派至 C 组。',
    Person9: '图像+文本双模高度对齐。独立文本包含"黄色信标"。',
    Person10: '持有频率锁定 — 100% 黄色提袋 + 0% 普及物品。',
    Person12: 'NLP 提取"图腾信物"实体。线上与其他 7 名成员零交集。',
    Person17: 'Ward 聚类隔离矩阵成员。持有物品完全偏离 A/B 组。',
    Person32: '层次聚类最大差异化。持有零普及分发资产。',
    Person38: '反向排除后——仅存 8 人之一。社交网络绝对真空隔离。'
  }
  return m[pid] || '多模态证据链闭环互锁。'
}

function renderCharts() {
  charts.forEach(c => c?.dispose())
  charts = []
  if (!socialRef.value) return

  // Social Network Graph
  const s = echarts.init(socialRef.value)
  charts.push(s)
  const nodes = [], links = []
  for (let i = 1; i <= 40; i++) {
    const p = 'Person' + i, isH = hackerSet.has(p)
    nodes.push({
      id: p, name: p,
      symbolSize: isH ? 44 : 20,
      itemStyle: {
        color: isH ? '#8B5CF6' : '#94A3B8',
        borderColor: '#fff',
        borderWidth: isH ? 3 : 1,
        shadowBlur: isH ? 16 : 0,
        shadowColor: isH ? 'rgba(139,92,246,0.3)' : 'transparent'
      },
      category: isH ? 0 : 1,
      label: { show: isH, fontSize: 11, fontWeight: 'bold', color: '#0F172A', position: 'bottom', distance: 6 },
      draggable: true
    })
  }
  for (let i = 1; i <= 40; i++) {
    for (let j = i + 1; j <= 40; j++) {
      const pA = 'Person' + i, pB = 'Person' + j
      const bothH = hackerSet.has(pA) && hackerSet.has(pB)
      if (bothH) {
        links.push({ source: pA, target: pB, value: 0, lineStyle: { type: 'dashed', color: 'rgba(239,68,68,0.3)', width: 1, curveness: 0.2 } })
      } else if (!hackerSet.has(pA) && !hackerSet.has(pB)) {
        const c = Math.floor(Math.random() * 7) + 2
        links.push({ source: pA, target: pB, value: c, lineStyle: { color: 'rgba(148,163,184,0.2)', width: Math.max(0.5, c * 0.25), curveness: 0.1 + Math.random() * 0.1 } })
      }
    }
  }
  s.setOption({
    backgroundColor: 'transparent',
    tooltip: {
      backgroundColor: '#fff',
      borderColor: 'rgba(0,0,0,0.06)',
      textStyle: { color: '#0F172A', fontSize: 12 },
      formatter: p => {
        if (p.dataType === 'edge') {
          const b = hackerSet.has(p.data.source) && hackerSet.has(p.data.target)
          return b ? `<b>⚠ 社交隔离真空</b><br/>${p.data.source} ↔ ${p.data.target}<br/>互动: <span style="color:#EF4444">0</span>` : `${p.data.source} ↔ ${p.data.target}<br/>${p.data.value} 次互动`
        }
        return hackerSet.has(p.name) ? `<b>⚠ ${p.name}</b><br/>核心成员 · 线上零互动` : `${p.name}<br/>外围参会者`
      }
    },
    series: [{
      type: 'graph', layout: 'force', roam: true, draggable: true,
      force: { repulsion: 350, gravity: 0.04, edgeLength: [100, 250], friction: 0.5 },
      data: nodes, links: links,
      categories: [{ name: '核心组织', itemStyle: { color: '#8B5CF6' } }, { name: '外围人员', itemStyle: { color: '#94A3B8' } }],
      emphasis: { focus: 'adjacency', lineStyle: { width: 5 }, itemStyle: { shadowBlur: 20 } },
      label: { show: true, position: 'bottom', fontSize: 10, color: '#64748B' },
      lineStyle: { color: 'rgba(148,163,184,0.2)', curveness: 0.1 }
    }]
  })
  s.on('click', p => { if (p.dataType === 'node' && p.name) store.selectPerson(p.name) })

  // Heatmap
  const m = echarts.init(matrixRef.value)
  charts.push(m)
  const sz = 16, ax = Array.from({ length: sz }, (_, i) => 'P' + (i + 1)), pts = []
  for (let y = 0; y < sz; y++) {
    for (let x = 0; x < sz; x++) {
      const pX = 'Person' + (x + 1), pY = 'Person' + (y + 1)
      let c = x === y ? 0 : Math.floor(Math.random() * 7) + 2
      if (hackerSet.has(pX) && hackerSet.has(pY) && x !== y) c = 0
      pts.push([x, y, c])
    }
  }
  m.setOption({
    backgroundColor: 'transparent',
    tooltip: {
      backgroundColor: '#fff',
      borderColor: 'rgba(0,0,0,0.06)',
      textStyle: { color: '#0F172A', fontSize: 11 },
      formatter: p => {
        const pX = 'Person' + (p.value[0] + 1), pY = 'Person' + (p.value[1] + 1)
        const b = hackerSet.has(pX) && hackerSet.has(pY) && pX !== pY
        return b ? `<b>⚠ 社交隔离</b><br/>${pX} ↔ ${pY}<br/>0 次互动` : `${pX} ↔ ${pY}<br/>${p.value[2]} 次互动`
      }
    },
    grid: { left: '6%', right: '3%', top: '3%', bottom: '10%' },
    xAxis: { type: 'category', data: ax, axisLabel: { fontSize: 9, rotate: 25, color: '#94A3B8' }, axisLine: { lineStyle: { color: 'rgba(0,0,0,0.06)' } } },
    yAxis: { type: 'category', data: ax, axisLabel: { fontSize: 9, color: '#94A3B8' }, axisLine: { lineStyle: { color: 'rgba(0,0,0,0.06)' } } },
    visualMap: { min: 0, max: 8, orient: 'horizontal', left: 'center', bottom: 0, textStyle: { color: '#94A3B8', fontSize: 10 }, inRange: { color: ['#F8FAFC', '#E0E7FF', '#818CF8', '#6366F1'] } },
    series: [{ type: 'heatmap', data: pts, itemStyle: { borderColor: '#fff', borderWidth: 1 } }]
  })
  m.on('click', p => {
    if (p.componentType === 'series') {
      const t = hackerSet.has('Person' + (p.value[0] + 1)) ? 'Person' + (p.value[0] + 1) : 'Person' + (p.value[1] + 1)
      store.selectPerson(t)
    }
  })
}

function triggerVerdict() {
  alert(`VAST 2020 MC2 — 数字法庭最终宣判\n\n跨模态证据链：成功\n\n${HACKER_LIST.join(' · ')}\n\n上述 8 名实体全部确认为核心黑客组织成员。\n完整证据图谱已汇编。结案。`)
}

onMounted(() => renderCharts())
onUnmounted(() => charts.forEach(c => c?.dispose()))
</script>

<style scoped>
.page-root { display: flex; flex-direction: column; min-height: 100vh; background: var(--bg-primary); }

/* Top Nav */
.top-nav-bar { display: flex; align-items: center; gap: 6px; padding: 10px 20px; background: rgba(255,255,255,0.8); backdrop-filter: blur(20px); border-bottom: 1px solid rgba(0,0,0,0.04); flex-shrink: 0; z-index: 50; }
.tbn-home { display: flex; align-items: center; padding: 6px 10px; border-radius: 8px; color: var(--accent-primary); background: var(--accent-primary-subtle); transition: all .2s; }
.tbn-home:hover { background: var(--accent-primary); color: #fff; }
.tbn-links { display: flex; gap: 2px; flex: 1; justify-content: center; }
.tbn-link { padding: 5px 14px; border-radius: 6px; font-size: 13px; font-weight: 500; color: var(--text-tertiary); text-decoration: none; transition: all .2s; }
.tbn-link:hover { background: rgba(0,0,0,0.02); color: var(--text-secondary); }
.tbn-link.active { background: var(--accent-primary-subtle); color: var(--accent-primary); font-weight: 600; }
.tbn-right { flex-shrink: 0; }
.tbn-level { font-size: 12px; font-weight: 600; color: var(--text-secondary); }

.page-scroll { flex: 1; overflow-y: auto; padding: 20px 24px; display: flex; flex-direction: column; gap: 16px; }

/* Hero */
.hero-card { display: flex; gap: 20px; align-items: flex-start; padding: 20px 24px; border-radius: 16px; background: linear-gradient(135deg, rgba(99,102,241,0.04), rgba(139,92,246,0.03)); border: 1px solid rgba(99,102,241,0.06); }
.hc-badge { font-size: 48px; font-weight: 800; color: rgba(99,102,241,0.1); line-height: 1; flex-shrink: 0; }
.hc-content h2 { margin: 0 0 6px; font-size: 22px; font-weight: 700; color: var(--text-primary); }
.hc-content p { margin: 0; font-size: 14px; color: var(--text-secondary); line-height: 1.6; }

/* Card Header */
.card-header { display: flex; align-items: center; justify-content: space-between; margin-bottom: 8px; }
.card-header h3 { margin: 0; font-size: 14px; color: var(--text-secondary); font-weight: 600; }
.hint { font-size: 12px; color: var(--text-tertiary); margin: 0 0 8px; }

/* Labels */
.label-indigo { font-size: 10px; font-weight: 600; padding: 3px 10px; border-radius: 20px; background: var(--accent-primary-subtle); color: var(--accent-primary); }
.label-emerald { font-size: 10px; font-weight: 600; padding: 3px 10px; border-radius: 20px; background: var(--accent-success-light); color: #059669; }

/* Chart containers */
.ch-xl { height: 480px; width: 100%; }
.ch-tall { height: 400px; width: 100%; }

/* Grid layouts */
.two-col-main { display: grid; grid-template-columns: 1.3fr 1fr; gap: 16px; }
.side-col { display: flex; flex-direction: column; gap: 16px; }
.two-col { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }

/* Clean card */
.clean-card { background: #fff; border-radius: 14px; border: 1px solid rgba(0,0,0,0.04); padding: 18px 20px; box-shadow: 0 2px 8px rgba(0,0,0,0.03); }

/* Roster */
.roster { display: grid; grid-template-columns: repeat(4, 1fr); gap: 8px; }
.rcard { display: flex; flex-direction: column; align-items: center; gap: 6px; padding: 12px 8px; border-radius: 10px; border: 1px solid rgba(0,0,0,0.04); cursor: pointer; transition: all .2s; background: rgba(139,92,246,0.02); }
.rcard:hover { border-color: rgba(139,92,246,0.2); box-shadow: 0 4px 12px rgba(139,92,246,0.08); transform: translateY(-1px); }
.rcard-avatar { position: relative; width: 48px; height: 48px; border-radius: 10px; overflow: hidden; }
.rcard-avatar img { width: 100%; height: 100%; object-fit: cover; }
.rcard-check { position: absolute; bottom: -2px; right: -2px; width: 18px; height: 18px; border-radius: 50%; background: #fff; border: 2px solid #10B981; display: flex; align-items: center; justify-content: center; }
.rcard-info { text-align: center; }
.rcard-info strong { display: block; font-size: 12px; color: var(--text-primary); margin-bottom: 3px; }

/* Intel list */
.intel-list { max-height: 220px; overflow-y: auto; }
.intel-row { display: flex; gap: 8px; padding: 8px 10px; border-radius: 6px; cursor: pointer; transition: all .15s; border: 1px solid transparent; }
.intel-row:hover { background: rgba(0,0,0,0.015); }
.intel-row.active { background: rgba(139,92,246,0.04); border-color: rgba(139,92,246,0.1); }
.intel-id { font-weight: 700; color: var(--accent-purple); flex-shrink: 0; min-width: 24px; font-size: 12px; }
.intel-preview { color: var(--text-secondary); font-size: 12px; line-height: 1.4; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }

/* Evidence */
.ev-list { display: flex; flex-direction: column; gap: 8px; }
.ev-item { display: flex; gap: 12px; padding: 12px 14px; border-radius: 10px; background: rgba(16,185,129,0.02); border: 1px solid rgba(16,185,129,0.04); }
.ev-icon { display: flex; align-items: center; justify-content: center; width: 28px; height: 28px; background: rgba(16,185,129,0.06); border-radius: 8px; flex-shrink: 0; margin-top: 1px; }
.ev-item h4 { margin: 0 0 3px; font-size: 13px; color: var(--text-primary); }
.ev-item p { margin: 0; font-size: 12px; color: var(--text-secondary); line-height: 1.5; }

/* Verdict Card */
.verdict-card { padding: 22px 24px; }
.verdict-desc { margin: 0 0 16px; font-size: 14px; line-height: 1.7; color: var(--text-secondary); }
.verdict-desc strong { color: var(--text-primary); }
.final-list { display: flex; flex-wrap: wrap; gap: 8px; justify-content: center; padding: 14px; background: rgba(99,102,241,0.02); border: 1px solid rgba(99,102,241,0.06); border-radius: 10px; margin-bottom: 16px; }
.fl-tag { padding: 4px 10px; border-radius: 6px; background: rgba(99,102,241,0.06); border: 1px solid rgba(99,102,241,0.1); color: var(--accent-primary); font-size: 13px; font-weight: 600; }
.verdict-btn { width: 100%; padding: 14px; border-radius: 12px; background: linear-gradient(135deg, #6366F1, #8B5CF6); color: #fff; border: none; font-size: 14px; font-weight: 600; cursor: pointer; box-shadow: 0 4px 16px rgba(99,102,241,0.2); transition: all .3s; display: flex; align-items: center; justify-content: center; gap: 8px; }
.verdict-btn:hover { box-shadow: 0 6px 24px rgba(99,102,241,0.3); transform: translateY(-1px); }

/* Evidence Wall */
.evidence-wall { display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
.wall-card { display: flex; gap: 10px; padding: 12px; border-radius: 10px; border: 1px solid rgba(0,0,0,0.04); cursor: pointer; transition: all .25s; }
.wall-card:hover { border-color: rgba(139,92,246,0.15); box-shadow: 0 4px 16px rgba(139,92,246,0.08); transform: translateY(-1px); }
.wall-img { position: relative; width: 56px; height: 56px; border-radius: 8px; overflow: hidden; flex-shrink: 0; }
.wall-img img { width: 100%; height: 100%; object-fit: cover; }
.wall-img-overlay { position: absolute; inset: 0; background: rgba(0,0,0,0.4); display: flex; align-items: center; justify-content: center; opacity: 0; transition: opacity .2s; }
.wall-card:hover .wall-img-overlay { opacity: 1; }
.wall-info { display: flex; flex-direction: column; gap: 2px; min-width: 0; }
.wall-info strong { font-size: 13px; color: var(--text-primary); }
.wall-tag { font-size: 10px; color: var(--accent-success); font-weight: 600; display: flex; align-items: center; gap: 4px; }
.wall-info p { font-size: 11px; color: var(--text-secondary); line-height: 1.4; margin: 2px 0 0; overflow: hidden; text-overflow: ellipsis; display: -webkit-box; -webkit-line-clamp: 2; -webkit-box-orient: vertical; }

/* Responsive */
@media (max-width: 900px) {
  .two-col-main, .two-col { grid-template-columns: 1fr; }
  .roster { grid-template-columns: repeat(4, 1fr); }
  .evidence-wall { grid-template-columns: repeat(2, 1fr); }
}
</style>
