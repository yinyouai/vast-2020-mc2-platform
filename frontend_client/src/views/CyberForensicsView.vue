<template>
  <div class="view-grid-layout page5-root-container">
    <header class="hero-banner apple-glass-card-fixed-layer5">
      <div class="banner-txt">
        <h2 class="高光白标题">🛡️ LAYER 05: 隐形社交网络疏离度审计与团伙骨干全案终极收网舱 (Task 5)</h2>
        <p class="高级灰文本">业务取证大结论：跨多模态数据全案证据链最终收网。调阅独立纯文本发帖日记图谱可知，这 8 名特异性独立持有【黄色接头提袋图腾】的嫌疑目标，在线上社交网络中呈现出了近乎完美的“零互动、零提及”特征。他们通过线上极致疏离以逃避情报监控，却在物理现场通过物资对齐完成了地下秘密接头。线上组织隔离、线下特征共现，铁证如山，全案告破！</p>
      </div>
    </header>

    <div class="forensics-golden-split-workspace">
      <div class="workspace-left-matrix-dock">
        <SocialIsolationMatrix />
      </div>

      <div class="workspace-right-evidence-dock">
        <ProvenanceNarrative />
      </div>
    </div>
  </div>
</template>

<script setup>
import SocialIsolationMatrix from '../components/targeting/SocialIsolationMatrix.vue'
import ProvenanceNarrative from '../components/targeting/ProvenanceNarrative.vue'
</script>

<style scoped>
.page5-root-container {
  display: flex; flex-direction: column; width: 100%; height: 100%; box-sizing: border-box; overflow: hidden;
}
.apple-glass-card-fixed-layer5 {
  padding: 14px 20px; border-radius: 12px; background: rgba(255, 255, 255, 0.01);
  border: 1px solid rgba(255, 255, 255, 0.04); border-left: 4px solid #30D158;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.5); margin-bottom: 12px; flex-shrink: 0;
}
.高光白标题 { color: #FFFFFF !important; font-size: 15px; font-weight: 600; margin: 0 0 4px 0; }
.高级灰文本 { color: #AEAED2 !important; font-size: 11px; line-height: 1.5; margin: 0; }

/* 🚀 终极左右大双翼排版骨架 */
.forensics-golden-split-workspace {
  display: grid; grid-template-columns: 1.25fr 1fr; gap: 16px; flex: 1; min-height: 0; width: 100%; padding-bottom: 10px;
}
.workspace-left-matrix-dock {
  min-height: 0; height: 100%; display: flex; flex-direction: column;
}
.workspace-right-evidence-dock {
  min-height: 0; height: 100%; display: flex; flex-direction: column;
}
</style>