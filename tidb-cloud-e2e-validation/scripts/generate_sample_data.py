#!/usr/bin/env python3
"""
TiDB Sample Data Generator
Generates test data for CDC testing

Usage:
    python generate_sample_data.py --mode small   # Small dataset for testing (~10MB)
    python generate_sample_data.py --mode full    # Full dataset for production (~3-5GB)
    python generate_sample_data.py                # Defaults to small mode

Environment:
    Copy .env.sample to .env and configure your TiDB connection settings.
"""

import argparse
import json
import os
import random
import string
import sys
import time
import uuid
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from pathlib import Path

import mysql.connector

# Try to load python-dotenv if available
try:
    from dotenv import load_dotenv

    # Load .env file from the same directory as the script
    env_path = Path(__file__).parent / ".env"
    load_dotenv(env_path)
except ImportError:
    pass  # python-dotenv not installed, will use environment variables directly


def get_config():
    """Get database configuration from environment variables"""
    ssl_verify = os.getenv("TIDB_SSL_VERIFY", "true").lower() in ("true", "1", "yes")
    ssl_ca = os.getenv("TIDB_SSL_CA", "")

    config = {
        "host": os.getenv("TIDB_HOST", "gateway01.us-east-1.prod.aws.tidbcloud.com"),
        "port": int(os.getenv("TIDB_PORT", "4000")),
        "user": os.getenv("TIDB_USER", "root"),
        "password": os.getenv("TIDB_PASSWORD", ""),
        "database": os.getenv("TIDB_DATABASE", "cdc_test"),
    }

    # Only add SSL options if SSL CA path is provided
    if ssl_ca:
        config["ssl_ca"] = ssl_ca
        config["ssl_verify_cert"] = ssl_verify

    return config


# Connection configuration (loaded from environment)
CONFIG = get_config()

# Data generation configurations
DATA_CONFIGS = {
    "small": {
        "customers": 100,
        "products": 50,
        "orders": 200,
        "order_items": 500,
        "event_logs": 300,
        "batch_size": 50,
        "description": "Small dataset for testing (~10MB)",
    },
    "full": {
        "customers": 100000,
        "products": 50000,
        "orders": 2000000,
        "order_items": 5000000,
        "event_logs": 3000000,
        "batch_size": 5000,
        "description": "Full dataset for production (~3-5GB)",
    },
}

# Sample data pools
FIRST_NAMES = [
    "James",
    "Mary",
    "John",
    "Patricia",
    "Robert",
    "Jennifer",
    "Michael",
    "Linda",
    "William",
    "Elizabeth",
]
LAST_NAMES = [
    "Smith",
    "Johnson",
    "Williams",
    "Brown",
    "Jones",
    "Garcia",
    "Miller",
    "Davis",
    "Rodriguez",
    "Martinez",
]
CITIES = [
    "New York",
    "Los Angeles",
    "Chicago",
    "Houston",
    "Phoenix",
    "Philadelphia",
    "San Antonio",
    "San Diego",
    "Dallas",
    "Austin",
]
STREETS = [
    "Main",
    "Oak",
    "Pine",
    "Maple",
    "Cedar",
    "Elm",
    "Washington",
    "Park",
    "Lake",
    "Hill",
]
STREET_TYPES = ["St", "Ave", "Blvd", "Dr", "Ln", "Way", "Ct", "Pl"]
CATEGORIES = [
    "Electronics",
    "Clothing",
    "Home",
    "Sports",
    "Books",
    "Toys",
    "Food",
    "Health",
]
COLORS = ["Red", "Blue", "Green", "Black", "White", "Gray", "Navy", "Brown"]
STATUSES = ["pending", "processing", "shipped", "delivered", "cancelled"]
PAYMENT_METHODS = ["credit_card", "debit_card", "paypal", "bank_transfer"]
EVENT_TYPES = [
    "page_view",
    "click",
    "purchase",
    "add_to_cart",
    "search",
    "login",
    "logout",
    "signup",
]
ENTITY_TYPES = ["product", "order", "customer", "page"]
BROWSERS = ["Chrome", "Firefox", "Safari", "Edge"]
DEVICES = ["mobile", "desktop", "tablet"]
REFERRERS = ["google.com", "facebook.com", "twitter.com", "direct", "email"]


