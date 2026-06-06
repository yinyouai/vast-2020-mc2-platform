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
          {{ caseItem.status === 'added' ? '移除人工补标' : '判定为误报' }}
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
const statusLabel = computed(() => ({ confirmed:'模型命中', added:'人工补标', rejected:'误报驳回', unreviewed:'待复核' }[props.caseItem?.status] || ''))
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
.correction-workbench { display:grid; grid-template-columns:minmax(0,1.45fr) minmax(310px,.55fr); gap:14px; padding:14px; border:1px solid var(--border); border-radius:10px; background:#fff; box-shadow:var(--shadow); }
.image-column { min-width:0; }.image-toolbar { display:flex; align-items:center; justify-content:space-between; gap:10px; margin-bottom:10px; }.image-toolbar span,.image-toolbar strong { display:block; }.image-toolbar span { color:var(--subtle); font-size:.72rem; }.image-toolbar strong { margin-top:3px; }
.toolbar-badges { display:flex; gap:6px; }.layer-badge { padding:6px 9px; border-radius:5px; font-size:.7rem; font-weight:800; }.status-confirmed{color:#187553;background:#eaf7f1}.status-added{color:#1d65c1;background:#ebf3ff}.status-rejected{color:#a94141;background:#fcecec}.difficult{color:#8a5a0a;background:#fff4d9}
.image-stage { position:relative; display:grid; place-items:center; overflow:hidden; height:520px; border:1px solid var(--border); border-radius:8px; background:#eef2f6; }.image-stage img { display:block; width:100%; height:100%; object-fit:contain; }
.real-detection-box { position:absolute; z-index:2; border:3px solid #cf5656; box-shadow:0 0 0 2px rgba(255,255,255,.8),0 8px 24px rgba(207,86,86,.22); pointer-events:none; }.real-detection-box span { position:absolute; left:-3px; top:-30px; padding:5px 8px; color:#fff; background:#b94646; font-size:.7rem; font-weight:800; white-space:nowrap; }
.missing-box-note { position:absolute; left:14px; bottom:14px; display:flex; flex-direction:column; padding:9px 11px; border:1px dashed #2f7df6; border-radius:6px; color:#1d65c1; background:rgba(244,248,255,.94); }.missing-box-note span { margin-top:3px; font-size:.7rem; }
.box-legend { display:flex; justify-content:space-between; gap:10px; margin-top:8px; color:var(--muted); font-size:.7rem; }.box-legend span{display:flex;align-items:center;gap:6px}.box-legend i{width:14px;height:9px;border:2px solid #cf5656}
.review-form { display:grid; gap:10px; align-content:start; }.review-layer,.review-context { padding:13px; border:1px solid var(--border); border-radius:8px; }.review-layer.raw{background:#f5f8fc}.review-layer.human{background:#f2faf7;border-color:#cbe8dc}
.review-layer > span,.review-context > span { display:block; color:var(--subtle); font-size:.7rem; font-weight:800; }.review-layer > strong { display:block; margin:7px 0; font-size:1.08rem; }.review-layer small { color:var(--muted); }
.review-layer label { display:block; margin-top:11px; color:var(--muted); font-size:.75rem; font-weight:700; }.review-layer select,.review-layer textarea { width:100%; margin-top:5px; border:1px solid var(--border-strong); border-radius:6px; color:var(--text); background:#fff; }.review-layer select { min-height:40px; padding:0 9px; }.review-layer textarea { padding:8px; resize:vertical; }
.check-row { display:flex!important; align-items:center; gap:8px; }.check-row input { width:17px;height:17px;margin:0;accent-color:var(--accent); }
.review-context p,.review-context blockquote { display:block!important; margin:6px 0 12px; color:var(--muted); font-size:.75rem; line-height:1.55; }.review-context blockquote { padding-left:9px;border-left:2px solid var(--accent) }
.review-actions { display:grid; grid-template-columns:1fr 1fr; gap:8px; }.review-actions button { min-height:44px; border-radius:7px; font-size:.78rem; font-weight:800; }.review-actions .confirm { color:#fff;background:#24956f }.review-actions .reject { color:#a94141;background:#fff4f4;border:1px solid #efc6c6 }.review-actions button:disabled{opacity:.5;cursor:wait}
@media(max-width:1050px){.correction-workbench{grid-template-columns:1fr}.image-stage{height:430px}}
</style>
