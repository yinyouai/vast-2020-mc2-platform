<template>
  <div class="view-grid-layout">
    <ControlSlider />

    <div class="exploration-workspace-grid">
      <div class="workspace-left">
        <ConflictPriorityQueue />
      </div>
      <div class="workspace-right">
        <CorrectionCanvas />
      </div>
    </div>
  </div>
</template>

<script setup>
import ControlSlider from '../components/interaction/ControlSlider.vue'
import ConflictPriorityQueue from '../components/interaction/ConflictPriorityQueue.vue'
import CorrectionCanvas from '../components/interaction/CorrectionCanvas.vue'
</script>

<style scoped>
.exploration-workspace-grid { display: grid; grid-template-columns: 1fr 2.1fr; gap: 24px; flex: 1; min-height: 0; }
.workspace-left, .workspace-right { min-height: 0; height: 100%; }
</style>