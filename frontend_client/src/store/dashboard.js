import { defineStore } from 'pinia'
import axios from 'axios'

const API_BASE = 'http://localhost:5000/api'

export const useDashboardStore = defineStore('dashboard', {
  state: () => ({
    scoreThreshold: 0.25,        // 全局动态置信度阈值 (由层级二滑块控制) [cite: 491]
    selectedPersonId: 'Person3', // 当前锁定的追踪嫌疑人 (默认初始化为黑客成员) [cite: 491]
    selectedImageId: 'Person3_1', // 当前在画布中正在被审查的图片主键ID [cite: 491]
    excludedItems: [],           // 被分析师放逐的大众参会礼品黑名单 (由层级四控制) [cite: 491]

    // 异步分布式数据缓存
    orderedSuspects: [],
    orderedItems: [],
    heatmapMatrixData: [],
    modelEvaluationData: {},
    isLoading: false,

      // 补充在 src/store/dashboard.js 的 state 内部
    activeTotem: 'yellowBag',      // 当前破译的秘密接头暗号图腾
    isFourthLayerActive: false,    // 第四层级深度下钻视窗开关
    hackerGroup: ['Person3', 'Person7', 'Person9', 'Person10', 'Person12', 'Person17', 'Person32', 'Person38', 'Person27']
  }),

  actions: {
    // 阈值滑动：通知全局并强制层次聚类重新洗牌
    setScoreThreshold(val) {
      this.scoreThreshold = val
      this.fetchHeatmapMatrix()
    },

    // 精准锁定嫌疑人：钻取级联，自动将层级二画布挂载为其首张多模态图片 [cite: 491]
    selectPerson(personId) {
      this.selectedPersonId = personId
      this.selectedImageId = `${personId}_1`
    },

    // 礼品黑名单过滤：强制矩阵削波 [cite: 491]
    toggleItemExclusion(itemName) {
      const idx = this.excludedItems.indexOf(itemName)
      if (idx > -1) {
        this.excludedItems.splice(idx, 1)
      } else {
        this.excludedItems.push(itemName)
      }
      this.fetchHeatmapMatrix()
    },

    // 🔌 异步调用 Flask: 拉取层次聚类矩阵
    async fetchHeatmapMatrix() {
      this.isLoading = true
      try {
        const res = await axios.post(`${API_BASE}/distribution_matrix`, {
          score_threshold: this.scoreThreshold,
          excluded_items: this.excludedItems
        })
        if (res.data.status === 'success') {
          this.orderedSuspects = res.data.ordered_suspects
          this.orderedItems = res.data.ordered_items
          this.heatmapMatrixData = res.data.matrix_data
        }
      } catch (err) {
        console.error("无法拉取后端层次聚类重排数据流:", err)
      } finally {
        this.isLoading = false
      }
    },

    // 🔌 异步调用 Flask: 拉取机器模型缺陷四分位数
    async fetchModelEvaluation() {
      try {
        const res = await axios.get(`${API_BASE}/model_evaluation`)
        if (res.data.status === 'success') {
          this.modelEvaluationData = res.data.data
        }
      } catch (err) {
        console.error("无法获取模型质量评估数据流:", err)
      }

    }
  }
})