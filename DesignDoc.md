# Design Document: Peer-to-Peer (P2P) Secure File Sharing System

## 1. Introduction

The P2P secure file sharing system aims to facilitate decentralized, secure, and efficient data transfer and storage. This design document delineates its architecture, user interactions, and various components ensuring its functionality.

## 2. System Overview

The system will function within a P2P network framework where participants can serve and request files. The design emphasizes user-friendliness, data integrity, and robust security mechanisms.

The Peer-to-Peer architecture will have the following properties:
1. Node Identification and Discovery:
Each peer node is identified by a unique identifier generated using a hash function (such as SHA-256) applied to its public key.
Implement a Distributed Hash Table (DHT) for efficient peer discovery. The DHT allows peers to find each other without relying on a central server.

Pseudocode for a Distributed Hash Table (DHT) used for peer discovery:

```python
class DHTNode:
    def __init__(self, node_id, data=None):
        self.node_id = node_id  # Unique identifier for the node
        self.data = data        # Data stored at this node
        self.neighbors = {}     # Dictionary to store neighboring nodes (node_id: node_address)

class DHT:
    def __init__(self):
        self.nodes = {}  # Dictionary to store nodes (node_id: DHTNode)

    def hash_function(self, data):
        # Implement a hash function to generate node IDs (e.g., SHA-256)
        pass

    def find_successor(self, target_id):
        # Find the successor node for a given target ID
        pass

    def join(self, new_node):
        # Join a new node to the DHT network
        # 1. Find the successor node for the new node's ID
        successor = self.find_successor(new_node.node_id)
        
        # 2. Update the new node's neighbors and notify other nodes about the new node
        new_node.neighbors = successor.neighbors
        successor.neighbors = {new_node.node_id: new_node}
        
        # 3. Add the new node to the DHT nodes dictionary
        self.nodes[new_node.node_id] = new_node

    def store(self, key, value):
        # Store a key-value pair in the DHT
        node_id = self.hash_function(key)
        successor = self.find_successor(node_id)
        successor.data[key] = value

    def lookup(self, key):
        # Look up a key in the DHT and return its value
        node_id = self.hash_function(key)
        successor = self.find_successor(node_id)
        return successor.data.get(key, None)
``` 
2. Data Encryption and Decryption:
Encrypt both file contents and metadata before storing them on peer nodes using strong encryption algorithms like AES (Advanced Encryption Standard).

Pseudocode for Data Encryption and Decryption

``` python
class PeerNode:
    def __init__(self, public_key):
        self.public_key = public_key  # Public key of the peer node

    def generate_aes_key(self):
        # Generate a random AES key for encrypting file contents and metadata
        return AES.new(self.generate_random_bytes(16), AES.MODE_ECB)

    def generate_random_bytes(self, size):
        # Generate random bytes for key generation
        pass

    def encrypt_file(self, file_data, aes_key):
        # Encrypt file contents using AES encryption
        cipher = aes_key.encrypt(self.pad_data(file_data))
        return cipher

    def decrypt_file(self, encrypted_data, aes_key):
        # Decrypt file contents using AES decryption
        decrypted_data = aes_key.decrypt(encrypted_data)
        return self.unpad_data(decrypted_data)

    def pad_data(self, data):
        # Implement data padding for AES encryption
        pass

    def unpad_data(self, data):
        # Implement data unpadding for AES decryption
        pass

    def encrypt_aes_key(self, recipient_public_key, aes_key):
        # Encrypt the AES key using recipient's public key (RSA encryption)
        cipher_rsa = RSA.encrypt(aes_key, recipient_public_key)
        return cipher_rsa

    def decrypt_aes_key(self, encrypted_aes_key, private_key):
        # Decrypt the AES key using recipient's private key (RSA decryption)
        aes_key = RSA.decrypt(encrypted_aes_key, private_key)
        return aes_key
```

3. Data Integrity and Verification:
Implement cryptographic hashes (e.g., SHA-256) to verify the integrity of file chunks. Peers can verify the received data chunks against these hashes to ensure they have not been tampered with during transmission.

Pseudocode for Data Integrity and Verification

``` python
class FileChunk:
    def __init__(self, data):
        self.data = data  # Data of the file chunk
        self.hash = self.calculate_hash()  # Hash of the file chunk's data

    def calculate_hash(self):
        # Calculate the SHA-256 hash of the file chunk's data
        sha256 = hashlib.sha256()
        sha256.update(self.data)
        return sha256.hexdigest()

class PeerNode:
    def __init__(self):
        self.received_chunks = {}  # Dictionary to store received file chunks (chunk_index: FileChunk)

    def receive_file_chunk(self, chunk_index, chunk_data, original_hash):
        # Receive a file chunk along with its index and original hash
        received_chunk = FileChunk(chunk_data)

        # Verify the integrity of the received chunk
        if received_chunk.hash == original_hash:
            self.received_chunks[chunk_index] = received_chunk
            print(f"Received chunk {chunk_index} successfully.")
        else:
            print(f"Received chunk {chunk_index} is corrupted. Discarding.")

    def verify_file_integrity(self, original_hashes):
        # Verify the integrity of received file chunks against original hashes
        for index, original_hash in original_hashes.items():
            received_chunk = self.received_chunks.get(index)
            if received_chunk:
                if received_chunk.hash == original_hash:
                    print(f"Chunk {index} verified and intact.")
                else:
                    print(f"Chunk {index} is corrupted.")
            else:
                print(f"Chunk {index} is missing.")
``` 
4. Routing and Message Passing:
Implement a routing algorithm based on the DHT to facilitate message passing between peers.

