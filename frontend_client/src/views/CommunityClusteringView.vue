<template>
  <div class="view-grid-layout">
    <div class="hero-banner apple-glass-card" style="border-left-color: var(--accent-totem);">
      <div class="banner-txt">
        <h2>📊 LAYER 03: 候选嫌疑社群物资共现光谱双向聚类舱 (Task 3)</h2>
        <p>全景总览：响应层级二调校过滤后的高置信度多模态特征，后端分布式数学引擎实时调用 Ward 层次聚类树对 40 名嫌疑人及物资轴执行平移洗牌，迫使无序的社交网络在屏幕上收敛为规整的聚类行为色块。</p>
      </div>
      <button class="apple-route-btn" @click="$router.push('/task4_totem')">
        进入下一层级：普及物资削波与秘密暗号漏斗 <span>→</span>
      </button>
    </div>

    <div class="clustering-workspace">
      <div class="workspace-left-heatmap">
        <ClusterHeatmap />
      </div>

      <div class="workspace-right-report apple-glass-card">
        <h4 class="舱室标题">📡 首席情报分析官·社群模式侦察报告</h4>

        <div class="report-scroll-area">
          <div class="verdict-card info-blue">
            <h5>🧬 嫌疑社群轴双向拓扑收敛态势：</h5>
            <p>经过数学矩阵重排，原先离散不相关的 40 位会议发言人已在空间上坍缩聚拢为<b>三大核心利益阵营</b>。这种特异性的行为同质化趋势，强力揭示了会场内部存在有组织、有预谋的秘密线下面基网络。</p>
          </div>

          <div class="verdict-card info-red">
            <h5>⚠️ 集团 A 与集团 B (外围正常参会群体)：</h5>
            <p>聚类块表明，占总数 80% 的外围参会人员其高亮色块死死锚定在【南瓜便签】、【眼球玩具】与【高危哨子】上。结合层级一的审计结论，这属于会场普及分发物资，且伴随着 YOLO 算法的大量低分机器假阳性虚警。此两类集团的嫌疑已被反向排除。</p>
          </div>

          <div class="verdict-card info-purple">
            <h5>🎯 集团 C (高度锁定的核心黑客组织帮派)：</h5>
            <p>极度高能警报！矩阵顶层洗牌后分离出了一个由 <b>8 名成员</b>（以 `Person3`, `Person27` 为首）组成的孤立方阵。该方阵的行为光谱完全脱离了会场主流，他们不持有任何普及免费礼品，却呈现出绝对死锁的共现特征！</p>
          </div>

          <div class="interactive-tip">
            💡 <b>交互提示</b>：在左侧热力图网格卡片中点击任意高危色块行，系统大动脉将自动下钻追踪，级联重置层级二的多模态纠错 Canvas 底片！
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import ClusterHeatmap from '../components/targeting/ClusterHeatmap.vue'
</script>

<style scoped>
.hero-banner { display: flex; justify-content: space-between; align-items: center; border-left: 4px solid var(--accent-totem); }
.banner-txt h2 { margin: 0 0 4px 0; font-size: 16px; color: #FFF; font-weight: 500; }
.banner-txt p { margin: 0; font-size: 12px; color: #8E8E93; line-height: 1.5; max-width: 82%; }
.apple-route-btn { background: rgba(255,255,255,0.06); border: 1px solid rgba(255,255,255,0.08); color: #FFF; padding: 10px 18px; border-radius: 20px; cursor: pointer; font-size: 12px; font-weight: 500; transition: all 0.3s; display: flex; align-items: center; gap: 4px; }
.apple-route-btn:hover { background: #FFF; color: #000; transform: scale(1.02); }
.apple-route-btn span { transition: transform 0.3s; }
.apple-route-btn:hover span { transform: translateX(4px); }

.clustering-workspace { display: grid; grid-template-columns: 1.4fr 1fr; gap: 24px; flex: 1; min-height: 0; margin-top: 5px; }
.workspace-left-heatmap { min-height: 0; height: 100%; display: flex; flex-direction: column; }
.workspace-right-report { display: flex; flex-direction: column; height: 100%; min-height: 0; }

.report-scroll-area { flex: 1; overflow-y: auto; display: flex; flex-direction: column; gap: 14px; padding-right: 4px; margin-top: 5px; }
.verdict-card { padding: 12px 14px; border-radius: 10px; border: 1px solid rgba(255,255,255,0.02); }
.verdict-card h5 { margin: 0 0 6px 0; font-size: 13px; font-weight: 500; }
.verdict-card p { margin: 0; font-size: 11.5px; line-height: 1.5; color: #C7C7CC; }

.info-blue { background: rgba(0, 122, 255, 0.04); h5 { color: #007AFF; } }
.info-red { background: rgba(255, 59, 48, 0.04); h5 { color: var(--accent-machine); } }
.info-purple { background: rgba(191, 90, 242, 0.05); border-color: rgba(191, 90, 242, 0.1); h5 { color: var(--accent-totem); } }
.interactive-tip { font-size: 11px; color: var(--accent-truth); background: rgba(48,209,88,0.03); padding: 8px 12px; border-radius: 6px; border: 1px solid rgba(48,209,88,0.05); margin-top: auto; }
</style>