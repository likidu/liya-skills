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
   - [ ] Create button is prominent
   - [ ] Cancel/back navigation works

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

## Functional Verification

### Backend State Checks

After cluster creation, verify:

1. **Cluster Exists**
   - Cluster appears in cluster list
   - Cluster ID is generated
   - API returns cluster details

2. **Status Progression**
   - Status shows "Creating" initially
   - Status updates to "Available" when ready
   - Status matches actual cluster state

3. **Resource Allocation**
   - Selected tier matches created cluster
   - Region is correct
   - Node configuration matches selection

### Verification Script Usage

```bash
# Check cluster status via API (if credentials available)
# This would be implemented in scripts/verify_cluster_status.py
```

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

## Common Issues to Watch For

| Issue | Severity | Description |
|-------|----------|-------------|
| Unclear tier differences | Medium | New users don't know which to pick |
| No cost visibility | High | Users surprised by costs |
| Poor progress feedback | Medium | Users unsure if creation is working |
| Confusing region names | Low | Technical region codes vs friendly names |
| Status lag | Medium | UI shows wrong status temporarily |
