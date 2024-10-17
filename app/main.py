from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from api import books, genres, authors
from fastapi.responses import HTMLResponse
from pathlib import Path
import socket
app = FastAPI()

# Serve static content
app.mount("/static",StaticFiles(directory='static'), name='static')


# Hostname endpoint
@app.get("/api/hostname")
async def get_hostname():
    hostname = socket.gethostname()
    return {"hostname": hostname}

# Serve the index.html file
@app.get("/", response_class=HTMLResponse)
async def read_index():
    index_file_path = Path("static/index.html")
    return index_file_path.read_text()

# Include router from endpoints
app.include_router(books.router)
app.include_router(genres.router)
app.include_router(authors.router)


