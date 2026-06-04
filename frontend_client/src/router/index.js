import { createRouter, createWebHistory } from 'vue-router'

const HomePage = () => import('../views/HomePage.vue')
const ModelAuditingView = () => import('../views/ModelAuditingView.vue')
const DataExplorationView = () => import('../views/DataExplorationView.vue')
const CommunityClusteringView = () => import('../views/CommunityClusteringView.vue')
const TotemFilterView = () => import('../views/TotemFilterView.vue')
const CyberForensicsView = () => import('../views/CyberForensicsView.vue')

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', component: HomePage, meta: { title: '首页' } },
    { path: '/task1_auditing', component: ModelAuditingView, meta: { depth: 1, title: '层级一: 算法不确定性审计' } },
    { path: '/task2_correction', component: DataExplorationView, meta: { depth: 2, title: '层级二: 多模态语义真值校准' } },
    { path: '/task3_clustering', component: CommunityClusteringView, meta: { depth: 3, title: '层级三: 嫌疑社群特征聚类' } },
    { path: '/task4_totem', component: TotemFilterView, meta: { depth: 4, title: '层级四: 秘密图腾反向排除' } },
    { path: '/task5_verdict', component: CyberForensicsView, meta: { depth: 5, title: '层级五: 黑客组织终极定案' } }
  ]
})

export default router
