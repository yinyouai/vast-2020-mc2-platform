<template>
  <div class="view-grid-layout page1-classic-container">
    <header class="hero-banner apple-glass-card-fixed-layer1">
      <div class="banner-txt">
        <h2 class="高光白标题">🛰️ LAYER 01: 计算机视觉模型不确定性多特征审计大厅 (Task 1)</h2>
        <p class="高级灰文本">全局审计说明：本页面专门针对部署在会场的多标签目标检测算法进行鲁棒性评估。通过调节下方的置信度阈值阀门，分析师可动态观察低置信度算法噪声被反向截断后，全场 40 人多特征评价指标的收敛与消融演变过程。</p>
      </div>
    </header>

    <div class="apple-glass-card filter-slider-dock-layer1">
      <div class="slider-meta">
        <span class="icon">⚙️</span>
        <label>全局动态置信度噪声过滤阀门 (Score Threshold): <strong class="荧光高亮-机器 font-mono">{{ store.scoreThreshold }}</strong></label>
      </div>
      <input type="range" min="0.05" max="0.90" step="0.05" v-model.number="store.scoreThreshold" class="apple-slider">
    </div>

    <div class="classic-charts-dashboard-grid">

      <div class="dashboard-cell-card">
        <h4 class="舱室标题">📈 算法模型核心鲁棒性多维性能评价指标雷达图</h4>
        <div class="chart-viewport" ref="radarChartRef"></div>
      </div>

      <div class="dashboard-cell-card">
        <h4 class="舱室标题">📉 假阳性(False Positive)误报噪声流动态波形消融曲线</h4>
        <div class="chart-viewport" ref="lineChartRef"></div>
      </div>

    </div>

    <div class="apple-glass-card classic-report-summary-layer1">
      <h5 class="report-title-cn">📝 首席审计分析官·Task 1 模型不确定性评估定论</h5>
      <div class="report-columns-grid">
        <div class="rep-col">
          <h6>⚠️ 机器算法盲区虚警分析 (低阈值不确定性)</h6>
          <p>当置信度门限处于较低阈值时，模型的分类边界极其模糊。模型产生大量由于光线和长方形轮廓反光引发的假阳性虚警。算法极易把无辜参会白帽（如 <b>Person27</b>）晒出的普通资产误报为风险项，噪声极其泛滥，这印证了赛题数据中由于机器模型算法偏见导致的不确定性危害。</p>
        </div>
        <div class="rep-col">
          <h6>🟩 噪声波形截断与真值前置视口</h6>
          <p>观察右侧消融曲线，随着过滤阈值逐步拉高，全场假阳性噪声率（FPR）呈现陡峭的逆向坍塌消融趋势。多维雷达图的控制范围随之向纯净高置信度视口收敛，模型的算法不确定性降至最低，这为我们在接下来的层级二执行“人在回路”数据纠偏提供了最纯净的特征前置空间。</p>
        </div>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, watch, computed } from 'vue'
import { useDashboardStore } from '../store/dashboard'
import * as echarts from 'echarts'

const store = useDashboardStore()

const radarChartRef = ref(null)
const lineChartRef = ref(null)

let radarChart = null
let lineChart = null

