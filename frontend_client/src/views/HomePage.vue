<template>
  <div class="home-root">
    <!-- 气泡层: 纯CSS动画 -->
    <div class="bubble-layer">
      <div
        v-for="b in bubbles"
        :key="b.id"
        class="bubble"
        :class="{ popping: b.popping }"
        :style="b.style"
        @click.stop="popBubble(b)"
      ></div>
    </div>

    <!-- 照片漂浮层: 纯CSS动画，无JS拖动 -->
    <div class="photos-layer">
      <div
        v-for="p in photos"
        :key="p.id"
        class="float-photo"
        :class="{ hacker: hackerSet.has(p.id) }"
        :style="p.style"
      >
        <img :src="p.url" :alt="p.id" draggable="false" @error="onImgErr" />
        <span class="fp-label">{{ p.id.replace('Person','P') }}</span>
        <span v-if="hackerSet.has(p.id)" class="fp-badge">⚠</span>
      </div>
    </div>

    <!-- 中心卡片 -->
    <div class="hero-center">
      <div class="hero-glass">
        <div class="hero-badge">🔍 IEEE VAST 2020 · Mini-Challenge 2</div>
        <h1 class="hero-title">数字取证<span class="hl">可视化分析</span>平台</h1>
        <p class="hero-desc">基于多模态全景数据，通过人在回路交互式可视分析，从 <strong>40</strong> 名参会者中精准锁定 <strong>8 人</strong> 秘密黑客组织。</p>
        <div class="task-cards">
          <div v-for="t in tasks" :key="t.id" class="task-entry" :style="{'--tc':t.color}" @click="$router.push(t.path)">
            <span class="te-num">{{t.num}}</span><div class="te-info"><strong>{{t.title}}</strong><span>{{t.sub}}</span></div>
            <div class="te-arrow"><svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg></div>
          </div>
        </div>
        <div class="hero-stats"><div class="hs"><b>40</b><span>嫌疑人</span></div><div class="hs"><b>7</b><span>物资品类</span></div><div class="hs"><b>5</b><span>分析层级</span></div><div class="hs accent"><b>8</b><span>确认为黑客</span></div></div>
      </div>
    </div>

    <!-- 静态光点粒子: 纯CSS -->
    <div class="sparkle-layer">
      <div v-for="n in 30" :key="'s'+n" class="sparkle" :style="sparkleStyle(n)"></div>
    </div>
  </div>
</template>

<script setup>
import { reactive, onBeforeUnmount } from 'vue'
import { HACKER_LIST } from '../constants/forensics'

const hackerSet = new Set(HACKER_LIST)

/* 气泡: 25个，所有动画用CSS keyframes驱动（GPU加速），零JS reflow */
const BUBBLE_COUNT = 25
const bubbles = reactive(
  Array.from({ length: BUBBLE_COUNT }, () => {
    const id = Math.random().toString(36).slice(2)
    const size = 20 + Math.random() * 140
    const dur = 18 + Math.random() * 30
    const delay = Math.random() * -30
    return {
      id, popping: false,
      style: {
        left: (Math.random() * 100) + '%',
        top: (Math.random() * 100) + '%',
        width: size + 'px', height: size + 'px',
        opacity: 0.04 + Math.random() * 0.07,
        '--drift-x': ((Math.random() - 0.5) * 300) + 'px',
        '--drift-y': ((Math.random() - 0.5) * 200) + 'px',
        '--bubble-dur': dur + 's',
        animationDelay: delay + 's'
      }
    }
  })
)
function popBubble(b) {
  b.popping = true
  setTimeout(() => {
    const idx = bubbles.findIndex(x => x.id === b.id)
    if (idx >= 0) {
      const s = 20 + Math.random() * 140
      const dur = 18 + Math.random() * 30
      bubbles.splice(idx, 1, {
        id: Math.random().toString(36).slice(2), popping: false,
        style: {
          left: (Math.random() * 100) + '%', top: (Math.random() * 100) + '%',
          width: s + 'px', height: s + 'px',
          opacity: 0.04 + Math.random() * 0.07,
          '--drift-x': ((Math.random() - 0.5) * 300) + 'px',
          '--drift-y': ((Math.random() - 0.5) * 200) + 'px',
          '--bubble-dur': dur + 's',
          animationDelay: '0s'
        }
      })
    }
  }, 500)
}

