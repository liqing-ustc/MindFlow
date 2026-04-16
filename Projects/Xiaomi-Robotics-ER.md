---
title: "Xiaomi-Robotics-0.5 Embodied Reasoning"
tags: [VLA, embodied-reasoning, scene-understanding, memory, navigation, mobile-manipulation]
status: planning
date_started: "2026-04-16"
---
## Goal

为 Xiaomi-Robotics-0.5 构建完整的 Embodied Reasoning (ER) 能力栈，使模型从 table-top manipulation 扩展到 ***scene-level* *long-horizon* tasks**。

### Tasks

| Level       | 描述                              | 示例任务                             | 对标工作                                              | Q2 目标 |
| ----------- | ------------------------------- | -------------------------------- | ------------------------------------------------- | ----- |
| **Level 0** | Table-top long-horizon（固定工位）    | 叠衣服 → 放鞋 → 收洗漱包 → 关箱子            | Gemini Robotics VLA, π0 (laundry folding)         | ✅ 基线  |
| **Level 1** | Single-room mobile manipulation | 从衣柜取衣服 → 到桌上叠 → 放进行李箱            | π0.5 (kitchen cleanup, 15min), MEM (recipe setup) | ✅ 主目标 |
| **Level 2** | Multi-room complex tasks        | 卧室取衣服 → 浴室收洗漱用品 → 客厅收充电器 → 回卧室打包 | *无人区*                                             | ❌ Q3+ |

### Capability Stack

| 层       | 模块                   | 子能力                               | 说明                       |
| ------- | -------------------- | --------------------------------- | ------------------------ |
| **任务层** | Task-Level Reasoning | Task decomposition                | 长序列任务分解为子任务序列            |
|         |                      | Success detection                 | 多视角判断当前步骤是否完成            |
|         |                      | Failure recovery                  | 规划级重规划（非动作级重试）           |
| **感知层** | Scene Understanding  | Object recognition & localization | 开放词汇物体检测 + 3D 定位         |
|         |                      | Event understanding               | 场景状态变化感知（门开了、物体被移动了）     |
| **记忆层** | Short-term Memory    | Video clip (~60s)                 | 密集视觉记忆，处理遮挡和动态           |
|         | Long-term Memory     | Spatial (persistent)              | 物体位置持久化，scene graph 增量更新 |
|         |                      | Episodic (~15min+)                | 语义事件摘要，跟踪已完成步骤           |
| **移动层** | Navigation           | Goal-conditioned nav              | 导航到目标物体/位置               |
|         |                      | Obstacle avoidance                | 动态避障                     |
| **执行层** | Manipulation (VLA)   | Dexterous manipulation            | 叠衣服、拉拉链                  |
|         |                      | Reliability, Speed, Improvisation | 可靠，高频，即兴解决意外状况           |

### Capability × Task 矩阵

| 能力                            | Level 0      | Level 1                           | Level 2                         |
| ----------------------------- | ------------ | --------------------------------- | ------------------------------- |
| Task Decomposition            | ✅ 5+ 步线性分解   | ✅ + 条件分支（柜子锁了→换方案）                | ✅ + 跨房间依赖调度                     |
| Spatial Reasoning             | ✅ 工作台内物体空间关系 | ✅ + 房间尺度物体定位                      | ✅ + 建筑尺度拓扑理解                    |
| Success Detection             | ✅ 单视角/多视角判断  | ✅ 同 Level 0                       | ✅ + 远程验证（离开房间后确认）               |
| Failure Recovery              | ⚡ 简单重试       | ✅ 重规划（换路线/换目标物体）                  | ✅ + 跨房间回退策略                     |
| Scene Understanding           | ❌            | ✅ 实时 3D scene graph（单房间）          | ✅ + 多房间 scene graph 拼接          |
| Short-term Memory: video clip | ⚡ 有帮助但非必需    | ✅ ~54s 视觉记忆                       | ✅ 同 Level 1                     |
| Long-term Memory: Spatial     | ❌            | ✅ 单房间物体位置持久化 (scene graph)        | ✅ + 多房间地图 + 跨 session 记忆        |
| Long-term Memory: Episodic    | ⚡ 有帮助（>5 步时） | ✅ 语义事件摘要（~15min）                  | ✅ + 跨房间事件追踪（~1hr）               |
| Navigation                    | ❌            | ✅ Room-scale goal-conditioned nav | ✅ + Building-scale nav + 门/电梯交互 |

