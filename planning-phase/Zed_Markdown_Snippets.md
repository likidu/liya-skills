# Add Zed Markdown Snippets to quickly comment on the plan

## Zed Snippets

Zed supports custom snippets. Add these to your snippets config:

**File:** `~/.config/zed/snippets/markdown.json`

```json
{
  "Plan Question": {
    "prefix": "pq",
    "body": "> **[Q]:** $0",
    "description": "Plan review question"
  },
  "Plan Reject": {
    "prefix": "px",
    "body": "> **[X]:** $0",
    "description": "Plan review rejection"
  },
  "Plan Constraint": {
    "prefix": "pi",
    "body": "> **[!]:** $0",
    "description": "Plan review constraint"
  },
  "Plan Todo": {
    "prefix": "pt",
    "body": "<!-- TODO: $0 -->",
    "description": "Plan todo note"
  }
}
```

## Zed Tasks (For Bulk Review)

If you want to scan a plan for all unresolved markers, add to `.zed/tasks.json`:

```json
[
  {
    "label": "Find plan comments",
    "command": "grep -n '\\[Q\\]:\\|\\[X\\]:\\|\\[!\\]:\\|<!-- TODO' tasks/plan.md",
    "use_new_terminal": false
  }
]
```
