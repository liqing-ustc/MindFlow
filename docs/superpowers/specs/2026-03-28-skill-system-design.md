# MindFlow Skill System Design

> **Date**: 2026-03-28
> **Status**: Approved
> **Scope**: Phase 2-5 全量 skill 设计 + 现有 skill/protocol 改造

---

## 1. Design Context

### 输入
- **AutoResearch 生态 Skill 设计分析**（`Topics/AutoResearch-SkillDesign.md`）：9 个开源项目的 skill 设计横向对比，提炼 5 大 pattern
- **MindFlow 现状**：4 个已有 skill（Phase 1），skill-protocol / memory-protocol / agenda-protocol 已定义

### 设计约束
- **架构路线**：方法论层为主（ARIS 模式），借鉴自进化机制（EvoScientist / AutoResearchClaw），B 层（ML 工程 skill）预留接口但暂不设计
- **轻量原则**：避免过度复杂，保持 Layer 1 零依赖（纯 Markdown + LLM）
- **融入的 Pattern**：pushy description、Verify 节、attempt budget、渐进式披露、Dual Memory 分离意识
- **不融入的 Pattern**：跨模型对抗评审（当前单 agent）、NPM 分发（个人知识库）

### 架构选型
**核心循环 + 卫星 skill**（方案 B）——中心是 `autoresearch`（L2 编排），根据 agenda 和 memory 的当前状态判断下一步行动，调用对应的卫星 skill。每个卫星 skill 独立可用，Supervisor 可直接触发。

---

## 2. Skill Protocol 改造

对 `references/skill-protocol.md` 新增 3 个轻量约定。

### 2.1 Pushy Description 原则

在 Frontmatter Specification 的 `description` 字段说明中新增：

> Description 应积极触发（"pushy"）——明确描述触发场景，降低 under-triggering 风险。不要只写"做什么"，要写"什么情况下该用我"。

示例：

| Before | After |
|--------|-------|
| `消化一篇论文，生成结构化笔记到 Papers/` | `当 Supervisor 给出论文 URL/标题/PDF/DOI，或阅读队列中有待处理论文时，消化论文并生成结构化笔记到 Papers/` |

### 2.2 新增可选 `## Verify` 节

在 Body Sections 表中新增：

| Section | Required | Purpose |
|---------|----------|---------|
| `## Verify` | Recommended | 执行完成后的质量自检清单，机械式检查产出是否达标 |

**Verify vs Guard**：
- **Guard** = 执行过程中的硬约束（"不准做什么"）——事前/事中
- **Verify** = 执行完成后的质量检查（"产出合格吗？"）——事后

格式：checklist，每条是可机械验证的断言。

```markdown
## Verify

- [ ] 输出文件存在且非空
- [ ] frontmatter 所有 required 字段已填写
- [ ] 正文无 `[TODO]` 或 `[TBD]` 占位符
- [ ] 所有论文引用使用 `[[wikilink]]` 格式
```

### 2.3 新增可选 `budget` Frontmatter 字段

防止 skill 无限循环（借鉴 EvoScientist 的 attempt 预算）：

```yaml
budget:
  max_web_calls: 10       # WebSearch + WebFetch 总调用上限
  timeout_hint: "30min"   # 建议超时（非强制，供 agent 参考）
```

类型为 `object`，可选字段，仅对重资源 skill 有意义。简单 skill 不需要填。

---

## 3. 现有 Skill 改造清单

不重写，只列出每个 skill 需要改的具体点。

### 3.1 paper-digest

| 改动 | 内容 |
|------|------|
| `description` | → `当 Supervisor 给出论文 URL/标题/PDF/DOI，或阅读队列中有待处理论文时，消化论文并生成结构化笔记到 Papers/` |
| 新增 `## Verify` | `[ ] Papers/YYMM-*.md 已创建且 >200 字` / `[ ] frontmatter title/authors/date_publish 非空` / `[ ] Summary 非空且 <3 句` / `[ ] 日志已追加` |
| `budget` | `max_web_calls: 5` |

