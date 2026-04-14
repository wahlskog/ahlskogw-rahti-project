from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from app.db import get_conn, create_schema
from pydantic import BaseModel # <--- LÄGG TILL
from datetime import date       # <--- LÄGG TILL

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Definiera datamodellen här
class Booking(BaseModel):
    guest_id: int
    room_id: int
    datefrom: date
    dateto: date
    addinfo: str = None

create_schema()

@app.get("/")
def read_root():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT 'databasen funkar!' AS msg, version() as version")
        db_status = cur.fetchone()
    return {"msg": "Välkommen till hotellets booking API", "db": db_status}

@app.get("/rooms")
def get_rooms():
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("SELECT id, room_number, type, price FROM hotel_rooms")
        rooms = cur.fetchall()
    return rooms

@app.post("/bookings")
def create_booking(booking: Booking):
    with get_conn() as conn, conn.cursor() as cur:
        cur.execute("""
            INSERT INTO hotel_bookings (guest_id, room_id, datefrom, dateto, addinfo)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING id
        """, (booking.guest_id, booking.room_id, booking.datefrom, booking.dateto, booking.addinfo))
        new_id = cur.fetchone()["id"]
    return {"msg": "Bokning lyckades!", "booking_id": new_id}