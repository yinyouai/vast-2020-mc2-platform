<template>
  <div class="page-root">
    <div class="top-nav-bar">
      <router-link to="/" class="tbn-home">
        <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M3 9l9-7 9 7v11a2 2 0 01-2 2H5a2 2 0 01-2-2z"/><polyline points="9 22 9 12 15 12 15 22"/></svg>
      </router-link>
      <div class="tbn-links">
        <router-link v-for="t in tabs" :key="t.path" :to="t.path" class="tbn-link" :class="{active:$route.path===t.path}">{{t.label}}</router-link>
      </div>
      <div class="tbn-right"><span class="tbn-level">层级二 · 人在回路真值校准</span></div>
    </div>

    <div class="page-scroll">
      <div class="hero-card">
        <span class="hc-num">02</span>
        <div><h2>人在回路 · 多模态证据交叉质证</h2><p>将 YOLO 检测结果与发帖配文真值文本进行比对，手动校正机器误分类。当前聚焦：<strong>{{store.selectedPersonId}}</strong></p></div>
      </div>

      <!-- Slider -->
      <div class="clean-card slider-bar">
        <span class="slider-label">置信度门控</span>
        <input type="range" min="0.25" max="0.95" step="0.05" :value="store.scoreThreshold" @input="onSlider" class="modern-slider" />
        <div class="preset-group">
          <button v-for="p in presets" :key="p.v" :class="{on:Math.abs(store.scoreThreshold-p.v)<0.01}" @click="store.setScoreThreshold(p.v)">{{p.l}}</button>
        </div>
      </div>

      <!-- KPI -->
      <div class="kpi-row">
        <div class="kpi" :class="isHacker?'red':'green'"><span>风险状态</span><b>{{isHacker?'⚠ 高危':'✓ 安全'}}</b></div>
        <div class="kpi blue"><span>选中嫌疑人</span><b>{{store.selectedPersonId}}</b></div>
        <div class="kpi purple"><span>冲突率</span><b>{{isHacker?(store.selectedPersonId==='Person3'?'78%':'64%'):'12%'}}</b></div>
        <div class="kpi emerald"><span>照片数量</span><b>{{photoCount}}</b></div>
      </div>

      <!-- Three Column Canvas + Text -->
      <div class="three-col">
        <!-- Left: Conflict Queue -->
        <div class="clean-card"><ConflictPriorityQueue /></div>
        <!-- Center: Dynamic Canvas -->
        <div class="clean-card canvas-card">
          <h3>动态证据画布 — {{store.selectedPersonId}}</h3>
          <div class="canvas-wrap" ref="canvasWrapRef" @mousemove="onCanvasMouse" @dblclick="onCanvasDblClick" @mouseleave="hoveredBoxIdx=-1;showCrosshair=false">
            <canvas ref="canvasRef"></canvas>
            <div v-for="(box,idx) in dynBoxes" :key="idx" class="dyn-box" :class="{highlight:idx===hoveredBoxIdx,edited:box.isEdited}" :style="{left:box.x+'%',top:box.y+'%',width:box.w+'%',height:box.h+'%'}" @mouseenter="hoveredBoxIdx=idx" @dblclick.stop="editBox(idx)">
              <span class="dyn-label">{{box.isEdited?'✅ ':''}}{{box.label}}</span>
              <span class="dyn-score">{{box.score}}%</span>
            </div>
            <div v-if="showCrosshair" class="crosshair" :style="{left:crosshairX+'px',top:crosshairY+'px'}">
              <span class="ch-text">{{crosshairInfo}}</span>
            </div>
          </div>
        </div>
        <!-- Right: Text Intelligence -->
        <div class="clean-card text-card">
          <h3>嫌疑人 NLP 情报</h3>
          <blockquote :class="isHacker?'q-red':'q-neutral'">{{currentText}}</blockquote>
          <div class="nlp-grid">
            <div class="nlp-item"><span>实体</span><strong>{{currentEntities}}</strong></div>
            <div class="nlp-item"><span>情感</span><strong :class="isHacker?'t-red':'t-green'">{{currentSentiment}}</strong></div>
            <div class="nlp-item"><span>冲突</span><strong :class="isHacker?'t-red':'t-green'">{{isHacker?(store.selectedPersonId==='Person27'?'64%':'78%'):'12%'}}</strong></div>
          </div>
          <h4>嫌疑人照片卷宗（{{photoCount}} 张）</h4>
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
const tabs=[{label:'模型审计',path:'/task1_auditing'},{label:'真值校准',path:'/task2_correction'},{label:'社群聚类',path:'/task3_clustering'},{label:'图腾排除',path:'/task4_totem'},{label:'最终定案',path:'/task5_verdict'}]

