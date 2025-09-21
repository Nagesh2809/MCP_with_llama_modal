

# uvicorn server:app --host 0.0.0.0 --port 8000 --reload



import contextlib
from fastapi import FastAPI
import uvicorn

# Import MCP instances from your servers
from app_server import mcp as Flight
from weather_server import mcp as weather

# Create a combined lifespan to manage both session managers
@contextlib.asynccontextmanager
async def lifespan(app: FastAPI):
    async with contextlib.AsyncExitStack() as stack:
        # Start both MCP session managers
        await stack.enter_async_context(Flight.session_manager.run())
        await stack.enter_async_context(weather.session_manager.run())
        yield

# Create FastAPI app with custom lifespan
app = FastAPI(lifespan=lifespan)

# Mount each MCP server under a path
app.mount("/echo", Flight.streamable_http_app())
app.mount("/math", weather.streamable_http_app())




# Optional root endpoint
@app.get("/")
async def root():
    return {"status": "running"}

# Run the app
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
