import socket

# Define the server host and port
HOST = '127.0.0.1'
PORT = 12345

def start_server():
    # Create a socket object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Bind the socket to the host and port
    server_socket.bind((HOST, PORT))

    # Listen for incoming connections
    server_socket.listen()

    print(f"Server is listening on {HOST}:{PORT}")

    while True:
        # Accept a connection from a client
        client_socket, client_address = server_socket.accept()
        print(f"Accepted connection from {client_address}")

        # Send a welcome message to the client
        client_socket.sendall(b"Welcome to the server!")

        # Receive data from the client
        data = client_socket.recv(1024)
        print(f"Received data: {data.decode('utf-8')}")

        # Close the client socket
        client_socket.close()

if __name__ == "__main__":
    start_server()
