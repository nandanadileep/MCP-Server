import asyncio
from mcp_use import MCPClient, MCPAgent
import json

async def main():
    with open("simple_mcp_server_config.json", "r") as f:
        config = json.load(f)

    client = MCPClient.from_dict(config)
    
    try:
        await client.create_all_sessions()

        # Check available tools via the session
        print("=== Available Tools ===")
        for session_name in client.get_server_names():
            session = client.get_session(session_name)
            tools_response = await session.list_tools()
            tool_names = [tool.name for tool in tools_response]
            print(f"Tools in session '{session_name}': {tool_names}")
            
            # Test a direct tool call
            if 'add' in tool_names:
                print(f"Testing direct tool call...")
                result = await session.call_tool("add", {"a": 5, "b": 7})
                print(f"Direct call result: {result.content[0].text}")

        # Try agent approach with Ollama
        print("\n=== Agent Approach with Ollama ===")
        try:
            from langchain_ollama import ChatOllama
            agent = MCPAgent(ChatOllama(model="llama3.1:8b"), client)
            result = await agent.run("What is the result of 98765 + 98767?")
            print(f"Agent result: {result}")
        except Exception as e:
            print(f"Ollama agent failed: {e}")
            print("\nTo use Ollama:")
            print("1. Install Ollama: https://ollama.ai/")
            print("2. Start Ollama: ollama serve")
            print("3. Pull the model: ollama pull llama3.1:8b")
            print("4. Run this script again")
            
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        await client.close_all_sessions()

if __name__ == "__main__":
    asyncio.run(main())
