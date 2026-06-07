<template>
  <section class="review-radar" aria-labelledby="review-radar-title">
    <header class="radar-header">
      <div>
        <div class="live-label"><i aria-hidden="true"></i>复核前筛选依据</div>
        <h4 id="review-radar-title">人工开始前，优先检查哪些 Person</h4>
        <p>只依据未经人工修正的模型输出排序，不使用已知误报、漏检或最终分组。默认选取异常分数前 25%，点击后由你完成实际判定。</p>
      </div>
      <div class="sync-copy" role="status">
        <span>{{ updatedLabel }}</span>
        <small>每 10 秒自动更新</small>
      </div>
    </header>

    <div class="radar-summary">
      <div><strong>{{ summary.people_to_review || 0 }}</strong><span>建议复核 Person</span></div>
      <div><strong>{{ summary.high_priority || 0 }}</strong><span>高优先级</span></div>
      <div><strong>{{ summary.raw_images || 0 }}</strong><span>参与筛选的原始图片</span></div>
    </div>

    <div v-if="people.length" class="priority-list">
      <button
        v-for="(person, index) in visiblePeople"
        :key="person.person_id"
        type="button"
        :class="['priority-row', `priority-${person.level}`]"
        @click="$emit('select-person', person)"
      >
        <span class="priority-rank">{{ String(index + 1).padStart(2, '0') }}</span>
        <span class="person-copy">
          <span class="person-title">
            <strong>{{ person.person_id }}</strong>
            <em>{{ levelLabel(person.level) }}</em>
          </span>
          <span class="risk-track" aria-hidden="true">
            <i :style="{ transform: `scaleX(${person.score / 100})` }"></i>
          </span>
          <span class="reason-line">{{ person.reasons.join('；') }}</span>
        </span>
        <span class="signal-grid" aria-label="风险信号明细">
          <span><b>{{ person.low_confidence_count }}</b>低置信</span>
          <span><b>{{ person.overlap_conflict_count }}</b>框冲突</span>
          <span><b>{{ person.empty_image_count }}</b>无检测图</span>
          <span><b>{{ person.corrupted_image_count }}</b>数据异常</span>
        </span>
        <span class="risk-score"><b>{{ person.score }}</b><small>/ 100</small></span>
      </button>
    </div>
    <div v-else class="radar-empty">正在根据原始模型信号计算复核优先级...</div>

    <footer class="score-legend">
      <details>
        <summary>查看评分规则</summary>
        <span v-for="(description, key) in scoring" :key="key">{{ description }}</span>
      </details>
      <button v-if="people.length > displayLimit" type="button" class="expand-button" @click="expanded = !expanded">
        {{ expanded ? '收起列表' : `查看全部 ${people.length} 人` }}
      </button>
    </footer>
  </section>
</template>

<script setup>
import { computed, ref } from 'vue'

const props = defineProps({
  people: { type: Array, default: () => [] },
  summary: { type: Object, default: () => ({}) },
  scoring: { type: Object, default: () => ({}) },
  updatedAt: { type: String, default: '' }
})
defineEmits(['select-person'])

const displayLimit = 6
const expanded = ref(false)
const visiblePeople = computed(() => expanded.value ? props.people : props.people.slice(0, displayLimit))
const updatedLabel = computed(() => {
  if (!props.updatedAt) return '等待首次同步'
  return `更新于 ${new Date(props.updatedAt).toLocaleTimeString('zh-CN', { hour12: false })}`
})
const levelLabel = (level) => ({ high: '优先复核', medium: '建议复核', low: '常规抽查' }[level] || '待评估')
</script>

