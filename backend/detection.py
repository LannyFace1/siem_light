from datetime import datetime
import os
from db import get_all_events, upsert_alert

ALERT_THRESHOLD = int(os.environ.get('FAILED_ATTEMPTS', 5))
TIME_WINDOW = int(os.environ.get('TIME_WINDOW', 300))

def run_detection():
    events = get_all_events()
    ip_attempts = {}

    for event in events:
        timestamp_str, ip_address = event[1], event[2]
        try:
            timestamp = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S')
        except ValueError:
            continue
        if ip_address not in ip_attempts:
            ip_attempts[ip_address] = []
        ip_attempts[ip_address].append(timestamp)

    for ip, timestamps in ip_attempts.items():
        timestamps.sort()
        max_window = 0
        for i in range(len(timestamps)):
            window = [t for t in timestamps if (timestamps[i] - t).total_seconds() <= TIME_WINDOW and t <= timestamps[i]]
            max_window = max(max_window, len(window))
        if max_window >= ALERT_THRESHOLD:
            upsert_alert(ip, max_window)
