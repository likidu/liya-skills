#!/usr/bin/env python3
"""
TiDB CDC Event Generator
Generates INSERT, UPDATE, DELETE operations for testing changefeed

Usage:
    python cdc_event_generator.py --mode continuous --rate 10     # Continuous mode at 10 events/sec
    python cdc_event_generator.py --mode burst --count 1000       # Burst mode with 1000 events
    python cdc_event_generator.py                                 # Defaults to continuous mode

Environment:
    Copy .env.sample to .env and configure your TiDB connection settings.
"""

import argparse
import json
import os
import random
import time
import uuid
from datetime import datetime, timedelta
from pathlib import Path
from threading import Thread

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

# Data pools for generating realistic data
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
    "David",
    "Sarah",
    "Richard",
    "Emma",
    "Joseph",
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
    "Wilson",
    "Anderson",
    "Taylor",
    "Thomas",
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
    "Seattle",
    "Denver",
    "Boston",
    "Miami",
]
STATUSES = ["pending", "processing", "shipped", "delivered", "cancelled"]
PAYMENT_METHODS = [
    "credit_card",
    "debit_card",
    "paypal",
    "bank_transfer",
    "apple_pay",
    "google_pay",
]
EVENT_TYPES = [
    "page_view",
    "click",
    "purchase",
    "add_to_cart",
    "search",
    "login",
    "logout",
    "signup",
    "wishlist_add",
    "review_submit",
]
ENTITY_TYPES = ["product", "order", "customer", "page", "category"]
BROWSERS = ["Chrome", "Firefox", "Safari", "Edge", "Opera"]
DEVICES = ["mobile", "desktop", "tablet"]


def get_connection():
    """Create a new database connection"""
    return mysql.connector.connect(**CONFIG)


def get_max_ids():
    """Get current max IDs from each table"""
    conn = get_connection()
    cursor = conn.cursor()

    ids = {}
    tables = {
        "customers": "customer_id",
        "products": "product_id",
        "orders": "order_id",
        "order_items": "item_id",
        "event_logs": "event_id",
    }

    for table, id_col in tables.items():
        cursor.execute(f"SELECT MAX({id_col}) FROM {table}")
        result = cursor.fetchone()[0]
        ids[table] = result if result else 0

    cursor.close()
    conn.close()
    return ids


