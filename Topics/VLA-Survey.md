---
title: Vision-Language-Action (VLA) Models Survey
tags:
  - VLA
  - manipulation
  - flow-matching
  - cross-embodiment
  - survey
date_updated: 2026-03-30
year_range: 2023-2026
papers_analyzed: 20
---
## Overview

Vision-Language-Action (VLA) 模型是将预训练 Vision-Language Models (VLMs) 扩展为 robot policy 的新范式，旨在通过统一视觉感知、语言理解和动作生成，构建跨任务、跨平台的通用机器人基础模型。该领域自 2023 年 RT-2 开创以来，经历了爆发式增长，短短三年内从"概念验证"演进到"真实家庭部署"。

**核心问题**：如何让机器人像 LLM 理解文本一样理解物理世界，并将互联网规模的视觉-语言知识迁移到机器人控制？传统 robot learning 受限于数据稀缺和 task-specific 设计，VLA 范式通过利用预训练 VLM 的泛化能力，有望突破这一瓶颈。

**研究活跃度**：2024-2026 年是 VLA 研究的井喷期——仅 arXiv 上的 VLA survey 就有 8+ 篇，主要会议（CoRL, RSS, ICML, NeurIPS, ICLR 2026）均有大量 VLA 论文。竞争格局从 Physical Intelligence 一家独大扩展为多巨头混战：Google DeepMind（Gemini Robotics）、NVIDIA（GR00T N1）、Figure AI（Helix）、Physical Intelligence（π 系列）、GigaAI（GigaBrain）以及开源社区（OpenVLA、SmolVLA、X-VLA）形成了多层次的技术路线竞争。

**整体趋势**：
1. **Action representation 从 discrete 到 continuous**：RT-2 的 token 预测 → Octo 的 diffusion → π₀ 的 flow matching，控制频率从 3 Hz 提升到 50-200 Hz
2. **Dual-System 架构成为共识**：π0.5、GR00T N1、Gemini Robotics、Helix 均采用 System 2（VLM 语义推理，~10 Hz）+ System 1（action 生成，50-200 Hz）的分层设计
3. **从 imitation 到 world model-conditioned RL**：π\*₀.₆ 的 Recap → GigaBrain 的 RAMP，RL 自我改进正从简单 advantage conditioning 演化为 world model-conditioned learning
4. **从大模型到高效模型**：SmolVLA（0.45B）、X-VLA（0.9B）、DM0（2B）证明精心设计的小模型可匹敌甚至超越大模型（3-4B）
5. **从实验室到真实世界**：π0.5 在全新家庭环境完成 10-15 分钟长时域任务，Gemini Robotics 折纸 100% 成功率，GR00T N1 humanoid 双臂操作 76.8%
6. **Embodied-Native vs. Pretrain-then-Adapt 范式之争**：DM0 挑战了主流的先 VLM 预训练再 robot fine-tune 范式，提出从一开始就融入 physical data
7. **Self-correction 成为新方向**：CycleVLA 首次系统性引入 VLA 自纠错机制，long-horizon 任务提升 39.9%

## 技术路线

### 路线 1：Autoregressive Token Prediction（离散动作生成）

**代表论文**：[[2307-RT2|RT-2]]、[[2406-OpenVLA|OpenVLA]]

**核心思路**：将 robot action 离散化为 token（256 bins），复用 VLM 的 autoregressive next-token prediction 进行动作生成。这是最早也是最直观的 VLA 范式——"actions as language tokens"。

**优势**：
- 直接复用 VLM 架构和预训练权重，无需额外 action head
- 天然支持 language-conditioned control
- RT-2 展示了 emergent reasoning（符号推理、常识迁移）

**劣势**：
- 控制频率低（RT-2 约 3 Hz），无法进行灵巧操作
- 离散化损失动作精度
- Autoregressive 生成慢，序列长度线性增加延迟

**现状**：作为 VLA 范式的奠基工作具有历史意义，但已被 continuous action 方法全面超越。OpenVLA 作为开源 baseline 仍广泛用于对比实验。[[2502-OpenVLA-OFT|OpenVLA-OFT]] 通过 parallel decoding + continuous action + L1 regression 将 OpenVLA 性能从 76.5% 提升至 97.1%（LIBERO），证明 fine-tuning 设计选择比模型规模更重要。

