# A Robust Secure P2P File-Sharing System

A comprehensive overview of the secure peer-to-peer (P2P) file-sharing system.

**Introduction**

Our P2P file system represents a decentralized network where each participant (peer) serves both as a client and a server. This architecture has direct sharing and communication between peers, which ensures efficiency and scalability of the system. The system is built with Python and utilizes PyQt5 for the graphical user interface.

**System Architecture**

Central Server
The central server acts as a registry for peers to register and discover each other. It maintains a list of active peers but does not involve itself in file transfers.
Peer
Each peer is capable of performing server-like (e.g., hosting files) and client-like (e.g., requesting files) operations. Peers register with the central server and use direct peer-to-peer connections for file transfers and messaging.
Graphical User Interface (GUI)
It is developed using PyQt5, the GUI provides a user-friendly platform for users to engage with the P2P network, manage files, send messages, and view active peers and system logs.

**Implementation**

The central server acts as a registry for active peers. On startup, it listens on a specified port for incoming connections. When a peer connects, it registers the peer's details (IP, port, name) and shares the list of currently active peers with it. For handling connections, it uses Python's socket and threading libraries to handle multiple simultaneous peer registrations.

Each peer acts as both client and server. On launch, it connects to the central server to register itself and fetch the list of active peers. While sharing files, it can initiate or accept file transfer requests. It handles file data transfer through direct socket connections with other peers. It sends and receives text messages directly to/from other peers, bypassing the central server.
For concurrency control it manages multiple operations (like listening for incoming connections and sending data) concurrently using threads. The GUI displays active peers, allows file transfer initiation, and supports sending/receiving messages. It updates the peer list and messages dynamically, reflecting the current network state. Each peer logs its activity to a unique file, aiding in monitoring and debugging.  Logs include timestamps, operations performed, messages sent/received, and any errors or important events.

Requirements:
You will need Python and PyQt5 for running this file system. For PyQt5 you can install via pip install pyqt5.

Procedure:
1. Start the Central Server:
Navigate to the directory containing the server script (central_server.py).
Run the script: python central_server.py.
The server will start and listen for incoming peer registrations.
2. Launch a Peer Instance:
Navigate to the directory with the peer script (peer.py and peer_gui.py).
Run python peer_gui.py.
Enter a unique name for the peer when prompted.
The GUI will launch, displaying available options like active peers, file transfer, and messaging.

Repeat the process for launching a peer instance for each additional peer you want in the network and ensure each peer has a unique name for identification.

**Key Functionalities and Advantages**

1. End-to-End File Sharing
Direct File Transfers: Peers can send and receive files directly with each other, bypassing the need for a centralized server. This approach reduces bottlenecks and potential points of failure.
GUI-Based Interaction: Users can easily choose files to send and specify destinations for incoming files through an intuitive interface.
Dynamic Participation: New peers can join the network and immediately start sharing files, enhancing the system's flexibility and responsiveness to changing network conditions.
2. Real-Time Messaging System
Instant Communication: The system supports real-time messaging, allowing peers to communicate instantly. This feature is crucial for coordinating file transfers and collaborative activities.
Seamless Integration: Messaging is seamlessly integrated into the peer interface, providing a holistic user experience that combines file sharing and communication.
3. Efficient Peer Discovery
Central Server for Initial Connection: A central server facilitates the initial discovery of peers. Once connected, peers communicate directly.
Scalable Network Topology: The system easily scales as the number of peers increases, maintaining efficiency in peer discovery and overall network performance.
4. Robust Logging Mechanism
Detailed Activity Logs: Each peer session is logged in detail, including actions taken, files transferred, messages sent, and any errors encountered.
Enhanced Troubleshooting: The logs provide valuable insights for troubleshooting and understanding peer behavior, aiding in system maintenance and improvement.
5. Concurrent Read/Write Operations
Simultaneous Operations: The system is designed to handle concurrent read and write operations, ensuring that multiple peers can interact with the system without significant delays or conflicts.

**Future Enhancements**

We have effectively demonstrated the core principles of a P2P network, but future enhancements could include:
Advanced File Versioning: To ensure users always access the latest version of a file.
Encryption: For secure data storage and communication.
User Authentication and Permissions: To provide more granular control over file access and modifications.

This P2P file system implements decentralized file sharing and communication. It has the advantages of P2P networks, such as scalability, direct peer interactions, and reduced reliance on centralized components. 

**References:**

[1] https://www.geeksforgeeks.org/p2p-peer-to-peer-file-sharing/

[2] https://www.tutorialspoint.com/securing-communication-channels-with-diffie-hellman-algorithm-an-implementation-guide

[3] https://cseweb.ucsd.edu/classes/sp16/cse291-e/applications/ln/lecture13.html


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

- **Logging**: 
  - The system incorporates logs to track each operation.
  - Attack detection features are built based on these logs. 
  - Logs differentiate between unauthorized and authorized access or modifications.

