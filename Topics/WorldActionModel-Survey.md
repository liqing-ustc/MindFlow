---
title: "World Action Model 文献调研"
tags: [world-model, VLA, diffusion-policy, imitation-learning, RL, cross-embodiment]
date_updated: 2026-03-30
year_range: "2024-2026"
papers_analyzed: 8
---

## Overview

World Action Model (WAM) 是 embodied AI 领域的新兴范式，核心思想是将 **world modeling**（理解和预测物理世界动态）与 **action prediction**（生成机器人控制信号）统一到同一框架中。这一范式的兴起源于一个关键洞察：**video generation model 天然具备对物理世界时空动态的理解，这种理解可以直接转化为 motor control 能力**——"World models are implicit policies"。

该领域在 2024-2026 年经历了爆发式增长。从 IRASim (2024) 的 action-conditioned video prediction，到 UWM/DreamGen (2025) 的 unified generative framework，再到 DreamZero (2026) 正式定义 WAM 概念并实现 zero-shot policy generalization，技术路线在短短两年内从"world model 辅助 policy learning"演进为"world model 即 policy"。

研究活跃度方面，NVIDIA、Google DeepMind、Tsinghua University、ETH Zurich、ByteDance 等机构深度参与。2025 年至少有两篇专题 survey（arXiv:2510.16732, arXiv:2511.02097）系统梳理了该领域，多个 "awesome list" 在 GitHub 上活跃维护。可以说，world action model 正在成为继 VLA 之后 embodied AI 的下一个核心范式。

**与 VLA 的关系**：WAM 不是 VLA 的替代，而是 VLA 的演进。VLA 将 VLM 的语义理解迁移到 action generation，但缺乏对物理动态的深层理解；WAM 在此基础上引入 video generation 作为物理世界的 "mental simulation"，使模型不仅能"看懂"场景，更能"想象"动作的后果。DreamZero 的实验表明，WAM 在 unseen tasks 上比最优 VLA 提升超过 2 倍，这种泛化优势正是 world modeling 带来的核心价值。

## 技术路线

### 路线 1：联合生成式世界-动作模型 (Joint Generative World-Action Models)

**核心思路**：在同一个 generative model 中联合建模 video prediction 和 action prediction，使 world understanding 与 action generation 深度耦合。

**代表论文**：
- [[2602-DreamZero|DreamZero]]：14B autoregressive diffusion transformer，joint video-action denoising，定义了 WAM 概念。在 seen tasks 上达到 62.2%（baseline 27.4%），unseen tasks 39.5%（baseline <1%）。支持从 human video 和其他 robot 无 action label 迁移。
- [[2504-UWM|UWM]]：通过 decoupled diffusion timesteps 在统一 transformer 中耦合 video diffusion 和 action diffusion。单一模型自然支持 policy / forward dynamics / inverse dynamics / video prediction 四种推理模式。RSS 2025，real robot 超 Diffusion Policy 达 20%。
- [[2512-Motus|Motus]]：Mixture-of-Transformers 架构，三个 specialized expert（generative / understanding / action）通过 Tri-model Joint Attention 连接。用 optical flow 压缩为 14 维 latent action，桥接 visual dynamics 和 control。RoboTwin 87.02%（超 X-VLA 15%，超 π0.5 45%）。

**优势**：泛化能力强——joint training 使 video 中的 physical dynamics knowledge 直接传递给 action prediction；自然支持 action-free video data 的利用。

**劣势**：计算开销极大（DreamZero 需 2×GB200 实现 7Hz），inference speed 与 VLA 仍有差距。

### 路线 2：世界模型驱动的策略学习 (World Model-Driven Policy Learning)

**核心思路**：world model 不直接输出 action，而是作为 "data generator" 或 "RL environment" 间接提升 policy 的泛化能力。

**代表论文**：
- [[2505-DreamGen|DreamGen]]：4 阶段 pipeline（fine-tune video model → generate synthetic videos → IDM extract actions → co-train policy）。从 single-task teleoperation 数据泛化到 22 种新行为，cross-embodiment 验证于 GR1/Franka/SO-100。CoRL 2025。
- [[2602-WorldVLALoop|World-VLA-Loop]]：video world model 作为 RL post-training 环境，与 VLA policy 闭环迭代优化。State-aware world model 联合预测 video 和 reward，避免外部 VLM reward 的不对齐问题。LIBERO +12.7%，真实机器人 +23.4%。

**优势**：与现有 VLA pipeline 兼容性好——world model 是辅助模块而非替代方案；DreamGen 展示了 log-linear scaling 趋势。

**劣势**：pipeline 中存在 error propagation（如 IDM 的 action recovery 精度）；World-VLA-Loop 受限于 short-horizon（~20s）。

### 路线 3：动作条件视频预测 (Action-Conditioned Video Prediction)

