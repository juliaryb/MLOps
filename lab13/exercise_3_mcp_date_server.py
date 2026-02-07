from datetime import date, datetime
from fastmcp import FastMCP

# create MCP server
mcp = FastMCP("date-time-server")


@mcp.tool(description="Get current date in YYYY-MM-DD format")
def get_current_date() -> str:
    return date.today().isoformat()


@mcp.tool(description="Get current date and time in YYYY-MM-DDTHH:MM:SS format")
def get_current_datetime() -> str:
    return datetime.now().replace(microsecond=0).isoformat()


if __name__ == "__main__":
    mcp.run(transport="streamable-http", port=8002)