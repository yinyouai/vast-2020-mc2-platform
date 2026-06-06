<template>
  <section class="triage-board">
    <article v-for="lane in lanes" :key="lane.key" :class="['review-lane', `lane-${lane.key}`]">
      <header>
        <div><span>{{ lane.eyebrow }}</span><h4>{{ lane.title }}</h4></div>
        <b>{{ lane.items.length }}</b>
      </header>
      <p>{{ lane.description }}</p>
      <div class="lane-list">
        <div v-for="item in lane.items" :key="item.id" :class="['review-card', activeId === item.id && 'is-active']">
          <button class="card-main" type="button" @click="$emit('select', item.id)">
            <span class="person-avatar">{{ personNumber(item.person_id) }}</span>
            <span class="card-copy">
              <strong>{{ item.person_id }}</strong>
              <small>{{ item.image_id }}</small>
              <em>{{ item.predicted_label }} → {{ item.corrected_label }}</em>
            </span>
            <span class="score">{{ item.score ? item.score.toFixed(3) : '—' }}</span>
          </button>
          <div class="card-actions">
            <button type="button" @click="$emit('select', item.id)">查看证据</button>
            <button v-if="lane.key === 'confirmed'" type="button" class="danger"
              :disabled="busyId === item.id" @click="$emit('update-case', { id: item.id, patch: { status: 'rejected' } })">改判误报</button>
            <button v-else-if="lane.key === 'added'" type="button" class="danger"
              :disabled="busyId === item.id" @click="$emit('update-case', { id: item.id, patch: { status: 'rejected' } })">移除补标</button>
            <button v-else type="button" class="restore"
              :disabled="busyId === item.id" @click="$emit('update-case', { id: item.id, patch: { status: 'confirmed', humanLabel: item.predicted_label } })">恢复预测</button>
          </div>
        </div>
        <div v-if="!lane.items.length" class="lane-empty">当前没有此类样本</div>
      </div>
    </article>
  </section>
</template>

<script setup>
import { computed } from 'vue'
const props = defineProps({
  items: { type: Array, default: () => [] },
  activeId: { type: String, default: '' },
  busyId: { type: String, default: '' }
})
defineEmits(['select', 'update-case'])
const lanes = computed(() => [
  { key: 'added', eyebrow: 'Human annotation', title: '人工标注', description: '模型在该图片漏检，由人工添加到校正层。', items: props.items.filter((item) => item.status === 'added') },
  { key: 'confirmed', eyebrow: 'Model hit', title: '模型命中', description: '模型框与人工判断一致，可再次改判。', items: props.items.filter((item) => item.status === 'confirmed') },
  { key: 'rejected', eyebrow: 'False positive', title: '误报驳回', description: '原始框被排除，也可恢复并重新进入计算。', items: props.items.filter((item) => item.status === 'rejected' || item.status === 'unreviewed') }
])
const personNumber = (personId = '') => personId.replace('Person', '').padStart(2, '0')
</script>

<style scoped>
.triage-board { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:14px; }
.review-lane { min-width:0; padding:14px; border:1px solid var(--border); border-top:4px solid var(--lane-color); border-radius:10px; background:#fff; box-shadow:var(--shadow-soft); }
.lane-added { --lane-color:#2f7df6; --lane-soft:#edf5ff; }.lane-confirmed { --lane-color:#24956f; --lane-soft:#ecf8f3; }.lane-rejected { --lane-color:#cf5656; --lane-soft:#fdf0f0; }
.review-lane header { display:flex; align-items:flex-start; justify-content:space-between; gap:10px; }.review-lane header span { color:var(--subtle); font-size:.68rem; font-weight:800; text-transform:uppercase; }
.review-lane h4 { margin:4px 0 0; font-size:1.02rem; }.review-lane header b { display:grid; place-items:center; min-width:34px; height:28px; border-radius:6px; color:var(--lane-color); background:var(--lane-soft); font-variant-numeric:tabular-nums; }
.review-lane > p { display:block!important; min-height:38px; margin:9px 0 12px; color:var(--muted); font-size:.75rem; line-height:1.5; }
.lane-list { display:grid; gap:8px; max-height:440px; overflow:auto; padding-right:3px; }
.review-card { border:1px solid var(--border); border-radius:8px; background:#fbfcfe; transition:150ms ease; }.review-card.is-active { border-color:var(--lane-color); box-shadow:0 0 0 2px color-mix(in srgb,var(--lane-color),transparent 82%); }
.card-main { display:grid; grid-template-columns:36px minmax(0,1fr) auto; align-items:center; gap:9px; width:100%; min-height:76px; padding:9px; color:inherit; text-align:left; background:transparent; }
.person-avatar { display:grid; place-items:center; width:36px; height:36px; border-radius:7px; color:var(--lane-color); background:var(--lane-soft); font-weight:900; }
.card-copy { min-width:0; }.card-copy strong,.card-copy small,.card-copy em { display:block; }.card-copy small { margin-top:2px; color:var(--muted); font-size:.72rem; }.card-copy em { margin-top:5px; overflow:hidden; color:var(--subtle); font-size:.68rem; font-style:normal; text-overflow:ellipsis; white-space:nowrap; }
.score { align-self:start; color:var(--muted); font-size:.7rem; font-variant-numeric:tabular-nums; }
.card-actions { display:grid; grid-template-columns:1fr 1fr; gap:6px; padding:0 8px 8px; }.card-actions button { min-height:34px; padding:0 7px; border:1px solid var(--border); border-radius:6px; color:var(--text); background:#fff; font-size:.7rem; font-weight:700; }
.card-actions .danger { color:#a94141; background:#fff7f7; }.card-actions .restore { color:#1d65c1; background:#f4f8ff; }.card-actions button:disabled { opacity:.48; cursor:wait; }
.lane-empty { padding:28px 10px; color:var(--subtle); text-align:center; font-size:.78rem; }
@media(max-width:1120px){.triage-board{grid-template-columns:1fr}.lane-list{max-height:300px}}
</style>
