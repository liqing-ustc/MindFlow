# Skill System Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement the full 14-skill MindFlow system — modify 4 existing skills and create 10 new SKILL.md files.

**Architecture:** Pure Markdown skill files (SKILL.md with YAML frontmatter + body sections). No code, no tests, no build system — this is an Obsidian vault. Each skill follows the protocol defined in `references/skill-protocol.md`.

**Tech Stack:** Markdown, YAML frontmatter, Obsidian wikilinks

**Note:** P0 protocol changes (skill-protocol.md, SPEC.md, CLAUDE.md) are already committed. This plan covers the remaining work: existing skill改造 + all new SKILL.md creation.

---

## File Map

**Modify (4 existing skills — add Verify, update description, add budget):**
- `skills/1-literature/paper-digest/SKILL.md`
- `skills/1-literature/cross-paper-analysis/SKILL.md`
- `skills/1-literature/literature-survey/SKILL.md`
- `skills/5-evolution/memory-distill/SKILL.md`

**Create (10 new skills):**
- `skills/2-ideation/idea-generate/SKILL.md`
- `skills/2-ideation/idea-evaluate/SKILL.md`
- `skills/3-experiment/experiment-design/SKILL.md`
- `skills/3-experiment/experiment-track/SKILL.md`
- `skills/3-experiment/result-analysis/SKILL.md`
- `skills/4-writing/draft-section/SKILL.md`
- `skills/4-writing/writing-refine/SKILL.md`
- `skills/5-evolution/agenda-evolve/SKILL.md`
- `skills/5-evolution/memory-retrieve/SKILL.md`
- `skills/6-orchestration/autoresearch/SKILL.md`

---

### Task 1: Modify paper-digest — pushy description + Verify + budget

**Files:**
- Modify: `skills/1-literature/paper-digest/SKILL.md`

**Spec reference:** `docs/superpowers/specs/2026-03-28-skill-system-design.md` §3.1

- [ ] **Step 1: Read the current file**

Read `skills/1-literature/paper-digest/SKILL.md` to understand current content.

- [ ] **Step 2: Update frontmatter description to pushy version**

Replace the `description` field:

```yaml
description: >
  当 Supervisor 给出论文 URL/标题/PDF/DOI，或阅读队列中有待处理论文时，
  消化论文并生成结构化笔记到 Papers/
```

- [ ] **Step 3: Add budget field to frontmatter**

Add after `output`:

```yaml
budget:
  max_web_calls: 5
```

- [ ] **Step 4: Add Verify section before Examples**

Insert before `## Examples`:

```markdown
## Verify

- [ ] `Papers/YYMM-ShortTitle.md` 已创建且正文 >200 字
- [ ] frontmatter 的 title、authors、date_publish 字段非空
- [ ] Summary 节非空且不超过 3 句话
- [ ] 日志已追加到 `Workbench/logs/YYYY-MM-DD.md`
```

- [ ] **Step 5: Commit**

```bash
git add skills/1-literature/paper-digest/SKILL.md
git commit -m "Improve paper-digest: pushy description, Verify section, budget"
```

---

### Task 2: Modify cross-paper-analysis — pushy description + Verify

**Files:**
- Modify: `skills/1-literature/cross-paper-analysis/SKILL.md`

**Spec reference:** §3.2

- [ ] **Step 1: Read the current file**

Read `skills/1-literature/cross-paper-analysis/SKILL.md`.

- [ ] **Step 2: Update frontmatter description**

```yaml
description: >
  当需要对比多篇论文的方法/结论/实验设置，或 Supervisor 说"对比""分析这几篇"时，
  执行跨论文对比并识别共识、矛盾和知识空白
```

- [ ] **Step 3: Add Verify section before Examples**

