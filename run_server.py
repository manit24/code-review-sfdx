from server import create_server

if __name__ == "__main__":
    mcp = create_server()
    mcp.run(
        transport="streamable-http",
        host="0.0.0.0",
        port=3333,
        path="/mcp"
    )