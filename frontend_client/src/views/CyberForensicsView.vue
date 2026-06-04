<template>
  <section class="view-grid-layout">
    <div class="page-intro">
      <div>
        <p class="eyebrow">Task 5 / Final Verdict</p>
        <h3>线下物证高度一致，线上社交刻意隔离</h3>
        <p>
          最后一层把物证过滤结果与社交网络矩阵合并判断。核心组在黄色接头包上形成强共现，却在线上几乎没有直接互动，这是最关键的反常组合。
        </p>
      </div>
      <span class="risk-pill risk-high">8 人核心组</span>
    </div>

    <div class="forensics-layout">
      <SocialIsolationMatrix />
      <ProvenanceNarrative />
    </div>
  </section>
</template>

<script setup>
import SocialIsolationMatrix from '../components/targeting/SocialIsolationMatrix.vue'
import ProvenanceNarrative from '../components/targeting/ProvenanceNarrative.vue'
</script>

<style scoped>
.forensics-layout {
  display: grid;
  grid-template-columns: minmax(0, 1.35fr) minmax(340px, 0.85fr);
  gap: 18px;
  min-height: 650px;
}

@media (max-width: 1040px) {
  .forensics-layout {
    grid-template-columns: 1fr;
  }
}
</style>
