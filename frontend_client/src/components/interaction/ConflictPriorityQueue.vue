<template>
  <div class="glass-card queue-container">
    <h4 class="舱室标题">🛰️ 多模态实体全景判定制工作台</h4>

    <!-- HUD 状态面板 -->
    <div class="focus-panel" :class="isHacker ? 'panel-danger' : 'panel-normal'">
      <div class="panel-top">
        <span class="status-indicator" :class="isHacker ? 'pulse-danger' : 'pulse-normal'"></span>
        <span class="panel-label">当前聚焦侦察实体</span>
      </div>
      <div class="panel-body">
        <div class="entity-row">
          <div class="entity-name font-mono">{{ store.selectedPersonId }}</div>
          <span class="badge" :class="isHacker ? 'badge-purple' : 'badge-default'">
            {{ isHacker ? '⚠️ 高危白帽骨干' : '🔒 反向排除路人' }}
          </span>
        </div>
        <p class="panel-verdict" v-if="isHacker">
          <strong>情报裁决：</strong>资产特征已被捕获！100% 独立持有接头图腾，社交关系极致隔离，白帽黑客团伙身份实锤。
        </p>
        <p class="panel-verdict" v-else>
          <strong>情报裁决：</strong>该人员已被捕获洗白。所有图片与配文特征均属于会场免费分发的无害背景噪声。
        </p>
      </div>
    </div>

    <!-- 双轨队列 -->
    <div class="dual-rail">
      <!-- 高危冲突区 -->
      <div class="rail-section">
        <div class="rail-divider danger-divider">
          <span>🚨 核心语义冲突推荐位</span>
        </div>
        <div class="rail-items">
          <div
            v-for="item in conflictItems"
            :key="item.id"
            class="rail-card card-danger"
            :class="{ active: store.selectedPersonId === item.id }"
            @click="store.selectPerson(item.id)"
          >
            <div class="card-stripe"></div>
            <div class="card-body">
              <div class="card-top">
                <h6>线索: <span class="font-mono">{{ item.id }}</span></h6>
                <span class="micro-badge err">冲突 {{ item.conflictRate }}%</span>
              </div>
              <p>{{ item.desc }}</p>
            </div>
          </div>
        </div>
      </div>

      <!-- 安全参照区 -->
      <div class="rail-section">
        <div class="rail-divider safe-divider">
          <span>🔒 外围无害普通参会者</span>
        </div>
        <div class="rail-items">
          <div
            v-for="item in safeItems"
            :key="item.id"
            class="rail-card card-safe"
            :class="{ active: store.selectedPersonId === item.id }"
            @click="store.selectPerson(item.id)"
          >
            <div class="card-stripe"></div>
            <div class="card-body">
              <div class="card-top">
                <h6>参照: <span class="font-mono">{{ item.id }}</span></h6>
                <span class="micro-badge ok">{{ item.label }}</span>
              </div>
              <p>{{ item.desc }}</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useDashboardStore } from '../../store/dashboard'
import { HACKER_LIST, NORMAL_REFERENCE_LIST } from '../../constants/forensics'

const store = useDashboardStore()

const isHacker = computed(() => HACKER_LIST.includes(store.selectedPersonId || 'Person3'))

const conflictItems = [
  {
    id: 'Person3',
    conflictRate: 78,
    desc: '机器错认成【红哨子误报】，配文强力自证持有秘密【黄色提袋】。'
  },
  {
    id: 'Person27',
    conflictRate: 64,
    desc: '图像判定为【南瓜便签】，文本意图声明为【笔记本资产】。'
  }
]

const safeItems = [
  {
    id: 'Person21',
    label: '无害参照',
    desc: '会场常规人员，不持有任何特异性图腾暗号，作为数据过滤基准比对组。'
  },
  {
    id: 'Person13',
    label: '行为洗白',
    desc: '多模态比对表明该实体属于安全背景，图像与文本关系链完全正常。'
  }
]
</script>

<style scoped>
.queue-container {
  display: flex;
  flex-direction: column;
  height: 100%;
  min-height: 0;
}

/* HUD 面板 */
.focus-panel {
  border-radius: var(--radius-md);
  padding: var(--space-md);
  margin-bottom: var(--space-md);
  transition: all 0.4s var(--ease-out-expo);
  flex-shrink: 0;
}

.panel-danger {
  background: linear-gradient(135deg, rgba(255, 90, 95, 0.06) 0%, rgba(0,0,0,0.02) 100%);
  border: 1px solid rgba(255, 90, 95, 0.15);
}

.panel-normal {
  background: linear-gradient(135deg, rgba(0,0,0,0.01) 0%, rgba(0,0,0,0.02) 100%);
  border: 1px solid rgba(0, 0, 0, 0.06);
}

.panel-top {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  margin-bottom: var(--space-sm);
}

.status-indicator {
  width: 7px;
  height: 7px;
  border-radius: 50%;
}

.pulse-danger {
  background: var(--accent-danger);
  animation: pulse-indicator 1.5s infinite;
}

.pulse-normal {
  background: var(--text-tertiary);
}

.panel-label {
  font-size: 10px;
  font-weight: var(--weight-semibold);
  color: var(--text-secondary);
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.entity-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.entity-name {
  font-size: var(--text-lg);
  font-weight: var(--weight-bold);
  color: var(--text-primary);
}

.panel-verdict {
  margin: 0;
  font-size: var(--text-xs);
  color: var(--text-secondary);
  line-height: var(--leading-normal);
}

.panel-verdict strong {
  color: var(--text-primary);
}

/* 双轨 */
.dual-rail {
  flex: 1;
  overflow-y: auto;
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}

.rail-divider {
  font-size: 10px;
  color: var(--text-tertiary);
  font-weight: var(--weight-medium);
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  margin: var(--space-sm) 0 var(--space-xs);
}

.rail-divider::after {
  content: '';
  flex: 1;
  height: 1px;
  background: rgba(0, 0, 0, 0.04);
}

.rail-items {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.rail-card {
  display: flex;
  border-radius: var(--radius-sm);
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s var(--ease-out-expo);
  border: 1px solid rgba(0, 0, 0, 0.04);
}

.card-stripe {
  width: 4px;
  flex-shrink: 0;
}

.card-danger .card-stripe { background: rgba(255, 90, 95, 0.25); }
.card-safe .card-stripe { background: rgba(49, 194, 124, 0.2); }

.rail-card:hover {
  transform: translateX(3px);
  box-shadow: var(--shadow-sm);
}

.rail-card.active {
  background: rgba(255, 255, 255, 0.8) !important;
  border-color: rgba(0, 0, 0, 0.1) !important;
  transform: translateX(4px);
}

.rail-card.active.card-danger { border-left: 4px solid var(--accent-danger); }
.rail-card.active.card-safe { border-left: 4px solid var(--accent-primary); }

.card-body {
  flex: 1;
  padding: var(--space-sm) var(--space-md);
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.card-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-top h6 {
  margin: 0;
  font-size: var(--text-xs);
  color: var(--text-primary);
  font-weight: var(--weight-medium);
}

.micro-badge {
  font-size: 9px;
  font-weight: var(--weight-bold);
  padding: 1px 6px;
  border-radius: var(--radius-full);
}

.micro-badge.err {
  background: rgba(255, 90, 95, 0.1);
  color: var(--accent-danger);
}

.micro-badge.ok {
  background: rgba(49, 194, 124, 0.1);
  color: var(--accent-primary);
}

.card-body p {
  margin: 0;
  font-size: 10px;
  color: var(--text-tertiary);
  line-height: var(--leading-tight);
}
</style>
