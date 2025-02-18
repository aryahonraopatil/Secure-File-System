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

    def handle_file_transfer_request_gui(self, file_name, file_size, client_socket):
        # Prompt the user to accept or reject the file transfer request
        response = QMessageBox.question(
            self, "File Transfer Request",
            f"Accept file '{file_name}' ({file_size} bytes)?",
            QMessageBox.Yes | QMessageBox.No
        )

        if response == QMessageBox.Yes:
            # Prompt the user to choose a save path for the file
            save_path, _ = QFileDialog.getSaveFileName(
                self, "Save File As", file_name, "All Files (*.*)"
            )

            if save_path:
                try:
                    # Send an acceptance message to the client
                    client_socket.send("TRANSFER_ACCEPTED".encode())
                except Exception as e:
                    print(f"Error sending acceptance: {e}")

                # Set up the server to receive the file
                self.peer.setup_file_receiving(file_size, save_path)
        else:
            try:
                # Send a rejection message to the client
                client_socket.send("TRANSFER_REJECTED".encode())
            finally:
                print('****Socket is being closed at gui file handling.****')
                client_socket.close()

    

    def test_connection(self):
        # Get the selected item from the peers_list
        selected_item = self.peers_list.currentItem()

        if selected_item:
            # Get the text of the selected item
            selected_text = selected_item.text()

            # Split the text into name and address
            name, addr = selected_text.split(' (')

            # Split the address into host and port
            host, port_str = addr.rstrip(')').split(':')

            # Convert the port to an integer
            port = int(port_str)

            # Create a target peer tuple with the host and port
            target_peer = (host.strip(), port)

            # Check the connection to the target peer
            self.peer.check_connection(target_peer)
        else:
            # Display a warning message if no peer is selected
            QMessageBox.warning(self, "Warning", "Select a peer first")

    @pyqtSlot(str)
    def on_message_received(self, message):
        self.message_received_signal.emit(message)

    def display_message(self, message):
        self.message_display.append(f"{message}")


    def send_message(self):
        selected_item = self.peers_list.currentItem()
        if selected_item:
            message = self.message_edit.text()
            
            if message:
                selected_text = selected_item.text()
                name, addr = selected_text.split(' (')
                host, port_str = addr.rstrip(')').split(':')
                port = int(port_str)
                target_peer = (host.strip(), port)
                message = f'{peer.name} to {name}: {message}'
                self.peer.send_message(target_peer, message)
                self.display_message(f"{message}")
                self.message_edit.clear()
            else:
                QMessageBox.warning(self, "Warning", "Enter a message")
        else:
            QMessageBox.warning(self, "Warning", "Select a peer first")
 
    

    def refresh_peers(self):
        self.peer.fetch_active_peers()
        self.update_peers_list(self.peer.active_peers)

    def update_peers_list(self, active_peers):
        self.peers_list.clear()
        for address, info in active_peers.items():
            if info['name'] != self.peer.name:
                self.peers_list.addItem(f"{info['name']} ({info['host']}:{info['port']})")

    def select_file_to_send(self):
        selected_item = self.peers_list.currentItem()
        
        if selected_item:
            # Prompt the user to select a file
            file_path, _ = QFileDialog.getOpenFileName(self, "Open File", "", "All Files (*.*)")
            
            if file_path:
                # Correctly parse the host and port from the selected item's text
                selected_text = selected_item.text()
                name, addr = selected_text.split(' (')
                host, port_str = addr.rstrip(')').split(':')
                port = int(port_str)
                target_peer = (host.strip(), port)
                
                # Send the file to the target peer
                self.peer.send_file(target_peer, file_path)
        else:
            QMessageBox.warning(self, "Warning", "Select a peer first")


    def handle_file_transfer_request_gui(self, file_name, file_size, client_socket):
        # Ask the user if they want to accept the file transfer request
        response = QMessageBox.question(
            self,
            "File Transfer Request",
            f"Accept file '{file_name}' ({file_size} bytes)?",
            QMessageBox.Yes | QMessageBox.No
        )

        if response == QMessageBox.Yes:
            # Ask the user to specify a save location
            save_path, _ = QFileDialog.getSaveFileName(
                self,
                "Save File As",
                file_name,
                "All Files (*.*)"
            )
            if save_path:
                # Only set up file receiving; the sending of the acceptance message is handled in peer.py
                self.peer.file_save_callback(save_path)
            else:
                print('File transfer rejected by user. No save location specified.')
        else:
            print('File transfer rejected by user.')

        # Close the client_socket in either case, as the response is handled in peer.py
        print('****Socket is being closed at GUI file handling.****')
        client_socket.close()

    def closeEvent(self, event):
        self.peer.close_connections()
        event.accept()

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
