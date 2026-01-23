# Cluster Management Validation

This reference covers validation steps for cluster creation, scaling, and management in TiDB Cloud.

## Feature Overview

Cluster management includes:
- Creating new clusters (Serverless and Dedicated)
- Viewing cluster details and status
- Scaling cluster resources
- Pausing/resuming clusters
- Deleting clusters

---

## Cluster Creation Validation

### Navigation Path
1. Dashboard -> Click "Create Cluster" or "+" button
2. Or: Clusters list -> "Create Cluster" button

### Happy Path Persona Test

**Goal**: A new user should be able to create their first cluster without confusion.

#### Step-by-Step Validation

1. **Landing on Create Page**
   - [ ] Clear explanation of cluster types (Serverless vs Dedicated)
   - [ ] Recommendation for new users visible
   - [ ] Pricing/cost information accessible
   - [ ] "Learn more" links work

2. **Cluster Type Selection**
   - [ ] Difference between types is clear
   - [ ] Serverless is highlighted as starting point for new users
   - [ ] Dedicated tier shows what's different/additional

3. **Configuration Options**
   - [ ] Default values are sensible for getting started
   - [ ] Region selection is clear (shows available regions)
   - [ ] Cluster name field has validation feedback
   - [ ] Tooltips explain technical options

4. **Review & Create**
   - [ ] Summary shows what will be created
   - [ ] Cost estimate visible (if applicable)
   - [ ] Create button is prominent and **not overlapped by other elements**
   - [ ] Cancel/back navigation works
   - [ ] **Check floating help icon doesn't overlap Create/Cancel buttons**

5. **Post-Creation**
   - [ ] Clear feedback that creation started
   - [ ] Progress/status indicator visible
   - [ ] Redirected to cluster details or list
   - [ ] Time estimate for cluster availability shown

### Power User Persona Test

**Goal**: An experienced user should be able to create a cluster quickly with specific configurations.

#### Step-by-Step Validation

1. **Quick Access**
   - [ ] Can reach create page in 2 clicks or less
   - [ ] Keyboard shortcuts available
   - [ ] Recent configurations remembered (if applicable)

2. **Configuration Efficiency**
   - [ ] Can quickly select Dedicated tier
   - [ ] Advanced options accessible without extra steps
   - [ ] Node count/sizing options clear
   - [ ] Region selection includes all available options
   - [ ] VPC/networking options visible for Dedicated

3. **Bulk/Repeat Operations**
   - [ ] Can clone existing cluster configuration
   - [ ] Settings can be imported/templated

4. **Speed to Completion**
   - [ ] Measure total clicks to complete
   - [ ] Target: < 10 clicks for full configuration
   - [ ] No unnecessary confirmation dialogs

---

## UI State Verification

After cluster creation, verify through the UI:

1. **Cluster Visible**
   - Cluster appears in cluster list
   - Cluster name matches what was entered

2. **Status Progression**
   - Status shows "Creating" initially
   - Status updates to "Available" when ready
   - Progress indicator visible during creation

3. **Details Match Configuration**
   - Selected tier displayed correctly
   - Region shown matches selection
   - Cluster details page accessible

---

## Error Scenarios to Test

1. **Invalid cluster name**
   - Empty name
   - Name with special characters
   - Duplicate name
   - Name too long

2. **Region unavailable**
   - Selected region has capacity issues
   - Region not available for account type

3. **Quota exceeded**
   - Too many clusters for account
   - Resource limits hit

4. **Network errors**
   - Timeout during creation
   - Connection lost mid-process

---

## UX Focus Areas

### Discoverability
- Is "Create Cluster" button visible on dashboard?
- Can users find creation from cluster list?
- Is empty state helpful for new users?

### Clarity
- Is Serverless vs Dedicated difference clear?
- Are region implications explained?
- Is sizing guidance provided?

### Feedback
- Creation progress indication
- Time estimate accuracy
- Error message helpfulness

### Consistency
- Does creation flow match other TiDB Cloud patterns?
- Are buttons/layouts consistent?

---

## Expected Validation Report Sections

When validating cluster creation, the report should include:

1. **Navigation Assessment**
   - Paths to reach create page
   - Number of clicks required
   - Discoverability score

2. **Form Usability**
   - Field clarity scores
   - Default value appropriateness
   - Validation feedback quality

3. **Creation Process**
   - Total time from start to cluster available
   - Progress feedback quality
   - Status accuracy

4. **Screenshots**
   - Empty state (before first cluster)
   - Create page initial state
   - Configuration options
   - Review step
   - Progress/status indicators
   - Final cluster in list

---

## Cluster List Page Validation

The cluster list page (My TiDB) has its own set of checks:

### Visual Consistency
- [ ] **Plan colors match** between list page badges and creation page cards
- [ ] **Status colors** are consistent (Active, Modifying, etc.)
- [ ] **Column alignment** is consistent

### Dropdown Menu Actions
- [ ] **Action menus** are consistent across different plan types
- [ ] Premium actions: Rename, Import, Delete, Get Support
- [ ] Essential actions: Should match Premium where applicable
- [ ] Starter actions: May have fewer options (no Import)
- [ ] **Disabled actions** show tooltip explaining why

### Filtering & Sorting
- [ ] Filters work correctly (by Plan, Region, Status, Project)
- [ ] Clear Filter button works
- [ ] Refresh button actually refreshes the data (not just cached)
- [ ] **Empty table** doesn't show pagination

### Create Resource Menu
- [ ] "Restore from Cloud Storage" shows warning if not supported for plan
- [ ] "Restore from Another Plan" shows warning if not supported
- [ ] Menu item names are complete (not truncated)

---

## Cross-Page Consistency Checks

**IMPORTANT**: When validating cluster features, always check consistency across these pages:

### Color Consistency
| Element | Creation Page | List Page | Should Match? |
|---------|---------------|-----------|---------------|
| Starter badge/card | Pink | Pink | Yes |
| Essential badge/card | Blue | Blue | Yes |
| Premium badge/card | Purple | Purple | Yes |
| Dedicated badge/card | Gray | Gray | Yes |

### Feature Availability by Plan
| Feature | Starter | Essential | Premium | Dedicated |
|---------|---------|-----------|---------|-----------|
| Restore from Cloud Storage | No | No | Yes | Yes |
| Restore from Another Plan | No | No | Yes | Yes |
| High Availability options | No | Yes | Yes | Yes |
| Advanced encryption | With spending limit | Yes | Yes | Yes |

**Note**: If a feature is shown but not available for a plan, there must be a clear indication (tooltip, message, or visual disabled state).

---

## Common Issues to Watch For

| Issue | Severity | Description |
|-------|----------|-------------|
| Unclear tier differences | Medium | New users don't know which to pick |
| No cost visibility | High | Users surprised by costs |
| Poor progress feedback | Medium | Users unsure if creation is working |
| Confusing region names | Low | Technical region codes vs friendly names |
| Status lag | Medium | UI shows wrong status temporarily |
| **Help icon overlaps Create button** | High | Floating elements cover action buttons |
| **Plan colors inconsistent** | Medium | Colors differ between list and creation pages |
| **Selected+hover thick border** | Medium | Visual glitch when hovering selected card |
| **Dropdown menu inconsistency** | Medium | Different plans have inconsistent menus |
| **Empty table shows pagination** | Low | Pagination visible when no data |
| **Restore options confuse non-Premium users** | High | Options shown but not available |
| **Disabled tier no explanation** | High | Dedicated tier grayed out with no tooltip |
