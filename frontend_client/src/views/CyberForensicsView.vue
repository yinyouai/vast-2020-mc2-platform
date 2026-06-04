<template>
  <section class="view-grid-layout">
    <div class="page-intro">
      <div>
        <p class="eyebrow">任务 5 / 最终定案</p>
        <h3>当线下物证高度收敛、线上互动却异常沉默时，嫌疑群体才真正闭环。</h3>
        <p>
          最后一层不再单独讨论某个物品，而是把线下共享物证、文本叙事和线上社交隔离放到同一个解释框架中。
          如果一组人同时共享同一暗号物证，却在公开社交网络中几乎没有直接互动，这种“线下强连接、线上弱连接”的组合就极不寻常。
        </p>
        <div class="intro-pills">
          <span class="data-chip">社交隔离</span>
          <span class="data-chip">证据叙事闭环</span>
          <span class="data-chip">群体级结论</span>
        </div>
      </div>
      <span class="risk-pill risk-high">8 人核心组</span>
    </div>

    <div class="analysis-grid">
      <article class="analysis-card">
        <span>判定依据</span>
        <strong>线下共享同物证并不足够，还要看线上是否刻意分散。</strong>
        <p>若一群人既共享同一暗号，又在公开互动矩阵中近乎空白，这种模式更符合有意规避监控的协同行动特征。</p>
      </article>
      <article class="analysis-card">
        <span>反向排除</span>
        <strong>Person27 更像误报样本，而不是核心成员。</strong>
        <p>其物品特征更接近普通会场资产，且社交行为没有表现出与核心组一致的异常沉默模式，因此更适合作为被洗白的对照样本。</p>
      </article>
      <article class="analysis-card">
        <span>最终解释</span>
        <strong>黄色提袋承担了线下识别符号的角色。</strong>
        <p>结合前几层结果，它既能在物证层完成群体收敛，又能在最后与社交隔离结构相互印证，从而形成最终嫌疑团体结论。</p>
      </article>
    </div>

    <EvidencePhotoGallery />

    <DynamicSocialTree />

    <div class="forensics-layout">
      <SocialIsolationMatrix />
      <ProvenanceNarrative />
    </div>
  </section>
</template>

<script setup>
import EvidencePhotoGallery from '../components/targeting/EvidencePhotoGallery.vue'
import DynamicSocialTree from '../components/targeting/DynamicSocialTree.vue'
import SocialIsolationMatrix from '../components/targeting/SocialIsolationMatrix.vue'
import ProvenanceNarrative from '../components/targeting/ProvenanceNarrative.vue'
</script>

<style scoped>
.forensics-layout {
  display: grid;
  grid-template-columns: minmax(0, 1.2fr) minmax(360px, 0.8fr);
  gap: clamp(20px, 2.6vw, 34px);
  min-height: 650px;
}

@media (max-width: 1040px) {
  .forensics-layout {
    grid-template-columns: 1fr;
  }
}
</style>
