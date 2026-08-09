"""
Message protocol for the socket client.

This module defines how messages are encoded and decoded
before being sent to or received from the server.
"""

from .config import ENCODING


def encode_message(message: str) -> bytes:
    """Convert a text message to bytes for socket transmission."""
    return message.encode(ENCODING)


def decode_message(data: bytes) -> str:
    """Convert received bytes back to a text message."""
    return data.decode(ENCODING)