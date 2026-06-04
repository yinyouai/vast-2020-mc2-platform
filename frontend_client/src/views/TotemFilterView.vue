<template>
  <section class="view-grid-layout">
    <div class="page-intro">
      <div>
        <p class="eyebrow">任务 4 / 暗号过滤</p>
        <h3>先排除所有“人人都可能有”的公共物品，再让真正的暗号物证自己浮出来。</h3>
        <p>
          这一层承接聚类结果，但进一步提出更严格的问题：某个物品即使共享人数较多，它是否真的只在目标团体中稳定出现？
          如果只是会场礼品，它就不应进入最终定案逻辑。
        </p>
        <div class="intro-pills">
          <span class="data-chip">覆盖率过滤</span>
          <span class="data-chip">候选收敛</span>
          <span class="data-chip">暗号稳定性</span>
        </div>
      </div>
    </div>

    <div class="analysis-grid">
      <article class="analysis-card">
        <span>筛选准则</span>
        <strong>共享人数只是第一步，更重要的是每个人是否多次稳定持有。</strong>
        <p>参考强队分析思路，真正的 totem 往往不仅共享于 8 人左右，而且每个人都具备足够多的出现次数，能构成稳定信号而非偶然碰撞。</p>
      </article>
      <article class="analysis-card">
        <span>对比价值</span>
        <strong>过滤前后结构若突然收紧，说明该物品具有判别力。</strong>
        <p>如果剔除公共物品后，只剩下某一小群体依然强共现，那么它就更可能是线下会合的符号而非随机背景。</p>
      </article>
      <article class="analysis-card">
        <span>当前假设</span>
        <strong>黄色提袋是更稳健的候选暗号物证。</strong>
        <p>因为它在剔除高覆盖物品后仍维持局部高密度收敛，这种“过滤后仍存在”的特征非常关键。</p>
      </article>
    </div>

    <NetworkBeforeAfter />

    <div class="totem-layout">
      <TotemEliminationPanel />
      <div class="totem-charts">
        <TotemBarChart />
        <TotemSankeyTunnel />
      </div>
    </div>

    <div v-if="store.isFourthLayerActive" class="modal-backdrop" role="dialog" aria-modal="true">
      <div class="panel evidence-modal">
        <div class="panel-header">
          <div>
            <h4 class="panel-title">黄色提袋证据摘要</h4>
            <p class="panel-subtitle">该物证在核心群体内高度集中，而在普通参会者中接近缺席。</p>
          </div>
          <button class="ghost-btn" @click="store.isFourthLayerActive = false">关闭</button>
        </div>
        <div class="modal-grid">
          <div class="evidence-preview">
            <span>黄色提袋</span>
          </div>
          <div>
            <h5>解释</h5>
            <p>
              当笔记本、胸牌、玩具等公共物品被剔除后，Person3、Person7、Person9、Person10、Person12、Person17、Person32 与 Person38 依然稳定围绕同一物证收敛，
              这使得黄色提袋成为进入最终社交隔离验证的最强候选信号。
            </p>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { useDashboardStore } from '../store/dashboard'
import TotemEliminationPanel from '../components/targeting/TotemEliminationPanel.vue'
import TotemBarChart from '../components/targeting/TotemBarChart.vue'
import TotemSankeyTunnel from '../components/targeting/TotemSankeyTunnel.vue'
import NetworkBeforeAfter from '../components/process/NetworkBeforeAfter.vue'

const store = useDashboardStore()
</script>

<style scoped>
.totem-layout {
  display: grid;
  grid-template-columns: minmax(300px, 0.75fr) minmax(0, 1.6fr);
  gap: 18px;
}

.totem-charts {
  display: grid;
  grid-template-rows: auto minmax(420px, 1fr);
  gap: 18px;
}

.modal-backdrop {
  position: fixed;
  inset: 0;
  z-index: 50;
  display: grid;
  place-items: center;
  padding: 24px;
  background: rgba(228, 237, 248, 0.72);
  backdrop-filter: blur(10px);
}

.evidence-modal {
  width: min(900px, 100%);
}

.modal-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 18px;
}

.evidence-preview {
  display: grid;
  place-items: center;
  min-height: 280px;
  border: 1px solid rgba(240, 180, 76, 0.34);
  border-radius: var(--radius);
  color: #8d6220;
  background: linear-gradient(135deg, #fff7db, #fff2ca);
  font-weight: 900;
  letter-spacing: 0.08em;
}

.modal-grid p {
  color: var(--muted);
  line-height: 1.75;
}

@media (max-width: 1040px) {
  .totem-layout,
  .modal-grid {
    grid-template-columns: 1fr;
  }
}
</style>
