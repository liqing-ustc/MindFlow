# MindFlow Minimalist Refactor

**Date**: 2026-03-27
**Status**: Approved
**Goal**: Propagate SPEC.md's minimalist philosophy (~600→~240 line simplification) to protocols and workbench structure.

## Decisions

| Area | Decision |
|------|----------|
| Memory hierarchy (L0-L4) | Keep as-is |
| Queue files (4 separate) | Merge into 1 file |
| Protocols (4 files) | Keep separate, trim each |
| Skills (4 files) | Leave alone |
| dist/website/docs/superpowers | Ignore (out of scope) |

## Changes

### 1. Trim agenda-protocol.md (~162 → ~90 lines)

**Remove:**
- "Copilot Mode" section (unused, no skill references it)
- "Sync with Memory" mechanics (premature -- no active directions exist)
- Verbose template examples (Workbench/agenda.md is self-documenting)

**Keep:**
- Core agenda.md format/template
- Researcher Permissions table
- Supervisor Override rules
- Integrity rules

### 2. Trim memory-protocol.md (~168 → ~120 lines)

**Remove:**
- Repeated per-file format blocks (currently defines field-by-field format 4x for patterns/insights/effective-methods/failed-directions)

**Replace with:**
- One canonical entry format block
- Compact table: File | What goes in it | Promotion trigger

**Keep:**
- L0-L4 hierarchy unchanged
- Promotion rules
- Append-only semantics
- Update rules

### 3. Queue consolidation

**Delete:**
- `Workbench/queue/reading.md`
- `Workbench/queue/review.md`
- `Workbench/queue/questions.md`
- `Workbench/queue/experiments.md`

**Create** `Workbench/queue.md` with sections: Reading, Review, Questions, Experiments.

### 4. SPEC.md updates

- Commit pending diff (naming clarifications, examples/, Reports/)
- Update directory tree: `queue/` → `queue.md`
- Update Workbench table: reflect single queue file

### 5. CLAUDE.md

No changes needed -- delegates to SPEC.md for structure details.

## Impact

- ~120 lines trimmed from protocols
- 4 files deleted, 1 created (queue)
- SPEC.md updated to match
- Skills, templates, memory, workbench structure: untouched
