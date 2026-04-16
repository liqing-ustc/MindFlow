---
title: ER OKR 讨论 — 战略方向与 Q2 规划
date: 2026-04-16
attendees:
  - ER Core
tags:
  - embodied-reasoning
  - OKR
related: "[[Projects/Xiaomi-Robotics-ER]]"
---

## Agenda

- ER 方向的战略定位与价值主张
- Q2 交付 vs 长期模型开发的平衡
- 社区影响力策略
- 能力维度拆解与 Level 定义
- 资源需求与获取路径

## 核心结论

### 三条并行路线达成共识

| 路线 | 目标 | 时间维度 | 产出形式 |
|------|------|---------|---------|
| **Demo** | 配合部门展示需求 | Short-term (Q2) | 真机演示，领导现场体验 |
| **Agent 框架** | 开源 Embodied Agent 框架 | Mid-term | 开源代码，社区影响力 |
| **ER 模型** | 自研多尺寸 Embodied VLM | Long-term (年度) | 开源模型 + Tech Report |

三条线**不是独立的**：Demo 用 Agent 框架实现，Agent 框架支撑多种 ER/VLA 模型，短期 Demo 的数据和经验沉淀到长期模型训练中。

### 影响力策略

团队一致认为：**当前阶段无产品落地，核心交付 = 社区影响力 + Demo 展示**。

影响力路径：
1. **开源泛化的小能力模型**（4B/8B）— 如泛化的状态监控模型、泛化的任务拆解模型，别人不需要微调就能用
2. **开源 Embodied Agent 框架** — 兼容不同 ER model 和 VLA model，降低社区上手门槛
3. **长期目标**: 全维度 Embodied VLM，某些能力维度超过闭源模型

> **Anti-pattern**: Overfit 到特定 demo 的模型没有开源价值，也发不出论文。用开源数据训的模型跟别人没差异化，tech report 里只能写一句话。

## Discussion Notes

### 1. Demo 的定位与约束

- Demo **不是视频剪辑**，而是**框定场景下的现场体验**（如领导来访，西班牙首相参观展厅），泛化性要求比纯视频高
- Demo 是整个部门协作项目：ER + VLA + 硬件系统 + 米家 API，不是 ER 单独交付
- **原则**: 完成即可，不要花太多脑力，更多是工程适配问题
- Demo 的本质目的：**拿 Demo 换资源** → 资源做 long-term research → 更 fancy 的 Demo → 正循环
- Demo 中用 Agent 框架 + 调用 Gemini API 作为 ER model 是可接受的短期方案

### 2. 社区影响力 — 核心诉求

**背景** (Taylor 补充): 最初团队按照 ERQA benchmark 路线做，review 了站内工作。但 Jason 的核心目标是**提升开源社区影响力**。被追问"这些指标能提升多少？会不会比正在做的更好？"之后，团队从刷 benchmark 思路转向 bottom-up 的能力构建。

**影响力的两种路径**:
1. 发一个特别强的 ER 模型，成为下游任务的标准 benchmark → 门槛高，需要时间
2. 做一个很小的切入点，但有 **insight** → 门槛低，短期可行

**开源策略**:
- 避免 overfit 模型（无法泛化 = 无影响力）
- 避免纯复现（用开源数据训 = 无差异化）
- **推荐**: 开源各尺寸（4B/8B/32B）的 ER 模型，在某些能力维度有突出表现
- 小尺寸模型的额外价值：别人能用有限资源复现和验证你的方法（ Jack 的观点：需要 2B 模型让资源有限的团队也能验证）

### 3. 资源获取 — 需要 Proposal

**Eric 的核心观点**: 要资源（GPU、数据采购）就必须有立项文档：
- 行业背景 → 技术路线图 → 一年期计划（季度清晰，远期粗糙）
- 对标谁？需要什么数据？多少数据？训多大模型？需要多少计算资源？一个 Q 内是否可行？
- 参考 Jason 之前做的 VLA 规划文档：NFT 数量、数据量、计算资源都非常具体

**ER 的现状差距**: 
- VLA 方向有 π0 等可以摸着石头过河，社区活跃
- ER 方向社区不够活跃，参考工作少（Gemini Robotics 可能是最好的对标）
- 团队自身沉淀不够，还没有花足够时间想清楚长期路径

