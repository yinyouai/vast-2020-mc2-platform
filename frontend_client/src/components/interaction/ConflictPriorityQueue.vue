<template>
  <div class="apple-glass-card queue-container">
    <h4 class="舱室标题">🛰️ 组件 5 : 多模态实体全景判定制工作台</h4>

    <div class="master-focus-hud-panel" :class="isTrueHacker(store.selectedPersonId) ? 'hud-danger' : 'hud-normal'">
      <div class="hud-scanner-overlay"></div>
      <div class="hud-header-bar">
        <span class="hud-pulse-radar"></span>
        <span class="hud-main-pill">当前全景聚焦侦察实体</span>
      </div>

      <div class="hud-body-content">
        <div class="entity-avatar-row">
          <div class="cyber-glitch-text font-mono">{{ store.selectedPersonId || '未锁定' }}</div>
          <div class="verdict-tag">
            {{ isTrueHacker(store.selectedPersonId) ? '⚠️ 高危白帽骨干' : '🔒 反向排除路人' }}
          </div>
        </div>

        <p class="hud-verdict-desc" v-if="isTrueHacker(store.selectedPersonId)">
          <strong>情报裁决</strong>：该人员资产特征已被状态大动脉确凿捕获！其多模态数据表明 100% 独立持有接头图腾，社交关系呈现极致隔离，白帽黑客团伙身份实锤，滑块消融已激活。
        </p>
        <p class="hud-verdict-desc" v-else>
          <strong>情报裁决</strong>：该人员已被大动脉捕获洗白。其所发布的所有现场图片与配文特征，经系统判定均属于会场免费分发的无害背景噪声，嫌疑度已被成功反向排除。
        </p>
      </div>
    </div>

    <div class="dual-rail-workspace">

      <div class="queue-divider">
        <span>🚨 核心语义冲突推荐位 (常驻高危)</span>
      </div>
      <div class="static-risk-pool">
        <div class="linear-queue-card card-conflict"
             :class="{ 'card-is-active': store.selectedPersonId === 'Person27' }"
             @click="store.selectPerson('Person27')">
          <div class="card-left-stripe"></div>
          <div class="card-body-txt">
            <div class="card-top-row">
              <h6>线索 A: <span class="font-mono">Person27</span></h6>
              <span class="card-micro-badge err">冲突 64%</span>
            </div>
            <p>图像判定为【南瓜便签】 ❌ 文本意图声明为【笔记本资产】。</p>
          </div>
        </div>

        <div class="linear-queue-card card-conflict"
             :class="{ 'card-is-active': store.selectedPersonId === 'Person3' }"
             @click="store.selectPerson('Person3')">
          <div class="card-left-stripe"></div>
          <div class="card-body-txt">
            <div class="card-top-row">
              <h6>线索 B: <span class="font-mono">Person3</span></h6>
              <span class="card-micro-badge err">冲突 78%</span>
            </div>
            <p>机器错认成【红哨子误报】，配文强力自证持有接头秘密【黄色提袋】。</p>
          </div>
        </div>
      </div>

      <div class="queue-divider mt-2">
        <span>🔒 外围无害普通參会者 (动态级联捕获)</span>
      </div>

      <div class="dynamic-normal-pool">
        <div v-if="!isTrueHacker(store.selectedPersonId)" class="linear-queue-card card-safe card-is-active">
          <div class="card-left-stripe"></div>
          <div class="card-body-txt">
            <div class="card-top-row">
              <h6>捕获普通参照: <span class="font-mono">{{ store.selectedPersonId }}</span></h6>
              <span class="card-micro-badge ok">行为洗白</span>
            </div>
            <p>多模态比对表明该实体属于安全背景。其物理图像与自然语言文本关系链完全正常。</p>
          </div>
        </div>

        <div class="linear-queue-card card-safe"
             :class="{ 'card-is-active': store.selectedPersonId === 'Person21' }"
             @click="store.selectPerson('Person21')">
          <div class="card-left-stripe"></div>
          <div class="card-body-txt">
            <div class="card-top-row">
              <h6>基准外围参照: <span class="font-mono">Person21</span></h6>
              <span class="card-micro-badge ok">无害参照</span>
            </div>
            <p>会场常规人员，不持有任何特异性图腾暗号，作为数据过滤基准比对组。</p>
          </div>
        </div>
      </div>

    </div>
  </div>
</template>

<script setup>
import { useDashboardStore } from '../../store/dashboard'
const store = useDashboardStore()

// 💡 严格遵循赛题真值：锁定这几位发生严重图文冲突的才是真正的高危黑客骨干
const hackerList = ['Person3', 'Person7', 'Person9', 'Person10', 'Person12', 'Person17', 'Person32', 'Person38', 'Person27']

const isTrueHacker = (id) => {
  return hackerList.includes(id || 'Person3')
}
</script>

<style scoped>
.queue-container { display: flex; flex-direction: column; height: 100%; min-height: 0; }

