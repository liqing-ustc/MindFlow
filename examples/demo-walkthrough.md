# MindFlow Demo Walkthrough

> 这个文档演示如何使用 MindFlow Phase 1 的 3 个核心 skill 完成一个完整的研究循环。

## 前提条件

1. 一个 coding agent（Claude Code / Codex / Cursor 等）
2. MindFlow skills 已复制到 agent 的 skills 目录（如 `~/.claude/skills/`）
3. 当前工作目录是你的 Obsidian vault

## Step 1: 消化论文 (paper-digest)

假设你想了解 EvoScientist 这篇论文：

```
/paper-digest "https://arxiv.org/abs/2603.08127"
```

AI 会：
1. 抓取论文内容
2. 生成 `Papers/2603-EvoScientist.md`，包含完整笔记
3. 自动关联 vault 中已有的相关论文
4. 记录到 `Workbench/logs/` 今日日志

打开 Obsidian 查看 Papers/2603-EvoScientist.md，确认笔记质量，填写 rating。

## Step 2: 重复几次

用同样方法消化几篇相关论文：

```
/paper-digest "The AI Scientist Sakana AI"
/paper-digest "https://github.com/karpathy/autoresearch"
```

## Step 3: 跨论文分析 (cross-paper-analysis)

现在有了多篇论文笔记，做对比分析：

```
/cross-paper-analysis --tags AutoResearch --focus "memory and evolution mechanisms"
```

AI 会：
1. 读取所有 AutoResearch 标签的论文
2. 构建对比表
3. 识别共识、矛盾、知识空白
4. 生成 `Topics/AutoResearch-Memory-Evolution-Analysis.md`
5. 如果发现 pattern → 写入 `Workbench/memory/patterns.md`

## Step 4: 蒸馏记忆 (memory-distill)

经过几天的论文阅读和分析后：

```
/memory-distill
```

AI 会：
1. 扫描最近 7 天的 `Workbench/logs/`
2. 提取重复出现的 pattern
3. 够格的 pattern 晋升为 provisional insight
4. 有足够证据的 insight 标记为 validated
5. 建议将高置信度 insight 添加到 `Domain-Map/{Name}.md`

## 查看 AI 状态

随时可以在 Obsidian 中查看：
- `Workbench/agenda.md` — AI 的研究议程
- `Workbench/memory/` — AI 积累的经验
- `Workbench/queue.md` — 待办队列
- `Workbench/logs/` — 每日工作日志
- `Domain-Map/` — 你和 AI 的共同认知地图（按 domain 拆分）

所有文件都是 Markdown，你可以直接阅读和编辑。
