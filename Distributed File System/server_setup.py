#ser_setup.py
import socket
import threading
import os
import json
import hashlib
from ml_pre import MaliciousActivityPredictor
import logging
import io
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad,pad
from fcntl import flock, LOCK_SH, LOCK_EX

secret_key = b'16ByteSecretKey!'
model_path = 'model.pkl' 
detect = MaliciousActivityPredictor(model_path)

BASE_DIR = os.path.join(os.getcwd(),"File_Sys")
RECYCLE_BIN_DIR = os.path.join(BASE_DIR, "RecycleBin")

if not os.path.exists(BASE_DIR):
    os.makedirs(BASE_DIR)

file_permissions = {
    
    BASE_DIR: {
        "admin": ["read", "write", "create"],
        "peer1": ["read", "write", "create"],
        "peer2": ["read", "write", "create"],
        # Other users and their permissions
    },

    RECYCLE_BIN_DIR: {
        "admin": ["restore"],
        "peer1": ["restore"],
        "peer2": ["restore"],
    }
}

# User management
users = {
    "admin": {"password": hashlib.sha256("admin123".encode()).hexdigest(), "permissions": ["all"]},
    "peer1": {"password": hashlib.sha256("peer123".encode()).hexdigest(), "permissions": []},
    "peer2": {"password": hashlib.sha256("peer123".encode()).hexdigest(), "permissions": []}

}

current_directories = {username: BASE_DIR for username in users}


# Configure logging
class StringHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.log_stream = io.StringIO()

    def emit(self, record):
        # Write the log message to a StringIO object
        self.log_stream.write(self.format(record) + '\n')

    def get_log(self):
        # Retrieve the entire log content
        return self.log_stream.getvalue()

# Create a logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Set up formatter
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

# Create a file handler and set level to info
file_handler = logging.FileHandler('file_system.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

# Create a console handler and set level to info
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(formatter)

# Create a custom string handler
string_handler = StringHandler()
string_handler.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)
logger.addHandler(string_handler)





def log_malicious_activity(activity):
    """
    Logs the malicious activity to a file.

    Parameters:
    activity (str): The log data that was detected as malicious.
    """
    with open('malicious.log', 'a') as log_file:
        log_file.write(activity + '\n')

def m_detect(data):
    """
    Detects malicious activity in the provided log data.

    Parameters:
    data (str): The log data to be analyzed.
    """
    if detect.predict_malicious_activity(data):
        log_malicious_activity(data)
        print('Malicious')




def change_directory(username, new_directory):
    global current_directories

    if new_directory == "..":
        # Go up one directory, but not above BASE_DIR
        current_directories[username] = os.path.dirname(current_directories[username]) \
            if os.path.dirname(current_directories[username]) != "" else BASE_DIR
    else:
        # Change to a specified subdirectory within the current directory
        potential_new_directory = os.path.join(current_directories[username], new_directory)
        if os.path.exists(potential_new_directory) and os.path.isdir(potential_new_directory):
            current_directories[username] = potential_new_directory
        else:
            raise FileNotFoundError(f"Directory '{new_directory}' not found.")


def has_permission(username, file_path, operation):
    if username == "admin":
        return True  # Admin has all permissions

    full_path = os.path.join(current_directories[username], file_path)  # Full path for the file

    # Check permissions for the specific file
    if full_path in file_permissions and username in file_permissions[full_path]:
        return operation in file_permissions[full_path][username]

    # If specific file permissions not set, check the directory permissions
    directory = os.path.dirname(full_path)
    if directory in file_permissions and username in file_permissions[directory]:
        return operation in file_permissions[directory][username]
    return False

def set_file_permissions(client_socket, username, file_path, permissions):
    response = ""
    permissions = permissions+f',{username}:read+write+delete+restore'
    try:
        full_path = os.path.join(current_directories[username], file_path)  # Ensure the full path is used

        if full_path not in file_permissions:
            file_permissions[full_path] = {}

        for user_perm in permissions.split(','):
            user, perm = user_perm.split(':')
            file_permissions[full_path][user] = perm.split('+')

        response = f"Permissions set successfully.{file_permissions}"
        
    except Exception as e:
        response = f"Error setting permissions: {str(e)}"
    client_socket.sendall(encrypt_message(response))


def add_user(username, password, permissions):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    users[username] = {"password": hashed_password, "permissions": permissions}

def remove_user(username):
    if username in users:
        del users[username]

