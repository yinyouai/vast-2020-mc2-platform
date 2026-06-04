<template>
  <div class="glass-card sankey-wrapper">
    <div class="sankey-header">
      <h4 class="舱室标题">🔮 特异性网络资产漏斗流向图 (桑基拓扑传导)</h4>
      <span class="glow-pill">💡 高纯度情报聚焦</span>
    </div>

    <div class="sankey-body">
      <div class="sankey-chart" ref="sankeyRef"></div>

      <div class="sankey-hud">
        <h5>🎯 去噪剥离研判手记</h5>

        <div v-if="store.excludedItems.length === 0" class="hud-status status-waiting">
          <p>❌ <b>会场背景干扰过高 (未去噪)：</b>全网发帖充斥会场泛滥礼品噪声 (骰子、发夹持有率 60%、47%)。</p>
          <p class="mt-1 text-warning">⚠️ <b>致命线索模糊：</b>普通参会白帽 (Person27) 的笔记本与真正黑客的黄色提袋交织共现。请勾选放逐普及物资！</p>
        </div>

        <div v-else-if="store.excludedItems.length < 3" class="hud-status status-progress">
          <p>⏳ <b>反向排除进行中：</b>系统正像过滤电磁噪声一样执行全局削波 (已排除 {{ store.excludedItems.length }} 项)。</p>
          <p class="mt-1">🔍 <b>洗白特征初现：</b>大量无辜参会人员行为光谱向正常背景收敛。继续放逐更多普及物资！</p>
        </div>

        <div v-else class="hud-status status-success">
          <p class="success-txt">🎉 <b>地下接头暗号图腾完全破译！</b></p>
          <p class="mt-1">🟩 <b>路人排除洗白：</b>当大众礼品被反向切除后，原本可疑的笔记本 (Person27) 流向彻底沉降入无害背景区。</p>
          <p class="mt-1">🚨 <b>铁证图腾锁死：</b>整个全景社交资产流以 100% 数学纯度全部汇聚指向 <strong class="text-purple">【秘密黄色接头提袋】</strong>！</p>
          <span class="blink-action" @click="triggerFourthLayer">👉 点击左图黄色提袋节点，下钻查阅像素级照片物证链！</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch, onUnmounted } from 'vue'
import { useDashboardStore } from '../../store/dashboard'
import * as echarts from 'echarts'

const store = useDashboardStore()
const sankeyRef = ref(null)
let chart = null

function renderSankey() {
  if (!sankeyRef.value) return
  if (chart) chart.dispose()
  chart = echarts.init(sankeyRef.value, undefined)

  const nodes = [
    { name: '40名候选人', itemStyle: { color: '#64B5F6' } },
    { name: '免费礼品背景', itemStyle: { color: '#BDBDBD' } },
    { name: '秘密组织暗号', itemStyle: { color: '#BF5AF2' } },
    { name: '💛 黄色提袋图腾', itemStyle: { color: '#FFD54F' } }
  ]

  let noiseFlow = store.excludedItems.length >= 3 ? 5 : store.excludedItems.length === 0 ? 50 : 25
  let secretFlow = 35

  const links = [
    { source: '40名候选人', target: '免费礼品背景', value: noiseFlow },
    { source: '40名候选人', target: '秘密组织暗号', value: secretFlow },
    { source: '秘密组织暗号', target: '💛 黄色提袋图腾', value: secretFlow }
  ]

  chart.setOption({
    backgroundColor: 'transparent',
    tooltip: {
      trigger: 'item',
      triggerOn: 'mousemove'
    },
    series: [{
      type: 'sankey',
      layout: 'none',
      emphasis: { focus: 'adjacency' },
      data: nodes,
      links: links,
      nodeWidth: 16,
      nodeGap: 18,
      label: { fontSize: 11, color: '#1A1A2E' },
      lineStyle: { color: 'source', curveness: 0.5, opacity: 0.2 }
    }]
  })

  chart.on('click', (params) => {
    if (params.name?.includes('黄色提袋') || params.name === '秘密组织暗号') {
      if (store.excludedItems.length >= 3) {
        store.isFourthLayerActive = true
      } else {
        alert('🔒 深度钻取被拦截：请先在上方漏斗中勾选排除全部大众普及小礼品！')
      }
    }
  })
}

function triggerFourthLayer() {
  if (store.excludedItems.length >= 3) {
    store.isFourthLayerActive = true
  }
}

watch(() => store.excludedItems, renderSankey, { deep: true })
onMounted(renderSankey)
onUnmounted(() => chart?.dispose())
</script>

<style scoped>
.sankey-wrapper { display: flex; flex-direction: column; height: 100%; }
.sankey-header { display: flex; justify-content: space-between; align-items: center; }
.glow-pill {
  font-size: 10px; background: rgba(191,90,242,0.1);
  color: var(--accent-purple); padding: 2px 10px;
  border-radius: var(--radius-full); font-weight: var(--weight-semibold);
  border: 1px solid rgba(191,90,242,0.2);
}
.sankey-body { display: grid; grid-template-columns: 1.2fr 1fr; gap: var(--space-lg); flex: 1; min-height: 0; margin-top: var(--space-sm); }
.sankey-chart { height: 100%; min-height: 200px; }

.sankey-hud {
  background: rgba(0,0,0,0.01); border: 1px solid rgba(0,0,0,0.04);
  padding: var(--space-md); border-radius: var(--radius-sm);
  font-size: var(--text-xs); color: var(--text-secondary); line-height: var(--leading-relaxed);
  display: flex; flex-direction: column;
}
.sankey-hud h5 { margin: 0 0 var(--space-sm); font-size: var(--text-sm); color: var(--text-primary); font-weight: var(--weight-medium); }
.hud-status { padding: var(--space-sm) var(--space-md); border-radius: var(--radius-sm); flex: 1; display: flex; flex-direction: column; justify-content: center; }
.hud-status p { margin: 0; }
.mt-1 { margin-top: 6px; }
.status-waiting { background: rgba(255,59,48,0.03); border: 1px solid rgba(255,59,48,0.08); }
.status-progress { background: rgba(255,159,10,0.03); border: 1px solid rgba(255,159,10,0.08); }
.status-success { background: rgba(49,194,124,0.03); border: 1px solid rgba(49,194,124,0.08); }
.text-warning { color: var(--accent-warning); }
.success-txt { color: var(--accent-primary); font-weight: var(--weight-bold); font-size: var(--text-sm); }
.blink-action { display: inline-block; margin-top: var(--space-md); color: var(--accent-primary); font-weight: var(--weight-semibold); cursor: pointer; animation: pulse-indicator 2s infinite; }
</style>
