<template>
  <section class="panel evidence-gallery-panel">
    <div class="panel-header">
      <div>
        <h4 class="panel-title">核心组织终端照片名册</h4>
        <p class="panel-subtitle">参考样例中的人物照片墙，将核心嫌疑、误报对照和外圈参会者做成可点击的证据样本册。</p>
      </div>
      <span class="data-chip">{{ visibleSamples.length }} 个样本</span>
    </div>

    <div class="evidence-filter-row" role="tablist" aria-label="照片样本筛选">
      <button
        v-for="filter in filters"
        :key="filter.key"
        type="button"
        :class="['evidence-filter', activeFilter === filter.key ? 'is-active' : '']"
        @click="activeFilter = filter.key"
      >
        <strong>{{ filter.label }}</strong>
        <span>{{ filter.caption }}</span>
      </button>
    </div>

    <div class="evidence-gallery-layout">
      <div class="evidence-card-grid" role="list">
        <button
          v-for="sample in visibleSamples"
          :key="sample.id"
          type="button"
          role="listitem"
          :class="['evidence-card', `is-${sample.kind}`, activeSample.id === sample.id ? 'is-selected' : '']"
          :style="{ '--sample-accent': sample.accent }"
          @click="selectSample(sample)"
        >
          <span class="evidence-thumb">
            <span class="thumb-placeholder">
              <strong>{{ sample.person }}</strong>
              <small>{{ sample.fallback }}</small>
            </span>
            <img
              :src="sample.image"
              :alt="`${sample.person} 证据照片`"
              loading="lazy"
              @error="hideBrokenImage"
            />
            <span class="sample-state">{{ sample.status }}</span>
          </span>
          <span class="sample-copy">
            <strong>{{ sample.person }}</strong>
            <small>{{ sample.summary }}</small>
          </span>
        </button>
      </div>

      <aside class="evidence-preview-panel" aria-live="polite">
        <div class="preview-head">
          <div>
            <span>{{ activeSample.groupLabel }}</span>
            <strong>{{ activeSample.person }} / {{ activeSample.title }}</strong>
          </div>
          <button type="button" class="ghost-btn" @click="store.selectPerson(activeSample.person)">锁定此人</button>
        </div>

        <div class="evidence-stage">
          <div class="stage-placeholder">
            <strong>{{ activeSample.person }}</strong>
            <span>{{ activeSample.fallback }}</span>
          </div>
          <img
            :key="activeSample.id"
            :src="activeSample.image"
            :alt="`${activeSample.person} 证据大图`"
            @error="hideBrokenImage"
          />
          <div
            v-for="box in activeSample.boxes"
            :key="box.label"
            :class="['detection-box', `is-${box.kind}`]"
            :style="box.style"
          >
            <span>{{ box.label }}</span>
          </div>
        </div>

        <div class="evidence-insight-grid">
          <article>
            <span>文本语义</span>
            <p>{{ activeSample.quote }}</p>
          </article>
          <article>
            <span>模型噪声</span>
            <p>{{ activeSample.machine }}</p>
          </article>
          <article class="is-verdict">
            <span>人工判定</span>
            <p>{{ activeSample.verdict }}</p>
          </article>
        </div>
      </aside>
    </div>
  </section>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useDashboardStore } from '../../store/dashboard'

const store = useDashboardStore()
const activeFilter = ref('all')
const activeSampleId = ref('Person3')

const imageUrl = (person, imageName) =>
  `http://localhost:5000/static/MC2-Image-Data/${person}/${imageName}`

