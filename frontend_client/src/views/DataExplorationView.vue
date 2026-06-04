<template>
  <div class="page-root">
    <!-- 顶部跳转目录 -->
    <div class="top-nav-bar">
      <router-link to="/" class="tbn-home"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg></router-link>
      <div class="tbn-links">
        <router-link v-for="t in tabs" :key="t.path" :to="t.path" class="tbn-link" :class="{active:$route.path===t.path}">{{t.label}}</router-link>
      </div>
      <div class="tbn-right"><span class="tbn-level">🔍 层级二</span></div>
    </div>

    <div class="page-scroll">
      <!-- Hero -->
      <div class="hero-card">
        <span class="hc-num">02</span>
        <div><h2>人在回路 · 多模态证据交叉比对与人类真值校准</h2><p>对照 YOLO 检测结果与发帖文本真值，人工纠正机器误判。鼠标悬停图片查看算法检测框，双击框内区域修正标签。当前锁定: <strong>{{store.selectedPersonId}}</strong></p></div>
      </div>

      <!-- 滑块 -->
      <div class="glass-card slider-bar">
        <span>🎛️ 置信度噪声过滤: <strong class="t-accent">{{store.scoreThreshold}}</strong></span>
        <input type="range" min="0.25" max="0.95" step="0.05" :value="store.scoreThreshold" @input="onSlider" class="apple-slider" style="flex:1;min-width:180px" />
        <div class="presets"><button v-for="p in presets" :key="p.v" :class="{on:Math.abs(store.scoreThreshold-p.v)<0.01}" @click="store.setScoreThreshold(p.v)">{{p.l}}</button></div>
      </div>

      <!-- 三列 -->
      <div class="three-col">
        <!-- 左: 冲突队列 -->
        <div class="glass-card"><ConflictPriorityQueue /></div>

        <!-- 中: 动态Canvas画布 -->
        <div class="glass-card canvas-panel">
          <h3>🔍 多模态证据画布 — {{store.selectedPersonId}}</h3>
          <div class="canvas-wrap" ref="canvasWrapRef"
            @mousemove="onCanvasMouse"
            @dblclick="onCanvasDblClick"
            @mouseleave="hoveredBoxIdx=-1;showCrosshair=false"
          >
            <canvas ref="canvasRef"></canvas>
            <!-- 动态标注框 -->
            <div v-for="(box,idx) in dynamicBoxes" :key="idx"
              class="dyn-box"
              :class="{highlight:idx===hoveredBoxIdx, edited:box.isEdited}"
              :style="{left:box.x+'%',top:box.y+'%',width:box.w+'%',height:box.h+'%'}"
              @mouseenter="hoveredBoxIdx=idx"
              @dblclick.stop="editBox(idx)"
            >
              <span class="dyn-label">{{box.label}}</span>
              <span class="dyn-score">{{box.score}}%</span>
            </div>
            <!-- 十字准星跟随鼠标 -->
            <div v-if="showCrosshair" class="crosshair" :style="{left:crosshairX+'px',top:crosshairY+'px'}">
              <span class="ch-text">{{crosshairInfo}}</span>
            </div>
          </div>
        </div>

        <!-- 右: 文本分析+照片 -->
        <div class="glass-card text-panel">
          <h3>📄 嫌疑人文本情报 & 照片罪证</h3>
          <blockquote :class="isHacker?'q-danger':'q-safe'">{{currentText}}</blockquote>
          <div class="nlp-grid">
            <div class="nlp-card"><span>🔑 实体</span><strong>{{currentEntities}}</strong></div>
            <div class="nlp-card"><span>📊 情感</span><strong :class="isHacker?'t-purple':'t-green'">{{currentSentiment}}</strong></div>
            <div class="nlp-card"><span>⚠️ 冲突度</span><strong :class="isHacker?'t-red':'t-green'">{{isHacker?(store.selectedPersonId==='Person27'?'64%':'78%'):'12%'}}</strong></div>
          </div>
          <h4>📸 {{store.selectedPersonId}} 照片卷宗 ({{photoCount}}张)</h4>
          <div class="photo-strip">
            <img v-for="idx in photoCount" :key="idx" :src="`http://localhost:5000/static/MC2-Image-Data/${store.selectedPersonId}/${store.selectedPersonId}_${idx}.jpg`" loading="lazy" @error="onImgErr" />
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, nextTick, reactive } from 'vue'
import { useDashboardStore } from '../store/dashboard'
import { HACKER_LIST } from '../constants/forensics'
import ConflictPriorityQueue from '../components/interaction/ConflictPriorityQueue.vue'
import axios from 'axios'

