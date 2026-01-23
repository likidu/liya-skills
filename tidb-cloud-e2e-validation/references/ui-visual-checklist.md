# UI Visual Checklist

This checklist covers common visual and layout issues to check during any validation. These issues are often missed but significantly impact user experience.

---

## 1. Element Overlapping

**Priority: HIGH** - Overlapping elements can block user interactions.

### What to Check
- [ ] **Floating help icons** (?) don't overlap action buttons (Create, Submit, Save)
- [ ] **FAB buttons** (floating action buttons) don't cover content when scrolling
- [ ] **Sticky headers/footers** don't overlap form fields or buttons
- [ ] **Tooltips** don't get cut off by viewport edges
- [ ] **Dropdown menus** don't extend beyond viewport
- [ ] **Modal dialogs** are properly centered and don't overlap navigation

### How to Test
1. Scroll to bottom of forms to check footer overlaps
2. Open dropdowns near page edges
3. Hover over elements to trigger tooltips near edges
4. Resize browser window to smaller sizes

### Common Issues Found
| Issue | Location | Severity |
|-------|----------|----------|
| Help center icon overlaps Create button | Cluster creation page footer | High |
| Tooltip cut off at right edge | Various hover states | Medium |

---

## 2. Alignment & Spacing

**Priority: MEDIUM** - Misalignment creates unprofessional appearance.

### What to Check
- [ ] **Card heights** are consistent when cards contain different amounts of content
- [ ] **Pricing text** aligns at bottom across plan/tier cards
- [ ] **Table columns** have consistent alignment (numbers right-aligned, text left-aligned)
- [ ] **Form labels** align consistently
- [ ] **Button groups** have equal spacing
- [ ] **Icon + text** combinations are vertically centered

### How to Test
1. Compare similar elements side-by-side
2. Look for "jagged" edges where elements should align
3. Check that "Starts from $X/month" text aligns across plan cards

### Common Issues Found
| Issue | Location | Severity |
|-------|----------|----------|
| Plan card pricing not bottom-aligned | Cluster creation - plan selection | Low |
| "POWERED BY" line missing on Dedicated causes misalignment | Cluster creation | Low |

---

## 3. Interaction States

**Priority: HIGH** - Incorrect states confuse users about what's clickable.

### What to Check
- [ ] **Hover state** is visible on all clickable elements
- [ ] **Selected + hover** combination doesn't create overly thick borders
- [ ] **Disabled state** uses correct color (typically lighter/grayed)
- [ ] **Focus state** is visible for keyboard navigation
- [ ] **Active/pressed state** provides feedback
- [ ] **Loading state** disables interactions appropriately

### How to Test
1. Hover over each interactive element
2. Select an item, then hover over it again
3. Tab through form fields to check focus states
4. Look for disabled elements and verify they look disabled

### Common Issues Found
| Issue | Location | Severity |
|-------|----------|----------|
| Selected + hover creates double-thick border | Plan tier cards | Medium |
| Disabled text color too dark (should use carbon6) | Dropdown menu items | Low |

---

## 4. Color Consistency

**Priority: HIGH** - Inconsistent colors break visual hierarchy and brand identity.

### What to Check
- [ ] **Plan/tier colors** match between creation page and list page
- [ ] **Status colors** are consistent (green=active, yellow=warning, red=error)
- [ ] **Badge colors** match their meaning across pages
- [ ] **Link colors** are consistent
- [ ] **Error colors** match design system

### How to Test
1. Navigate between related pages and compare colors
2. Check that Essential tier color on list matches creation page
3. Verify status indicators use same colors everywhere

### Common Issues Found
| Issue | Location | Severity |
|-------|----------|----------|
| Essential plan color differs between creation and list pages | My TiDB list vs Create page | Medium |
| Plan badge colors inconsistent | Various locations | Medium |

---

## 5. Empty & Edge States

**Priority: MEDIUM** - Poor empty states confuse users.

