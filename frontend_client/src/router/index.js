import { createRouter, createWebHistory } from 'vue-router'
import ModelAuditingView from '../views/ModelAuditingView.vue'
import DataExplorationView from '../views/DataExplorationView.vue'
import CommunityClusteringView from '../views/CommunityClusteringView.vue'
import TotemFilterView from '../views/TotemFilterView.vue'
import CyberForensicsView from '../views/CyberForensicsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', redirect: '/task1_auditing' },
    {
      path: '/task1_auditing',
      name: 'task1_auditing',
      component: ModelAuditingView,
      meta: { depth: 1, kicker: 'Layer 01', title: '模型不确定性审计' }
    },
    {
      path: '/task2_correction',
      name: 'task2_correction',
      component: DataExplorationView,
      meta: { depth: 2, kicker: 'Layer 02', title: '人工复核与图文校准' }
    },
    {
      path: '/task3_clustering',
      name: 'task3_clustering',
      component: CommunityClusteringView,
      meta: { depth: 3, kicker: 'Layer 03', title: '嫌疑群体共现聚类' }
    },
    {
      path: '/task4_totem',
      name: 'task4_totem',
      component: TotemFilterView,
      meta: { depth: 4, kicker: 'Layer 04', title: '公共物证过滤与暗号锁定' }
    },
    {
      path: '/task5_verdict',
      name: 'task5_verdict',
      component: CyberForensicsView,
      meta: { depth: 5, kicker: 'Layer 05', title: '社交隔离验证与最终定案' }
    }
  ]
})

export default router
