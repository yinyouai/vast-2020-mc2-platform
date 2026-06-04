<template>
  <div class="panel">
    <div class="panel-header">
      <div>
        <h4 class="panel-title">公共物品剔除</h4>
        <p class="panel-subtitle">勾选高覆盖物品，将其从共现基线中移除。</p>
      </div>
    </div>

    <div class="filter-list">
      <label v-for="item in items" :key="item.name" class="filter-row">
        <input
          type="checkbox"
          :checked="store.excludedItems.includes(item.name)"
          @change="store.toggleItemExclusion(item.name)"
        />
        <span>
          <strong>{{ item.name }}</strong>
          <small>{{ item.coverage }} 覆盖率</small>
        </span>
      </label>
    </div>

    <button class="primary-btn full" @click="store.isFourthLayerActive = true">查看候选暗号物证</button>
  </div>
</template>

<script setup>
import { useDashboardStore } from '../../store/dashboard'

const store = useDashboardStore()

const items = [
  { name: 'Notebook', coverage: '60%' },
  { name: 'Badge', coverage: '48%' },
  { name: 'Toy', coverage: '44%' },
  { name: 'Red Hat', coverage: '41%' },
  { name: 'Yellow Bag', coverage: '20%' }
]
</script>

<style scoped>
.filter-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 18px;
}

.filter-row {
  display: grid;
  grid-template-columns: 24px minmax(0, 1fr);
  gap: 10px;
  align-items: center;
  min-height: 56px;
  padding: 10px;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  background: rgba(255, 255, 255, 0.82);
}

.filter-row input {
  width: 20px;
  height: 20px;
  accent-color: var(--accent);
}

.filter-row strong,
.filter-row small {
  display: block;
}

.filter-row small {
  margin-top: 4px;
  color: var(--subtle);
}

.full {
  width: 100%;
}
</style>
