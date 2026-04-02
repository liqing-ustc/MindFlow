---
title: "Language-Conditioned Mobile Manipulation: From Modular Pipelines to End-to-End VLA"
tags: [mobile-manipulation, VLA, instruction-following, task-planning, scene-understanding]
date_updated: "2026-04-02"
year_range: 2023-2026
papers_analyzed: 24
---
## Overview

Language-conditioned mobile manipulation（LCMM）是 embodied AI 的核心挑战之一：机器人需要理解自然语言指令，在大规模环境中自主导航到目标位置，并完成精细操作。它同时涉及 language understanding、spatial reasoning、navigation 和 dexterous manipulation，是 VLN 和 VLA 两个领域的交叉地带。

**研究现状**：该领域正经历从"模块化 pipeline"向"端到端 VLA"的范式转变。早期工作（SayCan、TidyBot、OK-Robot）采用 LLM/VLM 做高层规划 + 独立 skill 模块执行的模块化架构，验证了 language-conditioned 任务的可行性但受限于模块间的信息断裂。2024-2025 年，VLA 模型开始向 mobile manipulation 延伸——MoManipVLA 尝试将 fixed-base VLA 迁移到移动场景，EchoVLA 为 VLA 增加空间记忆，SG-VLA 通过 auxiliary spatial grounding 增强 VLA 的空间理解。2025-2026 年，端到端统一架构出现：DM0 首次在同一框架中训练 navigation 和 manipulation，WholeBodyVLA 用 latent action 从无 action 标注视频学习全身控制，π0.5/Hi Robot 实现了 15 分钟级家务任务。

**核心难点**：
1. **Action space mismatch**：navigation（2-3D 底盘速度，~5 Hz）和 manipulation（6-7 DoF 末端控制，30-50 Hz）的控制频率和维度差异巨大
2. **Spatial representation gap**：导航需要 building-scale 的空间记忆（semantic map / scene graph），操作需要 object-level 的精细感知，两者缺乏统一表示
3. **Long-horizon reasoning**：LCMM 任务通常需要 10+ 步的多阶段推理（find → navigate → pick → navigate → place），错误在长 horizon 中累积
4. **数据稀缺**：真实 mobile manipulation 数据采集成本极高，simulation 与真实世界的 gap 显著

**整体趋势**：该领域正沿三个方向收敛——（1）端到端 VLA 替代模块化 pipeline；（2）显式空间表示（3D scene graph、semantic map）作为 VLA 的增强模块；（3）hierarchical 架构（VLM reasoning + VLA execution）成为平衡语义理解和精细控制的主流范式。

## 技术路线

### 路线 1：模块化 Pipeline（LLM/VLM Planning + Skill Library）

**核心思路**：用 LLM/VLM 做高层任务规划和语义理解，调用预定义的 skill 模块（navigation、grasping、placing）执行底层控制。各模块独立开发、独立优化。

**代表论文**：
- [[Papers/2204-SayCan|SayCan]]（2022）：开创性工作。LLM 生成候选技能序列，learned affordance function 评估每个技能在当前状态下的可行性，两者乘积做 scoring 选择最优技能。在 Everyday Robot 上实现 84% planning SR，但受限于 551 个预定义技能的覆盖范围。
- [[Papers/2305-TidyBot|TidyBot]]（2023）：LLM 从少量用户示例中归纳个性化偏好规则（如"衣服放衣柜，书放书架"），通过 CLIP 分类将规则泛化到未见物体。真实世界 85% SR。亮点在于 **personalization** 而非通用 planning。
- [[Papers/2401-OKRobot|OK-Robot]]（2024）：Zero-shot 模块化系统，集成 OWL-ViT（检测）+ VoxelMap（语义地图）+ AnyGrasp（抓取），无需任何训练即可在真实家庭环境中 pick-and-drop，58.5% SR。证明 off-the-shelf foundation models 组合已有实用价值。
- [[Papers/2410-BUMBLE|BUMBLE]]（2024）：Building-scale mobile manipulation。VLM 统一处理感知和推理，Set-of-Mark prompting 将深度信息注入 VLM，双层记忆（短期执行历史 + 长期失败案例）。3 栋建筑 70 次试验 47.1% SR。核心发现：**73.7% 的失败来自 VLM 推理错误**，spatial reasoning 是核心瓶颈。
- [[Papers/2602-UniPlan|UniPlan]]（2026）：VLM 做视觉语义 grounding → PDDL predicates，Fast Downward solver 做符号规划。通过 AST 操作将 tabletop PDDL domain 扩展到 mobile manipulation。50 个任务 ~84% SR，仅需 2 次 LLM 调用（baselines 需 4-9 次），规划时间 <0.7s。