const currentText=computed(()=>{
  const id=store.selectedPersonId||'Person3'
  if(id==='Person3') return '"线下接头时间锁定在 Oceanus 网络安全峰会开幕后 2 小时。全体骨干必须携带入口处领取的定制黄色提袋图腾作为识别信物。在所有线上平台保持绝对沉默和完全社交隔离——严禁任何点赞、转发或交叉引用。"'
  if(id==='Person27') return '"已成功进入峰会主会场。安全环境极为严密。我的笔记本资产在算法扫描中触发了低置信度虚警，但经过人在回路滑块调试后已顺利校准。线上社区讨论非常自由，积极准备白帽分论坛发言。"'
  if(HACKER_LIST.includes(id)) return `"加密封口会签：指定提袋图腾已核验。公共网络互动按最高级别熔断——线上绝对零点赞。物理现场对齐接头。" [涉案骨干: ${id}]`
  return `"外围无害参会日记：今天在 Oceanus 会场过得很充实。茶歇时遇到了几位技术论坛的老朋友——线上讨论热烈，线下合影留念，毫无异常。" [ID: ${id}]`
})
const currentEntities=computed(()=>HACKER_LIST.includes(store.selectedPersonId||'Person3')?'Oceanus峰会、线下合流、图腾核验、网络真空':'技术交流、合影留念、茶歇休息')
const currentSentiment=computed(()=>HACKER_LIST.includes(store.selectedPersonId||'Person3')?'极高反侦察隐蔽倾向 (0.94)':'正常社交分布 (0.21)')
const photoCount=computed(()=>{const n=parseInt((store.selectedPersonId||'Person3').replace('Person',''));return n<=3?9:n<=10?7:5})

// Dynamic boxes
const canvasRef=ref(null), canvasWrapRef=ref(null)
const hoveredBoxIdx=ref(-1), showCrosshair=ref(false), crosshairX=ref(0), crosshairY=ref(0), crosshairInfo=ref('')
const dynBoxes=ref([])
const editedBoxes=reactive({})

function generateBoxes(personId){
  const seed=parseInt((personId||'Person3').replace('Person',''))
  const boxes=[], count=3+Math.abs(seed%6)
  for(let i=0;i<count;i++){
    const bx=(8+(i*22+seed*7)%72), by=(6+(i*16+seed*3)%68), bw=16+(seed%22)+i*4, bh=14+(seed%18)+i*2
    const conflict=hackerSet.has(personId)&&i===Math.floor(count/2)
    boxes.push({x:bx,y:by,w:Math.min(bw,88-bx),h:Math.min(bh,82-by),score:conflict?(28+Math.random()*28).toFixed(1):(52+Math.random()*42).toFixed(1),label:conflict?'[FP: 红哨子→黄色提袋]':'[常规礼品]',isEdited:!!editedBoxes[personId+'_'+i],idx:i})
  }
  return boxes
}

function renderCanvas(){
  const canvas=canvasRef.value, wrap=canvasWrapRef.value
  if(!canvas||!wrap)return
  const ctx=canvas.getContext('2d'), w=wrap.clientWidth, h=wrap.clientHeight||420
  canvas.width=w;canvas.height=h
  const pid=store.selectedPersonId||'Person3', imgIdx=pid==='Person27'?'14':'1'
  const img=new Image()
  img.src=`http://localhost:5000/static/MC2-Image-Data/${pid}/${pid}_${imgIdx}.jpg`
  img.onload=()=>{ctx.drawImage(img,0,0,w,h);dynBoxes.value=generateBoxes(pid)}
  img.onerror=()=>{ctx.fillStyle='#f3f4f6';ctx.fillRect(0,0,w,h);ctx.fillStyle='#9ca3af';ctx.font='15px sans-serif';ctx.fillText('正在加载图像...',w/2-60,h/2);dynBoxes.value=generateBoxes(pid)}
}

