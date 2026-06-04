<template>
  <section class="view-grid-layout">
    <div class="page-intro">
      <div>
        <p class="eyebrow">Task 4 / Totem Filtering</p>
        <h3>先排除公共物品，再锁定真正的暗号物证</h3>
        <p>
          会场礼品覆盖率高，容易造成共现假象。通过剔除公共物品，系统会让少数群体共同持有的特殊物件变得更清晰。
        </p>
      </div>
      <button class="primary-btn" @click="$router.push('/task5_verdict')">进入最终定案</button>
    </div>

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
            <h4 class="panel-title">黄色接头包证据摘要</h4>
            <p class="panel-subtitle">该物证在核心组内高密度出现，在普通参会者中接近缺席。</p>
          </div>
          <button class="ghost-btn" @click="store.isFourthLayerActive = false">关闭</button>
        </div>
        <div class="modal-grid">
          <div class="evidence-preview">
            <span>YELLOW BAG</span>
          </div>
          <div>
            <h5>判定</h5>
            <p>剔除 Notebook、Badge、Toy 等公共物品后，Person3、Person7、Person9、Person10、Person12、Person17、Person32、Person38 在黄色接头包上形成共同特征。</p>
            <button class="primary-btn" @click="goVerdict">送入社交隔离验证</button>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useDashboardStore } from '../store/dashboard'
import TotemEliminationPanel from '../components/targeting/TotemEliminationPanel.vue'
import TotemBarChart from '../components/targeting/TotemBarChart.vue'
import TotemSankeyTunnel from '../components/targeting/TotemSankeyTunnel.vue'

const store = useDashboardStore()
const router = useRouter()

const goVerdict = () => {
  store.isFourthLayerActive = false
  router.push('/task5_verdict')
}
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
  background: rgba(0, 0, 0, 0.72);
  backdrop-filter: blur(12px);
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
  border: 1px solid rgba(244, 201, 93, 0.34);
  border-radius: var(--radius);
  color: #071013;
  background: linear-gradient(135deg, #f4c95d, #42d6c2);
  font-weight: 900;
  letter-spacing: 0.08em;
}

.modal-grid p {
  color: var(--muted);
  line-height: 1.6;
}

@media (max-width: 1040px) {
  .totem-layout,
  .modal-grid {
    grid-template-columns: 1fr;
  }
}
</style>
