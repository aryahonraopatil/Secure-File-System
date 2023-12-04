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
        # Set the log file name
        self.log_file = f"{name}_log_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        
        # Log the start of the peer session
        self.log_message("Peer session started")
        
        # Set the name of the PeerSession
        self.name = name
        
        # Set the server address
        self.server_address = (server_host, server_port)
        
        # Find a free port
        self.peer_port = self.find_free_port(start_port, end_port)
        
        # Raise an exception if no free ports are available
        if self.peer_port is None:
            raise Exception("No free ports available in the specified range.")
        
        # Create a socket for the peer
        self.peer_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.peer_socket.bind(("localhost", self.peer_port))
        self.peer_socket.listen(5)
        
        # Initialize the active peers dictionary
        self.active_peers = {}
        
        # Set the incoming file save path to None
        self.incoming_file_save_path = None
        
        # Create a socket for server communication
        self.server_communication_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Connect to the server
        self.server_communication_socket.connect(self.server_address)
        
        # Register with the server
        self.register_with_server()
        
        # Start a thread for accepting incoming connections
        threading.Thread(target=self.accept_incoming_connections, daemon=True).start()
        
        # Set the file transfer request callback to None
        self.file_transfer_request_callback = None
    
    def log_message(self, message):
        """Log a message to the peer's log file."""
        with open(self.log_file, 'a') as file:
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            file.write(f"{timestamp} - {message}\n")

    def find_free_port(self, start_port, end_port):
        for port in range(start_port, end_port):
            try:
                # Create a temporary socket
                temp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                
                # Bind the socket to localhost and the current port number
                temp_socket.bind(("localhost", port))
                
                # Close the socket
                temp_socket.close()
                
                # Return the port number if the bind was successful
                return port
            except OSError:
                continue
        
        # Return None if no free port is found
        return None

    def register_with_server(self):
        # Create the registration message
        registration_message = json.dumps({
            "type": "register",
            "peer_info": {
                "host": "localhost",
                "port": self.peer_port,
                "name": self.name
            }
        }) + "\n"

        # Send the registration message to the server
        self.server_communication_socket.send(registration_message.encode())

        # Log the registration message
        self.log_message(str(registration_message))

    def maintain_connection_with_server(self):
        while True:
            try:
                # Send heartbeat message to the server
                heartbeat_message = json.dumps({"type": "heartbeat"}) + "\n"
                self.server_communication_socket.send(heartbeat_message.encode())
                
                # Wait for 10 seconds before sending the next heartbeat message
                time.sleep(10)
            
            except BrokenPipeError:
                # Connection lost, attempt to reconnect
                self.log_message("Connection lost. Attempting to reconnect...")
                print("Connection lost. Attempting to reconnect...")
                
                # Wait for 5 seconds before attempting to reconnect
                time.sleep(5)
                
                try:
                    # Create a new socket and connect to the server
                    self.server_communication_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.server_communication_socket.connect(self.server_address)
                    
                    # Register with the server after reconnecting
                    self.register_with_server()
                
                except Exception as e:
                    # Failed to reconnect
                    self.log_message(f"Failed to reconnect: {e}")
                    print(f"Failed to reconnect: {e}")
                    
                    # Break out of the loop and stop maintaining the connection
                    break
            
            except Exception as e:
                # Error maintaining connection with server
                self.log_message(f"Error maintaining connection with server: {e}")
                print(f"Error maintaining connection with server: {e}")
                
                # Break out of the loop and stop maintaining the connection
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
        except json.JSONDecodeError:
            print("Failed to decode JSON from server response")
            self.log_message("Failed to decode JSON from server response")
        except Exception as e:
            print(f"Error: {e}")
            self.log_message(f"Error: {e}")

    def file_save_callback(self, save_path):
        """
        Callback function to be called from the GUI when the user selects a save path for an incoming file.
        """
        self.incoming_file_save_path = save_path

    def accept_incoming_connections(self):
        while True:
            client_socket, _ = self.peer_socket.accept()
            threading.Thread(target=self.handle_incoming_connection, args=(client_socket,)).start()

    
    def check_connection(self, target_peer):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(target_peer)
                check_message = "CONNECTION_CHECK\n"
                s.send(check_message.encode())
                print("Connection check message sent.")
                self.log_message(str(f'Connection check message sent to {target_peer}'))
        except Exception as e:
            print(f"Error checking connection: {e}")
            self.log_message(str(f"Error checking connection: {e}"))

    def set_file_transfer_request_callback(self, callback):
        self.file_transfer_request_callback = callback

    def send_message(self, target_peer, message):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(target_peer)
                message_data = f"MESSAGE:{message}\n"
                s.send(message_data.encode())
                self.log_message(str(f"MESSAGE:{message}\n"))
                print(f"Message sent: {message}")
        except Exception as e:
            print(f"Error sending message: {e}")
            self.log_message(str(f"Error sending message: {e}"))

    def set_message_received_callback(self, callback):
        self.message_received_callback = callback
            


    def handle_incoming_connection(self, client_socket):
        try:
            data = client_socket.recv(1024).decode()
            if data.startswith('CONNECTION_CHECK'):
                print(f"Connection check received from {client_socket.getpeername()}")
                self.message_received_callback(f"Connection check received from {client_socket.getpeername()}")
                # time.sleep(1)  # Delay to ensure message is sent before socket is closed
                client_socket.send("CONNECTION_OK".encode())
                self.log_message(f"Connection check received from {client_socket.getpeername()}")

            elif data.startswith('CONNECTION_OK'):
                print(f"CONNECTION_OK received from {client_socket.getpeername()}")
                self.message_received_callback(f"CONNECTION_OK received from {client_socket.getpeername()}")
                self.log_message(f"CONNECTION_OK received from {client_socket.getpeername()}")

            elif data.startswith('MESSAGE:'):
                # Correctly extract message using partition
                _, _, message = data.partition('MESSAGE:')
                print(f"Received message: {message}")
                self.log_message(f'MESSAGE:{message}')
                if self.message_received_callback:
                    self.message_received_callback(message)


            elif data.startswith('FILE_TRANSFER_REQUEST'):
                _, file_name, file_size = data.split(':')
                file_size = int(file_size)
                self.log_message(f'FILE_TRANSFER_REQUEST: {_},{file_name},{file_size}')
                # Use the file_save_callback to get the save path
                if self.file_save_callback:
                    save_path = self.incoming_file_save_path
                    if save_path is not None:
                        listening_port = self.setup_file_receiving(file_size, save_path)
                    else:
                        listening_port = self.setup_file_receiving(file_size, os.path.join(os.getcwd(), file_name))
                    acceptance_message = f"TRANSFER_ACCEPTED:{listening_port}"
                    self.log_message(f"TRANSFER_ACCEPTED:{file_size, os.path.join(os.getcwd(), file_name)}")
                    client_socket.send(acceptance_message.encode())
                        
                    
                else:
                    client_socket.send("TRANSFER_REJECTED".encode())
                    self.log_message(f'TRANSFER_REJECTED"')


                # Call the file transfer request callback if set
                if self.file_transfer_request_callback:
                    self.file_transfer_request_callback(file_name, file_size, client_socket)

            
            else:
                # Handle case when it's neither a message nor a connection check
                file_name, file_size = data.split(':')
                file_size = int(file_size)
                with open(file_name, 'wb') as file:
                    remaining = file_size
                    while remaining:
                        chunk_size = 4096 if remaining >= 4096 else remaining
                        chunk = client_socket.recv(chunk_size)
                        if not chunk: 
                            break
                        file.write(chunk)
                        remaining -= len(chunk)
                print(f"Received file: {file_name}")
                self.log_message(f"Received file: {file_name}")

        except Exception as e:
            print(f"Error in handle_incoming_connection: {e}")
            self.log_message(f"Error in handle_incoming_connection: {e}")
        finally:
            print("****Socket Closed: peer.py handling incomming connections!****")
            client_socket.close()

    def setup_file_receiving(self, file_size, save_path):
        # Set up a listening socket for the file transfer
        file_receiving_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        file_receiving_socket.bind(("localhost", 0))  # 0 allows the OS to choose an available port
        file_receiving_socket.listen(1)
        listening_port = file_receiving_socket.getsockname()[1]

        # Start a new thread to handle the file reception
        threading.Thread(target=self.receive_file, args=(file_receiving_socket, file_size, save_path), daemon=True).start()

        return listening_port

    def receive_file(self, file_socket, file_size, save_path):
        conn, _ = file_socket.accept()
        with conn:
            try:
                # Read the length of the metadata
                metadata_length = int.from_bytes(conn.recv(4), 'big')

                # Read the metadata
                metadata = conn.recv(metadata_length).decode()
                file_name, size_str = metadata.split(':')
                expected_size = int(size_str)

                # Read the file content
                with open(save_path, 'wb') as f:
                    received = 0
                    while received < expected_size:
                        chunk = conn.recv(min(4096, expected_size - received))
                        if not chunk:
                            break
                        f.write(chunk)
                        received += len(chunk)

                print(f"File received and saved to: {save_path}")
                self.log_message(f"File received and saved to: {save_path}")

            except Exception as e:
                print(f"Error receiving file: {e}")
                self.log_message(f"Error receiving file: {e}")

        file_socket.close()

        

    def send_file_transfer_request(self, target_peer, file_name, file_size):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect(target_peer)
                request_message = f"FILE_TRANSFER_REQUEST:{file_name}:{file_size}\n"
                self.log_message(f"FILE_TRANSFER_REQUEST:{file_name}:{file_size}\n")
                s.send(request_message.encode())
                # Receive the response, which should include the port for the file transfer
                response = s.recv(1024).decode()
                if response.startswith("TRANSFER_ACCEPTED"):
                    self.log_message("TRANSFER_ACCEPTED")
                    _, transfer_port = response.split(':')
                    return int(transfer_port)
                else:
                    return None
        except Exception as e:
            print(f"Error sending file transfer request: {e}")
            self.log_message(f"Error sending file transfer request: {e}")
            return None

    def send_file(self, target_peer, file_path):
        file_name = os.path.basename(file_path)
        file_size = os.path.getsize(file_path)
        transfer_port = self.send_file_transfer_request(target_peer, file_name, file_size)
        if transfer_port:
            try:
                file_transfer_address = (target_peer[0], transfer_port)
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect(file_transfer_address)

                    # Construct and send the metadata
                    metadata = f"{file_name}:{file_size}"
                    metadata_encoded = metadata.encode()
                    s.sendall(len(metadata_encoded).to_bytes(4, 'big'))
                    s.sendall(metadata_encoded)

                    # Send the file
                    with open(file_path, 'rb') as f:
                        while True:
                            bytes_read = f.read(4096)
                            if not bytes_read:
                                break
                            s.sendall(bytes_read)
                    print(f"File sent: {file_name}")
                    self.log_message(f"File sent: {file_name}")
            except Exception as e:
                print(f"Error sending file: {e}")
                self.log_message(f"Error sending file: {e}")

    def close_connections(self):
        self.peer_socket.close()
        self.server_communication_socket.close()

if __name__ == "__main__":
    try:
        name = input("Enter peer name: ")
        peer = Peer(name)
        print(f"Running peer on port {peer.peer_port}")
        peer.log_message(f"Running peer on port {peer.peer_port, name}")
    except Exception as e:
        print(f"Error: {e}")
