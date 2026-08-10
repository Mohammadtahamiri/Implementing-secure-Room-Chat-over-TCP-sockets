"""
Authentication utilities for the socket client.

This module handles username and password input
and prepares authentication data for the server.
"""

import getpass


def get_credentials() -> tuple[str, str]:
    """Read username and password from the user."""
    username = input("Username: ").strip()
    password = getpass.getpass("Password: ")

    return username, password


def build_auth_message(username: str, password: str) -> str:
    """Build the authentication message sent to the server."""
    return f"AUTH|{username}|{password}"