class CDCEventGenerator:
    def __init__(self, events_per_second=10):
        self.events_per_second = events_per_second
        self.running = False
        self.stats = {"inserts": 0, "updates": 0, "deletes": 0, "errors": 0}
        self.max_ids = get_max_ids()
        print(f"Current max IDs: {self.max_ids}")

    def insert_customer(self, cursor):
        """Insert a new customer"""
        sql = """INSERT INTO customers (email, first_name, last_name, phone, address, city, country)
                 VALUES (%s, %s, %s, %s, %s, %s, %s)"""

        unique_id = uuid.uuid4().hex[:8]
        values = (
            f"new_user_{unique_id}@example.com",
            random.choice(FIRST_NAMES),
            random.choice(LAST_NAMES),
            f"+1-{random.randint(100, 999)}-{random.randint(1000, 9999)}",
            f"{random.randint(1, 9999)} {random.choice(['Main', 'Oak', 'Pine', 'Maple'])} St",
            random.choice(CITIES),
            "USA",
        )
        cursor.execute(sql, values)
        return cursor.lastrowid

    def insert_order(self, cursor):
        """Insert a new order"""
        sql = """INSERT INTO orders (customer_id, order_date, total_amount, status, shipping_address, payment_method, notes)
                 VALUES (%s, %s, %s, %s, %s, %s, %s)"""

        values = (
            random.randint(1, max(1, self.max_ids["customers"])),
            datetime.now(),
            round(50 + random.random() * 500, 2),
            "pending",
            f"{random.randint(1, 9999)} {random.choice(['Main', 'Oak', 'Pine'])} St, {random.choice(CITIES)}",
            random.choice(PAYMENT_METHODS),
            f"New order placed at {datetime.now().isoformat()}",
        )
        cursor.execute(sql, values)
        return cursor.lastrowid

    def insert_order_item(self, cursor, order_id=None):
        """Insert a new order item"""
        sql = """INSERT INTO order_items (order_id, product_id, product_name, quantity, unit_price, discount)
                 VALUES (%s, %s, %s, %s, %s, %s)"""

        if order_id is None:
            order_id = random.randint(1, max(1, self.max_ids["orders"]))

        values = (
            order_id,
            random.randint(1, max(1, self.max_ids["products"])),
            f"{random.choice(['Premium', 'Standard', 'Deluxe'])} {random.choice(['Widget', 'Gadget', 'Device'])}",
            random.randint(1, 5),
            round(10 + random.random() * 200, 2),
            round(random.random() * 15, 2),
        )
        cursor.execute(sql, values)
        return cursor.lastrowid

    def insert_event_log(self, cursor):
        """Insert a new event log"""
        sql = """INSERT INTO event_logs (event_type, entity_type, entity_id, event_data, user_agent, ip_address)
                 VALUES (%s, %s, %s, %s, %s, %s)"""

        event_data = json.dumps(
            {
                "session_id": str(uuid.uuid4()),
                "referrer": random.choice(
                    ["google.com", "facebook.com", "direct", "email"]
                ),
                "device": random.choice(DEVICES),
                "browser": random.choice(BROWSERS),
                "timestamp": datetime.now().isoformat(),
            }
        )

        values = (
            random.choice(EVENT_TYPES),
            random.choice(ENTITY_TYPES),
            random.randint(1, 1000000),
            event_data,
            f"Mozilla/5.0 ({random.choice(['Windows', 'Mac', 'Linux'])}) {random.choice(BROWSERS)}",
            f"{random.randint(1, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(1, 255)}",
        )
        cursor.execute(sql, values)
        return cursor.lastrowid

    def update_order_status(self, cursor):
        """Update order status - simulates order lifecycle"""
        status_flow = {
            "pending": "processing",
            "processing": "shipped",
            "shipped": "delivered",
        }

        # Pick a random status to transition from
        from_status = random.choice(["pending", "processing", "shipped"])
        to_status = status_flow[from_status]

        sql = """UPDATE orders
                 SET status = %s, updated_at = NOW(), notes = CONCAT(notes, %s)
                 WHERE status = %s
                 LIMIT 1"""

        note = f"\n[{datetime.now().isoformat()}] Status changed to {to_status}"
        cursor.execute(sql, (to_status, note, from_status))
        return cursor.rowcount

    def update_product_stock(self, cursor):
        """Update product stock quantity"""
        sql = """UPDATE products
                 SET stock_quantity = stock_quantity + %s
                 WHERE product_id = %s"""

        product_id = random.randint(1, max(1, self.max_ids["products"]))
        quantity_change = random.randint(-10, 50)
        cursor.execute(sql, (quantity_change, product_id))
        return cursor.rowcount

    def update_customer_address(self, cursor):
        """Update customer address"""
        sql = """UPDATE customers
                 SET address = %s, city = %s
                 WHERE customer_id = %s"""

        customer_id = random.randint(1, max(1, self.max_ids["customers"]))
        new_address = f"{random.randint(1, 9999)} {random.choice(['New', 'Updated', 'Changed'])} {random.choice(['Main', 'Oak', 'Pine'])} St"
        cursor.execute(sql, (new_address, random.choice(CITIES), customer_id))
        return cursor.rowcount

    def delete_cancelled_orders(self, cursor):
        """Delete old cancelled orders"""
        sql = """DELETE FROM orders
                 WHERE status = 'cancelled'
                 AND order_date < DATE_SUB(NOW(), INTERVAL 30 DAY)
                 LIMIT 1"""
        cursor.execute(sql)
        return cursor.rowcount

    def delete_old_event_logs(self, cursor):
        """Delete old event logs"""
        sql = """DELETE FROM event_logs
                 WHERE created_at < DATE_SUB(NOW(), INTERVAL 90 DAY)
                 LIMIT 5"""
        cursor.execute(sql)
        return cursor.rowcount

    def generate_single_event(self):
        """Generate a single CDC event (INSERT, UPDATE, or DELETE)"""
        conn = get_connection()
        cursor = conn.cursor()

        try:
            # Weighted random choice: 60% INSERT, 30% UPDATE, 10% DELETE
            operation = random.choices(
                ["insert", "update", "delete"], weights=[60, 30, 10]
            )[0]

            if operation == "insert":
                # Choose which table to insert into
                table = random.choices(
                    ["order", "order_item", "event_log", "customer"],
                    weights=[30, 30, 35, 5],
                )[0]

                if table == "order":
                    order_id = self.insert_order(cursor)
                    # Also insert 1-3 order items for this order
                    for _ in range(random.randint(1, 3)):
                        self.insert_order_item(cursor, order_id)
                elif table == "order_item":
                    self.insert_order_item(cursor)
                elif table == "event_log":
                    self.insert_event_log(cursor)
                elif table == "customer":
                    self.insert_customer(cursor)

                self.stats["inserts"] += 1

            elif operation == "update":
                update_type = random.choices(
                    ["order_status", "product_stock", "customer_address"],
                    weights=[50, 30, 20],
                )[0]

                if update_type == "order_status":
                    self.update_order_status(cursor)
                elif update_type == "product_stock":
                    self.update_product_stock(cursor)
                elif update_type == "customer_address":
                    self.update_customer_address(cursor)

                self.stats["updates"] += 1

            elif operation == "delete":
                delete_type = random.choice(["cancelled_orders", "old_events"])

                if delete_type == "cancelled_orders":
                    self.delete_cancelled_orders(cursor)
                else:
                    self.delete_old_event_logs(cursor)

                self.stats["deletes"] += 1

            conn.commit()

        except Exception as e:
            conn.rollback()
            self.stats["errors"] += 1
            print(f"Error: {e}")
        finally:
            cursor.close()
            conn.close()

    def run_continuous(self, duration_seconds=None):
        """Run continuous event generation"""
        self.running = True
        start_time = time.time()
        interval = 1.0 / self.events_per_second

        print(
            f"\nStarting CDC event generation at {self.events_per_second} events/second"
        )
        print("Press Ctrl+C to stop\n")

        event_count = 0
        last_report_time = start_time

        try:
            while self.running:
                if duration_seconds and (time.time() - start_time) >= duration_seconds:
                    break

                self.generate_single_event()
                event_count += 1

                # Print stats every 10 seconds
                if time.time() - last_report_time >= 10:
                    elapsed = time.time() - start_time
                    rate = event_count / elapsed
                    print(
                        f"[{elapsed:.0f}s] Events: {event_count} | Rate: {rate:.1f}/s | "
                        f"INS: {self.stats['inserts']} | UPD: {self.stats['updates']} | "
                        f"DEL: {self.stats['deletes']} | ERR: {self.stats['errors']}"
                    )
                    last_report_time = time.time()

                time.sleep(interval)

        except KeyboardInterrupt:
            print("\n\nStopping...")

        self.running = False
        elapsed = time.time() - start_time

        print("\n" + "=" * 60)
        print("Final Statistics")
        print("=" * 60)
        print(f"Duration: {elapsed:.1f} seconds")
        print(f"Total Events: {event_count}")
        print(f"Average Rate: {event_count / elapsed:.1f} events/second")
        print(f"Inserts: {self.stats['inserts']}")
        print(f"Updates: {self.stats['updates']}")
        print(f"Deletes: {self.stats['deletes']}")
        print(f"Errors: {self.stats['errors']}")

    def run_burst(self, event_count=1000):
        """Run a burst of events as fast as possible"""
        print(f"\nGenerating {event_count} events in burst mode...")
        start_time = time.time()

        for i in range(event_count):
            self.generate_single_event()
            if (i + 1) % 100 == 0:
                print(f"Progress: {i + 1}/{event_count}")

        elapsed = time.time() - start_time
        print(
            f"\nCompleted {event_count} events in {elapsed:.1f}s ({event_count / elapsed:.1f} events/s)"
        )
        print(
            f"Inserts: {self.stats['inserts']} | Updates: {self.stats['updates']} | Deletes: {self.stats['deletes']}"
        )


def main():
    parser = argparse.ArgumentParser(description="TiDB CDC Event Generator")
    parser.add_argument(
        "--mode",
        choices=["continuous", "burst"],
        default="continuous",
        help="Generation mode: continuous or burst",
    )
    parser.add_argument(
        "--rate", type=int, default=10, help="Events per second (continuous mode)"
    )
    parser.add_argument(
        "--duration",
        type=int,
        default=None,
        help="Duration in seconds (continuous mode, None=infinite)",
    )
    parser.add_argument(
        "--count", type=int, default=1000, help="Number of events (burst mode)"
    )

    args = parser.parse_args()

    generator = CDCEventGenerator(events_per_second=args.rate)

    if args.mode == "continuous":
        generator.run_continuous(duration_seconds=args.duration)
    else:
        generator.run_burst(event_count=args.count)


if __name__ == "__main__":
    main()
