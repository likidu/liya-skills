# TiDB Cloud Navigation Patterns

Common UI navigation patterns and elements across TiDB Cloud console. Use this reference to validate consistency.

## Entity Hierarchy

TiDB Cloud has a 3-level hierarchy:

```
Organization
  └── Project
        └── Cluster
```

Each level has its own set of features accessible via the left sidebar. The sidebar content changes based on which level you're viewing.

---

## Global Navigation Structure

### Left Sidebar (Primary Navigation)

The left sidebar is the primary navigation element. It contains:

1. **Context Switcher** (top of sidebar)
   - Dropdown showing current Organization or Project name
   - Click to open quick switcher panel

2. **Feature Menu** (middle)
   - Changes based on current context level (Org, Project, or Cluster)
   - Highlights currently active section

3. **Bottom Section** (persistent across all levels)
   - Support
   - Notification
   - User Menu (account name with expand arrow)

### Quick Switcher Panel

Accessed by clicking the context switcher at top of sidebar:

- **Search box**: "Find organization or project..."
- **Organization list**: Shows all accessible organizations
  - Organizations marked with "ENT." badge if Enterprise
  - Checkmark indicates currently selected
  - Expandable to show projects within each org
- **Project list**: Shows projects under expanded org
  - Arrow icon to navigate directly to project
- **Cluster list**: When in project context, shows clusters
  - Breadcrumb path: "Org > Project"
  - "+ Create Cluster" action at bottom

**Note**: TiDB Cloud does NOT use breadcrumbs for navigation. The quick switcher and sidebar context provide navigation context instead.

---

## Sidebar Content by Level

### Organization Level
URL pattern: `/org-settings/...`

Sidebar sections:
- Projects
- Billing
- Console Audit Logging
- Organization Settings (expandable)
  - General
  - Users
  - API Keys
  - Authentication

### Project Level
URL pattern: `/project/clusters?orgId=...&projectId=...`

Sidebar sections:
- Clusters
- Data Service
- Recovery Group
- Project Settings (expandable)
  - Network Access
  - Integrations
  - Alert Subscription
  - Maintenance
  - Recycle Bin

### Cluster Level
URL pattern: `/clusters/{clusterId}/overview?orgId=...&projectId=...`

Sidebar sections:
- Overview
- SQL Editor
- Branches
- Data (expandable)
  - Import
  - Export
  - Changefeed
  - Backup
- Monitoring (expandable)
- Integrations
- Settings (expandable)
  - SQL Users
  - Networking

---

## Common UI Patterns

### List Views (e.g., Projects, Clusters)

All list views should have:
- [ ] Search/filter capability (search box above table)
- [ ] Column headers with data type indication
- [ ] Pagination controls at bottom (page numbers)
- [ ] "Create [Resource]" button (top right, primary blue)
- [ ] Actions menu (three dots "..." in Actions column)

**Columns typically include**:
- ID (where applicable)
- Name (clickable link)
- Status (with color indicator)
- Creation Time
- Other resource-specific attributes
- Actions

### Detail Views (e.g., Cluster Overview)

All detail pages should have:
- [ ] Context switcher showing resource name
- [ ] Title matching the page section
- [ ] Quick actions in top right (e.g., "Connect" button)
- [ ] More actions via "..." menu
- [ ] Status indicator in properties section

### Info Banners

Informational banners appear below page title:
- Blue/teal background with icon
- Dismissible (X button on right)
- "Learn more" link for additional context
- Example: "Serverless clusters are now the Starter clusters..."

### Forms

All forms should have:
- [ ] Clear field labels
- [ ] Required field indicators
- [ ] Inline validation
- [ ] Primary action button (blue)
- [ ] Cancel/secondary actions
- [ ] Loading state on submit

### Modals/Dialogs

All modals should have:
- [ ] Clear title
- [ ] Close button (X)
- [ ] Escape key closes modal
- [ ] Confirm/Cancel for destructive actions
- [ ] Focus trapped inside modal

---

## Status Indicators

### Cluster Status
| Status | Indicator | Meaning |
|--------|-----------|---------|
| Active | Green dot | Cluster is ready and running |
| Creating | Yellow/Blue | Cluster being provisioned |
| Modifying | Yellow/Blue | Changes in progress |
| Paused | Gray | Cluster is paused |
| Failed | Red | Error state |

---

## Action Patterns

### Primary Actions
- Located in top right of page
- Blue filled button style
- Examples: "Create Cluster", "Create New Project", "Connect"

### Secondary/More Actions
- Three dots menu ("...")
- Located in top right (next to primary) or in table rows
- Contains less common actions

### Destructive Actions
For delete/destroy operations:
- [ ] Requires confirmation modal
- [ ] Shows what will be deleted
- [ ] May require typing resource name
- [ ] Clear warning about irreversibility
- [ ] Red/danger button styling

### Long-Running Actions
For operations that take time:
- [ ] Immediate feedback that action started
- [ ] Status indicator updates
- [ ] User can navigate away (action continues)

---

## Navigation Validation Checklist

When validating navigation, check:

```markdown
### Context Awareness
- [ ] Context switcher shows correct current location
- [ ] Sidebar items match current level (Org/Project/Cluster)
- [ ] Quick switcher allows navigation to other orgs/projects/clusters

### Sidebar Behavior
- [ ] Current section highlighted
- [ ] Expandable sections work correctly
- [ ] Bottom section (Support, Notification, User) always visible

### List Navigation
- [ ] Clicking resource name navigates to detail
- [ ] Pagination works correctly
- [ ] Search filters results appropriately

### URL Structure
- [ ] URL reflects current context (orgId, projectId, clusterId)
- [ ] URLs are shareable/bookmarkable
- [ ] Browser back/forward works as expected
```

---

## Known Patterns (Not Present)

The following common patterns are **NOT used** in TiDB Cloud:

- **Breadcrumbs**: Navigation context provided by quick switcher instead
- **Top navigation bar**: All navigation is in left sidebar
- **Tabs for main navigation**: Sidebar sections used instead (though tabs may appear within pages)

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

### Empty States
- [ ] Friendly message explaining emptiness
- [ ] Call to action to create first item
- [ ] Link to documentation if helpful

---

## Loading States

### Initial Page Load
- [ ] Loading indicator visible
- [ ] No content flash/jump

### Action Loading
- [ ] Button shows loading state
- [ ] Form disabled during submission
- [ ] Clear indication something is happening
