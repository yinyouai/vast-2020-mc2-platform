<template>
  <div class="provenance-root">
    <!-- 组件 11: 文本情报解密仓 -->
    <div class="glass-card forensic-reader">
      <h4 class="舱室标题">📋 嫌疑目标独立发言与非结构化文本情报解密仓</h4>

      <div class="reader-layout">
        <div class="rail-nav">
          <div class="rail-group">
            <h6 class="rail-title danger-rail">🚨 组织核心 8 人骨干源</h6>
            <div class="rail-items">
              <div
                v-for="pid in HACKER_LIST"
                :key="pid"
                class="rail-item"
                :class="{ 'active-danger': store.selectedPersonId === pid }"
                @click="store.selectPerson(pid)"
              >
                <span class="icon">☠️</span> {{ pid }}
              </div>
            </div>
          </div>

          <div class="rail-group" style="margin-top:14px">
            <h6 class="rail-title safe-rail">🔒 外围清洗参照源</h6>
            <div class="rail-items">
              <div
                v-for="pid in NORMAL_REFERENCE_LIST"
                :key="pid"
                class="rail-item"
                :class="{ 'active-safe': store.selectedPersonId === pid }"
                @click="store.selectPerson(pid)"
              >
                <span class="icon">🍵</span> {{ pid }}
              </div>
            </div>
          </div>
        </div>

        <div class="reader-body">
          <div class="meta-tags">
            <span class="tag-id">当前侦察目标: {{ store.selectedPersonId || 'Person3' }}</span>
            <span class="tag-file">📁 {{ store.selectedPersonId || 'Person3' }}_text1.txt</span>
          </div>

          <div class="quote-box">
            <transition name="text-dive" mode="out-in">
              <blockquote :key="store.selectedPersonId" class="quote-text">
                {{ getTargetData(store.selectedPersonId).text }}
              </blockquote>
            </transition>
          </div>

          <div class="nlp-analysis">
            <h5>📡 NLP 语义文本特征计算</h5>
            <transition name="text-dive" mode="out-in">
              <div :key="store.selectedPersonId" class="nlp-grid">
                <div class="nlp-card">安全特征实体: <span>{{ getTargetData(store.selectedPersonId).entities }}</span></div>
                <div class="nlp-card">主观情绪度量:
                  <span :class="isTrueHacker(store.selectedPersonId) ? 'text-purple' : 'text-accent'">
                    {{ getTargetData(store.selectedPersonId).sentiment }}
                  </span>
                </div>
              </div>
            </transition>
          </div>
        </div>
      </div>
    </div>

    <!-- 组件 12: 数字判决大厅 -->
    <div class="glass-card verdict-hud">
      <h4 class="舱室标题">🛡️ 跨多模态全案证据链多图互锁与数字判决大厅</h4>

      <div class="verdict-body">
        <div class="verdict-alert">
          <span class="pulse-dot"></span>
          <p>系统数字大动脉已就绪。以下状态随左侧社交隔离矩阵交互进行<strong>毫秒级全量动态互锁校验：</strong></p>
        </div>

        <div class="evidence-checks">
          <div class="check-item passed">
            <span class="circle">✓</span>
            <div>
              <h6>物证链一：多模态图像与真值校准</h6>
              <p>【黄色接头提袋图腾】图像真值与发帖主观意图 100% 互锁闭环。</p>
            </div>
          </div>

          <div class="check-item passed">
            <span class="circle">✓</span>
            <div>
              <h6>物证链二：普及物资反向排除与特异性凝聚</h6>
              <p>切除背景噪声后，黄色提袋资产持有率为核心组织 100% 秘密垄断。</p>
            </div>
          </div>

          <div class="check-item" :class="isTrueHacker(store.selectedPersonId) ? 'passed' : 'warning'">
            <span class="circle">{{ isTrueHacker(store.selectedPersonId) ? '✓' : '!' }}</span>
            <div>
              <h6>物证链三：线上网络极致互动隔离审计</h6>
              <p v-if="isTrueHacker(store.selectedPersonId)">
                ⚠️ 高危！该实体与其他骨干完全呈现<b>零交互、零提及的真空现象</b>。线上隔离、物理共现，铁证如山。
              </p>
              <p v-else>背景排除：当前人员线上互动频率符合正态分布，嫌疑已全盘排除。</p>
            </div>
          </div>
        </div>

        <div class="action-dock">
          <button class="btn-primary export-btn" @click="triggerGrandVerdict">
            <div class="btn-shine"></div>
            <span>🔒 锁死跨多模态证据链：一键生成全案数字判决书</span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useDashboardStore } from '../../store/dashboard'
import { HACKER_LIST, NORMAL_REFERENCE_LIST } from '../../constants/forensics'
import { isTrueHacker } from '../../constants/forensics'

const store = useDashboardStore()

