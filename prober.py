from fastapi import FastAPI
import socket

app = FastAPI()

TARGET_IP = "20.109.32.217"
TARGET_PORT = 80
TIMEOUT = 5

def is_host_up(ip, port, timeout=5):
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return True
    except:
        return False

@app.get("/")
def health_check():
    return {"status": "ok"}

@app.get("/probe")
def probe():
    is_up = is_host_up(TARGET_IP, TARGET_PORT, TIMEOUT)
    return {
        "target": TARGET_IP,
        "port": TARGET_PORT,
        "status": "UP" if is_up else "DOWN"
    }