### 3.2 cross-paper-analysis

| 改动 | 内容 |
|------|------|
| `description` | → `当需要对比多篇论文的方法/结论/实验设置，或 Supervisor 说"对比""分析这几篇"时，执行跨论文对比并识别共识、矛盾和知识空白` |
| 新增 `## Verify` | `[ ] Topics/*-Analysis.md 已创建` / `[ ] 对比表包含所有输入论文` / `[ ] 共识/矛盾/空白三节均非空` / `[ ] 所有引用为 [[wikilink]]` |

### 3.3 literature-survey

| 改动 | 内容 |
|------|------|
| `description` | → `当 Supervisor 说"调研""survey""了解研究现状"，或需要系统了解某主题的文献全貌时，搜索外部文献、批量 digest、综合生成调研报告` |
| 新增 `## Verify` | `[ ] Topics/*-Survey.md 已创建` / `[ ] 技术路线 ≥2 条` / `[ ] 对比表论文数 ≥3` / `[ ] Open Problems 非空` |
| `budget` | 已有 Guard 中 `max 10 次 WebSearch`，移到 budget 字段：`max_web_calls: 10` |

### 3.4 memory-distill

| 改动 | 内容 |
|------|------|
| `description` | → `当积累了多天工作日志、或 Supervisor 说"整理记忆""蒸馏"时，从日志中提取 pattern 和 insight 到记忆库。也可被 autoresearch 在合适时机自动调用` |
| 新增 `## Verify` | `[ ] changelog.md 已追加本次蒸馏记录` / `[ ] 新增 pattern 数 + 晋升 insight 数 ≥ 0（允许无发现，但须记录）` |

---

## 4. Skill 全景图

### 4.1 分类体系

| 编号 | Category | 定位 | Skill 数量 |
|------|----------|------|-----------|
| `1-literature` | 文献技能 | 读、搜、比 | 3（已有） |
| `2-ideation` | 创意技能 | 想、评 | 2（新增） |
| `3-experiment` | 实验技能 | 设计、追踪、分析 | 3（新增） |
| `4-writing` | 写作技能 | 草稿、打磨 | 2（新增） |
| `5-evolution` | 进化技能 | 记忆、议程、检索 | 3（1 已有 + 2 新增） |
| `6-orchestration` | 编排技能 | 核心循环 | 1（新增） |

**总计**：14 个 skill（4 已有 + 10 新增）

### 4.2 完整目录结构

```
skills/
├── 1-literature/
│   ├── paper-digest/           ✅ L0  — 消化单篇论文
│   ├── cross-paper-analysis/   ✅ L0  — 跨论文对比
│   └── literature-survey/      ✅ L1  — 主题级调研
│
├── 2-ideation/
│   ├── idea-generate/          🆕 L0  — 从知识空白生成研究 idea
│   └── idea-evaluate/          🆕 L0  — 评估 idea 可行性和新颖性
│
├── 3-experiment/
│   ├── experiment-design/      🆕 L0  — 设计实验方案
│   ├── experiment-track/       🆕 L0  — 记录实验进展和结果
│   └── result-analysis/        🆕 L0  — 分析实验结果，提取 insight
│
├── 4-writing/
│   ├── draft-section/          🆕 L0  — 起草论文/报告章节
│   └── writing-refine/         🆕 L0  — 打磨已有文稿
│
├── 5-evolution/
│   ├── memory-distill/         ✅ L2  — 从日志蒸馏记忆
│   ├── agenda-evolve/          🆕 L2  — 演化研究议程
│   └── memory-retrieve/        🆕 L0  — 从记忆库检索相关经验
│
└── 6-orchestration/
    └── autoresearch/           🆕 L2  — 核心研究循环
```

### 4.3 架构关系图

