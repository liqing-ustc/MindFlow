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
