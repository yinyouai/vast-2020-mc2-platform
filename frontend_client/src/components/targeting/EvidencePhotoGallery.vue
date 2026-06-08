<template>
  <section class="panel evidence-gallery-panel">
    <div class="panel-header">
      <div><span class="section-kicker">图片级证据</span><h4 class="panel-title">成员证据浏览器</h4>
        <p class="visible-subtitle">选择成员和图片，核对模型命中、人工补标与文本支持。</p></div>
      <span class="data-chip">{{ totalImages }} 张已核验</span>
    </div>
    <div v-if="activeMember" class="evidence-browser">
      <nav class="member-rail" aria-label="最终成员">
        <button v-for="member in evidence" :key="member.person_id" :class="{active:member.person_id===activeMember.person_id}" @click="selectMember(member)">
          <span>{{ member.person_id.replace('Person','') }}</span><div><strong>{{ member.person_id }}</strong><small>{{ member.occurrence_count }} 图 · {{ member.raw_detected?'模型检出':'人工补标' }}</small></div>
        </button>
      </nav>
      <div class="image-viewer">
        <div v-if="activeImage" class="primary-image">
          <img :src="`${STATIC_BASE}${activeImage}`" :alt="`${activeMember.person_id} ${store.activeTotem} 证据`" />
          <span>{{ activeImageId }}</span>
        </div>
        <div v-else class="primary-image text-only-placeholder">
          <span>📝 纯文本证据 / 无图</span>
          <p>该成员（如 {{ activeMember.person_id }}）仅存在文字描述，或照片未找到有效实体。</p>
        </div>
        <div v-if="activeMember.image_paths.length > 0" class="thumbnail-strip">
          <button v-for="(path,index) in activeMember.image_paths" :key="path" :class="{active:path===activeImage}" @click="activeImage=path">
            <img :src="`${STATIC_BASE}${path}`" :alt="`${activeMember.image_ids[index]} 缩略图`" loading="lazy"/>
            <b :class="activeMember.raw_detection_images.includes(activeMember.image_ids[index])?'hit':'added'">
              {{ activeMember.raw_detection_images.includes(activeMember.image_ids[index])?'命中':'补标' }}
            </b>
          </button>
        </div>
      </div>
      <aside class="member-inspector">
        <div class="member-title"><span>当前成员</span><strong>{{ activeMember.person_id }}</strong><small>{{ activeMember.source }}</small></div>
        <div class="fact-grid">
          <article><span>图片</span><b>{{ activeMember.occurrence_count }}</b></article><article><span>模型命中</span><b>{{ activeMember.raw_detection_images.length }}</b></article>
          <article><span>最高分</span><b>{{ activeMember.raw_max_score || '—' }}</b></article><article><span>文本</span><b>{{ activeMember.text_snippets.length }}</b></article>
        </div>
        <div class="detection-progress"><div><span>模型图片召回</span><b>{{ detectionRate }}%</b></div><i><em :style="{width:`${detectionRate}%`}"></em></i></div>
        <div class="text-evidence"><span>文本交叉验证</span><blockquote v-for="text in activeMember.text_snippets" :key="text">{{ text }}</blockquote>
          <p v-if="!activeMember.text_snippets.length">没有直接文本提及，结论由重复图片证据支撑。</p></div>
      </aside>
    </div>
  </section>
