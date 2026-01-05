---
name: tidb-cloud-e2e-validation
description: >
  End-to-end feature validation for TiDB Cloud console UI. Use this skill when:
  (1) Validating new or existing console features work correctly,
  (2) Testing UI workflows from end-user perspectives (new user or power user),
  (3) Applying consistent UX review rubric across features,
  (4) Creating validation reports for feature releases.
  This skill simulates a real user operating the TiDB Cloud console through Chrome.
compatibility: Designed for Claude Code (or similar products)
---

# TiDB Cloud E2E Feature Validation

## Overview

This skill validates TiDB Cloud features by simulating real user behavior through the console UI. It focuses on:
1. **Functional Validation**: Walk through features end-to-end as a real user would
2. **UX Review**: Evaluate the experience using a consistent rubric from different user perspectives

All validation is performed through the UI only—no API calls or backend verification. This ensures we test exactly what users experience.

## Prerequisites

- Claude Code with Chrome integration enabled (`claude --chrome`)
- Chrome browser with Claude in Chrome extension installed
- Access to target environment (staging.tidbcloud.com or tidbcloud.com)
- User authentication (will pause for manual login if needed)

---

## User Personas

All validations should be performed from one or both of these perspectives:

### Happy Path Persona (New User)
- **Context**: First-time user, minimal prior knowledge of TiDB or TiDB Cloud
- **Behavior**: Follows UI prompts, reads tooltips/docs, expects guided experience
- **Goals**: Complete the task with minimal friction, understand what they're doing
- **Questions to answer**:
  - Can they complete the task without external documentation?
  - Are error messages helpful and actionable?
  - Is the terminology understandable to someone new to TiDB Cloud?

### Power User Persona
- **Context**: Experienced user, knows exactly what they want
- **Behavior**: Skips tutorials, expects efficiency
- **Goals**: Complete the task as quickly as possible, access advanced options
- **Questions to answer**:
  - Can they complete the task without unnecessary clicks?
  - Are advanced options accessible without digging?
  - Does the UI remember their preferences?

---

## Core Validation Workflow

### Phase 1: Setup & Context
1. Open Chrome and navigate to the target environment
2. If login required, pause and request user to authenticate
3. Identify the feature to validate and load the appropriate reference file:
   - **Cluster Management**: `references/cluster-management.md`
   - **TiCDC/Changefeeds**: `references/ticdc-validation.md`
   - **Navigation Patterns**: `references/navigation-patterns.md`
4. Determine which persona(s) to use for this validation

### Phase 2: Functional Validation
1. Execute the feature workflow end-to-end as a real user would
2. Observe UI feedback and confirm expected outcomes:
   - Success messages appear as expected
   - UI state updates correctly (e.g., new resource appears in list)
   - Status indicators show expected values
3. Test error scenarios by triggering validation errors or edge cases
4. Note any unexpected behavior or confusing UI states

### Phase 3: UX Review
Apply the UX Review Rubric below to score the experience.

### Phase 4: Reporting
1. Generate validation report using `assets/report-template.md`
2. Document issues with screenshots and severity ratings
3. Provide overall pass/fail with evidence
4. List actionable recommendations

---

## UX Review Rubric

Score each dimension 1-5 (1=Poor, 3=Acceptable, 5=Excellent)

### 1. Discoverability (Can users find the feature?)
| Score | Criteria |
|-------|----------|
| 1 | Feature hidden, requires documentation to find |
| 3 | Feature findable with some exploration |
| 5 | Feature obviously located, matches mental model |

**Check**: Navigation path, menu placement, search functionality

### 2. Clarity (Do users understand what they're doing?)
| Score | Criteria |
|-------|----------|
| 1 | Confusing terminology, no explanation of options |
| 3 | Some terms explained, basic guidance provided |
| 5 | Clear labels, helpful tooltips, context-aware help |

**Check**: Labels, tooltips, inline help, terminology consistency

### 3. Efficiency (Can users complete tasks quickly?)
| Score | Criteria |
|-------|----------|
| 1 | Excessive clicks, no shortcuts, redundant steps |
| 3 | Reasonable flow, some optimization possible |
| 5 | Minimal steps, smart defaults, keyboard accessible |

**Check**: Click count, form defaults, bulk operations, keyboard shortcuts

### 4. Feedback (Does the UI communicate state clearly?)
| Score | Criteria |
|-------|----------|
| 1 | No feedback, unclear if action worked |
| 3 | Basic feedback, some loading/success indicators |
| 5 | Rich feedback, progress indicators, clear status |

**Check**: Loading states, success/error messages, progress indicators

### 5. Error Handling (Does the UI help users recover?)
| Score | Criteria |
|-------|----------|
| 1 | Cryptic errors, no recovery path |
| 3 | Understandable errors, manual recovery needed |
| 5 | Clear errors with suggested fixes, easy retry |

**Check**: Error messages, validation timing, recovery options

### 6. Consistency (Does the UI match other parts of the console?)
| Score | Criteria |
|-------|----------|
| 1 | Inconsistent patterns, different from rest of UI |
| 3 | Mostly consistent, minor variations |
| 5 | Fully consistent with design system and patterns |

**Check**: Component usage, terminology, navigation patterns

---

## Templates

Use templates from `assets/` for validation output:

| Template | Purpose |
|----------|---------|
| `assets/report-template.md` | Full validation report with all findings |
| `assets/checklist-template.md` | Quick checklist to guide validation process |

---

## Feature-Specific References

Load the appropriate reference file for detailed validation steps:

| Feature | Reference File |
|---------|----------------|
| Cluster Creation/Management | `references/cluster-management.md` |
| TiCDC / Changefeeds | `references/ticdc-validation.md` |
| Common Navigation | `references/navigation-patterns.md` |

---

## Usage Examples

### Example 1: Validate Cluster Creation (Happy Path)
```
User: Validate the cluster creation flow for a new user
Assistant: I'll validate cluster creation from the Happy Path persona perspective...
[Loads references/cluster-management.md]
[Navigates through cluster creation as a new user would]
[Scores UX rubric, documents findings]
[Generates report]
```

### Example 2: Validate TiCDC Setup (Power User)
```
User: Test TiCDC changefeed creation as a power user
Assistant: I'll validate TiCDC from the Power User persona perspective...
[Loads references/ticdc-validation.md]
[Tests efficient paths, advanced options]
[Confirms UI shows changefeed status as expected]
[Generates report with efficiency focus]
```

### Example 3: Full Feature Validation
```
User: Do a complete validation of backup/restore
Assistant: I'll perform full validation with both personas...
[Runs through as Happy Path user first]
[Runs through as Power User second]
[Compares experiences, generates comprehensive report]
```
