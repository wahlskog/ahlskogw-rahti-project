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

# tillfällig databas med rum
temp_rooms = [
    {"room_number": 101, "room_type": "Double room", "price": 100},
    {"room_number": 201, "room_type": "Single room", "price": 80},
    {"room_number": 301, "room_type": "Suite", "price": 250}
]


@app.get("/")
def read_root():
    return { "msg": "Välkommen till hotellets booking API"}

@app.get("/rooms")
def rooms():
    return temp_rooms

@app.post("/bookings")
def create_booking():
    # Skapa bokningen i databasen, INSERT INTO bookings ...
    return {"msg": "Bokningen har skapats"}
