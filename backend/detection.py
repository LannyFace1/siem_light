## import necessary libraries
from datetime import datetime, timedelta
import os
from db import get_all_events, insert_alert, alert_exists


ALERT_THRESHOLD = int(os.environ.get('FAILED_ATTEMPTS', 5))
TIME_WINDOW = int(os.environ.get('TIME_WINDOW', 300))

## Get events and group them by IP
def run_detection():
    events = get_all_events()
    ip_attempts = {}
    
    for event in events:
        timestamp_str, ip_address, username = event[1], event[2], event[3]
        timestamp = datetime.strptime(timestamp_str, '%b %d %H:%M:%S')
        
        if ip_address not in ip_attempts:
            ip_attempts[ip_address] = []
        ip_attempts[ip_address].append(timestamp)
    
    ## Check for failed attempts within the time window
    for ip, timestamps in ip_attempts.items():
        timestamps.sort()
        attempt_count = 0
        
        for i in range(len(timestamps)):
            while (timestamps[i] - timestamps[0]).total_seconds() > TIME_WINDOW:
                timestamps.pop(0)
            attempt_count = len(timestamps)
            
            if attempt_count >= ALERT_THRESHOLD and not alert_exists(ip):
                insert_alert(ip, attempt_count)
                break

