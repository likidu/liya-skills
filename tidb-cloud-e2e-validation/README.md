# TiDB Cloud E2E Validation Skill

End-to-end feature validation for TiDB Cloud console UI, simulating real user behavior with consistent UX review.

## Purpose

This skill validates TiDB Cloud features by simulating how real users interact with the console:
1. **Walking through features** - Operating the UI exactly as a user would
2. **Applying UX rubric** - Consistent evaluation across all features using two personas:
   - **Happy Path**: New user with minimal context
   - **Power User**: Experienced user seeking efficiency

All validation is performed through the UI only—no API calls or backend verification.

## Directory Structure

```
tidb-cloud-e2e-validation/
├── SKILL.md                           # Core validation workflow & UX rubric
├── README.md                          # This file
├── references/
│   ├── cluster-management.md          # Cluster creation/management validation
│   ├── project-management.md          # Project/org structure validation
│   ├── navigation-patterns.md         # Common UI navigation patterns
│   └── ui-visual-checklist.md         # Visual/layout issues checklist (IMPORTANT)
├── assets/
│   ├── report-template.md             # Validation report template
│   └── checklist-template.md          # Quick validation checklist
└── reports/                           # Generated validation reports
```

## Usage

### Prerequisites
- Claude Code with Chrome integration (`claude --chrome`)
- Chrome browser with Claude extension
- Access to tidbcloud.com or staging.tidbcloud.com

### Running a Validation

```
# Validate cluster creation as a new user
"Validate the cluster creation flow using the Happy Path persona"

# Full validation with both personas
"Do a complete validation of [feature] with both personas"
```

## Adding New Features

1. Create a new reference file: `references/[feature-name].md`
2. Follow the structure in existing references:
   - Feature overview
   - Step-by-step validation for each persona
   - UI state verification steps
   - Error scenarios to test
   - UX focus areas
3. Update the feature table in `SKILL.md`

## UX Review Rubric

All features are scored on 6 dimensions (1-5 scale):

| Dimension | What it measures |
|-----------|------------------|
| Discoverability | Can users find the feature? |
| Clarity | Do users understand what they're doing? |
| Efficiency | Can users complete tasks quickly? |
| Feedback | Does the UI communicate state clearly? |
| Error Handling | Does the UI help users recover from errors? |
| Consistency | Does the UI match other parts of the console? |

## Visual & Layout Checks

**IMPORTANT**: Every validation should include visual/layout checks from `references/ui-visual-checklist.md`:

| Check Category | Common Issues |
|----------------|---------------|
| Element Overlapping | Help icons covering buttons, tooltips cut off |
| Interaction States | Selected+hover thick borders, incorrect disabled colors |
| Cross-Page Consistency | Colors differ between list/create pages, dropdown menu inconsistency |
| Empty/Edge States | Pagination on empty tables, long text breaking layouts |
| Platform Issues | Double scroll bars on Windows Chrome |

These visual issues are often missed but significantly impact user experience.

## Output

Validations produce:
- Structured report using `assets/report-template.md`
- UX scores for each persona
- Documented issues with screenshots
- Actionable recommendations
