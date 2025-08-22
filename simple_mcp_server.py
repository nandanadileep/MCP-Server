#!/usr/bin/env python3
from mcp.server.fastmcp import FastMCP

app = FastMCP("simple-server")

@app.tool()
def add(a: int, b: int) -> int:
    return a + b

if __name__ == "__main__":
    app.run()