import { defineStore } from 'pinia'
import axios from 'axios'
import { HACKER_LIST } from '../constants/forensics'

const API_BASE = 'http://localhost:5000/api'

export const useDashboardStore = defineStore('dashboard', {
  state: () => ({
    // ─── 全局控制 ───
    scoreThreshold: 0.25,
    selectedPersonId: 'Person3',
    selectedImageId: 'Person3_1',
    excludedItems: [],
    clusteringMethod: 'ward',          // 新增: 聚类方法选择

    // ─── 异步数据缓存 ───
    orderedSuspects: [],
    orderedItems: [],
    heatmapMatrixData: [],
    modelEvaluationData: {},
    isLoading: false,

    // ─── 网络图与照片 ───
    networkGraphData: null,            // 新增: 社交网络图数据
    photoClassificationData: null,     // 新增: 照片分组数据
    personPhotos: {},                  // 新增: 个人照片 URL 缓存

    // ─── 图腾与深层 ───
    activeTotem: 'yellowBag',
    isFourthLayerActive: false,
    hackerGroup: HACKER_LIST           // 现在引用集中式常量
  }),

  getters: {
    // 当前选中人物是否为黑客
    isSelectedHacker: (state) => HACKER_LIST.includes(state.selectedPersonId),

    // 排除进度百分比
    exclusionProgress: (state) => {
      const max = 4
      return Math.round((state.excludedItems.length / max) * 100)
    },

    // 去噪是否达标
    isDenoisingComplete: (state) => state.excludedItems.length >= 3
  },

  actions: {
    // ─── 阈值控制 ───
    setScoreThreshold(val) {
      this.scoreThreshold = val
      this.fetchHeatmapMatrix()
    },

    // ─── 人物选择 ───
    selectPerson(personId) {
      this.selectedPersonId = personId
      this.selectedImageId = `${personId}_1`
    },

    // ─── 物品排除 ───
    toggleItemExclusion(itemName) {
      const idx = this.excludedItems.indexOf(itemName)
      if (idx > -1) {
        this.excludedItems.splice(idx, 1)
      } else {
        this.excludedItems.push(itemName)
      }
      this.fetchHeatmapMatrix()
    },

    // ─── 聚类方法切换 ───
    setClusteringMethod(method) {
      this.clusteringMethod = method
      this.fetchHeatmapMatrix()
    },

    // ─── API: 获取层次聚类矩阵 ───
    async fetchHeatmapMatrix() {
      this.isLoading = true
      try {
        const res = await axios.post(`${API_BASE}/distribution_matrix`, {
          score_threshold: this.scoreThreshold,
          excluded_items: this.excludedItems,
          clustering_method: this.clusteringMethod
        })
        if (res.data.status === 'success') {
          this.orderedSuspects = res.data.ordered_suspects
          this.orderedItems = res.data.ordered_items
          this.heatmapMatrixData = res.data.matrix_data
        }
      } catch (err) {
        console.error('层次聚类数据拉取失败:', err)
      } finally {
        this.isLoading = false
      }
    },

    // ─── API: 获取模型评估数据 ───
    async fetchModelEvaluation() {
      try {
        const res = await axios.get(`${API_BASE}/model_evaluation`)
        if (res.data.status === 'success') {
          this.modelEvaluationData = res.data.data
        }
      } catch (err) {
        console.error('模型评估数据拉取失败:', err)
      }
    },

    // ─── API: 获取网络图数据 ───
    async fetchNetworkGraph() {
      try {
        const res = await axios.get(`${API_BASE}/network_graph`)
        if (res.data.status === 'success') {
          this.networkGraphData = res.data.data
        }
      } catch (err) {
        console.error('网络图数据拉取失败:', err)
      }
    },

    // ─── API: 获取照片分类数据 ───
    async fetchPhotoClassification() {
      try {
        const res = await axios.post(`${API_BASE}/photo_classification`, {
          score_threshold: this.scoreThreshold,
          excluded_items: this.excludedItems,
          clustering_method: this.clusteringMethod
        })
        if (res.data.status === 'success') {
          this.photoClassificationData = res.data.data
        }
      } catch (err) {
        console.error('照片分类数据拉取失败:', err)
      }
    },

    // ─── API: 获取人员照片列表 ───
    async fetchPersonPhotos() {
      try {
        const res = await axios.get(`${API_BASE}/person_photos`)
        if (res.data.status === 'success') {
          this.personPhotos = res.data.data
        }
      } catch (err) {
        console.error('人员照片数据拉取失败:', err)
      }
    }
  }
})
