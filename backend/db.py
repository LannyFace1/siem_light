import sqlite3
from datetime import datetime
import os

DB_PATH = os.environ.get('DB_PATH', 'backend/siem.db')

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
                alert_type TEXT,
                created_at TEXT
            )
        ''')
        conn.commit()

def insert_event(timestamp, ip_address, username):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO events (timestamp, ip_address, username)
            VALUES (?, ?, ?)
        ''', (timestamp, ip_address, username))
        conn.commit()

def get_all_events():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM events')
        return cursor.fetchall()

def upsert_alert(ip_address, attempt_count, alert_type):
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM alerts WHERE ip_address = ? AND alert_type = ?', (ip_address, alert_type))
        existing = cursor.fetchone()
        if existing:
            cursor.execute('''
                UPDATE alerts SET attempt_count = ?, created_at = ?
                WHERE ip_address = ? AND alert_type = ?
            ''', (attempt_count, created_at, ip_address, alert_type))
        else:
            cursor.execute('''
                INSERT INTO alerts (ip_address, attempt_count, alert_type, created_at)
                VALUES (?, ?, ?, ?)
            ''', (ip_address, attempt_count, alert_type, created_at))
        conn.commit()

def get_all_alerts():
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM alerts ORDER BY created_at DESC')
        return cursor.fetchall()

def event_exists(timestamp, ip_address):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT id FROM events WHERE timestamp = ? AND ip_address = ?', (timestamp, ip_address))
        return cursor.fetchone() is not None
