import socket

# Define the server host and port
HOST = '127.0.0.1'
PORT = 12345

def start_client():
    # Create a socket object
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Connect to the server
    client_socket.connect((HOST, PORT))

    # Receive the welcome message from the server
    welcome_message = client_socket.recv(1024)
    print(welcome_message.decode('utf-8'))

    # Send data to the server
    message = "Hello, server!"
    client_socket.sendall(message.encode('utf-8'))

    # Close the client socket
    client_socket.close()

if __name__ == "__main__":
    start_client()
