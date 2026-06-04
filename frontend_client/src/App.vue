<template>
  <div class="app-shell">
    <div class="app-shell__backdrop" aria-hidden="true"></div>

    <aside class="sidebar" aria-label="任务导航">
      <div class="brand-block">
        <div class="brand-mark">
          <span>MC2</span>
        </div>
        <div class="brand-copy">
          <p class="eyebrow">VAST Challenge 2020</p>
          <h1>多模态取证分析平台</h1>
          <p class="brand-description">
            围绕模型误差校正、群体特征收敛与最终嫌疑群体锁定，构建五层递进式可视分析流程。
          </p>
        </div>
      </div>

      <div class="sidebar-section">
        <p class="eyebrow">分析流程</p>
        <nav class="task-nav">
          <router-link
            v-for="item in navItems"
            :key="item.to"
            :to="item.to"
            class="nav-item"
          >
            <span class="nav-index">{{ item.index }}</span>
            <span class="nav-copy">
              <strong>{{ item.title }}</strong>
              <small>{{ item.caption }}</small>
            </span>
            <span :class="['nav-state', route.path === item.to ? 'is-active' : 'is-idle']"></span>
          </router-link>
        </nav>
      </div>

      <div class="sidebar-section story-card">
        <p class="eyebrow">当前叙事</p>
        <h3>{{ route.meta.storyTitle || '证据会在层层筛选后逐步收敛。' }}</h3>
        <p>
          {{ route.meta.storySummary || '结合图像、文本、物证和社交隔离关系，逐步逼近最终嫌疑团体。' }}
        </p>
      </div>

      <div class="case-card">
        <div class="case-card__header">
          <div>
            <p class="eyebrow">当前关注对象</p>
            <strong>{{ store.selectedPersonId }}</strong>
          </div>
          <span :class="['risk-pill', isCoreSuspect ? 'risk-high' : 'risk-low']">
            {{ isCoreSuspect ? '核心嫌疑' : '背景样本' }}
          </span>
        </div>

        <div class="case-card__grid">
          <div>
            <span>分析进度</span>
            <b>第 {{ activeLayer }} 层 / 共 5 层</b>
          </div>
          <div>
            <span>阈值设定</span>
            <b>{{ store.scoreThreshold.toFixed(2) }}</b>
          </div>
          <div>
            <span>已剔除物品</span>
            <b>{{ store.excludedItems.length }}</b>
          </div>
          <div>
            <span>当前暗号焦点</span>
            <b>{{ totemLabel }}</b>
          </div>
        </div>
      </div>
    </aside>

    <div class="workspace-shell">
      <header class="topbar">
        <div class="topbar-copy">
          <p class="eyebrow">{{ route.meta.kicker || '分析层' }}</p>
          <h2>{{ route.meta.title || '多模态取证分析平台' }}</h2>
          <p class="topbar-summary">
            {{ route.meta.summary || '用更清晰的叙事和更稳定的视觉层级，支撑竞赛级别的证据表达。' }}
          </p>
        </div>

        <div class="topbar-actions">
          <span :class="['sync-state', store.isLoading ? 'is-busy' : 'is-ready']">
            {{ store.isLoading ? '正在同步分析数据' : '分析数据已同步' }}
          </span>
          <span class="threshold-chip">置信阈值 {{ store.scoreThreshold.toFixed(2) }}</span>
          <div class="stage-progress" aria-label="分析层进度">
            <span
              v-for="item in navItems"
              :key="item.to"
              :class="['stage-progress__dot', Number(item.index) <= activeLayer ? 'is-past' : 'is-next', route.path === item.to ? 'is-current' : '']"
            ></span>
          </div>
        </div>
      </header>

      <nav class="mobile-nav" aria-label="移动任务导航">
        <router-link
          v-for="item in navItems"
          :key="item.to"
          :to="item.to"
          class="mobile-nav__item"
        >
          <span>{{ item.index }}</span>
          <strong>{{ item.title }}</strong>
        </router-link>
      </nav>

      <main ref="viewportRef" class="viewport-container">
        <router-view v-slot="{ Component, route: viewRoute }">
          <transition name="page-fade" mode="out-in">
            <component :is="Component" :key="viewRoute.path" class="page-layer" />
          </transition>
        </router-view>
      </main>
    </div>
  </div>