def format_size(bytes_size):
    """Format bytes to human readable size"""
    for unit in ["B", "KB", "MB", "GB"]:
        if bytes_size < 1024:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024
    return f"{bytes_size:.2f} TB"


def format_duration(seconds):
    """Format seconds to human readable duration"""
    if seconds < 60:
        return f"{seconds:.1f}s"
    elif seconds < 3600:
        mins = seconds / 60
        return f"{mins:.1f}m"
    else:
        hours = seconds / 3600
        return f"{hours:.1f}h"


def print_progress(table_name, current, total, start_time, batch_count):
    """Print detailed progress information"""
    elapsed = time.time() - start_time
    percent = (current / total) * 100
    rate = current / elapsed if elapsed > 0 else 0
    eta = (total - current) / rate if rate > 0 else 0

    progress_bar_width = 30
    filled = int(progress_bar_width * current / total)
    bar = "=" * filled + ">" + " " * (progress_bar_width - filled - 1)

    print(
        f"\r  [{bar}] {percent:5.1f}% | "
        f"{current:,}/{total:,} rows | "
        f"{rate:,.0f} rows/s | "
        f"Batch #{batch_count} | "
        f"Elapsed: {format_duration(elapsed)} | "
        f"ETA: {format_duration(eta)}",
        end="",
        flush=True,
    )


