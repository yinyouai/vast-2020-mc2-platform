<template>
  <div class="view-grid-layout">
    <!-- 👑 修复核心：重度加强高维对比度的 Apple 磨砂情报横幅 -->
    <header class="hero-banner apple-glass-card-fixed">
      <div class="banner-txt">
        <h2 class="高光白标题">🔮 LAYER 04: 全员泛滥物资特征削波与秘密图腾反向排除舱 (Task 4)</h2>
        <p class="高级灰文本">全景总览：会场免费分发物资形成了极强的背景噪声干扰。请利用下方的反向排除漏斗，像过滤无线电波噪声一样一键切除掉高持有率的大众普及资产，强行逼迫真正的核心黑客组织线下接头暗号图腾在流向图中显现！</p>
      </div>
      <!-- 🎛️ 控件美化：重塑为带有赛博霓虹微光、悬浮物理平移的高级进入按钮 -->
      <button class="cyber-neon-btn" @click="$router.push('/task5_verdict')">
        <span>进入层级五: 社交隔离定案</span>
        <svg class="arrow-icon" viewBox="0 0 24 24"><path d="M5 12h14M12 5l7 7-7 7" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </button>
    </header>

    <div class="totem-grid-layout">
      <!-- 组件 10 内部的英文乱码将在下一步被彻底洗净 -->
      <TotemEliminationPanel />
      <div class="charts-split">
        <TotemBarChart />
        <TotemSankeyTunnel />
      </div>
    </div>

    <!-- 🌟 第四层级全屏物证深度钻取舱保持高级性能 -->
    <transition name="fade-zoom">
      <div v-if="store.isFourthLayerActive" class="fourth-layer-overlay-fullscreen">
        <div class="fourth-layer-window apple-glass-card">
          <div class="window-header">
            <h3>🛸 LAYER 04 - SUB: 秘密图腾【黄色提袋】像素级物证链级联钻取分析舱</h3>
            <button class="close-btn" @click="store.isFourthLayerActive = false">✖ 退出第四层级</button>
          </div>
          <div class="window-body-grid">
            <div class="evidence-photo-box">
              <div class="badge-title">📷 现场查获核心物证照片流 (去噪真值)</div>
              <img src="http://localhost:5000/static/MC2-Image-Data/Person3/Person3_1.jpg" class="pure-evidence-img" />
            </div>
            <div class="evidence-log-panel">
              <h4>📋 破译终极结案陈词报告 (Task 4 Completed)</h4>
              <div class="bullet-item">🟩 <b>特异性实锤</b>：全场 40 人中，除了以 `Person3`, `Person27` 为首的 8 人组织外，其余 32 人对此资产的持有率表现为<b>绝对的零共现</b>！</div>
              <div class="bullet-item">🟩 <b>图文矛盾闭闭环</b>：该资产在层级二中曾被 YOLO 算法严重错认。人类真值校准后，它以 100% 的数学纯度凝结成了这个特定白帽黑客团伙的秘密线下会合“图腾（Totem）”。</div>
              <button class="action-forward-btn" @click="goToLayer5">证据锁死：一键前往层级五核对社交隔离网</button>
            </div>
          </div>
        </div>
      </div>
    </transition>
  </div>
</template>

<script setup>
import { useDashboardStore } from '../store/dashboard'
import { useRouter } from 'vue-router'
import TotemEliminationPanel from '../components/targeting/TotemEliminationPanel.vue'
import TotemBarChart from '../components/targeting/TotemBarChart.vue'
import TotemSankeyTunnel from '../components/targeting/TotemSankeyTunnel.vue'

const store = useDashboardStore()
const router = useRouter()

const goToLayer5 = () => {
  store.isFourthLayerActive = false
  router.push('/task5_verdict')
}
</script>

