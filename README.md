# A robust secure file-sharing system 

The file sharing system is described in detail below:

● This is a P2P file system. 
● Users can create, delete, read, write, restore files.
● A client should always see the latest version of a file, or at least that a
client should never see an older version of a file after it sees a newer one.
● Users should be able to set permissions on files and directories, which
also requires that your file system be able to name users.
● The system should be able to deal with concurrent write and read.
● File names (and directory names) should be treated as confidential. The
data stored in each peer node should be encrypted.
● The communication between Peer to Peer should be encrypted.
● Users should not be able to modify files or directories without being
detected unless they are authorized to do so.
● A malicious file server should not be able to create or delete files or
directories without being detected.
● Incorporate a log into your file system to track each operation on yourserver.
Using your knowledge from the first project, define features that will be used
to detect attacks to your system. Generate logs with unauthorized
access/modifications and logs with authorized access/modifications. Build your
detector.
● Define the vulnerability of your detector.