### What to Check
- [ ] **Empty tables** don't show pagination controls
- [ ] **Empty states** have helpful messages and CTAs
- [ ] **Loading states** show appropriate indicators
- [ ] **Error states** are styled consistently
- [ ] **Long text** truncates appropriately with ellipsis
- [ ] **Long names** don't break layouts

### How to Test
1. View pages with no data
2. Enter very long text in name fields
3. Check tables before any items are created

### Common Issues Found
| Issue | Location | Severity |
|-------|----------|----------|
| Pagination shown on empty table | My TiDB list when empty | Low |
| Very long cluster names break card layout | Cluster list | Medium |

---

## 6. Cross-Page Consistency

**Priority: HIGH** - Inconsistencies between pages confuse users.

### What to Check
- [ ] **Dropdown menus** have same options for similar items across pages
- [ ] **Action buttons** appear in same order across pages
- [ ] **Column headers** use same names for same data
- [ ] **Filters** work consistently across list views
- [ ] **Sort options** are consistent

### How to Test
1. Compare dropdown menus on different plan types
2. Check that Premium and Essential have same actions where applicable
3. Verify filters on different list pages work the same way

### Common Issues Found
| Issue | Location | Severity |
|-------|----------|----------|
| Premium dropdown has different options than Essential | My TiDB list action menus | Medium |
| Restore options shown but not supported for all plans | Create Resource menu | High |

---

## 7. Platform-Specific Issues

**Priority: MEDIUM** - Different platforms may render differently.

### What to Check
- [ ] **Scroll bars** appear correctly (especially on Windows)
- [ ] **Font rendering** is acceptable
- [ ] **Form inputs** style correctly across browsers
- [ ] **No double scroll bars** appear

### How to Test
1. Test on Windows Chrome specifically
2. Check for nested scrollable areas
3. Resize window to trigger scroll bars

### Common Issues Found
| Issue | Location | Severity |
|-------|----------|----------|
| Double scroll bar appears on Windows Chrome | Cluster creation page | Medium |

---

## 8. Feature Availability Indicators

**Priority: HIGH** - Users need to know what features are available to them.

### What to Check
- [ ] **Disabled features** have clear indication of why they're disabled
- [ ] **Plan-specific features** show which plan is required
- [ ] **Unavailable options** have tooltips explaining requirements
- [ ] **Beta/Preview badges** are shown for experimental features

### How to Test
1. Check disabled buttons/options for tooltips
2. Look for features that vary by plan
3. Try to access features not available for current plan

### Common Issues Found
| Issue | Location | Severity |
|-------|----------|----------|
| Dedicated tier disabled with no explanation | Cluster creation plan selection | High |
| Restore options visible but not available for Starter/Essential | Create Resource menu | High |

---

## 9. Icon & Typography

**Priority: LOW** - Subtle but affects polish.

### What to Check
- [ ] **Icon weight** is consistent (same stroke width)
- [ ] **Icon size** is consistent in similar contexts
- [ ] **Font weights** are consistent for similar elements
- [ ] **Text colors** for labels/values are consistent

### How to Test
1. Compare icons across the page
2. Check that all section headers use same font weight

### Common Issues Found
| Issue | Location | Severity |
|-------|----------|----------|
| Icons too heavy (should use carbon8, 1px bold) | Navigation sidebar | Low |

---

## Quick Validation Checklist

Use this abbreviated checklist for every validation:

```
[ ] No overlapping elements (especially floating buttons/icons)
[ ] Colors consistent with other pages showing same data
[ ] Selected + hover doesn't create visual glitch
[ ] Empty states don't show pagination
[ ] Disabled items have correct styling and explanations
[ ] Dropdown menus consistent across similar items
[ ] No platform-specific scroll issues
[ ] Plan-specific features clearly indicated
```

---

## Reporting Template

When reporting visual issues, include:

```
**Issue**: [Brief description]
**Location**: [Page > Section > Element]
**Steps to Reproduce**:
1. Navigate to...
2. Perform action...
**Expected**: [What should happen]
**Actual**: [What actually happens]
**Severity**: [High/Medium/Low]
**Screenshot**: [Capture the issue]
```
