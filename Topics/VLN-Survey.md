---
title: Vision-Language Navigation Survey
tags:
  - VLN
  - navigation
  - VLM
  - spatial-memory
  - task-planning
date_updated: 2026-03-27
year_range: 2022-2026
papers_analyzed: 8
---
## Overview

Vision-and-Language Navigation (VLN) 是 embodied AI 的核心任务之一，要求 agent 根据自然语言指令在视觉环境中导航到目标位置。自 2018 年 R2R benchmark 提出以来，VLN 经历了从 discrete navigation graph 到 continuous environment、从 task-specific 架构到 foundation model backbone 的深刻演变。

近三年（2022-2026）是 VLN 研究的一个范式转折期。核心趋势可以概括为三个方向的汇聚：

1. **From discrete to continuous**：从 nav-graph 上的 waypoint selection 走向连续环境中的真实导航。DUET → ETPNav → NaVid/NaVILA/Efficient-VLN 的演进清晰展示了这一轨迹。到 2025 年，VLN-CE（continuous environment）已成为研究主战场。

2. **From task-specific to foundation model**：从 task-specific transformer（DUET、ETPNav）到 LLM/VLM backbone（NavGPT、NaVid、NaVILA、Efficient-VLN）。Foundation model 的引入不仅提升了性能，更带来了 zero-shot generalization 和 sim-to-real transfer 能力。

3. **From navigation to embodied agent**：VLN 正与 VLA（Vision-Language-Action）架构趋同，NaVILA 直接将 VLN 重构为 navigation-focused VLA。同时，LH-VLN 将任务从单阶段导航扩展到多阶段长程任务，MTU3D 将 navigation 与 3D scene understanding 统一，都在推动 VLN 走向更通用的 embodied intelligence。

