# 🛰️ Multi-Layer Visual Analytics Platform for Automated Knowledge Graph Auditing and Cyber-Forensics (IEEE VAST Challenge 2020 MC2)

[![Framework: Vue 3](https://img.shields.io/badge/Framework-Vue_3-35495e?logo=vue.js)](https://vuejs.org/)
[![Bundler: Vite](https://img.shields.io/badge/Bundler-Vite-646CFF?logo=vite)](https://vitejs.dev/)
[![Graphics: ECharts 5](https://img.shields.io/badge/Graphics-ECharts_5-AA344D?logo=apache-echarts)](https://echarts.apache.org/)
[![State: Pinia](https://img.shields.io/badge/State-Pinia-60B5CC)](https://pinia.vuejs.org/)

---

## 📝 1. 引言与学术背景 (Introduction & Background)

在现代数字化取证与网络情报审计中，通过自然语言处理（NLP）和计算机视觉（CV）算法自发从非结构化开源数据中提取信息、构建知识图谱（如本赛题中的 **CatchNet**）已成为主流手段。然而，由于复杂多模态环境下的信号衰减及算法固有的混淆偏见，自动化模型极易产生大量的**假阳性虚警（False Positives）与认知噪声**。

本可视分析系统专为 **IEEE VAST Challenge 2020 Mini-Challenge 2 (MC2)** 设计。针对虚拟城市 Oceanus 安全峰会期间潜在的白帽黑客团伙密谋事件，本系统基于**“人在回路（Human-in-the-Loop, HITL）”**和**“协同质证（Cross-Validation）”的分析哲学，构建了一套五层级联式可视分析审查流水线。系统摒弃了单调的硬编码文本话术，全面采用异构多图表平铺排开的纯数据驱动底盘（Multi-Chart Unified Dashboard），旨在帮助分析师高效截断算法不确定性，定位高危罪证。

---

## 🔬 2. 五层渐进式可视分析流水线架构 (Forensic Pipeline)

系统采用严谨的漏洞拓扑（Funnel Topology）架构，将庞杂的多模态知识图谱数据流，通过五个紧密解耦且状态互锁（Pinia-driven Multi-Chart Synchronization）的层级视窗进行收敛提纯：




### 🛰️ LAYER 01: 计算机视觉模型不确定性多特征审计大厅 (`ModelAuditingView.vue`)
* **学术内涵**：响应 **Task 1** 需求，量化审计自动化 CV 模型因像素反光或物理轮廓模糊产生的混淆退化。
* **异构图表群设计**：
  * **全局动态置信度阀门 (Score Threshold 滑块)**：系统输入级总开关，动态截断低可信度机器噪声。
  * **算法性能雷达图 (Radar Chart)**：实时重算并呈现全局准确率（Accuracy）、F1-Score、查全率（Recall）与查准率（Precision）的演变，展示模型收敛过程。
  * **FP 噪声波形消融折线图 (Line Chart)**：绘制假阳性虚警率随阈值爬升而陡峭坍塌的消融数学曲线。

### 🎨 LAYER 02 & 03: 人在回路真值校准与冲突优先级重排 (`CorrectionCanvas.vue` / `ConflictPriorityQueue.vue`)
* **学术内涵**：响应 **Task 2 & 3**。当自动化图谱提取的“图像语义”与“发帖文本”发生深度对立冲突时，系统基于不一致性熵值计算对冲突进行优先级风险排序，引导分析师通过交互画布实施人在回路的物理坐标重订与标签重绑定（真值倒灌）。

### 🔮 LAYER 04: 全员泛滥物资特征削波与反向排除中枢 (`TotemFilterView.vue`)
* **学术内涵**：响应 **Task 4**。通过全局社会覆盖率削波，反向逼迫低共现率的特异性犯罪图腾显现。
* **异构图表群设计**：
  * **大众物资反向放逐控制台 (`TotemEliminationPanel.vue`)**：提供高持率物资复选矩阵（散装骰子 60%、通用发夹 47%、泛滥红哨子 45%）。
  * **社会覆盖率削波柱状图 (`TotemBarChart.vue`)**：直观展示资产占有率，点击放逐时相关物资柱体发生逆向波形塌陷。
  * **多维资产交叉平行坐标空间 (`TotemSankeyTunnel.vue`)**：经典的高维多特征穿透图表。当大众礼品被剔除后，全场 40 人的多维持有线在其他坐标轴强制归零，最终你会清晰观察到<b>有 8 条高危数据线，在【🎒 秘密黄色提袋】那一轴上展现出 100% 绝对垄断的高度凝聚收敛</b>。

### 🛡️ LAYER 05: 隐形社交网络疏离审计与骨干终审定案大厅 (`CyberForensicsView.vue`)
* **学术内涵**：响应 **Task 5** 最核心的多模态叙事还原诉求（Text Narratives），将线上行为伪装与线下真实物理轨迹实施互锁合拢。
* **异构图表群设计**：
  * **隐形社交零提及真空热力图 (`SocialIsolationMatrix.vue`)**：展现 40 名目标的两两线上互动频次。核心组织交汇处呈现大面积死黑的“零提及冷点盲区”，揭露其特意规避线上通讯的情报规避行为。
  * **NLP 独立非结构化文本特征词频气泡图 (`ProvenanceNarrative.vue` - 组件11)**：双轨制线索推荐池。支持自由下钻探索嫌疑目标的非结构化日记（`text1.txt`），点击不同目标时，气泡通过空间缓动粒子动效动态变幻，喷涌出“线上绝对缄默”、“暗号集结”等潜在主观串供实体词云。
  * **全案证据四维特征偏离度雷达判定图 (`ProvenanceNarrative.vue` - 组件12)**：整合多模态图像矛盾度、物资特异垄断率、线上社交隔离度、独立纯文本契合率 4 维严谨科学指标，输出清晰的几何偏离度面积。


## 🚨 3. 最终学术发现与定案宣判 (Key Findings & Verdict)

经过平台全链路可视分析证据链的交叉质证与双向物理互锁，得出最终毫无争议的学术裁决：

1. **白帽黑客核心犯罪组织 8 人骨干完整名单确凿抓取**：
   $$\text{Hacker Group} = \{ \text{Person3}, \text{Person7}, \text{Person9}, \text{Person10}, \text{Person12}, \text{Person17}, \text{Person32}, \text{Person38} \}$$
   * **研判定论**：该 8 人团伙在物理空间展现出 100% 的**核心物资特异性共同持有（黄色接头手提袋图腾）**；但在网络空间却展现出违反正常自然人交际规律的**社交媒体互动频次绝对归零（线上隐形真空防线）**。线上刻意装作互不认识以逃避情报监控，线下通过资产对齐完成物理面基。铁证如山，全案定罪。

2. **外围受牵连无辜人员反向洗白排除（以 Person27 为典型科学参照）**：
   * **研判定论**：**Person27** 晒出的网格笔记本资产，由于机器算法的假阳性虚警在层级二引发数据污染。经过人在回路校准后发现：笔记本在层级四属于全场普遍合法分发的公共物资，不具备特异性指征。且在层级五社交审计中，Person27 的线上提及与技术交流完全符合自然人健康的基准正态分布。其各项高危嫌疑雷达多边形面积全面内缩归零，**系统对其执行 100% 反向洗白，顺利排除嫌疑，回归无害组**。

---

## 📁 4. 项目关键工程目录树结构 (Directory Structure)

项目工程各组件各司其职，模块边界清晰，杜绝多图表挂载死锁及实例冲突：

```text
vast-2020-mc2-platform
│
├── challenge_analysis/                     # 离线分析与证据生成层
│   ├── data_cleaner.py
│   ├── text_mining.py
│   ├── model_auditor.py
│   ├── community_clustering.py
│   ├── totem_elimination.py
│   └── run_pipeline.py
│
├── backend_service/                        # 分析服务层
│   ├── app.py
│   ├── config.py
│   ├── requirements.txt
│   └── core_engines/
│
├── frontend_client/                        # 可视分析交互层
│
│   ├── src/
│   │
│   ├── assets/
│   ├── router/
│   ├── store/
│   │   └── dashboard.js
│   │
│   ├── views/
│   │   ├── DataExplorationView.vue
│   │   ├── ModelAuditingView.vue
│   │   ├── CommunityClusteringView.vue
│   │   ├── TotemFilterView.vue
│   │   └── CyberForensicsView.vue
│   │
│   └── components/
│       ├── auditing/
│       ├── interaction/
│       └── targeting/
│
└── raw_data/
    ├── MC2-Image-Data/               # 40个嫌疑人的图片、CSV和TXT碎片数据
    └── i3_new_data.json              # 清洗对齐、打好文本锚定真值后的多模态 Master JSON 主包
```

---

## 🏃‍♂️ 5. 项目部署与运行指南 (Deployment & Usage)

### 5.1 环境前置要求

* **Node.js**：建议安装 `Node.js 16.x` 或 `18.x`（LTS 版本）。
* **浏览器**：建议使用现代化浏览器（如 Chrome, Edge, Safari）以确保高级高斯模糊 CSS 滤镜与 Canvas 3D 动画性能完美释放。

### 5.2 部署步骤

1. 打开终端或命令提示符，单兵深入并定位到你本地的前端客户端物理目录中：
```bash
cd "./vast-2020-mc2-platform/frontend_client"

```


2. 执行依赖项全量本地下载与安装（此过程将无缝构建本地 PostCSS 与数据依赖骨架）：
```bash
npm install

```


3. 启动基于 Vite 的高性能毫秒级开发者本地服务器：
```bash
npm run dev

```


4. **系统访问与实战下钻**：
打开浏览器，访问命令行中提示的本地开发回环地址（通常为 `http://localhost:5173/`）。
* 使用顶部清爽的 极简导航条，即可在页面一至五之间进行无错的丝滑跨页面自由穿透切页。
* *页面四实战技巧*：在控制台漏斗中全量勾选放逐散装骰子、通用发夹、泛滥红哨子，即可观察平行坐标轴的几何塌陷；此时双击【黄色提袋】节点，即可一键下钻穿透调阅第四层级像素级现场照片物证弹窗！
* *页面五实战技巧*：在最上方矩阵中点击死黑冷点方格，底部的气泡词云图与四维判定雷达图将产生逼真的同频动态数据重算流变。



---

