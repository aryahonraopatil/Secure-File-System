from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QListWidget, QFileDialog, QMessageBox, QLineEdit, QTextEdit
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread
import sys, time
import threading
from peer import Peer

import faulthandler

faulthandler.enable()

class PeerThread(QThread):
    update_peers_signal = pyqtSignal(dict)

    def __init__(self, peer, refresh_interval=10):
        super().__init__()
        self.peer = peer
        self.refresh_interval = refresh_interval  # Time in seconds between each refresh

    def run(self):
        while True:
            self.peer.fetch_active_peers()
            self.update_peers_signal.emit(self.peer.active_peers)
            time.sleep(self.refresh_interval)  # Pause the thread


class PeerGUI(QMainWindow):
    file_transfer_request_signal = pyqtSignal(str, int, object)
    message_received_signal = pyqtSignal(str)

    def __init__(self, peer):
        super().__init__()
        self.peer = peer
        self.setWindowTitle(peer.name)
        self.initUI()

        self.peer.set_message_received_callback(self.on_message_received)
        self.message_received_signal.connect(self.display_message)
        self.file_transfer_request_signal.connect(self.handle_file_transfer_request_gui)
        self.peer.set_file_transfer_request_callback(lambda f, s, c: self.file_transfer_request_signal.emit(f, s, c))


        self.peer_thread = PeerThread(self.peer)
        self.peer_thread.update_peers_signal.connect(self.update_peers_list)
        self.peer_thread.start()

    def initUI(self):
        self.setGeometry(100, 100, 600, 400)
        layout = QVBoxLayout()

        self.peers_list = QListWidget()
        layout.addWidget(self.peers_list)

        self.refresh_button = QPushButton("Refresh Peers")
        self.refresh_button.clicked.connect(self.refresh_peers)
        layout.addWidget(self.refresh_button)

        self.test_connection_button = QPushButton("Test Connection")
        self.test_connection_button.clicked.connect(self.test_connection)
        layout.addWidget(self.test_connection_button)

        self.message_edit = QLineEdit()
        layout.addWidget(self.message_edit)

        self.send_message_button = QPushButton("Send Message")
        self.send_message_button.clicked.connect(self.send_message)
        layout.addWidget(self.send_message_button)

        self.message_display = QTextEdit()
        self.message_display.setReadOnly(True)
        layout.addWidget(self.message_display)

        self.send_file_button = QPushButton("Send File")
        self.send_file_button.clicked.connect(self.select_file_to_send)
        layout.addWidget(self.send_file_button)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    

if __name__ == "__main__":
    app = QApplication(sys.argv)
    peer_name = input("Enter your peer name: ")
    try:
        peer = Peer(peer_name)
        gui = PeerGUI(peer)
        gui.show()
        sys.exit(app.exec_())
    except Exception as e:
        print(f"Error: {e}")
