

# Run the MCP servers first, then: python client.py
# Assumes you have Ollama running locally with a tool-calling model like llama3.
# Install required packages: pip install langchain-ollama langgraph langchain-mcp-adapters mcp

import asyncio
from langchain_ollama import ChatOllama
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

async def main():
    
#########################################################################################################################

    # for connecting with single MCP server using streamable HTTP transport
    # "http://localhost:8000/mcp/"
    # client = MultiServerMCPClient(
    #     {
    #         "calc": {
    #             "transport": "streamable_http",
    #             "url": "http://0.0.0.0:8000/mcp"  # Adjust port if different
    #         },
    #     }
    # )




#########################################################################################################################
# Run the both server on different port
# If you want to connect multiple  MCP servers  without mounting with FastAPI  then use different port for them
#     client = MultiServerMCPClient(
#         {
#             "flights": {
#                 "transport": "streamable_http",
#                 "url": "http://localhost:8002/mcp/"
#             },
#             "weather": {
#                 "transport": "streamable_http",
#                 "url": "http://localhost:8001/mcp/"
#             },
#         }
#     )


#########################################################################################################################

# when you will mount multiple server with FastAPI the use below code 

    client = MultiServerMCPClient(
        {
            "Flight": {
                "transport": "streamable_http",
                "url": "http://localhost:8000/echo/mcp"  # FlightTools mounted at /echo
            },
            "Weather": {
                "transport": "streamable_http",
                "url": "http://localhost:8000/math/mcp"  # WeatherTools mounted at /math
            },
        }
    )


    
#########################################################################################################################


# this are my deployed api on render.com you can deploy your and use
# for connecting with enpoints of  different MCP server   
#     client = MultiServerMCPClient(
#     {
#         "Flight": {
#             "transport": "streamable_http",
#             "url": "https://mcp-flight-weather-2.onrender.com/echo/mcp"
#         },
#         "Weather": {
#             "transport": "streamable_http",
#             "url": "https://mcp-flight-weather-2.onrender.com/math/mcp"
#         },
#     }
# )
    
#########################################################################################################################



    # Load tools from MCP server
    tools = await client.get_tools()

    #  it will show tool description
    # for tool in tools:
    #     print(f"Tool: {tool.name}")
    #     print(f"Description: {getattr(tool, 'description', '')}")
        
    #     # args_schema may be dict or Pydantic model, handle both
    #     args_schema = getattr(tool, 'args_schema', {})
    #     if hasattr(args_schema, 'schema'):
    #         print(f"Schema: {args_schema.schema()}\n")
    #     else:
    #         print(f"Schema: {args_schema}\n")



    # Initialize Ollama model via ChatOllama
    model = ChatOllama(model="llama3.1:8b-instruct-q4_0")  # Use your Ollama model that supports tool calling

    # Create a ReAct agent with the model and MCP tools
    agent = create_react_agent(model, tools)


    # Example 1: Flight search
    flight_query = "Search for flights from New York to London on 2025-09-01"
    flight_response = await agent.ainvoke({"messages": [{"role": "user", "content": flight_query}]})
    print(f"Flight Response: {flight_response['messages'][-1].content}")

    # Example 2: Weather query
    weather_query = "What is the weather in Paris today?"
    weather_response = await agent.ainvoke({"messages": [{"role": "user", "content": weather_query}]})
    print(f"Weather Response: {weather_response['messages'][-1].content}")


    student_query = """
    Create a student with the following details:
    - Name: John Doee
    - Roll Number: A1234
    - Percentage: 85.55
    - Class: 10Aa
    """
    student_response = await agent.ainvoke({"messages": [{"role": "user", "content": student_query}]})
    print(f" student_response: {student_response['messages'][-1].content}")



asyncio.run(main())


########################################################################################################################################

# # this code will connect will multiple server directly with different port 8001,8002

# import asyncio
# from langchain_ollama import ChatOllama
# from langchain_mcp_adapters.client import MultiServerMCPClient
# from langgraph.prebuilt import create_react_agent

# async def main():
#     # Connect to both MCP servers
#     client = MultiServerMCPClient(
#         {
#             "flights": {
#                 "transport": "streamable_http",
#                 "url": "http://localhost:8002/mcp/"
#             },
#             "weather": {
#                 "transport": "streamable_http",
#                 "url": "http://localhost:8001/mcp/"
#             },
#         }
#     )

#     # Load tools from all servers
#     tools = await client.get_tools()
#     for tool in tools:
#         print(f"Tool: {tool.name}")
#         print(f"Description: {getattr(tool, 'description', '')}")
#         args_schema = getattr(tool, "args_schema", {})
#         if hasattr(args_schema, "schema"):
#             print(f"Schema: {args_schema.schema()}\n")
#         else:
#             print(f"Schema: {args_schema}\n")

#     # Initialize Ollama model
#     model = ChatOllama(model="llama3.1:8b-instruct-q4_0")

#     # Create a ReAct agent with all tools
#     agent = create_react_agent(model, tools)

#     # Example 1: Flight search
#     flight_query = "Search for flights from New York to London on 2025-09-01"
#     flight_response = await agent.ainvoke({"messages": [{"role": "user", "content": flight_query}]})
#     print(f"Flight Response: {flight_response['messages'][-1].content}")

#     # Example 2: Weather query
#     weather_query = "What is the weather in Paris today?"
#     weather_response = await agent.ainvoke({"messages": [{"role": "user", "content": weather_query}]})
#     print(f"Weather Response: {weather_response['messages'][-1].content}")

# asyncio.run(main())