const samples = [
  {
    id: 'Person3',
    person: 'Person3',
    image: imageUrl('Person3', 'Person3_1.jpg'),
    kind: 'core',
    accent: '#c653ff',
    status: '已确认',
    title: '黄色提袋入口识别标记',
    groupLabel: '核心组织 A / 高置信',
    summary: '黄色提袋与文本约定高度一致',
    fallback: '黄色提袋样本',
    quote: '入口处拿到明亮黄色提袋，这是线下识别标记。',
    machine: '模型曾把显著区域误推为“高危红帽/背景物”，存在类别偏移。',
    verdict: '人工复核后保留黄色提袋，作为核心组线下会合符号。',
    boxes: [
      { label: '人工确认：黄色提袋', kind: 'green', style: 'left:30%;top:22%;width:36%;height:46%;' },
      { label: '模型噪声：红帽误报', kind: 'red', style: 'left:22%;top:18%;width:54%;height:52%;' }
    ]
  },
  {
    id: 'Person7',
    person: 'Person7',
    image: imageUrl('Person7', 'Person7_11.jpg'),
    kind: 'core',
    accent: '#c653ff',
    status: '已确认',
    title: '线下同步行动记录',
    groupLabel: '核心组织 A / 高置信',
    summary: '行程记录与核心组共现',
    fallback: '同步行动样本',
    quote: '线下行程与核心组重叠，但公开社交互动近乎缺失。',
    machine: '图像侧没有强公共物品信号，社交侧反而呈现异常沉默。',
    verdict: '作为核心组成员保留，送入最终社交隔离网络验证。',
    boxes: [
      { label: '核心成员节点', kind: 'purple', style: 'left:16%;top:16%;width:56%;height:54%;' }
    ]
  },
  {
    id: 'Person9',
    person: 'Person9',
    image: imageUrl('Person9', 'Person9_1.jpg'),
    kind: 'core',
    accent: '#c653ff',
    status: '已确认',
    title: '笑脸贴标视觉线索',
    groupLabel: '核心组织 A / 高置信',
    summary: '贴标、袋身和会合暗号关联',
    fallback: '笑脸贴标样本',
    quote: '黄色符号反复出现，且与其他核心成员的线下物证同频。',
    machine: '机器会把局部图案拆成多个低置信类别，导致候选过散。',
    verdict: '保留为辅助视觉线索，与黄色提袋共同支撑线下识别链。',
    boxes: [
      { label: '局部符号高亮', kind: 'green', style: 'left:20%;top:20%;width:58%;height:44%;' }
    ]
  },
  {
    id: 'Person10',
    person: 'Person10',
    image: imageUrl('Person10', 'Person10_10.jpg'),
    kind: 'core',
    accent: '#c653ff',
    status: '已确认',
    title: '核心组静默节点',
    groupLabel: '核心组织 A / 高置信',
    summary: '物证指向强，线上互动弱',
    fallback: '静默节点样本',
    quote: '文本片段显示其与线下接头流程有关，但公开平台没有自然互动链。',
    machine: '模型可见证据有限，需要依赖多源交叉校准。',
    verdict: '在树状网络中表现为外圈核心节点，线下强连接、线上弱连接。',
    boxes: [
      { label: '外圈核心节点', kind: 'purple', style: 'left:22%;top:18%;width:52%;height:48%;' }
    ]
  },
  {
    id: 'Person12',
    person: 'Person12',
    image: imageUrl('Person12', 'Person12_3.jpg'),
    kind: 'core',
    accent: '#c653ff',
    status: '已确认',
    title: '加密协议相关分支',
    groupLabel: '核心组织 A / 高置信',
    summary: '文本证据指向核心分支',
    fallback: '文本证据样本',
    quote: '相关文本强调“不要在公开平台留下直接联系”。',
    machine: '图像证据不总是显著，需要文本侧补强。',
    verdict: '保留为核心组协同行为证据，连接最终叙事链。',
    boxes: [
      { label: '文本-物证交叉点', kind: 'green', style: 'left:24%;top:18%;width:48%;height:52%;' }
    ]
  },
  {
    id: 'Person17',
    person: 'Person17',
    image: imageUrl('Person17', 'Person17_11.jpg'),
    kind: 'core',
    accent: '#c653ff',
    status: '已确认',
    title: '图腾收敛成员',
    groupLabel: '核心组织 A / 高置信',
    summary: '与黄色提袋路径稳定同现',
    fallback: '图腾收敛样本',
    quote: '物证收敛后仍与核心路径一致，没有被公共物品过滤掉。',
    machine: '低置信检测会掺入无关物品，需要第四层过滤。',
    verdict: '过滤后仍保留，是核心组稳定成员。',
    boxes: [
      { label: '过滤后保留', kind: 'green', style: 'left:18%;top:20%;width:52%;height:48%;' }
    ]
  },
  {
    id: 'Person32',
    person: 'Person32',
    image: imageUrl('Person32', 'Person32_1.jpg'),
    kind: 'core',
    accent: '#c653ff',
    status: '已确认',
    title: '双鸟图像异常共现',
    groupLabel: '核心组织 A / 高置信',
    summary: '特殊图像与核心组闭环',
    fallback: '双鸟图像样本',
    quote: '图像中出现非公共会场资产，与核心组其他稀有线索共同出现。',
    machine: '单图像类别不能直接定案，但能作为共现矩阵中的高亮点。',
    verdict: '纳入核心名单，作为线下识别链的外部补强证据。',
    boxes: [
      { label: '特殊视觉线索', kind: 'green', style: 'left:14%;top:12%;width:64%;height:58%;' }
    ]
  },
  {
    id: 'Person38',
    person: 'Person38',
    image: imageUrl('Person38', 'Person38_1.jpg'),
    kind: 'core',
    accent: '#c653ff',
    status: '已确认',
    title: '最后一名核心收束节点',
    groupLabel: '核心组织 A / 高置信',
    summary: '与核心组同物证收束',
    fallback: '收束节点样本',
    quote: '其照片与文本均指向同一线下识别流程。',
    machine: '图像检测框需要人工确认边界，避免错归为普通装饰物。',
    verdict: '作为第八名核心成员进入最终网络。',
    boxes: [
      { label: '核心收束', kind: 'green', style: 'left:20%;top:20%;width:58%;height:46%;' }
    ]
  },
  {
    id: 'Person27',
    person: 'Person27',
    image: imageUrl('Person27', 'Person27_1.jpg'),
    kind: 'conflict',
    accent: '#df6a6a',
    status: '误报洗白',
    title: '公共物品误报对照',
    groupLabel: '对照样本 / 高冲突',
    summary: '南瓜笔记本更像普通资产',
    fallback: '公共物品对照',
    quote: '文本描述更接近会场记录用品，而非线下接头符号。',
    machine: '模型曾给出多个高重叠候选，制造“复杂嫌疑”的假象。',
    verdict: '从核心组排除，作为误报洗白样本保留。',
    boxes: [
      { label: '公共物品：笔记本', kind: 'green', style: 'left:22%;top:28%;width:42%;height:36%;' },
      { label: '误报候选', kind: 'red', style: 'left:12%;top:14%;width:58%;height:50%;' }
    ]
  },
  {
    id: 'Person21',
    person: 'Person21',
    image: imageUrl('Person21', 'Person21_2.jpg'),
    kind: 'outer',
    accent: '#35b5a6',
    status: '外圈参照',
    title: '正常参会基线',
    groupLabel: '外圈参会者 / 低噪声',
    summary: '无核心图腾、社交行为自然',
    fallback: '正常参会样本',
    quote: '活动记录更接近日常参会行为，缺少线下暗号语义。',
    machine: '视觉模型低置信输出不应直接放大为嫌疑。',
    verdict: '作为背景基线，帮助解释核心组为什么异常。',
    boxes: [
      { label: '背景基线', kind: 'green', style: 'left:26%;top:18%;width:44%;height:48%;' }
    ]
  },
  {
    id: 'Person13',
    person: 'Person13',
    image: imageUrl('Person13', 'Person13_11.jpg'),
    kind: 'outer',
    accent: '#35b5a6',
    status: '行为洗白',
    title: '自然互动参会者',
    groupLabel: '外圈参会者 / 对照',
    summary: '社交矩阵中互动自然',
    fallback: '自然互动样本',
    quote: '公开互动符合普通参会者模式，不呈现刻意隔离。',
    machine: '图像侧没有稳定暗号物证。',
    verdict: '排除出核心链条，用于对照社交隔离真空。',
    boxes: [
      { label: '自然互动', kind: 'green', style: 'left:24%;top:22%;width:48%;height:46%;' }
    ]
  }
]

