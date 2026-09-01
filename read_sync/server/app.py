from fastapi import FastAPI
import uvicorn
from typing import List, Dict
from read_sync.library import db

app = FastAPI(title="read-sync", description="Headless manga/comic server and OPDS")

@app.on_event("startup")
def startup():
    db.init_db()

@app.get("/")
def read_root():
    return {"status": "read-sync server running", "version": "0.1.0"}

@app.get("/api/library", response_model=List[Dict])
def get_library():
    """Returns all manga currently in the user's library."""
    return db.get_library()

@app.get("/opds")
def opds_catalog():
    """OPDS catalog endpoint for KOReader / Kavita."""
    return {
        "metadata": {"title": "read-sync OPDS Catalog"},
        "links": [{"rel": "self", "href": "/opds", "type": "application/atom+xml;profile=opds-catalog"}],
        "entries": []
    }

def run_server(port: int):
    print(f"Starting read-sync headless server on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