### 路线 2：Flow Matching / Diffusion Action Generation（连续动作生成）

**代表论文**：[[2410-Pi0|π₀]]、[[2405-Octo|Octo]]、[[2506-SmolVLA|SmolVLA]]

**核心思路**：用 flow matching（或 diffusion）建模连续 action 分布，通过 action expert 独立于 VLM backbone 进行动作生成。Action chunking（一次预测多步）进一步提升控制频率。

**优势**：
- 高频连续控制（π₀ 达 50 Hz），支持灵巧操作
- Action expert 的 MoE 设计避免 action loss 破坏 VLM 预训练分布
- Flow matching 对 multimodal action distribution 建模更准确

**劣势**：
- 需要额外的 action expert 参数（π₀ 的 300M action expert）
- Flow matching 的 denoising 步骤增加推理计算
- 最优 action chunk 长度需要 task-specific 调优

**现状**：目前性能最强的 VLA 技术路线。π₀ 系列占据该路线的领导地位，SmolVLA（0.45B）和 [[2510-XVLA|X-VLA]]（0.9B，ICLR 2026）证明 flow matching 在极小参数量下也能高效工作。[[2503-GR00TN1|GR00T N1]]（NVIDIA）将该范式扩展到 humanoid，120 Hz 控制频率。[[2412-RoboVLMs|RoboVLMs]] 的 600+ 实验系统验证了 continuous action + policy head history fusion 是最优配置。[[2603-DAMVLA|DAM-VLA]] 进一步将 diffusion action head 拆分为 arm/gripper 双头，针对不同操作模式独立建模。

### 路线 3：Hierarchical VLM-VLA（分层架构）

**代表论文**：[[2504-Pi05|π0.5]]、[[2502-HiRobot|Hi Robot]]、[[2412-NaVILA|NaVILA]]、[[2503-GR00TN1|GR00T N1]]、[[2503-GeminiRobotics|Gemini Robotics]]

**核心思路**：将 policy 分为两层——高层 VLM 进行语义推理和子任务规划（"what to do"），低层 VLA 生成精细动作（"how to do"）。这对应认知科学中的 System 2（deliberative）+ System 1（reactive）。

**优势**：
- 自然解耦语义理解和运动控制，各层可独立优化
- 支持 open-ended 指令理解和实时用户纠正（Hi Robot）
- 适用于 long-horizon 多步任务
- 架构天然兼容 navigation + manipulation 统一（NaVILA 用语言动作桥接）

**劣势**：
- 高层和低层通常独立训练，缺乏 end-to-end joint optimization
- 高层推理延迟（~1 Hz）与低层控制频率（10-50 Hz）不匹配
- Error propagation：低层失败时高层不一定能感知

**现状**：成为 2025-2026 年的绝对主流。π0.5 在全新家庭完成 10-15 分钟任务，Hi Robot 超越 GPT-4o 40%+。这一架构已被工业界全面采纳：NVIDIA GR00T N1（Eagle-2 VLM @10Hz + DiT @120Hz）、Google Gemini Robotics（Cloud Gemini 2.0 + Local Action Decoder @50Hz）、Figure AI Helix（VLM @7-9Hz + Policy @200Hz）均采用 System 2 + System 1 设计。Dual-system 已不只是学术方案，而是 industry consensus。

### 路线 4：RL Self-Improvement（强化学习自我改进）

**代表论文**：[[2511-PiStar06|π*₀.₆]]、[[2603-RoboClaw|RoboClaw]]、[[2602-GigaBrain|GigaBrain-0.5M*]]

**核心思路**：在 imitation learning 之后，通过真实世界部署经验进行 RL fine-tuning，突破 demonstration 数据质量的性能上限。π\*₀.₆ 的 Recap 算法用 advantage-conditioned policy extraction 绕过了 PPO 对 flow matching 的兼容性问题。

**优势**：
- 突破 imitation learning 天花板，从自身错误中学习
- Advantage conditioning 是 model-agnostic 的 RL 方法，兼容 flow matching
- 支持异构数据（demos + autonomous rollouts + interventions）统一训练

**劣势**：
- 仍需人工 reward labeling 和 intervention
- Exploration 策略简单，无 sophisticated exploration
- Batch offline RL，非 continuous online learning

