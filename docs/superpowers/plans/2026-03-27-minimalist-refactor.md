# Minimalist Refactor Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Propagate the SPEC.md minimalist philosophy to protocols and workbench structure — trim unused mechanics from protocols, consolidate queue files.

**Architecture:** Edit-in-place refactor of 3 protocol/workbench files, delete 4 queue files + create 1, update SPEC.md directory tree. Pure Markdown, no build system.

**Tech Stack:** Markdown, Git

**Spec:** `docs/superpowers/specs/2026-03-27-minimalist-refactor-design.md`

---

### Task 1: Trim agenda-protocol.md

**Files:**
- Modify: `references/agenda-protocol.md`

Remove "Copilot Mode" section (lines 119-122), "Sync with Memory" section (lines 135-152), and the "Active Direction Fields" redundant table (lines 79-101, which repeats what's already in the template above it). Keep: core template, Researcher Permissions, Supervisor Overrides, Integrity Rules.

- [ ] **Step 1: Replace agenda-protocol.md with trimmed version**

```markdown
# Agenda Protocol

This document defines the format and governance rules for `agenda.md` — the living research agenda that tracks active, paused, and abandoned directions.

---

## File Format

The agenda lives at `Workbench/agenda.md`. Below is the canonical template.

```markdown
---
last_updated: YYYY-MM-DD
updated_by: supervisor / <skill-name>
---

## Mission

One paragraph describing the long-term research mission and primary scientific question.
Researcher may propose evolution; Supervisor may edit directly.

---

## Active Directions

### [Direction Name]

- **priority**: high / medium / low
- **status**: exploring / validating / consolidating
- **origin**: supervisor-assigned / researcher-discovered / paper-inspired
- **hypothesis**: One-sentence falsifiable hypothesis
- **evidence**: [[Papers/xxx]], [[Experiments/xxx]] — or "none yet"
- **next_action**: Concrete next step
- **confidence**: 0.0-1.0

---

## Paused Directions

### [Direction Name]

- **priority**: high / medium / low
- **status**: paused
- **origin**: supervisor-assigned / researcher-discovered / paper-inspired
- **hypothesis**: One-sentence falsifiable hypothesis
- **evidence**: [[Papers/xxx]], [[Experiments/xxx]]
- **pause_reason**: Why this was paused
- **resume_condition**: What would trigger resuming
- **confidence**: 0.0-1.0

---

## Abandoned Directions

### [Direction Name]

- **abandoned_on**: YYYY-MM-DD
- **original_hypothesis**: What was believed when started
- **reason**: Why this was abandoned
- **lesson**: One-sentence takeaway
- **memory_ref**: [[Workbench/memory/failed-directions.md#heading]]

---

## Discussion Topics

### [Topic title] — [YYYY-MM-DD]

- **raised_by**: <skill-name> / researcher
- **context**: What prompted this topic
- **question**: What Researcher wants Supervisor's input on
- **related_direction**: Which direction this relates to
```

---

## Researcher Permissions

Researcher has full autonomy over the agenda. Like a PhD student, Researcher drives daily research independently.

| Action | Allowed? | Notes |
|---|---|---|
| Add a new direction (any priority) | Yes | Should be supported by evidence or reasoned argument |
| Change status (exploring -> validating -> consolidating) | Yes | Based on evidence state |
| Abandon a direction | Yes | Must write to `failed-directions.md` and log the lesson |
| Update `next_action`, `confidence`, `evidence` | Yes | Anytime |
| Move direction to Paused | Yes | Must populate `pause_reason` and `resume_condition` |
| Evolve Mission | Yes | May propose changes; Supervisor can always override |
| Merge duplicate directions | Yes | Log the merge in `evolution/changelog.md` |

---

## Supervisor Overrides

Supervisor edits to `agenda.md` take effect immediately and unconditionally. When a Supervisor edits the agenda:

- The `last_updated` and `updated_by` frontmatter fields should be updated.
- Researcher skills that run subsequently will read the current state as authoritative.
- Supervisor edits take precedence over any Researcher-proposed state.

---

## Integrity Rules

- Every active direction must have a non-empty `next_action`. If unclear, move to Paused.
- `confidence` values must be grounded in evidence. `exploring` with no evidence: 0.1-0.2. Multiple confirming papers: 0.7-0.8. Experimental confirmation needed for 0.9+.
- Discussion Topics do not block Researcher work — they are informational for next Supervisor check-in.
- Duplicate directions should be merged. Researcher merges autonomously and logs to `evolution/changelog.md`.
```

- [ ] **Step 2: Verify the file looks correct**

Run: `wc -l references/agenda-protocol.md`
Expected: ~90 lines (down from 162)

- [ ] **Step 3: Commit**

```bash
git add references/agenda-protocol.md
git commit -m "Trim agenda-protocol: remove Copilot Mode, Sync with Memory, redundant field table"
```

---

### Task 2: Trim memory-protocol.md

**Files:**
- Modify: `references/memory-protocol.md`

Replace the 4 repeated entry format blocks (lines 40-106, ~67 lines) with one canonical format + a compact per-file table. Keep: directory structure, promotion hierarchy, update rules.

- [ ] **Step 1: Replace memory-protocol.md with trimmed version**

```markdown
# Memory Protocol

This document defines how MindFlow stores, organizes, and promotes research knowledge. The memory system transforms raw observations into structured, reusable insights.

---

## Directory Structure

All persistent memory lives under `Workbench/memory/` as plain Markdown files.

```
Workbench/
  memory/
    patterns.md            # Cross-paper or cross-experiment patterns (not yet validated)
    insights.md            # Discovered insights (provisional -> validated)
    effective-methods.md   # Proven experiment and analysis strategies
    failed-directions.md   # Abandoned research directions and the reasons why
  logs/                    # Raw session logs (Level 0 input to memory)
  evolution/
    changelog.md           # Record of every Domain-Map update
```

| File | Purpose | Key Fields |
|---|---|---|
| `patterns.md` | Early-stage observations that recur across sources; feeds the promotion pipeline | observation, occurrences, confidence (low/medium), needs_verification |
| `insights.md` | Curated claims with evidence and confidence tracking; provisional -> validated | claim, evidence, confidence, source, impact, status |
| `effective-methods.md` | Strategies that worked, with context and caveats | context, method, evidence, pitfalls |
| `failed-directions.md` | What was tried and why it was abandoned; prevents re-exploring dead ends | original_hypothesis, evidence_against, lesson, related_directions |

---

## Entry Format

All memory files use the same heading-and-bullet structure. Entries are **append-only** — never edit past entries; add a new entry to supersede.

```markdown
### [YYYY-MM-DD] Entry title

- **field_1**: value
- **field_2**: value
- ...
```

Each file's specific fields are listed in the table above. Common rules:
- Use Obsidian `[[wikilinks]]` for all evidence references.
- Claims and hypotheses must be falsifiable and specific.
- `confidence` in `patterns.md` is capped at `medium` — validated patterns belong in `insights.md`.

---

## Insight Promotion Hierarchy

Knowledge is promoted upward through five levels as evidence accumulates.

```
Level 4  Domain Map           Domain-Map/{Name}.md
         Stable, integrated knowledge
              |  Researcher promotes when evidence sufficient
Level 3  Validated Insight    insights.md, status: validated
              |  >=2 independent sources confirm
Level 2  Provisional Insight  insights.md, status: provisional
              |  Pattern observed >=3 times independently
Level 1  Pattern              patterns.md
              |  memory-distill extracts from logs
Level 0  Raw Log              Workbench/logs/
```

### Promotion Rules

| Transition | Trigger | Who |
|---|---|---|
| L0 -> L1 | `memory-distill` processes session logs and extracts recurring observations | Researcher (via skill) |
| L1 -> L2 | Pattern appears in >=3 independent sources | Researcher (via skill) |
| L2 -> L3 | Provisional insight supported by >=2 independent evidence sources | Researcher (via skill) |
| L3 -> L4 | Researcher judges evidence sufficient for Domain Map integration. No numeric threshold — Researcher uses judgment. Logged to `evolution/changelog.md` | Researcher |

---

## Update Rules

1. **Append-only**: Never edit or delete existing entries. To supersede, append a new entry with updated date.

2. **Domain-Map logging**: Every L4 promotion must be logged to `Workbench/evolution/changelog.md`:

   ```markdown
   ### [YYYY-MM-DD] Domain Map updated: <map name>
   - **added**: <insight title>
   - **source**: [[Workbench/memory/insights.md#<heading>]]
   - **promoted_by**: <skill name or "human">
   ```

3. **Supervisor writes**: Supervisor may write directly to any memory file at any time without restrictions.

4. **Conflict handling**: If a new insight contradicts an existing validated one, create a new `provisional` entry noting the contradiction. Do not modify the old entry.
```

- [ ] **Step 2: Verify the file looks correct**

Run: `wc -l references/memory-protocol.md`
Expected: ~95 lines (down from 168)

- [ ] **Step 3: Commit**

```bash
git add references/memory-protocol.md
git commit -m "Trim memory-protocol: consolidate 4 format blocks into canonical format + table"
```

---

### Task 3: Consolidate queue files

**Files:**
- Delete: `Workbench/queue/reading.md`
- Delete: `Workbench/queue/review.md`
- Delete: `Workbench/queue/questions.md`
- Delete: `Workbench/queue/experiments.md`
- Create: `Workbench/queue.md`

- [ ] **Step 1: Create the consolidated queue.md**

```markdown
# Queue

> Supervisor 和 Researcher 都可以往这里添加条目。

## Reading

_队列为空。_

## Review

_队列为空。_

## Questions

_队列为空。_

## Experiments

_队列为空。_
```

- [ ] **Step 2: Delete old queue directory and files**

```bash
git rm Workbench/queue/reading.md Workbench/queue/review.md Workbench/queue/questions.md Workbench/queue/experiments.md
rmdir Workbench/queue
```

- [ ] **Step 3: Commit**

```bash
git add Workbench/queue.md
git commit -m "Consolidate 4 queue files into single Workbench/queue.md"
```

---

### Task 4: Update SPEC.md

**Files:**
- Modify: `SPEC.md`

Update the directory tree and Workbench table to reflect `queue.md` instead of `queue/`. Also commit the already-pending diff (naming clarifications, examples/, Reports/).

- [ ] **Step 1: Update the directory tree in SPEC.md**

In the directory tree (around line 91-96), change:

```
│   ├── queue/           #   待办队列（reading, review, questions）
```

to:

```
│   ├── queue.md         #   待办队列（Reading, Review, Questions, Experiments）
```

- [ ] **Step 2: Update the Workbench table in SPEC.md**

In the Workbench table (section 4.5, around line 185), change:

```
| `queue/` | 待办队列（reading、review、questions） |
```

to:

```
| `queue.md` | 待办队列（Reading、Review、Questions、Experiments） |
```

- [ ] **Step 3: Update memory-protocol.md directory tree reference**

In `references/memory-protocol.md`, the directory structure section references `queue/review.md`. This was already replaced in Task 2 — verify the new version does not reference `queue/`.

Run: `grep -n "queue/" references/memory-protocol.md`
Expected: No output (no references to old queue/ path)

- [ ] **Step 4: Commit**

```bash
git add SPEC.md
git commit -m "Update SPEC.md: queue/ -> queue.md, commit pending naming and structure cleanups"
```

---

### Task 5: Final verification

- [ ] **Step 1: Verify line counts**

```bash
wc -l references/agenda-protocol.md references/memory-protocol.md Workbench/queue.md SPEC.md
```

Expected:
- `agenda-protocol.md`: ~90 lines (was 162)
- `memory-protocol.md`: ~95 lines (was 168)
- `queue.md`: ~17 lines (was 4 files x 5 lines)
- `SPEC.md`: ~241 lines

- [ ] **Step 2: Verify no broken references to old queue/ path**

```bash
grep -r "queue/" Workbench/ references/ skills/ SPEC.md CLAUDE.md --include="*.md"
```

Expected: No output (all references updated)

- [ ] **Step 3: Verify git status is clean**

```bash
git status
```

Expected: Clean working tree, all changes committed.
