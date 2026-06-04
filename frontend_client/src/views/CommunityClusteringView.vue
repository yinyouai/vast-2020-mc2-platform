<template>
  <section class="view-grid-layout">
    <div class="page-intro">
      <div>
        <p class="eyebrow">任务 3 / 群体聚类</p>
        <h3>通过人-物共现矩阵重排，把“会场背景噪声”与“嫌疑群体结构”区分开来。</h3>
        <p>
          这一层不只是展示谁拥有什么物品，更重要的是解释哪些物品只在局部人群中密集共现。
          当矩阵出现窄而亮的块状结构时，往往意味着该物品具备更高的识别价值。
        </p>
        <div class="intro-pills">
          <span class="data-chip">矩阵重排</span>
          <span class="data-chip">群体结构</span>
          <span class="data-chip">异常共现</span>
        </div>
      </div>
      <button class="primary-btn" @click="$router.push('/task4_totem')">进入暗号过滤</button>
    </div>

    <div class="analysis-grid">
      <article class="analysis-card">
        <span>结构解读</span>
        <strong>公共物品会形成大面积浅色覆盖，而小群体暗号会形成高亮窄块。</strong>
        <p>这也是为什么我们不能凭“出现次数多”直接判断重要性，必须同时看分布范围是否收缩到少数目标内部。</p>
      </article>
      <article class="analysis-card">
        <span>参考启发</span>
        <strong>优秀作品会同时比较原始预测与修正结果之间的差异。</strong>
        <p>修正前后若某个物品只在少数人群中保留下来，就说明它更可能是稳定特征，而不是模型幻觉。</p>
      </article>
      <article class="analysis-card">
        <span>本页作用</span>
        <strong>为下一层筛选 totem 提供候选集合。</strong>
        <p>这一层先找出哪些物品有“形成小团体”的潜质，下一层再通过覆盖率和共享次数进一步排除公共物品。</p>
      </article>
    </div>

    <div class="cluster-layout">
      <ClusterHeatmap />

      <aside class="panel insight-panel">
        <div class="panel-header">
          <div>
            <h4 class="panel-title">聚类读数</h4>
            <p class="panel-subtitle">从大范围覆盖、局部高亮和钻取复核三个角度解释矩阵结构。</p>
          </div>
        </div>

        <div class="insight-card">
          <span>背景噪声</span>
          <strong>公共物品覆盖人数过广。</strong>
          <p>胸牌、笔记本或普通礼品往往横跨多数参与者，不能直接当成关键取证物证。</p>
        </div>
        <div class="insight-card high">
          <span>核心信号</span>
          <strong>黄色提袋在少数对象上形成明显收敛块。</strong>
          <p>这种“覆盖面窄但内部密度高”的模式，比单纯高频出现更接近暗号物证应有的结构特征。</p>
        </div>
        <div class="insight-card">
          <span>分析动作</span>
          <strong>点击矩阵单元可回到复核层验证样本。</strong>
          <p>这样可以把宏观结构与微观证据重新对齐，避免聚类结论脱离具体图像与文本上下文。</p>
        </div>
      </aside>
    </div>
  </section>
</template>

<script setup>
import ClusterHeatmap from '../components/targeting/ClusterHeatmap.vue'
</script>

<style scoped>
.cluster-layout {
  display: grid;
  grid-template-columns: minmax(0, 1.55fr) minmax(300px, 0.75fr);
  gap: 18px;
  min-height: 620px;
}

.insight-panel {
  align-self: stretch;
}

.insight-card {
  padding: 14px;
  border: 1px solid var(--border);
  border-radius: var(--radius-sm);
  background: rgba(255, 255, 255, 0.82);
}

.insight-card + .insight-card {
  margin-top: 12px;
}

.insight-card.high {
  border-color: rgba(240, 180, 76, 0.32);
  background: rgba(240, 180, 76, 0.1);
}

.insight-card span {
  color: var(--subtle);
  font-size: 0.78rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  text-transform: uppercase;
}

.insight-card strong {
  display: block;
  margin: 8px 0;
}

.insight-card p {
  margin: 0;
  color: var(--muted);
  line-height: 1.7;
}

@media (max-width: 1040px) {
  .cluster-layout {
    grid-template-columns: 1fr;
  }
}
</style>
