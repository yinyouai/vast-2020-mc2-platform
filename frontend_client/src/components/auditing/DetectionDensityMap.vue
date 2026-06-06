<template>
  <div class="apple-glass-card component-wrapper">
    <h4 class="舱室标题">组件 3：原始 YOLO v2 检测框空间密度</h4>
    <div class="density-viewport" ref="densityChartRef"></div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'

const densityChartRef = ref(null)

onMounted(() => {
  if (!densityChartRef.value) return
  const chart = echarts.init(densityChartRef.value)

  // 生成空间核密度散点
  const points = Array.from({ length: 180 }, () => [
    Math.random() * 800,
    Math.random() * 600,
    Math.random()
  ])

  chart.setOption({
    backgroundColor: 'transparent',
    grid: { left: '4%', right: '4%', top: '4%', bottom: '4%' },
    xAxis: { show: false, min: 0, max: 800 },
    yAxis: { show: false, min: 0, max: 600 },
    // 💡 修复核心：改用散点发光特效，完美契合数值轴，并达成 Apple 荧光色彩质感
    series: [{
      type: 'scatter',
      data: points,
      symbolSize: function (data) {
        return data[2] * 20 + 5; // 动态大小映射不确定性
      },
      itemStyle: {
        color: new echarts.graphic.RadialGradient(0.4, 0.3, 1, [{
          offset: 0, color: 'rgba(223, 106, 106, 0.72)' // 误报高密度热点
        }, {
          offset: 1, color: 'rgba(47, 125, 246, 0.08)' // 渐变外扩
        }]),
        shadowBlur: 10,
        shadowColor: 'rgba(223, 106, 106, 0.28)'
      }
    }]
  })
})
</script>

<style scoped>
.component-wrapper { display: flex; flex-direction: column; height: 100%; }
.density-viewport {
  width: 100%;
  height: 210px;
  border: 1px solid rgba(53, 89, 138, 0.1);
  border-radius: 14px;
  background:
    linear-gradient(rgba(47, 125, 246, 0.05) 1px, transparent 1px),
    linear-gradient(90deg, rgba(47, 125, 246, 0.05) 1px, transparent 1px),
    linear-gradient(180deg, #ffffff, #f7fbff);
  background-size: 100% 42px, 42px 100%, 100% 100%;
}
</style>
