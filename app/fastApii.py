
import uvicorn
import threading
import nest_asyncio
from fastapi import FastAPI, WebSocket, Form
from fastapi.responses import HTMLResponse
import requests
from app.config import HTML_URL
nest_asyncio.apply()

app = FastAPI()
connected_clients = set()

@app.get("/")
async def get():
    with open(HTML_URL) as f:
        html = f.read()
    return HTMLResponse(html)


@app.websocket("/ws")

async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    connected_clients.add(websocket)
    print("[Client connected. Total:", len(connected_clients))

    try:
        while True:
            await websocket.receive_text() 
    except:
        pass
    finally:
        connected_clients.remove(websocket)
        print("Client disconnected")

async def broadcast(msg: str):
    
    for ws in list(connected_clients):
        try:
            await ws.send_text(msg)
        except:
            connected_clients.remove(ws)

from fastapi import Form
@app.post("/broadcast")

async def broadcast_route(msg: str = Form(...)):
    await broadcast(msg)
    return {"status": "OK", "sent": msg}

def start():
    print("Starting FastAPI at http://localhost:8000")
    uvicorn.run(app, host="0.0.0.0", port=8000)


# def start_server():
#     t = threading.Thread(target=start_fastapi, daemon=True)
#     t.start()
#     print("Server thread started.")