**优势**：模块间可独立升级；利用成熟的 foundation models（CLIP、GPT-4V、SAM）；工程可行性高。
**局限**：模块间信息断裂导致错误传播；skill library 限制了任务覆盖范围；无法端到端优化全链路；BUMBLE 的实验清楚表明 VLM spatial reasoning 是系统瓶颈。

### 路线 2：端到端 VLA 适配 Mobile Manipulation

**核心思路**：将已有的 table-top VLA 模型（π₀、OpenVLA 等）扩展到 mobile manipulation 场景，解决 action space 扩展、spatial grounding 增强等问题。

**代表论文**：
- [[Papers/2503-MoManipVLA|MoManipVLA]]（2025, CVPR）：将 fixed-base VLA（OpenVLA-7B）的 EEF waypoints 通过双层轨迹优化（上层优化底盘位置，下层优化臂轨迹）转换为 mobile manipulation 轨迹。OVMM 49.4% SR。但**使用 GT segmentation 时 49.4%，切换到 Detic 后骤降至 11.3%**，暴露了感知而非规划是真正瓶颈。
- [[Papers/2603-SGVLA|SG-VLA]]（2026）：为 VLA 添加 5 个 auxiliary spatial grounding decoder（机器人位置、关节配置、抓取 affordance、目标物体位姿、分割 mask），通过渐进式 3 阶段训练注入空间理解。ManiSkill-HAB 上平均 SR 从 0.60 提升至 0.73（+22%）。关键发现：temporal history 反而降低性能（0.60 → 0.49），naive co-training 导致性能崩溃（0.60 → 0.51），progressive training 是关键。
- [[Papers/2511-EchoVLA|EchoVLA]]（2025）：为 VLA 增加双重 declarative memory——scene memory（3D voxel map + discrepancy-driven 更新）和 episodic memory（token FIFO buffer），通过 hierarchical coarse-to-fine attention 检索，per-part（base/arm）diffusion policy 生成动作。Mobile manipulation SR 0.31（+55% over π0.5 baseline）。
- [[Papers/2509-AnywhereVLA|AnywhereVLA]]（2025）：模块化集成 SLAM + frontier exploration + SmolVLA（450M），在嵌入式硬件（Jetson Orin NX）上 >10Hz 运行。仅 50 条 teleoperation demos 即可达 80% manipulation SR。但实验规模极小（50 episodes, 单一环境），无 baseline 对比。

**优势**：继承 VLA 预训练的视觉-语言理解能力；端到端训练避免模块间信息断裂；可利用大规模 manipulation 数据。
**局限**：现有 VLA 的 spatial reasoning 和 navigation 能力不足；从 table-top 到 mobile 的迁移带来 action space 和场景复杂度的双重挑战；绝对性能仍较低（0.31-0.49 SR）。

### 路线 3：统一 Navigation-Manipulation 架构

**核心思路**：从架构层面统一 navigation 和 manipulation，而非简单拼接。包括 hierarchical VLM-VLA 架构和 whole-body end-to-end 控制。

