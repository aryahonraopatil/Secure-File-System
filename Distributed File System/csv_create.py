import csv
import re

def parse_log_line(line):
    pattern = r'(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}),\d{3} - (\w+) - (.+)'
    match = re.match(pattern, line)
    
    if match:
        timestamp, log_level, message = match.groups()
        return timestamp, log_level, message
    return None

def extract_features(timestamp, log_level, message):
    source_ip = '127.0.0.1'  # Default IP
    username = 'unknown'     # Default username
    action_type = 'other'    # Default action
    status = 'failed' if log_level == 'ERROR' or 'Failed' in message else 'success'
    target = 'NA'            # Default target
    malicious = '1' if log_level == 'ERROR' or 'Failed' in message else '0'

    # Extracting IP Address
    ip_match = re.search(r"raddr=\('([\d\.]+)',", message)
    if not ip_match:
        ip_match = re.search(r"from \('([\d\.]+)',", message)
    if ip_match:
        source_ip = ip_match.group(1)

    # Extracting Username
    user_match = re.search(r"user (\w+)", message)
    if not user_match:
        user_match = re.search(r"for user (\w+)", message)
    if user_match:
        username = user_match.group(1)

    # Extracting Action Type
    action_match = re.search(r": (\w+)", message)
    if action_match:
        action_type = action_match.group(1)

    # Extracting Target if available
    target_match = re.search(r"on (\w+\.txt)", message)
    if target_match:
        target = target_match.group(1)

    return [timestamp, log_level, source_ip, username, action_type, status, target, malicious]

# Read the log file and write to CSV
with open('file_system.log', 'r') as log_file, open('file_system_data.csv', 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Timestamp', 'Log Level', 'Source IP', 'Username', 'Action Type', 'Status', 'Target', 'Malicious'])

    for line in log_file:
        parsed_line = parse_log_line(line.strip())
        if parsed_line:
            timestamp, log_level, message = parsed_line
            features = extract_features(timestamp, log_level, message)
            csv_writer.writerow(features)
