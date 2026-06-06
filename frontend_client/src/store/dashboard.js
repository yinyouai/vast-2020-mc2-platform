import { defineStore } from 'pinia'
import axios from 'axios'

export const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:5000/api'
export const STATIC_BASE = API_BASE.replace(/\/api$/, '')
let thresholdTimer

export const useDashboardStore = defineStore('dashboard', {
  state: () => ({
    scoreThreshold: 0.25,
    matrixDataSource: 'corrected',
    selectedPersonId: '',
    selectedImageId: '',
    selectedReviewContext: null,
    excludedItems: [],
    orderedSuspects: [],
    orderedItems: [],
    heatmapMatrixData: [],
    rawMatrixSnapshot: { suspects: [], items: [], cells: [] },
    correctedMatrixSnapshot: { suspects: [], items: [], cells: [] },
    modelEvaluationData: {},
    modelAudit: {},
    analysisSummary: null,
    reviewQueue: [],
    activeTotem: '',
    hackerGroup: [],
    finalEvidence: [],
    candidateRankings: [],
    selectedCandidateLabel: '',
    isFourthLayerActive: false,
    isLoading: false,
    correctionInFlight: '',
    correctionMessage: '',
    errorMessage: ''
  }),

  getters: {
    selectedEvidence(state) {
      return state.finalEvidence.find((item) => item.person_id === state.selectedPersonId) || null
    },
    selectedReviewItem(state) {
      return state.reviewQueue.find((item) => item.id === state.selectedReviewContext?.id) || null
    }
  },

  actions: {
    setScoreThreshold(value) {
      this.scoreThreshold = Number(value)
      window.clearTimeout(thresholdTimer)
      thresholdTimer = window.setTimeout(() => {
        if (this.matrixDataSource === 'raw') this.fetchHeatmapMatrix()
        this.fetchMatrixSnapshots()
      }, 120)
    },

    setMatrixDataSource(source) {
      this.matrixDataSource = source === 'raw' ? 'raw' : 'corrected'
      this.fetchHeatmapMatrix()
    },

    selectPerson(personId, imageId = '') {
      this.selectedPersonId = personId
      const evidence = this.finalEvidence.find((item) => item.person_id === personId)
      this.selectedImageId = imageId || evidence?.primary_image_id || ''
    },

    selectReviewTarget(item) {
      this.selectedReviewContext = item
      this.selectPerson(item.person_id, item.image_id)
    },

    toggleItemExclusion(itemName) {
      const index = this.excludedItems.indexOf(itemName)
      if (index >= 0) this.excludedItems.splice(index, 1)
      else this.excludedItems.push(itemName)
      this.fetchHeatmapMatrix()
      this.fetchMatrixSnapshots()
    },

    setExcludedItems(items) {
      this.excludedItems = [...new Set(items)]
      this.fetchHeatmapMatrix()
      this.fetchMatrixSnapshots()
    },

    async fetchAnalysisSummary() {
      try {
        const response = await axios.get(`${API_BASE}/analysis_summary`)
        if (response.data.status !== 'success') return
        const summary = response.data.data
        this.analysisSummary = summary
        this.activeTotem = summary.final.totem
        this.hackerGroup = summary.final.group
        this.finalEvidence = summary.final.evidence
        this.candidateRankings = summary.candidate_rankings
        if (!this.selectedCandidateLabel) {
          this.selectedCandidateLabel = summary.final.totem
        }
        if (!this.selectedPersonId && this.hackerGroup.length) {
          this.selectPerson(this.hackerGroup[0])
        }
      } catch (error) {
        this.errorMessage = '无法获取分析摘要'
        console.error(this.errorMessage, error)
      }
    },

    selectCandidate(label) {
      this.selectedCandidateLabel = label
    },

    async fetchHeatmapMatrix() {
      this.isLoading = true
      try {
        const response = await axios.post(`${API_BASE}/distribution_matrix`, {
          score_threshold: this.scoreThreshold,
          excluded_items: this.excludedItems,
          data_source: this.matrixDataSource
        })
        if (response.data.status === 'success') {
          this.orderedSuspects = response.data.ordered_suspects
          this.orderedItems = response.data.ordered_items
          this.heatmapMatrixData = response.data.matrix_data
        }
      } catch (error) {
        this.errorMessage = '无法获取人物-物品矩阵'
        console.error(this.errorMessage, error)
      } finally {
        this.isLoading = false
      }
    },

    async fetchModelEvaluation() {
      try {
        const response = await axios.get(`${API_BASE}/model_evaluation`)
        if (response.data.status === 'success') {
          this.modelEvaluationData = response.data.data
          this.modelAudit = response.data.audit
        }
      } catch (error) {
        this.errorMessage = '无法获取模型审计数据'
        console.error(this.errorMessage, error)
      }
    },

    async fetchMatrixSnapshots() {
      try {
        const [rawResponse, correctedResponse] = await Promise.all([
          axios.post(`${API_BASE}/distribution_matrix`, {
            score_threshold: this.scoreThreshold,
            excluded_items: this.excludedItems,
            data_source: 'raw'
          }),
          axios.post(`${API_BASE}/distribution_matrix`, {
            excluded_items: this.excludedItems,
            data_source: 'corrected'
          })
        ])
        if (rawResponse.data.status === 'success') {
          this.rawMatrixSnapshot = {
            suspects: rawResponse.data.ordered_suspects,
            items: rawResponse.data.ordered_items,
            cells: rawResponse.data.matrix_data
          }
        }
        if (correctedResponse.data.status === 'success') {
          this.correctedMatrixSnapshot = {
            suspects: correctedResponse.data.ordered_suspects,
            items: correctedResponse.data.ordered_items,
            cells: correctedResponse.data.matrix_data
          }
        }
      } catch (error) {
        console.error('无法获取矩阵对照快照', error)
      }
    },

    async fetchReviewQueue() {
      try {
        const response = await axios.get(`${API_BASE}/review_queue`)
        if (response.data.status === 'success') {
          this.reviewQueue = response.data.data
          if (!this.selectedReviewContext && this.reviewQueue.length) {
            this.selectReviewTarget(this.reviewQueue[0])
          }
        }
      } catch (error) {
        this.errorMessage = '无法获取人工复核队列'
        console.error(this.errorMessage, error)
      }
    },

    async submitCorrection(item, patch) {
      this.correctionInFlight = item.id
      this.correctionMessage = ''
      const nextStatus = patch.status || item.status
      let action = 'confirm'
      let newLabel = patch.humanLabel || item.corrected_label
      if (item.status === 'rejected' && nextStatus === 'confirmed') {
        action = 'restore'
        newLabel = patch.humanLabel || item.predicted_label
      } else if (nextStatus === 'rejected') {
        action = 'reject'
      } else if (item.box_id === -1 || item.predicted_label === '未检出') {
        action = 'add'
      } else if (newLabel && newLabel !== item.predicted_label) {
        action = 'modify'
      }

      try {
        await axios.post(`${API_BASE}/update_label`, {
          person_id: item.person_id,
          image_id: item.image_id,
          box_id: item.box_id,
          action,
          new_label: newLabel,
          difficult: Boolean(patch.difficult ?? item.difficult),
          note: patch.note || item.reason || ''
        })
        this.correctionMessage = `${item.image_id} 已写入校正层并完成重算`
        await Promise.all([
          this.fetchAnalysisSummary(),
          this.fetchReviewQueue(),
          this.fetchHeatmapMatrix(),
          this.fetchMatrixSnapshots(),
          this.fetchModelEvaluation()
        ])
      } catch (error) {
        this.errorMessage = '复核操作保存失败'
        throw error
      } finally {
        this.correctionInFlight = ''
      }
    },

    async initialize() {
      this.isLoading = true
      await Promise.all([
        this.fetchAnalysisSummary(),
        this.fetchModelEvaluation(),
        this.fetchReviewQueue(),
        this.fetchMatrixSnapshots()
      ])
      await this.fetchHeatmapMatrix()
      this.isLoading = false
    }
  }
})