**现状**：VLA 研究的最新前沿。π\*₀.₆ 在 laundry folding 等任务上实现 >2× throughput 提升，13 小时连续部署验证了实用性。[[2602-GigaBrain|GigaBrain-0.5M*]] 的 RAMP 框架将 world model latent representation 引入 RL 训练，理论证明 RECAP 是 RAMP 的退化特例，在 RoboChallenge 上排名第一（51.67%）。RoboClaw 的 EAP（Entangled Action Pairs）提供了自主数据收集的替代方案。RL self-improvement 正从简单的 advantage conditioning 演化为 world model-conditioned learning。

### 路线 5：Embodied-Native Training（原生物理训练）

**代表论文**：[[2602-DM0|DM0]]

**核心思路**：摒弃主流的 "Pretrain-then-Adapt" 范式（先 internet VLM 预训练，再 robot fine-tune），从训练起点就将 physical data 作为一等公民，统一 web text、autonomous driving 和 embodied interaction 数据进行联合训练。

**优势**：
- 模型从一开始就获得 physical priors，避免 domain gap
- Gradient decoupling 有效防止 action training 侵蚀 VLM semantic capacity
- Spatial Scaffolding（subtask → bbox → trajectory → action）构成自然的 coarse-to-fine 课程
- 单一模型统一 manipulation 和 navigation

**劣势**：
- 数据工程复杂度极高（1.2T tokens pretraining + 200M mid-training）
- 三阶段 pipeline 复现成本大
- Real-world navigation 评测不足

**现状**：DM0 仅 2B 参数在 RoboChallenge Table30 达到 62% SR，超越 GigaBrain-0.1（3B, 51.67%）和 π0.5（3B, 42.67%）。Embodied-Native 理念是否真正优于 Pretrain-then-Adapt 还需更多 controlled ablation 验证，但 2B 打败 3-4B 的结果暗示 data recipe 比 model scaling 更重要。

### 路线 6：Self-Correction / Error Recovery（自纠错与错误恢复）

**代表论文**：[[2601-CycleVLA|CycleVLA]]

**核心思路**：为 VLA 赋予主动自纠错能力——在错误完全发生前检测异常并触发 subtask backtracking，而非事后被动应对。这是 VLA 走向真实世界部署的关键能力。

**优势**：
- Proactive 而非 reactive：通过 progress tracking 在错误萌芽阶段就介入
- MBR decoding 作为 zero-shot test-time scaling，无需额外训练即可提升 retry 成功率
- Long-horizon 任务改善极为显著（+39.9%）

**劣势**：
- 依赖可逆性假设（contact-rich 或不可逆操作中不成立）
- 需要外部 VLM（GPT-5.2）作为 failure predictor
- 目前仅在 simulation 验证

**现状**：CycleVLA 在 LIBERO 上平均 +18.8%，long-horizon +39.9%。Self-correction 是 VLA 安全部署的关键缺失能力，但当前方法仍有较强假设约束。

## 发展时间线

