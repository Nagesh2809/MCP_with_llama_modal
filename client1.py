


    # client.py - Connect MCP Tools to LLM using ChatOllama in LangGraph
# Run the server first, then: python client.py
# Assumes you have Ollama running locally with a tool-calling model like llama3.
# Install required packages: pip install langchain-ollama langgraph langchain-mcp-adapters mcp

import asyncio
from langchain_ollama import ChatOllama
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent

async def main():
    # Connect to the MCP server using streamable HTTP transport
    client = MultiServerMCPClient(
        {
            "calc": {
                "transport": "streamable_http",
                "url": "http://localhost:8000/mcp/"  # Adjust port if different
            },
        }
    )

    # Load tools from MCP server
    tools = await client.get_tools()

    for tool in tools:
        print(f"Tool: {tool.name}")
        print(f"Description: {getattr(tool, 'description', '')}")
        
        # args_schema may be dict or Pydantic model, handle both
        args_schema = getattr(tool, 'args_schema', {})
        if hasattr(args_schema, 'schema'):
            print(f"Schema: {args_schema.schema()}\n")
        else:
            print(f"Schema: {args_schema}\n")



    # Initialize Ollama model via ChatOllama
    model = ChatOllama(model="llama3.1:8b-instruct-q4_0")  # Use your Ollama model that supports tool calling

    # Create a ReAct agent with the model and MCP tools
    agent = create_react_agent(model, tools)

    # Invoke the agent with a query that requires tool use
    # response = await agent.ainvoke(
    #     {"messages": [{"role": "user", "content": "What is (2 + 3) * 4?"}]}
    # )


    # # "Search for flights from New York to London on 2025-09-01"
    # response = await agent.ainvoke(
    #     {"messages": [{"role": "user", "content": "Search for flights from New York to London on 2025-09-01"}]}
    # )


    # # Print the response
    # print(response["messages"][-1].content)  # Final answer from the agent


    # Example 1: Flight search
    flight_query = "Search for flights from New York to London on 2025-09-01"
    flight_response = await agent.ainvoke({"messages": [{"role": "user", "content": flight_query}]})
    print(f"Flight Response: {flight_response['messages'][-1].content}")

    # Example 2: Weather query
    weather_query = "What is the weather in Paris today?"
    weather_response = await agent.ainvoke({"messages": [{"role": "user", "content": weather_query}]})
    print(f"Weather Response: {weather_response['messages'][-1].content}")



asyncio.run(main())



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
#                 "url": "http://localhost:8000/mcp/"
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
