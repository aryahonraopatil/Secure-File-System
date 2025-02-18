# Design Document: Peer-to-Peer (P2P) Secure File Sharing System

## 1. Introduction

The P2P secure file sharing system aims to facilitate decentralized, secure, and efficient data transfer and storage. This design document delineates its architecture, user interactions, and various components ensuring its functionality.

## 2. System Overview

The system will function within a P2P network framework where participants can serve and request files. The design emphasizes user-friendliness, data integrity, and robust security mechanisms.

## 3. System Components

### 3.1 User Management
Handles user-based interactions and cryptographic operations:

- **Registration**: Enables account creation and initiates Diffie-Hellman key pair generation.
- **Login**: Validates and authenticates users.
- **Key Exchange**: Allows users to securely share public keys and compute a shared secret for encrypted communication.

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
- Hash the password using a secure method (e.g., bcrypt) and store in the database.
- Generate a Diffie-Hellman key pair (public_key, private_key) for the user.
- Store the public_key in the database (the private_key remains confidential to the user).

#### 4.1.2 Login

- Authenticate by comparing the entered password with the stored hashed password.

#### 4.1.3 Initiate Key Exchange

- Send the user's public_key to a specified peer.

#### 4.1.4 Receive Key Exchange

- Receive a public_key from a requesting peer.
- Use the stored private_key and the received public_key to compute a shared_secret.
- Store this shared_secret securely for encrypted communication with the specific peer.


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

- **Key Exchange**: Employ the Diffie-Hellman protocol to securely exchange keys and derive a shared secret for encrypted peer-to-peer communications. The shared secret, combined with a symmetric encryption algorithm like AES, ensures secure data transmission between peers.

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

- Flask (web framework)
- Flask-Login (user session management)
- Cryptography (encryption and key management)
- SQLite (database)
- Bcrypt (password hashing)
- Diffie-Hellman library (for key exchange and deriving shared secrets)

### B. Risks & Mitigations

- **Eavesdropping**: Mitigated via encrypted communication.
- **Unauthorized File Operations**: File integrity checks and permissions validations.