def validate_user(username, password):
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return username in users and users[username]["password"] == hashed_password

# File operations with version control
def list_files_and_dirs(username):
    items = os.listdir(current_directories[username])
    return "\n".join(items)

def create_directory(username, dirname):
    dir_path = os.path.join(current_directories[username], dirname)
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    else:
        raise FileExistsError(f"Directory '{dirname}' already exists.")

def create_file(username, filename, content=""):
    file_path = os.path.join(current_directories[username], filename)
    with open(file_path, 'w') as file:
        file.write(content + '\n')

def delete_file(username, filename):
    file_path = os.path.join(current_directories[username], filename)
    if not os.path.exists(RECYCLE_BIN_DIR):
        os.makedirs(RECYCLE_BIN_DIR)

    if os.path.exists(file_path):
        # Move the file to the recycle bin instead of deleting
        os.rename(file_path, os.path.join(RECYCLE_BIN_DIR, filename))
    else:
        raise FileNotFoundError(f"File '{filename}' not found.")
    
def restore_file(username, filename):
    file_path_in_bin = os.path.join(RECYCLE_BIN_DIR, filename)
    if os.path.exists(file_path_in_bin):
        # Move the file back to its original directory
        original_path = os.path.join(current_directories[username], filename)
        os.rename(file_path_in_bin, original_path)
    else:
        raise FileNotFoundError(f"File '{filename}' not found in recycle bin.")

def read_file(client_socket, username, filename):
    file_path = os.path.join(current_directories[username], filename)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File '{filename}' not found.")

    with open(file_path, 'r') as file:
        fd = file.fileno()
        flock(fd, LOCK_SH)
        content = file.read()
        client_socket.sendall(encrypt_message(content))

def write_file(username, filename, choice, content):
    file_path = os.path.join(current_directories[username], filename)
    with open(file_path, 'w' if choice == 'w' else 'a') as file:
        fd = file.fileno()
        flock(fd, LOCK_EX)
        file.write(content + '\n')

def encrypt_message(message):
    cipher = AES.new(secret_key, AES.MODE_ECB)
    padded_message = pad(message.encode(), AES.block_size)
    encrypted_message = cipher.encrypt(padded_message)
    return encrypted_message

def decrypt_message(encrypted_message):
    cipher = AES.new(secret_key, AES.MODE_ECB)
    decrypted_message = unpad(cipher.decrypt(encrypted_message), AES.block_size)
    return decrypted_message.decode()

