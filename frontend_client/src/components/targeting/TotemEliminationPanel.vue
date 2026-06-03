<template>
  <div class="apple-glass-card panel-root">
    <h4 class="舱室标题">⚙️ 组件 10 : 大众参会普及物资/泛滥礼品反向排除漏斗控制台</h4>
    <div class="checkbox-row-flow">
      <label v-for="item in filterItems" :key="item.id"
             class="neon-checkbox-label"
             :class="{ 'is-checked': store.excludedItems.includes(item.id) }">
        <input type="checkbox"
               :value="item.id"
               :checked="store.excludedItems.includes(item.id)"
               @change="handleToggle(item.id)">
        <span class="custom-indicator"></span>
        <span class="label-txt">{{ item.cnName }} <span class="coverage-txt">(社会覆盖率: {{ item.coverage }}%)</span></span>
      </label>
    </div>
  </div>
</template>

<script setup>
import { useDashboardStore } from '../../store/dashboard'
const store = useDashboardStore()

// 💡 彻底消灭乱码！将英文键映射为无懈可击的中文判定
const filterItems = [
  { id: 'lavenderDie', cnName: '🔮 薰衣草散装骰子', coverage: 60 },
  { id: 'sign', cnName: '🚩 现场标志性标牌', coverage: 60 },
  { id: 'hairClip', cnName: '发夹普及物资', coverage: 47 },
  { id: 'redWhistle', cnName: '📢 会场泛滥红哨子', coverage: 45 }
]

const handleToggle = (id) => {
  const currentExcludes = [...store.excludedItems]
  const idx = currentExcludes.indexOf(id)
  if (idx > -1) {
    currentExcludes.splice(idx, 1)
  } else {
    currentExcludes.push(id)
  }
  // 强力驱动 Pinia 状态管理层
  store.excludedItems = currentExcludes
  store.fetchHeatmapMatrix() // 动态通知后端重排引擎更新
}
</script>

<style scoped>
.panel-root { padding: 14px 18px; }
.checkbox-row-flow { display: flex; flex-wrap: wrap; gap: 16px; margin-top: 10px; }

/* Apple 风格高灵敏复选胶囊样式 */
.neon-checkbox-label {
  display: flex; align-items: center; gap: 8px; background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.05); padding: 8px 14px; border-radius: 20px;
  cursor: pointer; font-size: 11.5px; color: #8E8E93; transition: all 0.3s cubic-bezier(0.25, 1, 0.5, 1);
  user-select: none;
}
.neon-checkbox-label input { display: none; }
.custom-indicator {
  width: 6px; height: 6px; border-radius: 50%; background: rgba(255,255,255,0.15);
  transition: all 0.3s; display: inline-block;
}

/* 激活态时产生利落的荧光红削波警示色 */
.neon-checkbox-label.is-checked {
  background: rgba(255, 90, 95, 0.05); border-color: rgba(255, 90, 95, 0.25); color: #FF5A5F;
  box-shadow: 0 4px 12px rgba(255, 90, 95, 0.05);
  .custom-indicator { background: #FF5A5F; box-shadow: 0 0 8px #FF5A5F; }
}
.neon-checkbox-label:hover {
  background: rgba(255,255,255,0.04); border-color: rgba(255,255,255,0.1);
}
.coverage-txt { font-size: 10px; opacity: 0.7; font-family: monospace; }
</style>