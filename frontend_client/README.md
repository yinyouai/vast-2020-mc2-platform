# 🛰️ Multi-Layer Visual Analytics Platform for Automated Knowledge Graph Auditing and Cyber-Forensics (IEEE VAST Challenge 2020 MC2)

[![Framework: Vue 3](https://img.shields.io/badge/Framework-Vue_3-35495e?logo=vue.js)](https://vuejs.org/)
[![Bundler: Vite](https://img.shields.io/badge/Bundler-Vite-646CFF?logo=vite)](https://vitejs.dev/)
[![Graphics: ECharts 5](https://img.shields.io/badge/Graphics-ECharts_5-AA344D?logo=apache-echarts)](https://echarts.apache.org/)
[![State: Pinia](https://img.shields.io/badge/State-Pinia-60B5CC)](https://pinia.vuejs.org/)

---

## 📝 1. 引言与学术背景 (Introduction & Background)

在现代数字化取证与网络情报审计中，通过自然语言处理（NLP）和计算机视觉（CV）算法自发从非结构化开源数据中提取信息、构建知识图谱（如本赛题中的 **CatchNet**）已成为主流手段。然而，由于复杂多模态环境下的信号衰减及算法固有的混淆偏见，自动化模型极易产生大量的**假阳性虚警（False Positives）与认知噪声**。

本可视分析系统专为 **IEEE VAST Challenge 2020 Mini-Challenge 2 (MC2)** 设计。针对虚拟城市 Oceanus 安全峰会期间潜在的白帽黑客团伙密谋事件，本系统基于**“人在回路（Human-in-the-Loop, HITL）”**和**“协同质证（Cross-Validation）”**的分析哲学，构建了一套五层级联式可视分析审查流水线。系统摒弃了单调的硬编码文本话术，全面采用异构多图表平铺排开的纯数据驱动底盘（Multi-Chart Unified Dashboard），旨在帮助分析师高效截断算法不确定性，定位高危罪证。

---

## 🔬 2. 五层渐进式可视分析流水线架构 (Forensic Pipeline)

系统采用严谨的漏洞拓扑（Funnel Topology）架构，将庞杂的多模态知识图谱数据流，通过五个紧密解耦且状态互锁（Pinia-driven Multi-Chart Synchronization）的层级视窗进行收敛提纯：