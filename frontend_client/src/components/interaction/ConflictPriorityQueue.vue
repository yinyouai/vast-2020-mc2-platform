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
          <div v-if="item.ai_reasoning || item.reason" class="card-reason">
            <span v-if="item.ai_confidence !== undefined && item.ai_confidence !== null" class="ai-badge">AI置信度: {{ Math.round(item.ai_confidence * 100) }}%</span>
            <span>{{ item.ai_reasoning || item.reason }}</span>
          </div>
          <div class="card-actions">
            <button type="button" @click="$emit('select', item.id)">查看证据</button>
            <button v-if="item.status === 'confirmed'" type="button" class="danger"
              :disabled="busyId === item.id" @click="$emit('update-case', { id: item.id, patch: { status: 'rejected' } })">改判误报</button>
            <button v-else-if="item.status === 'added'" type="button" class="danger"
              :disabled="busyId === item.id" @click="$emit('update-case', { id: item.id, patch: { status: 'rejected' } })">移除补标</button>
            <button v-else-if="item.status === 'rejected'" type="button" class="restore"
              :disabled="busyId === item.id" @click="$emit('update-case', { id: item.id, patch: { status: 'confirmed', humanLabel: item.predicted_label } })">恢复预测</button>
            <button v-else type="button" class="restore"
              :disabled="busyId === item.id" @click="$emit('update-case', { id: item.id, patch: { status: 'confirmed', humanLabel: item.corrected_label } })">
              {{ item.status === 'dismissed' ? '改为补标' : item.box_id === -1 ? '确认有此物品' : '确认模型命中' }}
            </button>
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
  {
    key: 'review',
    eyebrow: 'Recommended review',
    title: '建议人工复核',
    description: '仅展示最不确定或最可能漏检的高优先图片。',
    items: props.items.filter((item) =>
      item.status === 'unreviewed'
      && ['evidence_search'].includes(item.review_kind)
    )
  },
  {
    key: 'model',
    eyebrow: 'Model detections',
    title: '模型命中',
    description: '原始模型命中无需全部人工确认，未被驳回时会参与最终评分。',
    items: props.items.filter((item) =>
      item.box_id >= 0
      && ['model_hit','weak_model_hit','verified'].includes(item.review_kind)
      && item.status !== 'rejected'
    )
  },
  {
    key: 'human',
    eyebrow: 'Human overrides',
    title: '人工修正',
    description: '只记录人工补标、误报驳回与其他明确覆盖操作。',
    items: props.items.filter((item) =>
      ['added','rejected','dismissed'].includes(item.status)
    )
  }
])
const personNumber = (personId = '') => personId.replace('Person', '').padStart(2, '0')
</script>

<style scoped>
.triage-board { display:grid; grid-template-columns:repeat(3,minmax(0,1fr)); gap:14px; }
.review-lane { min-width:0; padding:0 14px; border: none; }
  .lane-review { --lane-color:var(--warning); --lane-soft:rgba(245, 158, 11, 0.15); }.lane-model { --lane-color:var(--success); --lane-soft:rgba(16, 185, 129, 0.15); }.lane-human { --lane-color:var(--accent); --lane-soft:rgba(59, 130, 246, 0.15); }
.review-lane header { display:flex; align-items:flex-start; justify-content:space-between; gap:10px; }.review-lane header span { color:var(--subtle); font-size:.68rem; font-weight:800; text-transform:uppercase; }
.review-lane h4 { margin:4px 0 0; font-size:1.02rem; }.review-lane header b { display:grid; place-items:center; min-width:34px; height:28px; border-radius: 12px; color:var(--lane-color); background:var(--lane-soft); font-variant-numeric:tabular-nums; }
.review-lane > p { display:block!important; min-height:38px; margin:9px 0 12px; color:var(--muted); font-size:.75rem; line-height:1.5; }
.lane-list { display:grid; gap:8px; max-height:440px; overflow:auto; padding-right:3px; }
.review-card { border-bottom: 1px solid rgba(255, 255, 255, 0.05); padding: 8px 0; transition: 150ms ease; }.review-card.is-active { border-color:var(--lane-color); box-shadow: none; }
.card-main { display:grid; grid-template-columns:36px minmax(0,1fr) auto; align-items:center; gap:9px; width:100%; min-height:60px; padding:0 9px; color:inherit; text-align:left; background: transparent; border: none; outline: none; cursor: pointer; }
.person-avatar { display:grid; place-items:center; width:36px; height:36px; border-radius: 12px; color:var(--lane-color); background:var(--lane-soft); font-weight:900; }
.card-copy { min-width:0; }.card-copy strong,.card-copy small,.card-copy em { display:block; }.card-copy small { margin-top:2px; color:var(--muted); font-size:.72rem; }.card-copy em { margin-top:5px; overflow:hidden; color:var(--subtle); font-size:.68rem; font-style:normal; text-overflow:ellipsis; white-space:nowrap; }
.score { align-self:start; color:var(--muted); font-size:.7rem; font-variant-numeric:tabular-nums; }
.card-reason { padding:0 9px 8px; font-size:.72rem; color:var(--subtle); line-height:1.3; }
.ai-badge { display:inline-block; padding:2px 4px; border-radius: 12px; background:rgba(6, 182, 212, 0.15); color:var(--cyan); margin-right:6px; font-weight:700; font-size:.65rem; }
.card-actions { display:grid; grid-template-columns:1fr 1fr; gap:6px; padding:0 8px 8px; }.card-actions button { min-height:34px; padding:0 7px; border: none; border-radius: 12px; color:var(--text); background: transparent; font-size:.7rem; font-weight:700; }
.card-actions .danger { color:var(--danger); background: transparent; }.card-actions .restore { color:var(--accent); background: transparent; }.card-actions button:disabled { opacity:.48; cursor:wait; }
.lane-empty { padding:28px 10px; color:var(--subtle); text-align:center; font-size:.78rem; }
@media(max-width:1120px){.triage-board{grid-template-columns:1fr}.lane-list{max-height:300px}}
</style>
