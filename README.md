# Secure-Payment-Processing-Distibuted-Systems

## Overview
This project implements a secure and synchronized payment processing system in a distributed environment using Python. It models a real-world scenario where multiple clients can perform transactions through a server using the Two-Phase Commit Protocol to ensure atomicity and consistency.

Key features of the system include:
- Secure communication using encryption keys (symmetric/asymmetric).
- Vector clocks for tracking event order across distributed nodes.
- Transaction validation via vote-based commit/abort decisions.
- A central server that coordinates and ensures consistent updates between clients.

## Repository Structure
```
.
Secure-Payment-Processing-Distributed-System/
│
├── .venv/            
├── .gitignore       
├── Client1.py        
├── Client2.py        
├── server.py         
└── README.md        
```

## Installation and Usage

### Prerequisites
- Python 3.7+: Download Python
- Git (for cloning the repository): Download Git
- VS Code or any Python IDE

### Installation
1. Clone the repository:
```bash
   git clone https://github.com/your_username/distributed-systems-chandy-misra-hass.git
   ```
2. Navigate to the project directory:
   ```bash
   cd Secure-Payment-Processing-Distributed-System
   ```
3. Set up a virtual environment:
   ```bash
   python -m venv .venv
   ```
4. Activate the virtual environment:
    1. On Windows:
        ```bash
        .venv\Scripts\activate
        ```
    2. On macOS/Linux:
        ```bash
        source .venv/bin/activate
        ```
5. Install dependencies:
    ```bash
    pip install cryptography flask
    ```

### Running the Server Code
1. Run the `Server` script::
   ```bash
   python server.py
   ```
2. Follow the prompt to configure the server settings, such as port number and IP address. The server will wait for incoming connections from clients.

### Running the Client1 Code
1. Run the `Client1` script::
   ```bash
   python Client1.py

   ```
2. Follow the prompts to input the server IP address and port number. The client will connect to the server and send/receive data based on the protocol.

### Running the Client2 Code
1. Run the `Client2` script::
   ```bash
   python Client2.py
   ```
2. Follow the prompts to input the server IP address and port number. The client will connect to the server and send/receive data, similar to client1, but with a different user or functionality.

## Code Details

### Server (`server.py`)
This script sets up a secure server using sockets and SSL (Secure Sockets Layer) to handle encrypted payment transactions. It validates client connections, processes payment requests, and sends acknowledgments back to clients securely.

### Client1 (`Client1.py`)
This script simulates a payment request from a customer. It establishes an SSL-encrypted connection with the server, sends payment details (like amount, card info, and transaction ID), and waits for confirmation.

### Client2 (`Client2.py`)
This script acts as a second client initiating a different payment transaction. It behaves similarly to client1.py but can be used concurrently to simulate multiple client interactions with the server.

## Conclusion
The Secure Payment Processing system effectively demonstrates encrypted client-server communication using SSL, ensuring safe handling of sensitive payment data. It supports multiple clients, maintains data integrity, and mirrors real-world financial transactions. Future improvements may include authentication and transaction logging.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

### Acknowledgments
- Our project supervisor and course instructors.
- The open-source community for their contributions to the libraries used in this project.



