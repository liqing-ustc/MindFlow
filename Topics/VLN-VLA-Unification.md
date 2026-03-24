---
title: "VLN-VLA Unification: Foundation Models for Indoor Robot Navigation and Manipulation"
tags: [VLN, VLA, SLAM, embodied-AI, foundation-model, indoor-scene, navigation, manipulation]
status: draft
date_updated: "2026-03-24"
---

## Overview
本 Topic 从 foundation model 视角，梳理 VLN（Vision-and-Language Navigation）和 VLA（Vision-Language-Action）两个领域的交汇与趋同。核心问题：VLN 和 VLA 在架构上正在趋同（都使用 VLM backbone + action prediction），能否统一？SLAM-based 空间表示在其中扮演什么角色？

## 1. VLA 基础模型现状

Vision-Language-Action（VLA）模型是 embodied AI 领域近年来最重要的进展之一。其核心思路是将预训练 VLM 的视觉-语言理解能力迁移到 robot action 生成，形成"看懂场景 → 理解指令 → 输出动作"的端到端 pipeline。自 2023 年 [[Brohan2023-RT2|RT-2]] 开创 VLA 范式以来，该领域经历了三个关键演进：（1）**action representation 从 discrete token 到 continuous flow matching**——RT-2 和 [[Kim2024-OpenVLA|OpenVLA]] 将 action 离散化为 text token，控制频率受限于 autoregressive decoding（~3 Hz）；[[Black2024-Pi0|π₀]] 引入 flow matching + action expert 实现 50 Hz 连续控制；（2）**从单任务到 cross-embodiment generalist**——[[Ghosh2024-Octo|Octo]] 和 OpenVLA 在 Open X-Embodiment 数据集上训练，覆盖多种 robot 平台；π₀ 进一步扩展到 7 个平台 68 个任务；（3）**从短时操作到 long-horizon 自主系统**——[[Black2025-Pi05|π0.5]] 加入 hierarchical inference 实现 15 分钟级家务任务，[[Torne2026-MEM|MEM]] 引入多尺度记忆机制，[[Li2026-RoboClaw|RoboClaw]] 用 VLM agent loop 统一数据收集和执行。

### Key VLA Models

| Model | Year | VLM Backbone | Action Space | Training | Key Innovation |
|-------|------|-------------|-------------|----------|---------------|
| [[Brohan2023-RT2\|RT-2]] | 2023 | PaLM-E 12B / PaLI-X 55B | Discrete tokens (7-DoF, 256 bins) | Co-fine-tuning (web + robot) | VLM → action tokens 范式开创 |
| [[Ghosh2024-Octo\|Octo]] | 2024 | Transformer (27M/93M, 无 VLM) | Continuous (diffusion, action chunk) | 800k trajectories, OXE | 轻量开源 generalist + diffusion head |
| [[Kim2024-OpenVLA\|OpenVLA]] | 2024 | Llama 2 7B + DINOv2/SigLIP | Discrete tokens (7-DoF) | 970k demonstrations, OXE | 开源 VLA baseline，超越 RT-2-X |
| [[Black2024-Pi0\|π₀]] | 2024 | PaliGemma 3B + Action Expert 300M | Continuous (flow matching, 50 Hz) | 10K+ hrs, 7 platforms, 68 tasks | Flow matching + MoE-style action expert |
| [[Black2025-Pi05\|π0.5]] | 2025 | PaliGemma 3B (extended) | Hybrid (discrete pre-train → continuous post-train) | Co-training 5 类异构数据 | Hierarchical inference + open-world generalization |
| [[Torne2026-MEM\|MEM]] | 2026 | Gemma3-4B (π0.6 base) | Continuous (flow matching) | Robot demos + video + web | 多尺度记忆（视频短期 + 语言长期） |
| [[Li2026-RoboClaw\|RoboClaw]] | 2026 | Off-the-shelf VLM + π0.5 | Continuous (flow matching) | 自主采集 + 迭代学习 | EAP 自主数据收集 + VLM agent loop |

### 架构趋势 Takeaway

1. **Action representation 是核心分野**：discrete token（RT-2, OpenVLA）→ diffusion（Octo）→ flow matching（π₀ 系列）。连续 action 生成显著提升了控制频率和灵巧操作能力。
2. **VLM backbone 不是越大越好**：RT-2 用 55B 参数，但 π₀ 用 3B + 300M action expert 就实现了更强的操作能力。关键在于 action head 的设计和训练数据的多样性。
3. **Hierarchical 架构成为主流**：π0.5 和 MEM 都采用高层语义推理 + 低层 action 生成的分层设计，这与 VLN 领域的 high-level planning + low-level control 高度相似，暗示了 VLN-VLA 统一的可能性。
4. **开源生态推动快速迭代**：Octo 和 OpenVLA 的开源使社区能够快速复现和改进，Open X-Embodiment 数据集成为事实标准。

## 2. VLN 基础模型现状
<!-- Survey of VLN models leveraging foundation models -->

## 3. 语义 SLAM 与空间表示
<!-- Semantic SLAM and spatial representations for VLMs -->

## 4. 架构趋同分析
<!-- Cross-cutting comparison of VLN and VLA architectures -->

## 5. 现有 Nav+Manip 系统
<!-- Systems combining navigation and manipulation -->

## 6. Gap 分析与潜在方向
<!-- Research gaps, benchmarks, and future directions -->
