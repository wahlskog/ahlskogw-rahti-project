from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

rooms_db = [
    {"key": 1001, "name": "Room 1", "available": True},
    {"key": 1002, "name": "Room 2", "available": False},
    {"key": 1003, "name": "Room 3", "available": True}
]

@app.get("/rooms")
def get_rooms():
    return rooms_db

@app.get("/")
def read_root():
    return { "msg": "Hello local docker"}

@app.get("/api/ip")
def ip(request: Request):
    return { "ip": request.client.host}


@app.get("/ip", response_class=HTMLResponse)
def ip(request: Request):
    return f"<h1>Din ip är {request.client.host}</h1>"

@app.get("/hello")
def hello():
    return { "msg": "Hello William"}