import os
import psycopg

DATABASE_URL = os.getenv("DATABASE_URL")

def get_conn():
    return psycopg.connect(DATABASE_URL, autocommit=True, row_factory=psycopg.rows.dict_row)

def create_schema():
    with get_conn() as conn, conn.cursor() as cur:
            # Create the schema
            cur.execute("""
            -- tabell för rum
            CREATE TABLE IF NOT EXISTS hotel_rooms (
                id SERIAL PRIMARY KEY,
                room_number INT UNIQUE NOT NULL,
                type VARCHAR NOT NULL,
                price NUMERIC DEFAULT 0
            );

            -- Tabell för gäster
            CREATE TABLE IF NOT EXISTS hotel_guests (
                id SERIAL PRIMARY KEY,
                firstname VARCHAR NOT NULL,
                lastname VARCHAR NOT NULL,
                address VARCHAR
            );

            -- Tabell för bokningar
            CREATE TABLE IF NOT EXISTS hotel_bookings (
                id SERIAL PRIMARY KEY,
                guest_id INT REFERENCES hotel_guests(id) NOT NULL,
                room_id INT REFERENCES hotel_rooms(id) NOT NULL,
                datefrom DATE NOT NULL,
                dateto DATE NOT NULL,
                addinfo VARCHAR
            );

            -- Fyll på lite exempeldata om tom
            INSERT INTO hotel_rooms (room_number, type, price)
            VALUES (101, 'Double', 1200), (201, 'Single', 800)
            ON CONFLICT (room_number) DO NOTHING;
            
            INSERT INTO hotel_guests (firstname, lastname, address)
            SELECT 'Erik', 'Svensson', 'Gatan 1'
            WHERE NOT EXISTS (SELECT 1 FROM hotel_guests WHERE firstname = 'Erik');
        """)