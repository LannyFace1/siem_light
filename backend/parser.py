import re
import os

LOG_FILE_PATH = os.environ.get('CONTAINER_LOG_PATH', 'backend/test.log')

def read_log_file():
    with open(LOG_FILE_PATH, 'r') as file:
        log_entries = file.readlines()
    return log_entries

def extract_failed_attempts(log_entries):
    failed_logins = []
    for entry in log_entries:
        if 'Failed password' in entry:
            timestamp = re.search(r'(\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2})', entry)
            ip_address = re.search(r'from (\d+\.\d+\.\d+\.\d+)', entry)
            username = re.search(r'for (\w+)', entry)
            if timestamp and ip_address and username:
                failed_logins.append({
                    'timestamp': timestamp.group(1),
                    'ip_address': ip_address.group(1),
                    'username': username.group(1)
                })
    return failed_logins

def get_failed_attempts():
    log_entries = read_log_file()
    return extract_failed_attempts(log_entries)
