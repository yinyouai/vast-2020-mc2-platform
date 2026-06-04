<template>
  <section class="view-grid-layout">
    <div class="page-intro">
      <div>
        <p class="eyebrow">任务 2 / 人工复核</p>
        <h3>把图像预测、文本叙事和人工判断放到同一工作面，修正模型最容易犯错的地方。</h3>
        <p>
          这一层参考优秀作品中的复核工作台思路，不只展示当前图片，而是强调“候选标签排序、图文冲突提示、人工保存结果”三者之间的闭环。
          这样可以把单点纠错转成可复用的证据修正流程。
        </p>
        <div class="intro-pills">
          <span class="data-chip">冲突排序</span>
          <span class="data-chip">人工标注</span>
          <span class="data-chip">真值回灌</span>
        </div>
      </div>
    </div>

    <div class="analysis-grid">
      <article class="analysis-card">
        <span>复核逻辑</span>
        <strong>先看冲突最强的样本，而不是平均浏览全部图像。</strong>
        <p>优先队列能让分析师把时间投在“文本明确但图像误判”的样本上，这类记录最可能改变后续群体判断。</p>
      </article>
      <article class="analysis-card">
        <span>不确定性</span>
        <strong>不确定性既来自模型，也来自人。</strong>
        <p>模型的不确定性体现在低置信框和类别混淆；人的不确定性则体现在主观判断。因此复核界面应同时保留机器预测和人工结论。</p>
      </article>
      <article class="analysis-card">
        <span>效率提升</span>
        <strong>相似样本应支持批量纠错。</strong>
        <p>参考外部案例，若一组图像的检测框重叠模式接近，纠正其中一张后，应能给其余近邻样本提供联动提示，从而提升校正效率。</p>
      </article>
    </div>

    <ManualReviewComparison />

    <ControlSlider />

    <div class="exploration-workspace-grid">
      <ConflictPriorityQueue />
      <CorrectionCanvas />
    </div>
  </section>
</template>

<script setup>
import ControlSlider from '../components/interaction/ControlSlider.vue'
import ConflictPriorityQueue from '../components/interaction/ConflictPriorityQueue.vue'
import CorrectionCanvas from '../components/interaction/CorrectionCanvas.vue'
import ManualReviewComparison from '../components/process/ManualReviewComparison.vue'
</script>

<style scoped>
.exploration-workspace-grid {
  display: grid;
  grid-template-columns: minmax(320px, 0.9fr) minmax(0, 1.7fr);
  gap: 18px;
  min-height: 560px;
}

@media (max-width: 1040px) {
  .exploration-workspace-grid {
    grid-template-columns: 1fr;
  }
}
</style>
