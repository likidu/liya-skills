# TiDB Cloud Changefeed Testing Guide: TiDB → Confluent Cloud → S3

This guide walks you through testing the TiCDC feature with your existing 3-5GB sample data flowing from TiDB Cloud Essential through Confluent Cloud Kafka to an S3 Data Lake.

## Prerequisites

- TiDB Cloud Essential cluster with sample data already loaded in `cdc_test` database
- Tables: `customers`, `products`, `orders`, `order_items`, `event_logs`
- AWS account with S3 access
- Confluent Cloud account (free tier works)

---

## Part 1: Set Up Confluent Cloud Kafka

### 1.1 Create Confluent Cloud Cluster

1. Go to [confluent.io/cloud](https://confluent.io) and sign up/login
2. Click **Add Cluster** → Select **Basic** (free tier)
3. Choose your cloud provider (AWS recommended for S3 integration) and region (match your TiDB region if possible)
4. Name your cluster (e.g., `tidb-cdc-test`) and create it

### 1.2 Create Kafka Topic

1. In your cluster, go to **Topics** → **Create Topic**
2. Configure:
   - Topic name: `tidb-cdc-events`
   - Partitions: `6` (allows parallelism)
   - Click **Create with defaults**

### 1.3 Create API Keys

1. Go to **API Keys** → **Add Key**
2. Select **Global access** → **Next**
3. Download and save the API Key and Secret
4. Note your **Bootstrap server** from the cluster settings (looks like `pkc-xxxxx.us-east-1.aws.confluent.cloud:9092`)

---

## Part 2: Set Up S3 Bucket

### 2.1 Create S3 Bucket

```bash
# Create bucket
aws s3 mb s3://tidb-cdc-data-lake-test --region us-east-1

# Create folder structure
aws s3api put-object --bucket tidb-cdc-data-lake-test --key raw/tidb-events/
```

### 2.2 Create IAM User for Confluent

```bash
# Create policy file
cat > confluent-s3-policy.json << 'EOF'
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:ListBucket",
                "s3:DeleteObject",
                "s3:GetBucketLocation"
            ],
            "Resource": [
                "arn:aws:s3:::tidb-cdc-data-lake-test",
                "arn:aws:s3:::tidb-cdc-data-lake-test/*"
            ]
        }
    ]
}
EOF

# Create IAM user and attach policy
aws iam create-user --user-name confluent-s3-sink
aws iam put-user-policy --user-name confluent-s3-sink --policy-name S3SinkPolicy --policy-document file://confluent-s3-policy.json

# Create access keys
aws iam create-access-key --user-name confluent-s3-sink
# Save the AccessKeyId and SecretAccessKey from the output
```

---

## Part 3: Configure TiDB Cloud Changefeed

### 3.1 Create Changefeed in TiDB Cloud Console

1. Go to your TiDB Cloud cluster → **Data** → **Changefeed**
2. Click **Create Changefeed**

### 3.2 Step 1 - Destination Configuration

| Field | Value |
|-------|-------|
| Destination | **Kafka** |
| Connectivity Method | **Public** |
| Bootstrap Servers | `pkc-xxxxx.us-east-1.aws.confluent.cloud:9092` (your Confluent bootstrap server) |

**Authentication:**

| Field | Value |
|-------|-------|
| Authentication | **SASL/PLAIN** |
| SASL Username | Your Confluent API Key |
| SASL Password | Your Confluent API Secret |

**Advanced Settings:**

| Field | Value |
|-------|-------|
| Kafka Version | **Kafka v3** |
| Compression | **lz4** |
| TLS Encryption | **Enabled** (toggle on) |

Click **Next**

### 3.3 Step 2 - Replication Configuration

| Setting | Value |
|---------|-------|
| Data Format | **Canal-JSON** |
| Topic Distribution | **Single topic** |
| Topic Name | `tidb-cdc-events` |
| Partition Distribution | **By table** |

**Select Tables:**

- Expand `cdc_test` database
- Check all tables: `customers`, `products`, `orders`, `order_items`, `event_logs`

Click **Next**

### 3.4 Step 3 - Review and Create

Review your configuration and click **Create**

Wait for the changefeed status to become **Running** (usually 1-2 minutes)

---

## Part 4: Set Up Confluent S3 Sink Connector

### 4.1 Create S3 Sink Connector

1. In Confluent Cloud, go to your cluster → **Connectors**
2. Click **Add Connector** → Search for **Amazon S3 Sink**
3. Click **Amazon S3 Sink** → **Add new connector**

### 4.2 Configure the Connector

**Step 1 - Select topic:**

- Select `tidb-cdc-events`

**Step 2 - Kafka credentials:**

- Use existing or create new API key for the connector

**Step 3 - Authentication:**

| Field | Value |
|-------|-------|
| AWS Access Key ID | Your IAM user access key |
| AWS Secret Access Key | Your IAM user secret key |

**Step 4 - Configuration:**

| Field | Value |
|-------|-------|
| Input Kafka record value format | **JSON** |
| Connector name | `s3-sink-tidb-cdc` |

**Step 5 - S3 Configuration:**

| Field | Value |
|-------|-------|
| S3 Bucket Name | `tidb-cdc-data-lake-test` |
| S3 Region | `us-east-1` |
| Output message format | **JSON** |
| Time interval (ms) | `60000` (1 minute) |
| Flush size | `100` (records, lower for testing) |

Click **Continue** → **Launch**

Wait for connector status to become **Running**

---

## Part 5: Generate CDC Events for Testing

Use the `cdc_event_generator.py` script to generate real-time INSERT, UPDATE, and DELETE operations.

### 5.1 Install Dependencies

```bash
pip install mysql-connector-python
```

### 5.2 Configure the Script

Edit the `CONFIG` section in `cdc_event_generator.py` with your TiDB Cloud connection details:

```python
CONFIG = {
    'host': 'gateway01.us-east-1.prod.aws.tidbcloud.com',  # Your TiDB host
    'port': 4000,
    'user': 'root',
    'password': 'YOUR_PASSWORD',  # Your TiDB password
    'database': 'cdc_test',
}
```

### 5.3 Run the Script

```bash
# Run in continuous mode (10 events/second, runs until Ctrl+C)
python cdc_event_generator.py --mode continuous --rate 10

# Run for specific duration (5 minutes at 20 events/second)
python cdc_event_generator.py --mode continuous --rate 20 --duration 300

# Run burst mode (500 events as fast as possible)
python cdc_event_generator.py --mode burst --count 500
```

---

## Part 6: Verify the Pipeline

### 6.1 Check TiDB Cloud Changefeed Status

1. Go to TiDB Cloud → **Data** → **Changefeed**
2. Verify:
   - Status: **Running**
   - Checkpoint TS: Should be advancing
   - Replication Lag: Should be < 10 seconds

### 6.2 Check Confluent Cloud Messages

1. Go to Confluent Cloud → Your cluster → **Topics** → `tidb-cdc-events`
2. Click **Messages** tab
3. You should see CDC events appearing in Canal-JSON format

Sample message structure:

```json
{
  "id": 0,
  "database": "cdc_test",
  "table": "orders",
  "pkNames": ["order_id"],
  "isDdl": false,
  "type": "INSERT",
  "es": 1704825600000,
  "ts": 1704825600001,
  "data": [{
    "order_id": "2000001",
    "customer_id": "42",
    "total_amount": "299.99",
    "status": "pending"
  }],
  "old": null
}
```

### 6.3 Check S3 Data Lake

The S3 Sink Connector writes data based on flush conditions (flush size or time interval). After generating enough events:

```bash
# List files in S3 (default path: topics/<topic-name>/partition=<N>/)
aws s3 ls s3://tidb-cdc-data-lake-test/topics/ --recursive

# Download and inspect a sample file
aws s3 cp s3://tidb-cdc-data-lake-test/topics/tidb-cdc-events/partition=0/tidb-cdc-events+0+0000000000.json ./sample.json

# View content (pretty print)
cat sample.json | head -5 | jq '.'
```

> **Note:** If no files appear in S3, the flush conditions may not be met yet. Either generate more events to reach the flush size, or wait for the time interval to trigger a flush. Check your connector settings for `flush.size` and `rotate.interval.ms` values.

### 6.4 Verify Event Types

Run different scenarios with the Python script and verify in S3:

| Action | Expected `type` in S3 |
|--------|----------------------|
| Insert new order | `INSERT` |
| Update order status | `UPDATE` (with `old` and `data` fields) |
| Delete cancelled order | `DELETE` (with `old` field) |

---

## Part 7: Testing Checklist

| Test | How to Verify | Expected Result |
|------|---------------|-----------------|
| Changefeed Running | TiDB Cloud Console | Status: Running |
| Kafka Receiving | Confluent Cloud → Topics → Messages | Messages appearing |
| S3 Connector Running | Confluent Cloud → Connectors | Status: Running |
| S3 Data Arriving | `aws s3 ls` | JSON files in bucket |
| INSERT captured | Run script, check S3 | `type: "INSERT"` with `data` |
| UPDATE captured | Run script, check S3 | `type: "UPDATE"` with `old` and `data` |
| DELETE captured | Run script, check S3 | `type: "DELETE"` with `old` |
| Latency | Insert row, time until S3 | < 2-3 minutes end-to-end |

---

## Cleanup

When done testing:

```bash
# Delete S3 data
aws s3 rm s3://tidb-cdc-data-lake-test/ --recursive
aws s3 rb s3://tidb-cdc-data-lake-test

# Delete IAM user
aws iam delete-user-policy --user-name confluent-s3-sink --policy-name S3SinkPolicy
aws iam delete-access-key --user-name confluent-s3-sink --access-key-id YOUR_ACCESS_KEY_ID
aws iam delete-user --user-name confluent-s3-sink
```

In TiDB Cloud:

- Delete the changefeed from **Data** → **Changefeed**

In Confluent Cloud:

- Delete the S3 Sink connector
- Delete the topic
- Delete the cluster (if no longer needed)
