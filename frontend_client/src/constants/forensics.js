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
  { key: 'ward', label: 'Ward Hierarchical', desc: 'Minimize intra-cluster variance, compact cluster blocks' },
  { key: 'complete', label: 'Complete Linkage', desc: 'Maximum inter-cluster distance, robust to outliers' },
  { key: 'average', label: 'Average Linkage', desc: 'Mean inter-cluster distance, balanced results' },
  { key: 'kmeans', label: 'K-Means', desc: 'Centroid-based partition clustering' },
  { key: 'dbscan', label: 'DBSCAN', desc: 'Density-based clustering, auto-identifies noise' }
]

/** Item metadata (name, coverage rate, secret totem flag) */
export const ITEM_METADATA = {
  yellowBag:       { cnName: 'Yellow Handoff Bag Totem', isSecretTotem: true,  coverage: 20, color: '#BF5AF2' },
  lavenderDie:     { cnName: 'Lavender Loose Dice',      isSecretTotem: false, coverage: 60, color: '#9370DB' },
  hairClip:        { cnName: 'Generic Hair Clip',        isSecretTotem: false, coverage: 47, color: '#FFB800' },
  redWhistle:      { cnName: 'High-Risk Red Whistle',    isSecretTotem: false, coverage: 45, color: '#FF3333' },
  pumpkinNotes:    { cnName: 'Pumpkin Sticky Notes',     isSecretTotem: false, coverage: 35, color: '#FF8C00' },
  eyeball:         { cnName: 'Eyeball Toy',              isSecretTotem: false, coverage: 30, color: '#00BFFF' },
  sign:            { cnName: 'Venue Marker Signage',     isSecretTotem: false, coverage: 60, color: '#6495ED' },
  paperPlate:      { cnName: 'Paper Plate',              isSecretTotem: false, coverage: 55, color: '#A0A0A0' }
}

/** Excludable mass-distributed items (Level 4 funnel) */
export const EXCLUDABLE_ITEMS = [
  { id: 'lavenderDie', cnName: 'Lavender Loose Dice',      coverage: 60 },
  { id: 'sign',         cnName: 'Venue Marker Signage',     coverage: 60 },
  { id: 'hairClip',     cnName: 'Hair Clip (Universal)',    coverage: 47 },
  { id: 'redWhistle',   cnName: 'Red Whistle (Flooded)',    coverage: 45 }
]

/** Level 5 evidence chain status descriptions */
export const EVIDENCE_CHAINS = [
  {
    key: 'multimodal',
    title: 'Chain I: Multi-Modal Image / Ground-Truth Calibration',
    desc: 'Yellow carry-bag totem image truth and post intent 100% interlock closed-loop.'
  },
  {
    key: 'totem',
    title: 'Chain II: Universal Material Reverse Elimination & Specificity',
    desc: 'After excising background noise, yellow bag asset holding is 100% core cell monopoly.'
  },
  {
    key: 'isolation',
    title: 'Chain III: Online Network Extreme Interaction Isolation Audit',
    desc: 'Online zero-interaction, offline feature co-occurrence. Counter-surveillance confirmed.'
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