**代表论文**：
- [[Papers/2602-DM0|DM0]]（2026）：Embodied-Native VLA，从训练伊始融合 web、driving、embodied 数据。Spatial Scaffolding 策略（subtask → bbox → trajectory → action）构成自然的 coarse-to-fine 课程学习。2B 参数在 RoboChallenge Table30 上 62% SR，超越 π0.5（3B, 42.67%）。**首次在同一框架中训练 navigation（Habitat sim）和 manipulation**，但 navigation 仅在仿真中验证。
- [[Papers/2504-Pi05|π0.5]]（2025）：Hierarchical inference（VLM 高层规划 → VLA 低层执行），通过 co-training 5 类异构数据实现 open-world generalization。在真实家庭中完成 15 分钟级家务任务（laundry folding、table bussing）。但 **navigation 范围有限**，主要处理 room-scale 移动。
- [[Papers/2502-HiRobot|Hi Robot]]（2025）：Hierarchical VLM-VLA 架构，独立 VLM 做 open-ended 指令理解 + π₀ 做低层执行。通过 synthetic data generation 从少量 teleoperation 数据大规模生成 multi-turn 交互训练数据。超越 GPT-4o baseline 40%+。
- [[Papers/2512-WholeBodyVLA|WholeBodyVLA]]（2025, ICLR 2026）：面向 humanoid 的统一 loco-manipulation VLA。从无 action 标注的 egocentric 视频训练 Latent Action Model（VQ-VAE），VLA 预测 dual latent codes（locomotion + manipulation），LMO RL controller 执行。AgiBot X2 上 78.0% SR（+21.3pp），8x 数据效率。
- [[Papers/2401-MobileALOHA|Mobile ALOHA]]（2024）：End-to-end 全身控制的先驱。ACT policy 直接预测底盘速度 + 双臂关节 + 夹爪的 16D action chunk。Co-training（50 条 mobile demo + 大量 static 数据）将 SR 提升高达 90%。证明了 end-to-end whole-body control 的可行性，但无 language conditioning。

**优势**：从架构层面消除 navigation-manipulation 割裂；端到端优化全链路；hierarchical 设计平衡了语义理解和精细控制。
**局限**：训练数据需求巨大；real-world navigation 验证不足（DM0 仅 sim，π0.5 仅 room-scale）；统一 action space 的设计尚无定论。

**值得关注的相邻进展**：纯 navigation 侧已出现 cross-embodiment foundation model——[[Papers/2509-NavFoM|NavFoM]]（12.7M 样本，Qwen2-7B backbone）zero-shot 覆盖 VLN、ObjectNav、visual tracking、autonomous driving 四类任务和四类平台，VLN-CE RxR 4-view 达 64.4% SR（+8.1% over SOTA）。其 multi-task co-training 的协同效应极为显著（tracking +49.4%、searching +34.9%），进一步验证了跨任务数据共享的价值。将此类 navigation foundation 与 table-top VLA 的 manipulation 能力融合，是实现统一 mobile manipulation 系统的一个自然研究方向。

### 路线 4：Spatial Representation 增强

**核心思路**：构建显式的空间表示（semantic map、3D scene graph）作为 navigation 和 manipulation 的共享基础设施，弥合 VLM/VLA 的 spatial reasoning gap。

**代表论文**：
- [[Papers/2210-VLMaps|VLMaps]]（2022）：将 CLIP/LSeg dense features 融合到 3D 重建的 top-down grid map，创建 language-queryable 空间表示。与 LLM 指令解析结合实现 open-vocabulary 空间导航。
- [[Papers/2309-ConceptGraphs|ConceptGraphs]]（2023）：从 RGB-D 序列用 2D foundation models（SAM、CLIP、GPT-4）构建 open-vocabulary 3D scene graph，无需任何 3D 训练数据。支持 language-conditioned navigation 和 manipulation planning。
- [[Papers/2410-DovSG|DovSG]]（2024, RA-L 2025）：动态可更新的 open-vocabulary 3D scene graph。通过 ACE relocalization + voxel-level change detection 实现增量局部更新（13x 更少内存，20x 更快）。长期任务 SR 33.3% vs 静态 OK-Robot 5.0%，验证了**动态更新对长期操作的关键价值**。
- [[Papers/2306-HomeRobot|HomeRobot/OVMM]]（2023, NeurIPS 2023）：定义了 Open-Vocabulary Mobile Manipulation benchmark（find-pick-find-place in unseen multi-room homes），包含 Habitat 仿真和 Hello Robot Stretch 真机。Baseline real-world SR ~20%。核心发现：**GT segmentation → Detic 导致性能断崖式下降**，perception 是绝对瓶颈。

