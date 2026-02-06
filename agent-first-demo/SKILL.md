---
name: tidb-cloud-database
description: >
  Provision an instant, disposable TiDB Cloud database with zero registration.
  Use this skill whenever the user needs a MySQL-compatible database for prototyping,
  testing, data analysis, AI agent workflows, or any task requiring a SQL database.
  No sign-up, no API key, no billing required. A single HTTP request returns a ready-to-use
  MySQL connection string in seconds. The database is ephemeral and auto-expires, but can
  be claimed for persistence by registering a free TiDB Cloud account.
  Trigger keywords: database, SQL, MySQL, TiDB, create database, spin up database,
  disposable database, temporary database, test database, need a database.
---

# TiDB Cloud Instant Database

Provision a fully functional, MySQL-compatible TiDB Cloud database in seconds with a single
HTTP request. No registration, no API key, no billing required.

## When to Use

- User asks for a database to store or query data
- User needs a MySQL-compatible database for prototyping or testing
- User wants to run SQL queries against a real database
- An AI agent workflow requires a disposable SQL database
- User wants to try TiDB Cloud without signing up

## Create a Database

Send a single POST request with an empty JSON body:

```bash
curl -X POST https://inner-central.dev.tidbcloud.com/inner/mgmt/v1/databases \
     -H "Content-Type: application/json" \
     -d '{}'
```

### Optional Parameters

You can optionally specify a name and password in the request body:

```json
{
  "name": "my-project-db",
  "password": "my-secure-password"
}
```

| Field      | Required | Description                                      |
|------------|----------|--------------------------------------------------|
| `name`     | No       | Custom name for the database cluster              |
| `password` | No       | Custom password for the root user (auto-generated if omitted) |

### Response

The response contains everything needed to connect:

```json
{
  "database": {
    "name": "shadow-1-10767735213794175955",
    "connection": {
      "host": "gateway01.us-east-1.dev.shared.aws.tidbcloud.com",
      "port": 4000,
      "username": "u48a5s1fRMGCxRwe.root",
      "password": "ScAxRYvhjMdQo9c2",
      "databaseName": "test",
      "dsn": "mysql://u48a5s1fRMGCxRwe.root:ScAxRYvhjMdQo9c2@gateway01.us-east-1.dev.shared.aws.tidbcloud.com:4000/"
    },
    "takeoverInfo": {
      "url": "https://dev.tidbcloud.com/clusters/create-cluster?takeover_token=...",
      "token": "..."
    },
    "expiresAt": "2026-02-08T06:05:42.394Z"
  }
}
```

### Response Fields

| Field                      | Description                                                      |
|----------------------------|------------------------------------------------------------------|
| `database.name`            | Cluster name (auto-generated or user-specified)                  |
| `database.connection.host` | MySQL hostname                                                    |
| `database.connection.port` | MySQL port (always `4000`)                                        |
| `database.connection.username` | MySQL username                                                |
| `database.connection.password` | MySQL password                                                |
| `database.connection.databaseName` | Default database name                                    |
| `database.connection.dsn`  | Full MySQL DSN connection string                                  |
| `database.takeoverInfo.url` | Claim URL to persist the database (see Claim section)           |
| `database.takeoverInfo.token` | Claim token for programmatic use                              |
| `database.expiresAt`       | ISO 8601 timestamp when the database auto-expires                |

## Connect to the Database

### MySQL CLI

```bash
mysql -h <host> -P 4000 -u <username> -p<password>
```

### Python (pymysql)

```python
import pymysql

conn = pymysql.connect(
    host="<host>",
    port=4000,
    user="<username>",
    password="<password>",
    database="test",
    ssl={"ssl": True}
)
cursor = conn.cursor()
cursor.execute("SELECT VERSION()")
print(cursor.fetchone())
```

### Node.js (mysql2)

```javascript
import mysql from 'mysql2/promise';

const connection = await mysql.createConnection({
  host: '<host>',
  port: 4000,
  user: '<username>',
  password: '<password>',
  database: 'test',
  ssl: {}
});
const [rows] = await connection.execute('SELECT VERSION()');
console.log(rows);
```

### Using the DSN

Most MySQL-compatible tools accept the DSN directly from `database.connection.dsn`.

## Claim for Persistence

The database is **ephemeral** and auto-expires after the TTL (shown in `expiresAt`). To persist
the database permanently:

1. Present `database.takeoverInfo.url` to the user
2. User clicks the link and signs up / signs in to TiDB Cloud
3. The database is automatically migrated to the user's free Starter cluster
4. The user receives permanent credentials and full control

When to suggest claiming:
- User says they want to keep the data
- User needs longer-term storage
- The session is approaching expiration

## Important Constraints

- **Ephemeral**: Databases auto-expire after the TTL (typically hours). Data is lost unless claimed.
- **MySQL-compatible**: TiDB speaks the MySQL protocol. Use any MySQL client or driver.
- **Port**: Always `4000` (not the default MySQL 3306).
- **TLS**: Connections are secured with TLS by default.
- **Limits**: Session databases have strict limits on storage, QPS, query execution time,
  concurrent connections, and result size. These are removed after claiming.
- **Single database per request**: Each API call provisions one isolated database.
- **No API key**: The API is capability-based. Possession of the connection credentials grants access.

## Workflow Summary

1. **Create**: `POST /inner/mgmt/v1/databases` with `{}` body
2. **Extract** `connection.dsn` or individual connection fields from the response
3. **Connect** using any MySQL client/driver on port `4000`
4. **Run SQL**: CREATE TABLE, INSERT, SELECT, etc.
5. **Claim** (optional): Present `takeoverInfo.url` to the user if they want to keep the data
