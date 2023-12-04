# A Robust Secure P2P File-Sharing System

A comprehensive overview of the secure peer-to-peer (P2P) file-sharing system.

**Introduction**

Our P2P file system represents a decentralized network where each participant (peer) serves both as a client and a server. This architecture has direct sharing and communication between peers, which ensures efficiency and scalability of the system. The system is built with Python and utilizes PyQt5 for the graphical user interface.

## Core Features:

- **File Operations**: 
  - Users have the ability to:
    * Create files
    * Delete files
    * Read files
    * Write to files
    * Restore files

- **Version Control**: 
  - Clients are always presented with the latest version of a file. They should never see an older version once they've accessed a newer one.

- **User Permissions and Naming**: 
  - Users can set specific permissions on files and directories.
  - For effective permissions, the system is capable of uniquely naming users.

- **Concurrency**: 
  - The system effectively handles concurrent read and write operations.

- **Data Confidentiality and Encryption**: 
  - File and directory names are treated with confidentiality.
  - Data stored on each peer node is encrypted.
  - Peer-to-Peer communications are encrypted for additional security.

- **Integrity and Authorization**: 
  - Unauthorized file or directory modifications are detected.
  - Only authorized users can make modifications.

- **Malicious Activity Prevention**: 
  - Malicious servers are prevented from creating or deleting files/directories without detection.

- **Logging**: 
  - The system incorporates logs to track each operation.
  - Attack detection features are built based on these logs. 
  - Logs differentiate between unauthorized and authorized access or modifications.

## Security and Detection:

- **Attack Detection**: 
  - Features are in place to detect potential attacks on the system.
  - Unauthorized access or modifications are logged and detected.

- **Vulnerability Assessment**: 
  - Regular assessments are conducted to define and understand potential vulnerabilities in the attack detection system.

