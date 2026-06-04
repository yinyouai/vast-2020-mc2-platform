<template>
  <div class="app-shell">
    <aside class="sidebar" aria-label="任务导航">
      <div class="brand-block">
        <div class="brand-mark">MC2</div>
        <div>
          <p class="eyebrow">VAST Challenge 2020</p>
          <h1>Evidence Console</h1>
        </div>
      </div>

      <nav class="task-nav">
        <router-link
          v-for="item in navItems"
          :key="item.to"
          :to="item.to"
          class="nav-item"
        >
          <span class="nav-index">{{ item.index }}</span>
          <span>
            <strong>{{ item.title }}</strong>
            <small>{{ item.caption }}</small>
          </span>
        </router-link>
      </nav>

      <div class="case-card">
        <p class="eyebrow">当前证据链</p>
        <strong>{{ store.selectedPersonId }}</strong>
        <span :class="['risk-pill', isCoreSuspect ? 'risk-high' : 'risk-low']">
          {{ isCoreSuspect ? '核心嫌疑' : '背景样本' }}
        </span>
      </div>
    </aside>

    <div class="workspace-shell">
      <header class="topbar">
        <div>
          <p class="eyebrow">{{ route.meta.kicker || 'Investigation Layer' }}</p>
          <h2>{{ route.meta.title || 'Evidence Console' }}</h2>
        </div>
        <div class="topbar-actions">
          <span :class="['sync-state', store.isLoading ? 'is-busy' : 'is-ready']">
            {{ store.isLoading ? '同步中' : '数据已就绪' }}
          </span>
          <span class="threshold-chip">阈值 {{ store.scoreThreshold.toFixed(2) }}</span>
        </div>
      </header>

      <main class="viewport-container">
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
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useDashboardStore } from './store/dashboard'

const store = useDashboardStore()
const route = useRoute()

const navItems = [
  { index: '01', to: '/task1_auditing', title: '模型审计', caption: '不确定性与误报' },
  { index: '02', to: '/task2_correction', title: '人工校准', caption: '图文冲突复核' },
  { index: '03', to: '/task3_clustering', title: '群体聚类', caption: '人-物共现结构' },
  { index: '04', to: '/task4_totem', title: '物证过滤', caption: '公共物品剔除' },
  { index: '05', to: '/task5_verdict', title: '最终定案', caption: '社交隔离验证' }
]

const isCoreSuspect = computed(() => store.hackerGroup.includes(store.selectedPersonId))

onMounted(() => {
  store.fetchModelEvaluation()
  store.fetchHeatmapMatrix()
})
</script>