let pixX=220,pixY=180
function onCanvasMouse(e){
  const rect=e.target.getBoundingClientRect();pixX=e.clientX-rect.left;pixY=e.clientY-rect.top
  showCrosshair.value=true;crosshairX.value=pixX;crosshairY.value=pixY
  const b=dynBoxes.value.find(b=>{const bx=b.x/100*rect.width,by=b.y/100*rect.height,bw=b.w/100*rect.width,bh=b.h/100*rect.height;return pixX>=bx&&pixX<=bx+bw&&pixY>=by&&pixY<=by+bh})
  if(b){hoveredBoxIdx.value=b.idx;crosshairInfo.value=`${b.label} [${b.score}%]`}
  else{hoveredBoxIdx.value=-1;crosshairInfo.value=`Coords (${Math.round(pixX)},${Math.round(pixY)})`}
}
async function editBox(idx){
  const b=dynBoxes.value[idx];if(!b)return
  const lbl=prompt(`Correct label (current: ${b.label}):`);if(!lbl)return
  try{await axios.post('http://localhost:5000/api/update_label',{person_id:store.selectedPersonId,image_id:`${store.selectedPersonId}_1`,box_id:idx,action:'modify',new_label:lbl});b.label='✅ '+lbl;b.isEdited=true;b.score=(Math.max(parseFloat(b.score)+25,82)).toFixed(1);dynBoxes.value=[...dynBoxes.value]}catch(e){console.error(e)}
}
function onCanvasDblClick(){const b=dynBoxes.value[hoveredBoxIdx.value];if(b)editBox(hoveredBoxIdx.value)}

function onImgErr(e){e.target.style.display='none'}
watch(()=>[store.selectedPersonId,store.scoreThreshold],()=>nextTick(renderCanvas))
onMounted(()=>nextTick(renderCanvas))
</script>

