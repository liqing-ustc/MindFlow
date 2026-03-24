# 🔬 MindFlow

An Obsidian-based research workspace for building a **human-AI collaborative research pipeline** from paper reading to idea generation to experiment validation.

基于 Obsidian 的 AI 研究知识管理工作区，构建从论文阅读到 idea 生成再到实验验证的 **human-AI 协作研究流水线**。

## 🎯 Vision

论文太多，靠人工逐篇阅读不现实。这个项目的核心目标是让人和 AI 更好地配合——**人专注于创造性工作，AI 负责重复性、工程性的事情**，共同构建一个 personalized knowledge space。

具体来说，我们希望实现一个逐步递进的协作流程：

1. **AI 阅读与总结** — 论文太多读不过来，让 AI 批量阅读、生成结构化笔记
2. **人工精炼与补充** — AI 总结并不完美，需要人来修改、补充个人见解
3. **交互式讨论** — 人和 AI 围绕论文内容深入讨论，碰撞想法
4. **知识网络构建** — 逐步积累形成 personalized knowledge space（人和 AI 共享）
5. **智能论文筛选** — AI 基于已有知识网络，主动推荐相关论文 *(planned)*
6. **Research Idea 生成** — 基于知识积累，人和 AI 讨论产出可行的研究想法 *(planned)*
7. **代码实现与实验验证** — AI 将 idea 转化为代码，跑实验验证 *(planned)*

![Obsidian Demo](Attachments/obsidian-demo.png)

## ✨ Features

- **Paper Notes** — 结构化论文笔记模板（含 Mermaid Mind Map）
- **Research Ideas** — 灵感记录，双向链接到相关论文
- **Project Tracking** — 研究项目进展追踪
- **Literature Survey** — 按主题整理多篇论文对比
- **Meeting Notes** — 会议/讨论记录
- **AI Workflow** — 用 Claude Code 或其他 AI 工具自动生成论文笔记

## 🚀 Getting Started

1. Clone this repo and open it as an Obsidian vault
2. Obsidian settings are pre-configured (templates, attachments, link format)
3. Start creating notes using templates: `Ctrl/Cmd + P` → "Templates: Insert template"

### Prerequisites

- [Obsidian](https://obsidian.md/) (free)
- [Claude Code](https://claude.ai/code) (optional, for AI-assisted paper reading)

## 📁 Structure

| Folder | Purpose | Naming |
|--------|---------|--------|
| `Papers/` | 论文笔记 | `AuthorYear-ShortTitle.md` |
| `Ideas/` | 研究灵感 | 自由命名 |
| `Projects/` | 项目追踪 | 项目名称 |
| `Topics/` | 主题综述 | 主题名称 |
| `Meetings/` | 会议记录 | `YYYY-MM-DD-Description.md` |
| `Daily/` | 每日日志 | `YYYY-MM-DD.md` |
| `Templates/` | Obsidian 模板 | — |
| `Attachments/` | 附件 | — |
| `Resources/` | AI Prompts 等参考资料 | — |

## 📝 Templates

| Template | Purpose |
|----------|---------|
| Paper | 论文笔记（含 YAML frontmatter、Mind Map、Connections） |
| Idea | 研究灵感（status: raw → developing → validated → archived） |
| Project | 项目追踪（status: planning → active → paused → completed） |
| Topic | 主题综述/文献对比（含论文对比表格） |
| Meeting | 会议记录（含 Action Items） |
| Daily | 每日研究日志 |

## 🤖 AI-Assisted Paper Reading

### With Claude Code (recommended)

Tell Claude Code a paper name or link, it will automatically fetch, summarize, and save structured notes:

```
总结论文 pi0
```

Claude Code will:
1. Fetch paper content via web search / URL
2. Generate notes following the Paper template
3. Save to `Papers/AuthorYear-ShortTitle.md`

### With other AI tools

Copy the prompt from [Resources/AI-Prompts.md](Resources/AI-Prompts.md), paste it along with the paper info into any AI chat, then paste the output into Obsidian.

## 🏷️ Tags

Flat tags using canonical English terms:

- **Domain**: `LLM`, `CV`, `RL`, `multimodal`, `diffusion`
- **Method**: `transformer`, `RLHF`, `distillation`, `RAG`
- **Venue** (optional): `NeurIPS`, `ICML`, `ICLR`, `ACL`, `CVPR`
- **Task**: `text-generation`, `image-classification`, `alignment`

## 🔗 Linking Strategy

Notes are connected via `[[wikilinks]]` to form a knowledge graph:

- Paper ↔ Paper (related work)
- Idea → Paper (inspiration source)
- Project → Paper + Idea (foundations)
- Topic → Papers (literature survey)
- Meeting → Project / Paper (follow-ups)

Use Obsidian's **Graph View** to visualize your research knowledge network.

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=liqing-ustc/MindFlow&type=Date)](https://star-history.com/#liqing-ustc/MindFlow&Date)

If you find this useful, please give it a star 🌟! It helps others discover this project.

**Author**: [Qing Li](https://liqing.io/)

## 📄 License

Feel free to use this as a template for your own research workspace.