<style scoped>
/* 🎨 终极强光白与质感灰样式，彻底告别“一片黑” */
.apple-glass-card-fixed {
  display: flex; justify-content: space-between; align-items: center;
  padding: 18px 24px; border-radius: 12px; background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06); border-left: 4px solid var(--accent-totem);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4); margin-bottom: 12px;
}
.高光白标题 { color: #FFFFFF !important; font-size: 16px; font-weight: 600; margin: 0 0 6px 0; letter-spacing: -0.1px; text-shadow: 0 2px 4px rgba(0,0,0,0.5); }
.高级灰文本 { color: #AEAED2 !important; font-size: 11.5px; line-height: 1.5; margin: 0; max-width: 80%; }

/* 🎛️ 赛博霓虹智能按钮样式重塑 */
.cyber-neon-btn {
  background: rgba(191, 90, 242, 0.08); border: 1px solid rgba(191, 90, 242, 0.3);
  color: #BF5AF2; padding: 10px 18px; border-radius: 20px; font-size: 12px;
  font-weight: 600; cursor: pointer; display: flex; align-items: center; gap: 8px;
  transition: all 0.4s cubic-bezier(0.25, 1, 0.5, 1); box-shadow: 0 4px 12px rgba(191, 90, 242, 0.1);
}
.cyber-neon-btn:hover {
  background: #BF5AF2; color: #000000; transform: scale(1.03) translateY(-1px);
  box-shadow: 0 0 20px rgba(191, 90, 242, 0.4);
}
.arrow-icon { width: 14px; height: 14px; fill: none; transition: transform 0.3s; }
.cyber-neon-btn:hover .arrow-icon { transform: translateX(4px); }

.totem-grid-layout { display: flex; flex-direction: column; gap: 14px; flex: 1; min-height: 0; }
.charts-split { display: grid; grid-template-columns: 1fr 1.3fr; gap: 14px; flex: 1; min-height: 0; }

/* 第四层级深度全屏窗口 */
.fourth-layer-overlay-fullscreen { position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background: rgba(5,5,8,0.94); backdrop-filter: blur(20px); z-index: 999; display: flex; align-items: center; justify-content: center; padding: 40px; }
.fourth-layer-window { width: 100%; height: 100%; max-width: 1100px; max-height: 620px; border: 1px solid rgba(191,90,242,0.3) !important; display: flex; flex-direction: column; padding: 24px; background: #0A0A0C; }
.window-header { display: flex; justify-content: space-between; align-items: center; border-bottom: 1px solid rgba(255,255,255,0.05); padding-bottom: 12px; margin-bottom: 16px; }
.window-header h3 { margin: 0; font-size: 15px; color: #FFF; font-weight: 500; }
.close-btn { background: rgba(255,255,255,0.06); border: none; color: #8E8E93; padding: 6px 14px; border-radius: 20px; cursor: pointer; font-size: 12px; transition: all 0.3s; }
.close-btn:hover { background: #FF5A5F; color: #FFF; }
.window-body-grid { display: grid; grid-template-columns: 1.2fr 1fr; gap: 24px; flex: 1; min-height: 0; }
.evidence-photo-box { background: #000; border-radius: 12px; border: 1px solid rgba(255,255,255,0.04); display: flex; flex-direction: column; overflow: hidden; }
.badge-title { font-size: 11px; color: #8E8E93; padding: 10px; background: rgba(255,255,255,0.02); }
.pure-evidence-img { flex: 1; width: 100%; object-fit: contain; background: #0F0F12; }
.evidence-log-panel { display: flex; flex-direction: column; gap: 14px; background: rgba(255,255,255,0.01); padding: 16px; border-radius: 12px; }
.evidence-log-panel h4 { margin: 0 0 6px 0; font-size: 14px; color: var(--accent-totem); }
.bullet-item { font-size: 12px; line-height: 1.5; color: #E5E5EA; padding: 8px 10px; background: rgba(255,255,255,0.02); border-radius: 6px; }
.action-forward-btn { margin-top: auto; background: linear-gradient(135deg, var(--accent-totem), #651fff); border: none; color: #FFF; padding: 12px; border-radius: 24px; cursor: pointer; font-size: 12px; font-weight: bold; transition: all 0.3s; }
.action-forward-btn:hover { transform: translateY(-1px); }
.fade-zoom-enter-from, .fade-zoom-leave-to { opacity: 0; transform: scale(0.96); filter: blur(5px); }
.fade-zoom-enter-active, .fade-zoom-leave-active { transition: all 0.4s cubic-bezier(0.25, 1, 0.5, 1); }
</style>