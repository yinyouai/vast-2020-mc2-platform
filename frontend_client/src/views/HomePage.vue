<template>
  <div class="home-root">
    <!-- Decorative subtle background gradient -->
    <div class="bg-glow"></div>

    <!-- Floating photos as gentle background decoration -->
    <div class="photos-layer">
      <div
        v-for="p in photos"
        :key="p.id"
        class="float-photo"
        :class="{ hacker: hackerSet.has(p.id) }"
        :style="p.style"
      >
        <img :src="p.url" :alt="p.id" draggable="false" @error="onImgErr" />
      </div>
    </div>

    <!-- Main content -->
    <div class="content-center">
      <div class="hero-card">
        <!-- Brand badge -->
        <div class="brand-badge">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>
          IEEE VAST 2020 · Mini-Challenge 2
        </div>

        <!-- Title -->
        <h1 class="hero-title">
          Digital Forensics
          <span class="hl">Visual Analytics</span>
          Platform
        </h1>
        <p class="hero-desc">
          Multi-modal panoramic data investigation with human-in-the-loop interactive visual analytics.
          From <strong>40</strong> conference attendees, precisely identify an
          <strong class="text-accent">8-person</strong> covert hacker cell.
        </p>

        <!-- Stats row -->
        <div class="stats-row">
          <div class="stat-item">
            <span class="stat-num">40</span>
            <span class="stat-label">Suspects</span>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <span class="stat-num">7</span>
            <span class="stat-label">Materials</span>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item">
            <span class="stat-num">5</span>
            <span class="stat-label">Analysis Layers</span>
          </div>
          <div class="stat-divider"></div>
          <div class="stat-item accent">
            <span class="stat-num">8</span>
            <span class="stat-label">Confirmed</span>
          </div>
        </div>

        <!-- Task mission cards -->
        <div class="task-grid">
          <div
            v-for="(t, idx) in tasks"
            :key="t.id"
            class="task-card"
            :class="'task-' + t.id"
            :style="{'--delay': idx * 0.06 + 's'}"
            @click="$router.push(t.path)"
          >
            <div class="tc-icon" :style="{background: t.bg}">
              <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" v-html="t.iconPath"></svg>
            </div>
            <div class="tc-body">
              <div class="tc-num">{{ t.num }}</div>
              <div class="tc-title">{{ t.title }}</div>
              <div class="tc-sub">{{ t.sub }}</div>
            </div>
            <div class="tc-arrow">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { HACKER_LIST } from '../constants/forensics'

const hackerSet = new Set(HACKER_LIST)

const photos = reactive(
  Array.from({ length: 30 }, (_, i) => {
    const idx = (i * 7 % 40) + 1
    const id = 'Person' + idx
    const isH = hackerSet.has(id)
    return {
      id,
      url: `http://localhost:5000/static/MC2-Image-Data/${id}/${id}_1.jpg`,
      style: {
        left: (2 + Math.random() * 94) + '%',
        top: (2 + Math.random() * 94) + '%',
        width: (isH ? 56 : 32 + Math.random() * 24) + 'px',
        height: (isH ? 56 : 32 + Math.random() * 24) + 'px',
        zIndex: isH ? 2 : 1,
        opacity: isH ? 0.15 : 0.06,
        filter: isH ? 'saturate(0.8) hue-rotate(240deg)' : 'none',
        animationDelay: (Math.random() * -30) + 's',
        '--float-dur': (20 + Math.random() * 25) + 's'
      }
    }
  })
)

function onImgErr(e) { e.target.style.display = 'none' }

const tasks = [
  { id: 1, num: '01', title: 'Model Uncertainty Audit', sub: 'YOLO v2 robustness · False positive ablation', color: '#6366F1', bg: 'rgba(99,102,241,0.1)', iconPath: '<circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/>', path: '/task1_auditing' },
  { id: 2, num: '02', title: 'Multi-Modal Ground Truth Calibration', sub: 'Human-in-the-loop · Image-text cross validation', color: '#06B6D4', bg: 'rgba(6,182,212,0.1)', iconPath: '<path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/>', path: '/task2_correction' },
  { id: 3, num: '03', title: 'Community Feature Clustering', sub: 'Ward hierarchical · Person-item matrix reorder', color: '#F59E0B', bg: 'rgba(245,158,11,0.1)', iconPath: '<rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/>', path: '/task3_clustering' },
  { id: 4, num: '04', title: 'Secret Totem Elimination', sub: 'Noise clipping · Force-directed network · Sankey flow', color: '#8B5CF6', bg: 'rgba(139,92,246,0.1)', iconPath: '<polygon points="12 2 22 8.5 22 15.5 12 22 2 15.5 2 8.5 12 2"/><line x1="12" y1="22" x2="12" y2="15.5"/><polyline points="22 8.5 12 15.5 2 8.5"/>', path: '/task4_totem' },
  { id: 5, num: '05', title: 'Hacker Cell Final Verdict', sub: 'Social network isolation · Evidence chain convergence', color: '#EF4444', bg: 'rgba(239,68,68,0.1)', iconPath: '<path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11 14 15 10"/>', path: '/task5_verdict' }
]
</script>

<style scoped>
.home-root {
  width: 100vw;
  height: 100vh;
  position: relative;
  overflow: hidden;
  background: var(--bg-primary);
  user-select: none;
}

/* Decorative background */
.bg-glow {
  position: absolute;
  top: -30%;
  left: -10%;
  width: 80%;
  height: 80%;
  background: radial-gradient(ellipse at center, rgba(99, 102, 241, 0.03) 0%, transparent 70%);
  pointer-events: none;
  z-index: 0;
}