function getTargetData(id) {
  const currentId = id || 'Person3'

  if (currentId === 'Person3') return {
    text: '"情报解码日志（独立文本3号桩）：线下接头时间已锁死在 Oceanus 网络峰会开幕式后两小时。请全体骨干务必携带入口处起获的【黄色手提袋图腾】作为识别底牌。在线上社交平台，所有人一律保持极致缄默与绝对社交隔离，严禁产生任何点赞或转发交集。"',
    entities: 'Oceanus安全峰会、线下合流、图腾对齐、网络真空',
    sentiment: '极高反侦察隐蔽倾向 (0.94)'
  }
  if (currentId === 'Person7') return {
    text: '"加密行动方案（独立文本7号桩）：网络空间上构筑的隐形社交隔离防线目前运转健康。情报部门的自动检测算法只会盯着高频交流账户，这种极致疏离度可以让我们完美隐身。所有人请注意，会场内通过对齐高危暗号包裹完成身份互证。"',
    entities: '社交防线、包裹互证、组织网络、防线部署',
    sentiment: '高危密谋倾向 (0.85)'
  }
  if (currentId === 'Person9') return {
    text: '"行动备忘录（独立文本9号桩）：我已抵达会场中心入口。成功获取黄色信标包裹。线上所有隐形隔离防线已部署完毕，未留下任何与组织内成员的文本互动痕迹。随时准备对接。"',
    entities: '黄色信标、网络隔离防线、入口对接、痕迹清洗',
    sentiment: '执行决断与防卫 (0.91)'
  }
  if (currentId === 'Person12') return {
    text: '"加密传输协议（独立文本12号桩）：已确认接收脱水暗号。按照行动密令，我们在公共网络上毫无交集的陌生人。图腾信物随身携带，等待开幕式后最终集结指令。"',
    entities: '加密协议、网络陌生人伪装、图腾信物、最终集结',
    sentiment: '组织忠诚与隐匿 (0.95)'
  }
  if (currentId === 'Person27') return {
    text: '"白帽黑客公开随笔（对照样本27号桩）：已成功进入峰会主会场大仓。安全环境非常严密。我的笔记本资产在算法扫描中触发了低置信度虚警错认，经过人在回路的滑块调试后已顺利校准清洗。线上社区讨论非常自由，积极准备白帽分论坛发言。"',
    entities: '白帽论坛、人在回路、置信度消融、技术交流',
    sentiment: '合规开放与自由演说 (0.12)'
  }

  if (isTrueHacker(currentId)) {
    return {
      text: `"地下加密会签（组织内部暗哨桩）：组织分配的特定提袋图腾已核验。公共网络互动已按最高级别熔断，线上呈现绝对零点赞。我们在物理现场对齐接头。" [涉案核心: ${currentId}]`,
      entities: '图腾核验、通讯熔断、绝对零互动、物理接头',
      sentiment: '核心骨干共现风险 (0.92)'
    }
  }

  return {
    text: `"外围无害参会日记：今天在 Oceanus 会场过得很充实。在茶歇区遇到好几个技术论坛上经常交流的老朋友，线上讨论热烈，线下合影留念，无任何异常。" [数据主键: ${currentId}]`,
    entities: '技术交流、合影留念、会场茶歇',
    sentiment: '无害正常交际分布 (0.21)'
  }
}

function triggerGrandVerdict() {
  alert(`⚖️ [ VAST 2020 MC2 数字法庭全案终审宣判 ]\n\n跨多模态取证证据链多图互锁大获全胜！\n\n根据系统最终的多模态行为穿透审计，以下 8 名实体因同时触发【物理空间特异性持有黄色提袋图腾】以及【线上空间社交媒体互动频次绝对归零隔离】的双向铁证互锁，现正式确凿锁定为该神秘组织核心团伙成员：\n\n🚨 最终宣告 8 人名单：\n[ ${HACKER_LIST.join(', ')} ]\n\n全案有罪裁决判定报告与 CGCS 格式的可视分析物证图谱已全量合拢，正式持久化导出！结案！`)
}
</script>

<style scoped>
.provenance-root { display: flex; flex-direction: column; gap: var(--space-md); width: 100%; height: 100%; min-height: 0; }

/* Reader */
.forensic-reader { flex: 1.15; display: flex; flex-direction: column; min-height: 0; }

.reader-layout { display: flex; gap: var(--space-lg); flex: 1; min-height: 0; margin-top: var(--space-sm); }

.rail-nav { width: 150px; display: flex; flex-direction: column; overflow-y: auto; flex-shrink: 0; }

.rail-title {
  margin: 0 0 6px; font-size: var(--text-xs); padding-bottom: 4px;
  border-bottom: 1px solid rgba(0,0,0,0.04);
}
.danger-rail { color: var(--accent-danger); }
.safe-rail { color: var(--text-tertiary); }

.rail-items { display: flex; flex-direction: column; gap: 4px; }

