import asyncio
from mcp_use import MCPClient
import json

async def main():
    """Simple MCP client that demonstrates direct tool calls."""
    
    with open("simple_mcp_server_config.json", "r") as f:
        config = json.load(f)

    client = MCPClient.from_dict(config)
    
    try:
        await client.create_all_sessions()

        print("=== MCP Server Tools ===")
        for session_name in client.get_server_names():
            session = client.get_session(session_name)
            tools_response = await session.list_tools()
            tool_names = [tool.name for tool in tools_response]
            print(f"Available tools in '{session_name}': {tool_names}")
            
            # Test each available tool
            for tool_name in tool_names:
                if tool_name == 'add':
                    print(f"\nTesting {tool_name} tool...")
                    result = await session.call_tool("add", {"a": 10, "b": 20})
                    print(f"  {tool_name}(10, 20) = {result.content[0].text}")
                    
                    result2 = await session.call_tool("add", {"a": 100, "b": 200})
                    print(f"  {tool_name}(100, 200) = {result2.content[0].text}")
                    
                    result3 = await session.call_tool("add", {"a": 98765, "b": 98767})
                    print(f"  {tool_name}(98765, 98767) = {result3.content[0].text}")

        print("\n✅ All tool calls completed successfully!")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await client.close_all_sessions()
        print("🔌 Sessions closed.")

if __name__ == "__main__":
    asyncio.run(main())
