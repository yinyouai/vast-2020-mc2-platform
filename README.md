# VAST 2020 MC2 多模态取证分析平台

本项目分析 IEEE VAST Challenge 2020 Mini-Challenge 2 的 40 名候选人数据。系统不把某个物品或 8 人名单写死在前端，而是沿着以下证据链逐步得到结论：

```text
原始 YOLO 预测
  -> 模型能力审计
  -> 人工确认、误报驳回与漏检补标
  -> 校正后人物-物品矩阵
  -> 候选物品评分
  -> 逐人图片与文本验证
  -> 最终 8 人组
```

## 最终结论

当前校正数据和评分规则得到：

```text
暗号物品：canadaPencil（加拿大枫叶铅笔）

8 位嫌疑人：
Person4, Person7, Person14, Person15,
Person22, Person25, Person35, Person39
```

该结果不是由前端常量返回。`ForensicAnalysisEngine.analysis_summary()` 会遍历所有校正候选，先筛选“拥有者人数恰好为 8 且每位至少出现 2 次”的候选，再按综合分排序。当前只有 `canadaPencil` 同时满足两项硬条件。

当前可复算的关键结果：

| 指标 | 结果 |
|---|---:|
| 候选人数 | 40 |
| 人员图片 | 907 |
| 训练图片及人员图片合计 | 1423 |
| YOLO 检测 CSV | 907 |
| 文本文件 | 193 |
| 训练类别 | 43 |
| 原始预测实际出现类别 | 22 |
| 缺失类别 | 21 |
| `yellowBag` 高阈值框 | 12 |
| `yellowBag` 复核结果 | 12 个均为误报，假设失效 |
| `canadaPencil` 校正拥有者 | 8 |
| `canadaPencil` 已核验图片 | 25 |
| 每位成员最少图片数 | 2 |
| 具有直接文本支持的成员 | 3 |
| 综合分 | 0.9375 |

## 为什么旧结论是错的

旧实现以 `score >= 0.55` 过滤原始 YOLO 预测，发现 `yellowBag` 恰好落到 8 人，于是直接把该标签和 8 人写进前端。这个过程有两个根本问题：

1. 高置信度不等于分类正确。逐图检查后，12 个高阈值 `yellowBag` 框全部是误报。
2. “恰好 8 人”不代表稳定暗号。若某候选只在每人一张图中偶然出现，证据强度不足。

因此当前系统保留这条历史路径，但只把它显示为 `invalidated` 的原始假设，不再作为结论。

## 与参考作品的差异

项目改进参考了以下公开分析：