> ✅ = 必需　⚡ = 有帮助但非必需　❌ = 不需要


### 三条并行线

| 路线           | 目标                   | 时间维度       | 产出形式               | 核心价值  |
| ------------ | -------------------- | ---------- | ------------------ | ----- |
| **Demo**     | 配合部门展示需求             | Short-term | 真机演示，现场体验          | 争取资源  |
| **Agent 框架** | 开源 Embodied Agent 框架 | Mid-term   | 开源代码               | 社区影响力 |
| **ER 模型**    | 自研多尺寸 Embodied VLM   | Long-term  | 开源模型 + Tech Report | 技术壁垒  |

三条线相互促进：Demo 用 Agent 框架实现，Agent 框架支撑多种 ER/VLA 模型，短期 Demo 数据沉淀到长期 ER 模型训练。

### 开源影响力策略

- **开源 Agent 框架** — 兼容不同 ER/VLA model，降低上手门槛（参考 OpenVLA/LeRobot 降低门槛的思路）
- **开源 ER 模型**: 全维度 Embodied VLM，某些能力超过闭源模型


## 技术方案

### 1. Task-Level Reasoning
- **方法**: Hierarchical ER-VLA (参考 Gemini Robotics dual-system + π0.5 hierarchical inference)
- **训练**: SFT baseline → GRPO (参考 Embodied-R1, Robot-R1; RL >> SFT 是已验证结论)
- **输出**: 子任务序列 + 每步的 sub-goal description
- **与 EWM 协同**: EWM 生成 sub-goal image 作为 planning intermediate representation
- **ER→VLA 指令设计**: 给 VLA 的指令必须是 **instance 唯一 + 多模态**的（语言 + 参考图片），不是模糊自然语言。VLM 语言理解不是瓶颈，瓶颈在翻译成 VLA 可执行指令。例: 不说"拿个喝的"，而是"去冰箱拿那个喝了一半的牛奶" + 目标物体参考图

### 2. Scene Understanding
- **方案**: ConceptGraphs 式 3D scene graph + MTU3D 式 online incremental update
- **节点信息**: object class, CLIP embedding, 3D bbox, state (open/closed/empty), graspability
- **关键**: 避免 offline batch processing，实现实时增量更新

### 3. Multi-Scale Memory
参考 MEM (Pi, 2026) 的三尺度架构:

| 尺度 | 模态 | 窗口 | 参考 | 能力 |
|------|------|------|------|------|
| Short-term | Video encoder | ~54s | MEM video encoder (零新参数, space-time separable attention) | 遮挡处理、动态理解、in-context 策略调整 |
| Long-term | Language summary | ~15min | MEM language memory (LLM 压缩摘要) | 跟踪已完成步骤、避免重复 |
| Spatial | 3D scene graph | Persistent | EchoVLA scene memory + MTU3D online query | 物体位置记忆、导航目标定位 |

**差异化机会**: MEM 缺乏 explicit 3D spatial memory，EchoVLA 缺乏 language long-term memory。统一三尺度是 open question (见 [[DomainMaps/SpatialRep.md]])。

### 4. Navigation
- **Q2 方案**: Modular pipeline (goal-conditioned nav policy + obstacle avoidance)，快速落地
- **Q3 目标**: 统一到 end-to-end Nav-Manip VLA (参考 DM0, Hi-Robot)
- **Nav-Manip 衔接**: 参考 [[Ideas/NavPreGrasp-JointOptimization.md]] jointly 优化 approach pose