const filters = [
  { key: 'all', label: '全部样本', caption: `${samples.length}` },
  { key: 'core', label: '核心组织', caption: '8' },
  { key: 'conflict', label: '高冲突', caption: '误报' },
  { key: 'outer', label: '外圈对照', caption: '基线' }
]

const visibleSamples = computed(() => {
  if (activeFilter.value === 'all') return samples
  return samples.filter((sample) => sample.kind === activeFilter.value)
})

const activeSample = computed(() =>
  visibleSamples.value.find((sample) => sample.id === activeSampleId.value) || visibleSamples.value[0] || samples[0]
)

const selectSample = (sample) => {
  activeSampleId.value = sample.id
  store.selectPerson(sample.person)
}

const hideBrokenImage = (event) => {
  event.target.style.display = 'none'
}
</script>

<style scoped>
.evidence-gallery-panel {
  overflow: hidden;
  padding: clamp(22px, 3vw, 34px);
}

.evidence-filter-row {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 20px;
}

.evidence-filter {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  min-height: 42px;
  padding: 0 14px;
  border: 1px solid var(--border);
  border-radius: 999px;
  color: var(--muted);
  background: rgba(255, 255, 255, 0.74);
  transition:
    transform var(--motion-fast) var(--ease-spring),
    border-color var(--motion-fast) ease,
    color var(--motion-fast) ease,
    background var(--motion-fast) ease;
}

