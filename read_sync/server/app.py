from fastapi import FastAPI
import uvicorn

app = FastAPI(title="read-sync", description="Headless manga/comic server and OPDS")

@app.get("/")
def read_root():
    return {"status": "read-sync server running"}

def run_server(port: int):
    uvicorn.run(app, host="0.0.0.0", port=port)
