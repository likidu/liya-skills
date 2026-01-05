# E2E Validation Checklist

## Feature: _______________
## Date: _______________
## Environment: _______________

---

## Pre-Validation Setup

- [ ] Chrome launched with Claude integration
- [ ] Logged into target environment
- [ ] Feature reference file loaded (if available)
- [ ] Persona selected: [ ] Happy Path [ ] Power User [ ] Both

---

## Navigation Validation

- [ ] Feature accessible from expected location
- [ ] Breadcrumbs display correctly
- [ ] Back navigation works
- [ ] URL is shareable/bookmarkable

**Navigation clicks to reach feature**: ___

---

## Functional Validation

### Happy Path
- [ ] Primary workflow completes successfully
- [ ] Expected result achieved
- [ ] UI reflects correct state after completion

### Error Handling
- [ ] Invalid input shows clear error
- [ ] Network error handled gracefully
- [ ] Recovery path available
- [ ] Error messages are actionable

### Edge Cases
- [ ] Empty state handled
- [ ] Maximum limits tested
- [ ] Concurrent operations (if applicable)
- [ ] Permissions/access controls work

---

## UX Rubric Scores

Rate each 1-5 (1=Poor, 3=Acceptable, 5=Excellent)

| Dimension | Happy Path | Power User | Notes |
|-----------|------------|------------|-------|
| Discoverability | /5 | /5 | |
| Clarity | /5 | /5 | |
| Efficiency | /5 | /5 | |
| Feedback | /5 | /5 | |
| Error Handling | /5 | /5 | |
| Consistency | /5 | /5 | |

**Happy Path Average**: ___/5
**Power User Average**: ___/5

---

## UI Consistency Checks

- [ ] Buttons match design system
- [ ] Forms follow standard patterns
- [ ] Status colors are consistent
- [ ] Loading states present
- [ ] Modal behavior correct
- [ ] Responsive layout (if applicable)

---

## Accessibility Quick Check

- [ ] Tab navigation works
- [ ] Focus indicators visible
- [ ] Button/link labels descriptive
- [ ] Color not sole indicator

---

## Issues Found

### Critical (Blocks usage)
1. 

### Major (Degrades experience)
1. 

### Minor (Polish items)
1. 

---

## Screenshots Captured

- [ ] Initial/empty state
- [ ] Form/configuration state
- [ ] Loading/progress state
- [ ] Success state
- [ ] Error state
- [ ] Key issue screenshots

---

## Summary

**Overall Result**: [ ] PASS [ ] FAIL [ ] PASS WITH ISSUES

**Key Findings**:
1. 
2. 
3. 

**Top Recommendations**:
1. 
2. 

---

*Checklist completed by TiDB Cloud E2E Validation Skill*