</template>
<script setup>
import { computed,ref,watch } from 'vue'
import { STATIC_BASE,useDashboardStore } from '../../store/dashboard'
const store=useDashboardStore();const activeImage=ref('')
const evidence=computed(()=>store.finalEvidence);const totalImages=computed(()=>evidence.value.reduce((sum,item)=>sum+item.image_ids.length,0))
const activeMember=computed(()=>evidence.value.find((item)=>item.person_id===store.selectedPersonId)||evidence.value[0]||null)
const activeImageId=computed(()=>{const index=activeMember.value?.image_paths.indexOf(activeImage.value)??-1;return activeMember.value?.image_ids[index]||''})
const detectionRate=computed(()=>activeMember.value?.image_ids.length?Math.round(activeMember.value.raw_detection_images.length/activeMember.value.image_ids.length*100):0)
const selectMember=(member)=>{store.selectPerson(member.person_id,member.primary_image_id);activeImage.value=member.image_paths[0]||''}
watch(activeMember,(member)=>{if(member&&!member.image_paths.includes(activeImage.value))activeImage.value=member.image_paths[0]||''},{immediate:true})
</script>
<style scoped>
.section-kicker{color:var(--subtle);font-size:.7rem;font-weight:800}.visible-subtitle{display:block!important;margin:5px 0 0;color:var(--muted);font-size:.76rem}
.evidence-browser{display:grid;grid-template-columns:210px minmax(0,1fr) 290px;gap:14px}.member-rail{display:grid;gap:6px;align-content:start;max-height:570px;overflow:auto}.member-rail button{display:grid;grid-template-columns:34px 1fr;align-items:center;gap:8px;min-height:58px;padding:7px;border: none;border-radius: 12px;color:inherit;text-align:left;background: var(--surface-2)}.member-rail button.active{border-color:var(--accent);background: var(--surface-glow)}.member-rail button>span{display:grid;place-items:center;width:34px;height:34px;border-radius: 12px;color:var(--accent);background: var(--surface-glow);font-weight:900}.member-rail strong,.member-rail small{display:block}.member-rail small{margin-top:3px;color:var(--muted);font-size:.68rem}
.image-viewer{min-width:0}.primary-image{position:relative;display:grid;place-items:center;height:460px;overflow:hidden;border: none;border-radius: 12px;background: var(--surface-2)}.primary-image img{width:100%;height:100%;object-fit:contain}.primary-image>span{position:absolute;left:10px;bottom:10px;padding:5px 8px;border-radius: 12px;color: var(--text);background:rgba(23,50,77,.8);font-size:.7rem}
.text-only-placeholder { display:flex; flex-direction:column; justify-content:center; align-items:center; color:var(--muted); text-align:center; padding: 2rem; }
.text-only-placeholder span { position:static !important; background:none !important; color:var(--subtle) !important; font-size:1.5rem !important; margin-bottom:10px; }
.thumbnail-strip{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:7px;margin-top:8px}.thumbnail-strip button{position:relative;overflow:hidden;min-height:70px;padding:0;border:2px solid transparent;border-radius: 12px;background: var(--surface-3)}.thumbnail-strip button.active{border-color:var(--accent)}.thumbnail-strip img{width:100%;height:70px;object-fit:cover}.thumbnail-strip b{position:absolute;right:3px;top:3px;padding:3px 5px;border-radius: 12px;color: var(--text);font-size:.62rem}.thumbnail-strip .hit{background:var(--success)}.thumbnail-strip .added{background:var(--accent)}
.member-inspector{display:grid;gap:10px;align-content:start}.member-title,.text-evidence,.detection-progress{padding:12px;border: none;border-radius: 12px;background: var(--surface-2)}.member-title span,.member-title strong,.member-title small{display:block}.member-title span,.text-evidence>span{color:var(--subtle);font-size:.68rem;font-weight:800}.member-title strong{margin:6px 0;font-size:1.3rem}.member-title small{color:var(--muted)}
.fact-grid{display:grid;grid-template-columns:1fr 1fr;gap:7px}.fact-grid article{padding:9px;border: none;border-radius: 12px;background: var(--surface)}.fact-grid span,.fact-grid b{display:block}.fact-grid span{color:var(--subtle);font-size:.66rem}.fact-grid b{margin-top:4px;font-variant-numeric:tabular-nums}
.detection-progress>div{display:flex;justify-content:space-between;color:var(--muted);font-size:.72rem}.detection-progress i{display:block;height:7px;margin-top:8px;border-radius: 12px;background:#dfe7ef;overflow:hidden}.detection-progress em{display:block;height:100%;background:var(--success)}
.text-evidence blockquote,.text-evidence p{display:block!important;margin:8px 0 0;padding-left:8px;border-left:2px solid var(--accent);color:var(--muted);font-size:.72rem;line-height:1.5}
@media(max-width:1180px){.evidence-browser{grid-template-columns:180px 1fr}.member-inspector{grid-column:1/-1;grid-template-columns:repeat(3,1fr)}}
@media(max-width:760px){.evidence-browser{grid-template-columns:1fr}.member-rail{grid-template-columns:repeat(2,1fr);max-height:none}.primary-image{height:340px}.member-inspector{grid-template-columns:1fr}}
</style>
