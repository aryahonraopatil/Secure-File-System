from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QListWidget, QFileDialog, QMessageBox, QLineEdit, QTextEdit
from PyQt5.QtCore import pyqtSignal, pyqtSlot, QThread
import sys, time
import threading
from peer import Peer

import faulthandler


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
