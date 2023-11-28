# central_server.py
from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

peers = {}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    unique_id = str(uuid.uuid4())
    peer_name = f'Peer-{unique_id[:8]}'
    peers[request.sid] = {'id': unique_id, 'name': peer_name}
    emit('update_peers', peers, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    if request.sid in peers:
        del peers[request.sid]
    emit('update_peers', peers, broadcast=True)

if __name__ == '__main__':
    socketio.run(app, debug=True)
