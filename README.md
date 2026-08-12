# Secure Room Chat over TCP Sockets

The first telecommunications network project.

## Project Description

This project implements a secure room chat application using TCP sockets in Python. It provides client-server communication with secure connections, user authentication, and real-time message exchange between connected users.

## Features

- TCP socket communication
- Secure connection using SSL/TLS
- User registration and authentication
- Multiple client support
- Real-time message receiving
- Background thread for receiving messages
- Message encoding and decoding
- Automatic reconnection after connection loss
- Missed message recovery after reconnection

## Project Structure

```text
client/
    authentication.py
    config.py
    connection.py
    main.py
    protocol.py

server/
    certs/
    database.py
    server.py

tests/
    test_protocol.py

README.md
requirements.txt
```

## Requirements

- Python 3
- pip

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## How to Run

First, start the server from the project root:

```bash
python server/server.py
```

Then open another terminal and start a client:

```bash
python client/main.py
```

To test communication between multiple users, open additional terminals and run:

```bash
python client/main.py
```

## Running Tests

Run the automated tests from the project root:

```bash
python -m pytest
```

## Git Workflow

Development is performed using separate feature branches. Changes are committed progressively using Conventional Commit messages and merged into the main branch through Pull Requests.