/* 照片: 40张，纯CSS漂浮 */
const photos = reactive(
  Array.from({ length: 40 }, (_, i) => {
    const id = 'Person' + (i + 1)
    const isH = hackerSet.has(id)
    const size = isH ? 70 + Math.random() * 45 : 38 + Math.random() * 50
    const dur = 22 + Math.random() * 35
    return {
      id,
      url: `http://localhost:5000/static/MC2-Image-Data/${id}/${id}_1.jpg`,
      style: {
        left: (2 + Math.random() * 93) + '%',
        top: (2 + Math.random() * 93) + '%',
        width: size + 'px', height: size + 'px',
        zIndex: isH ? 10 : 1 + Math.floor(Math.random() * 5),
        '--drift-x': ((Math.random() - 0.5) * 180) + 'px',
        '--drift-y': ((Math.random() - 0.5) * 140) + 'px',
        '--photo-dur': dur + 's',
        animationDelay: (Math.random() * -dur) + 's'
      }
    }
  })
)
function onImgErr(e) { e.target.style.display = 'none' }

/* 光点粒子 */
function sparkleStyle(n) {
  const x = (n * 17 + 3) % 100, y = (n * 13 + 7) % 100
  const dur = 3 + (n % 5)
  return { left: x + '%', top: y + '%', animationDuration: dur + 's', animationDelay: (n * 0.3) + 's' }
}

const tasks = [
  { id: 1, num: '01', title: '算法模型不确定性审计', sub: 'YOLO v2 鲁棒性评估 · 假阳性噪声动态消融', color: '#31C27C', path: '/task1_auditing' },
  { id: 2, num: '02', title: '多模态语义真值校准', sub: '人在回路 · 图文交叉比对 · 机器纠偏', color: '#007AFF', path: '/task2_correction' },
  { id: 3, num: '03', title: '嫌疑社群特征聚类', sub: 'Ward 层次聚类 · 人-物矩阵双向重排', color: '#FF9F0A', path: '/task3_clustering' },
  { id: 4, num: '04', title: '秘密图腾反向排除', sub: '噪声削波 · 力导向网络图 · 桑基流向', color: '#BF5AF2', path: '/task4_totem' },
  { id: 5, num: '05', title: '黑客组织终极定案', sub: '社交网络隔离审计 · 全案证据收网', color: '#FF5A5F', path: '/task5_verdict' }
]
</script>

