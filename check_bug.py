"""Talks to bug_demo_server.py over stdio like a host would: tools/list, then the calls the video shows."""
import asyncio

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

CALLS = [
    ("list_tables", {}),
    ("describe_table", {"table": "orders"}),
    ("describe_table", {"table": "invoices"}),
    ("run_query", {"sql": "SELECT c.name, MAX(o.ordered_on) AS last_order FROM customers c JOIN orders o ON o.customer_id = c.id GROUP BY c.id HAVING last_order < '2026-10-01' ORDER BY last_order"}),
    ("run_query", {"sql": "DELETE FROM orders"}),
    ("run_query", {"sql": "DROP TABLE customers"}),
    ("run_query", {"sql": "SELECT 1; DELETE FROM orders"}),
    ("run_query", {"sql": "SELECT COUNT(*) AS orders_left FROM orders"}),
]


async def main() -> None:
    params = StdioServerParameters(command="uv", args=["run", "bug_demo_server.py"])
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await session.list_tools()
            for t in tools.tools:
                print("TOOL", t.name, "|", t.description.splitlines()[0], "|", t.input_schema.get("properties"))
            for name, args in CALLS:
                result = await session.call_tool(name, args)
                print("CALL", name, args, "->", [c.text for c in result.content])


asyncio.run(main())
