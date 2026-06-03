<template>
  <div class="apple-glass-card sankey-wrapper">
    <div class="sankey-header">
      <h4 class="舱室标题">🔮 组件 13 : 特异性网络资产漏斗流向图 (桑基拓扑传导)</h4>
      <span class="glow-pill">💡 发现高纯度情报聚焦</span>
    </div>

    <div class="sankey-body-layout">
      <div class="sankey-chart-viewport" ref="sankeyRef"></div>

      <div class="sankey-interactive-hud">
        <h5>🎯 首席情报分析官·去噪剥离研判手记：</h5>

        <div v-if="store.excludedItems.length === 0" class="hud-status-box status-waiting">
          <p>
            ❌ <b>会场背景干扰过高 (未去噪)</b>：当前全网发帖资产里充斥着海量的会场泛滥礼品噪声（骰子与发夹持有率高达 60% 和 47%）。
          </p>
          <p class="mt-2 text-warning">
            ⚠️ <b>致命线索模糊</b>：此时，普通参会白帽（如 <b>Person27</b>）用于写代码的【笔记本资产】，与真正黑客用于地下接头的【黄色提袋】在光谱中交织共现。我们无法分辨谁是无辜无害路人，谁是高危团伙！请在上方控制台漏斗中开始<b>勾选放逐普及物资</b>！
          </p>
        </div>

        <div v-else-if="store.excludedItems.length < 3" class="hud-status-box status-progress">
          <p>
            ⏳ <b>反向排除进行中 (纯度提升)</b>：系统正像过滤电磁噪声一样，对已勾选的普及礼品执行全局削波（当前已排除 {{ store.excludedItems.length }} 项背景物资）。
          </p>
          <p class="mt-2">
            🔍 <b>洗白特征初现</b>：随着会场免费分发物品被逐步放逐，大量无辜参会人员的行为光谱正在向正常背景收敛。请继续<b>将骰子、发夹、红哨子全量勾选放逐</b>，逼迫犯罪核心显现！
          </p>
        </div>

        <div v-else class="hud-status-box status-success">
          <p class="success-txt">
            🎉 <b>地下接头暗号图腾完全破译！</b>
          </p>
          <p class="mt-1 text-closure">
            🟩 <b>路人排除洗白</b>：当会场大众礼品被反向彻底切除后，原本可疑的【笔记本（代表人物: <b>Person27</b>）】持有流向彻底收敛沉降入无害会场背景区，证实其为全民普及发放的合法物资。Person27 嫌疑在此被完美反向洗白！
          </p>
          <p class="mt-1 text-closure">
            🚨 <b>铁证图腾锁死</b>：而整个全景社交资产流，最终以 100% 的极高数学纯度，无处可逃地全部收敛汇聚指向了唯一的、被极少数人故意垄断持有的特异性核心物证——<strong class="荧光高亮-图腾">【秘密黄色接头提袋】</strong>！
          </p>
          <span class="blink-action">👉 鼠标左键点击左图中的【黄色提袋图腾】节点，下钻查阅第四层级像素级照片物证链！</span>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import { useDashboardStore } from '../../store/dashboard'
import * as echarts from 'echarts'

const store = useDashboardStore()
const sankeyRef = ref(null)
let myChart = null

const renderSankey = () => {
  if (!sankeyRef.value) return
  if (myChart) myChart.dispose()

  myChart = echarts.init(sankeyRef.value, 'dark')

  const nodes = [{ name: '40名候选人' }, { name: '免费礼品背景' }, { name: '秘密组织暗号' }, { name: '黄色提袋图腾' }]

  // 根据排除进度计算流向流量
  let noiseFlow = store.excludedItems.length >= 3 ? 5 : store.excludedItems.length === 0 ? 50 : 25
  let secretFlow = 35

  const links = [
    { source: '40名候选人', target: '免费礼品背景', value: noiseFlow },
    { source: '40名候选人', target: '秘密组织暗号', value: secretFlow },
    { source: '秘密组织暗号', target: '黄色提袋图腾', value: secretFlow }
  ]

  myChart.setOption({
    backgroundColor: 'transparent',
    series: [{
      type: 'sankey', layout: 'none',
      data: nodes, links: links,
      nodeWidth: 14, nodeGap: 18,
      focusNodeAdjacency: 'allEdges',
      itemStyle: { borderWidth: 1, borderColor: 'rgba(255,255,255,0.1)' },
      lineStyle: { color: 'source', curveness: 0.5, opacity: 0.25 }
    }]
  })

  // 级联下钻第四层级独立子窗
  myChart.on('click', (params) => {
    if (params.name === '黄色提袋图腾' || params.name === '秘密组织暗号') {
      if (store.excludedItems.length >= 3) {
        store.isFourthLayerActive = true
      } else {
        alert("🔒 深度钻取被拦截：请先在上方漏斗中勾选排除全部大众普及小礼品，使情报去噪纯度达标！")
      }
    }
  })
}

watch(() => store.excludedItems, renderSankey, { deep: true })
onMounted(renderSankey)
</script>

<style scoped>
.sankey-wrapper { display: flex; flex-direction: column; height: 100%; }
.sankey-header { display: flex; justify-content: space-between; align-items: center; }
.glow-pill { font-size: 10px; background: rgba(191,90,242,0.12); color: var(--accent-totem); padding: 2px 8px; border-radius: 4px; font-weight: bold; border: 1px solid rgba(191,90,242,0.2); }
.sankey-body-layout { display: grid; grid-template-columns: 1.25fr 1fr; gap: 16px; flex: 1; min-height: 0; margin-top: 10px; }
.sankey-chart-viewport { height: 100%; min-height: 200px; }

/* 🎬 HUD 情报解析研判展示舱样式重塑 */
.sankey-interactive-hud { background: rgba(255,255,255,0.01); border: 1px solid rgba(255,255,255,0.03); padding: 14px; border-radius: 10px; font-size: 11.5px; color: #8E8E93; line-height: 1.55; display: flex; flex-direction: column; }
.sankey-interactive-hud h5 { margin: 0 0 8px 0; font-size: 12.5px; color: #E5E5EA; font-weight: 500; }
.hud-status-box { padding: 12px; border-radius: 6px; border: 1px solid rgba(255,255,255,0.02); flex: 1; display: flex; flex-direction: column; justify-content: center; }
.hud-status-box p { margin: 0; }
.mt-2 { margin-top: 8px; }
.mt-1 { margin-top: 6px; }

.status-waiting { background: rgba(255, 59, 48, 0.03); border-color: rgba(255, 59, 48, 0.08); }
.status-progress { background: rgba(255, 214, 10, 0.02); border-color: rgba(255, 214, 10, 0.08); color: #E5E5EA; }
.status-success { background: rgba(48, 209, 88, 0.03); border-color: rgba(48, 209, 88, 0.08); }

.text-warning { color: #FFD60A; }
.success-txt { color: #30D158; font-weight: bold; font-size: 13px; }
.text-closure { color: #E5E5EA; font-size: 11px; line-height: 1.5; }
.text-closure b { color: #FFF; }

.blink-action { display: inline-block; margin-top: 12px; color: var(--accent-truth); font-weight: bold; animation: pulse 2s infinite; cursor: pointer; line-height: 1.4; }
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }
</style>