| 时间 | 里程碑 | 意义 |
|:-----|:-------|:-----|
| 2023-07 | [[2307-RT2\|RT-2]] (Google DeepMind) | 🏆 VLA 范式开创：Actions as Tokens，证明 VLM→robot control 可行 |
| 2024-05 | [[2405-Octo\|Octo]] (UC Berkeley) | 首个开源 generalist robot policy，diffusion action head |
| 2024-06 | [[2406-OpenVLA\|OpenVLA]] (Stanford) | 7B 开源 VLA baseline，超越 55B RT-2-X，降低研究门槛 |
| 2024-10 | [[2410-Pi0\|π₀]] (Physical Intelligence) | 🏆 Flow matching + action expert 范式，50 Hz 灵巧操作 |
| 2024-12 | [[2412-NaVILA\|NaVILA]] (NVIDIA) | VLA 扩展到 navigation，语言作为 mid-level action |
| 2024-12 | [[2412-RoboVLMs\|RoboVLMs]] (Tsinghua/ByteDance) | 600+ 实验系统研究 VLA 设计选择 |
| 2025-02 | [[2502-HiRobot\|Hi Robot]] (Physical Intelligence) | Hierarchical VLM-VLA，超越 GPT-4o |
| 2025-02 | [[2502-OpenVLA-OFT\|OpenVLA-OFT]] (Stanford) | Fine-tuning 优化，26× 推理加速，97.1% LIBERO |
| 2025-03 | [[2503-GR00TN1\|GR00T N1]] (NVIDIA) | 🏆 首个开源 humanoid VLA，dual-system + Data Pyramid，76.8% real-world |
| 2025-03 | [[2503-GeminiRobotics\|Gemini Robotics]] (Google DeepMind) | 🏆 Gemini 2.0→robot control，折纸 100%，Google 重返 VLA 赛道 |
| 2025-04 | [[2504-Pi05\|π0.5]] (Physical Intelligence) | 🏆 Open-world generalization，全新家庭 10-15 分钟任务 |
| 2025-06 | [[2506-SmolVLA\|SmolVLA]] (Hugging Face) | 0.45B 紧凑 VLA，证明小模型可比大模型 |
| 2025-10 | [[2510-XVLA\|X-VLA]] (Tsinghua/Shanghai AI Lab) | 🏆 ICLR 2026 + IROS 冠军，soft prompt cross-embodiment，0.9B SOTA |
| 2025-11 | [[2511-PiStar06\|π*₀.₆]] (Physical Intelligence) | 🏆 首次 VLA RL 自我改进，>2× throughput |
| 2026-01 | [[2601-CycleVLA\|CycleVLA]] (Oxford/Cambridge) | VLA self-correction 首作，long-horizon +39.9% |
| 2026-02 | [[2602-DM0\|DM0]] (Dexmal) | Embodied-Native VLA，2B 超越 3-4B 竞品，62% Table30 |
| 2026-02 | [[2602-GigaBrain\|GigaBrain-0.5M*]] (GigaAI) | World model RL (RAMP)，证明 RECAP 是退化特例 |
| 2026-03 | [[2603-MEM\|MEM]] (Physical Intelligence) | 多尺度记忆，15 分钟级长任务 |
| 2026-03 | [[2603-RoboClaw\|RoboClaw]] (HKU/Galbot) | Agentic VLA，自主数据收集 + long-horizon |
| 2026-03 | [[2603-DAMVLA\|DAM-VLA]] | Arm/gripper 解耦双头 VLA，SIMPLER 83% |

## Paper Comparison