# Server function to handle client requests
def client_handler(client_socket):
    global users, current_directories
    current_user = None
    failed_login_attempts = 0  # Track failed login attempts

    while True:
        encrypted_data = client_socket.recv(1024)
        data = decrypt_message(encrypted_data)
        if not data:
            break
        
        info_log = f"Received command from {client_socket.getpeername()}: {data}"
        logging.info(info_log)
        captured_log = string_handler.get_log()
        m_detect(captured_log)
        

        command = data.split()
        response = ""

        # Process commands
        try:
            if command[0] == "login":
                username, password = command[1], command[2]
                if validate_user(username, password):
                    current_user = username
                    failed_login_attempts = 0  # Reset on successful login
                    response = "Login successful."
                    info_log = f"Login successful for user {username}"
                    logging.info(info_log)
                    captured_log = string_handler.get_log()
                    m_detect(captured_log)
                else:
                    failed_login_attempts += 1
                    response = "Invalid username or password."
                    info_log = f"Failed login attempt for user {username}"
                    logging.warning(info_log)
                    captured_log = string_handler.get_log()
                    m_detect(captured_log)
                    if failed_login_attempts > 3:  # Example threshold for failed attempts
                        info_log = f"Multiple failed login attempts from {client_socket.getpeername()}"
                        logging.warning(info_log)
                        captured_log = string_handler.get_log()
                        m_detect(captured_log)

            elif current_user:
                if command[0] == "list":
                    response = list_files_and_dirs(current_user)
                    info_log = f"List directory command executed by {current_user}"
                    logging.info(info_log)
                    captured_log = string_handler.get_log()
                    m_detect(captured_log)

                elif command[0] == "mkdir" and has_permission(current_user, command[1], "create"):
                    try:
                        create_directory(current_user, command[1])
                        response = f"Directory '{command[1]}' created."
                        info_log = f"Directory created: {command[1]} by {current_user}"
                        logging.info(info_log)
                        captured_log = string_handler.get_log()
                        m_detect(captured_log)
                    except Exception as e:
                        response = str(e)
                        info_log = f"Error creating directory: {command[1]} by {current_user}, Error: {e}"
                        logging.error(info_log)
                        captured_log = string_handler.get_log()
                        m_detect(captured_log)

                elif command[0] == "create" and has_permission(current_user, command[1], "create"):
                    filename = command[1]
                    content = " ".join(command[2:])
                    create_file(current_user, filename, content)
                    response = f"File '{filename}' created."
                    info_log = f"File created: {filename} by {current_user}"
                    logging.info(info_log)
                    captured_log = string_handler.get_log()
                    m_detect(captured_log)

                elif command[0] == "delete" and has_permission(current_user, command[1], "delete"):
                    delete_file(current_user, command[1])
                    response = f"File '{command[1]}' deleted."
                    info_log = f"File deleted: {command[1]} by {current_user}"
                    logging.info(info_log)
                    captured_log = string_handler.get_log()
                    m_detect(captured_log)

                elif command[0] == "restore" and has_permission(current_user, command[1], "restore"):
                    restore_file(current_user, command[1])
                    response = f"File '{command[1]}' restored."
                    info_log = f"File restored: {command[1]} by {current_user}"
                    logging.info(info_log)
                    captured_log = string_handler.get_log()
                    m_detect(captured_log)

                elif command[0] == "read" and has_permission(current_user, command[1], "read"):
                    read_file(client_socket, current_user, command[1])
                    info_log = f"File read: {command[1]} by {current_user}"
                    logging.info(info_log)
                    captured_log = string_handler.get_log()
                    m_detect(captured_log)

                elif command[0] == "write" and has_permission(current_user, command[1], "write"):
                    write_file(current_user, command[1], command[2], " ".join(command[3:]))
                    response = f"Written to '{command[1]}'."
                    info_log = f"File written to: {command[1]} by {current_user}"
                    logging.info(info_log)
                    captured_log = string_handler.get_log()
                    m_detect(captured_log)

                elif command[0] == "setperm" and has_permission(current_user, command[1], "create"):
                    file_path = command[1]
                    permissions = " ".join(command[2:])
                    set_file_permissions(client_socket, current_user, file_path, permissions)
                    info_log =f"Permissions set for {file_path} by {current_user}"
                    logging.info(info_log)
                    captured_log = string_handler.get_log()
                    m_detect(captured_log)

                elif command[0] == "cd" and has_permission(current_user, command[1], "create"):
                    try:
                        change_directory(current_user, command[1])
                        response = f"Now in directory: {current_directories[current_user]}"
                        info_log = f"Changed directory to: {current_directories[current_user]} by {current_user}"
                        logging.info(info_log)
                        captured_log = string_handler.get_log()
                        m_detect(captured_log)

                    except Exception as e:
                        response = str(e)
                        info_log = f"Error changing directory: {command[1]} by {current_user}, Error: {e}"
                        logging.error(info_log)
                        captured_log = string_handler.get_log()
                        m_detect(captured_log)

                else:
                    response = "Permission denied or invalid command."
                    info_log = f"Permission denied or invalid command for {current_user}: {data}"
                    logging.warning(info_log)
                    captured_log = string_handler.get_log()
                    m_detect(captured_log)

            else:
                response = "Please login first."
                info_log = f"Command attempted without login: {data}"
                logging.warning(info_log)
                captured_log = string_handler.get_log()
                m_detect(captured_log)


        except Exception as e:
            response = f"Error: {str(e)}"
            info_log = f"Unexpected error for {current_user}: {e}"
            logging.error(f"Unexpected error for {current_user}: {e}")
            captured_log = string_handler.get_log()
            m_detect(captured_log)
        client_socket.send(encrypt_message(response))

    client_socket.close()

# Server main function
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(('localhost', 12345))
    server_socket.listen(5)
    print("Server started. Listening for connections...")
    info_log = f"Server started. Listening for connections at {server_socket}"
    logging.info(info_log)
    captured_log = string_handler.get_log()
    m_detect(captured_log)

    while True:
        client_sock, addr = server_socket.accept()
        print(f"Connection from {addr} has been established.")
        info_log = f"Connection from {client_sock}, {addr} has been established."
        logging.info(f"Connection from {client_sock}, {addr} has been established.")
        client_thread = threading.Thread(target=client_handler, args=(client_sock,))
        client_thread.start()

if __name__ == "__main__":
    start_server()