### 5. Success Detection
- **方案**: 多视角推理判断步骤完成 (参考 Gemini ER 1.6)
- **作用**: 串联长序列任务的关键组件，驱动 memory 更新和 sub-goal 切换
- **现状**: 开源界还没有特别好的多视角 success detection 方案 → 这本身是一个可开源的泛化小模型切入点

### 6. Failure Recovery (规划级)
- VLA 层面只能动作级重试，ER 解决的是**规划级重规划**
- 场景: 去冰箱发现没有牛奶 → 更新 memory → 重新 plan（换目标物体/换路线）
- 这是 ER 区别于 VLA 的核心价值之一，VLA 无法处理此类问题

### 7. Embodied Agent 框架 (新增)
- **定位**: 开源框架，兼容不同 ER model（自研/Gemini API）和 VLA model
- **设计目标**: 降低社区上手门槛（参考 OpenVLA/LeRobot 的成功经验）
- **特色**: 集成米家/智能家居 API
- **短期**: Demo 中调用 Gemini API 作为 ER model 是可接受方案
- **长期**: 替换为自研 ER model

## Key Results (目标)

| 指标                              | w/o ER | w/ ER 目标        |
| ------------------------------- | ------ | --------------- |
| 行李箱打包成功率 (Level 0, table-top)   | X%     | X+15%+          |
| 行李箱打包成功率 (Level 1, single-room) | N/A    | ≥40%            |
| 子任务分解准确率                        | N/A    | ≥80%            |
| 长序列平均完成步数                       | Y/8    | ≥6/8            |
| 失败后恢复率                          | 0%     | ≥50%            |
| Success detection 准确率           | N/A    | ≥90%            |
| ER scaling (8B→32B→更大?)         | —      | 拿到 monotonic 曲线 |

## Papers

### Embodied Reasoning
- [[2503-GeminiRobotics]] — Gemini Robotics ER: 定义了 ER 能力维度, ERQA benchmark
- [[2604-GeminiRoboticsER16]] — ER 1.6: agentic vision, multi-view success detection, instrument reading
- [[2508-EmbodiedR1]] — Pointing as embodiment-agnostic intermediate repr., GRPO >> SFT
- [[2510-VLASER]] — **OOD reasoning data 不 transfer, in-domain 才是决定性的**
- [[2512-Lumo1]] — 统一 reasoning + action, 407B tokens, GRPO multi-reward
- [[2602-DM0]] — Embodied-Native VLA, spatial scaffolding, gradient decoupling
- [[2601-Thinker]] — Robotics-specific VLM, 4.8M 数据, 4 core abilities

### Memory
- [[2603-MEM]] — **核心参考**: multi-scale memory (video short-term + language long-term), 15min 任务
- [[2511-EchoVLA]] — Scene memory (3D voxel) + episodic memory (FIFO), mobile manipulation

### Scene Understanding & Spatial Representation
- [[2309-ConceptGraphs]] — 3D scene graph with language grounding, Nav + Manip 最优表示
- [[2410-DovSG]] — Dynamic open-vocabulary 3D scene graphs
- [[2507-MTU3D]] — Online query spatial memory, unified grounding-exploration, 4 benchmarks SOTA
- [[2604-OpenSpatial]] — Open-vocabulary spatial understanding

### Navigation & Mobile Manipulation
- [[2504-Pi05]] — Heterogeneous co-training, hierarchical inference, 15min household tasks
- [[2412-NaVILA]] — Navigation VLA, real robot deployment
- [[2502-HiRobot]] — Hierarchical VLM-VLA, open-ended instruction
- [[2503-MoManipVLA]] — Adapting fixed-base VLA to mobile manipulation
- [[2601-CycleVLA]] — Self-correction for long-horizon tasks

### Surveys
- [[Topics/Embodied-Reasoning-Survey]] — 四条技术路线, RL >> SFT 结论
- [[Topics/VLN-VLA-Unification]] — VLN-VLA 统一分析, shared spatial representation 是关键
- [[Topics/LanguageConditioned-MobileManipulation-Survey]] — 四条 mobile manipulation 路线
- [[Topics/VLA-Survey]] — VLA 全景, dual-system + flow matching 是共识

