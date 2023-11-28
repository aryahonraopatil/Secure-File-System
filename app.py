from flask import Flask, render_template, request, send_from_directory
from flask_socketio import SocketIO

import os
import subprocess
import multiprocessing

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a secret key
socketio = SocketIO(app)

# Define the upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Define the server host and port
SERVER_HOST = '127.0.0.1'
SERVER_PORT = 12345

# Store server and client process objects and status flags
server_process = None
client_process = None
server_running = False
client_running = False

# Store communication messages
communication_messages = []

def start_server():
    global server_process, server_running
    try:
        server_process = subprocess.Popen(['python', 'server.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                          stdin=subprocess.PIPE, text=True, bufsize=1, universal_newlines=True)
        server_running = True
        while server_running:
            line = server_process.stdout.readline()
            if line:
                communication_messages.append(f'Server: {line.strip()}')
            else:
                server_running = False
        server_process.communicate()
    except Exception as e:
        print(f"Error: {str(e)}")

def start_client():
    global client_process, client_running
    try:
        client_process = subprocess.Popen(['python', 'client.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                          stdin=subprocess.PIPE, text=True, bufsize=1, universal_newlines=True)
        client_running = True
        while client_running:
            line = client_process.stdout.readline()
            if line:
                communication_messages.append(f'Client: {line.strip()}')
            else:
                client_running = False
        client_process.communicate()
    except Exception as e:
        print(f"Error: {str(e)}")

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the 'file' input field is empty
        if 'file' not in request.files:
            return 'No file part'

        file = request.files['file']

        # Check if the user submitted a file without a filename
        if file.filename == '':
            return 'No selected file'

        # Save the uploaded file to the UPLOAD_FOLDER
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

        return 'File uploaded successfully'

    return render_template('upload.html')

@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

    if os.path.isfile(file_path):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)
    else:
        return 'File not found'

@socketio.on('connect')
def handle_connect():
    emit_communication_messages()

def emit_communication_messages():
    for message in communication_messages:
        socketio.emit('communication_message', message)

@app.route('/start_server')
def start_server_route():
    global server_process, server_running, communication_messages
    if not server_running:
        # Start the server process if it's not already running
        server_process = multiprocessing.Process(target=start_server)
        server_process.start()
        communication_messages = []
        return "Server is starting..."
    else:
        return "Server is already running"

@app.route('/start_client')
def start_client_route():
    global client_process, client_running, communication_messages
    if not client_running:
        # Start the client process if it's not already running
        client_process = multiprocessing.Process(target=start_client)
        client_process.start()
        communication_messages = []
        return "Client is starting..."
    else:
        return "Client is already running"

if __name__ == '__main__':
    # Create the 'uploads' directory if it doesn't exist
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    socketio.run(app, debug=True)
