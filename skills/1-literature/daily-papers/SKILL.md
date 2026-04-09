---
name: daily-papers
description: >
  每日论文推荐。抓取 HuggingFace Daily/Trending + arXiv 最新论文，按研究方向打分筛选，
  生成论文笔记后基于深度阅读写出有态度的推荐锐评，保存到 Workbench/daily/。
  触发词："今日论文推荐""过去3天论文推荐""过去一周论文推荐""看看最近有什么论文"
argument-hint: "[今日 / 过去N天 / 过去一周]"
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

## Purpose

自动发现与研究方向相关的最新论文，生成推荐列表。分三步：

1. **Python 脚本**抓取 + 打分（零 token）
2. **快速分流** → 为优先论文生成笔记（paper-digest，独立 agent）
3. **基于笔记的深度点评** → 保存推荐文件

## Steps

### Step 0：解析时间范围

从用户输入中解析天数：
- "今日论文推荐"、"今日论文"、"每日推荐" → 当天（`--days 1`）
- "过去3天"、"最近三天" → `--days 3`
- "过去一周"、"最近7天" → `--days 7`
- "过去两周" → `--days 14`
- 无特殊指定 → 默认当天

将解析出的天数存为 `DAYS` 变量。

### Step 1：抓取 + 打分（Python 脚本，零 token）

运行 `fetch_and_score.py`，输出到 `Workbench/daily/.candidates.json`：

```bash
python3 skills/1-literature/daily-papers/fetch_and_score.py \
  --days {DAYS} \
  --output Workbench/daily/.candidates.json
```

**检查输出**：确认文件存在且包含有效 JSON 数组。如果为空数组，检查 stderr 诊断问题（可能是周末 arXiv 无更新、网络问题等），告知用户原因后停止。

**历史去重**：脚本在 output 同目录维护 `.history.json`，单天模式自动过滤已推荐过的论文（30 天窗口），多天模式跳过去重。每次运行后自动更新历史。

### Step 2：快速分流

读取 `Workbench/daily/.candidates.json`，做**轻量级分类**，不写详细点评。

**检查已有推荐文件**：读取 `Workbench/daily/YYYY-MM-DD.md`（如存在），提取已点评论文的 arXiv ID 列表，在后续步骤中复用已有点评。

#### 2a：兜底过滤

参照研究兴趣判断论文相关性，所有列出的方向均为核心。如果发现某篇论文与所有研究兴趣均无关，而且 score 不高，直接跳过。记录被跳过的论文标题和原因。

#### 2b：分流

基于摘要和 score，将论文分为三个等级：
- 🔥 **必读**：核心方向 + 方法有新意或结果显著
- 👀 **值得看**：相关方向 + 有参考价值
- 💤 **可跳过**：边缘相关或增量有限

每篇论文只需**一句话分流理由**，不写详细点评。已有笔记的论文直接标注 `📒 已有笔记`。

### Step 3：论文笔记生成

必须通过 Task agent 调用 /paper-digest skill 生成论文笔记。不要因为"怕 context overflow"或"论文太多"就自己写个 70 行的骨架糊弄过去。paper-digest 在独立的 Task agent 中运行，不会占用主 agent 的 context。

**范围控制**：仅对“必读”论文生成笔记，"值得看"和"可跳过"的不生成笔记

**跳过条件**（满足任一即跳过）：
- 用 Glob 扫描 `Papers/` 目录，**已有笔记的论文跳过**
- 已有推荐文件中**已有点评的论文跳过**（Step 2 中已识别）

**并行执行**：多篇论文的笔记生成应并行启动（background agents）。等待所有笔记完成后再进入下一步。

**失败 fallback**：如果某篇论文笔记生成失败（PDF 抓不到、网络超时等），在 Step 4 中基于摘要写简评，并标注"笔记生成失败，基于摘要评价"。

### Step 4：深度点评

**仅对本次新增论文生成点评**。已有推荐文件中的点评直接复用，不重新生成。

读取需点评论文的笔记文件，基于笔记中的完整信息生成推荐点评。

**分流校准**：基于笔记内容，可以调整 Step 2 的分流结果（升级或降级 tier）。分流表以 Step 4 的最终判断为准。

#### 点评格式

