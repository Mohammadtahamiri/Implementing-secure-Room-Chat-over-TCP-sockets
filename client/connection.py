"""
Socket connection management for the client.

This module is responsible for creating a TCP socket
and connecting the client to the configured server.
"""
import ssl
import socket

from .config import SERVER_HOST, SERVER_PORT


def create_connection():
    """Create a secure TLS socket and connect it to the server."""

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.check_hostname = False
    context.load_verify_locations("server/certs/server.crt")

    secure_socket = context.wrap_socket(
        client_socket,
        server_hostname=SERVER_HOST
    )

    secure_socket.connect((SERVER_HOST, SERVER_PORT))

    return secure_socket
def close_connection(client_socket: socket.socket) -> None:
    """Close the client socket connection."""
    client_socket.close()