```
                    Supervisor（随时 drop in）
                         │
                         ▼
               ┌─── autoresearch (L2) ───┐
               │   读 agenda + memory     │
               │   + queue → 判断行动     │
               └────┬──┬──┬──┬──┬────────┘
                    │  │  │  │  │
        ┌───────────┘  │  │  │  └───────────┐
        ▼              ▼  ▼  ▼              ▼
   1-literature   2-ideation  3-experiment  4-writing
        │              │         │
        └──────┬───────┘         │
               ▼                 ▼
          5-evolution（memory-distill / agenda-evolve）
               │
               └──► 更新 Workbench/ 状态 ──► 下一轮 autoresearch
```

**关键设计决策**：
- autoresearch 是唯一的编排 skill，不硬编码调用顺序，每轮由 LLM 判断
- 每个卫星 skill 可被 autoresearch 调用，也可被 Supervisor 自然语言直接触发
- memory-retrieve 是被其他 skill 内部调用的工具性 skill，不独立触发

---

## 5. 新增 Skill 详细设计

### 5.1 idea-generate（L0）

**目录**：`skills/2-ideation/idea-generate/SKILL.md`

**Frontmatter**：
```yaml
name: idea-generate
description: >
  当 cross-paper-analysis 发现知识空白、memory 中有 validated insight 待探索、
  或 Supervisor 说"想个 idea""有什么研究机会"时，
  从知识空白和已有洞察中生成可证伪的研究 idea
version: 1.0.0
intent: ideation
capabilities: [research-planning, cross-validation]
domain: general
roles: [autopilot, copilot]
autonomy: medium
allowed-tools: [Read, Write, Edit, Glob, Grep]
input:
  - name: source
    description: "触发来源：Topics/*-Analysis.md 中的知识空白、insights.md 中的 validated insight、Supervisor 直接给的方向、或 agenda direction 的 next_action"
  - name: constraints
    description: "（可选）约束条件，如 '不需要 GPU'、'偏理论'"
output:
  - file: "Ideas/*.md"
  - memory: "Workbench/logs/YYYY-MM-DD.md"
related-skills: [cross-paper-analysis, idea-evaluate, memory-retrieve]
```

**Steps**：
1. 读取来源材料（知识空白 / insight / Supervisor 指令）
2. 调用 memory-retrieve（scope: `failed-directions`）——避免重蹈覆辙
3. 读取 `Domain-Map/` 相关 domain——理解当前知识边界
4. 生成 2-3 个候选 idea，每个包含：hypothesis（可证伪）、motivation、approach sketch、expected outcome、risk
5. 按 `Templates/Idea.md` 格式写入 `Ideas/`，status 设为 `raw`
6. 追加日志

