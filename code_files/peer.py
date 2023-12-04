# peer.py
import socket
import threading
import json
import os, time
import re
import datetime


import faulthandler

faulthandler.enable()

class Peer:
    def __init__(self, name, server_host="localhost", server_port=12345, start_port=5001, end_port=5100):
        self.log_file = f"{name}_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        self.log_message("Peer session started")
        self.name = name
        
        self.server_address = (server_host, server_port)
        self.peer_port = self.find_free_port(start_port, end_port)
        if self.peer_port is None:
            raise Exception("No free ports available in the specified range.")
        self.peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.peer_socket.bind(("localhost", self.peer_port))
        self.peer_socket.listen(5)
        self.active_peers = {}
        self.incoming_file_save_path = None
        self.server_communication_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_communication_socket.connect(self.server_address)
        self.register_with_server()
        
        
        self.file_transfer_request_callback = None

    def find_free_port(self, start_port, end_port):
        for port in range(start_port, end_port):
            try:
                temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                temp_socket.bind(("localhost", port))
                temp_socket.close()
                return port
            except OSError:
                continue
        return None
    
    def log_message(self, message):
        """Log a message to the peer's log file."""
        with open(self.log_file, 'a') as file:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            file.write(f"{timestamp} - {message}\n")

    def register_with_server(self):
        registration_message = json.dumps({
            "type": "register",
            "peer_info": {
                "host": "localhost",
                "port": self.peer_port,
                "name": self.name
            }
        }) + "\n"
        self.server_communication_socket.send(registration_message.encode())
        self.log_message(str(registration_message))

    def maintain_connection_with_server(self):
        while True:
            try:
                heartbeat_message = json.dumps({"type": "heartbeat"}) + "\n"
                self.server_communication_socket.send(heartbeat_message.encode())
                time.sleep(10)
            except BrokenPipeError:
                self.log_message("Connection lost. Attempting to reconnect...")
                print("Connection lost. Attempting to reconnect...")
                time.sleep(5)
                try:
                    self.server_communication_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.server_communication_socket.connect(self.server_address)
                    self.register_with_server()
                except Exception as e:
                    self.log_message(f"Failed to reconnect: {e}")
                    print(f"Failed to reconnect: {e}")
                    break
            except Exception as e:
                self.log_message(f"Error maintaining connection with server: {e}")
                print(f"Error maintaining connection with server: {e}")
                break

    def fetch_active_peers(self):
        try:
            self.log_message("Requesting active peers list from server...")
            print("Requesting active peers list from server...")
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(self.server_address)
                request_message = json.dumps({"type": "request_list"}) + "\n"
                s.send(request_message.encode())
                self.log_message(str(request_message))
                response = s.recv(1024).decode()
                if response:
                    self.active_peers = json.loads(response)
                    print("Received active peers list:", self.active_peers)
                    self.log_message(f"Received active peers list: {self.active_peers}")
                else:
                    print("No response or empty response received from server")
                    self.log_message("No response or empty response received from server")
        
        except Exception as e:
            print(f"Error: {e}")
            self.log_message(f"Error: {e}")
if __name__ == "__main__":
    try:
        name = input("Enter peer name: ")
        peer = Peer(name)
        print(f"Running peer on port {peer.peer_port}")
        peer.log_message(f"Running peer on port {peer.peer_port, name}")
    except Exception as e:
        print(f"Error: {e}")
