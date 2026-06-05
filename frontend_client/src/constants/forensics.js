/**
 * VAST 2020 MC2 · Global Forensics Constants Library
 * Centralized data — eliminates cross-component duplication
 * White-Hat Hacker Digital Forensics Platform
 */

/** Core hacker cell 8-person roster (ground truth) */
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

/** Total attendees */
export const TOTAL_PEOPLE = 40

/** Hacker periphery reference group (reverse-eliminated suspects) */
export const NORMAL_REFERENCE_LIST = [
  'Person27',
  'Person13',
  'Person21'
]

/** Clustering method options */
export const CLUSTERING_METHODS = [
  { key: 'ward', label: 'Ward 层次聚类', desc: '最小化簇内方差，紧凑聚类块' },
  { key: 'complete', label: '完全链接', desc: '最大化簇间距离，对离群值鲁棒' },
  { key: 'average', label: '平均链接', desc: '簇间平均距离，平衡结果' },
  { key: 'kmeans', label: 'K-Means', desc: '基于质心的划分聚类' },
  { key: 'dbscan', label: 'DBSCAN', desc: '基于密度的聚类，自动识别噪声' }
]

/** Item metadata (name, coverage rate, secret totem flag) */
export const ITEM_METADATA = {
  yellowBag:       { cnName: '黄色接头提袋图腾', isSecretTotem: true,  coverage: 20, color: '#BF5AF2' },
  lavenderDie:     { cnName: '薰衣草散装骰子',   isSecretTotem: false, coverage: 60, color: '#9370DB' },
  hairClip:        { cnName: '通用发夹',          isSecretTotem: false, coverage: 47, color: '#FFB800' },
  redWhistle:      { cnName: '泛滥红哨子',        isSecretTotem: false, coverage: 45, color: '#FF3333' },
  pumpkinNotes:    { cnName: '南瓜便利贴',        isSecretTotem: false, coverage: 35, color: '#FF8C00' },
  eyeball:         { cnName: '眼球玩具',          isSecretTotem: false, coverage: 30, color: '#00BFFF' },
  sign:            { cnName: '会场标识牌',        isSecretTotem: false, coverage: 60, color: '#6495ED' },
  paperPlate:      { cnName: '纸盘',              isSecretTotem: false, coverage: 55, color: '#A0A0A0' }
}

/** Excludable mass-distributed items (Level 4 funnel) */
export const EXCLUDABLE_ITEMS = [
  { id: 'lavenderDie', cnName: '薰衣草散装骰子',   coverage: 60 },
  { id: 'sign',         cnName: '会场标识牌',         coverage: 60 },
  { id: 'hairClip',     cnName: '通用发夹',           coverage: 47 },
  { id: 'redWhistle',   cnName: '泛滥红哨子',         coverage: 45 }
]

/** Level 5 evidence chain status descriptions */
export const EVIDENCE_CHAINS = [
  {
    key: 'multimodal',
    title: '物证链一：多模态图像与真值校准',
    desc: '黄色提袋图腾图像真值与发帖意图 100% 互锁闭环。'
  },
  {
    key: 'totem',
    title: '物证链二：普及物资反向排除与特异性凝聚',
    desc: '切除背景噪声后，黄色提袋持有率为核心组织 100% 垄断。'
  },
  {
    key: 'isolation',
    title: '物证链三：线上网络极致互动隔离审计',
    desc: '线上零互动、线下特征共现。反侦察行为已确认。'
  }
]

/** GitHub repository URL */
export const REPO_URL = 'https://github.com/your-org/vast-2020-mc2-platform'

/** Determine if person is a true hacker */
export function isTrueHacker(personId) {
  return HACKER_LIST.includes(personId)
}

/** Get person cluster group label */
export function getPersonClusterGroup(personId) {
  if (HACKER_LIST.includes(personId)) return 'C'
  const num = parseInt(personId.replace('Person', ''))
  if (num <= 8) return 'B'
  return 'A'
}
