# TiDB CDC Testing Tools

Tools for testing TiDB CDC (Change Data Capture) functionality.

## Tools Included

1. **Sample Data Generator** (`generate_sample_data.py`) - Generates initial test data
2. **CDC Event Generator** (`cdc_event_generator.py`) - Generates continuous INSERT/UPDATE/DELETE operations for testing changefeeds

## Features

### Sample Data Generator
- Generates sample data across 5 tables: customers, products, orders, order_items, event_logs
- Two modes: `small` (~10MB for testing) and `full` (~3-5GB for production)
- Detailed progress output with ETA and throughput metrics

### CDC Event Generator
- Generates realistic INSERT, UPDATE, and DELETE operations
- Two modes: `continuous` (sustained event generation) and `burst` (maximum speed)
- Configurable event rate and duration
- Real-time statistics tracking
- Weighted operation distribution (60% INSERT, 30% UPDATE, 10% DELETE)

Both tools are configurable via environment variables.

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

### Sample Data Generator

Generate initial test data in your TiDB database:

```bash
# Small dataset for testing (~10MB, ~1,150 records)
python generate_sample_data.py --mode small

# Full dataset for production (~3-5GB, ~10M records)
python generate_sample_data.py --mode full

# Preview without generating data
python generate_sample_data.py --mode full --dry-run
```

**Data Generated:**

| Mode | Customers | Products | Orders | Order Items | Event Logs | Total |
|------|-----------|----------|--------|-------------|------------|-------|
| small | 100 | 50 | 200 | 500 | 300 | ~1,150 |
| full | 100K | 50K | 2M | 5M | 3M | ~10.15M |

### CDC Event Generator

Generate continuous database operations to test CDC changefeeds:

```bash
# Continuous mode - generate events at 10 events/second (default)
python cdc_event_generator.py --mode continuous --rate 10

# Continuous mode - custom rate for 5 minutes
python cdc_event_generator.py --mode continuous --rate 50 --duration 300

# Continuous mode - infinite duration (Ctrl+C to stop)
python cdc_event_generator.py --mode continuous --rate 20

# Burst mode - generate 1000 events as fast as possible
python cdc_event_generator.py --mode burst --count 1000

# Burst mode - generate 10000 events
python cdc_event_generator.py --mode burst --count 10000
```

**Operation Types:**

| Operation | Weight | Description |
|-----------|--------|-------------|
| INSERT | 60% | New customers, orders (with items), order items, event logs |
| UPDATE | 30% | Order status changes, product stock updates, customer address updates |
| DELETE | 10% | Old cancelled orders, old event logs |

**Statistics Output:**

The generator provides real-time statistics every 10 seconds:
- Total events generated
- Event rate (events/second)
- Breakdown by operation type (INS/UPD/DEL)
- Error count

## Typical Workflow

1. **Generate initial data** using `generate_sample_data.py`
2. **Set up TiDB changefeed** to capture changes
3. **Run CDC event generator** using `cdc_event_generator.py` to simulate live traffic
4. **Monitor changefeed** to verify all changes are captured correctly

## Tables Schema

Both tools work with the following tables:

- **customers** - Customer information (email, name, address)
- **products** - Product catalog (SKU, name, price, stock)
- **orders** - Order records (customer_id, total, status, payment)
- **order_items** - Line items for orders (order_id, product_id, quantity, price)
- **event_logs** - Application events (event_type, entity, metadata)
