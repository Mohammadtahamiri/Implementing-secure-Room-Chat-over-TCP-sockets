"""
Socket connection management for the client.

This module is responsible for creating a TCP socket
and connecting the client to the configured server.
"""

import socket

from .config import SERVER_HOST, SERVER_PORT


def create_connection() -> socket.socket:
    """Create a TCP socket and connect it to the server."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client_socket.connect((SERVER_HOST, SERVER_PORT))

    return client_socket


def close_connection(client_socket: socket.socket) -> None:
    """Close the client socket connection."""
    client_socket.close()