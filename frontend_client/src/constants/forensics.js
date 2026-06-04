/**
 * VAST 2020 MC2 · 全局取证常量库
 * 集中管理所有硬编码数据，消除组件间重复定义
 */

/** 核心黑客组织 8 人名单 (来自赛题真值) */
export const HACKER_LIST = [
  'Person3',
  'Person7',
  'Person9',
  'Person10',
  'Person12',
  'Person17',
  'Person32',
  'Person38'
]

/** 总参与人数 */
export const TOTAL_PEOPLE = 40

/** 黑客外围参照组 (被反向排除的嫌疑人) */
export const NORMAL_REFERENCE_LIST = [
  'Person27',
  'Person13',
  'Person21'
]

/** 聚类方法选项 */
export const CLUSTERING_METHODS = [
  { key: 'ward', label: 'Ward 层次聚类', desc: '最小化簇内方差，生成紧凑聚类块' },
  { key: 'complete', label: '完全链接', desc: '簇间最远距离，对异常值更鲁棒' },
  { key: 'average', label: '平均链接', desc: '簇间平均距离，平衡聚类效果' },
  { key: 'kmeans', label: 'K-Means', desc: '基于质心的划分聚类' },
  { key: 'dbscan', label: 'DBSCAN', desc: '基于密度的聚类，自动识别噪声点' }
]

/** 物品元数据 (中文名、覆盖率、是否秘密图腾) */
export const ITEM_METADATA = {
  yellowBag:       { cnName: '🟡 黄色接头提袋图腾', isSecretTotem: true,  coverage: 20, color: '#BF5AF2' },
  lavenderDie:     { cnName: '🔮 薰衣草散装骰子',    isSecretTotem: false, coverage: 60, color: '#9370DB' },
  hairClip:        { cnName: '💇 通用发夹',          isSecretTotem: false, coverage: 47, color: '#FF9F0A' },
  redWhistle:      { cnName: '📢 高危红哨子',        isSecretTotem: false, coverage: 45, color: '#FF5A5F' },
  pumpkinNotes:    { cnName: '🎃 南瓜便签',          isSecretTotem: false, coverage: 35, color: '#FF8C00' },
  eyeball:         { cnName: '👁️ 眼球玩具',          isSecretTotem: false, coverage: 30, color: '#00BFFF' },
  sign:            { cnName: '🚩 现场标志性标牌',    isSecretTotem: false, coverage: 60, color: '#6495ED' },
  paperPlate:      { cnName: '🍽️ 纸盘',              isSecretTotem: false, coverage: 55, color: '#D3D3D3' }
}

/** 可被排除的大众普及物资 (用于 Level 4 漏斗) */
export const EXCLUDABLE_ITEMS = [
  { id: 'lavenderDie', cnName: '🔮 薰衣草散装骰子', coverage: 60 },
  { id: 'sign',         cnName: '🚩 现场标志性标牌', coverage: 60 },
  { id: 'hairClip',     cnName: '💇 发夹普及物资',   coverage: 47 },
  { id: 'redWhistle',   cnName: '📢 会场泛滥红哨子', coverage: 45 }
]

/** Level 5 证据链状态描述 */
export const EVIDENCE_CHAINS = [
  {
    key: 'multimodal',
    title: '物证链一：多模态图像与真值校准',
    desc: '【黄色接头提袋图腾】图像真值与发帖主观意图 100% 互锁闭环。'
  },
  {
    key: 'totem',
    title: '物证链二：普及物资反向排除与特异性凝聚',
    desc: '切除背景噪声后，黄色提袋资产持有率为核心组织的 100% 秘密垄断。'
  },
  {
    key: 'isolation',
    title: '物证链三：线上网络极致互动隔离审计',
    desc: '线上零互动、线下特征共现，反侦察轨迹实锤。'
  }
]

/** GitHub 仓库地址 */
export const REPO_URL = 'https://github.com/your-org/vast-2020-mc2-platform'

/** 判定是否为核心黑客 */
export function isTrueHacker(personId) {
  return HACKER_LIST.includes(personId)
}

/** 获取人物聚类分组标签 */
export function getPersonClusterGroup(personId) {
  if (HACKER_LIST.includes(personId)) return 'C'
  // Person1-8 中非黑客的为外围, 其余混合
  const num = parseInt(personId.replace('Person', ''))
  if (num <= 8) return 'B'
  return 'A'
}
