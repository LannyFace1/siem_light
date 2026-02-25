from datetime import datetime
import os
from db import get_all_events, upsert_alert

ALERT_THRESHOLD = int(os.environ.get('FAILED_ATTEMPTS', 5))
TIME_WINDOW = int(os.environ.get('TIME_WINDOW', 300))

SLOW_ATTACK_ATTEMPTS = int(os.environ.get('SLOW_ATTACK_ATTEMPTS', 20))
SLOW_ATTACK_WINDOW = int(os.environ.get('SLOW_ATTACK_WINDOW', 86400))

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

        # Regel 1 – Brute Force: X Versuche in Y Sekunden
        max_brute = 0
        for i in range(len(timestamps)):
            window = [t for t in timestamps if (timestamps[i] - t).total_seconds() <= TIME_WINDOW and t <= timestamps[i]]
            max_brute = max(max_brute, len(window))
        if max_brute >= ALERT_THRESHOLD:
            upsert_alert(ip, max_brute, 'BRUTE_FORCE')

        # Regel 2 – Slow Attack: X Versuche in 24 Stunden
        max_slow = 0
        for i in range(len(timestamps)):
            window = [t for t in timestamps if (timestamps[i] - t).total_seconds() <= SLOW_ATTACK_WINDOW and t <= timestamps[i]]
            max_slow = max(max_slow, len(window))
        if max_slow >= SLOW_ATTACK_ATTEMPTS:
            upsert_alert(ip, max_slow, 'SLOW_ATTACK')
