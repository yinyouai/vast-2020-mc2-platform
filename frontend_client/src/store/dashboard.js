import { defineStore } from 'pinia'
import axios from 'axios'

const API_BASE = 'http://localhost:5000/api'

export const useDashboardStore = defineStore('dashboard', {
  state: () => ({
    scoreThreshold: 0.25,        // 全局动态置信度阈值 (由层级二滑块控制) [cite: 491]
    selectedPersonId: 'Person3', // 当前锁定的追踪嫌疑人 (默认初始化为黑客成员) [cite: 491]
    selectedImageId: 'Person3_1', // 当前在画布中正在被审查的图片主键ID [cite: 491]
    selectedReviewContext: null,
    cachedReviewTargets: [],
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

    selectReviewTarget({ personId, itemName, intensity = 0 }) {
      this.selectPerson(personId)
      this.selectedReviewContext = {
        personId,
        itemName,
        intensity,
        source: 'cluster-heatmap'
      }

      const existing = this.cachedReviewTargets.find((item) => item.id === personId)
      const target = {
        rank: `P${this.cachedReviewTargets.length + 1}`,
        id: personId,
        source: 'cluster',
        status: 'unreviewed',
        priority: intensity >= 3 ? '高' : '低',
        risk: intensity >= 3 ? 'high' : 'low',
        conflictScore: Math.min(0.95, 0.28 + Number(intensity || 0) * 0.16),
        machineLabel: `${itemName || '未知物品'} / 聚类选择`,
        humanLabel: itemName || '待选择标签',
        caption: `来自聚类矩阵的选择：${personId} 与 ${itemName || '未知物品'} 的关联强度为 ${intensity}。`,
        textComment: `Cluster drill-down note: ${personId} was selected because ${itemName || 'an item'} appeared in the co-occurrence matrix.`,
        semanticKeywords: [personId, itemName || 'unknown item', `strength ${intensity}`],
        semanticSignal: intensity >= 3 ? '高强度共现' : '低强度对照',
        semanticConflict: intensity > 0 ? '矩阵提示存在共现，需要人工核对文本和图像是否一致。' : '矩阵无明显信号，可作为背景噪声对照。',
        verdict: '等待人工复核确认，可手动调整标签后再标记为已确认或已修正。',
        note: '聚类选择'
      }

      if (existing) {
        Object.assign(existing, target, { rank: existing.rank, status: existing.status, humanLabel: existing.humanLabel })
      } else {
        this.cachedReviewTargets.push(target)
      }
    },

    updateReviewTarget(personId, patch) {
      const target = this.cachedReviewTargets.find((item) => item.id === personId)
      if (target) Object.assign(target, patch)
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
