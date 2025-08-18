# # server.py - MCP Server with Streamable HTTP Transport and Tools
# # Run this first: python server.py
# # Assumes you have installed: pip install mcp fastapi uvicorn (if needed, but mcp.run handles the server)
# # Note: MCP runs the HTTP server on port 8000 by default; check output for port.

# from mcp.server.fastmcp import FastMCP

# mcp = FastMCP("Calculator")

# @mcp.tool()
# def add(a: int, b: int) -> int:
#     """Adds two numbers."""
#     return a + b

# @mcp.tool()
# def multiply(a: int, b: int) -> int:
#     """Multiplies two numbers."""
#     return a * b



# @mcp.tool()
# def weather(city: str) -> str:
#     """Returns the current weather of a city."""
#     return f"The weather in {city} is sunny, 25°C."


# if __name__ == "__main__":
#     mcp.run(transport="streamable-http")




from mcp.server.fastmcp import FastMCP

mcp = FastMCP("FlightTools")

flight_tool_def = {
    "name": "searchFlights",
    "description": "Search for available flights",
    "inputSchema": {
        "type": "object",
        "properties": {
            "origin": {"type": "string"},
            "destination": {"type": "string"},
            "date": {"type": "string", "format": "date"}
        },
        "required": ["origin", "destination", "date"]
    }
}

@mcp.tool(name=flight_tool_def["name"], description=flight_tool_def["description"])
def search_flights(origin: str, destination: str, date: str):
    """Searches flights from origin to destination on the given date."""
    # Placeholder response
    return "there is no flight avalibvle for this location"


Weather_tool_def = {
    "name": "getWeather",
    "description": "Get weather information for a city",
    "inputSchema": {
        "type": "object",
        "properties": {
            "city": {"type": "string"}
        },
        "required": ["city"]
    }
}

@mcp.tool(name=Weather_tool_def["name"], description=Weather_tool_def["description"])
def get_weather(city: str):
    """Returns weather information for a given city."""
    return f"The weather in {city} is sunny with 25°C"

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