def print_section_header(step, total_steps, title, count):
    """Print a section header for each generation phase"""
    print(f"\n{'=' * 70}")
    print(f"[{step}/{total_steps}] {title}")
    print(f"{'=' * 70}")
    print(f"  Target: {count:,} records")
    print(f"  Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()


def print_section_complete(table_name, count, start_time, estimated_size=None):
    """Print completion message for a section"""
    elapsed = time.time() - start_time
    rate = count / elapsed if elapsed > 0 else 0
    print()  # New line after progress bar
    print(f"  Completed: {count:,} {table_name} records")
    print(f"  Duration: {format_duration(elapsed)}")
    print(f"  Average rate: {rate:,.0f} rows/second")
    if estimated_size:
        print(f"  Estimated size: ~{format_size(estimated_size)}")
    print()


def get_connection():
    return mysql.connector.connect(**CONFIG)


def create_tables():
    """Create the test tables"""
    print("  Connecting to database...")
    conn = get_connection()
    cursor = conn.cursor()
    print("  Connection established")

    tables = [
        (
            "customers",
            """
        CREATE TABLE IF NOT EXISTS customers (
            customer_id INT PRIMARY KEY AUTO_INCREMENT,
            email VARCHAR(255) UNIQUE,
            first_name VARCHAR(100),
            last_name VARCHAR(100),
            phone VARCHAR(20),
            address TEXT,
            city VARCHAR(100),
            country VARCHAR(100),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        ),
        (
            "products",
            """
        CREATE TABLE IF NOT EXISTS products (
            product_id INT PRIMARY KEY AUTO_INCREMENT,
            sku VARCHAR(50) UNIQUE,
            name VARCHAR(200),
            description TEXT,
            category VARCHAR(100),
            price DECIMAL(10,2),
            stock_quantity INT DEFAULT 0,
            attributes JSON,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        ),
        (
            "orders",
            """
        CREATE TABLE IF NOT EXISTS orders (
            order_id BIGINT PRIMARY KEY AUTO_INCREMENT,
            customer_id INT NOT NULL,
            order_date DATETIME DEFAULT CURRENT_TIMESTAMP,
            total_amount DECIMAL(12,2),
            status VARCHAR(20) DEFAULT 'pending',
            shipping_address TEXT,
            payment_method VARCHAR(50),
            notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            INDEX idx_customer (customer_id),
            INDEX idx_date (order_date),
            INDEX idx_status (status)
        )
        """,
        ),
        (
            "order_items",
            """
        CREATE TABLE IF NOT EXISTS order_items (
            item_id BIGINT PRIMARY KEY AUTO_INCREMENT,
            order_id BIGINT NOT NULL,
            product_id INT NOT NULL,
            product_name VARCHAR(200),
            quantity INT DEFAULT 1,
            unit_price DECIMAL(10,2),
            discount DECIMAL(5,2) DEFAULT 0,
            INDEX idx_order (order_id)
        )
        """,
        ),
        (
            "event_logs",
            """
        CREATE TABLE IF NOT EXISTS event_logs (
            event_id BIGINT PRIMARY KEY AUTO_INCREMENT,
            event_type VARCHAR(50),
            entity_type VARCHAR(50),
            entity_id BIGINT,
            event_data JSON,
            user_agent TEXT,
            ip_address VARCHAR(45),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            INDEX idx_type (event_type),
            INDEX idx_created (created_at)
        )
        """,
        ),
    ]

    for table_name, table_sql in tables:
        print(f"  Creating table '{table_name}'...")
        cursor.execute(table_sql)
        print(f"    Table '{table_name}' ready")

    conn.commit()
    cursor.close()
    conn.close()
    print("  All tables created successfully")


def generate_customers(count=100000, batch_size=5000):
    """Generate customer records"""
    start_time = time.time()
    print("  Connecting to database...")
    conn = get_connection()
    cursor = conn.cursor()
    print("  Connection established")
    print(f"  Batch size: {batch_size:,} records")
    print()

    sql = """INSERT INTO customers (email, first_name, last_name, phone, address, city, country)
             VALUES (%s, %s, %s, %s, %s, %s, %s)"""

    total_inserted = 0
    batch = []
    batch_count = 0

    for i in range(1, count + 1):
        record = (
            f"user{i}_{random.randint(1000, 9999)}@example.com",
            random.choice(FIRST_NAMES),
            random.choice(LAST_NAMES),
            f"+1-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
            f"{random.randint(1, 9999)} {random.choice(STREETS)} {random.choice(STREET_TYPES)}",
            random.choice(CITIES),
            "USA",
        )
        batch.append(record)

        if len(batch) >= batch_size:
            batch_count += 1
            cursor.executemany(sql, batch)
            conn.commit()
            total_inserted += len(batch)
            print_progress("customers", total_inserted, count, start_time, batch_count)
            batch = []

    if batch:
        batch_count += 1
        cursor.executemany(sql, batch)
        conn.commit()
        total_inserted += len(batch)
        print_progress("customers", total_inserted, count, start_time, batch_count)

    cursor.close()
    conn.close()
    # Estimate ~200 bytes per customer record
    print_section_complete("customer", total_inserted, start_time, total_inserted * 200)


def generate_products(count=50000, batch_size=5000):
    """Generate product records"""
    start_time = time.time()
    print("  Connecting to database...")
    conn = get_connection()
    cursor = conn.cursor()
    print("  Connection established")
    print(f"  Batch size: {batch_size:,} records")
    print()

    sql = """INSERT INTO products (sku, name, description, category, price, stock_quantity, attributes)
             VALUES (%s, %s, %s, %s, %s, %s, %s)"""

    prefixes = ["Premium", "Standard", "Deluxe", "Basic", "Pro", "Ultra", "Classic"]
    items = [
        "Widget",
        "Gadget",
        "Device",
        "Tool",
        "Component",
        "Module",
        "Unit",
        "System",
        "Kit",
    ]
    suffixes = ["Alpha", "Beta", "Gamma", "Delta", "Omega", "Plus", "Max", "Mini"]

    total_inserted = 0
    batch = []
    batch_count = 0

    for i in range(1, count + 1):
        attributes = json.dumps(
            {
                "weight": round(0.1 + random.random() * 10, 2),
                "color": random.choice(COLORS),
                "material": random.choice(
                    ["Metal", "Plastic", "Wood", "Fabric", "Glass"]
                ),
                "dimensions": f"{random.randint(5, 50)}x{random.randint(5, 50)}x{random.randint(5, 50)}cm",
            }
        )

        record = (
            f"SKU-{i:08d}",
            f"{random.choice(prefixes)} {random.choice(items)} {random.choice(suffixes)}",
            f"High-quality product. " + "Lorem ipsum dolor sit amet. " * 10,
            random.choice(CATEGORIES),
            round(10 + random.random() * 990, 2),
            random.randint(0, 1000),
            attributes,
        )
        batch.append(record)

        if len(batch) >= batch_size:
            batch_count += 1
            cursor.executemany(sql, batch)
            conn.commit()
            total_inserted += len(batch)
            print_progress("products", total_inserted, count, start_time, batch_count)
            batch = []

    if batch:
        batch_count += 1
        cursor.executemany(sql, batch)
        conn.commit()
        total_inserted += len(batch)
        print_progress("products", total_inserted, count, start_time, batch_count)

    cursor.close()
    conn.close()
    # Estimate ~500 bytes per product record
    print_section_complete("product", total_inserted, start_time, total_inserted * 500)


def generate_orders(count=2000000, batch_size=5000, max_customer_id=100000):
    """Generate order records"""
    start_time = time.time()
    print("  Connecting to database...")
    conn = get_connection()
    cursor = conn.cursor()
    print("  Connection established")
    print(f"  Batch size: {batch_size:,} records")
    print(f"  Customer ID range: 1 to {max_customer_id:,}")
    print()

    sql = """INSERT INTO orders (customer_id, order_date, total_amount, status, shipping_address, payment_method, notes)
             VALUES (%s, %s, %s, %s, %s, %s, %s)"""

    total_inserted = 0
    batch = []
    batch_count = 0
    base_date = datetime.now()

    for i in range(1, count + 1):
        order_date = base_date - timedelta(
            days=random.randint(0, 365),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
        )
        record = (
            random.randint(1, max_customer_id),
            order_date,
            round(50 + random.random() * 500, 2),
            random.choice(STATUSES),
            f"{random.randint(1, 9999)} {random.choice(STREETS)} {random.choice(STREET_TYPES)}, Apt {random.randint(1, 500)}, {random.choice(CITIES)}",
            random.choice(PAYMENT_METHODS),
            f"Order notes: " + "Sample order details. " * 5,
        )
        batch.append(record)

        if len(batch) >= batch_size:
            batch_count += 1
            cursor.executemany(sql, batch)
            conn.commit()
            total_inserted += len(batch)
            print_progress("orders", total_inserted, count, start_time, batch_count)
            batch = []

    if batch:
        batch_count += 1
        cursor.executemany(sql, batch)
        conn.commit()
        total_inserted += len(batch)
        print_progress("orders", total_inserted, count, start_time, batch_count)

    cursor.close()
    conn.close()
    # Estimate ~300 bytes per order record
    print_section_complete("order", total_inserted, start_time, total_inserted * 300)


def generate_order_items(
    count=5000000, batch_size=10000, max_order_id=2000000, max_product_id=50000
):
    """Generate order item records"""
    start_time = time.time()
    print("  Connecting to database...")
    conn = get_connection()
    cursor = conn.cursor()
    print("  Connection established")
    print(f"  Batch size: {batch_size:,} records")
    print(f"  Order ID range: 1 to {max_order_id:,}")
    print(f"  Product ID range: 1 to {max_product_id:,}")
    print()

    sql = """INSERT INTO order_items (order_id, product_id, product_name, quantity, unit_price, discount)
             VALUES (%s, %s, %s, %s, %s, %s)"""

    prefixes = ["Premium", "Standard", "Deluxe", "Basic", "Pro"]
    items = ["Widget", "Gadget", "Device", "Tool", "Component"]

    total_inserted = 0
    batch = []
    batch_count = 0

    for i in range(1, count + 1):
        record = (
            random.randint(1, max_order_id),
            random.randint(1, max_product_id),
            f"{random.choice(prefixes)} {random.choice(items)}",
            random.randint(1, 5),
            round(10 + random.random() * 200, 2),
            round(random.random() * 20, 2),
        )
        batch.append(record)

        if len(batch) >= batch_size:
            batch_count += 1
            cursor.executemany(sql, batch)
            conn.commit()
            total_inserted += len(batch)
            print_progress(
                "order_items", total_inserted, count, start_time, batch_count
            )
            batch = []

    if batch:
        batch_count += 1
        cursor.executemany(sql, batch)
        conn.commit()
        total_inserted += len(batch)
        print_progress("order_items", total_inserted, count, start_time, batch_count)

    cursor.close()
    conn.close()
    # Estimate ~100 bytes per order item record
    print_section_complete(
        "order item", total_inserted, start_time, total_inserted * 100
    )


def generate_event_logs(count=3000000, batch_size=10000):
    """Generate event log records"""
    start_time = time.time()
    print("  Connecting to database...")
    conn = get_connection()
    cursor = conn.cursor()
    print("  Connection established")
    print(f"  Batch size: {batch_size:,} records")
    print()

    sql = """INSERT INTO event_logs (event_type, entity_type, entity_id, event_data, user_agent, ip_address)
             VALUES (%s, %s, %s, %s, %s, %s)"""

    total_inserted = 0
    batch = []
    batch_count = 0

    for i in range(1, count + 1):
        event_data = json.dumps(
            {
                "session_id": str(uuid.uuid4()),
                "referrer": random.choice(REFERRERS),
                "device": random.choice(DEVICES),
                "browser": random.choice(BROWSERS),
                "duration": random.randint(1, 300),
                "metadata": "x" * 100,
            }
        )

        record = (
            random.choice(EVENT_TYPES),
            random.choice(ENTITY_TYPES),
            random.randint(1, 1000000),
            event_data,
            f"Mozilla/5.0 ({random.choice(['Windows NT 10.0', 'Macintosh', 'Linux'])}) AppleWebKit/537.36",
            f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 255)}",
        )
        batch.append(record)

        if len(batch) >= batch_size:
            batch_count += 1
            cursor.executemany(sql, batch)
            conn.commit()
            total_inserted += len(batch)
            print_progress("event_logs", total_inserted, count, start_time, batch_count)
            batch = []

    if batch:
        batch_count += 1
        cursor.executemany(sql, batch)
        conn.commit()
        total_inserted += len(batch)
        print_progress("event_logs", total_inserted, count, start_time, batch_count)

    cursor.close()
    conn.close()
    # Estimate ~400 bytes per event log record
    print_section_complete(
        "event log", total_inserted, start_time, total_inserted * 400
    )


