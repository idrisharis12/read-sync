from fastapi import FastAPI, Response
import uvicorn
from typing import List, Dict
from read_sync.library import db

app = FastAPI(title="read-sync", description="Headless manga/comic server and OPDS")

@app.on_event("startup")
def startup():
    db.init_db()

@app.get("/")
def read_root():
    return {"status": "read-sync server running", "version": "0.1.10"}

@app.get("/api/library", response_model=List[Dict])
def get_library():
    """Returns all manga currently in the user's library."""
    return db.get_library()

@app.get("/opds")
def opds_catalog():
    """Valid OPDS XML catalog endpoint for KOReader / Kavita."""
    library = db.get_library()
    
    # Generate OPDS XML Feed
    xml = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml += '<feed xmlns="http://www.w3.org/2005/Atom" xmlns:opds="http://opds-spec.org/2010/catalog">\n'
    xml += '  <id>urn:uuid:read-sync-library</id>\n'
    xml += '  <title>read-sync Local Library</title>\n'
    xml += '  <updated>2026-09-01T00:00:00Z</updated>\n'
    xml += '  <author><name>read-sync OPDS Server</name></author>\n'
    xml += '  <link rel="self" href="/opds" type="application/atom+xml;profile=opds-catalog;kind=acquisition"/>\n'
    xml += '  <link rel="start" href="/opds" type="application/atom+xml;profile=opds-catalog;kind=acquisition"/>\n'
    
    for manga in library:
        xml += '  <entry>\n'
        xml += f'    <id>urn:uuid:manga-{manga["id"]}</id>\n'
        xml += f'    <title>{manga["title"]}</title>\n'
        xml += f'    <updated>2026-09-01T00:00:00Z</updated>\n'
        xml += f'    <content type="text">{manga.get("description", "No description")}</content>\n'
        # In a real app, href points to the .cbz file download endpoint
        xml += f'    <link rel="http://opds-spec.org/acquisition" href="/api/download/{manga["id"]}" type="application/x-cbz"/>\n'
        xml += '  </entry>\n'
        
    xml += '</feed>'
    return Response(content=xml, media_type="application/atom+xml")

def run_server(port: int):
    print(f"Starting read-sync headless server on port {port}...")
    uvicorn.run(app, host="0.0.0.0", port=port, log_level="info")