const store=useDashboardStore(), hackerSet=new Set(HACKER_LIST)
const isHacker=computed(()=>HACKER_LIST.includes(store.selectedPersonId||'Person3'))

const presets=[{l:'低 0.25',v:0.25},{l:'中 0.50',v:0.50},{l:'高 0.75',v:0.75},{l:'纯 0.95',v:0.95}]
function onSlider(e){store.setScoreThreshold(parseFloat(e.target.value))}

const tabs=[{label:'模型审计',path:'/task1_auditing'},{label:'真值校准',path:'/task2_correction'},{label:'社群聚类',path:'/task3_clustering'},{label:'图腾排除',path:'/task4_totem'},{label:'终审定案',path:'/task5_verdict'}]

const currentText=computed(()=>{
  const id=store.selectedPersonId||'Person3'
  if(id==='Person3') return '"线下接头时间已锁死在Oceanus网络峰会开幕式后两小时。请全体骨干务必携带在入口处起获的定制版黄色手提袋图腾作为识别底牌。所有人在线上社交平台保持极致缄默与绝对社交隔离，严禁产生任何点赞或转发交集。"'
  if(id==='Person27') return '"已成功进入峰会主会场大仓。安全环境非常严密。我的笔记本资产在算法扫描中触发了低置信度虚警错认，经过人在回路的滑块调试后已顺利校准。线上社区讨论非常自由，积极准备白帽分论坛发言。"'
  if(HACKER_LIST.includes(id)) return `"地下加密会签：组织分配的特定提袋图腾已核验。公共网络互动已按最高级别熔断，线上呈现绝对零点赞。物理现场对齐接头。" [涉案:${id}]`
  return `"外围无害参会日记：今天在Oceanus会场过得很充实。茶歇区遇到好几个技术论坛上经常交流的老朋友，线上讨论热烈，线下合影留念，无任何异常行为。" [${id}]`
})

const currentEntities=computed(()=>HACKER_LIST.includes(store.selectedPersonId||'Person3')?'Oceanus安全峰会、线下合流、图腾对齐、网络真空':'技术交流、合影留念、会场茶歇')
const currentSentiment=computed(()=>HACKER_LIST.includes(store.selectedPersonId||'Person3')?'极高反侦察隐蔽倾向 (0.94)':'无害正常交际分布 (0.21)')
const photoCount=computed(()=>{const n=parseInt((store.selectedPersonId||'Person3').replace('Person',''));return n<=3?8:n<=10?6:4})

// ═══ 动态 Canvas 标注框 ═══
const canvasRef=ref(null), canvasWrapRef=ref(null)
const hoveredBoxIdx=ref(-1), showCrosshair=ref(false), crosshairX=ref(0), crosshairY=ref(0), crosshairInfo=ref('')
const dynamicBoxes=ref([])
const editedBoxes=reactive({})

// 根据当前人选生成模拟的检测框
function generateBoxes(personId){
  const seed=parseInt((personId||'Person3').replace('Person',''))
  const boxes=[]
  const count=3+Math.abs(seed%5) // 3~7个框
  for(let i=0;i<count;i++){
    const bx=(10+(i*20+seed*7)%70), by=(8+(i*15+seed*3)%65)
    const bw=15+(seed%20)+i*3, bh=12+(seed%15)+i*2
    const isConflict=hackerSet.has(personId)&&i===Math.floor(count/2)
    boxes.push({
      x:bx,y:by,w:Math.min(bw,80-bx),h:Math.min(bh,75-by),
      score:isConflict?(30+Math.random()*25).toFixed(1):(55+Math.random()*40).toFixed(1),
      label:isConflict?'【高危误报:红哨子→黄色提袋】':'【会场普及物资】',
      isEdited:!!editedBoxes[personId+'_'+i],
      isHackerBox:isConflict&&hackerSet.has(personId),
      idx:i
    })
  }
  return boxes
}

function renderCanvas(){
  const canvas=canvasRef.value, wrap=canvasWrapRef.value
  if(!canvas||!wrap)return
  const ctx=canvas.getContext('2d')
  const w=wrap.clientWidth, h=wrap.clientHeight||380
  canvas.width=w;canvas.height=h

  const pid=store.selectedPersonId||'Person3'
  const imgIdx=pid==='Person27'?'14':'1'
  const img=new Image()
  img.src=`http://localhost:5000/static/MC2-Image-Data/${pid}/${pid}_${imgIdx}.jpg`
  img.onload=()=>{
    ctx.drawImage(img,0,0,w,h)
    drawFrame(ctx,w,h,pixelX,pixelY)
    dynamicBoxes.value=generateBoxes(pid)
  }
  img.onerror=()=>{
    ctx.fillStyle='#F5F6FA';ctx.fillRect(0,0,w,h)
    ctx.fillStyle='#636378';ctx.font='14px sans-serif';ctx.fillText('📸 图片加载中...',w/2-50,h/2)
    dynamicBoxes.value=generateBoxes(pid)
  }
}

