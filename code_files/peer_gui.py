from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QListWidget, QFileDialog, QMessageBox, QLineEdit, QTextEdit
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread
import sys, time
import threading
from peer import Peer

import faulthandler

faulthandler.enable()




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
