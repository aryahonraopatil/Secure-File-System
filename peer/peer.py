# peer.py
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import socket

app = Flask(__name__)
app.config['SECRET_KEY'] = 'peer_secret'
socketio = SocketIO(app)

def find_free_port():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(('', 0))
        return s.getsockname()[1]

@app.route('/')
def index():
    return render_template('peer.html')

if __name__ == '__main__':
    port = find_free_port()
    print(f'Starting peer on port {port}')
    socketio.run(app, host='0.0.0.0', port=port, debug=True)