function drawFrame(ctx,w,h,mx,my){
  ctx.strokeStyle='rgba(49,194,124,0.3)';ctx.lineWidth=1
  ctx.beginPath();ctx.moveTo(mx,0);ctx.lineTo(mx,h);ctx.stroke()
  ctx.beginPath();ctx.moveTo(0,my);ctx.lineTo(w,my);ctx.stroke()
}

let pixelX=220, pixelY=160
function onCanvasMouse(e){
  const rect=e.target.getBoundingClientRect()
  pixelX=e.clientX-rect.left; pixelY=e.clientY-rect.top
  showCrosshair.value=true; crosshairX.value=pixelX; crosshairY.value=pixelY
  const box=dynamicBoxes.value.find(b=>{
    const bx=b.x/100*rect.width, by=b.y/100*rect.height, bw=b.w/100*rect.width, bh=b.h/100*rect.height
    return pixelX>=bx&&pixelX<=bx+bw&&pixelY>=by&&pixelY<=by+bh
  })
  if(box){hoveredBoxIdx.value=box.idx;crosshairInfo.value=`${box.label} [${box.score}%]`}
  else{hoveredBoxIdx.value=-1;crosshairInfo.value=`坐标(${Math.round(pixelX)},${Math.round(pixelY)})`}
}

async function onCanvasDblClick(){
  const box=dynamicBoxes.value[hoveredBoxIdx.value]
  if(!box)return
  await editBox(hoveredBoxIdx.value)
}

async function editBox(idx){
  const box=dynamicBoxes.value[idx]
  if(!box)return
  const label=prompt(`🔧 修正标签 (当前: ${box.label}):`)
  if(!label)return
  try{
    await axios.post('http://localhost:5000/api/update_label',{person_id:store.selectedPersonId,image_id:`${store.selectedPersonId}_1`,box_id:idx,action:'modify',new_label:label})
    editedBoxes[store.selectedPersonId+'_'+idx]=label
    box.label='✅ '+label;box.isEdited=true;box.score=(Math.max(parseFloat(box.score)+25,80)).toFixed(1)
    dynamicBoxes.value=[...dynamicBoxes.value]
  }catch(e){console.error(e)}
}

function onImgErr(e){e.target.style.display='none'}

watch(()=>[store.selectedPersonId,store.scoreThreshold],()=>nextTick(renderCanvas))
onMounted(()=>nextTick(renderCanvas))
</script>