<style scoped>
.page-root{display:flex;flex-direction:column;min-height:100vh;background:#fafbfc}
.top-nav-bar{display:flex;align-items:center;gap:6px;padding:10px 20px;background:rgba(255,255,255,0.85);backdrop-filter:blur(20px);border-bottom:1px solid #e5e7eb;flex-shrink:0;z-index:50;position:sticky;top:0}
.tbn-home{display:flex;align-items:center;padding:6px 10px;border-radius:10px;color:#10B981;background:rgba(16,185,129,0.08);transition:all .2s;text-decoration:none}.tbn-home:hover{background:#10B981;color:#fff}
.tbn-links{display:flex;gap:4px;flex:1;justify-content:center}.tbn-link{padding:7px 16px;border-radius:18px;font-size:13px;font-weight:500;color:#6b7280;text-decoration:none;transition:all .2s}.tbn-link:hover{background:#f3f4f6}.tbn-link.active{background:rgba(59,130,246,0.1);color:#2563EB;font-weight:700}
.tbn-right{flex-shrink:0}.tbn-level{font-size:12px;font-weight:600;color:#374151;letter-spacing:0.5px}
.page-scroll{flex:1;overflow-y:auto;padding:24px 28px;display:flex;flex-direction:column;gap:20px}

.hero-card{display:flex;gap:20px;align-items:flex-start;padding:22px 28px;border-radius:16px;background:linear-gradient(135deg,rgba(59,130,246,0.05),rgba(99,102,241,0.03));border:1px solid rgba(59,130,246,0.12)}
.hc-num{font-size:60px;font-weight:900;color:rgba(59,130,246,0.08);line-height:1;flex-shrink:0;font-family:'Inter',sans-serif}.hero-card h2{margin:0 0 6px;font-size:24px;font-weight:700;color:#111827}.hero-card p{margin:0;font-size:15px;color:#6b7280;line-height:1.6}strong{color:#111827}

.clean-card{background:#fff;border-radius:16px;border:1px solid #e5e7eb;padding:20px 24px;box-shadow:0 1px 3px rgba(0,0,0,0.04);transition:all .3s}
.slider-bar{display:flex;align-items:center;gap:16px;padding:14px 24px}.slider-label{font-size:14px;font-weight:600;color:#374151;white-space:nowrap}.modern-slider{-webkit-appearance:none;flex:1;height:8px;background:#e5e7eb;border-radius:4px;outline:none}.modern-slider::-webkit-slider-thumb{-webkit-appearance:none;width:22px;height:22px;background:#3B82F6;border-radius:50%;cursor:pointer;box-shadow:0 2px 8px rgba(59,130,246,0.3)}.preset-group{display:flex;gap:6px}.preset-group button{padding:6px 14px;border-radius:14px;border:1px solid #e5e7eb;background:#fff;font-size:11px;font-weight:500;cursor:pointer}.preset-group button.on{background:#3B82F6;color:#fff;border-color:#3B82F6}

.kpi-row{display:grid;grid-template-columns:repeat(4,1fr);gap:14px}
.kpi{padding:18px 12px;text-align:center;border-radius:14px;background:#fff;border:1px solid #e5e7eb}.kpi span{display:block;font-size:11px;color:#9ca3af;text-transform:uppercase;letter-spacing:0.5px;margin-bottom:4px}.kpi b{display:block;font-size:28px;font-weight:900}.kpi.green b{color:#10B981}.kpi.red b{color:#EF4444}.kpi.blue b{color:#3B82F6}.kpi.purple b{color:#8B5CF6}.kpi.emerald b{color:#059669}

.three-col{display:grid;grid-template-columns:0.9fr 2.4fr 1fr;gap:20px;flex:1;min-height:0}
.three-col>.clean-card{padding:16px 20px;overflow-y:auto}

.canvas-card h3{margin:0 0 10px;font-size:14px;font-weight:600;color:#374151}
.canvas-wrap{position:relative;width:100%;height:420px;border-radius:12px;overflow:hidden;background:#f9fafb;border:1px solid #e5e7eb;cursor:crosshair}
.canvas-wrap canvas{display:block;width:100%;height:100%}

.dyn-box{position:absolute;border:2.5px dashed rgba(239,68,68,0.5);border-radius:4px;pointer-events:auto;cursor:pointer;transition:all .2s;z-index:5}.dyn-box.highlight{border-color:rgba(16,185,129,0.9);border-style:solid;border-width:3px;box-shadow:0 0 16px rgba(16,185,129,0.4);z-index:10}.dyn-box.edited{border-color:rgba(16,185,129,0.8);border-style:solid;background:rgba(16,185,129,0.04)}
.dyn-label{position:absolute;top:-22px;left:2px;font-size:9px;font-weight:600;color:#111827;background:rgba(255,255,255,0.9);padding:2px 8px;border-radius:4px;white-space:nowrap;pointer-events:none}.dyn-score{position:absolute;bottom:3px;right:3px;font-size:9px;color:#fff;background:rgba(0,0,0,0.55);padding:1px 5px;border-radius:4px;pointer-events:none}.dyn-box.highlight .dyn-score{background:rgba(16,185,129,0.85)}

.crosshair{position:absolute;pointer-events:none;z-index:20}.ch-text{position:absolute;top:14px;left:14px;font-size:10px;background:rgba(0,0,0,0.75);color:#fff;padding:4px 10px;border-radius:6px;white-space:nowrap}

.text-card h3{margin:0 0 10px;font-size:14px;font-weight:600;color:#374151}.text-card h4{margin:12px 0 6px;font-size:13px;font-weight:600;color:#374151}
blockquote{margin:0 0 14px;padding:16px;border-radius:10px;font-size:14px;line-height:1.75;font-style:italic}
.q-red{border-left:4px solid #EF4444;background:rgba(239,68,68,0.03);color:#374151}.q-neutral{border-left:4px solid #d1d5db;background:rgba(0,0,0,0.015);color:#6b7280}

.nlp-grid{display:flex;flex-direction:column;gap:6px;margin-bottom:10px}.nlp-item{display:flex;justify-content:space-between;padding:6px 10px;border-radius:6px;background:#f9fafb;font-size:13px}.nlp-item span{color:#9ca3af}.nlp-item strong{color:#374151}
.t-red{color:#EF4444!important}.t-green{color:#10B981!important}

.photo-strip{display:flex;gap:6px;flex-wrap:wrap}.photo-strip img{width:60px;height:60px;border-radius:10px;object-fit:cover;border:2px solid #e5e7eb;transition:all .2s;cursor:pointer}.photo-strip img:hover{transform:scale(1.2);border-color:#10B981;box-shadow:0 4px 14px rgba(0,0,0,0.12);z-index:10}
</style>