**核心思路**：给定 action trajectory 作为条件，生成未来视频帧。可用作 policy evaluation、model-based planning、或作为通用 world simulation 基础设施。

**代表论文**：
- [[2406-IRASim|IRASim]]：diffusion transformer with frame-level action conditioning。解决了 action-trajectory 与 video-frame 的精确对齐问题。Policy evaluation 与 ground-truth simulator 相关度达 0.99；model-based planning 将 Push-T IoU 从 0.637 提升到 0.961。ICCV 2025。
- [[2501-Cosmos|Cosmos]]：NVIDIA 的 World Foundation Model 平台。End-to-end pipeline（data processing → video tokenizer → pre-trained WFM → post-training）。2000 万小时视频训练，10,000 张 H100，开源开放。

**优势**：IRASim 证明了 frame-level conditioning 的必要性和有效性；Cosmos 提供了基础设施级支撑，下游多个工作（World-VLA-Loop 基于 Cosmos-Predict 2）都依赖其 backbone。

**劣势**：不直接产出 action（需搭配 policy 模块）；Cosmos 自身缺乏 robotics task 的定量评估。

### 路线 4：状态空间世界模型 (State-Space World Models)

**核心思路**：在低维 state space 而非 pixel space 建模环境动力学，通过 model-based RL 优化 policy。

**代表论文**：
- [[2501-RoboticWorldModel|Robotic World Model]]：dual-autoregressive GRU 架构，self-supervised training 匹配训练/推理分布，解决 error accumulation。MBPO-PPO 在 ANYmal D 和 Unitree G1 上实现 zero-shot sim-to-real transfer。ETH Zurich。

**优势**：计算高效（预训练 50min + policy 5min，inference 1ms/step）；sim-to-real 验证充分。

**劣势**：仅限低维 proprioceptive state（joint angle、force），不处理 visual observation；与 VLA 趋势（端到端视觉-语言-动作）相距较远；对比 model-free RL 优势微弱。

## 发展时间线

```
2024.06  IRASim — Frame-level action-conditioned video prediction (ByteDance)
         └─ 奠基：证明 action-frame alignment 对 world model 质量至关重要

2025.01  Cosmos — NVIDIA World Foundation Model Platform
         └─ 基础设施：开源 video tokenizer + pre-trained WFM，成为下游工作的 backbone

2025.01  Robotic World Model — State-space world model for locomotion (ETH)
         └─ 经典路线：model-based RL + zero-shot sim-to-real

2025.04  UWM — Unified video+action diffusion (RSS 2025, UW + TRI)
         └─ 突破：decoupled timesteps 统一 world model 与 policy

2025.05  DreamGen — Video WM as synthetic data generator (CoRL 2025, NVIDIA)
         └─ 应用：video generation 作为 robot learning 的 data flywheel

2025.12  Motus — Unified latent action world model (Tsinghua)
         └─ 推进：MoT 架构 + optical flow latent action，5 种建模模式统一

2026.02  World-VLA-Loop — Closed-loop WM + VLA co-optimization (NUS)
         └─ 闭环：world model 与 VLA policy 迭代互利

2026.02  DreamZero — World Action Model 定义 (NVIDIA)
         └─ 里程碑：正式提出 WAM 概念，14B 模型 2x 超越 VLA，7Hz 实时控制
```

**关键趋势**：
1. **从辅助到核心**：world model 从 policy evaluation 工具（IRASim）→ data generator（DreamGen）→ 直接作为 policy（DreamZero）
2. **从分离到统一**：video prediction 和 action prediction 从独立模块 → unified architecture（UWM, Motus, DreamZero）
3. **从 pixel 到 foundation**：从单个 task-specific model → platform-level foundation model（Cosmos）→ 在其上 post-training（World-VLA-Loop）

## Paper Comparison