<style scoped>
.home-root {
  width: 100vw; height: 100vh; position: relative; overflow: hidden;
  background: linear-gradient(135deg, #c8f0d8 0%, #dce8ff 28%, #f0e6ff 52%, #fde4ec 76%, #c8f0d8 100%);
  user-select: none;
}

/* ═══ 气泡 (纯CSS动画，GPU加速) ═══ */
.bubble-layer { position: absolute; inset: 0; z-index: 1; pointer-events: none; }
.bubble {
  position: absolute; border-radius: 50%;
  background: radial-gradient(circle at 30% 30%, rgba(255,255,255,0.5), rgba(49,194,124,0.07) 50%, transparent 85%);
  transform: translate(-50%, -50%);
  pointer-events: auto; cursor: pointer;
  transition: transform 0.5s ease-out, opacity 0.5s ease-out;
  will-change: transform;
  animation: bubble-float var(--bubble-dur, 25s) ease-in-out infinite;
}
.bubble:hover { transform: translate(-50%, -50%) scale(1.2); }
.bubble.popping { transform: translate(-50%, -50%) scale(3); opacity: 0 !important; }

@keyframes bubble-float {
  0%, 100% { transform: translate(-50%, -50%) translate(0, 0) scale(1); }
  25%  { transform: translate(-50%, -50%) translate(calc(var(--drift-x)*0.6), calc(var(--drift-y)*0.8)) scale(1.1); }
  50%  { transform: translate(-50%, -50%) translate(calc(var(--drift-x)*0.9), calc(var(--drift-y)*0.3)) scale(0.9); }
  75%  { transform: translate(-50%, -50%) translate(calc(var(--drift-x)*0.4), calc(var(--drift-y)*0.7)) scale(1.05); }
}

/* ═══ 照片 (纯CSS动画，GPU加速) ═══ */
.photos-layer { position: absolute; inset: 0; z-index: 2; pointer-events: none; }
.float-photo {
  position: absolute; border-radius: 10px; overflow: hidden;
  transform: translate(-50%, -50%);
  border: 2px solid rgba(255,255,255,0.7);
  box-shadow: 0 4px 20px rgba(0,0,0,0.06);
  cursor: default; pointer-events: auto;
  will-change: transform;
  animation: photo-float var(--photo-dur, 30s) ease-in-out infinite;
  transition: transform 0.3s ease-out, box-shadow 0.3s;
}
.float-photo:hover {
  transform: translate(-50%, -50%) scale(1.35) !important;
  z-index: 300 !important;
  border-color: #31C27C;
  box-shadow: 0 10px 30px rgba(0,0,0,0.15);
  transition: transform 0.2s ease-out, box-shadow 0.2s;
}
.float-photo.hacker {
  border-color: rgba(191,90,242,0.5);
  box-shadow: 0 4px 20px rgba(191,90,242,0.12), 0 0 0 3px rgba(191,90,242,0.08);
}
.float-photo img { width: 100%; height: 100%; object-fit: cover; pointer-events: none; }
.fp-label { position: absolute; bottom: 0; left: 0; right: 0; padding: 3px 5px; background: linear-gradient(transparent, rgba(0,0,0,0.6)); color: #fff; font-size: 9px; font-weight: 700; text-align: center; pointer-events: none; }
.fp-badge { position: absolute; top: 3px; right: 3px; font-size: 10px; pointer-events: none; }

@keyframes photo-float {
  0%, 100% { transform: translate(-50%, -50%) translate(0, 0) rotate(0deg); }
  25%  { transform: translate(-50%, -50%) translate(calc(var(--drift-x)*0.5), calc(var(--drift-y)*1.0)) rotate(1deg); }
  50%  { transform: translate(-50%, -50%) translate(calc(var(--drift-x)*1.0), calc(var(--drift-y)*0.3)) rotate(-0.5deg); }
  75%  { transform: translate(-50%, -50%) translate(calc(var(--drift-x)*0.4), calc(var(--drift-y)*0.7)) rotate(0.5deg); }
}

/* ═══ 光点粒子 (纯CSS) ═══ */
.sparkle-layer { position: absolute; inset: 0; z-index: 0; pointer-events: none; }
.sparkle { position: absolute; width: 4px; height: 4px; border-radius: 50%; background: rgba(49,194,124,0.35); animation: sparkle-blink linear infinite; }
@keyframes sparkle-blink { 0%,100%{opacity:0.2;transform:scale(1)} 50%{opacity:0.7;transform:scale(2)} }

/* ═══ 中心卡片 ═══ */
.hero-center { position: relative; z-index: 10; display: flex; align-items: center; justify-content: center; height: 100%; padding: 32px; pointer-events: none; }
.hero-center > * { pointer-events: auto; }
.hero-glass { background: rgba(255,255,255,0.58); backdrop-filter: blur(40px) saturate(200%); -webkit-backdrop-filter: blur(40px) saturate(200%); border-radius: 28px; border: 1px solid rgba(255,255,255,0.7); box-shadow: 0 10px 60px rgba(0,0,0,0.07); padding: 38px 44px 30px; max-width: 640px; width: 100%; text-align: center; }
.hero-badge { display: inline-block; padding: 6px 16px; border-radius: 20px; background: rgba(49,194,124,0.1); color: #1DA85C; font-size: 14px; font-weight: 600; margin-bottom: 16px; }
.hero-title { font-size: 44px; font-weight: 800; color: #1A1A2E; margin: 0 0 10px; line-height: 1.2; }
.hero-title .hl { background: linear-gradient(135deg,#31C27C,#1DB954); -webkit-background-clip:text; -webkit-text-fill-color:transparent; background-clip:text; }
.hero-desc { font-size: 16px; color: #636378; line-height: 1.7; margin: 0 0 26px; } .hero-desc strong { color: #1A1A2E; }
.task-cards { display: flex; flex-direction: column; gap: 8px; margin-bottom: 22px; }
.task-entry { display: flex; align-items: center; gap: 14px; padding: 14px 18px; border-radius: 16px; background: rgba(255,255,255,0.5); border: 1px solid rgba(0,0,0,0.04); cursor: pointer; transition: all 0.35s cubic-bezier(0.16,1,0.3,1); text-align: left; }
.task-entry:hover { background: #fff; border-color: var(--tc); box-shadow: 0 8px 28px rgba(0,0,0,0.07); transform: translateX(6px); }
.te-num { font-size: 32px; font-weight: 900; color: var(--tc); opacity: 0.28; min-width: 42px; text-align: center; } .te-info { flex: 1; } .te-info strong { display: block; font-size: 16px; color: #1A1A2E; font-weight: 600; margin-bottom: 2px; } .te-info span { font-size: 13px; color: #8E8E93; }
.te-arrow { color: #C7C7CC; transition: all 0.3s; } .task-entry:hover .te-arrow { color: var(--tc); transform: translateX(4px); }
.hero-stats { display: flex; justify-content: center; gap: 48px; } .hs { display: flex; flex-direction: column; align-items: center; gap: 3px; } .hs b { font-size: 28px; font-weight: 800; color: #1A1A2E; } .hs span { font-size: 12px; color: #9E9EB0; } .hs.accent b { color: #31C27C; }
</style>
