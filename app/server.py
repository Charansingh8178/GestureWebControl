# server.py

import threading
from app.fastApii import start as start_fastapi

def start_server():
    t = threading.Thread(target=start_fastapi, daemon=True)
    t.start()
    print("Server thread started.")
