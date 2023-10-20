# UML Diagrams

## 1. Component Diagram

The component diagram offers a high-level view of how different components of the system interact with each other.

- **User Management**: Handles user registration, login, and key exchange processes.
- **File Management**: Manages file CRUD operations, encryption/decryption, and version control.
- **P2P Communication**: Manages the peer-to-peer interactions, including listening and sending modes.
- **Logs**: Captures and displays user actions and system events.

Arrows indicate the flow of data and control between the components.

![Component Diagram](/diagrams/component.svg "Component Diagram")

## 2. Deployment Diagram

The deployment diagram illustrates the system's deployment architecture, showing how different software components are placed on hardware.

- **Client Node**: Represents a user's machine in the P2P network. It hosts the P2P Secure File Sharing application.
- **Database Server**: Represents the centralized server where user credentials and file metadata are stored.

Connections show data flow and interactions between nodes.

![Deployment Diagram](/diagrams/deployment.svg "Deployment Diagram")

## 3. Activity Diagram

The activity diagram depicts the flow of control in the system, showing the sequence of activities performed.

- Starts with the "User Login" activity.
- Branches out based on user choices, such as "Upload File", "Download File", or "View Logs".
- Each activity, like "Encrypt File" or "P2P Transfer", represents a specific action in the system.
- Ends with the "Logout" activity.

Arrows indicate the flow from one activity to the next, and decision nodes represent points where choices are made.

![Activity Diagram](/diagrams/activity.svg "Activity Diagram")