## Ideas
- [[Ideas/NavPreGrasp-JointOptimization]] — Navigation-aware manipulation pre-positioning
- [[Ideas/SpatialToken-VLA]] — 3D scene graph 编码为 VLM native tokens
- [[Ideas/Unified-GEM-Framework]] — Grounding-Exploration-Manipulation 统一框架

## Timeline

```
4月底  ─── P0: ER 能力定义 + 技术架构文档
           - 确定 scene graph 方案、memory 架构、nav 方案
           - 明确 ER 与 EWM 的接口定义

5月中  ─── P0: Scene Understanding + Memory 原型
           - 3D scene graph 实时构建 pipeline
           - Video encoder 集成到 VLA
           - 语言记忆 annotation 开始构建
           P0: Xiaomi-ERQA Benchmark
           - 覆盖 scene understanding + memory + reasoning 维度
           - 200-400 题, 针对自有任务分布

5月底  ─── P1: Navigation 模块
           - Goal-conditioned nav policy
           - Nav-Manip 衔接验证
           P1: In-domain Reasoning Data
           - 从 20k+ 小时数据构建 reasoning annotations
           - 参考 VLASER-6M 四类数据格式

6月中  ─── P1: ER Training Pipeline
           - SFT → GRPO training
           - 2B/4B/8B scaling curve

6月底  ─── P0: 行李箱 Demo (Level 1) + Ablation
           - 端到端: 导航 + 操作 + 记忆
           - w/ vs w/o 每个 ER 组件的 ablation
           P1: Technical Report ER 章节
```

## 资源策略

### 计算资源
- 当前 ER 团队计算资源有限，scope 决定能分到多少卡（overfit demo 级 = 十几二十张卡，全尺寸训练 = 更多）
- **与 MiMo 团队合作方案**: ER 出数据 + 标注 + 评测，MiMo 出算力训练 → MiMo 训完给 checkpoint → ER 评测反馈 → 迭代。双赢: MiMo 模型获得 embodied 能力，ER 获得计算资源
- 需要写**年度 Proposal**（对标 Jason 的 VLA 规划文档级别）: 行业背景 → 技术路线 → 数据需求 × 计算需求 × 模型尺寸 → 年度计划（Q 级清晰，远期粗糙）

### 数据资源
- Jason 规划的 100 万小时 ego-centric 视频数据对 ER 训练也友好（大部分是 ego-centric）
- 需要明确: 需要什么数据？多少数据？数据来源（采集/采购/合成）？
- 已有 ~5-10 篇 7B/32B 规模的参考工作（智源等），可参考其训练数据来源和 benchmark

### 团队资源
- 5-6 月团队 ~20 → ~40 人（社招校招 1:1），需要清晰方向承接新人
- ER 方向如果有清晰 proposal，有利于争取更多 headcount

## Risks

| 风险 | 影响 | 缓解 |
|------|------|------|
| Scope 过大 | Q2 交付不了 | Nav 用 modular pipeline; spatial memory 先用简化 scene graph |
| Scene graph 实时性不足 | Demo 卡顿 | 参考 MTU3D online query merging, 避免 offline ConceptGraphs |
| Memory 训练数据不足 | 记忆能力不涌现 | MEM 发现: 预训练阶段在多样化视频数据上训练记忆至关重要 |
| Nav-Manip 衔接 | 导航到位后操作失败 | [[Ideas/NavPreGrasp-JointOptimization]] jointly 优化 approach pose |
| ER 贡献不显著 | 无法证明 ER 价值 | 必须做 w/ vs w/o ablation, 如果 delta < 10% 需要重新审视 |
| 计算资源不足 | 无法训大模型 | MiMo 合作方案; 先做小模型（4B/8B）验证方法再 scale |
| 年度 Proposal 缺失 | 拿不到资源 | 尽快完成，参考 Jason 的 VLA 文档级别详细度 |

