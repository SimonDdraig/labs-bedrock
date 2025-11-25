import os
import json
import requests
from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio

server = Server("news-api")

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="fetch_news",
            description="Fetch news from external API using OAuth authentication",
            inputSchema={
                "type": "object",
                "properties": {},
                "required": []
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name != "fetch_news":
        raise ValueError(f"Unknown tool: {name}")
    
    oauth_token = os.environ.get('OAUTH_TOKEN')
    api_url = os.environ.get('API_URL')
    
    if not oauth_token or not api_url:
        return [TextContent(type="text", text=json.dumps({"error": "Missing OAUTH_TOKEN or API_URL"}))]
    
    headers = {
        'Authorization': f'Bearer {oauth_token}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        return [TextContent(type="text", text=json.dumps(response.json()))]
    except Exception as e:
        return [TextContent(type="text", text=json.dumps({"error": str(e)}))]

async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
