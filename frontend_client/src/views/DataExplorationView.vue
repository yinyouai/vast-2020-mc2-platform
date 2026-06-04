<template>
  <section class="view-grid-layout">
    <div class="page-intro">
      <div>
        <p class="eyebrow">Task 2 / Human-in-the-loop</p>
        <h3>把机器判断和文本语义放到同一张桌面上复核</h3>
        <p>
          左侧列出最高优先级的图文冲突样本，右侧展示当前目标的图像证据、机器框选与人工语义判定。这里的选择会贯穿后续聚类、过滤和定案页面。
        </p>
      </div>
      <button class="ghost-btn" @click="$router.push('/task3_clustering')">查看群体聚类</button>
    </div>

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