```markdown
---
date: YYYY-MM-DD
tags: [daily-papers, tag1, tag2, ...]
---
# 🔪 今日锐评

2-3 句话，简短直接：
- 今天论文整体水平如何，有没有跨论文的主线或 pattern
- 哪个方向在爆发、哪些是灌水重灾区
- 如果和笔记库里已有的工作撞车了，直接点名

## 分流表

| 等级 | 论文 |
|------|------|
| 🔥 必读 | [[#1. Paper1 短标题\|Paper1]]（理由）· [[#2. Paper2 短标题\|Paper2]]（理由） |
| 👀 值得看 | [[#3. Paper3 短标题\|Paper3]]（理由）· [[#4. Paper4 短标题\|Paper4]]（理由） |
| 💤 可跳过 | [[#5. Paper5 短标题\|Paper5]]（理由） |

## 论文点评

### 1. 论文短标题
- **Title**:
- **Authors**:
- **Institutes**: (如没有，则跳过)
- **Source**: [link](url)  📰 HF Daily ⬆️ N / 🔥 HF Trending ⬆️ N / 📄 arXiv
- **Method**: 用3-5 句话讲清楚方法的核心机制和主要结果，要通俗易懂，避免不必要的专业术语。
- **锐评**: 这篇到底行不行？方法有没有硬伤？claim 和证据匹配吗？跟已有工作的本质区别在哪？哪些数字亮眼、哪些数字暴露问题？
- **📒 论文笔记**: [[笔记文件名]] （如有笔记）

...（按推荐等级排序，每篇论文一个 ### 段落）

## 已排除论文

| 论文 | 排除原因 |
|------|----------|
| ... | ... |
```

#### 点评原则

- **点评人设**: 你是一个毒舌但眼光极准的 AI 论文审稿人，说话像一个见多识广、对灌水零容忍的 senior researcher。
- **语气要求**：毒舌、尖锐、精炼、有态度。不和稀泥，不说"总体还行"。明确判断好/坏
- **点评依据**：有笔记的论文，评价必须基于笔记内容。无笔记的论文，评价基于摘要。
- **内容具体**：夸要具体：哪个数字强、哪个设计有新意，一句话点到。骂要更具体：哪个假设不成立、哪个实验缺了、哪个 claim 站不住脚
- **来源格式**：
  - `hf-daily` → `📰 HF Daily ⬆️ {hf_upvotes}`
  - `hf-trending` → `🔥 HF Trending ⬆️ {hf_upvotes}`
  - `arxiv` → `📄 arXiv`

### Step 5：保存推荐文件

保存到 `Workbench/daily/YYYY-MM-DD.md`（日期为目标日期）。

**合并逻辑**：若推荐文件已存在：
1. 读取已有文件，按 `### N. 标题` 提取每篇论文的完整点评块
2. **已有论文保留原点评**：如果本次候选中的论文在已有文件中已有点评（按 arXiv URL 匹配），直接复用原点评内容，不重新生成
3. **新论文追加**：本次新增的论文点评插入到对应 tier 的位置，重新编号
4. **重新生成锐评和分流表**：基于合并后的全部论文更新 `# 🔪 今日锐评` 和 `## 分流表`
5. 用 Write 写入合并后的完整文件

### Step 6：追加工作日志

将以下格式的 log entry 追加到 `Workbench/logs/YYYY-MM-DD.md`（日期为今天）：

```markdown
### [HH:MM] daily-papers
- **input**: {DAYS} 天
- **output**: [[Workbench/daily/YYYY-MM-DD]]
- **observation**: 推荐 N 篇（必读 X / 值得看 Y / 可跳过 Z）
- **status**: success
```

若日志文件不存在，先创建文件（包含一级标题 `# YYYY-MM-DD`），再追加 entry。

### Step 7：输出摘要

告知用户：
- 抓取了多少篇候选论文
- 推荐了多少篇（必读 / 值得看 / 可跳过 各多少）
- 已为 N 篇必读论文生成笔记

## Guard

- **不捏造论文信息**：所有内容必须来自抓取数据或生成的笔记。不确定就标注"摘要未提及"

## Verify

- [ ] `Workbench/daily/.candidates.json` 存在且非空
- [ ] `Workbench/daily/YYYY-MM-DD.md` 已创建
- [ ] 分流表中的 `[[#heading|display]]` 链接与论文点评的 `###` 标题完全匹配
- [ ] 必读论文已通过 paper-digest 生成笔记
- [ ] 有笔记的论文点评基于笔记内容
- [ ] 日志已追加到 `Workbench/logs/YYYY-MM-DD.md`

## Examples

**示例 1：今日推荐**

```
今日论文推荐
```

执行过程：
1. 运行 `fetch_and_score.py --days 1`
2. 读取 JSON，扫描 `Papers/` 匹配已有笔记，快速分流（tier + 一句话理由）
3. 并行启动 Task agents 为必读论文生成笔记
4. 读取所有笔记，基于深度阅读生成点评，一次成型保存到 `Workbench/daily/2026-04-07.md`
5. 追加日志

**示例 2：过去一周**

```
过去一周论文推荐
```

执行过程：
1. 运行 `fetch_and_score.py --days 7`
2. 快速分流，仅对必读论文生成笔记（top_n = min(30 * 7, 100) = 100）
3. 后续同示例 1