**可能的合作方案** (Taylor 提出):
- ER 团队负责**数据构建 + 标注 + 评测**
- 把大规模训练交给 MiMo 团队（他们有足够计算资源）
- MiMo 训完给 API/checkpoint → ER 团队评测 → 反馈优化数据 → 迭代
- 这样可以绕过 ER 团队自身计算资源不足的问题

### 4. 能力维度拆解（from Qing）

已整合到 [[Projects/Xiaomi-Robotics-ER]] 的 Scope 和能力矩阵中。会上补充的关键细节：

**Task Decomposition**:
- 不同方式给指令都应正确拆解（语言泛化）
- VLM 对语言理解不是瓶颈，瓶颈在于**翻译成 VLA 可执行的指令**
- 给 VLA 的指令必须是**具体的、instance 唯一的**（不是"拿个喝的"而是"去冰箱拿脉动"）
- 甚至应该是多模态的：语言 + 参考图片

**Spatial Reasoning**:
- 当前 VLM 在 multi-view 空间推理上表现很差
- 字节 Seed-VL 也在做 3D 空间推理能力，方向是让通用 VLM 具备这种能力
- 数据构造是主要手段（收集 + 构造更多 spatial reasoning 数据）

**Success Detection**:
- 培然在做状态监控
- Gemini ER 1.6 的多视角 success detection 效果好，但开源界还没有特别好的方案

**Memory**:
- Short-term: 放所有帧到 context（简单场景可行）或采帧
- Long-term: 需要存储/访问/修改机制，类似 Claude Code 的 Markdown 文件式 memory
- Memory 本身可以作为独立研究方向
- 现有 LLM Agent 的 Markdown memory 方式可借鉴到 Embodied Agent

**Navigation**:
- 保底方案: SLAM（临时方案）
- 长期: 需要与模型结合更好的方案
- ER 的 navigation 精度要求不高，到大致位置即可，精细操作交给 VLA

**Failure Recovery**:
- VLA 层面: 动作级重试
- ER 层面: **规划级重规划**（去冰箱发现没有牛奶 → 重新 plan）
- 这是 VLA 无法解决的，必须由 ER 处理

**给 VLA 指令的粒度问题（重要洞察）**:
- 当前给 VLA 的是纯语言指令
- 理想状态应该是**多模态指令**: 参考图片 + 语言 prompt
- 例: 冰箱里两罐牛奶（一罐喝了一半），应该拿喝了一半的那个 → 需要 VLM 推理 + 给 VLA 精确指令（含参考图片）
- 类似场景: 两份鸡蛋先吃快过期的、高钙低钙牛奶分老人小孩
- VLA 训练数据需要包含 video prompt 的数据（无技术瓶颈）

### 5. 与 MiMo 和其他团队的关系

- MiMo 团队重点在 LLM Agent（tool call 能力），不关心具身场景
- 如果 ER scope 做大，可以承接 MiMo 更大规模的模型 → 加入 embodied 能力
- 这是双赢：MiMo 的模型获得具身能力，ER 获得计算资源

### 6. Q2 交付与节奏

- **Q2 明确交付**: Demo（非常具体，手头工作一边推进）
- **Q2 同步推进**: Agent 框架搭建 + 能力维度铺石头（Task decomposition、Success detection 等各做一个 baseline）
- **长期工作**: 每次周会拿出来讨论，持续兜售 idea
- **人员扩张**: 5月底6月份会有校招+社招，团队从~20人扩到~40人（社招校招 1:1）

> Eric: "这是个创业团队的研究团队，大家要敢于兜售自己的 idea，敢于尝试别人没尝试过的事情，否则就有点浪费这个团队的资源。"

### 7. Demo 展示场景

- 目标场景: A 栋展厅，两室一厅环境，展示智能家居全场景
- 需要现场体验级别的鲁棒性，不是视频剪辑
- 需要结合米家 API / 智能家居 API

## Key Insights

1. **Demo → 资源 → Research → 更好的 Demo** 是当前阶段的核心循环，不存在产品和营收
2. ER 必须作为**独立模块**迭代，不能只是 VLA 的附属（只做 VLA 适配的 ER = 只做 Demo = 没有长期价值）
3. 小模型开源 > 大模型闭源：社区验证门槛低 = 影响力大
4. **给 VLA 的指令应该是多模态的**（语言 + 参考图片），这是 ER-VLA 接口设计的重要方向
5. 计算资源是关键瓶颈，scope 大小直接决定能分到多少资源 — 需要写大 proposal 才能争取大资源
