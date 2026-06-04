<template>
  <section class="view-grid-layout">
    <div class="page-intro">
      <div>
        <p class="eyebrow">Task 3 / Co-occurrence Clustering</p>
        <h3>从“人-物”共现里寻找异常小团体</h3>
        <p>
          热力矩阵将 40 名目标与关键物品重新排序。普通会场物品会形成大面积背景噪声，而核心嫌疑组会在特定物证上高度收敛。
        </p>
      </div>
      <button class="primary-btn" @click="$router.push('/task4_totem')">进入物证过滤</button>
    </div>

    <div class="cluster-layout">
      <ClusterHeatmap />

      <aside class="panel insight-panel">
        <div class="panel-header">
          <div>
            <h4 class="panel-title">聚类读数</h4>
            <p class="panel-subtitle">异常结构会在后续过滤层继续被验证。</p>
          </div>
        </div>

        <div class="insight-card">
          <span>背景噪声</span>
          <strong>公共物品覆盖面过大</strong>
          <p>便签、玩具和普通礼品覆盖大量参会者，不能直接作为定案证据。</p>
        </div>
        <div class="insight-card high">
          <span>核心线索</span>
          <strong>黄色接头包高度集中</strong>
          <p>核心组候选在同一暗号物上形成收敛，值得进入反向过滤。</p>
        </div>
        <div class="insight-card">
          <span>操作建议</span>
          <strong>点击热力单元回钻</strong>
          <p>选中目标后会回到第 2 层复核画布，检查其图文证据链。</p>
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
  border-radius: var(--radius);
  background: rgba(255, 255, 255, 0.035);
}

.insight-card + .insight-card {
  margin-top: 12px;
}

.insight-card.high {
  border-color: rgba(244, 201, 93, 0.34);
  background: rgba(244, 201, 93, 0.08);
}

.insight-card span {
  color: var(--subtle);
  font-size: 0.78rem;
  font-weight: 800;
}

.insight-card strong {
  display: block;
  margin: 8px 0;
}

.insight-card p {
  margin: 0;
  color: var(--muted);
  line-height: 1.55;
}

@media (max-width: 1040px) {
  .cluster-layout {
    grid-template-columns: 1fr;
  }
}
</style>
