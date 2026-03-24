---
{"dg-publish":true,"permalink":"/ideas/hierarchical-vla-scene-graph/","title":"Hierarchical VLA with Shared Semantic Scene Graph for Unified Navigation-Manipulation","tags":["VLN","VLA","SLAM","scene-graph","flow-matching","hierarchical-planning","mobile-manipulation","gardenEntry"],"dg-note-properties":{"title":"Hierarchical VLA with Shared Semantic Scene Graph for Unified Navigation-Manipulation","tags":["VLN","VLA","SLAM","scene-graph","flow-matching","hierarchical-planning","mobile-manipulation","gardenEntry"],"status":"raw","date_created":"2026-03-24"}}
---


## Core Idea
构建一个三层 hierarchical VLA 架构，以 semantic scene graph 作为 navigation 和 manipulation 的 shared spatial representation，实现 building-scale 导航与 dexterous manipulation 的统一。

## Motivation
从 [[Topics/VLN-VLA-Unification\|VLN-VLA-Unification]] survey 的 gap 分析中发现：（1）现有系统的 navigation 和 manipulation 使用完全不同的空间表示（如 OK-Robot 的 2D occupancy grid vs. 3D point cloud），没有 shared representation；（2）没有 end-to-end model 能同时处理 building-scale navigation 和 dexterous manipulation；（3）SLAM representations 未针对 VLM consumption 优化。本 idea 的核心假设是：**shared semantic spatial representation 能显著提升 Nav+Manip 的协调性和任务成功率**。每个组件都有成熟的技术基础（VLM backbone、ConceptGraphs、flow matching），且 HomeRobot OVMM 提供了直接可用的评估平台，使验证路径清晰可行。

## Related Work
- [[Papers/Black2024-Pi0\|Black2024-Pi0]] — Flow matching action generation，manipulation head 的技术基础
- [[Papers/Black2025-Pi05\|Black2025-Pi05]] — VLM + hierarchical planning for long-horizon tasks，验证了 hierarchical 架构的可行性
- [[Papers/Cheng2024-NaVILA\|Cheng2024-NaVILA]] — VLM-driven navigation with language actions，high-level planner 的参考
- [[Papers/Gu2024-ConceptGraphs\|Gu2024-ConceptGraphs]] — Open-vocabulary 3D scene graph，shared representation 的核心技术
- [[Papers/Liu2024-OKRobot\|Liu2024-OKRobot]] — Modular Nav+Manip baseline，使用 separate representations（对比基线）
- [[Papers/Torne2026-MEM\|Torne2026-MEM]] — 多尺度记忆机制（视频短期 + 语言长期），memory 设计的参考
- [[Papers/An2024-ETPNav\|An2024-ETPNav]] — Hierarchical navigation with explicit topological planning
- [[Papers/Huang2023-VLMaps\|Huang2023-VLMaps]] — Language-indexed spatial features for navigation

## Rough Plan

### 三层架构设计

1. **High-level VLM Planner**（基于 fine-tuned PaliGemma 或 VILA）
   - 输入：语言指令 + scene graph 的文本化 summary
   - 输出：sub-goal sequence（如 "navigate to kitchen → locate mug → pick up mug → navigate to sink → place mug"）
   - 关键：设计高效的 graph-to-text serialization 方案，控制 context window 占用

2. **Mid-level Scene Graph Memory**（基于 ConceptGraphs 简化版）
   - Online incremental 构建，每个 node 包含：CLIP embedding + 3D position + navigability flag + graspability flag
   - 同时服务 navigation（nodes 作为 waypoints）和 manipulation（nodes 作为 grasp targets）
   - 支持 language query：VLM planner 可以通过自然语言查询 graph

3. **Low-level Dual Action Heads**
   - Navigation head：在 scene graph 上做 waypoint selection → local planner 执行 continuous locomotion
   - Manipulation head：flow matching policy（à la π₀）生成 continuous joint-level control

### 实验计划

- **平台**：HomeRobot OVMM（simulation → real Hello Robot Stretch）
- **关键对比实验**：shared scene graph vs. separate representations（OK-Robot 式）的 Nav+Manip 成功率
- **渐进路径**：先在 Habitat simulation 验证架构 → 再 transfer 到 real robot
- **Metrics**：task success rate、navigation efficiency、manipulation success rate、re-planning frequency

## Open Questions
1. **Scene graph scalability**：building-scale 环境可能产生数千 nodes，如何高效 serialize 并输入 VLM 的有限 context window？需要 graph summarization 或 attention-based selection。
2. **Online construction 效率**：ConceptGraphs 需要离线构建，如何实现 real-time incremental update？可能需要简化 graph 结构或引入 lazy evaluation。
3. **Co-training 策略**：navigation head 主要依赖 sim data（Habitat），manipulation head 需要 real data（OXE）。Sim-real mixed training 的 domain gap 如何处理？
4. **Graph-to-text serialization 格式**：哪种 serialization 方案对 VLM reasoning 最友好？JSON？natural language description？structured template？需要 ablation study。
5. **Failure recovery**：当 scene graph 中的信息过时（物体被移动）或错误（misdetection）时，如何触发 re-observation 和 graph update？
