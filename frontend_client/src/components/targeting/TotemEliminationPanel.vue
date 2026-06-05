<template>
  <div class="panel elimination-panel">
    <div class="panel-header">
      <div>
        <h4 class="panel-title">公共物品剔除</h4>
        <p class="panel-subtitle">勾选覆盖率过高的物品，实时观察暗号物证是否仍然收敛。</p>
      </div>
    </div>

    <div class="filter-list">
      <label v-for="item in items" :key="item.name" class="filter-row" :class="{ 'is-excluded': item.excluded }">
        <input
          type="checkbox"
          :checked="item.excluded"
          @change="$emit('toggle', item.name)"
        />
        <span>
          <strong>{{ item.name }}</strong>
          <small>{{ item.coverage }}% 覆盖率</small>
        </span>
        <b>{{ item.excluded ? '已剔除' : item.role }}</b>
      </label>
    </div>

    <div class="live-explain">
      <span>实时解释</span>
      <strong>{{ explanation.title }}</strong>
      <p>{{ explanation.detail }}</p>
    </div>

    <button class="primary-btn full" @click="$emit('open-evidence')">查看候选暗号物证</button>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  items: {
    type: Array,
    default: () => []
  }
})

defineEmits(['toggle', 'open-evidence'])

const explanation = computed(() => {
  const excluded = props.items.filter((item) => item.excluded)
  const candidate = props.items.find((item) => item.role === '候选暗号')

  if (!excluded.length) {
    return {
      title: '尚未剔除公共噪声',
      detail: 'Notebook、Badge 等高覆盖物仍在网络里，会把普通参会者和核心嫌疑组混在一起。'
    }
  }

  return {
    title: `已剔除 ${excluded.length} 个公共物品`,
    detail: `${excluded.map((item) => item.name).join('、')} 被移出背景流后，${candidate?.name || '候选物证'} 的低覆盖但高收敛特征会更明显。`
  }
})
</script>

<style scoped>
.elimination-panel {
  align-self: start;
}

.filter-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 14px;
}

.filter-row {
  display: grid;
  grid-template-columns: 24px minmax(0, 1fr) auto;
  gap: 10px;
  align-items: center;
  min-height: 58px;
  padding: 10px;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  background: rgba(255, 255, 255, 0.82);
  transition:
    border-color var(--motion-fast) ease,
    background var(--motion-fast) ease,
    transform var(--motion-fast) var(--ease-spring);
}

.filter-row:hover {
  transform: translateY(-2px);
  border-color: rgba(47, 125, 246, 0.2);
}

.filter-row.is-excluded {
  background: rgba(232, 238, 246, 0.78);
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

.filter-row b {
  color: var(--subtle);
  font-size: 0.76rem;
}

.live-explain {
  margin-bottom: 14px;
  padding: 14px;
  border: 1px solid rgba(47, 125, 246, 0.16);
  border-radius: var(--radius-sm);
  background:
    radial-gradient(circle at top right, rgba(47, 125, 246, 0.1), transparent 28%),
    rgba(247, 250, 255, 0.88);
}

.live-explain span {
  display: block;
  color: var(--subtle);
  font-size: 0.76rem;
  font-weight: 900;
  letter-spacing: 0.08em;
}

.live-explain strong {
  display: block;
  margin-top: 6px;
}

.live-explain p {
  display: block !important;
  margin: 8px 0 0;
  color: var(--muted);
  line-height: 1.6;
}

.full {
  width: 100%;
}
</style>
