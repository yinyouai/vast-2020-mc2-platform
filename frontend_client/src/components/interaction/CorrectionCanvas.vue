<template>
  <section v-if="caseItem" class="correction-workbench">
    <div class="image-column">
      <div class="image-toolbar">
        <div><span>{{ caseItem.person_id }}</span><strong>{{ caseItem.image_id }}</strong></div>
        <div class="toolbar-badges">
          <span :class="['layer-badge', `status-${caseItem.status}`]">{{ statusLabel }}</span>
          <span v-if="caseItem.difficult" class="layer-badge difficult">困难样本</span>
        </div>
      </div>
      <div ref="stageRef" class="image-stage">
        <img ref="imageRef" :src="imageUrl" :alt="`${caseItem.image_id} 人工复核证据图`" @load="updateOverlay" />
        <div v-if="overlayStyle" class="real-detection-box" :style="overlayStyle">
          <span>{{ caseItem.predicted_label }} · {{ Number(caseItem.score).toFixed(3) }}</span>
        </div>
        <div v-else class="missing-box-note"><b>无原始识别框</b><span>该样本来自人工漏检补标</span></div>
      </div>
      <div class="box-legend">
        <span><i></i>原始 YOLO 边界框</span>
        <small v-if="caseItem.bbox">x {{ caseItem.bbox.x }} · y {{ caseItem.bbox.y }} · w {{ caseItem.bbox.width }} · h {{ caseItem.bbox.height }}</small>
      </div>
    </div>

    <aside class="review-form">
      <div class="review-layer raw">
        <span>01 / 原始模型</span><strong>{{ caseItem.predicted_label }}</strong>
        <small>box {{ caseItem.box_id }} · score {{ Number(caseItem.score || 0).toFixed(3) }}</small>
      </div>
      <div class="review-layer human">
        <span>02 / 本次人工判断</span>
        <label>校正标签
          <select v-model="draftLabel">
            <option v-for="label in labelOptions" :key="label" :value="label">{{ label }}</option>
          </select>
        </label>
        <label class="check-row"><input v-model="draftDifficult" type="checkbox" />标记为困难样本</label>
        <label>复核说明
          <textarea v-model="draftNote" rows="3"></textarea>
        </label>
      </div>
      <div class="review-context">
        <span>图片说明</span><p>{{ caseItem.caption || '该图片没有配套 caption。' }}</p>
        <template v-if="caseItem.text_snippets?.length"><span>文本证据</span><blockquote v-for="text in caseItem.text_snippets" :key="text">{{ text }}</blockquote></template>
      </div>
      <div class="review-actions">
        <button type="button" class="confirm" :disabled="isBusy" @click="submit('confirmed')">
          {{ caseItem.status === 'rejected' ? '恢复并确认' : '确认校正结果' }}
        </button>
        <button type="button" class="reject" :disabled="isBusy" @click="submit('rejected')">
          {{ caseItem.status === 'added' ? '移除人工补标' : caseItem.box_id === -1 ? '该图无此物品' : '判定为误报' }}
        </button>
      </div>
    </aside>
  </section>
</template>

