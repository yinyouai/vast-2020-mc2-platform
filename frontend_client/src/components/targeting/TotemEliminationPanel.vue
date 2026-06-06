<template>
  <section class="panel elimination-panel">
    <div class="panel-header">
      <div><span class="section-kicker">交互过滤器</span><h4 class="panel-title">公共物品剔除</h4><p class="visible-subtitle">同步到覆盖率、评分图、流动图和聚类矩阵。</p></div>
      <b>{{ excludedCount }} / {{ items.length }}</b>
    </div>
    <div class="bulk-actions"><button @click="$emit('auto-exclude')">剔除人数不匹配</button><button @click="$emit('clear')">全部恢复</button></div>
    <div class="filter-list">
      <label v-for="item in items" :key="item.name" :class="['filter-row',item.excluded&&'is-excluded',item.name===selected&&'is-selected']">
        <input type="checkbox" :checked="item.excluded" @change="$emit('toggle',item.name)" />
        <button type="button" class="item-select" @click.prevent="$emit('select',item.name)">
          <span><strong>{{ item.name }}</strong><small>{{ item.ownerCount }} 人 · 最少 {{ item.minOccurrence }} 次</small></span><b>{{ item.score.toFixed(3) }}</b>
        </button>
      </label>
    </div>
    <div class="filter-summary"><span>当前观察</span><strong>{{ selected || '未选择' }}</strong><p>{{ explanation }}</p></div>
  </section>
</template>
<script setup>
import { computed } from 'vue'
const props=defineProps({items:{type:Array,default:()=>[]},selected:{type:String,default:''}})
defineEmits(['toggle','select','auto-exclude','clear'])
const excludedCount=computed(()=>props.items.filter((item)=>item.excluded).length)
const explanation=computed(()=>{const item=props.items.find((entry)=>entry.name===props.selected);if(!item)return'选择一个候选查看其覆盖和稳定性。'
  if(item.excluded)return'该候选已从当前可视分析中隐藏，可随时恢复。'
  return `${item.ownerCount} 位拥有者，稳定率 ${Math.round(item.stability*100)}%，${item.role}。`})
</script>
<style scoped>
.section-kicker{color:var(--subtle);font-size:.7rem;font-weight:800}.visible-subtitle{display:block!important;margin:5px 0 0;color:var(--muted);font-size:.76rem}.panel-header>b{color:var(--accent);font-variant-numeric:tabular-nums}
.bulk-actions{display:grid;grid-template-columns:1fr 1fr;gap:7px;margin-bottom:10px}.bulk-actions button{min-height:38px;border:1px solid var(--border);border-radius:6px;color:var(--text);background:#f8fafc;font-size:.72rem;font-weight:800}
.filter-list{display:grid;gap:6px;max-height:420px;overflow:auto}.filter-row{display:grid;grid-template-columns:22px 1fr;align-items:center;gap:7px;padding:7px;border:1px solid var(--border);border-radius:7px;background:#fff}.filter-row.is-selected{border-color:var(--accent);box-shadow:0 0 0 2px rgba(47,125,246,.1)}.filter-row.is-excluded{opacity:.45;background:#eef1f4}
.filter-row input{width:17px;height:17px;accent-color:var(--accent)}.item-select{display:flex;align-items:center;justify-content:space-between;gap:9px;min-width:0;min-height:42px;padding:0;color:inherit;text-align:left;background:transparent}.item-select span{min-width:0}.item-select strong,.item-select small{display:block}.item-select small{margin-top:3px;color:var(--muted);font-size:.68rem}.item-select>b{color:var(--accent);font-size:.78rem;font-variant-numeric:tabular-nums}
.filter-summary{margin-top:10px;padding:12px;border:1px solid #cfe0f5;border-radius:7px;background:#f3f8ff}.filter-summary span{color:var(--subtle);font-size:.68rem;font-weight:800}.filter-summary strong{display:block;margin:5px 0}.filter-summary p{display:block!important;margin:0;color:var(--muted);font-size:.74rem;line-height:1.5}
</style>
