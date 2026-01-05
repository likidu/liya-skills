# TiDB Sample Data Generator

Generates test data for TiDB CDC (Change Data Capture) testing.

## Features

- Generates sample data across 5 tables: customers, products, orders, order_items, event_logs
- Two modes: `small` (~10MB for testing) and `full` (~3-5GB for production)
- Detailed progress output with ETA and throughput metrics
- Configurable via environment variables

## Setup

### 1. Install Dependencies

```bash
# Create virtual environment (recommended)
python -m venv test_cdc_env
source test_cdc_env/bin/activate  # On Windows: test_cdc_env\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy the sample environment file
cp .env.sample .env

# Edit .env with your TiDB connection details
```

Required environment variables:
| Variable | Description | Default |
|----------|-------------|---------|
| `TIDB_HOST` | TiDB server hostname | `gateway01.us-east-1.prod.aws.tidbcloud.com` |
| `TIDB_PORT` | TiDB server port | `4000` |
| `TIDB_USER` | Database username | `root` |
| `TIDB_PASSWORD` | Database password | (empty) |
| `TIDB_DATABASE` | Database name | `cdc_test` |
| `TIDB_SSL_CA` | Path to SSL CA certificate | (empty) |
| `TIDB_SSL_VERIFY` | Verify SSL certificate | `true` |

## Usage

```bash
# Small dataset for testing (~10MB, ~1,150 records)
python generate_sample_data.py --mode small

# Full dataset for production (~3-5GB, ~10M records)
python generate_sample_data.py --mode full

# Preview without generating data
python generate_sample_data.py --mode full --dry-run
```

## Data Generated

| Mode | Customers | Products | Orders | Order Items | Event Logs | Total |
|------|-----------|----------|--------|-------------|------------|-------|
| small | 100 | 50 | 200 | 500 | 300 | ~1,150 |
| full | 100K | 50K | 2M | 5M | 3M | ~10.15M |
