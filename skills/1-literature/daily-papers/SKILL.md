---
name: daily-papers
description: >
  每日论文推荐。抓取 HuggingFace Daily/Trending + arXiv 最新论文，按研究方向打分筛选，
  生成有态度的推荐点评，保存到 Workbench/daily/，并按等级更新阅读列表。
  触发词："今日论文推荐""过去3天论文推荐""过去一周论文推荐""看看最近有什么论文"
argument-hint: "[今日 / 过去N天 / 过去一周]"
allowed-tools: Bash, Read, Write, Edit, Glob, Grep
---

## Purpose

自动发现与研究方向相关的最新论文，生成推荐列表。分两步：

1. **Python 脚本**抓取 + 打分（零 token）
2. **LLM 点评**分流 + 锐评 → 保存推荐文件 + 更新阅读列表

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
  --history Workbench/daily/.history.json \
  --output Workbench/daily/.candidates.json
```

**检查输出**：确认文件存在且包含有效 JSON 数组。如果为空数组，检查 stderr 诊断问题（可能是周末 arXiv 无更新、网络问题等），告知用户原因后停止。

> 脚本会自动更新 `.history.json`（追加本次所有论文，保留 30 天窗口），无需手动处理。

### Step 2：点评 + 分流

读取 `Workbench/daily/.candidates.json`，生成推荐点评。

#### 2a：扫描已有笔记

用 Glob 扫描 `Papers/` 目录，将候选论文标题与已有笔记做匹配。已有笔记的论文标记为 `has_existing_note`。

#### 2b：兜底过滤

参照研究兴趣判断论文相关性，所有列出的方向均为核心,如果发现某篇论文与所有研究兴趣均无关，而且score不高，直接跳过。在末尾注明被跳过的论文标题和原因。

#### 2c：生成点评

按以下格式生成推荐文件内容：

```markdown
---
date: YYYY-MM-DD
tags: [daily-papers]
---
# YYYY-MM-DD 论文推荐

> 2-3 句话总结：今天推荐的论文主要包含哪些方面。

## 分流表

| 等级 | 论文 |
|------|------|
| 🔥 必读 | [[#1. Paper1 短标题\|Paper1]]（理由）· [[#2. Paper2 短标题\|Paper2]]（理由） |
| 👀 值得看 | [[#3. Paper3 短标题\|Paper3]]（理由）· [[#4. Paper4 短标题\|Paper4]]（理由） |
| 💤 可跳过 | [[#5. Paper5 短标题\|Paper5]]（理由） |

## 详评

### 1. 论文短标题
- **Title**:
- **Authors**:
- **Source**: [link](url) 📰 HF Daily ⬆️ N / 🔥 HF Trending ⬆️ N / 📄 arXiv
- **Method**: 3-5 句话讲清楚方法怎么工作。
- **锐评**: 有态度的点评。好在哪，差在哪，跟已有工作的区别

...（按推荐等级排序，每篇论文一个 ### 段落）

## 已排除论文

| 论文 | 排除原因 |
|------|----------|
| ... | ... |
```

#### 点评原则

- **有态度**：不和稀泥，不说"总体还行"。明确判断好/坏
- **基于事实**：所有评价必须有摘要中的依据。不确定的信息标注"摘要未提及"
- **来源格式**：
  - `hf-daily` → `📰 HF Daily ⬆️ {hf_upvotes}`
  - `hf-trending` → `🔥 HF Trending ⬆️ {hf_upvotes}`
  - `arxiv` → `📄 arXiv`
- **已有笔记**的论文用精简格式：`📒 已有笔记: [[Papers/YYMM-ShortTitle]]`，不重复介绍
- **再推论文**（`is_re_recommend: true`）标注：`> ⏪ 再推提醒：{last_recommend_date} 推荐过`

### Step 3：保存推荐文件

用 Write 保存到 `Workbench/daily/YYYY-MM-DD.md`（日期为目标日期）。

若文件已存在，告知用户并询问是否覆盖。

### Step 4：更新阅读列表

将推荐论文按等级写入 `Workbench/daily/reading_list.md`。

若文件不存在，先创建：

```markdown
# Reading List

## 🔥 必读

## 👀 值得看
```

**追加规则**：

- 将"🔥 必读"论文追加到 `## 🔥 必读` 下方（`## 👀 值得看` 之前）
- 将"👀 值得看"论文追加到 `## 👀 值得看` 下方（文件末尾）
- 不追加"💤 可跳过"的论文
- 不追加已有笔记的论文（`has_existing_note`）
- 不追加已存在于列表中的论文（按 URL 去重）

每条格式：

```markdown
- [ ] [论文标题](arXiv URL) — 一句话理由 ← YYYY-MM-DD
```

### Step 5：追加工作日志

将以下格式的 log entry 追加到 `Workbench/logs/YYYY-MM-DD.md`（日期为今天）：

```markdown
### [HH:MM] daily-papers
- **input**: {DAYS} 天
- **output**: [[Workbench/daily/YYYY-MM-DD]]
- **observation**: 推荐 N 篇（必读 X / 值得看 Y / 可跳过 Z）
- **status**: success
```

若日志文件不存在，先创建文件（包含一级标题 `# YYYY-MM-DD`），再追加 entry。

### Step 6：输出摘要

告知用户：
- 抓取了多少篇候选论文
- 推荐了多少篇（必读 / 值得看 / 可跳过 各多少）
- 已将 N 篇论文加入阅读列表（必读 X / 值得看 Y）
- 提示：可以用 `/paper-digest URL` 消化感兴趣的论文

## Guard

- **不自动生成论文笔记**：本 skill 只负责发现和推荐，不调用 paper-digest
- **不捏造论文信息**：所有内容必须来自抓取数据。不确定就标注"摘要未提及"
- **不覆盖已有推荐文件**：若 `Workbench/daily/YYYY-MM-DD.md` 已存在，先询问用户

## Verify

- [ ] `Workbench/daily/.candidates.json` 存在且非空
- [ ] `Workbench/daily/YYYY-MM-DD.md` 已创建
- [ ] 分流表中的 `[[#heading|display]]` 链接与详评的 `###` 标题完全匹配
- [ ] `Workbench/daily/.history.json` 已由脚本自动更新
- [ ] 必读和值得看论文已追加到 `Workbench/daily/reading_list.md`
- [ ] 日志已追加到 `Workbench/logs/YYYY-MM-DD.md`

## Examples

**示例 1：今日推荐**

```
今日论文推荐
```

执行过程：
1. 运行 `fetch_and_score.py --days 1 --history Workbench/daily/.history.json`（自动更新 history）
2. 读取 JSON，扫描 `Papers/` 匹配已有笔记
3. 生成点评，保存到 `Workbench/daily/2026-04-07.md`
4. 将必读和值得看论文写入 `Workbench/daily/reading_list.md`
5. 追加日志

**示例 2：过去一周**

```
过去一周论文推荐
```

执行过程：
1. 运行 `fetch_and_score.py --days 7 --history Workbench/daily/.history.json`（多天模式跳过 history 去重和更新）
2. 后续同示例 1，但 top_n = 30 * 7 = 210