</template>

<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useDashboardStore } from './store/dashboard'

const store = useDashboardStore()
const route = useRoute()
const viewportRef = ref(null)
let revealObserver
let mutationObserver
let revealFrame = 0

const navItems = [
  { index: '01', to: '/task1_auditing', title: '模型审计', caption: '识别不确定性与误报来源' },
  { index: '02', to: '/task2_correction', title: '人工复核', caption: '修正图文冲突与错误标签' },
  { index: '03', to: '/task3_clustering', title: '群体聚类', caption: '寻找人-物共现异常结构' },
  { index: '04', to: '/task4_totem', title: '暗号过滤', caption: '排除公共物品并收敛线索' },
  { index: '05', to: '/task5_verdict', title: '最终定案', caption: '结合社交隔离完成判定' }
]

const isCoreSuspect = computed(() => store.hackerGroup.includes(store.selectedPersonId))
const activeLayer = computed(() => Number(route.meta.depth || 1))
const totemLabel = computed(() => {
  const map = {
    yellowBag: '黄色提袋'
  }
  return map[store.activeTotem] || store.activeTotem
})

const revealSelector = [
  '.page-intro',
  '.analysis-card',
  '.panel',
  '.metric-card',
  '.cluster-layout',
  '.totem-layout',
  '.forensics-layout',
  '.workbench-sidebar > *',
  '.sample-dot',
  '.compare-card',
  '.case-card',
  '.network-card'
].join(',')

const prefersReducedMotion = () =>
  window.matchMedia?.('(prefers-reduced-motion: reduce)').matches

const observeRevealTargets = () => {
  const root = viewportRef.value
  if (!root) return

  const nodes = Array.from(root.querySelectorAll(revealSelector))
  nodes.forEach((node, index) => {
    if (node.dataset.revealObserved === 'true') return

    node.dataset.revealObserved = 'true'
    node.classList.add('reveal')
    node.style.setProperty('--reveal-delay', `${Math.min((index % 7) * 72, 432)}ms`)

    if (prefersReducedMotion() || !revealObserver) {
      node.classList.add('is-visible')
      return
    }

    revealObserver.observe(node)
  })
}

const queueRevealObservation = () => {
  window.cancelAnimationFrame(revealFrame)
  revealFrame = window.requestAnimationFrame(observeRevealTargets)
}

const setupRevealObserver = () => {
  const root = viewportRef.value
  if (!root) return

  if (!('IntersectionObserver' in window)) {
    queueRevealObservation()
    return
  }

  revealObserver = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (!entry.isIntersecting) return
        entry.target.classList.add('is-visible')
        revealObserver?.unobserve(entry.target)
      })
    },
    {
      root,
      threshold: 0.16,
      rootMargin: '0px 0px -12% 0px'
    }
  )

  mutationObserver = new MutationObserver(queueRevealObservation)
  mutationObserver.observe(root, { childList: true, subtree: true })
  queueRevealObservation()
}

onMounted(() => {
  store.fetchModelEvaluation()
  store.fetchHeatmapMatrix()
  setupRevealObserver()
})

watch(
  () => route.path,
  () => {
    nextTick(() => {
      viewportRef.value?.scrollTo({
        top: 0,
        behavior: prefersReducedMotion() ? 'auto' : 'smooth'
      })
      window.setTimeout(queueRevealObservation, 260)
    })
  }
)

onBeforeUnmount(() => {
  window.cancelAnimationFrame(revealFrame)
  revealObserver?.disconnect()
  mutationObserver?.disconnect()
})
</script>
