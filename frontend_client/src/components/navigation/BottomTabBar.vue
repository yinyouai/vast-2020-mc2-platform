<template>
  <nav class="bottom-tab-bar">
    <router-link
      v-for="item in tabItems"
      :key="item.path"
      :to="item.path"
      class="tab-item"
      :class="{ active: isActive(item.path) }"
    >
      <span class="tab-icon" v-html="item.icon"></span>
      <span class="tab-label">{{ item.shortTitle }}</span>
      <span v-if="item.badge" class="tab-badge">{{ item.badge }}</span>
    </router-link>
  </nav>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'

const route = useRoute()

const tabItems = [
  {
    path: '/task1_auditing',
    shortTitle: '模型审计',
    icon: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><circle cx="12" cy="12" r="6"/><circle cx="12" cy="12" r="2"/></svg>`,
    depth: 1
  },
  {
    path: '/task2_correction',
    shortTitle: '真值校准',
    icon: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4L16.5 3.5z"/></svg>`,
    depth: 2
  },
  {
    path: '/task3_clustering',
    shortTitle: '社群聚类',
    icon: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="3" width="7" height="7" rx="1"/><rect x="14" y="3" width="7" height="7" rx="1"/><rect x="3" y="14" width="7" height="7" rx="1"/><rect x="14" y="14" width="7" height="7" rx="1"/></svg>`,
    depth: 3
  },
  {
    path: '/task4_totem',
    shortTitle: '图腾排除',
    icon: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><polygon points="12 2 22 8.5 22 15.5 12 22 2 15.5 2 8.5 12 2"/><line x1="12" y1="22" x2="12" y2="15.5"/><polyline points="22 8.5 12 15.5 2 8.5"/></svg>`,
    depth: 4
  },
  {
    path: '/task5_verdict',
    shortTitle: '终审定案',
    icon: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/><polyline points="9 12 11 14 15 10"/></svg>`,
    depth: 5
  }
]

function isActive(path) {
  return route.path === path
}
</script>

<style scoped>
.bottom-tab-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  height: var(--bottom-bar-height, 64px);
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 0;
  background: rgba(255, 255, 255, 0.85);
  backdrop-filter: blur(30px) saturate(180%);
  -webkit-backdrop-filter: blur(30px) saturate(180%);
  border-top: 1px solid rgba(0, 0, 0, 0.06);
  z-index: 200;
  padding: 4px 16px env(safe-area-inset-bottom);
}

.tab-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 3px;
  flex: 1;
  max-width: 80px;
  padding: 6px 4px;
  border-radius: var(--radius-sm);
  color: var(--text-tertiary);
  text-decoration: none;
  transition: all 0.3s var(--ease-out-expo);
  position: relative;
  cursor: pointer;
  -webkit-tap-highlight-color: transparent;
  user-select: none;
}

.tab-item:hover {
  color: var(--text-secondary);
}

.tab-item.active {
  color: var(--accent-primary);
}

.tab-item.active::before {
  content: '';
  position: absolute;
  top: 0;
  left: 50%;
  transform: translateX(-50%);
  width: 20px;
  height: 3px;
  background: var(--accent-primary);
  border-radius: 0 0 3px 3px;
}

.tab-icon {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 28px;
  height: 28px;
  transition: transform 0.3s var(--ease-spring);
}

.tab-item.active .tab-icon {
  transform: scale(1.12);
}

.tab-label {
  font-size: 10px;
  font-weight: var(--weight-medium);
  letter-spacing: 0.1px;
  white-space: nowrap;
}

.tab-badge {
  position: absolute;
  top: 2px;
  right: calc(50% - 20px);
  min-width: 16px;
  height: 16px;
  padding: 0 4px;
  background: var(--accent-danger);
  color: #fff;
  font-size: 9px;
  font-weight: var(--weight-bold);
  border-radius: var(--radius-full);
  display: flex;
  align-items: center;
  justify-content: center;
  line-height: 1;
}
</style>