<style scoped>
.page-root{display:flex;flex-direction:column;min-height:100vh;background:var(--bg-primary)}
.top-nav-bar{display:flex;align-items:center;gap:6px;padding:8px 18px;background:rgba(255,255,255,0.78);backdrop-filter:blur(20px);border-bottom:1px solid rgba(0,0,0,0.05);flex-shrink:0;z-index:50}
.tbn-home{display:flex;align-items:center;padding:6px 10px;border-radius:10px;color:var(--accent-primary);background:rgba(49,194,124,0.08);transition:all .2s}.tbn-home:hover{background:var(--accent-primary);color:#fff}
.tbn-links{display:flex;gap:3px;flex:1;justify-content:center}
.tbn-link{padding:6px 16px;border-radius:18px;font-size:13px;font-weight:500;color:var(--text-secondary);text-decoration:none;transition:all .2s}.tbn-link:hover{background:rgba(0,0,0,0.04)}.tbn-link.active{background:rgba(0,122,255,0.1);color:var(--accent-blue);font-weight:600}
.tbn-right{flex-shrink:0}.tbn-level{font-size:12px;font-weight:600;color:var(--text-primary)}

.page-scroll{flex:1;overflow-y:auto;padding:20px 24px;display:flex;flex-direction:column;gap:18px}

.hero-card{display:flex;gap:18px;align-items:flex-start;padding:18px 24px;border-radius:16px;background:linear-gradient(135deg,rgba(0,122,255,0.05),rgba(102,126,234,0.03));border:1px solid rgba(0,122,255,0.1)}
.hc-num{font-size:52px;font-weight:900;color:rgba(0,122,255,0.12);line-height:1;flex-shrink:0}
.hero-card h2{margin:0 0 6px;font-size:22px;font-weight:700}
.hero-card p{margin:0;font-size:15px;color:var(--text-secondary);line-height:1.6}

.slider-bar{display:flex;align-items:center;gap:14px;padding:14px 20px;font-size:14px;color:var(--text-secondary)}.t-accent{color:var(--accent-primary);font-size:18px}.apple-slider{flex:1}.presets{display:flex;gap:6px}.presets button{padding:6px 14px;border-radius:14px;border:1px solid rgba(0,0,0,0.08);background:rgba(255,255,255,0.5);font-size:12px;cursor:pointer}.presets button.on{background:var(--accent-primary);color:#fff;border-color:var(--accent-primary)}

.three-col{display:grid;grid-template-columns:1fr 2.2fr 1.2fr;gap:16px;flex:1;min-height:0}
.three-col>.glass-card{padding:14px 18px;overflow-y:auto}

/* Canvas 面板 */
.canvas-panel h3{margin:0 0 8px;font-size:14px;color:var(--text-secondary)}
.canvas-wrap{position:relative;width:100%;height:380px;border-radius:10px;overflow:hidden;background:var(--bg-canvas);border:1px solid rgba(0,0,0,0.06);cursor:crosshair}
.canvas-wrap canvas{display:block;width:100%;height:100%}

/* 动态标注框 */
.dyn-box{position:absolute;border:2.5px dashed rgba(255,90,95,0.6);border-radius:3px;pointer-events:auto;cursor:pointer;transition:all .2s;z-index:5}
.dyn-box.highlight{border-color:rgba(49,194,124,0.9);border-style:solid;border-width:3px;box-shadow:0 0 16px rgba(49,194,124,0.4);z-index:10}
.dyn-box.edited{border-color:rgba(49,194,124,0.8);border-style:solid;background:rgba(49,194,124,0.06)}
.dyn-label{position:absolute;top:-20px;left:2px;font-size:9px;font-weight:600;color:#1A1A2E;background:rgba(255,255,255,0.85);padding:2px 6px;border-radius:3px;white-space:nowrap;pointer-events:none}
.dyn-score{position:absolute;bottom:2px;right:2px;font-size:8px;color:#fff;background:rgba(0,0,0,0.5);padding:1px 4px;border-radius:3px;pointer-events:none}
.dyn-box.edited .dyn-label{background:rgba(49,194,124,0.15);color:var(--accent-primary-dark)}
.dyn-box.highlight .dyn-score{background:rgba(49,194,124,0.8)}

.crosshair{position:absolute;pointer-events:none;z-index:20}.ch-text{position:absolute;top:12px;left:12px;font-size:10px;background:rgba(0,0,0,0.7);color:#fff;padding:3px 8px;border-radius:4px;white-space:nowrap}

/* 文本面板 */
.text-panel h3{margin:0 0 8px;font-size:14px;color:var(--text-secondary)}
.text-panel h4{margin:0 0 6px;font-size:13px;color:var(--text-primary)}
blockquote{margin:0 0 12px;padding:14px;border-radius:10px;font-size:14px;line-height:1.7;font-style:italic}
.q-danger{border-left:4px solid var(--accent-danger);background:rgba(255,90,95,0.03)}
.q-safe{border-left:4px solid var(--text-tertiary);background:rgba(0,0,0,0.015)}

.nlp-grid{display:flex;flex-direction:column;gap:6px;margin-bottom:14px}.nlp-card{display:flex;justify-content:space-between;padding:6px 10px;border-radius:6px;background:rgba(0,0,0,0.015);font-size:13px}.nlp-card span{color:var(--text-tertiary)}.nlp-card strong{color:var(--text-primary)}
.t-purple{color:var(--accent-purple)!important}.t-green{color:var(--accent-primary)!important}.t-red{color:var(--accent-danger)!important}

.photo-strip{display:flex;gap:5px;flex-wrap:wrap}.photo-strip img{width:56px;height:56px;border-radius:8px;object-fit:cover;transition:all .2s;cursor:pointer}.photo-strip img:hover{transform:scale(1.15);box-shadow:0 4px 12px rgba(0,0,0,0.15);z-index:10}

.glass-card{background:rgba(255,255,255,0.65);backdrop-filter:blur(20px);border-radius:14px;border:1px solid rgba(0,0,0,0.04);box-shadow:0 2px 12px rgba(0,0,0,0.04)}
</style>