研究活跃度方面，VLN 领域近年发表密度持续增长，RSS、CVPR、ICLR、NeurIPS 等顶会均有高影响力论文。2024 年已有综合性 survey [[Vision-and-Language Navigation Today and Tomorrow: A Survey in the Era of Foundation Models](https://arxiv.org/abs/2407.07035)]（TMLR 2024）对 foundation model 时代的 VLN 做了全面梳理。

## 技术路线

### 路线 1：Topological Map + Task-Specific Planning

代表论文：[[2202-DUET]]、[[2304-ETPNav]]

这是 VLN 的"经典范式"。核心思想是在导航过程中在线构建 topological map 作为结构化空间记忆，再用 cross-modal transformer 进行路径规划。

- **DUET**（CVPR 2022）提出 dual-scale graph transformer，在 topological map 上进行 global coarse-grained reasoning + local fine-grained grounding，在 R2R、REVERIE、SOON 上取得 SOTA。但仅限于 discrete nav-graph。
- **ETPNav**（TPAMI 2024）将 topological planning 扩展到 continuous environment，通过 waypoint prediction + hierarchical architecture（high-level planner + low-level obstacle-avoiding controller），在 R2R-CE 和 RxR-CE 上大幅超越 prior SOTA。

**优势**：结构化空间表示对长程规划至关重要；hierarchical 设计解耦了语义理解和运动控制。
**局限**：task-specific 架构缺乏泛化能力；topological map 是 hand-designed 而非 learned representation；low-level controller 基于 heuristic。

### 路线 2：VLM/LLM-Based End-to-End Navigation

代表论文：[[2305-NavGPT]]、[[2402-NaVid]]、[[2512-EfficientVLN]]

这是 foundation model 时代的新范式。核心思想是将预训练 VLM/LLM 作为 navigation backbone，通过 fine-tuning 或 prompting 实现视觉导航。

- **NavGPT**（AAAI 2024）首次将 GPT-4 用于 VLN 的 zero-shot reasoning，证明了 LLM 的 instruction decomposition 和 commonsense 能力，但纯文本输入导致视觉信息严重损失（R2R SR ~30%），为后续 visual alignment 指明了方向。
- **NaVid**（RSS 2024）提出 video-based VLM 方案，将导航历史编码为 spatio-temporal visual tokens（仅 4 tokens/frame），基于 LLaMA-VID 实现 map-free、sensor-free 导航。在 R2R-CE 上 SPL 35.9%（SOTA），RxR 零样本 SPL 提升 236%，真实环境 66% SR。
- **Efficient-VLN**（NAACL 2025）针对 MLLM-based VLN 训练开销问题，提出 progressive memory（遗忘曲线式压缩）、recursive memory（KV cache 传递）、dynamic DAgger policy，在仅 282 GPU hours 下达到 R2R-CE 64.2% SR 和 RxR-CE 67.0% SR 的新 SOTA，训练效率提升 78%。

**优势**：强大的 zero-shot generalization 和 cross-dataset transfer；end-to-end 训练简化了系统设计；natural language interface 便于人机交互。
**局限**：推理延迟较高（1-2s/action）；long-horizon 能力仍不足；训练开销虽已降低但仍需数百 GPU hours。

### 路线 3：Navigation as VLA（VLN-VLA 统一）

代表论文：[[2412-NaVILA]]

将 VLN 重构为 navigation-focused VLA，是当前最前沿的方向。

- **NaVILA**（RSS 2025）将 VLM（VILA）微调为 navigation VLA，通过生成 mid-level 语言化动作指令（如 "move forward 75cm"）而非 low-level joint action，再由 RL locomotion policy 执行。R2R-CE 54% SR，真实 legged robot 88% SR。利用 YouTube 视频生成 20k 训练轨迹，证明了 web-scale 数据在 navigation 中的潜力。

**优势**：语言化 mid-level action 优雅地解耦了语义理解与运动控制；robot-agnostic；sim-to-real transfer 最佳。
**局限**：mid-level action 粒度需要 task-specific 调优；语言化 action 能否扩展到 manipulation 尚未验证。

### 路线 4：Unified Scene Understanding + Navigation

代表论文：[[2507-MTU3D]]

将 3D 场景理解与 active exploration 统一到一个框架。

- **MTU3D**（ICCV 2025）提出 online query representation + dynamic spatial memory bank，将 object grounding 和 frontier exploration 统一到同一决策空间。无需显式 3D 重建，在 HM3D-OVON、GOAT-Bench、SG3D-Nav、A-EQA 四个 benchmark 上取得 SOTA，并 zero-shot 部署到真实机器人。

**优势**：首次实现 grounding-exploration joint optimization；online query 避免了离线 3D 重建；spatial memory 支持 lifelong navigation。
**局限**：266M 参数为 task-specific 架构，未与 VLM-based 方法结合；low-level 仍依赖 shortest path planner。

### 路线 5：Long-Horizon Extension

代表论文：[[2412-LHVLN]]

将 VLN 从单阶段短程导航扩展到多阶段长程任务。

- **LH-VLN**（CVPR 2025）提出 long-horizon VLN benchmark（LHPR-VLN，3,260 个多阶段任务，平均 150 步），以及 MGDM 模型（entropy-based memory forgetting + long-term memory retrieval）。所有现有方法 SR = 0%，揭示了 long-horizon 导航的根本性挑战。

**优势**：填补了 long-horizon VLN 的 benchmark 空白；memory 机制设计对 long-horizon 任务有启发。
**局限**：当前方法完全无法解决；仅在 simulation 中验证。

## 发展时间线

| 时间 | 里程碑 | 意义 |
|:-----|:-------|:-----|
| 2022-02 | [[2202-DUET]] 提出 dual-scale graph transformer | 确立 topological map 作为 VLN 核心空间表示 |
| 2023-04 | [[2304-ETPNav]] 将 topological planning 扩展到 continuous env | VLN-CE 性能大幅突破（+10-20% SR） |
| 2023-05 | [[2305-NavGPT]] 首次将 LLM 用于 VLN | 开创 LLM-for-navigation 范式，暴露纯文本输入瓶颈 |
| 2024-02 | [[2402-NaVid]] 提出 video-based VLM for VLN | Map-free sensor-free 导航，video tokens 替代 explicit map |
| 2024-12 | [[2412-NaVILA]] 将 VLN 重构为 navigation VLA | VLN-VLA 架构统一的直接证据，legged robot 88% SR |
| 2024-12 | [[2412-LHVLN]] 提出 long-horizon VLN benchmark | 揭示多阶段长程导航的根本性挑战（所有方法 SR=0%） |
| 2025-07 | [[2507-MTU3D]] 统一 grounding 与 exploration | 无需 3D 重建的 online spatial reasoning |
| 2025-12 | [[2512-EfficientVLN]] 达到 VLN-CE 新 SOTA | R2R-CE 64.2% SR，训练效率提升 78% |

## Paper Comparison

| Paper | Venue | 技术路线 | 核心方法 | 关键结果 | 局限性 |
|:------|:-----|:---------|:---------|:---------|:-------|
| [[2202-DUET]] | CVPR 2022 | Topological + Planning | Dual-scale graph transformer | R2R/REVERIE/SOON SOTA | 仅 discrete nav-graph |
| [[2304-ETPNav]] | TPAMI 2024 | Topological + Planning | Online topological map + hierarchical planning | R2R-CE/RxR-CE +10-20% | Task-specific，heuristic controller |
| [[2305-NavGPT]] | AAAI 2024 | LLM-Based | GPT-4 zero-shot reasoning | R2R SR ~30%，显式推理链 | 无视觉 grounding，性能差距大 |
| [[2402-NaVid]] | RSS 2024 | VLM End-to-End | Video-based VLM (LLaMA-VID)，4 tokens/frame | R2R-CE SPL 35.9%，real 66% SR | 推理延迟 1.2-1.5s/action |
| [[2412-NaVILA]] | RSS 2025 | Navigation as VLA | VLM → mid-level language action → RL policy | R2R-CE 54% SR，real legged 88% SR | Mid-level 粒度需调优 |
| [[2412-LHVLN]] | CVPR 2025 | Long-Horizon | NavGen 数据平台 + MGDM memory 模块 | 所有方法 SR=0%，NE 降至 1.23 | 当前方法无法解决 |
| [[2507-MTU3D]] | ICCV 2025 | Unified Understanding | Online query repr + grounding-exploration 统一 | 4 benchmarks SOTA，real 零样本 | 无 VLM backbone，无 manipulation |
| [[2512-EfficientVLN]] | NAACL 2025 | VLM End-to-End | Progressive memory + dynamic DAgger | R2R-CE 64.2% SR，282 GPU hrs | 仅 simulation 验证 |

## Key Takeaways

1. **VLN-CE 已成为主战场**：从 DUET 的 discrete nav-graph 到 Efficient-VLN 的 64.2% R2R-CE SR，continuous environment 下的导航性能在三年间实现了质的飞跃。R2R-CE 从"困难挑战"变为"基本可解"。

2. **VLM backbone 正在取代 task-specific 架构**：NavGPT → NaVid → NaVILA → Efficient-VLN 的演进表明，预训练 VLM 作为 navigation backbone 是不可逆的趋势。VLM 带来了 zero-shot generalization、cross-dataset transfer、sim-to-real 能力。

3. **Hierarchical architecture 是跨范式的共识**：无论是 ETPNav 的 topological planner + heuristic controller，NaVILA 的 VLM planner + RL locomotion policy，还是 LH-VLN 的 short-term + long-term memory，都采用了 hierarchical 设计。High-level semantic planning + low-level motor execution 的分层是 embodied navigation 的通用架构。

4. **VLN-VLA 架构趋同是最值得关注的趋势**：NaVILA 直接证明了 VLN 可以重构为 VLA。语言化 mid-level action 桥接了高层指令理解和低层运动控制，这一思路可能成为统一 navigation 和 manipulation 的关键。（**建议加入 DomainMaps**）

5. **Long-horizon 是 VLN 的下一个根本性挑战**：LH-VLN 的所有方法 SR=0% 表明，多阶段长程导航远未被解决。Memory management（如何在有限计算预算内保留关键的长程记忆）是核心技术瓶颈。

## Open Problems

### 1. Long-Horizon Navigation
LH-VLN benchmark 上所有方法 SR=0%，暴露了当前 VLN 模型在多阶段、150+ 步任务上的根本性不足。核心问题是 memory management——如何在有限 context window 下保留跨子任务的关键空间和语义信息？Efficient-VLN 的 progressive memory 和 LH-VLN 的 entropy-based forgetting 是初步探索，但远不够。

### 2. Sim-to-Real Gap
尽管 NaVILA 在 legged robot 上实现了 88% SR，NaVid 在真实环境达到 66% SR，但大多数 VLN 工作（包括 Efficient-VLN、LH-VLN）仍仅在 Habitat simulator 中验证。真实世界的动态障碍物、光照变化、传感器噪声仍是开放挑战。

### 3. VLN-VLA 统一
NaVILA 证明了 navigation 可以重构为 VLA，但语言化 mid-level action 能否扩展到 manipulation 仍未验证。Navigation 过程中构建的空间表示（topological map、spatial memory）能否直接服务于到达目的地后的 manipulation？这是 embodied AI 最关键的 open question 之一。

### 4. Spatial Representation 的最优形式
VLN 领域存在多种空间表示方案：topological map（DUET、ETPNav）、video tokens（NaVid）、online query（MTU3D）、language memory（NaVILA）。哪种表示最适合同时服务 navigation 和 manipulation？3D scene graph 可能是有潜力的统一方案，但尚无端到端验证。

### 5. 训练效率与 Scaling
Efficient-VLN 将训练开销降至 282 GPU hours，但 VLN 模型的 scaling law（更大模型 + 更多数据是否持续提升性能？）尚不清楚。YouTube 等 web-scale 数据的利用（NaVILA）值得深入探索。

## 调研日志

- **调研日期**: 2026-03-27
- **论文统计**: vault 已有 5 篇 + 新 digest 3 篇 + 跳过 0 篇
- **未能获取**: 无