- [TTU Nguyen MC2](https://huyen-nguyen.github.io/VAST2020mc2/TTU-Nguyen-MC2/)
- [ASU VAST 2020 MC2](https://vacommunity.org/VAST+Challenge+2020+MC2)

参考作品的重要启发是：不能只调检测阈值，而要人工修正候选物品分布，并检查每位拥有者是否重复出现。当前项目据此增加了独立校正层和逐图证据层。

运行时不会请求参考网站，也不会从网页读取答案。参考分布被作为人工审核记录写入 `raw_data/human_corrections.json`；最终候选、分数和名单仍由本地代码重新计算。

证据强度需要区分：

- `canadaPencil`：已定位 8 人的 25 张具体图片，并核对模型命中与漏检。
- 其余 8 至 10 人近邻候选：当前保存人工校正后的人员分布与出现次数，用于候选排除比较；尚未全部补齐逐图证据。

## 数据分层

系统明确区分三层数据，避免人工操作污染原始模型结果。

### 1. 原始预测层

文件：`raw_data/i3_new_data.json`

包含：

- 40 人的图片路径；
- caption 与独立文本；
- YOLO 检测框、标签和置信度；
- 损坏框标记。

该文件是只读分析输入。人工复核不会修改其中的标签或分数。

### 2. 人工校正层

文件：`raw_data/human_corrections.json`

包含：

- `corrected_labels`：人工确认的候选物品分布；
- 每个人的 `image_ids` 和 `occurrence_count`；
- `rejected_predictions`：被判定为误报的原始框；
- `audit_log`：交互式确认、补标、修改或驳回记录；
- `target_group_size`：题目给出的组织规模先验，当前为 8。

### 3. 推断结果层

文件：`raw_data/analysis_results.json`

由流水线或 `/api/export_analysis` 生成，包含：

- 原始假设状态；
- 完整候选排名；
- 最终物品和人员组；
- 每位成员的图片、原始模型命中、文本支持；
- 非成员排除记录；
- 各分析阶段及其数据依据。

该文件是输出，可以重新生成。

## 计算过程

### Step 1：读取原始多模态快照

`backend_service/core_engines/data_provider.py` 的 `load_master_snapshot()` 读取 `i3_new_data.json`。清洗脚本 `challenge_analysis/data_cleaner.py` 可从原始人员目录重新构造该快照：

```text
PersonX_N.jpg
PersonX_N.csv
PersonX_Ncaption.txt
PersonX_textN.txt
```

损坏或缺字段的检测框被标为 `unknown` 且分数归零，后续不会进入有效预测。

当前主流水线默认使用已经生成的快照，避免每次分析覆盖人工整理后的 caption。只有需要从原始目录重建数据时，才单独运行 `data_cleaner.py` 和 `text_mining.py`。

### Step 2：审计原始模型

核心文件：`backend_service/core_engines/analysis_engine.py`

`model_audit()` 完成：

1. 统计各标签置信度五数概括；
2. 比较 43 个训练类别与 22 个实际输出类别；
3. 列出 21 个模型完全未输出的类别；
4. 计算真实检测框中心分布；
5. 以当前候选排名第一名（本数据为 `canadaPencil`）的人工校正拥有者为人员级真值，计算 precision、recall 和 F1；
6. 生成多个阈值下的真实指标曲线。

当前未阈值过滤的人员级结果为：

```text
canadaPencil precision = 0.1935
canadaPencil recall    = 0.7500
```

这说明模型找到了 8 位真实拥有者中的 6 位，但同时把许多非成员也预测为 `canadaPencil`。因此不能直接使用原始预测人员集合。

### Step 3：否定 `yellowBag` 原始假设

`raw_hypothesis(threshold=0.55)` 自动寻找拥有者人数最接近目标规模的高阈值原始候选；当前数据选中 `yellowBag`：

```text
8 位人员
12 个检测框
```

`human_corrections.json` 中逐框保存了复核结果。12 个框全部位于 `rejected_predictions`，所以状态计算为：

```python
status = "invalidated"
```

这一步保留旧方案的可追溯性，但阻止其继续进入校正矩阵。

### Step 4：建立人工校正分布

校正层记录 9 个接近目标人数的候选：

| 候选 | 拥有者 | 最少出现次数 | 是否恰好 8 人 |
|---|---:|---:|---|
| `canadaPencil` | 8 | 2 | 是 |
| `rainbowPens` | 8 | 1 | 是 |
| `rubiksCube` | 8 | 1 | 是 |
| `blueSunglasses` | 9 | 2 | 否 |
| `noisemaker` | 9 | 1 | 否 |
| `pinkEraser` | 9 | 1 | 否 |
| `lavenderDie` | 9 | 1 | 否 |
| `metalKey` | 10 | 1 | 否 |
| `miniCards` | 10 | 1 | 否 |

`Person15` 与 `Person22` 的加拿大铅笔属于重要漏检补标。它们说明只依赖模型召回会丢失真实成员。

### Step 5：构造两种人物-物品矩阵

系统提供两套矩阵。

#### 原始矩阵

`raw_matrix(threshold, excluded_items)` 使用：

```math
R_{p,i}(\tau)=
\sum_b 1[label(b)=i \land score(b)\ge\tau \land b\notin rejected]
```

特点：

- 受前端阈值影响；
- 保留原始模型不确定性；
- 已确认误报不再计入；
- 用于比较模型修正前结构。

#### 校正矩阵

`corrected_matrix(excluded_items)` 使用人工记录的 `occurrence_count`：

```math
C_{p,i}=corrected\_occurrence\_count(p,i)
```

特点：

- 不使用置信度阈值；
- 包含人工漏检补标；
- 用于候选评分和最终推断。

两种矩阵都对人员轴和物品轴执行 Ward 层次聚类重排。聚类仅改变展示顺序，不决定谁进入最终 8 人组。

### Step 6：候选评分

`candidate_rankings()` 为每个校正候选计算：

```math
specificity = max(0, 1 - |ownerCount-8|/8)
```

```math
stability = count(occurrenceCount >= 2) / ownerCount
```

```math
visual = min(1, evidenceImageCount / (ownerCount * 2))
```

```math
text = textSupportedOwnerCount / ownerCount
```

综合分：

```math
score =
0.40*specificity +
0.35*stability +
0.15*visual +
0.10*text
```

若拥有者人数不等于 8：

```math
score = score * 0.72
```

当前排名：

| 排名 | 候选 | 人数 | 最少次数 | 分数 |
|---:|---|---:|---:|---:|
| 1 | `canadaPencil` | 8 | 2 | 0.9375 |
| 2 | `blueSunglasses` | 9 | 2 | 0.5280 |
| 3 | `rainbowPens` | 8 | 1 | 0.4000 |
| 4 | `rubiksCube` | 8 | 1 | 0.4000 |
| 5 | `noisemaker` | 9 | 1 | 0.2680 |
| 6 | `lavenderDie` | 9 | 1 | 0.2600 |
| 7 | `pinkEraser` | 9 | 1 | 0.2600 |
| 8 | `metalKey` | 10 | 1 | 0.2160 |
| 9 | `miniCards` | 10 | 1 | 0.2160 |

最终选择先应用硬条件：

```python
exact_target_size is True
min_occurrence >= 2
```

再从通过者中取最高分。这里不是简单把最高分标签写死为 `canadaPencil`；修改校正分布后，候选排名和最终结果会自动重算。

### Step 7：逐人证据验证

`evidence_for()` 对最终候选的每位成员生成：

- 人员 ID；
- 全部核验图片 ID 和静态路径；
- 重复出现次数；
- 模型是否曾检出；
- 模型最高分；
- 模型实际命中的图片；
- caption 或独立文本中的直接支持；
- 标注来源和困难样本标记。

当前图片证据：

| 人员 | 图片 ID | 数量 |
|---|---|---:|
| Person4 | 21, 22, 23, 24 | 4 |
| Person7 | 1, 14, 15 | 3 |
| Person14 | 8, 9, 10, 16, 17 | 5 |
| Person15 | 1, 2 | 2 |
| Person22 | 3, 5 | 2 |
| Person25 | 9, 10, 11 | 3 |
| Person35 | 7, 8 | 2 |
| Person39 | 3, 4, 11, 12 | 4 |

文本直接支持包括：

- Person14 caption 提到 maple leaf pencil；
- Person35 独立文本提到 maple leaf pencil；
- Person39 独立文本提到 Canada souvenir 与削铅笔。

文本不是每位成员都必须具备的硬条件，因为图片已经是主要证据；它作为额外交叉验证进入 10% 评分项。

### Step 8：非成员排除

`exclusion_evidence()` 检查不在最终组中、但模型曾预测过 `canadaPencil` 的人员。前端展示其最高分和图片 ID，并明确说明：

```text
模型曾预测该物品，但人工校正分布未确认其为真实拥有者。
```

这比只展示正例更完整，因为它同时回答“为什么不是其他人”。

## 项目结构

```text
vast-2020-mc2/
├── README.md
├── challenge_analysis/
│   ├── run_pipeline.py           # 可复现总调度
│   ├── data_cleaner.py           # 原始目录转主快照
│   ├── text_mining.py            # caption 文本写入与简单锚定
│   ├── model_auditor.py          # 调用统一引擎输出模型审计
│   ├── community_clustering.py   # 输出校正或原始矩阵
│   └── totem_elimination.py      # 输出候选排名与最终结果
├── backend_service/
│   ├── app.py                    # Flask API 与图片静态服务
│   ├── config.py                 # 统一绝对路径配置
│   ├── requirements.txt
│   ├── test_analysis.py          # 核心结论与 API 回归测试
│   └── core_engines/
│       ├── analysis_engine.py    # 审计、矩阵、评分、证据主引擎
│       ├── data_provider.py      # 原始层和校正层读写
│       └── cluster_engine.py     # 旧矩阵引擎，保留兼容
├── frontend_client/
│   ├── package.json
│   ├── vite.config.js
│   └── src/
│       ├── App.vue
│       ├── router/index.js
│       ├── store/dashboard.js    # API 状态与交互动作
│       ├── views/                # 五层分析页面
│       └── components/
│           ├── auditing/
│           ├── interaction/
│           ├── process/
│           └── targeting/
├── raw_data/
│   ├── i3_new_data.json          # 原始预测主快照
│   ├── human_corrections.json    # 独立人工校正层
│   ├── analysis_results.json     # 可重新生成的推断结果
│   └── MC2-Image-Data/
│       ├── Person1 ... Person40
│       └── TrainingImages/
└── others/                       # 原始参考/旧版本副本，不参与运行
```

## 后端 API

### `GET /api/model_evaluation`

返回：

- 每类置信度五数概括；
- 训练/预测类别覆盖；
- 人员级 precision 与 recall；
- 阈值曲线；
- 真实检测框中心点。

### `POST /api/distribution_matrix`

请求：

```json
{
  "data_source": "corrected",
  "score_threshold": 0.55,
  "excluded_items": []
}
```

`data_source` 可为：

- `raw`：原始预测矩阵；
- `corrected`：人工校正矩阵。

### `GET /api/analysis_summary`

返回候选排名、失效假设、最终结果、逐人证据和排除证据。

### `GET /api/review_queue`

返回 25 张加拿大铅笔证据图和 12 个黄色包误报样本。状态包括：

- `confirmed`：当前图片被模型正确检出；
- `added`：模型在当前图片漏检，人工补标；
- `rejected`：原始预测被人工驳回；
- `unreviewed`：尚未复核。

### `POST /api/update_label`

支持：

- `confirm`：确认现有检测；
- `add`：补录漏检；
- `modify`：驳回旧框并添加新标签；
- `reject` / `delete`：驳回原始框或移除人工补标。

所有操作写入 `human_corrections.json`，不覆盖 `i3_new_data.json`。

### `GET /api/export_analysis`

重新计算并写入 `raw_data/analysis_results.json`。

## 前端五层可视化

### 第一层：模型审计

路由：`/task1_auditing`

- 真实置信度箱线图；
- 43 个训练类别与 22 个预测类别覆盖；
- 真实检测框空间散点；
- `canadaPencil` 人员级 precision/recall/F1 阈值曲线；
- `yellowBag` 假设失效状态。

这里不展示无法由现有真值计算的全局 Accuracy，也不生成随机密度点。

### 第二层：人工复核

路由：`/task2_correction`

- 直接读取后端复核队列；
- 展示具体图片、原始标签、校正标签和文本；
- 区分模型命中、漏检补标、误报驳回；
- 操作通过 `/api/update_label` 持久化；
- 展示 Raw prediction、Human correction、Inference usage 三层对照。

### 第三层：人物-物品矩阵

路由：`/task3_clustering`

- 可切换原始预测与人工校正矩阵；
- 原始矩阵受阈值影响；
- 校正矩阵用于最终分析；
- 空单元保持 0，不补合成高亮块；
- 行列使用 Ward 聚类重排；
- 点击有对应证据的单元可回到复核层。

### 第四层：候选评分

路由：`/task4_totem`

- 候选列表直接来自 `candidate_rankings`；
- 展示人数、最少出现次数、稳定率、文本支持和综合分；
- 完整比较 9 个近邻候选；
- 证据弹窗读取后端最终结果和理由；
- 勾选排除只影响矩阵观察，不篡改评分依据。

### 第五层：最终验证

路由：`/task5_verdict`

- 8 位成员逐人切换；
- 展示每人的全部证据图片；
- 每张图标明模型命中或人工补标；
- 展示重复出现次数、最高模型分和文本片段；
- 展示最终评分理由；
- 展示模型误检的非成员排除项。

原项目没有可复算的人际社交边数据，因此当前版本删除了模拟社交树和合成社交矩阵，不再用不存在的数据证明“社交隔离”。

## 环境与安装

建议：

```text
Python >= 3.10
Node.js >= 18
npm >= 9
```

### 安装 Python 依赖

```powershell
cd D:\vast-2020-mc2
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r backend_service\requirements.txt
```

### 安装前端依赖

```powershell
cd D:\vast-2020-mc2\frontend_client
npm install
```

## 运行

### 1. 运行完整分析

可以从项目根目录直接运行：

```powershell
cd D:\vast-2020-mc2
python challenge_analysis\run_pipeline.py
```

脚本使用绝对项目路径，不依赖当前工作目录。它不会覆盖原始预测快照，最终会写入：

```text
raw_data\analysis_results.json
```

### 2. 运行后端

```powershell
cd D:\vast-2020-mc2\backend_service
python app.py
```

默认地址：

```text
http://localhost:5000
```

### 3. 运行前端

另开终端：

```powershell
cd D:\vast-2020-mc2\frontend_client
npm run dev
```

默认地址：

```text
http://localhost:5173
```

可通过环境变量修改 API：

```powershell
$env:VITE_API_BASE = "http://localhost:5000/api"
npm run dev
```

### 4. 生产构建

```powershell
cd D:\vast-2020-mc2\frontend_client
npm run build
```

输出目录：`frontend_client/dist/`

## 测试

### 后端核心回归测试

```powershell
cd D:\vast-2020-mc2\backend_service
python -m unittest test_analysis.py
```

测试覆盖：

- 12 个 `yellowBag` 高阈值框全部被驳回；
- 最终候选由规则得到 `canadaPencil`；
- 最终组为 8 人且每人至少两张证据图；
- 原始矩阵和校正矩阵 API 均可用。

### 前端构建检查

```powershell
cd D:\vast-2020-mc2\frontend_client
npm run build
```

## 修改数据后的因果链

人工复核一次操作会触发：

```text
POST /api/update_label
  -> 更新 human_corrections.json
  -> 重建 ForensicAnalysisEngine
  -> 重算校正矩阵
  -> 重算候选人数、稳定性和分数
  -> 重选最终物品与 8 人组
  -> 刷新复核队列、热图和最终证据册
```

因此系统不是“改了标签但结论仍固定不变”的演示界面。只要校正分布变化到不再满足硬条件，当前结论就会随之变化。

## 已知边界

1. 组织规模 8 来自赛题先验，不是系统自动估计。
2. `canadaPencil` 已完成逐图核验；其他候选还需要进一步补齐图片级证据。
3. 文本匹配采用受控别名和关键词，不是完整 NLP 实体链接。
4. 评分权重是可解释的启发式权重，尚未做统计学习或敏感性优化。
5. 当前前端包包含 ECharts，生产主包较大，Vite 会提示超过 500 kB；不影响正确性，可后续按路由拆包。
6. 原始数据中没有可靠的人际社交边，因此系统不再输出社交隔离结论。

## 结论复述

本项目当前可审计的结论是：

```text
yellowBag：
原始模型阈值产生的 8 人假设，经 12 个检测框逐图复核后失效。

canadaPencil：
人工校正后恰好由 8 人持有；
每人至少有 2 张图片；
共 25 张图片；
3 人有直接文本支持；
综合评分 0.9375；
因此成为最终暗号物品。

最终 8 人：
Person4, Person7, Person14, Person15,
Person22, Person25, Person35, Person39
```

最重要的是，这份结论能够从 `i3_new_data.json`、`human_corrections.json` 和 `analysis_engine.py` 逐步重算，而不是由前端写死。
