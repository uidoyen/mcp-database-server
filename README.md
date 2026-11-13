# MCP server for your database (Python, read-only)

A minimal [Model Context Protocol](https://modelcontextprotocol.io) server that lets Claude (or any MCP host) query a SQLite
database through three tools, `list_tables`, `describe_table` and `run_query`, over a connection that **cannot write**.
It's the code from the video **Build an MCP Server for Your Database in Python (Read-Only)**: https://youtu.be/ox2xk1gXLeM

```
Claude Desktop  --(MCP over stdio)-->  db_server.py  --(sqlite3, mode=ro)-->  shop.db
```

## Requirements

- Python 3.10 or newer
- [uv](https://docs.astral.sh/uv/)
- Claude Desktop, or any other MCP host

## Run it

```bash
uv sync
uv run python make_db.py      # creates shop.db: 5 made-up customers, 8 orders
uv run python check_client.py # lists the tools, then calls each one
```

Or try it in the MCP Inspector:

```bash
uv run mcp dev db_server.py
```

## Connect it to Claude Desktop

1. Find your full paths: `which uv` (on Windows `where uv`), and `pwd` in this folder.
2. Open Claude Desktop's config file (Settings, Developer, Edit Config) and add the `shop-db` entry from
   `claude_desktop_config.example.json`, with the full path to this folder (and the full path to `uv` if Claude can't find it).
3. Restart Claude Desktop. `shop-db` appears in the list of connectors. Ask: "Which customers placed their last order before
   October 1, 2026?"

## The three tools

| Tool | Does | Returns |
|---|---|---|
| `list_tables()` | lists the tables (its description says "Call this first") | table names, comma separated |
| `describe_table(table)` | columns and their types | `name TYPE` pairs, or "There is no table called ..." |
| `run_query(sql)` | runs one SQL statement | at most 50 rows, or the database's error as text |

## Why read-only matters

`run_query` runs whatever statement the model writes. The one line that makes it safe is the connection:

```python
sqlite3.connect(f"{DB.as_uri()}?mode=ro", uri=True)
```

With `mode=ro`, SQLite itself refuses every write: `DELETE FROM orders` comes back as
"The query failed: attempt to write a readonly database". Telling the model "never delete" is only a request; filtering the
word DELETE misses DROP and UPDATE. The lock is in the database connection, not in the prompt.

`bug_demo_server.py` is the same server with a normal, writable connection, for showing the risk:
`uv run python check_bug.py` deletes all 8 orders (and answers "No rows."). Run `make_db.py` again to restore them.
**Never point the bug demo at real data.**

## What it doesn't do

Read-only is the first step, not the whole job:
- There is no login, and the model sees every table in the file. Point it at a copy, or at a database that holds only what
  the model may see.
- On Postgres or MySQL, connect as a database user that can only read, so the database enforces the rule.
- A large query can still be slow; `run_query` returns at most 50 rows but doesn't limit the work.

## License

MIT