**优势**：显式空间表示弥补 VLM/VLA 的 spatial reasoning 不足；支持 open-vocabulary 查询；可同时服务 navigation 和 manipulation。
**局限**：构建和维护成本高；动态环境中更新的鲁棒性不足；与端到端 VLA 的集成方式尚不成熟（是否应该作为 VLA 的输入 modality？还是独立模块？）。

## Datasets & Benchmarks

| Benchmark | 类型 | 规模 | 评估指标 | SOTA | 特点 |
|:----------|:-----|:-----|:---------|:-----|:-----|
| **HomeRobot OVMM** | Sim + Real | 多房间家庭环境 | Overall SR | ~49.4% (MoManipVLA, GT seg) | Open-vocabulary, pick-and-place in unseen homes |
| **ManiSkill-HAB** | Sim | 家庭环境 4 类任务 | Success Rate | 0.73 (SG-VLA) | Mobile manipulation, pick/place/open/close |
| **ALFRED** | Sim (AI2-THOR) | 8K+ expert demos, 7 task types | Task SR / GC SR | ~70%+ (recent VLM methods) | Language-guided household tasks |
| **BEHAVIOR-1K** | Sim (OmniGibson) | 1000 活动, 50 场景 | Activity completion | 较低 | 大规模日常活动, 但难度极高 |
| **RoboChallenge Table30** | Real | 30 任务 | Overall SR | 62% (DM0, specialist) | 包含 navigation + manipulation |
| **CALVIN** | Sim | 4 environments, long-horizon | Avg completed tasks | 4.80 (Xiaomi-Robotics-0) | Multi-step language instructions |

**关键观察**：
- 没有一个 benchmark 完整覆盖 "open-vocabulary + building-scale navigation + dexterous manipulation + language instruction" 的全链路。HomeRobot OVMM 最接近但 manipulation 简化（snap grasping in sim），RoboChallenge Table30 有真实操作但 navigation 有限。
- **Perception 是跨 benchmark 的一致瓶颈**：HomeRobot（GT seg → Detic 性能断崖）、MoManipVLA（GT → Detic 从 49.4% 降至 11.3%）、BUMBLE（73.7% 失败来自 VLM 推理）。

## Key Takeaways

1. **Perception 是当前 LCMM 的绝对瓶颈，不是 planning 也不是 control**。HomeRobot、MoManipVLA、BUMBLE 的实验一致表明：GT 感知 → learned 感知的性能跌落远大于 planning 或 policy 的改进带来的提升。这意味着短期内投入更好的 open-vocabulary detection/segmentation（如 Grounding DINO 2、SAM 2）可能比改进 VLA 架构更有效。

2. **Hierarchical architecture（VLM reasoning + VLA execution）正在成为 LCMM 的主流范式**。π0.5、Hi Robot、DM0、UniPlan 都采用了某种形式的 hierarchical decomposition。这源于 LCMM 本身的双重需求——高层语义推理（理解指令、规划步骤）和底层精细控制（灵巧抓取、精确放置）需要不同的计算范式。

3. **从 fixed-base VLA 到 mobile VLA 的迁移并非简单的 action space 扩展**。MoManipVLA 的双层优化、SG-VLA 的 auxiliary spatial grounding、EchoVLA 的 declarative memory 都表明：mobile manipulation 需要 VLA 具备 building-scale spatial understanding，而这不是在 table-top 数据上预训练能自然获得的能力。

4. **Spatial representation 是统一 navigation 和 manipulation 的关键基础设施**。VLMaps、ConceptGraphs、DovSG 证明了显式空间表示对 LCMM 的价值；DovSG 的 6.6x 性能提升（33.3% vs 5.0%）表明动态更新是长期部署的必要条件。但如何将显式空间表示与端到端 VLA 优雅集成仍是 open question。