<script setup>
import { computed, nextTick, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { STATIC_BASE, useDashboardStore } from '../../store/dashboard'
const props = defineProps({ caseItem: { type: Object, default: null } })
const emit = defineEmits(['submit-review'])
const store = useDashboardStore()
const stageRef = ref(null)
const imageRef = ref(null)
const overlayStyle = ref(null)
const draftLabel = ref('')
const draftDifficult = ref(false)
const draftNote = ref('')
let resizeObserver
const imageUrl = computed(() => `${STATIC_BASE}${props.caseItem?.image_path || ''}`)
const isBusy = computed(() => store.correctionInFlight === props.caseItem?.id)
const labelOptions = computed(() => Array.from(new Set([
  props.caseItem?.predicted_label,
  props.caseItem?.corrected_label,
  ...store.candidateRankings.map((item) => item.label)
].filter((label) => label && label !== '未检出' && label !== '误报'))))
const statusLabel = computed(() => ({ confirmed:'模型命中', added:'人工补标', rejected:'误报驳回', unreviewed:'待复核', dismissed:'该图未确认' }[props.caseItem?.status] || ''))
const resetDraft = () => {
  draftLabel.value = props.caseItem?.corrected_label === '误报' ? props.caseItem?.predicted_label : props.caseItem?.corrected_label || ''
  draftDifficult.value = Boolean(props.caseItem?.difficult)
  draftNote.value = props.caseItem?.reason || ''
  nextTick(updateOverlay)
}
const updateOverlay = () => {
  const bbox = props.caseItem?.bbox
  const image = imageRef.value
  const stage = stageRef.value
  if (!bbox || !image?.naturalWidth || !stage) { overlayStyle.value = null; return }
  const scale = Math.min(stage.clientWidth / image.naturalWidth, stage.clientHeight / image.naturalHeight)
  const renderedWidth = image.naturalWidth * scale
  const renderedHeight = image.naturalHeight * scale
  const offsetX = (stage.clientWidth - renderedWidth) / 2
  const offsetY = (stage.clientHeight - renderedHeight) / 2
  overlayStyle.value = {
    left: `${offsetX + bbox.x * scale}px`, top: `${offsetY + bbox.y * scale}px`,
    width: `${bbox.width * scale}px`, height: `${bbox.height * scale}px`
  }
}
const submit = (status) => emit('submit-review', {
  id: props.caseItem.id,
  patch: { status, humanLabel: draftLabel.value, difficult: draftDifficult.value, note: draftNote.value }
})
watch(() => props.caseItem, resetDraft, { immediate:true, deep:true })
onMounted(() => { resizeObserver = new ResizeObserver(updateOverlay); if(stageRef.value) resizeObserver.observe(stageRef.value) })
onBeforeUnmount(() => resizeObserver?.disconnect())
</script>

<style scoped>
.correction-workbench { display:grid; grid-template-columns:minmax(0,1.45fr) minmax(310px,.55fr); gap:14px; padding:14px; border: none; border-radius: 12px; background: transparent; box-shadow: none; }
.image-column { min-width:0; }.image-toolbar { display:flex; align-items:center; justify-content:space-between; gap:10px; margin-bottom:10px; }.image-toolbar span,.image-toolbar strong { display:block; }.image-toolbar span { color:var(--subtle); font-size:.72rem; }.image-toolbar strong { margin-top:3px; }
.toolbar-badges { display:flex; gap:6px; }.layer-badge { padding:6px 9px; border-radius: 12px; font-size:.7rem; font-weight:800; }.status-confirmed{color: var(--success);background: rgba(16, 185, 129, 0.1)}.status-added{color:var(--accent);background: rgba(59, 130, 246, 0.15)}.status-rejected{color:var(--danger);background: rgba(244, 63, 94, 0.1)}.status-unreviewed{color: var(--warning);background: rgba(245, 158, 11, 0.15)}.status-dismissed{color:#68788b;background: var(--surface-2)}.difficult{color: var(--warning);background: rgba(245, 158, 11, 0.15)}
.image-stage { position:relative; display:grid; place-items:center; overflow:hidden; height:520px; border: none; border-radius: 12px; background: rgba(0, 0, 0, 0.2); }.image-stage img { display:block; width:100%; height:100%; object-fit:contain; }
.real-detection-box { position:absolute; z-index:2; border:3px solid var(--danger); box-shadow: none; pointer-events:none; }.real-detection-box span { position:absolute; left:-3px; top:-30px; padding:5px 8px; color: var(--text); background: var(--danger); font-size:.7rem; font-weight:800; white-space:nowrap; }
.missing-box-note { position:absolute; left:14px; bottom:14px; display:flex; flex-direction:column; padding:9px 11px; border:1px dashed var(--accent); border-radius: 12px; color:var(--accent); background: rgba(59, 130, 246, 0.15); }.missing-box-note span { margin-top:3px; font-size:.7rem; }
.box-legend { display:flex; justify-content:space-between; gap:10px; margin-top:8px; color:var(--muted); font-size:.7rem; }.box-legend span{display:flex;align-items:center;gap:6px}.box-legend i{width:14px;height:9px;border:2px solid var(--danger)}
.review-form { display:grid; gap:10px; align-content:start; }.review-layer, .review-context { padding:13px 0; border-bottom: 1px solid rgba(255, 255, 255, 0.05); }.review-layer.raw{background: transparent}.review-layer.human{background: transparent;border-color: rgba(16, 185, 129, 0.3)}
.review-layer > span,.review-context > span { display:block; color:var(--subtle); font-size:.7rem; font-weight:800; }.review-layer > strong { display:block; margin:7px 0; font-size:1.08rem; }.review-layer small { color:var(--muted); }
.review-layer label { display:block; margin-top:11px; color:var(--muted); font-size:.75rem; font-weight:700; }.review-layer select,.review-layer textarea { width:100%; margin-top:5px; border: none; border-radius: 12px; color:var(--text); background: transparent; }.review-layer select { min-height:40px; padding:0 9px; }.review-layer textarea { padding:8px; resize:vertical; }
.check-row { display:flex!important; align-items:center; gap:8px; }.check-row input { width:17px;height:17px;margin:0;accent-color:var(--accent); }
.review-context p,.review-context blockquote { display:block!important; margin:6px 0 12px; color:var(--muted); font-size:.75rem; line-height:1.55; }.review-context blockquote { padding-left:9px;border-left:2px solid var(--accent) }
.review-actions { display:grid; grid-template-columns:1fr 1fr; gap:8px; }.review-actions button { min-height:44px; border-radius: 12px; font-size:.78rem; font-weight:800; }.review-actions .confirm { color: var(--text);background:var(--success) }.review-actions .reject { color:var(--danger);background: transparent;border: none;cursor:wait}
@media(max-width:1050px){.correction-workbench{grid-template-columns:1fr}.image-stage { position:relative; display:grid; place-items:center; overflow:hidden; height:520px; border: none; border-radius: 12px; background: rgba(0, 0, 0, 0.2); }}
</style>