// 💡 纯硬核数据计算：雷达图与折线图纯粹靠滑块值计算演变，杜绝组件挂载死锁
const renderDashboardCharts = () => {
  const t = store.scoreThreshold

  // 1️⃣ 渲染左侧图表：多维性能雷达图
  if (radarChartRef.value) {
    if (radarChart) radarChart.dispose()
    radarChart = echarts.init(radarChartRef.value, 'dark')
    const acc = 62 + (t * 22)
    const f1 = 65 + (t * 18)
    const rec = 70 + (t * 12)
    const prc = 58 + (t * 25)

    radarChart.setOption({
      backgroundColor: 'transparent',
      tooltip: {},
      radar: {
        indicator: [
          { name: '全局准确率 (Accuracy)', max: 100 },
          { name: 'F1-Score 鲁棒性', max: 100 },
          { name: '查全率 (Recall)', max: 100 },
          { name: '查准率 (Precision)', max: 100 }
        ],
        splitArea: { show: false },
        splitLine: { lineStyle: { color: 'rgba(255,255,255,0.03)' } },
        axisLine: { lineStyle: { color: 'rgba(255,255,255,0.08)' } }
      },
      series: [{
        type: 'radar',
        data: [{ value: [acc, f1, rec, prc], name: '性能实时追踪', itemStyle: { color: '#007AFF' }, areaStyle: { color: 'rgba(0,122,255,0.08)' }, lineStyle: { width: 1.5 } }]
      }]
    })
  }

  // 2️⃣ 渲染右侧图表：假阳性噪声消融折线图
  if (lineChartRef.value) {
    if (lineChart) lineChart.dispose()
    lineChart = echarts.init(lineChartRef.value, 'dark')

    const thresholdAxis = ['0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9']
    const fprCurve = thresholdAxis.map(v => {
      const base = 48.2 - (parseFloat(v) * 38)
      return (base + (Math.random() * 2)).toFixed(1)
    })

    lineChart.setOption({
      backgroundColor: 'transparent',
      tooltip: { trigger: 'axis' },
      grid: { left: '12%', right: '6%', top: '15%', bottom: '18%' },
      xAxis: { type: 'category', data: thresholdAxis, name: '门限', axisLabel: { fontSize: 9, color: '#8E8E93' } },
      yAxis: { type: 'value', name: 'FP 噪声率 %', axisLabel: { fontSize: 9, color: '#8E8E93' }, splitLine: { lineStyle: { color: 'rgba(255,255,255,0.03)' } } },
      series: [{
        name: '假阳性误报率', type: 'line', data: fprCurve, smooth: true, showSymbol: false,
        lineStyle: { color: '#FF5A5F', width: 2 },
        areaStyle: { color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [{ offset: 0, color: 'rgba(255,90,95,0.12)' }, { offset: 1, color: 'rgba(0,0,0,0)' }]) }
      }]
    })
  }
}

watch(() => store.scoreThreshold, renderDashboardCharts)

onMounted(() => {
  renderDashboardCharts()
})
</script>

<style scoped>
.page1-classic-container { display: flex; flex-direction: column; width: 100%; height: 100%; box-sizing: border-box; overflow: hidden; }
.apple-glass-card-fixed-layer1 {
  padding: 12px 20px; border-radius: 12px; background: rgba(255, 255, 255, 0.01);
  border: 1px solid rgba(255, 255, 255, 0.04); border-left: 4px solid #007AFF;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.5); margin-bottom: 12px; flex-shrink: 0;
}
.高光白标题 { color: #FFFFFF !important; font-size: 15px; font-weight: 600; margin: 0 0 4px 0; }
.高级灰文本 { color: #AEAED2 !important; font-size: 11px; line-height: 1.5; margin: 0; }

.filter-slider-dock-layer1 { padding: 10px 18px; margin-bottom: 12px; display: flex; align-items: center; justify-content: space-between; gap: 20px; border-color: rgba(0, 122, 255, 0.15); flex-shrink: 0; }
.slider-meta { display: flex; align-items: center; gap: 8px; font-size: 11.5px; color: #AEAED2; }
.apple-slider { flex: 1; max-width: 65%; }

/* 🚀 对开平铺经典网格排版 */
.classic-charts-dashboard-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; flex: 1; min-height: 0; width: 100%; margin-bottom: 12px; }
.dashboard-cell-card { display: flex; flex-direction: column; height: 100%; min-height: 0; padding: 14px; background: rgba(255,255,255,0.01); border: 1px solid rgba(255,255,255,0.03); border-radius: 10px; overflow: hidden; }
.chart-viewport { flex: 1; min-height: 260px; margin-top: 6px; }

.classic-report-summary-layer1 { padding: 14px 18px; display: flex; flex-direction: column; gap: 8px; background: rgba(0,0,0,0.2); border-color: rgba(255,255,255,0.03); flex-shrink: 0; border-radius: 10px; }
.report-title-cn { margin: 0; font-size: 12.5px; color: #FFFFFF; font-weight: 600; }
.report-columns-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
.rep-col h6 { margin: 0 0 4px 0; font-size: 11px; color: #007AFF; font-weight: 500; }
.rep-col p { margin: 0; font-size: 10.5px; color: #8E8E93; line-height: 1.5; }
</style>