5. **End-to-end whole-body control 已被验证可行，但 language conditioning 是缺失环节**。Mobile ALOHA 证明了 16D 全身端到端控制的可行性；WholeBodyVLA 用 latent action 从视频学习 humanoid 控制（78% SR）。但这些工作的 language understanding 能力较弱或缺失，与 hierarchical VLM-VLA 方案形成互补。

## Open Problems

1. **统一的 spatial representation**：如何设计一种空间表示同时服务 building-scale navigation（需要 topological/metric map）和 object-level manipulation（需要 6-DoF pose、affordance）？ConceptGraphs 式 3D scene graph 是最有潜力的候选，但其构建和维护成本高、动态更新鲁棒性不足。MTU3D 的 online query spatial memory 提供了轻量替代方案。

2. **Perception-action 闭环**：当前 LCMM 系统的感知和控制基本是单向的（感知 → 决策 → 控制）。如何让机器人在操作过程中 actively 探索和感知（如 MTU3D 的 grounding-exploration 联合决策），而非先感知后行动？

3. **真正的 open-vocabulary mobile manipulation**：当前大多数系统对 "open-vocabulary" 的定义局限于 "open-vocabulary object detection"。但真正的 open-vocabulary 应包括理解复杂空间关系（"把沙发后面的遥控器拿到二楼卧室的床头柜上"）、处理模糊指令（"整理一下客厅"）、以及 personalized 偏好（TidyBot）。

4. **数据获取与 sim-to-real**：Mobile manipulation 的训练数据极度稀缺。Mobile ALOHA 的物理 teleoperation 方案成本低但范围有限；WholeBodyVLA 从无 action 视频学习是创新方向但需结构化人类演示；simulation（HomeRobot/ManiSkill-HAB）提供大规模数据但 sim-to-real gap 显著。π0.5 和 DM0 的 heterogeneous data co-training 是目前最有效的数据策略。

5. **长期部署的鲁棒性**：DovSG 是唯一认真处理环境动态变化的工作，但其 33.3% SR 仍远不够。长期部署需要 continual learning、failure recovery、human-in-the-loop correction 等机制，几乎全部空白。

6. **统一 action space 设计**：Navigation（2-3D velocity）和 manipulation（6-7 DoF EEF / joint）的 action space 差异巨大。EchoVLA 的 per-part diffusion policy、WholeBodyVLA 的 dual latent action、DM0 的 shared backbone + separate head 代表了三种不同的解决思路，但哪种最优尚无定论。

## 调研日志
- **调研日期**: 2026-04-02
- **论文统计**: vault 已有 14 篇 + 新 digest 10 篇（成功 10 / 跳过 0 / 失败 0）
- **未能获取**: 无
- **总共分析**: 24 篇论文

### 已有论文（vault）
[[Papers/2204-SayCan|SayCan]], [[Papers/2210-VLMaps|VLMaps]], [[Papers/2309-ConceptGraphs|ConceptGraphs]], [[Papers/2401-OKRobot|OK-Robot]], [[Papers/2401-MobileALOHA|Mobile ALOHA]], [[Papers/2402-NaVid|NaVid]], [[Papers/2410-Pi0|π₀]], [[Papers/2412-NaVILA|NaVILA]], [[Papers/2412-RoboVLMs|RoboVLMs]], [[Papers/2502-HiRobot|Hi Robot]], [[Papers/2504-Pi05|π0.5]], [[Papers/2507-MTU3D|MTU3D]], [[Papers/2511-PiStar06|π*₀.₆]], [[Papers/2602-DM0|DM0]]

### 新 digest 论文
[[Papers/2305-TidyBot|TidyBot]], [[Papers/2306-HomeRobot|HomeRobot]], [[Papers/2410-BUMBLE|BUMBLE]], [[Papers/2410-DovSG|DovSG]], [[Papers/2503-MoManipVLA|MoManipVLA]], [[Papers/2509-AnywhereVLA|AnywhereVLA]], [[Papers/2511-EchoVLA|EchoVLA]], [[Papers/2512-WholeBodyVLA|WholeBodyVLA]], [[Papers/2602-UniPlan|UniPlan]], [[Papers/2603-SGVLA|SG-VLA]]