/* Photos layer — gentle decoration */
.photos-layer {
  position: absolute;
  inset: 0;
  z-index: 1;
  pointer-events: none;
  overflow: hidden;
}
.float-photo {
  position: absolute;
  border-radius: 8px;
  overflow: hidden;
  transform: translate(-50%, -50%);
  border: 1px solid rgba(0, 0, 0, 0.03);
  opacity: 0.08;
  will-change: transform;
  animation: gentle-float var(--float-dur, 30s) ease-in-out infinite;
  transition: opacity 0.3s;
}
.float-photo.hacker {
  border-color: rgba(139, 92, 246, 0.08);
  z-index: 2;
}
.float-photo img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

@keyframes gentle-float {
  0%, 100% { transform: translate(-50%, -50%) translate(0, 0); }
  33% { transform: translate(-50%, -50%) translate(calc(var(--drift-x, 30px) * 0.6), calc(var(--drift-y, 20px) * -0.8)); }
  66% { transform: translate(-50%, -50%) translate(calc(var(--drift-x, 30px) * -0.4), calc(var(--drift-y, 20px) * 0.6)); }
}

/* ═══ Center Content ═══ */
.content-center {
  position: relative;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  padding: 32px;
  pointer-events: none;
}
.content-center > * { pointer-events: auto; }

/* ═══ Hero Card ═══ */
.hero-card {
  background: var(--bg-card);
  backdrop-filter: blur(30px) saturate(200%);
  -webkit-backdrop-filter: blur(30px) saturate(200%);
  border-radius: 24px;
  border: 1px solid rgba(255, 255, 255, 0.8);
  box-shadow: 0 8px 40px rgba(0, 0, 0, 0.04), 0 0 1px rgba(0, 0, 0, 0.06);
  padding: 40px 48px 36px;
  max-width: 680px;
  width: 100%;
  text-align: center;
}

/* Brand badge */
.brand-badge {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 6px 16px;
  border-radius: 20px;
  background: var(--accent-primary-subtle);
  color: var(--accent-primary);
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 20px;
  letter-spacing: 0.2px;
}

/* Title */
.hero-title {
  font-size: 40px;
  font-weight: 800;
  color: var(--text-primary);
  margin: 0 0 12px;
  line-height: 1.15;
  letter-spacing: -0.5px;
}
.hero-title .hl {
  background: linear-gradient(135deg, #6366F1, #8B5CF6, #06B6D4);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.hero-desc {
  font-size: 16px;
  color: var(--text-secondary);
  line-height: 1.7;
  margin: 0 0 28px;
  max-width: 540px;
  margin-left: auto;
  margin-right: auto;
}
.hero-desc strong { color: var(--text-primary); font-weight: 600; }

/* Stats row */
.stats-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0;
  margin-bottom: 28px;
  padding: 16px 24px;
  background: rgba(0, 0, 0, 0.015);
  border-radius: 14px;
  border: 1px solid rgba(0, 0, 0, 0.03);
}
.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 2px;
  padding: 0 24px;
}
.stat-num {
  font-size: 26px;
  font-weight: 800;
  color: var(--text-primary);
  letter-spacing: -0.3px;
}
.stat-label {
  font-size: 11px;
  color: var(--text-tertiary);
  font-weight: 500;
  letter-spacing: 0.3px;
}
.stat-divider {
  width: 1px;
  height: 32px;
  background: rgba(0, 0, 0, 0.06);
}
.stat-item.accent .stat-num {
  color: var(--accent-primary);
}

/* ═══ Task Cards Grid ═══ */
.task-grid {
  display: flex;
  flex-direction: column;
  gap: 8px;
}
.task-card {
  display: flex;
  align-items: center;
  gap: 14px;
  padding: 14px 18px;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.5);
  border: 1px solid rgba(0, 0, 0, 0.03);
  cursor: pointer;
  transition: all 0.3s var(--ease-out);
  text-align: left;
  animation: card-enter 0.5s var(--ease-out) both;
  animation-delay: var(--delay, 0s);
}
.task-card:hover {
  background: #fff;
  border-color: rgba(0, 0, 0, 0.06);
  box-shadow: var(--shadow-card-hover);
  transform: translateX(4px);
}

@keyframes card-enter {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}

.tc-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 40px;
  height: 40px;
  border-radius: 12px;
  flex-shrink: 0;
  color: var(--text-primary);
}
.task-card:hover .tc-icon {
  color: var(--text-primary);
}

.tc-body { flex: 1; }
.tc-num {
  font-size: 11px;
  font-weight: 700;
  color: var(--text-tertiary);
  margin-bottom: 2px;
  letter-spacing: 0.5px;
}
.tc-title {
  font-size: 15px;
  font-weight: 600;
  color: var(--text-primary);
  margin-bottom: 1px;
}
.tc-sub {
  font-size: 12px;
  color: var(--text-tertiary);
  line-height: 1.4;
}
.tc-arrow {
  color: #D1D5DB;
  transition: all 0.3s;
}
.task-card:hover .tc-arrow {
  color: var(--accent-primary);
  transform: translateX(3px);
}

/* ═══ Responsive ═══ */
@media (max-width: 640px) {
  .hero-card {
    padding: 28px 20px 24px;
  }
  .hero-title {
    font-size: 28px;
  }
  .hero-desc {
    font-size: 14px;
  }
  .stats-row {
    flex-wrap: wrap;
    gap: 4px;
    padding: 12px 8px;
  }
  .stat-item {
    padding: 0 10px;
  }
  .stat-num {
    font-size: 20px;
  }
}
</style>