| Paper | Venue | 技术路线 | 核心方法 | 关键结果 | 局限性 |
|:------|:-----|:---------|:---------|:---------|:-------|
| [[2307-RT2\|RT-2]] | CoRL 2023 | Token Prediction | PaLM-E/PaLI-X + action tokenization | Emergent reasoning 3×提升 | 3 Hz 低频，55B 巨大，未开源 |
| [[2405-Octo\|Octo]] | RSS 2024 | Diffusion | Transformer + diffusion head，27M/93M | 9 平台验证，开源生态 | 参数量小，无 VLM 预训练 |
| [[2406-OpenVLA\|OpenVLA]] | ICML 2025 | Token Prediction | Llama 2 7B + DINOv2/SigLIP | 超 RT-2-X 16.5%，开源 | Autoregressive 低频 |
| [[2410-Pi0\|π₀]] | RSS 2025 | Flow Matching | PaliGemma 3B + flow matching expert | 50 Hz，超越 OpenVLA/Octo | 数据配比 heuristic |
| [[2412-NaVILA\|NaVILA]] | RSS 2025 | Hierarchical | VILA + mid-level language action + RL | R2R-CE 54% SR，real 88% | 仅 navigation |
| [[2412-RoboVLMs\|RoboVLMs]] | arXiv | Benchmark | 8 backbone × 4 架构，600+ 实验 | CALVIN 4.49 SOTA | 仅 table-top |
| [[2502-HiRobot\|Hi Robot]] | arXiv | Hierarchical | VLM planner + π₀ executor + synthetic data | 超 GPT-4o 40%+ IA | Navigation 有限 |
| [[2502-OpenVLA-OFT\|OpenVLA-OFT]] | RSS 2025 | Optimized FT | Parallel decoding + continuous + L1 | LIBERO 97.1%，26× 加速 | 仅验证 OpenVLA |
| [[2504-Pi05\|π0.5]] | arXiv | Hierarchical + FM | Hierarchical inference + co-training | 全新家庭 50-85% | 无 memory |
| [[2506-SmolVLA\|SmolVLA]] | arXiv | Efficient FM | 0.45B + layer skip + community data | LIBERO 87.3%，快 40% | 短 horizon 为主 |
| [[2511-PiStar06\|π*₀.₆]] | arXiv | RL + FM | Recap: advantage-conditioned RL | >2× throughput，13h 部署 | 需人工 reward |
| [[2503-GR00TN1\|GR00T N1]] | arXiv | Dual-System FM | Eagle-2 VLM + DiT flow matching, Data Pyramid, latent actions | Real-world 76.8%，humanoid bimanual | 仅 tabletop manipulation |
| [[2503-GeminiRobotics\|Gemini Robotics]] | arXiv | Cloud+Local VLA | Gemini 2.0 cloud backbone + local decoder, ALOHA 2 | 折纸 100%，cross-embodiment 63% | 未开源，sim2real gap |
| [[2510-XVLA\|X-VLA]] | ICLR 2026 | Soft Prompt FM | Soft prompt + flow matching, 0.9B | ICLR 2026，IROS 冠军，LIBERO SOTA | 数据规模有限（290K） |
| [[2601-CycleVLA\|CycleVLA]] | arXiv | Self-Correction | Progress-aware VLA + VLM failure predictor + MBR decoding | LIBERO +18.8%，Long +39.9% | 仅 simulation，可逆性假设 |
| [[2602-DM0\|DM0]] | arXiv | Embodied-Native | 三阶段训练 + gradient decoupling + Spatial Scaffolding | Table30 62% SOTA，2B 超 3-4B | Benchmark 较新，复现成本高 |
| [[2602-GigaBrain\|GigaBrain-0.5M*]] | arXiv | World Model RL | RAMP: world model latent conditioned RL | RoboChallenge #1，~30% 提升 | 内部评估为主 |
| [[2603-MEM\|MEM]] | arXiv | Memory + FM | 视频短期记忆 + 语言长期记忆 | 15min 任务 70-80% | 仅 π₀.₆ 验证 |
| [[2603-RoboClaw\|RoboClaw]] | arXiv | Agentic | VLM agent + EAP 自主数据收集 | +25% SR，-53.7% 人工 | Cloud VLM 延迟 |
| [[2603-DAMVLA\|DAM-VLA]] | arXiv | Dual-Head Diffusion | Arm/gripper 解耦双头 + action routing + dual-scale weighting | SIMPLER 83%，real 86.8% | 二元切换假设 |

## Key Takeaways

1. **Dual-System + Flow Matching 已成为工业界共识**：不再仅是学术方案——NVIDIA GR00T N1、Google Gemini Robotics、Figure AI Helix、Physical Intelligence π 系列均采用 System 2（VLM ~10 Hz）+ System 1（action generation 50-200 Hz）架构，flow matching 是 action generation 的事实标准。

2. **Fine-tuning 设计和 data recipe 比模型规模更重要**：DM0（2B）超越 π0.5（3B）和 GigaBrain（3B）在 Table30 上 20+ 百分点；SmolVLA（0.45B）超越 OpenVLA（7B）；X-VLA（0.9B）在 LIBERO 上达到 SOTA。"小而精"持续挑战 "bigger is better"。（建议加入 DomainMaps：Established Knowledge）

3. **Data diversity >> Data specificity，但数据整合方式是关键**：π0.5 的 co-training + post-training、GR00T N1 的 Data Pyramid（人类视频 → 合成数据 → 真实数据）、DM0 的 Embodied-Native 三阶段训练，三种不同的 data recipe 策略均有效，共识是异构数据整合本身比单一来源的数据量更重要。

4. **RL 正从 advantage conditioning 演化为 world model-conditioned learning**：π\*₀.₆ 的 RECAP 开创了 VLA RL 自我改进，GigaBrain 的 RAMP 理论证明 RECAP 是其退化特例——通过引入 world model latent representation 进一步提升 foresight 能力。这标志着 VLA RL 从简单的 reward labeling 走向结构化的 world knowledge 利用。（建议加入 DomainMaps：Active Debates）

5. **Cross-embodiment 进入实用阶段**：X-VLA 的 soft prompt（1% 参数适配新平台）、GR00T N1 的 embodiment-specific MLPs + latent action、Gemini Robotics 的 cross-embodiment 迁移（ALOHA 2 → Franka → Apollo），三种方案证明 cross-embodiment 不再只是理想，而是可工程化的能力。

