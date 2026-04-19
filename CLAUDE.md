## Precedence

When guidance conflicts, resolve in this order:

1. **Coding Principles (below)** — Andrej Karpathy's four rules always apply, regardless of framework.
2. **Framework / skill-suite flow** — if work is driven by gstack, superpower, or a similar suite, follow its prescribed flow next.
3. **The rest of this document** — planning, review, orchestration, and task-management conventions apply where the above two are silent.

## Coding Principles

Behavioral guardrails to reduce common LLM coding mistakes. Bias toward caution over speed; for trivial tasks, use judgment.

### 1. Think Before Coding
**Don't assume. Don't hide confusion. Surface tradeoffs.**
- State your assumptions explicitly. If uncertain, ask.
- If multiple interpretations exist, present them — don't pick silently.
- If a simpler approach exists, say so. Push back when warranted.
- If something is unclear, stop. Name what's confusing. Ask.

### 2. Simplicity First
**Minimum code that solves the problem. Nothing speculative.**
- No features beyond what was asked.
- No abstractions for single-use code.
- No "flexibility" or "configurability" that wasn't requested.
- No error handling for impossible scenarios.
- If you write 200 lines and it could be 50, rewrite it.
- Ask yourself: "Would a senior engineer say this is overcomplicated?" If yes, simplify.
- For non-trivial changes: pause and ask "is there a more elegant way?" If a fix feels hacky, implement the elegant solution instead.

### 3. Surgical Changes
**Touch only what you must. Clean up only your own mess.**
- Don't "improve" adjacent code, comments, or formatting.
- Don't refactor things that aren't broken.
- Match existing style, even if you'd do it differently.
- If you notice unrelated dead code, mention it — don't delete it.
- Remove imports/variables/functions that YOUR changes made unused. Don't remove pre-existing dead code unless asked.
- The test: every changed line should trace directly to the user's request.

### 4. Goal-Driven Execution & Verification
**Define success criteria. Loop until verified.**

Transform tasks into verifiable goals:
- "Add validation" → "Write tests for invalid inputs, then make them pass"
- "Fix the bug" → "Write a test that reproduces it, then make it pass"
- "Refactor X" → "Ensure tests pass before and after"

For multi-step tasks, state a brief plan:
```
1. [Step] → verify: [check]
2. [Step] → verify: [check]
```

Before marking a task complete:
- Never mark done without proving it works. Run tests, check logs, demonstrate correctness.
- Diff behavior between main and your changes when relevant.
- Ask: "Would a staff engineer approve this?"

## Planning & Review Workflow

### 1. Plan-First Development
- For ANY non-trivial task (3+ steps or architectural decisions), create a plan in `tasks/plan.md` before coding
- Enter plan mode to draft the plan, then present it for user review
- If something goes sideways mid-implementation, STOP and re-plan immediately
- Write detailed specs upfront to reduce ambiguity

### 2. Iterating on Plans with Inline Comments
When the user adds inline comments to a plan, follow this protocol:

**Comment markers the user will use:**
- `> **[Q]:**` — A question that needs answering before proceeding
- `> **[X]:**` — Rejection. This part needs to be reworked
- `> **[!]:**` — Important constraint or requirement to incorporate
- `<!-- TODO: ... -->` — A note for later consideration

**How to respond:**
1. Read the plan file and identify all comment markers
2. Address every `[Q]` with a direct answer or options
3. Rework every section marked with `[X]` based on the feedback
4. Incorporate all `[!]` constraints into the revised plan
5. Preserve `<!-- TODO -->` comments unless explicitly resolved
6. Produce a clean revised plan — remove addressed `[Q]` and `[X]` markers
7. Commit each revision so the full iteration history is in git

**The plan is not final until all comment markers are resolved and the user explicitly approves.**

## Workflow Orchestration

### 1. Subagent Strategy
- Use subagents liberally to keep main context window clean
- Offload research, exploration, and parallel analysis to subagents
- For complex problems, throw more compute at it via subagents
- One task per subagent for focused execution

### 2. Self-Improvement Loop
- After ANY correction from the user: update `tasks/lessons.md` with the pattern
- Write rules for yourself that prevent the same mistake
- Ruthlessly iterate on these lessons until mistake rate drops
- Review lessons at session start for relevant project

### 3. Autonomous Bug Fixing
- When given a bug report: just fix it. Don't ask for hand-holding
- Point at logs, errors, failing tests — then resolve them
- Zero context switching required from the user
- Go fix failing CI tests without being told how

## Task Management

1. **Plan First**: Write plan to `tasks/plan.md` with checkable items
2. **Review & Iterate**: User comments inline using `[Q]`, `[X]`, `[!]` markers — iterate until approved
3. **Track Progress**: Mark items complete as you go
4. **Explain Changes**: High-level summary at each step
5. **Document Results**: Add review section to `tasks/plan.md`
6. **Capture Lessons**: Update `tasks/lessons.md` after corrections

## gstack
Use /browse from gstack for all web browsing. Never use mcp__claude-in-chrome__* tools.

Available skills: /office-hours, /plan-ceo-review, /plan-eng-review, /plan-design-review, /design-consultation, /review, /ship, /land-and-deploy, /canary, /benchmark, /browse, /qa, /qa-only, /design-review, /setup-browser-cookies, /setup-deploy, /retro, /investigate, /document-release, /codex, /cso, /autoplan, /careful, /freeze, /guard, /unfreeze, /gstack-upgrade.

---

**These guidelines are working if:** fewer unnecessary changes in diffs, fewer rewrites due to overcomplication, and clarifying questions come before implementation rather than after mistakes.