```markdown
## Verify

- [ ] `Topics/*-Analysis.md` 已创建
- [ ] 对比表包含所有输入论文
- [ ] 共识、矛盾、知识空白三节均非空
- [ ] 所有论文引用使用 `[[wikilink]]` 格式
```

- [ ] **Step 4: Commit**

```bash
git add skills/1-literature/cross-paper-analysis/SKILL.md
git commit -m "Improve cross-paper-analysis: pushy description, Verify section"
```

---

### Task 3: Modify literature-survey — pushy description + Verify + budget

**Files:**
- Modify: `skills/1-literature/literature-survey/SKILL.md`

**Spec reference:** §3.3

- [ ] **Step 1: Read the current file**

Read `skills/1-literature/literature-survey/SKILL.md`.

- [ ] **Step 2: Update frontmatter description**

```yaml
description: >
  当 Supervisor 说"调研""survey""了解研究现状"，或需要系统了解某主题的文献全貌时，
  搜索外部文献、批量 digest、综合生成调研报告
```

- [ ] **Step 3: Add budget field to frontmatter**

```yaml
budget:
  max_web_calls: 10
```

- [ ] **Step 4: Add Verify section before Examples**

```markdown
## Verify

- [ ] `Topics/*-Survey.md` 已创建
- [ ] 技术路线分类 ≥2 条
- [ ] Paper Comparison 对比表论文数 ≥3
- [ ] Open Problems 节非空
```

- [ ] **Step 5: Remove redundant Guard item about max 10 WebSearch**

The Guard section currently has "最多执行 10 次 WebSearch". Since this is now captured in the `budget` field, remove that specific bullet from Guard to avoid duplication.

- [ ] **Step 6: Commit**

```bash
git add skills/1-literature/literature-survey/SKILL.md
git commit -m "Improve literature-survey: pushy description, Verify section, budget"
```

---

### Task 4: Modify memory-distill — pushy description + Verify

**Files:**
- Modify: `skills/5-evolution/memory-distill/SKILL.md`

**Spec reference:** §3.4

- [ ] **Step 1: Read the current file**

Read `skills/5-evolution/memory-distill/SKILL.md`.

- [ ] **Step 2: Update frontmatter description**

```yaml
description: >
  当积累了多天工作日志、或 Supervisor 说"整理记忆""蒸馏"时，
  从日志中提取 pattern 和 insight 到记忆库。也可被 autoresearch 在合适时机自动调用
```

- [ ] **Step 3: Add Verify section before Examples**

```markdown
## Verify

- [ ] `Workbench/evolution/changelog.md` 已追加本次蒸馏记录
- [ ] 蒸馏结果已记录（新增 pattern 数 + 晋升 insight 数，允许为 0 但须明确记录）
```

- [ ] **Step 4: Commit**

```bash
git add skills/5-evolution/memory-distill/SKILL.md
git commit -m "Improve memory-distill: pushy description, Verify section"
```

---

### Task 5: Create memory-retrieve skill

**Files:**
- Create: `skills/5-evolution/memory-retrieve/SKILL.md`

**Spec reference:** §5.9

- [ ] **Step 1: Create directory and SKILL.md**

Write `skills/5-evolution/memory-retrieve/SKILL.md` with the complete content from the spec. The full file:

```markdown
---
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
---

## Purpose

memory-retrieve 是 MindFlow 记忆系统的检索接口。它被其他 skill 内部调用（如 idea-generate 查失败方向、experiment-design 查有效方法），从 `Workbench/memory/` 的结构化记忆文件中检索与当前任务语义相关的历史经验。

这是 Layer 1 的轻量实现——纯 Markdown 文件读取 + LLM 语义匹配，零外部依赖。未来 Layer 2 可用向量检索替换，接口不变。

## Steps

### Step 1：确定检索范围

根据 `scope` 参数确定要读取的记忆文件：

| scope | 目标文件 |
|:------|:---------|
| `patterns` | `Workbench/memory/patterns.md` |
| `insights` | `Workbench/memory/insights.md` |
| `effective-methods` | `Workbench/memory/effective-methods.md` |
| `failed-directions` | `Workbench/memory/failed-directions.md` |
| `all` | 以上全部 |

### Step 2：读取记忆文件

用 Read 读取 scope 对应的记忆文件。若文件不存在或为空，返回空结果并告知调用方"该记忆类别暂无条目"。

### Step 3：语义匹配

逐条扫描记忆文件中的条目（每个 `### [YYYY-MM-DD]` 标题为一条），判断其与 `query` 的语义相关性。判断标准：

- 条目的 observation/claim/method 是否与 query 描述的任务/问题直接相关
- 条目中引用的论文/实验是否与 query 涉及的领域重叠
- 条目的 lesson/pitfall 是否对 query 的任务有参考价值

### Step 4：返回结果

返回 top-k 相关条目（默认 k=5），每条包含：

- 条目原文（完整保留，不做概括改写）
- 来源文件路径（如 `[[Workbench/memory/patterns.md#条目标题]]`）

若相关条目不足 k 条，返回全部匹配条目，不补凑。

## Guard

- **只读**：不修改任何记忆文件，不修改任何 vault 文件
- **原文保真**：返回结果必须包含条目原文和 `[[wikilink]]` 来源引用，不做概括性改写
- **诚实返回**：若无相关条目，返回空结果，不编造记忆内容
```

- [ ] **Step 2: Commit**

```bash
git add skills/5-evolution/memory-retrieve/SKILL.md
git commit -m "Add memory-retrieve skill: lightweight memory search for other skills"
```

---

### Task 6: Create idea-generate skill

**Files:**
- Create: `skills/2-ideation/idea-generate/SKILL.md`

**Spec reference:** §5.1

- [ ] **Step 1: Read Idea template for reference**

Read `Templates/Idea.md` to understand the output format.

- [ ] **Step 2: Create directory and SKILL.md**

Write `skills/2-ideation/idea-generate/SKILL.md` with the full content. The frontmatter comes directly from §5.1. The body sections:

**Purpose**: 2-3 sentences explaining this generates research ideas from knowledge gaps, validated insights, or Supervisor direction, writing to `Ideas/` in raw status.

**Steps**:
1. 读取来源材料：根据 `source` 参数类型读取对应内容（`Topics/*-Analysis.md` 的知识空白节、`Workbench/memory/insights.md` 的 validated insight、Supervisor 的直接指令、或 `Workbench/agenda.md` 中某 direction 的 next_action）
2. 读取 `Workbench/memory/failed-directions.md`（若存在），提取已废弃方向列表，避免重蹈覆辙
3. 读取 `Domain-Map/_index.md` 找到相关 domain，再读取对应 `Domain-Map/{Name}.md`，了解 Established Knowledge、Active Debates、Open Questions
4. 生成 2-3 个候选 idea。每个 idea 包含：
   - **hypothesis**：可证伪的一句话断言
   - **motivation**：为什么这个问题值得研究
   - **approach sketch**：初步的方法思路
   - **expected outcome**：成功的话预期看到什么
   - **risk**：主要失败模式
5. 读取 `Templates/Idea.md`，按模板格式为每个候选 idea 创建文件到 `Ideas/`，status 设为 `raw`。文件名为描述性名称（如 `Cross-Domain-VLA-Transfer.md`）
6. 追加日志到 `Workbench/logs/YYYY-MM-DD.md`：
   ```markdown
   ### [HH:MM] idea-generate
   - **input**: source: <来源描述>
   - **output**: [[Ideas/xxx]], [[Ideas/yyy]]
   - **observation**: <一句话概括生成的 idea 方向>
   - **status**: success
   ```

**Verify**:
- `[ ]` `Ideas/*.md` 已创建（至少 1 个文件）
- `[ ]` 每个 Idea 的 hypothesis 字段是可证伪的一句话断言
- `[ ]` 未与 `Workbench/memory/failed-directions.md` 中的已废弃方向重复
- `[ ]` 日志已追加

**Guard**:
- 不修改任何已有 Idea 文件
- 不捏造文献支持——所有引用必须指向 vault 中已有的 Paper 笔记（`[[Papers/...]]`）
- 不直接修改 `agenda.md`（idea 只写入 `Ideas/`，由 agenda-evolve 或 Supervisor 决策是否纳入 agenda）
- 语言规范：中文正文 + 英文术语

**Examples**: 1-2 个示例展示从 Analysis 空白生成 idea 和从 Supervisor 指令生成 idea。

- [ ] **Step 3: Commit**

```bash
git add skills/2-ideation/idea-generate/SKILL.md
git commit -m "Add idea-generate skill: create research ideas from knowledge gaps"
```

---

### Task 7: Create idea-evaluate skill

**Files:**
- Create: `skills/2-ideation/idea-evaluate/SKILL.md`

**Spec reference:** §5.2

- [ ] **Step 1: Create SKILL.md**

Write `skills/2-ideation/idea-evaluate/SKILL.md`. Frontmatter from §5.2. Body sections:

**Purpose**: Evaluates a research idea from 5 dimensions (novelty, feasibility, impact, risk, evidence), producing a recommend/revise/shelve verdict and updating the Idea's status.

**Steps**:
1. 读取目标 Idea 笔记（`source` 参数指向的 `[[Ideas/xxx.md]]`）
2. 读取 Idea 中 related_papers 字段引用的 Paper 笔记（用 Read 逐一读取 Summary、Method、Key Results）
3. 读取 `Domain-Map/_index.md` 找到相关 domain，再读取对应 `Domain-Map/{Name}.md` 的 Active Debates 和 Open Questions
4. 从 5 个维度评估，每维度给出 1-5 分和简要说明：
   - **Novelty**（1-5）：与已有工作的差异化程度
   - **Feasibility**（1-5）：当前资源条件下能否执行
   - **Impact**（1-5）：若成功，对领域的贡献
   - **Risk**（1-5）：主要失败模式和概率（分越高风险越低）
   - **Evidence**（1-5）：当前支撑假设的证据强度
5. 基于评分生成结论：
   - **recommend**：总分 ≥18 或无致命短板 → 建议推进
   - **revise**：有潜力但某维度 ≤2 → 附具体修改建议
   - **shelve**：总分 <12 或可行性 =1 → 建议搁置并说明原因
6. 用 Edit 在目标 Idea 笔记末尾追加评估记录：
   ```markdown
   ## Evaluation — YYYY-MM-DD

   | Dimension | Score | Notes |
   |:----------|:------|:------|
   | Novelty | N/5 | ... |
   | Feasibility | N/5 | ... |
   | Impact | N/5 | ... |
   | Risk | N/5 | ... |
   | Evidence | N/5 | ... |

   **Verdict**: recommend / revise / shelve
   **Reasoning**: ...
   **Suggestions**: ...
   ```
7. 用 Edit 更新 Idea frontmatter 的 `status`：recommend → `developing`；shelve → `archived`；revise → 保持 `raw`
8. 追加日志

**Verify**:
- `[ ]` Idea 文件已追加 `## Evaluation` 节
- `[ ]` 5 个维度均有评分（1-5）和简要说明
- `[ ]` 结论为 recommend / revise / shelve 之一
- `[ ]` Idea 的 frontmatter status 已同步更新

**Guard**:
- 不修改 Idea 的 hypothesis 字段
- 评估必须基于 vault 中可追溯的证据，不凭空判断
- 语言规范：中文正文 + 英文术语

- [ ] **Step 2: Commit**

```bash
git add skills/2-ideation/idea-evaluate/SKILL.md
git commit -m "Add idea-evaluate skill: 5-dimension assessment of research ideas"
```

---

### Task 8: Create agenda-evolve skill

**Files:**
- Create: `skills/5-evolution/agenda-evolve/SKILL.md`

**Spec reference:** §5.8

- [ ] **Step 1: Read agenda-protocol for reference**

Read `references/agenda-protocol.md` to understand format and permissions.

- [ ] **Step 2: Create SKILL.md**

Write `skills/5-evolution/agenda-evolve/SKILL.md`. Frontmatter from §5.8. Body sections:

**Purpose**: Evolves the research agenda based on accumulated insights, experiment results, and idea evaluations. Updates directions (add/modify/pause/abandon) in `Workbench/agenda.md`.

**Steps**:
1. 读取 `Workbench/agenda.md` 当前完整内容
2. 读取 `Workbench/memory/insights.md`，提取近期（30 天内）的 validated insights
3. 读取 `Workbench/memory/failed-directions.md`（若存在），了解已废弃方向
4. 读取 `Workbench/queue.md` 的 Questions 和 Review 部分
5. 用 Grep 在 `Ideas/` 中搜索 `status: developing` 或 `status: validated` 的 Idea 文件，用 Read 读取其 hypothesis 和评估结论
6. 综合以上信息，判断 agenda 需要哪些变更：
   - **新增 direction**：从 validated idea 或 validated insight 衍生，按 `references/agenda-protocol.md` 格式填写所有字段
   - **更新 direction**：修改 status / confidence / evidence / next_action（证据增强→提升 confidence；新实验完成→更新 evidence 和 next_action）
   - **暂停 direction**：长期无进展的方向移入 Paused，必须填写 `pause_reason` 和 `resume_condition`
   - **废弃 direction**：被实验明确反驳的方向移入 Abandoned，必须填写 `reason` 和 `lesson`，同步用 Edit 追加到 `Workbench/memory/failed-directions.md`
7. 用 Edit 更新 `Workbench/agenda.md`（修改对应 section 内容），同步更新 frontmatter 的 `last_updated` 和 `updated_by: agenda-evolve`
8. 用 Edit 追加变更记录到 `Workbench/evolution/changelog.md`：
   ```markdown
   ### [YYYY-MM-DD] agenda-evolve
   - **trigger**: <触发原因>
   - **added**: <新增 direction 名称列表，或 "无">
   - **updated**: <更新的 direction 及变更内容>
   - **paused**: <暂停的 direction 及原因>
   - **abandoned**: <废弃的 direction 及原因>
   - **reasoning**: <简要说明变更逻辑>
   ```
9. 追加日志到 `Workbench/logs/YYYY-MM-DD.md`

**Verify**:
- `[ ]` `agenda.md` 的 `last_updated` 已更新为今天日期
- `[ ]` 每个 Active Direction 都有非空 `next_action`
- `[ ]` 新增或变更有 `changelog.md` 记录
- `[ ]` 日志已追加

**Guard**:
- 严格遵循 `references/agenda-protocol.md` 的所有规则和字段格式
- 不删除 Supervisor 手动添加的 direction（只可暂停并注明原因）
- 每次变更在 changelog 中记录推理过程
- 不修改 Mission 节（Mission 的演化由 Supervisor 决定或 Researcher 提议后 Supervisor 确认）
- 语言规范：中文正文 + 英文术语

- [ ] **Step 3: Commit**

```bash
git add skills/5-evolution/agenda-evolve/SKILL.md
git commit -m "Add agenda-evolve skill: evolve research agenda from insights and results"
```

---

### Task 9: Create experiment-design skill

**Files:**
- Create: `skills/3-experiment/experiment-design/SKILL.md`

**Spec reference:** §5.3

- [ ] **Step 1: Read Experiment template**

Read `Templates/Experiment.md` to understand output format.

- [ ] **Step 2: Create SKILL.md**

Write `skills/3-experiment/experiment-design/SKILL.md`. Frontmatter from §5.3. Body sections:

**Purpose**: Designs a complete experiment plan for a research idea, covering variables, baseline, metrics, steps, expected outcomes, and risks.

**Steps**:
1. 读取目标 Idea 笔记（`idea` 参数），提取 hypothesis 和 approach sketch。验证 Idea 的 status 为 `developing` 或 `validated`，否则停止并提示
2. 读取 `skills/5-evolution/memory-retrieve/SKILL.md` 并按其 Steps 执行，scope 设为 `effective-methods`，query 为 Idea 的 hypothesis 关键词。再次执行 memory-retrieve，scope 设为 `failed-directions`
3. 设计实验方案，包含以下六部分：
   - **Variables**：自变量（被操控的因素）、因变量（被测量的结果）、控制变量（保持不变的条件）
   - **Baseline**：对比基线是什么，为什么选择这个基线
   - **Metrics**：衡量指标（必须可量化或可明确判定），指标名 + 计算方式 + 判定阈值
   - **Steps**：具体实验步骤（按执行顺序编号）
   - **Expected Outcome**：分两种情况——假设成立时预期什么结果；假设不成立时预期什么结果
   - **Risk & Mitigation**：主要失败点 + 对应备选方案
4. 读取 `Templates/Experiment.md`，按模板格式将实验方案写入 `Experiments/`，status 设为 `planning`。文件名为描述性名称
5. 用 Edit 在目标 Idea 笔记的适当位置追加实验链接：`- **experiment**: [[Experiments/xxx]]`
6. 追加日志

**Verify**:
- `[ ]` `Experiments/*.md` 已创建
- `[ ]` Variables、Baseline、Metrics 三节均非空
- `[ ]` Expected Outcome 包含假设成立和不成立两种情况
- `[ ]` 日志已追加

**Guard**:
- Metrics 必须可量化或可明确判定（不接受"看起来更好"等主观指标）
- 不修改源 Idea 的 hypothesis（实验是验证假设，不是改假设）
- 若 Idea status 不为 developing/validated，停止执行并告知 Supervisor
- 语言规范：中文正文 + 英文术语

- [ ] **Step 3: Commit**

```bash
git add skills/3-experiment/experiment-design/SKILL.md
git commit -m "Add experiment-design skill: design experiment plans for ideas"
```

---

### Task 10: Create experiment-track skill

**Files:**
- Create: `skills/3-experiment/experiment-track/SKILL.md`

**Spec reference:** §5.4

- [ ] **Step 1: Create SKILL.md**

Write `skills/3-experiment/experiment-track/SKILL.md`. Frontmatter from §5.4. Body sections:

**Purpose**: Records experiment progress by appending Run Entries to Experiment notes. Tracks config, results, observations, and next steps for each run.

**Steps**:
1. 读取目标 Experiment 笔记（`experiment` 参数），确认文件存在
2. 计算当前 Run 编号：扫描笔记中已有的 `### Run [N]` 标题，新 Run 编号为 max(N) + 1
3. 用 Edit 在 Experiment 笔记末尾（`## Analysis` 之前，若存在；否则文件末尾）追加：
   ```markdown
   ### Run [N] — YYYY-MM-DD
   - **config**: <从 `result` 参数和对话上下文提取本轮配置/参数>
   - **result**: <结果数据>
   - **observation**: <一句话关键发现>
   - **next**: <下一步打算——继续 / 调整 / 停止>
   ```
4. 用 Edit 更新 Experiment frontmatter 的 `status`：
   - 若当前为 `planning` → 改为 `running`
   - 若当前为 `running` → 保持 `running`
   - 若 `next` 为"停止"→ 改为 `completed`（目标达成时）或 `failed`（确认失败时）
5. 追加日志

**Verify**:
- `[ ]` Experiment 文件已追加 Run Entry
- `[ ]` Run Entry 的 result 字段非空
- `[ ]` 日志已追加

**Guard**:
- 不修改已有 Run Entry（append-only，与 memory protocol 一致）
- 不修改 Experiment 的 Variables / Baseline / Metrics 设计（那是 experiment-design 的职责）
- 语言规范：中文正文 + 英文术语

- [ ] **Step 2: Commit**

```bash
git add skills/3-experiment/experiment-track/SKILL.md
git commit -m "Add experiment-track skill: record experiment runs and results"
```

---

### Task 11: Create result-analysis skill

**Files:**
- Create: `skills/3-experiment/result-analysis/SKILL.md`

**Spec reference:** §5.5

- [ ] **Step 1: Create SKILL.md**

Write `skills/3-experiment/result-analysis/SKILL.md`. Frontmatter from §5.5. Body sections:

**Purpose**: Analyzes experiment results to determine whether the hypothesis is supported, refuted, or inconclusive. Updates the Experiment note with an Analysis section and syncs the linked Idea's status.

**Steps**:
1. 读取目标 Experiment 笔记，提取所有 Run Entries 的 result 和 observation
2. 从 Experiment 笔记的 frontmatter 或正文中找到关联的 Idea 引用（如 `[[Ideas/xxx]]`），读取该 Idea 的 hypothesis
3. 读取 `skills/5-evolution/memory-retrieve/SKILL.md` 并按其 Steps 执行，scope 设为 `insights`，query 为 hypothesis 关键词。再次执行 memory-retrieve，scope 设为 `patterns`
4. 综合分析：
   - **Hypothesis verdict**：`supported`（数据一致支持）/ `refuted`（数据明确反驳）/ `inconclusive`（证据不足），附具体数据证据
   - **Key findings**：实验揭示的主要发现（可能超出原始假设范围）
   - **Comparison to baseline**：与 Baseline 的定量/定性对比
   - **Limitations**：本实验的局限性（样本量、设置简化、外部效度等）
   - **Implications**：对当前研究方向的影响——是否需要调整 agenda
5. 用 Edit 在 Experiment 笔记中追加 `## Analysis` 节（若已存在，在其末尾追加新分析并标注日期）
6. 若分析发现跨实验 pattern（如"所有 X 方法在 Y 条件下失败"），读取 `Workbench/memory/patterns.md`，用 Edit 追加新 pattern 条目
7. 若 hypothesis verdict 明确（supported 或 refuted），用 Edit 更新关联 Idea 的 frontmatter status：
   - supported → `validated`
   - refuted → `archived`
8. 追加日志

**Verify**:
- `[ ]` Experiment 笔记有 `## Analysis` 节
- `[ ]` Hypothesis verdict 为 supported / refuted / inconclusive 之一
- `[ ]` 若 verdict 明确，关联 Idea 的 status 已同步更新
- `[ ]` 日志已追加

**Guard**:
- Hypothesis verdict 必须基于 Run Entries 中的实际数据，不凭推测
- 若结果为 inconclusive，不强行下结论——标注需要更多实验
- 不修改 Run Entries（只追加 Analysis 节）
- 语言规范：中文正文 + 英文术语

- [ ] **Step 2: Commit**

```bash
git add skills/3-experiment/result-analysis/SKILL.md
git commit -m "Add result-analysis skill: analyze experiments and judge hypotheses"
```

---

### Task 12: Create draft-section skill

**Files:**
- Create: `skills/4-writing/draft-section/SKILL.md`

**Spec reference:** §5.6

- [ ] **Step 1: Create SKILL.md**

Write `skills/4-writing/draft-section/SKILL.md`. Frontmatter from §5.6. Body sections:

**Purpose**: Drafts a specific section of a paper or report using vault sources as material. Follows academic writing conventions with `[[wikilink]]` citations.

**Steps**:
1. 读取 `sources` 参数中引用的所有笔记（用 Read 逐一读取 `[[Papers/...]]`、`[[Experiments/...]]`、`[[Ideas/...]]`、`[[Topics/...]]` 的相关内容）
2. 若 `target` 文件已存在，用 Read 读取全部内容，了解已有章节的上下文、风格和论述方向
3. 读取 `Domain-Map/_index.md` 找到相关 domain，再读取对应 `Domain-Map/{Name}.md` 了解领域背景
4. 起草 `section` 指定的章节，遵循以下规范：
   - 学术写作规范：逻辑清晰、论据充分、行文连贯
   - 所有论文引用使用 `[[wikilink]]` 格式
   - 中文正文 + 英文术语（与 vault 规范一致）
   - 每个核心 claim 必须有来源支撑
5. 写入文件：
   - 若 `target` 文件不存在：用 Write 创建文件，包含基本 frontmatter（title、date、tags）和起草的章节
   - 若 `target` 文件已存在：用 Edit 在合适位置插入新 section（按章节逻辑顺序）
6. 追加日志

**Verify**:
- `[ ]` 目标文件中指定 section 已写入且 >200 字
- `[ ]` 所有事实性陈述有 `[[wikilink]]` 来源
- `[ ]` 无 `[TODO]`、`[TBD]` 占位符
- `[ ]` 日志已追加

**Guard**:
- 不修改目标文件中的其他章节（只动指定 section）
- 不捏造引用——所有 `[[wikilink]]` 必须指向 vault 中实际存在的笔记
- copilot 模式下先输出草稿预览，Supervisor 确认后再写入文件
- 语言规范：中文正文 + 英文术语

- [ ] **Step 2: Commit**

```bash
git add skills/4-writing/draft-section/SKILL.md
git commit -m "Add draft-section skill: draft paper/report sections from vault sources"
```

---

### Task 13: Create writing-refine skill

**Files:**
- Create: `skills/4-writing/writing-refine/SKILL.md`

**Spec reference:** §5.7

- [ ] **Step 1: Create SKILL.md**

Write `skills/4-writing/writing-refine/SKILL.md`. Frontmatter from §5.7. Body sections:

**Purpose**: Refines existing drafts from three dimensions — structure (logical flow), clarity (expression), and evidence (citation support). Defaults to copilot mode where suggestions are presented for Supervisor approval.

**Steps**:
1. 读取 `target` 文件内容。若指定了 `section`，定位到该章节；否则审视全文
2. 根据 `focus` 参数（默认 `all`）逐维度审视：
   - **structure**：段落间逻辑链是否连贯？过渡是否自然？论证顺序是否合理？
   - **clarity**：有无冗余表达？有无歧义？有无过度抽象？术语使用是否一致？
   - **evidence**：每个核心 claim 是否有 `[[wikilink]]` 来源支撑？引用是否指向 vault 中实际存在的笔记？
3. 生成修改建议列表，每条包含：
   - 位置（章节名 + 段落/句子定位）
   - 问题描述
   - 修改建议（具体替换文字或结构调整方案）
4. 输出建议列表供 Supervisor 确认（copilot 模式为默认）。Supervisor 逐条确认/拒绝/修改后，用 Edit 执行已确认的修改
5. 追加日志

**Verify**:
- `[ ]` 修改后无新引入的 `[TODO]`、`[TBD]` 占位符
- `[ ]` 修改后 `[[wikilink]]` 引用仍有效（未误删或打断链接）
- `[ ]` 日志已追加

**Guard**:
- 默认 copilot 模式（autonomy: low）——打磨是主观判断，应让 Supervisor 确认
- 不改变核心论点或结论（打磨是改表达，不是改观点）
- 不增删章节（增删章节是 draft-section 的职责）
- 语言规范：中文正文 + 英文术语

- [ ] **Step 2: Commit**

```bash
git add skills/4-writing/writing-refine/SKILL.md
git commit -m "Add writing-refine skill: polish drafts for structure, clarity, evidence"
```

---

### Task 14: Create autoresearch skill

**Files:**
- Create: `skills/6-orchestration/autoresearch/SKILL.md`

**Spec reference:** §5.10

- [ ] **Step 1: Create SKILL.md**

Write `skills/6-orchestration/autoresearch/SKILL.md`. Frontmatter from §5.10. Body sections:

**Purpose**: MindFlow 的核心研究循环。持续运行，每轮读取 Workbench 状态（agenda、queue、memory、logs），判断当前研究进展的最大瓶颈，调用对应卫星 skill 执行最高价值行动，记录后进入下一轮。Supervisor 随时可中断。

**Steps**:

每轮执行以下 4 步，然后循环：

**Step 1：READ STATE**

读取以下文件了解当前状态：
1. `Workbench/agenda.md` — 当前研究方向、优先级、各 direction 的 next_action
2. `Workbench/queue.md` — 待处理任务（Reading / Review / Questions / Experiments）
3. `Workbench/memory/insights.md` — 近期 insight（关注 status: validated 且近 30 天）
4. `Workbench/memory/patterns.md` — 近期 pattern
5. 用 Glob 列出最近 3 天的 `Workbench/logs/YYYY-MM-DD.md`，用 Read 读取，了解近期执行了什么

若 `focus` 参数指定了某个 direction，重点关注该 direction 相关的信息。

**Step 2：JUDGE**

基于 Step 1 读取的状态，判断下一个最高价值行动。以下为参考启发（非硬编码，由 LLM 综合判断）：

| 状态信号 | 可能的行动 |
|:--------|:----------|
| queue 的 Reading 部分有待处理论文 | 读取 `skills/1-literature/paper-digest/SKILL.md` 并执行 |
| agenda 中某 direction 缺乏文献支撑（evidence 稀疏） | 读取 `skills/1-literature/literature-survey/SKILL.md` 并执行 |
| 近期有 Topics/*-Analysis.md 标注了知识空白 | 读取 `skills/2-ideation/idea-generate/SKILL.md` 并执行 |
| Ideas/ 中有 status: raw 的 idea 待评估 | 读取 `skills/2-ideation/idea-evaluate/SKILL.md` 并执行 |
| Ideas/ 中有 status: developing 的 idea 缺实验方案 | 读取 `skills/3-experiment/experiment-design/SKILL.md` 并执行 |
| Experiments/ 中有 status: completed 且无 Analysis 节 | 读取 `skills/3-experiment/result-analysis/SKILL.md` 并执行 |
| 最近一次 memory-distill 距今 >5 天 | 读取 `skills/5-evolution/memory-distill/SKILL.md` 并执行 |
| 近期有新 validated insight 但 agenda 未反映 | 读取 `skills/5-evolution/agenda-evolve/SKILL.md` 并执行 |
| 某 direction 已有充足论文+实验+idea，需要成文 | 读取 `skills/4-writing/draft-section/SKILL.md` 并执行 |

**Step 3：ACT**

读取判断出的目标 skill 的 SKILL.md，严格按其 Steps、Guard、Verify 执行。一轮只调一个 skill。

**Step 4：LOG**

用 Edit 追加本轮行动到 `Workbench/logs/YYYY-MM-DD.md`：

```markdown
### [HH:MM] autoresearch — round N
- **state_summary**: <读到了什么关键状态>
- **judgment**: <为什么选这个行动（一句话推理）>
- **action**: <调了哪个 skill，传了什么参数>
- **outcome**: <产出什么文件/更新>
```

然后回到 Step 1 开始下一轮。

**Verify**（每轮）:
- `[ ]` 本轮有明确的 skill 调用（不允许"思考了一圈但什么都没做"）
- `[ ]` 日志已追加本轮记录

**Guard**:
- **原子性**：一轮只调一个卫星 skill——做一件事，做完记录，再想下一件
- **状态刷新**：每轮必须重新读取最新状态（不跳过 READ STATE），因为上一轮的行动可能改变了 vault 状态
- **Mission 只读**：不修改 `agenda.md` 的 Mission 节
- **卡住检测**：若连续 3 轮的 JUDGE 判断结果指向同一个 skill 且同一个目标（如连续 3 轮都想对同一个 idea 做 evaluate），说明被卡住了——暂停循环，在 `agenda.md` 的 Discussion Topics 中添加一条问题，等待 Supervisor 输入
- **不对外发布**：不投稿论文、不发送外部通讯——PhD 导师制的唯一硬约束
- **Skill 执行规范**：调用卫星 skill 时，必须先 Read 对应的 SKILL.md 文件，严格按其 Steps 和 Guard 执行，不凭记忆执行

- [ ] **Step 2: Commit**

```bash
git add skills/6-orchestration/autoresearch/SKILL.md
git commit -m "Add autoresearch skill: core research loop orchestrating all satellite skills"
```

---

### Task 15: Final commit — all skills complete

- [ ] **Step 1: Verify all 14 skill files exist**

Run:
```bash
find skills/ -name "SKILL.md" | sort
```

Expected output (14 files):
```
skills/1-literature/cross-paper-analysis/SKILL.md
skills/1-literature/literature-survey/SKILL.md
skills/1-literature/paper-digest/SKILL.md
skills/2-ideation/idea-evaluate/SKILL.md
skills/2-ideation/idea-generate/SKILL.md
skills/3-experiment/experiment-design/SKILL.md
skills/3-experiment/experiment-track/SKILL.md
skills/3-experiment/result-analysis/SKILL.md
skills/4-writing/draft-section/SKILL.md
skills/4-writing/writing-refine/SKILL.md
skills/5-evolution/agenda-evolve/SKILL.md
skills/5-evolution/memory-distill/SKILL.md
skills/5-evolution/memory-retrieve/SKILL.md
skills/6-orchestration/autoresearch/SKILL.md
```

- [ ] **Step 2: Verify no placeholder text in any skill**

Run:
```bash
grep -r "TBD\|TODO\|TBC\|PLACEHOLDER" skills/ || echo "No placeholders found"
```

Expected: "No placeholders found"

- [ ] **Step 3: Final verification commit if clean**

If all checks pass, no additional commit needed — each task already committed individually.
