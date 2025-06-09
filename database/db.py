# database/db.py

import sqlite3
from tkinter import messagebox

DB_NAME = "project_data.db"

def get_connection():
    return sqlite3.connect(DB_NAME)

def init_db():
    conn = get_connection()
    cursor = conn.cursor()

    # Create table for storing PDF content
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS pdf_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            content TEXT
        )
    ''')

    # Create table for storing flight data
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS flights (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            serial_no TEXT,
            flight_name TEXT,
            destination TEXT,
            iata TEXT
        )
    ''')

    conn.commit()
    conn.close()

def insert_pdf_data(filename, content):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO pdf_data (filename, content) VALUES (?, ?)", (filename, content))
        conn.commit()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Failed to insert PDF data: {str(e)}")
    finally:
        conn.close()

def insert_flight(serial_no, flight_name, destination, iata):
    if flight_exists(serial_no, flight_name, destination, iata):
        messagebox.showerror("Duplicate Entry", "This flight already exists in the database.")
        return

    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO flights (serial_no, flight_name, destination, iata) VALUES (?, ?, ?, ?)",
            (serial_no, flight_name, destination, iata)
        )
        conn.commit()
    except sqlite3.Error as e:
        messagebox.showerror("Database Error", f"Failed to insert flight: {str(e)}")
    finally:
        conn.close()

def flight_exists(serial_no, flight_name, destination, iata):
    """
    Checks if any of the given values already exist in the flights table.
    Returns True if at least one match is found.
    """
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM flights
        WHERE serial_no = ? OR flight_name = ? OR destination = ? OR iata = ?
    ''', (serial_no, flight_name, destination, iata))
    exists = cursor.fetchone() is not None
    conn.close()
    return exists

def get_all_flights():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT serial_no, flight_name, destination, iata FROM flights")
    rows = cursor.fetchall()
    conn.close()
    return rows

def update_flight(old_values, new_values):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        UPDATE flights
        SET serial_no = ?, flight_name = ?, destination = ?, iata = ?
        WHERE serial_no = ? AND flight_name = ? AND destination = ? AND iata = ?
    ''', (*new_values, *old_values))
    conn.commit()
    conn.close()

def delete_flight(serial_no, flight_name, destination, iata):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        DELETE FROM flights
        WHERE serial_no = ? AND flight_name = ? AND destination = ? AND iata = ?
    ''', (serial_no, flight_name, destination, iata))
    conn.commit()
    conn.close()
