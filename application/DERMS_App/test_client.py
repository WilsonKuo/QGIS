#!/bin/python3.6
import os
import uvicorn
from fastapi import FastAPI

app = FastAPI()

# API Server settings
# PORT = os.environ.get("PORT")
# IP = os.environ.get("IP")

PORT = 8000
IP = "127.0.0.1"

@app.get("/")
async def root():
    return {"message": "Hello World"}

if __name__ == "__main__":
    # Local WSGI: Uvicorn
    ip = IP
    port = PORT
    uvicorn.run(
        "test_server:app",
        host=ip,
        port=port,
        workers=4,
        log_level="info",
        access_log=True,
        use_colors=True,
        reload=True,
    )