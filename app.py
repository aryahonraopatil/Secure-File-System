from flask import Flask, render_template
from flask_socketio import SocketIO
import subprocess

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
socketio = SocketIO(app)

server_process = None
client_process = None

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/start_server')
def start_server():
    global server_process
    if server_process is None or server_process.poll() is not None:
        server_process = subprocess.Popen(['python', 'server.py'])
    return '', 204

@app.route('/start_client')
def start_client():
    global client_process
    if client_process is None or client_process.poll() is not None:
        client_process = subprocess.Popen(['python', 'client.py'])
    return '', 204

@app.route('/server_started')
def server_started():
    return "Server started successfully. [Add more content or redirect as needed]"

@app.route('/client_started')
def client_started():
    return "Client started successfully. [Add more content or redirect as needed]"


if __name__ == '__main__':
    socketio.run(app, debug=True)