5. Secure Communication Channels:
Use secure communication protocols (such as TLS/SSL) for all communication channels between peers to prevent eavesdropping and man-in-the-middle attacks.

Pseudocode for building secure communication channels

``` python
class SecurePeerNode:
    def __init__(self, host, port):
        self.host = host
        self.port = port

    def create_secure_connection(self):
        # Create a TCP socket
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Wrap the socket with SSL/TLS context
        context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        secure_socket = context.wrap_socket(client_socket, server_hostname=self.host)

        # Establish a connection to the server
        secure_socket.connect((self.host, self.port))
        return secure_socket
```

6. Intrusion Detection and Prevention:

Implement an Intrusion Detection System (IDS) to monitor peer activities and detect suspicious behavior.

``` python
class IntrusionDetectionSystem:
    def __init__(self):
        self.rules = []  # List to store detection rules

    def add_detection_rule(self, rule):
        # Add a detection rule to the IDS
        self.rules.append(rule)

    def monitor_peer_activity(self, peer_activity):
        # Monitor peer activity and check against detection rules
        for rule in self.rules:
            if rule.matches(peer_activity):
                self.handle_intrusion(peer_activity, rule)

    def handle_intrusion(self, peer_activity, rule):
        # Handle detected intrusion (e.g., log, block, alert)
        print(f"Intrusion detected: {peer_activity} - {rule.description}")

class DetectionRule:
    def __init__(self, pattern, description):
        self.pattern = pattern  # Regular expression pattern to match peer activity
        self.description = description  # Description of the detection rule

    def matches(self, peer_activity):
        # Check if the peer activity matches the rule's pattern
        # Return True if there is a match, False otherwise
        pass
```
## 3. System Components

### 3.1 User Management

Facilitates user-based interactions:

- **Registration**: Enables unique account creation.
- **Login**: Validates and authenticates existing users.

### 3.2 File Management

Guarantees file integrity and confidentiality:

- **CRUD Operations**: Encompasses standard file operations.
- **Encryption/Decryption**: Safeguards file data.
- **Version Control**: Guarantees up-to-date file access.

### 3.3 Peer-to-Peer Communication

Orchestrates secure peer transactions:

- **Listening Mode**: Awaits incoming file transfer requests.
- **Send Mode**: Initiates outbound file transfer requests.

### 3.4 Logs

Monitors, records, and reports all user actions for security and auditing.

## 4. Detailed Component Specifications

### 4.1 User Management

#### 4.1.1 Registration

- Gather `username`, `password`.
- Use secure password hashing (e.g., bcrypt) before storage.

#### 4.1.2 Login

- Authenticate by comparing entered and stored hashed passwords.

### 4.2 File Management

#### 4.2.1 File Encryption/Decryption

- Employ AES for encryption.
- Ensure secure key management.

#### 4.2.2 Version Control

- Associate files with version tags.
- On update, increment version tag.

### 4.3 Peer-to-Peer Communication

#### 4.3.1 Start Listening

- Await incoming file requests on a dedicated port.

#### 4.3.2 Send File

- Designate file and recipient.
- Transfer encrypted file data.

### 4.4 Logs

- Timestamp and document each user action.

## 5. User Interface (UI)

Tkinter-based user interface:

- **Main Window**: Display system status; access modes.
- **Login/Registration Window**: Facilitate user account operations.
- **Logs Window**: Present real-time system logs.

## 6. Security Considerations

- **Communication**: Secure peer interactions via TLS.
- **Data at Rest**: Ensure files are encrypted when stored.
- **Data in Transit**: Preserve encryption during file transfers.
- **Authentication**: Store passwords as secure hashes.
- **Authorization**: Validate user permissions for actions.

## 7. Development Strategy

### 7.1 Phase 1: Core Backend Development

- Establish User and File Management systems.

### 7.2 Phase 2: P2P Communication

- Create mechanisms for secure data transfers.

### 7.3 Phase 3: Frontend Development

- Sculpt the Tkinter-based GUI.

### 7.4 Phase 4: Testing and Refinement

- Evaluate components and fine-tune as necessary.

### 7.5 Phase 5: Security Auditing

- Conduct external and internal security reviews.

## 8. Testing Strategy

### 8.1 Unit Testing

- Isolate and evaluate individual components.

### 8.2 Integration Testing

- Examine the seamless operation between components.

### 8.3 Security Testing

- Identify vulnerabilities using ethical hacking methods.

## 9. Malicious Activity Detection

### 9.1 Overview

Incorporate a basic detection framework to spot and flag potentially malicious peer actions.

### 9.2 Detector Design

#### 9.2.1 File Integrity Checks

- Each file has a unique hash.
- Mismatches in hash values after operations suggest unauthorized alterations.

#### 9.2.2 Permission Verification

- Validate each peer operation against a permissions list.
- Flag and deny unauthorized activities.

### 9.3 Alerts & Responses

#### 9.3.1 Notifications

- Notify users or admins of potential malicious activities.

#### 9.3.2 Log Tracking

- Thoroughly log all operations.
- Frequent checks can unveil suspicious patterns.

## 10. Conclusion

The P2P Secure File Sharing System aims to be a vanguard solution for modern decentralized data transfer needs, with in-built mechanisms to detect and counteract malicious activities.

## Appendices

### A. Libraries and Technologies

- Python 3.x
- Tkinter (UI)
- Cryptography (encryption)
- Socket programming (network communication)
- Bcrypt (password hashing)

### B. Risks & Mitigations

- **Eavesdropping**: Mitigated via encrypted communication.
- **Unauthorized File Operations**: File integrity checks and permissions validations.