**Verify**：
- `[ ]` Ideas/*.md 已创建
- `[ ]` hypothesis 字段是可证伪的一句话断言
- `[ ]` 未与 `failed-directions.md` 中的已废弃方向重复

**Guard**：
- 不修改任何已有 Idea 文件
- 不捏造文献支持（引用必须指向 vault 中已有的 Paper 笔记）
- 不直接修改 agenda.md（只提议，由 agenda-evolve 或 Supervisor 决策）

---

### 5.2 idea-evaluate（L0）

**目录**：`skills/2-ideation/idea-evaluate/SKILL.md`

**Frontmatter**：
```yaml
name: idea-evaluate
description: >
  当 Supervisor 说"评估一下这个 idea""这个可行吗"，
  或 autoresearch 需要筛选 idea 优先级时，
  从 novelty/feasibility/impact/risk/evidence 五维评估研究 idea
version: 1.0.0
intent: ideation
capabilities: [research-planning, cross-validation]
domain: general
roles: [autopilot, copilot, sparring]
autonomy: medium
allowed-tools: [Read, Edit, Glob, Grep]
input:
  - name: idea
    description: "[[Ideas/xxx.md]] 引用"
  - name: criteria
    description: "（可选）额外评估标准"
output:
  - memory: "Workbench/logs/YYYY-MM-DD.md"
related-skills: [idea-generate, experiment-design, memory-retrieve]
```

**Steps**：
1. 读取目标 Idea 笔记
2. 读取相关 Paper 笔记（从 Idea 的 related_papers 字段获取）
3. 读取 `Domain-Map/` 相关 domain 的 Active Debates 和 Open Questions
4. 从 5 个维度评估：
   - **Novelty**：与已有工作的差异化程度
   - **Feasibility**：当前资源条件下能否执行
   - **Impact**：若成功，对领域的贡献
   - **Risk**：主要失败模式
   - **Evidence**：当前支撑假设的证据强度
5. 生成评估结论（recommend / revise / shelve），附具体建议
6. 用 Edit 更新目标 Idea 的 status（raw → developing 或 raw → archived）和追加评估记录
7. 追加日志

**Verify**：
- `[ ]` Idea 文件已更新评估记录
- `[ ]` 5 个维度均有评分和简要说明
- `[ ]` 结论为 recommend / revise / shelve 之一

**Guard**：
- 不修改 Idea 的 hypothesis 字段（那是 idea-generate 的职责）
- 评估必须基于 vault 中可追溯的证据，不凭空判断

---

### 5.3 experiment-design（L0）

**目录**：`skills/3-experiment/experiment-design/SKILL.md`

**Frontmatter**：
```yaml
name: experiment-design
description: >
  当 Supervisor 说"设计个实验""怎么验证这个 idea"，
  或 autoresearch 判断某个 developing/validated idea 需要实验验证时，
  为 idea 设计完整实验方案
version: 1.0.0
intent: experiment
capabilities: [research-planning]
domain: general
roles: [autopilot, copilot]
autonomy: medium
allowed-tools: [Read, Write, Edit, Glob, Grep]
input:
  - name: idea
    description: "[[Ideas/xxx.md]] 引用（status 为 developing 或 validated）"
  - name: constraints
    description: "（可选）资源约束，如 '单卡 A100'、'纯理论推导'"
output:
  - file: "Experiments/*.md"
  - memory: "Workbench/logs/YYYY-MM-DD.md"
related-skills: [idea-evaluate, experiment-track, memory-retrieve]
```

**Steps**：
1. 读取目标 Idea 笔记的 hypothesis 和 approach sketch
2. 调用 memory-retrieve（scope: `effective-methods` + `failed-directions`）获取相关经验
3. 设计实验方案：
   - **Variables**：自变量、因变量、控制变量
   - **Baseline**：对比基线
   - **Metrics**：衡量指标（尽量可量化）
   - **Steps**：具体实验步骤
   - **Expected outcome**：假设成立/不成立分别预期什么结果
   - **Risk & Mitigation**：可能的失败点和备选方案
4. 按 `Templates/Experiment.md` 格式写入 `Experiments/`，status 设为 `planning`
5. 在目标 Idea 笔记中追加 `[[Experiments/xxx]]` 链接
6. 追加日志

**Verify**：
- `[ ]` Experiments/*.md 已创建
- `[ ]` Variables / Baseline / Metrics 三节均非空
- `[ ]` 有明确的 expected outcome（假设成立 vs 不成立两种情况）

**Guard**：
- Metrics 必须可量化或可明确判定（不接受主观指标）
- 不修改源 Idea 的 hypothesis

---

### 5.4 experiment-track（L0）

**目录**：`skills/3-experiment/experiment-track/SKILL.md`

**Frontmatter**：
```yaml
name: experiment-track
description: >
  当 Supervisor 说"记录一下实验结果""实验跑完了"，
  或 Researcher 完成一轮实验需要记录时，
  在 Experiment 笔记中追加 Run Entry 并更新状态
version: 1.0.0
intent: experiment
capabilities: [data-processing]
domain: general
roles: [autopilot]
autonomy: high
allowed-tools: [Read, Edit, Glob]
input:
  - name: experiment
    description: "[[Experiments/xxx.md]] 引用"
  - name: result
    description: "实验结果（自由文本、数字、或指向结果文件的路径）"
output:
  - memory: "Workbench/logs/YYYY-MM-DD.md"
related-skills: [experiment-design, result-analysis]
```

**Steps**：
1. 读取目标 Experiment 笔记
2. 在笔记中追加一条 Run Entry：
   ```markdown
   ### Run [N] — YYYY-MM-DD
   - **config**: <本轮具体配置/参数>
   - **result**: <结果数据>
   - **observation**: <一句话发现>
   - **next**: <下一步——继续/调整/停止>
   ```
3. 更新 Experiment 的 status（planning → running / 保持 running）
4. 若 `next` 为"停止"，更新 status 为 `completed` 或 `failed`
5. 追加日志

**Verify**：
- `[ ]` Experiment 文件已追加 Run Entry
- `[ ]` Run Entry 的 result 字段非空

**Guard**：
- 不修改已有 Run Entry（append-only）
- 不修改 Experiment 的 Variables / Baseline / Metrics 设计

---

### 5.5 result-analysis（L0）

**目录**：`skills/3-experiment/result-analysis/SKILL.md`

**Frontmatter**：
```yaml
name: result-analysis
description: >
  当 Supervisor 说"分析一下实验结果"，
  或实验 status 变为 completed 后 autoresearch 自动调用，
  分析实验数据并判断假设是否成立
version: 1.0.0
intent: analysis
capabilities: [cross-validation, research-planning]
domain: general
roles: [autopilot, copilot]
autonomy: medium
allowed-tools: [Read, Edit, Glob, Grep]
input:
  - name: experiment
    description: "[[Experiments/xxx.md]] 引用（status 为 running 或 completed）"
output:
  - memory: "Workbench/memory/patterns.md"
  - memory: "Workbench/logs/YYYY-MM-DD.md"
related-skills: [experiment-track, memory-retrieve, agenda-evolve]
```

**Steps**：
1. 读取目标 Experiment 笔记的全部 Run Entries
2. 读取关联 Idea 的 hypothesis
3. 调用 memory-retrieve（scope: `insights` + `patterns`）获取相关上下文
4. 分析：
   - **Hypothesis verdict**：supported / refuted / inconclusive，附证据
   - **Key findings**：主要发现
   - **Comparison to baseline**：与基线的对比
   - **Limitations**：本实验的局限性
   - **Implications**：对当前研究方向的影响
5. 将分析结果写入 Experiment 笔记的 `## Analysis` 节
6. 将发现写入 `Workbench/memory/patterns.md`（如有 cross-experiment pattern）
7. 若 hypothesis 被明确支持或反驳，更新关联 Idea 的 status
8. 追加日志

**Verify**：
- `[ ]` Experiment 笔记有 `## Analysis` 节
- `[ ]` Hypothesis verdict 为 supported / refuted / inconclusive 之一
- `[ ]` 关联 Idea 的 status 已同步更新（若有明确结论）

**Guard**：
- Hypothesis verdict 必须基于 Run Entries 中的实际数据
- 若结果为 inconclusive，不强行下结论
- 不修改 Run Entries（只追加 Analysis 节）

---

### 5.6 draft-section（L0）

**目录**：`skills/4-writing/draft-section/SKILL.md`

**Frontmatter**：
```yaml
name: draft-section
description: >
  当 Supervisor 说"写一下 introduction""起草 related work"，
  或 autoresearch 判断某 direction 已积累足够素材需要成文时，
  起草论文或报告的指定章节
version: 1.0.0
intent: writing
capabilities: [prompt-structured-output]
domain: general
roles: [autopilot, copilot]
autonomy: medium
allowed-tools: [Read, Write, Edit, Glob, Grep]
input:
  - name: target
    description: "目标文件路径（Reports/xxx.md 或已有草稿文件）"
  - name: section
    description: "要起草的章节名（如 Introduction、Related Work、Method）"
  - name: sources
    description: "素材引用列表——[[Papers/...]]、[[Experiments/...]]、[[Ideas/...]]、[[Topics/...]]"
output:
  - memory: "Workbench/logs/YYYY-MM-DD.md"
related-skills: [writing-refine, cross-paper-analysis]
```

**Steps**：
1. 读取所有 sources 笔记的相关内容
2. 若 target 文件已存在，读取已有内容了解上下文和风格
3. 读取 `Domain-Map/` 相关 domain 了解领域背景
4. 起草指定章节：学术写作规范、`[[wikilink]]` 引用、中文正文 + 英文术语
5. 若 target 不存在用 Write 创建；若已存在用 Edit 插入指定 section
6. 追加日志

**Verify**：
- `[ ]` 目标文件中指定 section 已写入且 >200 字
- `[ ]` 所有事实性陈述有 `[[wikilink]]` 来源
- `[ ]` 无 `[TODO]`、`[TBD]` 占位符

**Guard**：
- 不修改目标文件中的其他章节
- 不捏造引用
- copilot 模式下先输出草稿预览，确认后再写入

---

### 5.7 writing-refine（L0）

**目录**：`skills/4-writing/writing-refine/SKILL.md`

**Frontmatter**：
```yaml
name: writing-refine
description: >
  当 Supervisor 说"打磨一下""改改这段""逻辑不通顺"，
  或 autoresearch 在写作阶段自检时，
  从结构/清晰度/论据三个维度打磨已有文稿
version: 1.0.0
intent: writing
capabilities: [prompt-structured-output]
domain: general
roles: [copilot]
autonomy: low
allowed-tools: [Read, Edit, Glob, Grep]
input:
  - name: target
    description: "目标文件路径"
  - name: section
    description: "（可选）指定章节，不指定则全文"
  - name: focus
    description: "（可选）打磨重点——structure / clarity / evidence / all"
output:
  - memory: "Workbench/logs/YYYY-MM-DD.md"
related-skills: [draft-section]
```

**Steps**：
1. 读取目标文件（或指定 section）
2. 根据 focus 维度审视：
   - **structure**：段落间逻辑链、过渡
   - **clarity**：冗余、歧义、过度抽象
   - **evidence**：每个核心 claim 是否有来源支撑
3. 生成修改建议列表，每条标注位置和原因
4. copilot 模式（默认）：输出建议供 Supervisor 确认后执行
5. 追加日志

**Verify**：
- `[ ]` 修改后无新引入的 `[TODO]` 占位符
- `[ ]` `[[wikilink]]` 引用仍有效

**Guard**：
- 默认 copilot（autonomy: low）
- 不改变核心论点或结论
- 不增删章节

---

### 5.8 agenda-evolve（L2）

**目录**：`skills/5-evolution/agenda-evolve/SKILL.md`

**Frontmatter**：
```yaml
name: agenda-evolve
description: >
  当积累了新的 validated insight、实验结果改变了方向判断、
  或 Supervisor 说"更新研究方向""复盘 agenda"时，
  根据记忆和发现演化研究议程
version: 1.0.0
intent: evolution
capabilities: [research-planning, cross-validation]
domain: general
roles: [autopilot, copilot]
autonomy: high
allowed-tools: [Read, Edit, Glob, Grep]
input:
  - name: trigger
    description: "（可选）触发原因——new insights / experiment results / supervisor redirect"
output:
  - memory: "Workbench/evolution/changelog.md"
  - memory: "Workbench/logs/YYYY-MM-DD.md"
related-skills: [memory-distill, autoresearch, result-analysis]
```

**Steps**：
1. 读取 `Workbench/agenda.md` 当前状态
2. 读取 `Workbench/memory/insights.md`（重点关注近期 validated insights）
3. 读取 `Workbench/memory/failed-directions.md`
4. 读取 `Workbench/queue.md` 的 Questions 和 Review 部分
5. 读取近期 `Ideas/` 中 status 为 developing 或 validated 的 idea
6. 判断 agenda 需要哪些变更：
   - 新增 direction（从 validated idea 或 validated insight 衍生）
   - 更新 direction 的 status / confidence / evidence / next_action
   - 暂停无进展的 direction
   - 废弃被证伪的 direction（同步写 failed-directions.md）
7. 用 Edit 更新 `Workbench/agenda.md`
8. 追加 `Workbench/evolution/changelog.md`
9. 追加日志

**Verify**：
- `[ ]` agenda.md 的 last_updated 已更新
- `[ ]` 每个 Active Direction 都有非空 next_action
- `[ ]` 新增/变更有 changelog 记录

**Guard**：
- 遵循 agenda-protocol.md 的所有规则
- 不删除 Supervisor 手动添加的 direction（只可暂停并注明原因）
- 每次变更记录推理过程到 changelog

---

### 5.9 memory-retrieve（L0）

**目录**：`skills/5-evolution/memory-retrieve/SKILL.md`

**Frontmatter**：
```yaml
name: memory-retrieve
description: >
  被其他 skill 内部调用，从 Workbench/memory/ 中检索与当前任务相关的历史经验。
  当 idea-generate 需要查失败方向、experiment-design 需要查有效方法、
  或任何 skill 需要历史上下文时调用
version: 1.0.0
intent: utility
capabilities: [search-retrieval]
domain: general
roles: [autopilot]
autonomy: high
allowed-tools: [Read, Glob, Grep]
input:
  - name: query
    description: "自然语言检索问题"
  - name: scope
    description: "检索范围——patterns / insights / effective-methods / failed-directions / all"
output: []
related-skills: [memory-distill]
```

**Steps**：
1. 根据 scope 确定目标文件
2. 读取目标记忆文件
3. 逐条匹配 query 的语义相关性（LLM 判断，非向量检索——保持 Layer 1 零依赖）
4. 返回 top-k 相关条目（默认 k=5），每条包含原文 + 来源引用

**设计说明**：Layer 1 轻量实现——纯 Markdown 读取 + LLM 语义匹配。未来 Layer 2 可用向量检索替换，接口不变。

**Guard**：
- 只读，不修改任何记忆文件
- 返回结果必须包含原文引用（wikilink）

---

### 5.10 autoresearch（L2）

**目录**：`skills/6-orchestration/autoresearch/SKILL.md`

**Frontmatter**：
```yaml
name: autoresearch
description: >
  MindFlow 的核心研究循环。当 Supervisor 说"自己干活吧""开始研究"，
  或系统需要自主推进研究时启动。
  持续运行：读取当前状态 → 判断最高价值行动 → 调用卫星 skill → 记录 → 循环
version: 1.0.0
intent: orchestration
capabilities: [agent-workflow, research-planning]
domain: general
roles: [autopilot]
autonomy: high
allowed-tools: [Read, Write, Edit, Glob, Grep, WebSearch, WebFetch]
input:
  - name: focus
    description: "（可选）聚焦某个 agenda direction"
output:
  - memory: "Workbench/logs/YYYY-MM-DD.md"
related-skills: [paper-digest, cross-paper-analysis, literature-survey, idea-generate, idea-evaluate, experiment-design, experiment-track, result-analysis, draft-section, writing-refine, memory-distill, agenda-evolve, memory-retrieve]
```

**Steps**（每轮）：

**1. READ STATE**
- `Workbench/agenda.md` → 当前方向和优先级
- `Workbench/queue.md` → 待处理任务
- `Workbench/memory/` → 近期记忆
- 最近 3 天 `Workbench/logs/` → 近期活动

**2. JUDGE**

基于当前状态，由 LLM 判断（非硬编码）下一个最高价值行动：

| 状态信号 | 可能的行动 |
|---------|-----------|
| queue 中有待处理论文 | → paper-digest |
| agenda direction 缺文献支撑 | → literature-survey |
| cross-paper-analysis 发现知识空白 | → idea-generate |
| 有 raw idea 待评估 | → idea-evaluate |
| 有 developing idea 缺实验方案 | → experiment-design |
| 有 completed experiment 未分析 | → result-analysis |
| 日志积累 >5 天未蒸馏 | → memory-distill |
| 近期有新 insight 但 agenda 未更新 | → agenda-evolve |
| 某 direction 素材充足需成文 | → draft-section |

**3. ACT** — 调用判断出的目标 skill（一轮只调一个）

**4. LOG** — 追加本轮行动到 `Workbench/logs/YYYY-MM-DD.md`：
```markdown
### [HH:MM] autoresearch — round N
- **state_summary**: <读到了什么>
- **judgment**: <为什么选这个行动>
- **action**: <调了哪个 skill>
- **outcome**: <产出什么>
```

**5. LOOP** — 回到 1

**停止条件**：
- Supervisor 中断
- 连续 3 轮判断结果相同（卡住）→ 自动暂停，在 `agenda.md` 的 Discussion Topics 中提出问题等待 Supervisor 输入

**Verify**（每轮）：
- `[ ]` 本轮有明确的 skill 调用（不允许"思考了一圈但什么都没做"）
- `[ ]` 日志已追加本轮记录

**Guard**：
- 一轮只调一个卫星 skill（原子性）
- 每轮必须重新读取最新状态（不跳过 READ STATE）
- 不修改 agenda.md 的 Mission
- 连续卡住 3 轮 → 暂停提问
- 不对外发布（投稿、发邮件）——PhD 导师制唯一硬约束

---

## 6. CLAUDE.md 自然语言触发更新

新增 skill 的自然语言触发映射：

| Supervisor 说 | 触发 Skill |
|--------|-----------|
| "想个 idea" / "有什么研究机会" | idea-generate |
| "评估一下这个 idea" / "这个可行吗" | idea-evaluate |
| "设计个实验" / "怎么验证" | experiment-design |
| "记录实验结果" / "实验跑完了" | experiment-track |
| "分析实验结果" | result-analysis |
| "写一下 introduction" / "起草 related work" | draft-section |
| "打磨一下" / "改改这段" | writing-refine |
| "更新研究方向" / "复盘 agenda" | agenda-evolve |
| "自己干活吧" / "开始研究" | autoresearch |

---

## 7. B 层扩展预留

当前 3-experiment 类 skill 聚焦知识管理（设计方案、追踪结果、分析数据），不涉及代码执行。未来加入 B 层时的扩展策略：

- **experiment-design** 的 Steps 中增加"生成实验代码"步骤
- **experiment-track** 的 Steps 中增加"自动抓取训练日志 / W&B metrics"
- **新增 `experiment-iterate`**（L1 编排）：设计 → 执行 → 追踪 → 分析 的自动循环，类似 Karpathy autoresearch 的实验迭代模式
- **新增 3-experiment 下的工程 skill**：如 `hyperparameter-sweep`、`distributed-training` 等，参考 Orchestra SKILLs 的分类体系

接口不变，只在 Steps 内部扩展——现有 skill 的 frontmatter、Guard、Verify 均无需修改。

---

## 8. Implementation Priority

按依赖关系排序的实现顺序：

| 优先级 | Skill | 理由 |
|--------|-------|------|
| P0 | skill-protocol 改造 | 所有新 skill 依赖更新后的 protocol |
| P0 | 现有 4 skill 改造 | pushy description + Verify，小改动大收益 |
| P1 | memory-retrieve | 被多个 skill 内部依赖 |
| P1 | idea-generate | Core Loop 起点 |
| P1 | idea-evaluate | 与 idea-generate 配对 |
| P1 | agenda-evolve | Core Loop 闭环必需 |
| P2 | experiment-design | Phase 3 起点 |
| P2 | experiment-track | 与 experiment-design 配对 |
| P2 | result-analysis | Phase 3 闭环 |
| P3 | draft-section | Phase 5 起点 |
| P3 | writing-refine | 与 draft-section 配对 |
| P4 | autoresearch | 最后实现——所有卫星 skill 就位后才有意义 |
| P4 | CLAUDE.md 触发表更新 | 随 skill 实现同步更新 |
