from mcp.server.fastmcp import FastMCP

mcp = FastMCP("WeatherTools")

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

# if __name__ == "__main__":
#     mcp.run(transport="streamable-http")
if __name__ == "__main__":
    # Run on port 8001
    mcp.run(transport="streamable-http")