<style scoped>
.review-radar{padding:18px;border:1px solid var(--border);border-radius:10px;background:#fff;box-shadow:var(--shadow-soft)}
.radar-header{display:flex;align-items:flex-start;justify-content:space-between;gap:20px}.radar-header h4{margin:6px 0 4px;font-size:1.12rem}.radar-header p{max-width:720px;margin:0;color:var(--muted);font-size:.78rem;line-height:1.55}
.live-label{display:flex;align-items:center;gap:7px;color:#187553;font-size:.7rem;font-weight:900;letter-spacing:.08em}.live-label i{width:8px;height:8px;border-radius:50%;background:#24956f;box-shadow:0 0 0 5px rgba(36,149,111,.12);animation:pulse 1.8s ease-out infinite}
.sync-copy{text-align:right}.sync-copy span,.sync-copy small{display:block}.sync-copy span{color:var(--text);font-size:.74rem;font-weight:800}.sync-copy small{margin-top:4px;color:var(--subtle);font-size:.68rem}
.radar-summary{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:8px;margin:16px 0 12px}.radar-summary div{display:flex;align-items:baseline;gap:8px;padding:10px 12px;border:1px solid var(--border);border-radius:7px;background:#f7f9fc}.radar-summary strong{font-size:1.22rem;font-variant-numeric:tabular-nums}.radar-summary span{color:var(--muted);font-size:.72rem}
.priority-list{display:grid;gap:7px}.priority-row{display:grid;grid-template-columns:38px minmax(0,1fr) auto 68px;align-items:center;gap:12px;width:100%;min-height:82px;padding:10px 12px;border:1px solid var(--border);border-left:4px solid var(--risk-color);border-radius:8px;color:var(--text);text-align:left;background:#fff;transition:transform 160ms ease,border-color 160ms ease,box-shadow 160ms ease;cursor:pointer}.priority-row:hover,.priority-row:focus-visible{transform:translateY(-1px);border-color:var(--risk-color);box-shadow:0 8px 22px rgba(32,47,66,.09);outline:none}.priority-high{--risk-color:#cf5656;--risk-soft:#fdf0f0}.priority-medium{--risk-color:#d18a22;--risk-soft:#fff6e5}.priority-low{--risk-color:#24956f;--risk-soft:#ecf8f3}
.priority-rank{display:grid;place-items:center;width:34px;height:34px;border-radius:7px;color:var(--risk-color);background:var(--risk-soft);font-size:.76rem;font-weight:900;font-variant-numeric:tabular-nums}.person-copy{min-width:0}.person-title{display:flex;align-items:center;gap:8px}.person-title strong{font-size:.9rem}.person-title em{padding:3px 6px;border-radius:4px;color:var(--risk-color);background:var(--risk-soft);font-size:.63rem;font-style:normal;font-weight:800}
.risk-track{display:block;overflow:hidden;height:4px;margin:8px 0 6px;border-radius:3px;background:#edf0f4}.risk-track i{display:block;width:100%;height:100%;border-radius:inherit;background:var(--risk-color);transform-origin:left center;transition:transform 240ms ease}.reason-line{display:block;overflow:hidden;color:var(--muted);font-size:.7rem;text-overflow:ellipsis;white-space:nowrap}
.signal-grid{display:grid;grid-template-columns:repeat(2,52px);gap:5px}.signal-grid span{color:var(--subtle);font-size:.65rem}.signal-grid b{margin-right:3px;color:var(--text);font-size:.74rem;font-variant-numeric:tabular-nums}.risk-score{text-align:right}.risk-score b,.risk-score small{display:block}.risk-score b{color:var(--risk-color);font-size:1.32rem;font-variant-numeric:tabular-nums}.risk-score small{color:var(--subtle);font-size:.62rem}
.score-legend{display:flex;align-items:flex-start;justify-content:space-between;gap:12px;margin-top:12px}.score-legend details{color:var(--muted);font-size:.7rem}.score-legend summary{min-height:36px;padding:9px 0;font-weight:800;cursor:pointer}.score-legend details span{display:block;margin:5px 0}.expand-button{min-height:38px;padding:0 12px;border:1px solid var(--border);border-radius:6px;color:var(--text);background:#fff;font-size:.72rem;font-weight:800}.radar-empty{padding:28px;color:var(--muted);text-align:center}
@keyframes pulse{0%{box-shadow:0 0 0 0 rgba(36,149,111,.28)}70%{box-shadow:0 0 0 8px rgba(36,149,111,0)}100%{box-shadow:0 0 0 0 rgba(36,149,111,0)}}
@media(prefers-reduced-motion:reduce){.live-label i{animation:none}.priority-row,.risk-track i{transition:none}}
@media(max-width:900px){.priority-row{grid-template-columns:34px minmax(0,1fr) 58px}.signal-grid{grid-column:2/-1;grid-template-columns:repeat(4,1fr)}}
@media(max-width:620px){.radar-header{display:block}.sync-copy{margin-top:10px;text-align:left}.radar-summary{grid-template-columns:1fr}.priority-row{grid-template-columns:34px minmax(0,1fr) 54px}.signal-grid{grid-template-columns:repeat(2,1fr)}}
</style>