## Progress Log
- 2026-04-16: 项目启动，完成 ER 能力栈定义和技术方案设计
- 2026-04-16: [[Meetings/2026-04-16-ER-OKR-Discussion|ER OKR 讨论会]]，达成三线并行共识（Demo + Agent框架 + ER模型），明确社区影响力为核心交付，需写年度 proposal 争取资源

## TODOs

### P0: 战略 & 资源 (4月底前)
- [ ] **写 ER 年度 Proposal** — 对标 Jason VLA 文档级别：行业背景、对标工作、数据需求、计算资源需求、模型尺寸规划、年度 timeline（Q 级清晰）
- [ ] 评估与 MiMo 团队合作训练的可行性（数据 ↔ 算力交换）
- [ ] 完成 ER 技术架构文档
- [ ] 确定 scene graph 实现方案: ConceptGraphs 式 vs MTU3D 式
- [ ] 定义 ER 与 EWM 的接口规范

### P0: 能力 Baseline 铺设 (5月中)
- [ ] Task decomposition baseline — 从 overfit 找 know-how，再泛化
- [ ] Success detection baseline — 培然推进，多视角判断
- [ ] 构建 Xiaomi-ERQA benchmark (覆盖 scene understanding + memory + reasoning)
- [ ] 搭建 3D scene graph 实时构建 pipeline
- [ ] 集成 MEM-style video encoder 到 VLA

### P1: 数据 & 训练 (5月底-6月中)
- [ ] 构建 in-domain reasoning data annotations（从 20k+ 小时数据）
- [ ] 搭建 goal-conditioned navigation module
- [ ] SFT → GRPO training pipeline
- [ ] 2B/4B/8B ER scaling curve

### P0: Demo & 交付 (6月底)
- [ ] Level 1 行李箱 Demo 端到端验证（导航 + 操作 + 记忆）
- [ ] ER ablation study (w/ vs w/o 每个组件)
- [ ] Technical report ER 章节初稿

### 开源产出 (持续)
- [ ] Embodied Agent 框架设计与开源准备
- [ ] 泛化 Success Detection 小模型（4B/8B）开源候选
- [ ] 泛化 Task Decomposition 小模型（4B/8B）开源候选

## Notes
- **核心差异化**: 三尺度统一记忆 (video + language + spatial) 是 open question，MEM 和 EchoVLA 各做了一半
- **ER 与 EWM 关系**: EWM 提供 imagination (sub-goal images), ER 提供 reasoning (task decomposition + scene understanding + memory)，两者互补
- **训练方法 bet**: GRPO (RL) 是 primary bet，已有充分证据 (Embodied-R1: 65.5% vs SFT 41.25%)
- **数据策略**: VLASER 的核心发现——OOD reasoning data 几乎不 transfer，必须构建 in-domain reasoning data
- **ER-VLA 接口设计**: 给 VLA 的指令应该是**多模态的**（语言 + 参考图片），不能是模糊语言（"拿个喝的"），必须是 instance 唯一的具体指令（"去冰箱拿那个喝了一半的牛奶" + 参考图片）
- **Failure Recovery 是 ER 独有价值**: VLA 只能动作级重试，ER 做规划级重规划（去了发现没有→更新 memory→重新 plan）
- **战略定位**: ER 必须作为独立模块迭代，不能只是 VLA 的附属。Demo → 资源 → Research → 更好的 Demo 是当前核心循环
- **开源策略**: 小模型（4B/8B）开源 > 大模型闭源。社区验证门槛低 = 影响力大。Overfit 模型无开源价值
- **对标与竞争格局**: ER 社区不如 VLA 活跃，Gemini Robotics 是目前最好的对标；字节 Seed-VL 在做 3D 空间推理；已有 5-10 篇 7B/32B 规模参考工作（智源等）
- **参考**: 详见 [[Meetings/2026-04-16-ER-OKR-Discussion]]