.evidence-filter:hover,
.evidence-filter.is-active {
  transform: translateY(-2px);
  border-color: rgba(53, 181, 166, 0.28);
  color: var(--text);
  background: rgba(53, 181, 166, 0.1);
}

.evidence-filter span {
  color: var(--subtle);
  font-size: 0.78rem;
}

.evidence-gallery-layout {
  display: grid;
  grid-template-columns: minmax(360px, 1fr) minmax(420px, 0.86fr);
  gap: clamp(22px, 3vw, 36px);
  align-items: stretch;
}

.evidence-card-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(142px, 1fr));
  gap: 14px;
  align-content: start;
}

.evidence-card {
  display: flex;
  flex-direction: column;
  gap: 10px;
  min-height: 208px;
  padding: 10px;
  border: 2px solid color-mix(in srgb, var(--sample-accent), white 35%);
  border-radius: 18px;
  color: var(--text);
  text-align: left;
  background:
    linear-gradient(180deg, rgba(255, 255, 255, 0.92), rgba(247, 251, 255, 0.82)),
    rgba(255, 255, 255, 0.8);
  box-shadow: 0 12px 28px rgba(48, 78, 114, 0.08);
  transition:
    transform var(--motion-medium) var(--ease-spring),
    box-shadow var(--motion-medium) ease,
    border-color var(--motion-medium) ease;
}

.evidence-card:hover,
.evidence-card.is-selected {
  transform: translateY(-6px) scale(1.02);
  border-color: var(--sample-accent);
  box-shadow: 0 24px 46px color-mix(in srgb, var(--sample-accent), transparent 74%);
}

