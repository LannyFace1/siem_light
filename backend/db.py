## importing necessary libraries
import sqlite3
from datetime import datetime
import os

DB_PATH = os.environ.get('DB_PATH', 'backend/siem.db')

## table events of each parsed log entry and Table alerts – triggered alarms
def init_db():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                ip_address TEXT,
                username TEXT
            )
        ''')
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ip_address TEXT,
                attempt_count INTEGER,
                created_at TEXT
            )
        ''')
        conn.commit()

## save events to the database
def insert_event(timestamp, ip_address, username):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO events (timestamp, ip_address, username)
            VALUES (?, ?, ?)
        ''', (timestamp, ip_address, username))
        conn.commit()

##  View all events
def get_all_events():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM events')
        return cursor.fetchall()
    
## Save alerts to the database
def insert_alert(ip_address, attempt_count):
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO alerts (ip_address, attempt_count, created_at)
            VALUES (?, ?, ?)
        ''', (ip_address, attempt_count, created_at))
        conn.commit()

## View all alerts
def get_all_alerts():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM alerts')
        return cursor.fetchall()

## Checks whether an alert already exists for an IP address.
def event_exists(timestamp, ip_address):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM events WHERE timestamp = ? AND ip_address = ?', (timestamp, ip_address))
        return cursor.fetchone() is not None