def check_data_size():
    """Check the total data size"""
    print("  Connecting to database...")
    conn = get_connection()
    cursor = conn.cursor()
    print("  Querying table statistics...")

    cursor.execute("""
        SELECT
            table_name,
            ROUND(data_length / 1024 / 1024, 2) AS data_mb,
            ROUND(index_length / 1024 / 1024, 2) AS index_mb,
            table_rows
        FROM information_schema.tables
        WHERE table_schema = 'cdc_test'
        ORDER BY data_length DESC
    """)

    print("\n" + "=" * 70)
    print(f"{'Table':<20} {'Data MB':<12} {'Index MB':<12} {'Rows':<15}")
    print("=" * 70)

    total_data = 0
    total_index = 0
    for row in cursor.fetchall():
        print(f"{row[0]:<20} {row[1]:<12} {row[2]:<12} {row[3]:<15,}")
        total_data += row[1] or 0
        total_index += row[2] or 0

    print("=" * 70)
    print(f"{'TOTAL':<20} {total_data:<12.2f} {total_index:<12.2f}")
    print(f"\nTotal Data Size: {format_size((total_data + total_index) * 1024 * 1024)}")

    cursor.close()
    conn.close()


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="TiDB Sample Data Generator for CDC Testing",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --mode small    Generate small dataset for testing (~10MB)
  %(prog)s --mode full     Generate full dataset for production (~3-5GB)
  %(prog)s                 Defaults to small mode
        """,
    )
    parser.add_argument(
        "--mode",
        "-m",
        choices=["small", "full"],
        default="small",
        help="Data generation mode: small (testing) or full (production). Default: small",
    )
    parser.add_argument(
        "--dry-run",
        "-n",
        action="store_true",
        help="Show what would be generated without actually generating data",
    )
    return parser.parse_args()


def main():
    args = parse_args()
    config = DATA_CONFIGS[args.mode]

    print("=" * 70)
    print("TiDB Sample Data Generator")
    print("=" * 70)
    print(f"\nMode: {args.mode.upper()}")
    print(f"Description: {config['description']}")
    print(f"\nPlanned data generation:")
    print(f"  - Customers:    {config['customers']:>10,} records")
    print(f"  - Products:     {config['products']:>10,} records")
    print(f"  - Orders:       {config['orders']:>10,} records")
    print(f"  - Order Items:  {config['order_items']:>10,} records")
    print(f"  - Event Logs:   {config['event_logs']:>10,} records")
    print(f"  - Batch Size:   {config['batch_size']:>10,} records")

    total_records = (
        config["customers"]
        + config["products"]
        + config["orders"]
        + config["order_items"]
        + config["event_logs"]
    )
    print(f"\n  Total records:  {total_records:>10,}")

    if args.dry_run:
        print("\n[DRY RUN] No data will be generated.")
        return

    print(f"\nStarted at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    start_time = time.time()

    # Create database first (run manually or uncomment)
    # conn = get_connection()
    # cursor = conn.cursor()
    # cursor.execute("CREATE DATABASE IF NOT EXISTS cdc_test")
    # conn.close()

    print_section_header(1, 6, "Creating Tables", 5)
    create_tables()

    print_section_header(2, 6, f"Generating Customers", config["customers"])
    generate_customers(config["customers"], config["batch_size"])

    print_section_header(3, 6, f"Generating Products", config["products"])
    generate_products(config["products"], config["batch_size"])

    print_section_header(4, 6, f"Generating Orders", config["orders"])
    generate_orders(
        config["orders"], config["batch_size"], max_customer_id=config["customers"]
    )

    print_section_header(5, 6, f"Generating Order Items", config["order_items"])
    # Use larger batch size for order items
    order_items_batch = (
        config["batch_size"] * 2 if args.mode == "full" else config["batch_size"]
    )
    generate_order_items(
        config["order_items"],
        order_items_batch,
        max_order_id=config["orders"],
        max_product_id=config["products"],
    )

    print_section_header(6, 6, f"Generating Event Logs", config["event_logs"])
    # Use larger batch size for event logs
    event_logs_batch = (
        config["batch_size"] * 2 if args.mode == "full" else config["batch_size"]
    )
    generate_event_logs(config["event_logs"], event_logs_batch)

    elapsed = time.time() - start_time

    print("\n" + "=" * 70)
    print("GENERATION COMPLETE")
    print("=" * 70)
    print(f"  Mode: {args.mode.upper()}")
    print(f"  Total records generated: {total_records:,}")
    print(f"  Total time: {format_duration(elapsed)}")
    print(f"  Average rate: {total_records / elapsed:,.0f} records/second")
    print(f"  Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

    print("\n" + "=" * 70)
    print("FINAL DATA SIZE")
    print("=" * 70)
    check_data_size()


if __name__ == "__main__":
    main()