.evidence-thumb {
  position: relative;
  display: block;
  overflow: hidden;
  border-radius: 14px;
  aspect-ratio: 1 / 0.82;
  background:
    linear-gradient(rgba(47, 125, 246, 0.06) 1px, transparent 1px),
    linear-gradient(90deg, rgba(47, 125, 246, 0.06) 1px, transparent 1px),
    linear-gradient(180deg, #ffffff, #f4f8fd);
  background-size: 100% 28px, 28px 100%, 100% 100%;
}

.evidence-thumb img,
.evidence-stage img {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.thumb-placeholder,
.stage-placeholder {
  position: absolute;
  inset: 0;
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: 12px;
  color: var(--muted);
}

.thumb-placeholder strong,
.stage-placeholder strong {
  color: var(--text);
}

.thumb-placeholder small,
.stage-placeholder span {
  margin-top: 5px;
  line-height: 1.45;
}

.sample-state {
  position: absolute;
  top: 8px;
  right: 8px;
  z-index: 2;
  padding: 5px 9px;
  border-radius: 999px;
  color: #ffffff;
  background: var(--sample-accent);
  font-size: 0.72rem;
  font-weight: 900;
}

.sample-copy strong,
.sample-copy small {
  display: block;
}

.sample-copy small {
  margin-top: 5px;
  color: var(--muted);
  line-height: 1.45;
}

.evidence-preview-panel {
  display: flex;
  flex-direction: column;
  gap: 14px;
  min-width: 0;
}

.preview-head {
  display: flex;
  align-items: flex-start;
  justify-content: space-between;
  gap: 14px;
  padding: 14px;
  border: 1px solid var(--border);
  border-radius: var(--radius);
  background: rgba(255, 255, 255, 0.78);
}

.preview-head span,
.evidence-insight-grid span {
  color: var(--subtle);
  font-size: 0.78rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.preview-head strong {
  display: block;
  margin-top: 8px;
  font-size: 1.12rem;
}

.evidence-stage {
  position: relative;
  overflow: hidden;
  min-height: clamp(360px, 48dvh, 560px);
  border: 1px solid rgba(53, 89, 138, 0.14);
  border-radius: var(--radius-xl);
  background:
    radial-gradient(circle at top right, rgba(240, 180, 76, 0.12), transparent 28%),
    linear-gradient(rgba(47, 125, 246, 0.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(47, 125, 246, 0.05) 1px, transparent 1px),
    linear-gradient(180deg, #ffffff, #f7fbff);
  background-size: auto, 100% 56px, 56px 100%, 100% 100%;
  box-shadow: var(--shadow-soft);
}

.stage-placeholder {
  padding: 24px;
  font-size: 1rem;
}

.detection-box {
  position: absolute;
  z-index: 3;
  border: 3px solid;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.08);
  animation: box-breathe 2.8s ease-in-out infinite;
}

.detection-box span {
  position: absolute;
  top: -10px;
  left: 12px;
  transform: translateY(-100%);
  display: inline-flex;
  padding: 6px 10px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.94);
  box-shadow: var(--shadow-soft);
  white-space: nowrap;
  font-size: 0.74rem;
  font-weight: 900;
}

.detection-box.is-green {
  border-color: #39a97d;
}

.detection-box.is-green span {
  color: #1c8a67;
}

.detection-box.is-red {
  border-color: #df6a6a;
  border-style: dashed;
}

.detection-box.is-red span {
  color: #b44e4e;
}

.detection-box.is-purple {
  border-color: #c653ff;
}

.detection-box.is-purple span {
  color: #9a35d8;
}

.evidence-insight-grid {
  display: grid;
  grid-template-columns: repeat(3, minmax(0, 1fr));
  gap: 12px;
}

.evidence-insight-grid article {
  padding: 14px;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  background: rgba(255, 255, 255, 0.82);
}

.evidence-insight-grid article.is-verdict {
  border-color: rgba(57, 169, 125, 0.28);
  background: rgba(57, 169, 125, 0.08);
}

.evidence-insight-grid p {
  margin: 8px 0 0;
  color: var(--muted);
  line-height: 1.7;
}

@keyframes box-breathe {
  0%,
  100% {
    box-shadow: 0 0 0 0 rgba(57, 169, 125, 0.18);
  }
  50% {
    box-shadow: 0 0 0 8px rgba(57, 169, 125, 0);
  }
}

@media (max-width: 1320px) {
  .evidence-gallery-layout {
    grid-template-columns: 1fr;
  }
}

@media (max-width: 760px) {
  .evidence-card-grid,
  .evidence-insight-grid {
    grid-template-columns: 1fr;
  }

  .preview-head {
    flex-direction: column;
  }
}
</style>