6. **Self-correction 是安全部署的缺失关键能力**：CycleVLA 首次系统性引入 VLA proactive self-correction，long-horizon +39.9% 的提升证明了其价值。但当前方案受限于可逆性假设和外部 VLM 依赖，real-world self-correction 仍有很大探索空间。

7. **开源生态持续加速**：从 Octo → OpenVLA → SmolVLA → X-VLA → GR00T N1，开源 VLA 的能力不断提升。X-VLA 已集成到 LeRobot 平台，GR00T N1 开源了模型+代码+数据。开源使得学术组以 0.9B-2B 参数量就能竞争甚至超越工业界闭源大模型。

## Open Problems

1. **Navigation + Manipulation 统一**：DM0 迈出了重要一步（在单一模型中统一两者，specialist 62% SR），但其 navigation 能力主要来自 Habitat simulation，real-world 验证不足。如何在真实部署中同时支持 building-scale navigation 和灵巧操作仍是核心开放问题。参见 [[VLN-VLA-Unification]]。

2. **长期记忆与空间理解**：MEM 初步解决了 15 分钟级记忆，但缺乏 explicit spatial memory。GR00T N1 和 Gemini Robotics 均无 spatial memory 组件。如何让 VLA 维护 persistent、incrementally updated 的空间表示（如 3D scene graph）以支持跨房间任务？

3. **Fully Autonomous Self-Improvement**：尽管 RL 方向快速推进（RECAP → RAMP），GigaBrain 的 RAMP 仍需 human-in-the-loop rollout collection，RoboClaw 的 EAP 减少但未消除人工。World model 是否能提供足够准确的 reward signal 来完全替代人工标注？

4. **World Model 在 VLA 中的最优角色**：GigaBrain 用 world model 做 latent conditioning，WorldVLALoop 用 world model 做 reward prediction，DreamGen 用 world model 生成 synthetic trajectories。World model 应作为 training signal provider、data augmenter 还是 inference-time planner？这三种角色是否可以统一？

5. **Cross-Embodiment 的最优处理方式**：X-VLA 的 soft prompt、GR00T N1 的 embodiment-specific MLPs + latent action、DM0 的 gradient decoupling、Gemini Robotics 的 foundation model 迁移——四种方案各有优劣。什么条件下哪种方案最优？Zero-shot cross-embodiment（无需 fine-tuning 直接部署新平台）何时可行？

6. **Self-Correction 与安全部署**：CycleVLA 开创性地引入了 proactive self-correction，但受限于可逆性假设和外部 VLM 依赖。对于 contact-rich、不可逆操作（切割、倒液体），如何实现 self-correction？如何在不显著增加延迟的前提下集成 safety monitoring？

7. **VLA 的 Scaling Law**：SmolVLA（0.45B）、X-VLA（0.9B）、DM0（2B）频繁超越更大模型，暗示 VLA 的 scaling law 与 LLM 有根本不同。模型规模、数据规模、数据多样性、training recipe 之间的 scaling 关系尚不清楚。X-VLA 报告三个维度均未饱和，但系统性 scaling 研究缺失。

8. **Benchmark 碎片化**：LIBERO、SIMPLER、CALVIN、Table30、RoboChallenge 等 benchmark 各有侧重，不同论文在不同 benchmark 上声称 SOTA，缺乏统一的、全面的评测标准。ERQA（Gemini Robotics 提出）填补了 embodied reasoning 评测空白，但 end-to-end manipulation 的"标准 benchmark"仍未确立。

## 调研日志

### 第二轮更新（2026-03-30）
- **调研日期**: 2026-03-30
- **论文统计**: vault 已有 13 篇 + 新 digest 7 篇（成功 7 / 跳过 0 / 失败 0），总计 20 篇
- **新增论文**: GR00T N1, Gemini Robotics, X-VLA, CycleVLA, DM0, GigaBrain-0.5M*, DAM-VLA
- **未能获取**: Figure AI Helix（无 arXiv 论文，仅 blog post）

### 第一轮（2026-03-27）
- **调研日期**: 2026-03-27
- **论文统计**: vault 已有 10 篇 + 新 digest 3 篇 + 跳过 0 篇
- **未能获取**: 无
