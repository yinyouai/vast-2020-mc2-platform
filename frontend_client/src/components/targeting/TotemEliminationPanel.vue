<template>
  <div class="glass-card panel-root">
    <h4 class="舱室标题">⚙️ 大众普及物资反向排除漏斗控制台</h4>
    <p class="panel-desc">勾选放逐会场免费分发物资，强行逼迫核心黑客组织接头暗号图腾在流向图中显现</p>
    <div class="checkbox-flow">
      <label
        v-for="item in filterItems"
        :key="item.id"
        class="filter-checkbox"
        :class="{ checked: store.excludedItems.includes(item.id) }"
      >
        <input
          type="checkbox"
          :value="item.id"
          :checked="store.excludedItems.includes(item.id)"
          @change="handleToggle(item.id)"
        />
        <span class="check-indicator">
          <span class="check-mark" v-if="store.excludedItems.includes(item.id)">✕</span>
        </span>
        <span class="label-txt">
          {{ item.cnName }}
          <span class="coverage">覆盖率 {{ item.coverage }}%</span>
        </span>
      </label>
    </div>
    <div class="panel-status">
      已排除 <strong>{{ store.excludedItems.length }}</strong> / {{ filterItems.length }} 项 —
      <span v-if="store.excludedItems.length >= 3" class="text-accent">去噪纯度已达标 ✓</span>
      <span v-else class="text-danger">请继续放逐普及物资</span>
    </div>
  </div>
</template>

<script setup>
import { useDashboardStore } from '../../store/dashboard'
import { EXCLUDABLE_ITEMS } from '../../constants/forensics'

const store = useDashboardStore()

// use centralized constants
const filterItems = EXCLUDABLE_ITEMS

const handleToggle = (id) => {
  const currentExcludes = [...store.excludedItems]
  const idx = currentExcludes.indexOf(id)
  if (idx > -1) {
    currentExcludes.splice(idx, 1)
  } else {
    currentExcludes.push(id)
  }
  store.excludedItems = currentExcludes
  store.fetchHeatmapMatrix()
}
</script>

<style scoped>
.panel-root { padding: var(--space-md) var(--space-lg); }
.panel-desc { margin: 0 0 var(--space-md); font-size: var(--text-xs); color: var(--text-tertiary); }

.checkbox-flow {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-sm);
  margin-bottom: var(--space-md);
}

.filter-checkbox {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  padding: var(--space-sm) var(--space-md);
  border-radius: var(--radius-full);
  border: 1px solid rgba(0, 0, 0, 0.08);
  cursor: pointer;
  font-size: var(--text-xs);
  color: var(--text-secondary);
  transition: all 0.3s var(--ease-out-expo);
  user-select: none;
  background: rgba(255,255,255,0.5);
}

.filter-checkbox input { display: none; }

.check-indicator {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 2px solid rgba(0,0,0,0.15);
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s var(--ease-out-expo);
  flex-shrink: 0;
}

.check-mark {
  font-size: 11px;
  font-weight: var(--weight-bold);
  color: #fff;
}

.filter-checkbox:hover {
  border-color: rgba(0,0,0,0.15);
  background: rgba(0,0,0,0.02);
}

.filter-checkbox.checked {
  background: rgba(255, 90, 95, 0.06);
  border-color: rgba(255, 90, 95, 0.3);
  color: var(--accent-danger);
}

.filter-checkbox.checked .check-indicator {
  background: var(--accent-danger);
  border-color: var(--accent-danger);
}

.coverage {
  font-size: 10px;
  opacity: 0.6;
  font-family: var(--font-mono);
  margin-left: 2px;
}

.panel-status {
  font-size: var(--text-xs);
  color: var(--text-secondary);
  padding: var(--space-sm) var(--space-md);
  background: rgba(0,0,0,0.02);
  border-radius: var(--radius-sm);
}

.panel-status strong {
  color: var(--text-primary);
}
</style>
