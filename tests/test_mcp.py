import asyncio
from fastmcp import Client
from langchain.mcp import MCPAdapter


async def main():
    client = Client(
        "https://mcp.zepto.co.in/mcp",
        auth="oauth",
    )

    async with MCPAdapter(client) as adapter:
        allowed = {
            "search_products",
            "get_product_details",
            "get_product_details",
            "view_cart",
            "update_cart",
            "get_order_detail",
            "list_order_history",
            "get_past_order_items"
        }
        tools = [
            tool for tool in await adapter.list_tools()
            if tool.name in allowed
        ]
        print([tool.name for tool in tools])


if __name__ == "__main__":
    asyncio.run(main())