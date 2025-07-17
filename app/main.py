from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from api import books, genres, authors
from fastapi.responses import HTMLResponse
from pathlib import Path
from environment import ( FAIL_LIVENESS, FAIL_READINESS, DELAY_STARTUP)
import socket
import random
import time

# For testing purposes, K8s Probes
delay_startup = DELAY_STARTUP == 'true'
fail_liveness = FAIL_LIVENESS == 'true'
fail_readiness = random.random() < 0.5 if FAIL_READINESS == 'false' else False

print(f"Delay startup: {delay_startup}")
print(f"Fail liveness: {fail_liveness}")    
print(f"Fail readiness: {fail_readiness}")


app = FastAPI()

# Serve static content
app.mount("/static",StaticFiles(directory='static'), name='static')

# Hostname endpoint
@app.get("/api/hostname")
async def get_hostname():
    hostname = socket.gethostname()
    return {"hostname": hostname}

# Readiness and liveness endpoints
@app.get("/ready")
async def readiness_check():
    if fail_readiness:
        raise HTTPException(status_code=503, detail="Service is not ready")
    return {"status": "ready", "message": "Service is ready"}

@app.get("/up")
async def readiness_check():
    return {"status": "Up", "message": "Service is Up"}

@app.get("/health")
async def liveness_check():
    if fail_liveness:
        raise HTTPException(status_code=503, detail="Service is not healthy")
    return {"status": "healthy", "message": "Service is healthy"}


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
app.include_router(books.router)
app.include_router(genres.router)
app.include_router(authors.router)