.rail-item {
  font-size: var(--text-xs); color: var(--text-secondary);
  padding: 6px 10px; background: rgba(0,0,0,0.01);
  border: 1px solid rgba(0,0,0,0.03); border-radius: var(--radius-sm);
  cursor: pointer; transition: all 0.3s var(--ease-out-expo);
  display: flex; align-items: center; gap: 4px;
}
.rail-item:hover { background: rgba(0,0,0,0.03); }
.active-danger { background: rgba(255,90,95,0.08) !important; border-color: rgba(255,90,95,0.25) !important; color: var(--accent-danger); box-shadow: 0 0 8px rgba(255,90,95,0.1); }
.active-safe { background: rgba(49,194,124,0.08) !important; border-color: rgba(49,194,124,0.25) !important; color: var(--accent-primary-dark); }

.icon { font-size: 12px; }

.reader-body { flex: 1; display: flex; flex-direction: column; gap: var(--space-sm); overflow-y: auto; padding-left: var(--space-sm); border-left: 1px solid rgba(0,0,0,0.04); }

.meta-tags { display: flex; gap: var(--space-sm); font-size: var(--text-xs); }
.tag-id { background: rgba(191,90,242,0.1); color: var(--accent-purple); padding: 2px 8px; border-radius: var(--radius-full); font-weight: var(--weight-semibold); }
.tag-file { background: rgba(0,0,0,0.03); color: var(--text-tertiary); padding: 2px 8px; border-radius: var(--radius-full); }

.quote-box { min-height: 80px; }
.quote-text {
  margin: 0; padding: var(--space-md); background: var(--bg-canvas);
  border-left: 4px solid var(--accent-purple); border-radius: var(--radius-sm);
  font-size: var(--text-xs); color: var(--text-primary); line-height: var(--leading-relaxed);
  font-style: italic;
}

.nlp-analysis { border-top: 1px solid rgba(0,0,0,0.04); padding-top: var(--space-sm); }
.nlp-analysis h5 { margin: 0 0 6px; font-size: var(--text-xs); color: var(--text-secondary); }
.nlp-grid { display: flex; flex-direction: column; gap: 4px; }
.nlp-card { font-size: var(--text-xs); padding: 4px 8px; background: rgba(0,0,0,0.01); border-radius: var(--radius-xs); color: var(--text-secondary); }

/* Verdict */
.verdict-hud { flex: 1; display: flex; flex-direction: column; min-height: 0; }
.verdict-body { display: flex; flex-direction: column; height: 100%; min-height: 0; margin-top: var(--space-sm); }

.verdict-alert {
  display: flex; align-items: flex-start; gap: var(--space-sm);
  background: rgba(191,90,242,0.04); border: 1px solid rgba(191,90,242,0.1);
  padding: var(--space-sm) var(--space-md); border-radius: var(--radius-sm);
  margin-bottom: var(--space-md);
}
.verdict-alert p { margin: 0; font-size: var(--text-xs); line-height: var(--leading-normal); color: var(--text-secondary); }
.verdict-alert strong { color: var(--accent-purple); }
.pulse-dot { width: 6px; height: 6px; background: var(--accent-purple); border-radius: 50%; margin-top: 4px; flex-shrink: 0; animation: pulse-indicator 2s infinite; }

.evidence-checks { display: flex; flex-direction: column; gap: var(--space-sm); flex: 1; overflow-y: auto; }

.check-item { display: flex; gap: var(--space-sm); padding: var(--space-sm) var(--space-md); border-radius: var(--radius-sm); border: 1px solid rgba(0,0,0,0.02); }
.check-item.passed { background: rgba(49,194,124,0.02); border-color: rgba(49,194,124,0.06); }
.check-item.passed .circle { color: var(--accent-primary); }
.check-item.warning { background: rgba(0,0,0,0.01); }
.check-item.warning .circle { color: var(--text-tertiary); }

.circle { font-size: 14px; font-weight: var(--weight-bold); margin-top: 1px; }
.check-item h6 { margin: 0 0 2px; font-size: var(--text-xs); color: var(--text-primary); font-weight: var(--weight-medium); }
.check-item p { margin: 0; font-size: 10px; color: var(--text-secondary); line-height: var(--leading-tight); }

.action-dock { padding: var(--space-sm) 0; flex-shrink: 0; }
.export-btn {
  width: 100%; position: relative; overflow: hidden;
  background: linear-gradient(135deg, var(--accent-primary) 0%, var(--accent-blue) 100%);
  box-shadow: 0 4px 16px rgba(49,194,124,0.3);
  font-size: var(--text-sm); padding: 14px;
}
.export-btn:hover { box-shadow: 0 6px 22px rgba(49,194,124,0.5); transform: translateY(-2px); }

.btn-shine {
  position: absolute; top: 0; left: -100%; width: 60%; height: 100%;
  background: linear-gradient(90deg, transparent, rgba(255,255,255,0.2), transparent);
  transition: left 0.6s;
  pointer-events: none;
}
.export-btn:hover .btn-shine { left: 200%; }
</style>
