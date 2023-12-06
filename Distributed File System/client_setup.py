#client_setup.py
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import socket
import time

SECRET_KEY = b'16ByteSecretKey!'  # Ensure 16/24/32 bytes for AES key

def encrypt_message(message):
    cipher = AES.new(SECRET_KEY, AES.MODE_ECB)
    padded_message = pad(message.encode(), AES.block_size)
    encrypted_message = cipher.encrypt(padded_message)
    return encrypted_message

def decrypt_message(encrypted_message):
    cipher = AES.new(SECRET_KEY, AES.MODE_ECB)
    decrypted_message = unpad(cipher.decrypt(encrypted_message), AES.block_size)
    return decrypted_message.decode()

def send_command(sock, command):
    sock.send(encrypt_message(command))
    time.sleep(1)
    encrypted_response = sock.recv(1024)
    response = decrypt_message(encrypted_response)
    return response

def get_available_commands(state):
    commands = {
        "not_logged_in": ["login [username] [password]", "exit"],
        "logged_in": ["create [filename] [content]", "delete [filename]", "restore [filename]", "read [filename]",
                      "write [filename][choice:a-append, w-overwrite)][content]", "mkdir [directory name]", "list", 
                      "setperm [path] [user:perm+perm,user:perm]", "cd [path]", "logout"]
    }
    return commands[state]

def set_permissions_prompt(sock, file_or_dir_name):
    print(f"\nSet permissions for '{file_or_dir_name}' (format: user1:read+write,user2:read):")
    permissions = input("Enter permissions: ").strip()
    if permissions:
        perm_command = f"setperm {file_or_dir_name} {permissions}"
        print(send_command(sock, perm_command))

def main():
    state = "not_logged_in"
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect(('localhost', 12345))

        while True:
            print("\nAvailable Commands:")
            for cmd in get_available_commands(state):
                print(f" - {cmd}")

            command = input("\nEnter command: ").strip()
            if not command:
                continue

            if state == "not_logged_in" and command.startswith("login"):
                response = send_command(sock, command)
                if "successful" in response:
                    state = "logged_in"
                print(response)

            elif state == "logged_in":
                if command.startswith("create") or command.startswith("mkdir"):
                    response = send_command(sock, command)
                    print(response)
                    if "created" in response:
                        file_or_dir_name = command.split()[1]
                        set_permissions_prompt(sock, file_or_dir_name)
                elif command == "logout":
                    state = "not_logged_in"
                    print("Logged out.")
                else:
                    print(send_command(sock, command))

            elif command == "exit":
                break

if __name__ == "__main__":
    main()
