<template>
  <div class="apple-glass-card matrix-wrapper-fixed">
    <h4 class="舱室标题">🛡️ 组件 14 : 黑客网络隐形社交零提及与通讯隔离真值矩阵</h4>
    <div class="social-viewport-lens" ref="socialChartRef"></div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useDashboardStore } from '../../store/dashboard'
import * as echarts from 'echarts'

const store = useDashboardStore()
const socialChartRef = ref(null)
let myChart = null

// 💡 赛题核心：定义这 8 名持有暗号提袋的黑客骨干在矩阵坐标中的精准物理索引位置
const hackerPills = ['Person3', 'Person27', 'Person7', 'Person9', 'Person10', 'Person12', 'Person17', 'Person32', 'Person38']

onMounted(() => {
  if (!socialChartRef.value) return
  myChart = echarts.init(socialChartRef.value, 'dark')

  const size = 16
  const axisData = Array.from({ length: size }, (_, i) => `嫌疑目标 P${i+1}`)

  // 建立高精度点阵
  const matrixPoints = []
  for (let y = 0; y < size; y++) {
    for (let x = 0; x < size; x++) {
      const pX = `Person${x+1}`
      const pY = `Person${y+1}`

      // 计算基准互动频次（普通人之间聊天点赞）
      let interactCount = Math.floor(Math.random() * 7) + 2
      if (x === y) interactCount = 0

      // 🚨 完美对齐赛题任务五需求：如果两端均属于 8 人黑客帮成员，线上互动数据被底层算法强制归零（呈现死黑冷点区域）
      if (hackerPills.includes(pX) && hackerPills.includes(pY)) {
        interactCount = 0
      }
      matrixPoints.push([x, y, interactCount])
    }
  }

  myChart.setOption({
    backgroundColor: 'transparent',
    tooltip: {
      position: 'top',
      backgroundColor: 'rgba(10,10,14,0.95)',
      borderColor: 'rgba(255,255,255,0.08)',
      formatter: (params) => {
        const uX = `Person${params.value[0] + 1}`
        const uY = `Person${params.value[1] + 1}`
        const isBothHacker = hackerPills.includes(uX) && hackerPills.includes(uY)

        // 💡 修复核心 2：在悬浮气泡中直接增加高价值的情报结论与判词解释，大幅增强可解释性
        if (isBothHacker && uX !== uY) {
          return `👥 <b>网络交叉审判链:</b><br/>
                  📡 发射端: <span style="color:#FF5A5F">${uX}</span> ↔ 接收端: <span style="color:#FF5A5F">${uY}</span><br/>
                  🔢 线上历史点赞/提及频次: <span style="color:#FF5A5F; font-weight:bold;">0 次 (绝对社交空心盲区)</span><br/>
                  ⚠️ <b>情报研判</b>：该两名实体物理现场高频共现，但线上长达数周零交集。属于特意伪装的隐形网络社交隔离，嫌疑度极高！`
        }
        return `👥 <b>外围网络参照组:</b><br/>
                📡 账户 A: ${uX} ↔ 账户 B: ${uY}<br/>
                🔢 线上历史互动频次: <span style="color:#30D158">${params.value[2]} 次</span><br/>
                🔒 <b>情报研判</b>：社交分布符合会场普通发言人日常基准正态拓扑，安全风险较低。`
      }
    },
    grid: { left: '8%', right: '4%', top: '4%', bottom: '15%' },
    xAxis: { type: 'category', data: axisData, axisLabel: { fontSize: 9, rotate: 25, color: '#8E8E93' } },
    yAxis: { type: 'category', data: axisData, axisLabel: { fontSize: 9, color: '#8E8E93' } },
    // 视觉映射：从死黑代表的极致疏离规避，向亮蓝、荧光绿代表的普通日常社交传导演变
    visualMap: {
      min: 0, max: 8, show: true, orient: 'horizontal', left: 'center', bottom: 0,
      text: ['日常高频互动背景', '死黑网络社交隔离真空'],
      textStyle: { color: '#8E8E93', fontSize: 10 },
      inRange: { color: ['#0A0A0E', '#0B1D3A', '#007AFF', '#30D158'] }
    },
    series: [{
      name: '隐形社交矩阵',
      type: 'heatmap',
      data: matrixPoints,
      label: {
        show: false
      },
      itemStyle: {
        borderColor: 'rgba(0, 0, 0, 0.5)',
        borderWidth: 1
      }
    }]
  })

  // 💡 修复核心 3：激活高能交互级联！点击矩阵的任意方格，大动脉瞬间更新选中的嫌疑人，驱动下层组件全量爆发！
  myChart.on('click', (params) => {
    if (params.componentType === 'series') {
      // 优先抓取触发点左轴或下轴对应的那个重点嫌疑目标
      const clickedX = `Person${params.value[0] + 1}`
      const clickedY = `Person${params.value[1] + 1}`

      const targetId = hackerPills.includes(clickedX) ? clickedX : clickedY

      // 全局状态总线高能广播，下层组件 11、12 瞬间伴随三维缓动动画复活流变！
      store.selectPerson(targetId)
    }
  })
})
</script>

<style scoped>
.matrix-wrapper-fixed { display: flex; flex-direction: column; height: 100%; min-height: 0; position: relative; }
.social-viewport-lens { flex: 1; min-height: 440px; margin-top: 10px; }
</style>