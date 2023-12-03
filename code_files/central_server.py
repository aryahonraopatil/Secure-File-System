from PyQt5.QtWidgets import QApplication, QMainWindow, QTextEdit, QVBoxLayout, QWidget, QPushButton
from PyQt5.QtCore import QThread, pyqtSignal
import socket
import threading
import json
import sys

class CentralServer:
    def __init__(self, host="localhost", port=12345):
        self.active_peers = {}
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.bind((host, port))
        self.server_socket.listen(5)

    def handle_peer(self, client_socket, address, log_callback):
        buffer = ""
        while True:
            try:
                data = client_socket.recv(1024).decode()
                if not data:
                    break

                buffer += data
                while "\n" in buffer:
                    message, buffer = buffer.split("\n", 1)
                    data = json.loads(message)

                    if data["type"] == "register":
                        self.active_peers[str(address)] = data["peer_info"]
                        log_callback.emit(f"Peer registered: {data['peer_info']}")
                    elif data["type"] == "request_list":
                        response_data = {str(key): value for key, value in self.active_peers.items()}
                        response = json.dumps(response_data) + "\n"
                        client_socket.send(response.encode())

            except Exception as e:
                log_callback.emit(f"Error with peer {address}: {e}")
                break

        self.active_peers.pop(str(address), None)
        log_callback.emit(f"Peer is still connected: {address}")
        client_socket.close()

    def run(self, log_callback):
        while True:
            client_socket, address = self.server_socket.accept()
            threading.Thread(target=self.handle_peer, args=(client_socket, address, log_callback)).start()
            
class ServerThread(QThread):
    log_signal = pyqtSignal(str)

    def __init__(self, server):
        QThread.__init__(self)
        self.server = server

    def run(self):
        self.server.run(self.log_signal)
        
class CentralServerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.server = CentralServer()
        self.server_thread = ServerThread(self.server)
        self.server_thread.log_signal.connect(self.log_message)
        self.server_thread.start()
        
def initUI(self):
        self.setWindowTitle("Central Server")
        self.setGeometry(100, 100, 600, 400)

        layout = QVBoxLayout()
        
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        layout.addWidget(self.log_area)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)
        
        def log_message(self, message):
            self.log_area.append(message)
