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
      meta: {
        depth: 1,
        kicker: '第 01 层',
        title: '模型不确定性审计',
        summary: '先把自动识别里的误报和漏报噪声压下去，后续人工复核和聚类分析才不会被错误证据带偏。',
        storyTitle: '第一层的目标不是找答案，而是先判断模型到底能不能信。',
        storySummary: '这一层决定整条证据链的干净程度。阈值一旦调得过低，会把公共物品错判成高风险物证；调得过高，又可能丢掉关键线索。'
      }
    },
    {
      path: '/task2_correction',
      name: 'task2_correction',
      component: DataExplorationView,
      meta: {
        depth: 2,
        kicker: '第 02 层',
        title: '人工复核与图文校准',
        summary: '将模型预测、文本语义和人工判断放在同一个工作面板上，修复最关键的分类偏差。',
        storyTitle: '第二层把“机器猜测”转化为“可追责的人类判断”。',
        storySummary: '参考优秀参赛作品的做法，纠错不应只看一张图，而应同时查看候选标签、文本上下文和后续导出的修正结果。'
      }
    },
    {
      path: '/task3_clustering',
      name: 'task3_clustering',
      component: CommunityClusteringView,
      meta: {
        depth: 3,
        kicker: '第 03 层',
        title: '人-物共现聚类分析',
        summary: '把 40 个目标和关键物品重新排序，区分公共噪声和真正值得追踪的小团体结构。',
        storyTitle: '第三层开始从局部纠错，转向整体结构识别。',
        storySummary: '优秀分析并不是只找到“谁有某个物品”，而是解释为什么某些物品只集中出现在某一小组内部，而另一些物品只是会场普遍分发。'
      }
    },
    {
      path: '/task4_totem',
      name: 'task4_totem',
      component: TotemFilterView,
      meta: {
        depth: 4,
        kicker: '第 04 层',
        title: '暗号物证过滤与收敛',
        summary: '逐步剔除覆盖率过高的公共物品，让真正具有群体识别价值的“暗号物证”浮现出来。',
        storyTitle: '第四层的重点是证明：真正的群体特征不是“大家都有”，而是“只有他们稳定共有”。',
        storySummary: '参考往届强队的思路，判断 totem 不能只看共享人数，还要结合每个人出现次数是否足够稳定，以及该物品是否能形成闭合的小群体。'
      }
    },
    {
      path: '/task5_verdict',
      name: 'task5_verdict',
      component: CyberForensicsView,
      meta: {
        depth: 5,
        kicker: '第 05 层',
        title: '社交隔离验证与最终定案',
        summary: '将线下物证收敛结果与线上社交隔离模式结合，验证该群体是否具备协同行动却刻意规避公开互动的特征。',
        storyTitle: '最后一层要把“共同持有物证”提升为“有组织协同行动”的叙事闭环。',
        storySummary: '只有当线下同物证收敛与线上异常沉默同时出现时，才能更有说服力地支撑最终嫌疑群体结论。'
      }
    }
  ]
})

export default router
