import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

// 1. 显式引入全局卡片美学样式表
import './assets/global.css'

// 2. 物理初始化 Vue 根实例对象
const app = createApp(App)

// 3. 🚨 核心修正：必须先注册创建 Pinia 实体，将其激活注入全局生命周期
const pinia = createPinia()
app.use(pinia)

// 4. 紧接着注入二级目录渐进式路由中心
app.use(router)

// 5. 最终，当所有核心生态地基完全激活后，才执行 DOM 视口挂载
app.mount('#app')

console.log("🍏 Apple 视觉分析分析大屏终端生态骨架已完全按顺序挂载激活！")