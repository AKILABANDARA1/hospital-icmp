from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from ping3 import ping
import socket
import os

app = FastAPI()
templates = Jinja2Templates(directory="templates")

TARGET_IP = os.getenv("TARGET_IP", "20.109.32.217")
TARGET_PORT = int(os.getenv("TARGET_PORT", "80"))
TIMEOUT = 5

def is_host_up_icmp(ip):
    try:
        result = ping(ip, timeout=TIMEOUT)
        return result is not None
    except Exception:
        return None

def is_host_up_tcp(ip, port, timeout=TIMEOUT):
    try:
        with socket.create_connection((ip, port), timeout=timeout):
            return True
    except:
        return False

@app.get("/")
def web_status(request: Request):
    up = is_host_up_icmp(TARGET_IP)
    if up is None:
        up = is_host_up_tcp(TARGET_IP, TARGET_PORT)
    return templates.TemplateResponse("status.html", {
        "request": request,
        "status_class": "up" if up else "down",
        "status_text": "UP" if up else "DOWN",
        "ip": TARGET_IP,
        "port": TARGET_PORT
    })

@app.get("/probe")
def probe():
    icmp_up = is_host_up_icmp(TARGET_IP)
    if icmp_up is None:
        tcp_up = is_host_up_tcp(TARGET_IP, TARGET_PORT)
        return {
            "target": TARGET_IP,
            "method": "tcp",
            "port": TARGET_PORT,
            "status": "UP" if tcp_up else "DOWN"
        }
    return {
        "target": TARGET_IP,
        "method": "icmp",
        "status": "UP" if icmp_up else "DOWN"
    }
