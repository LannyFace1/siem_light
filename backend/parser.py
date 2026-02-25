## import Regex for log parsing and Flask for web app
import re
import os

## Data path for the log file
LOG_FILE_PATH = os.environ.get('CONTAINER_LOG_PATH', 'backend/test.log')
## read log file line by line and return a list of log entries
def read_log_file():
    with open(LOG_FILE_PATH, 'r') as file:
        log_entries = file.readlines()
    return log_entries

## examine log entries for failed login attempts and return timestamps and ip addresses per Regex
def extract_failed_attempts(log_entries):
    failed_logins = []
    for entry in log_entries:
        if 'Failed' in entry:
            timestamp = datetime.strptime(timestamp_str, '%Y-%m-%dT%H:%M:%S')
            ip_address = re.search(r'from (\d+\.\d+\.\d+\.\d+)', entry)
            username = re.search(r'for (\w+)', entry)
            if timestamp and ip_address and username:
                failed_logins.append({'timestamp': timestamp.group(1), 'ip_address': ip_address.group(1), 'username': username.group(1)})
    return failed_logins

## return everything as list from Dicts 
def get_failed_attempts():
    log_entries = read_log_file()
    failed_attempts = extract_failed_attempts(log_entries)
    return failed_attempts



