<template>
  <div class="terminal-app-root">
    <header class="cyber-header">
      <div class="header-left">
        <span class="pulse-dot"></span>
        <h1>VAST 2020 MC2 · 现代多模态全景数字取证智能终端</h1>
      </div>
      <nav class="apple-capsule-nav">
        <router-link to="/task1_auditing">🛰️ 层级一: 算法不确定性审计</router-link>
        <router-link to="/task2_correction">🔍 层级二: 多模态真值校准</router-link>
        <router-link to="/task3_clustering">📊 层级三: 嫌疑社群行为特征</router-link>
        <router-link to="/task4_totem">🔮 层级四: 泛滥资产反向排除</router-link>
        <router-link to="/task5_verdict">🛡️ 层级五: 组织暗号终极定案</router-link>
      </nav>
      <div class="header-right">
        <div class="status-badge" :class="{ 'status-active': !store.isLoading }">
          {{ store.isLoading ? '⚙️ 后端动态聚类重算中...' : '🔒 证据链多图互锁同步中' }}
        </div>
      </div>
    </header>

    <main class="viewport-container">
      <router-view v-slot="{ Component, route }">
        <transition :name="transitionName" mode="out-in">
          <component :is="Component" :key="route.path" class="page-layer" />
        </transition>
      </router-view>
    </main>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useDashboardStore } from './store/dashboard'

const store = useDashboardStore()
const route = useRoute()
const transitionName = ref('zoom-dive')

watch(() => route.meta.depth, (toD, fromD) => {
  if (toD && fromD) {
    transitionName.value = toD > fromD ? 'zoom-dive' : 'zoom-rise'
  }
})

onMounted(() => {
  // 💡 修复核心：初始化仅拉取统计模型数据，绝对不能无脑调用 selectPerson() 覆写干扰状态！
  store.fetchModelEvaluation()
  store.fetchHeatmapMatrix()
})
</script>

<style scoped>
.terminal-app-root { display: flex; flex-direction: column; width: 100vw; height: 100vh; background-color: #0A0A0C; }
.cyber-header { height: 64px; display: flex; justify-content: space-between; align-items: center; padding: 0 24px; background: rgba(10, 10, 12, 0.85); backdrop-filter: blur(20px); border-bottom: 1px solid rgba(255, 255, 255, 0.05); z-index: 100; }
.header-left { display: flex; align-items: center; gap: 12px; }
.header-left h1 { margin: 0; font-size: 15px; font-weight: 500; letter-spacing: -0.2px; color: #E5E5EA; }
.pulse-dot { width: 8px; height: 8px; background: #30D158; border-radius: 50%; box-shadow: 0 0 8px #30D158; }
.apple-capsule-nav { display: flex; background: rgba(255, 255, 255, 0.04); padding: 4px; border-radius: 32px; border: 1px solid rgba(255, 255, 255, 0.02); }
.apple-capsule-nav a { text-decoration: none; color: #8E8E93; padding: 6px 14px; font-size: 12px; font-weight: 500; border-radius: 24px; transition: all 0.4s cubic-bezier(0.25, 1, 0.5, 1); }
.apple-capsule-nav a.router-link-active { background: rgba(255, 255, 255, 0.1); color: #FFFFFF; backdrop-filter: blur(5px); box-shadow: 0 4px 12px rgba(0, 0, 0, 0.3); }
.status-badge { font-size: 12px; color: #8E8E93; background: rgba(255,255,255,0.02); padding: 6px 12px; border-radius: 20px; border: 1px solid rgba(255,255,255,0.03); }
.status-active { color: #30D158; }
.viewport-container { flex: 1; position: relative; overflow: hidden; background: #000; }
.page-layer { position: absolute; width: 100%; height: 100%; box-sizing: border-box; }
.zoom-dive-enter-active, .zoom-dive-leave-active, .zoom-rise-enter-active, .zoom-rise-leave-active { transition: all 0.6s cubic-bezier(0.25, 1, 0.5, 1); }
.zoom-dive-leave-to { transform: scale(0.85); opacity: 0; filter: blur(12px); }
.zoom-dive-enter-from { transform: scale(1.15); opacity: 0; filter: blur(6px); }
.zoom-rise-leave-to { transform: scale(1.15); opacity: 0; filter: blur(12px); }
.zoom-rise-enter-from { transform: scale(0.85); opacity: 0; filter: blur(6px); }
</style>