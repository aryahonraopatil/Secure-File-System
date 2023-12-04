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
        self.name = name
        
        self.server_address = (server_host, server_port)
        self.peer_port = self.find_free_port(start_port, end_port)
        if self.peer_port is None:
            raise Exception("No free ports available in the specified range.")
        self.peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.peer_socket.bind(("localhost", self.peer_port))
        self.peer_socket.listen(5)
        self.active_peers = {}
        self.server_communication_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_communication_socket.connect(self.server_address)
        self.register_with_server()
        
        
        self.file_transfer_request_callback = None

if __name__ == "__main__":
    try:
        name = input("Enter peer name: ")
        peer = Peer(name)
        print(f"Running peer on port {peer.peer_port}")
        peer.log_message(f"Running peer on port {peer.peer_port, name}")
    except Exception as e:
        print(f"Error: {e}")
