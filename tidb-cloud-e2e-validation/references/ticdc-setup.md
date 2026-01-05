# TiCDC Changefeed Setup Reference

## Feature Overview

TiCDC (TiDB Change Data Capture) Changefeed enables real-time data replication from TiDB Cloud to external systems like Kafka or MySQL. This reference covers the complete setup workflow for validation.

> **Note**: The Changefeed feature is in BETA for TiDB Cloud Essential.

## Prerequisites for Validation

- An existing TiDB Cloud Essential cluster in the target project
- Kafka server details (for Kafka destination testing):
  - Bootstrap server address (e.g., `broker:9092`)
  - Authentication credentials (if using SASL)

---

## UI Navigation Path

1. Sign in to TiDB Cloud
2. Select Organization > Project
3. Click on target Cluster
4. Left sidebar: **Data** > **Changefeed**
5. Click **Create Changefeed** button

---

## Workflow Steps

### Step 1: Configure Destination

| Field | Options | Notes |
|-------|---------|-------|
| Destination | Kafka, MySQL | Primary destination type |
| Connectivity Method | Public, Private Link | Network access method |
| Bootstrap Servers | `host:port` | Kafka broker address |
| Authentication | Disable, SASL/PLAIN, SASL/SCRAM-SHA-256, SASL/SCRAM-SHA-512 | Security method |
| Kafka Version | Kafka v3 (default) | Advanced setting |
| Compression | None, Lz4, Snappy, Zstd | Advanced setting |
| TLS Encryption | Enable/Disable | Required for cloud Kafka |

**Validation Points:**
- [ ] All destination types are selectable
- [ ] Bootstrap server field validates format
- [ ] Authentication options show/hide credential fields appropriately
- [ ] TLS toggle works correctly

### Step 2: Configure Replication

#### Table Filter Tab
| Field | Default | Notes |
|-------|---------|-------|
| Filter Rules | `*.*` | Matches all tables |
| Matched Tables | (dynamic) | Shows preview of tables |

#### Event Filter Tab (Optional)
- Add custom event filters as needed

#### Column Selector Tab (Optional)
- Select specific columns for replication

#### Start Replication Position
| Option | Description |
|--------|-------------|
| From now on | Start from current position (default) |
| From a specific TSO | Start from Transaction Status Oracle |
| From a specific time | Start from timestamp |

#### Data Format
| Format | Use Case |
|--------|----------|
| Canal-JSON | General purpose, human-readable |
| Avro | Schema registry integration |
| Open Protocol | TiDB native format |
| Debezium | Debezium ecosystem compatibility |

#### Topic Configuration
| Field | Default | Notes |
|-------|---------|-------|
| Distribution Mode | Single topic, By table, By database | How topics are organized |
| Topic Name | (required) | Kafka topic name |
| Partition Distribution | Table, RowID | Event distribution strategy |
| Replication Factor | 2 | Kafka replication |
| Partition Number | 5 | Kafka partitions |

#### TiDB Extension
- Enable/disable TiDB-specific fields in output

#### Event Splitting
- Configure UPDATE event handling behavior

**Validation Points:**
- [ ] Table filter preview updates dynamically
- [ ] All data format options are available
- [ ] Topic name field is required (validation error if empty)
- [ ] Distribution mode changes show/hide relevant fields
- [ ] Numeric fields validate input ranges

### Step 3: Review and Submit

- Summary of all configuration settings
- Submit button to create Changefeed

**Validation Points:**
- [ ] All configured values display correctly in review
- [ ] Submit button creates the Changefeed
- [ ] Success message appears after creation
- [ ] Changefeed appears in list with correct status

---

## Expected UI States

### Changefeed List View
| State | Indicator | Description |
|-------|-----------|-------------|
| Creating | Spinner/Badge | Changefeed being provisioned |
| Running | Green badge | Actively replicating |
| Paused | Yellow badge | Manually paused |
| Error | Red badge | Replication error |
| Stopped | Gray badge | Terminated |

### After Successful Creation
1. Redirects to Changefeed list or detail page
2. New Changefeed visible in list
3. Status shows "Creating" then transitions to "Running"

---

## Functional Validation Checklist

### Happy Path (New User)
- [ ] Can complete setup following only UI prompts
- [ ] Tooltips explain technical terms (TSO, partition dispatcher, etc.)
- [ ] Default values are sensible for basic use case
- [ ] Error messages are clear if validation fails
- [ ] Success state is obvious after creation

### Power User Path
- [ ] Can quickly navigate to Changefeed creation
- [ ] Advanced settings are accessible without extra clicks
- [ ] Can configure all options without unnecessary steps
- [ ] Keyboard navigation works for form fields

---

## Common Test Scenarios

### Scenario 1: Kafka with SASL/PLAIN (Confluent Cloud)
```
Destination: Kafka
Bootstrap Servers: pkc-xxxxx.region.aws.confluent.cloud:9092
TLS Encryption: Enabled
Authentication: SASL/PLAIN
Username: <API Key>
Password: <API Secret>
Data Format: Canal-JSON
Topic Name: tidb-cdc-events
Distribution: Single Topic
```

### Scenario 2: Kafka without Authentication (Local/Dev)
```
Destination: Kafka
Bootstrap Servers: localhost:9092
TLS Encryption: Disabled
Authentication: Disable
Data Format: Canal-JSON
Topic Name: test-events
Distribution: By Table
```

### Scenario 3: MySQL Destination
```
Destination: MySQL
Host: mysql.example.com
Port: 3306
Username: replication_user
Password: ********
Database: replica_db
```

---

## Error Scenarios to Test

| Scenario | Expected Behavior |
|----------|-------------------|
| Invalid bootstrap server format | Validation error on field |
| Missing required topic name | Cannot proceed to next step |
| Invalid credentials | Connection test fails with clear message |
| Network unreachable | Timeout with actionable error |
| Duplicate Changefeed name | Error message indicating conflict |

---

## UX Review Focus Areas

### Discoverability
- Is "Changefeed" clearly labeled under Data menu?
- Is the "Create Changefeed" button prominent?

### Clarity
- Are Kafka-specific terms explained (bootstrap server, partition, etc.)?
- Is the 3-step wizard progress clear?
- Are optional vs required fields distinguished?

### Efficiency
- How many clicks from cluster page to created Changefeed?
- Are there smart defaults that reduce configuration?
- Can power users skip optional sections?

### Feedback
- Is there a connection test before submission?
- Does the UI show progress during creation?
- Are status transitions visible in the list?

### Error Handling
- Are validation errors inline or at form level?
- Can users recover from errors without losing configuration?
- Are error messages actionable?

---

## Related References

- [Cluster Management](cluster-management.md) - For cluster prerequisites
- [Navigation Patterns](navigation-patterns.md) - For common UI patterns