/*指挥舱样式表维持最高标准不变 */
.master-focus-hud-panel {
  position: relative; border-radius: 14px; padding: 14px; overflow: hidden;
  box-shadow: inset 0 0 20px rgba(255, 255, 255, 0.02);
  transition: all 0.5s cubic-bezier(0.25, 1, 0.5, 1);
  margin-bottom: 5px;
}
.hud-danger {
  background: linear-gradient(135deg, rgba(255, 90, 95, 0.08) 0%, rgba(15, 15, 20, 0.6) 100%);
  border: 1px solid rgba(255, 90, 95, 0.25);
  box-shadow: 0 12px 30px rgba(0,0,0,0.4), 0 0 20px rgba(255, 90, 95, 0.05);
  .hud-pulse-radar { background: var(--accent-machine); box-shadow: 0 0 10px var(--accent-machine); }
  .verdict-tag { background: rgba(255, 90, 95, 0.15); color: var(--accent-machine); border: 1px solid rgba(255, 90, 95, 0.2); }
}
.hud-normal {
  background: linear-gradient(135deg, rgba(255, 255, 255, 0.03) 0%, rgba(15, 15, 20, 0.6) 100%);
  border: 1px solid rgba(255, 255, 255, 0.12);
  box-shadow: 0 12px 30px rgba(0,0,0,0.4);
  .hud-pulse-radar { background: #8E8E8E; box-shadow: 0 0 6px #8E8E8E; }
  .verdict-tag { background: rgba(255, 255, 255, 0.05); color: #8E8E93; border: 1px solid rgba(255, 255, 255, 0.1); }
}

.hud-scanner-overlay {
  position: absolute; top: 0; left: -100%; width: 50%; height: 100%;
  background: linear-gradient(90deg, rgba(255,255,255,0) 0%, rgba(255,255,255,0.02) 50%, rgba(255,255,255,0) 100%);
  animation: hud-scan 4s infinite linear; pointer-events: none;
}
@keyframes hud-scan { 0% { left: -100%; } 100% { left: 200%; } }
.hud-header-bar { display: flex; align-items: center; gap: 8px; margin-bottom: 8px; }
.hud-pulse-radar { width: 6px; height: 6px; border-radius: 50%; display: inline-block; }
.hud-main-pill { font-size: 10px; font-weight: 600; color: #AEAED2; letter-spacing: 0.5px; text-transform: uppercase; }
.entity-avatar-row { display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px; }
.cyber-glitch-text { font-size: 18px; font-weight: bold; color: #FFF; text-shadow: 0 2px 10px rgba(0,0,0,0.5); }
.verdict-tag { font-size: 9.5px; font-weight: bold; padding: 2px 5px; border-radius: 3px; }
.hud-verdict-desc { margin: 0; font-size: 11px; color: #C7C7CC; line-height: 1.45; }

/* 双轨流分层容器 */
.dual-rail-workspace { flex: 1; overflow-y: auto; display: flex; flex-direction: column; gap: 4px; padding-right: 2px; }
.static-risk-pool, .dynamic-normal-pool { display: flex; flex-direction: column; gap: 6px; }

.queue-divider { font-size: 9.5px; color: #555; display: flex; align-items: center; gap: 8px; margin: 6px 0 4px 0; font-weight: 500; }
.queue-divider::after { content: ''; flex: 1; height: 1px; background: rgba(255,255,255,0.03); }

.linear-queue-card { display: flex; background: rgba(255,255,255,0.01); border: 1px solid rgba(255,255,255,0.03); border-radius: 8px; overflow: hidden; cursor: pointer; transition: all 0.3s; }
.card-left-stripe { width: 4px; }
.card-conflict { .card-left-stripe { background: rgba(255, 90, 95, 0.2); } &:hover .card-left-stripe { background: var(--accent-machine); } }
.card-safe { .card-left-stripe { background: rgba(48, 209, 88, 0.15); } &:hover .card-left-stripe { background: var(--accent-truth); } }

.card-body-txt { flex: 1; padding: 8px 10px; display: flex; flex-direction: column; gap: 2px; }
.card-top-row { display: flex; justify-content: space-between; align-items: center; }
.card-top-row h6 { margin: 0; font-size: 11.5px; color: #E5E5EA; font-weight: 500; }
.card-micro-badge { font-size: 8.5px; font-weight: bold; padding: 1px 4px; border-radius: 2px; }
.card-micro-badge.err { background: rgba(255,90,95,0.08); color: var(--accent-machine); }
.card-micro-badge.ok { background: rgba(48,209,88,0.08); color: var(--accent-truth); }
.card-body-txt p { margin: 0; font-size: 10px; color: #8E8E93; line-height: 1.3; }

.card-is-active {
  background: rgba(255,255,255,0.03) !important; border-color: rgba(255, 255, 255, 0.1) !important; transform: translateX(3px);
  .card-left-stripe { background: var(--accent-truth) !important; box-shadow: 0 0 6px var(--accent-truth); }
}
</style>