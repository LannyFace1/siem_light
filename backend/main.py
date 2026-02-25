## import necessary libraries
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import os
from db import init_db, get_all_events, get_all_alerts, insert_event
from detection import run_detection
from parser import get_failed_attempts

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'fallback_key')
CORS(app)

@app.route('/')
def dashboard():
    return send_from_directory('/app/frontend', 'index.html')

## app status
@app.route('/status')
def index():
    return jsonify({"status": "SIEM-Light running"})

## scan the log file for failed login attempts and save them to the database
@app.route('/scan')
def scan():
    events = get_failed_attempts()
    for e in events:
        insert_event(e['timestamp'], e['ip_address'], e['username'])
    return jsonify({"status": "scan complete", "events_found": len(events)})

## get all alerts
@app.route('/alerts')
def alerts():
    results = [{"id": a[0], "ip_address": a[1], "attempt_count": a[2], "created_at": a[3]} for a in get_all_alerts()]
    return jsonify({"alerts": results})

## get all logs
@app.route('/logs')
def logs():
    run_detection()
    events = get_all_events()
    result = [{"id": e[0], "timestamp": e[1], "ip_address": e[2], "username": e[3]} for e in events]
    return jsonify({"logs": result})

## start the app
if __name__ == "__main__":
    init_db()
    app.run(debug=False, host='0.0.0.0', port=5000)




