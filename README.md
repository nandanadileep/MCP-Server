# MCP Server and Client Setup

This project demonstrates a simple Model Context Protocol (MCP) server and client implementation using `fastmcp` and `mcp_use`.

## Project Structure

```
MCP-Server/
├── simple_mcp_server.py          # Simple MCP server with an "add" tool
├── simple_mcp_server_config.json # Configuration for the server
├── simple_mcp_client.py          # Basic client for direct tool calls
├── simple_client.py              # Enhanced simple client with multiple tool tests
├── client.py                     # Advanced client with agent capabilities
├── mcp-env/                      # Virtual environment with dependencies
└── README.md                     # This file
```

## Setup

1. **Virtual Environment**: The project uses a virtual environment located in `mcp-env/`

2. **Dependencies**: The following packages are installed:
   - `fastmcp` - For creating MCP servers
   - `mcp_use` - For creating MCP clients and agents
   - `langchain-openai` - For OpenAI integration
   - `langchain-ollama` - For Ollama integration

## Usage

### 1. Simple Direct Tool Calls

The `simple_mcp_client.py` demonstrates basic direct tool calls:

```bash
python simple_mcp_client.py
```

### 2. Enhanced Simple Client

The `simple_client.py` provides a more comprehensive demonstration:

```bash
python simple_client.py
```

This will:
- List all available tools
- Test the "add" tool with multiple parameter sets
- Show clear success/failure indicators

### 3. Advanced Client with Agent Capabilities

The `client.py` demonstrates both direct tool calls and agent-based approaches:

```bash
python client.py
```

This will:
- Perform direct tool calls (works without LLM)
- Attempt agent-based approach if Ollama is available
- Provide helpful error messages and setup instructions

### 4. Using the Agent Approach

To use the agent approach with Ollama:

1. Install Ollama: https://ollama.ai/
2. Start Ollama: `ollama serve`
3. Pull the model: `ollama pull llama3.1:8b`
4. Run the client: `python client.py`

## Configuration

The `simple_mcp_server_config.json` file contains the server configuration:

```json
{
  "mcpServers": {
    "simple-server": {
      "command": "/Users/nandana/Documents/Projects/MCP-Server/mcp-env/bin/python",
      "args": ["simple_mcp_server.py"]
    }
  }
}
```

## Server Implementation

The `simple_mcp_server.py` implements a simple MCP server with an "add" tool:

```python
#!/usr/bin/env python3
from mcp.server.fastmcp import FastMCP

app = FastMCP("simple-server")

@app.tool()
def add(a: int, b: int) -> int:
    return a + b

if __name__ == "__main__":
    app.run()
```

## Client Examples

### Direct Tool Call Example

```python
import asyncio
from mcp_use import MCPClient

async def main():
    client = MCPClient("simple_mcp_server_config.json")
    
    try:
        session = await client.create_session("simple-server")
        result = await session.call_tool("add", {"a": 5, "b": 7})
        print(f"Result: {result.content[0].text}")
    finally:
        await client.close_all_sessions()

if __name__ == "__main__":
    asyncio.run(main())
```

### Enhanced Client Example

```python
import asyncio
from mcp_use import MCPClient
import json

async def main():
    with open("simple_mcp_server_config.json", "r") as f:
        config = json.load(f)

    client = MCPClient.from_dict(config)
    
    try:
        await client.create_all_sessions()
        
        for session_name in client.get_server_names():
            session = client.get_session(session_name)
            tools_response = await session.list_tools()
            tool_names = [tool.name for tool in tools_response]
            print(f"Available tools: {tool_names}")
            
            # Test tools
            for tool_name in tool_names:
                if tool_name == 'add':
                    result = await session.call_tool("add", {"a": 10, "b": 20})
                    print(f"add(10, 20) = {result.content[0].text}")
                    
    finally:
        await client.close_all_sessions()

if __name__ == "__main__":
    asyncio.run(main())
```

### Agent Example

```python
import asyncio
from mcp_use import MCPClient, MCPAgent
from langchain_ollama import ChatOllama

async def main():
    client = MCPClient("simple_mcp_server_config.json")
    await client.create_all_sessions()
    
    llm = ChatOllama(model="llama3.1:8b")
    agent = MCPAgent(llm=llm, client=client, max_steps=5)
    
    result = await agent.run("What is the result of 98765 + 98767?")
    print(result)
    
    await client.close_all_sessions()

if __name__ == "__main__":
    asyncio.run(main())
```

## Current Status

✅ **Working Features:**
- MCP server with "add" tool
- Direct tool calls via `mcp_use`
- Tool listing and discovery
- Multiple client implementations
- Proper error handling and cleanup

⚠️ **Requires Setup:**
- Ollama installation and model download for agent functionality
- OpenAI API key for OpenAI-based agents

## Troubleshooting

### Common Issues

1. **ModuleNotFoundError**: Make sure you're using the Python interpreter from the virtual environment:
   ```bash
   /Users/nandana/Documents/Projects/MCP-Server/mcp-env/bin/python your_script.py
   ```

2. **Connection Errors**: Ensure the server configuration points to the correct Python interpreter path.

3. **Agent Connection Issues**: 
   - For Ollama: Install Ollama and pull the required model
   - For OpenAI: Set the `OPENAI_API_KEY` environment variable

### Debug Mode

Enable debug mode for more verbose output:

```bash
DEBUG=1 python your_script.py
```

## Extending the Server

To add more tools to your server, simply add more functions with the `@app.tool()` decorator:

```python
@app.tool()
def multiply(a: int, b: int) -> int:
    return a * b

@app.tool()
def divide(a: float, b: float) -> float:
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
```

## Next Steps

1. **Add More Tools**: Extend the server with additional functionality
2. **Multiple Servers**: Configure multiple MCP servers in the configuration
3. **Custom Agents**: Build more sophisticated agents with different LLM providers
4. **Error Handling**: Add comprehensive error handling and retry logic
5. **Testing**: Add unit tests for your tools and integration tests for the client

## Resources

- [MCP Documentation](https://modelcontextprotocol.io/)
- [FastMCP Documentation](https://gofastmcp.com/)
- [MCP-Use Documentation](https://github.com/mcp-use/mcp-use)
- [LangChain Documentation](https://python.langchain.com/)