| Paper | Venue | 技术路线 | 核心方法 | 关键结果 | 局限性 |
|:------|:-----|:---------|:---------|:---------|:-------|
| [[2406-IRASim\|IRASim]] | ICCV 2025 | Action-conditioned video | DiT + frame-level action conditioning | Policy eval r=0.99; Push-T IoU 0.637→0.961 | 非实时生成；核心组件为已有技术组合 |
| [[2501-Cosmos\|Cosmos]] | arXiv | World Foundation Model | Diffusion/AR WFM + video tokenizer | PSNR 35.85 (DAVIS); 2-12x faster tokenizer | 缺乏 robotics task 定量评估；10K H100 |
| [[2501-RoboticWorldModel\|Robotic World Model]] | arXiv | State-space world model | Dual-autoregressive GRU + MBPO-PPO | ANYmal D zero-shot sim-to-real; 1ms inference | 仅 proprioceptive state；对比 model-free 优势微弱 |
| [[2504-UWM\|UWM]] | RSS 2025 | Joint video+action | Decoupled diffusion timesteps | Real robot +20% over DP; LIBERO 0.79 | 主要收益来自 pretraining 而非架构 |
| [[2505-DreamGen\|DreamGen]] | CoRL 2025 | WM-driven policy | Video WM → IDM → co-train policy | 22 novel behaviors; cross-embodiment GR1/Franka/SO-100 | 1500 L40 GPU×54h; IDM 仍需 robot-specific 数据 |
| [[2512-Motus\|Motus]] | arXiv | Joint latent action | MoT + optical flow latent action | RoboTwin 87.02%; +45% over π0.5 | 依赖 optical flow; 18K GPU hours 预训练 |
| [[2602-WorldVLALoop\|World-VLA-Loop]] | arXiv | WM-driven policy (RL) | State-aware WM + co-evolving closed loop | LIBERO +12.7%; real robot +23.4% | 仅 short-horizon ~20s; 单任务实验 |
| [[2602-DreamZero\|DreamZero]] | arXiv | Joint video+action (WAM) | 14B AR diffusion, joint video-action | Seen 62.2% (2.3x baseline); unseen 39.5% | 2×GB200 for 7Hz; 6.6s context window |

## Key Takeaways

1. **WAM 是 VLA 的自然演进**：DreamZero 的实验证明，联合建模 video + action 在泛化能力上远超纯 action prediction（VLA）。World modeling 提供的 physical dynamics understanding 是 zero-shot generalization 的关键来源。

2. **Video generation 是 WAM 的核心引擎**：所有主要工作都基于 video diffusion / video generation 模型。Internet-scale video pretraining 所蕴含的 physics knowledge 是 WAM 泛化的基础。Cosmos 平台化 + DreamZero/Motus 端到端训练的组合正在成为主流技术栈。

3. **Unified architecture 优于 pipeline**：UWM 和 Motus 证明，在同一模型中联合训练 video 和 action 比分离 pipeline（先 predict video 再 extract action）效果更好。关键设计包括 decoupled diffusion timesteps（UWM）和 Mixture-of-Transformers（Motus）。

4. **Action-free video data 是核心数据优势**：WAM 最大的差异化优势之一是能自然利用海量无 action label 的视频数据。UWM 的 cotraining、DreamGen 的 neural trajectories、Motus 的 optical flow latent action 都在不同层面验证了这一点。

5. **计算成本是主要瓶颈**：DreamZero 需要 2×GB200 GPU 实现 7Hz，DreamGen 生成数据需 1500×L40 GPU，Cosmos 预训练需 10,000×H100。这制约了 WAM 在资源有限实验室的可复现性和在消费级硬件上的部署。**建议加入 DomainMaps**：world-model 作为新 domain，与 VLA domain 存在强关联。

## Open Problems

1. **Long-horizon reasoning 缺失**：当前所有 WAM 本质上是 "System 1" reactive model，context window 有限（DreamZero 6.6s，World-VLA-Loop ~20s）。如何在 WAM 中引入 hierarchical planning 或 explicit memory 来支持分钟级别的 long-horizon 任务，是核心未解难题。

2. **Scaling laws 未知**：尽管 DreamGen 展示了 log-linear scaling 趋势，Motus 和 DreamZero 的 scaling behavior 尚未被系统研究。WAM 是否存在类似 LLM 的 power-law scaling，optimal compute allocation 在 video vs. action 之间如何分配，均无明确结论。

3. **High-precision manipulation 不足**：当前 WAM 在 pick-and-place 级别任务上表现优异，但 sub-centimeter 精度任务（如插钥匙、电子装配）的表现尚不理想。Video prediction 的 pixel-level 精度是否足以支撑精细操作，值得深入探索。

4. **Real-time inference gap**：联合 video+action generation 的计算开销远超纯 action prediction。DreamZero 的 38x 加速工程值得关注，但 7Hz on 2×GB200 仍远不及 VLA 在消费级 GPU 上的 20Hz+。Model distillation、speculative decoding 等技术在 WAM 上的适用性尚待验证。

5. **Evaluation framework 缺失**：现有 benchmark（LIBERO、RoboTwin、Push-T）侧重 success rate，缺少对 physical consistency、temporal coherence、action-video alignment 的系统评估。DreamGen Bench 和 TokenBench 是初步尝试，但远未形成共识标准。

6. **Cross-embodiment 的系统验证不足**：DreamZero 和 DreamGen 初步验证了 cross-embodiment transfer（robot-to-robot, human-to-robot），但实验规模有限。能否 scale 到 internet-scale human video → diverse robot fleet 的大规模迁移，是决定 WAM paradigm 上限的关键问题。

## 调研日志

- **调研日期**: 2026-03-30
- **论文统计**: vault 已有 0 篇 + 新 digest 8 篇 + 跳过 0 篇
- **未能获取**: 无
