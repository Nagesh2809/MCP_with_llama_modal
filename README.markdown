# Multi-Server MCP Application

This repository contains a Python-based application that integrates multiple MCP (Microservices Communication Protocol) servers using FastAPI, LangChain, and SQLAlchemy. The application provides tools for flight search, weather information, and student record management, with a client to interact with these services.

## Features
- **Flight Search**: Search for flights between cities on a specified date.
- **Weather Information**: Retrieve weather details for a given city.
- **Student Management**: Create and manage student records in a PostgreSQL database.
- **Multi-Server Architecture**: Combines multiple MCP servers under a single FastAPI application.
- **Client Interaction**: Uses LangChain and a ReAct agent to interact with the servers.

## Prerequisites
- Python 3.8+
- PostgreSQL database (configured with user `postgres` and password `1234`)
- Ollama running locally with a tool-calling model (e.g., `llama3.1:8b-instruct-q4_0`)
- Required Python packages:
  ```bash
  pip install fastapi uvicorn mcp langchain-ollama langgraph langchain-mcp-adapters sqlalchemy psycopg2-binary
  ```

## Project Structure
- `server.py`: Main FastAPI server that mounts MCP servers for flight and weather/student tools.
- `app_server.py`: MCP server for flight-related tools.
- `weather_server.py`: MCP server for weather and student management tools.
- `r_server.py`: Alternative MCP server for weather and student management (similar to `weather_server.py`).
- `client1.py`: Client script to interact with the MCP servers using LangChain and a ReAct agent.

## Setup Instructions

1. **Clone the Repository**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Set Up PostgreSQL Database**
   - Ensure PostgreSQL is running on `localhost:5432`.
   - Create a database named `nagesh`:
     ```sql
     CREATE DATABASE nagesh;
     ```
   - Update the `DATABASE_URL` in `weather_server.py` and `r_server.py` if your PostgreSQL credentials differ:
     ```python
     DATABASE_URL = "postgresql://postgres:1234@localhost:5432/nagesh"
     ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   *Note*: You may need to create a `requirements.txt` file with the listed dependencies or install them manually as shown in the prerequisites.

4. **Run the Servers**
   - Start the main FastAPI server:
     ```bash
     python server.py
     ```
     This runs the server on `http://localhost:8000`, mounting flight tools at `/echo` and weather/student tools at `/math`.

   - Alternatively, run individual MCP servers (if not using `server.py`):
     ```bash
     python app_server.py  # Runs FlightTools on port 8001
     python weather_server.py  # Runs WeatherTools/StudentTools on port 8002
     ```

5. **Run the Client**
   - Ensure Ollama is running locally with the specified model.
   - Run the client script to interact with the servers:
     ```bash
     python client1.py
     ```
   - The client demonstrates three example queries:
     - Flight search (e.g., "Search for flights from New York to London on 2025-09-01")
     - Weather query (e.g., "What is the weather in Paris today?")
     - Student creation (e.g., creating a student record with name, roll number, percentage, and class)

## Usage
- **Server**: The FastAPI server (`server.py`) combines multiple MCP servers under a single application. Access the root endpoint at `http://localhost:8000/` to verify it's running.
- **Client**: The `client1.py` script connects to the MCP servers (either locally or via deployed endpoints) and uses a ReAct agent to process queries. Modify the `client1.py` configuration to switch between local and remote server URLs.
- **Database**: Student records are stored in the `student` table in the `nagesh` PostgreSQL database. The `create_student_tool` ensures unique roll numbers and validates input using Pydantic.

## Example Queries
Run `client1.py` to execute the following example queries:
- **Flight Search**:
  ```plaintext
  Search for flights from New York to London on 2025-09-01
  ```
  *Response*: Placeholder response (e.g., "there is no flight avalibvle for this location").
- **Weather Query**:
  ```plaintext
  What is the weather in Paris today?
  ```
  *Response*: "The weather in Paris is sunny, 25°C."
- **Student Creation**:
  ```plaintext
  Create a student with the following details:
  - Name: John Doee
  - Roll Number: A1234
  - Percentage: 85.55
  - Class: 10Aa
  ```
  *Response*: Details of the created student or an error if the roll number already exists.

## Deployment
- The repository includes commented code in `client1.py` for connecting to deployed endpoints (e.g., on Render.com). To deploy:
  1. Deploy `server.py` to a hosting platform like Render or Heroku.
  2. Update the `url` fields in `client1.py` to point to your deployed endpoints (e.g., `https://your-deployment-url/echo/mcp`).
  3. Ensure the PostgreSQL database is accessible from the deployed server.

## Notes
- The `r_server.py` file is an alternative to `weather_server.py` with identical functionality. Use either based on your preference.
- The flight search tool currently returns a placeholder response. Extend `app_server.py` to integrate with a real flight API for production use.
- Ensure the Ollama model supports tool calling for the ReAct agent to work correctly.
- The database connection assumes a local PostgreSQL setup. Adjust `DATABASE_URL` for remote or different configurations.

## Contributing
Contributions are welcome! Please submit a pull request or open an issue for bugs, improvements, or new features.

