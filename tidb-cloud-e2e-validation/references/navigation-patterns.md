# TiDB Cloud Navigation Patterns

Common UI navigation patterns and elements across TiDB Cloud console. Use this reference to validate consistency.

## Global Navigation Structure

### Top Navigation Bar
- **Logo/Home**: Returns to dashboard
- **Organization Selector**: Switch between organizations (if multiple)
- **Project Selector**: Switch between projects
- **User Menu**: Account settings, logout, help

### Left Sidebar (Primary Navigation)
Expected sections:
- Dashboard/Overview
- Clusters
- Data Services (if applicable)
- Billing
- Settings

### Breadcrumbs
- Should show: Organization > Project > Feature > Detail
- Each level should be clickable
- Current page should not be a link

---

## Common UI Patterns

### List Views
All list views should have:
- [ ] Search/filter capability
- [ ] Sort options
- [ ] Pagination or infinite scroll
- [ ] Empty state message
- [ ] Create/Add button

### Detail Views
All detail pages should have:
- [ ] Back navigation (breadcrumb or button)
- [ ] Title with resource name
- [ ] Status indicator
- [ ] Actions menu or buttons
- [ ] Tabbed sections for complex resources

### Forms
All forms should have:
- [ ] Clear field labels
- [ ] Required field indicators
- [ ] Inline validation
- [ ] Submit and Cancel buttons
- [ ] Loading state on submit
- [ ] Success/error feedback

### Modals/Dialogs
All modals should have:
- [ ] Clear title
- [ ] Close button (X)
- [ ] Escape key closes modal
- [ ] Click outside closes (for non-critical)
- [ ] Focus trapped inside modal
- [ ] Confirm/Cancel for destructive actions

---

## Status Indicators

### Cluster Status
| Status | Color | Meaning |
|--------|-------|---------|
| Available | Green | Cluster is ready |
| Creating | Blue/Yellow | Cluster being created |
| Modifying | Blue/Yellow | Changes in progress |
| Paused | Gray | Cluster is paused |
| Failed | Red | Error state |

### Component Status
| Status | Color | Meaning |
|--------|-------|---------|
| Running | Green | Component active |
| Stopped | Gray | Component stopped |
| Error | Red | Component failed |

---

## Action Patterns

### Destructive Actions
For delete/destroy operations:
- [ ] Requires confirmation
- [ ] Shows what will be deleted
- [ ] Requires typing resource name (for critical resources)
- [ ] Clear warning about irreversibility
- [ ] Different button color (red/danger)

### Long-Running Actions
For operations that take time:
- [ ] Immediate feedback that action started
- [ ] Progress indicator or spinner
- [ ] Status updates during operation
- [ ] Clear completion indication
- [ ] Ability to navigate away (action continues)

---

## Keyboard Navigation

### Expected Shortcuts
- `Tab`: Move between interactive elements
- `Enter`: Activate buttons/links
- `Escape`: Close modals/dropdowns
- `Arrow keys`: Navigate menus/lists

### Accessibility Checks
- [ ] All interactive elements focusable
- [ ] Focus visible indicator
- [ ] Logical tab order
- [ ] Screen reader labels present

---

## Error States

### Page-Level Errors
- [ ] Clear error message
- [ ] Suggested action to resolve
- [ ] Retry option if applicable
- [ ] Contact support link for unrecoverable

### Field-Level Errors
- [ ] Error appears near the field
- [ ] Red color/icon indicator
- [ ] Clear description of the issue
- [ ] Appears on blur or submit (not while typing)

### Empty States
- [ ] Friendly message explaining emptiness
- [ ] Call to action to create/add first item
- [ ] Link to documentation if helpful

---

## Loading States

### Initial Page Load
- [ ] Skeleton loaders or spinners
- [ ] Partial content shown if possible
- [ ] No content flash/jump

### Action Loading
- [ ] Button shows loading state
- [ ] Form disabled during submission
- [ ] Clear indication something is happening

---

## Consistency Checklist

When validating any feature, check against these patterns:

```markdown
### Navigation Consistency
- [ ] Breadcrumbs present and accurate
- [ ] Left sidebar highlights current section
- [ ] Back navigation works correctly

### UI Component Consistency
- [ ] Buttons use standard styles
- [ ] Forms follow standard patterns
- [ ] Tables/lists match other pages
- [ ] Status indicators consistent colors

### Interaction Consistency
- [ ] Destructive actions have confirmation
- [ ] Loading states present
- [ ] Error handling follows patterns
- [ ] Empty states are helpful
```
