from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api import health, api
from environment import ( DELAY_STARTUP)
import time
from fastapi.responses import HTMLResponse
from pathlib import Path

# For testing purposes, K8s Probes
delay_startup = DELAY_STARTUP == 'true'
print(f"Delay startup: {delay_startup}")

app = FastAPI()

# Serve static content
app.mount("/static",StaticFiles(directory='static'), name='static')
# Serve the index.html file
@app.get("/", response_class=HTMLResponse)
async def read_index():
    index_file_path = Path("static/index.html")
    return index_file_path.read_text()


# Delay startup endpoint
if delay_startup:
    start =  time.time()
    # Simulate a delay for startup, purposefully blocking event loop
    # to illustrate startup probes
    print(f"Delaying startup for seconds 60s")
    while time.time() - start < 60000:
        pass  

# Include router from endpoints
app.include_router(api.router)
app.include_router(health.router)
# app.include_router(books.router)
# app.include_router(genres.router)
# app.include_router(authors.router)

