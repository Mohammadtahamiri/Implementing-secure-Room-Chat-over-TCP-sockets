"""
Main entry point for the socket client.

This module connects to the server, authenticates the user,
and provides a simple loop for sending and receiving messages.
"""
import time
from .authentication import get_credentials, build_auth_message
from .connection import create_connection, close_connection
from .protocol import encode_message, decode_message
from .config import BUFFER_SIZE

def reconnect(username: str, password: str):
    """Reconnect to the server and log the user in again."""
    while True:
        client_socket = None

        try:
            print("Connection lost. Reconnecting...")
            client_socket = create_connection()

            # Receive AUTH_REQUIRED from the server
            response = client_socket.recv(BUFFER_SIZE)
            print("Server:", decode_message(response))

            # Login again with the existing credentials
            login_message = f"LOGIN {username} {password}"
            client_socket.sendall(encode_message(login_message))

            response = client_socket.recv(BUFFER_SIZE)
            login_response = decode_message(response).strip()

            print("Server:", login_response)

            if login_response == "LOGIN_SUCCESS":
                print("Reconnected successfully.")
                return client_socket

            close_connection(client_socket)

        except OSError as error:
            print(f"Reconnect failed: {error}")

            if client_socket is not None:
                close_connection(client_socket)

        print("Retrying in 3 seconds...")
        time.sleep(3)

def main() -> None:
    """Run the socket client."""
    client_socket = None

    try:
        print("Connecting to server...")
        client_socket = create_connection()
        print("Connected successfully.")

        response = client_socket.recv(BUFFER_SIZE)
        print("Server:", decode_message(response))

        username, password = get_credentials()

        register_message = f"REGISTER {username} {password}"
        client_socket.sendall(encode_message(register_message))

        response = client_socket.recv(BUFFER_SIZE)
        register_response = decode_message(response)
        print("Server:", register_response)

        login_message = f"LOGIN {username} {password}"
        client_socket.sendall(encode_message(login_message))

        response = client_socket.recv(BUFFER_SIZE)
        login_response = decode_message(response).strip()
        print("Server:", login_response)

        if login_response != "LOGIN_SUCCESS":
           print("Authentication failed.")
           return
        client_socket.sendall(encode_message("GET_MISSED"))

        while True:
            response = client_socket.recv(BUFFER_SIZE)

            if not response:
                break

            response_text = decode_message(response).strip()

            if response_text == "[MISSED_MESSAGES_START]":
                continue

            if response_text == "[MISSED_MESSAGES_END]":
                break

            print(response_text)

        while True:
            message = input("Message (type 'exit' to quit): ").strip()

            if message.lower() == "exit":
                break

            if not message:
                continue

            client_socket.sendall(encode_message(message))

            response = client_socket.recv(BUFFER_SIZE)
            print("Server:", decode_message(response))

    except ConnectionRefusedError:
        print("Connection failed: server is not available.")

    except OSError as error:
        print(f"Socket error: {error}")

    finally:
        if client_socket is not None:
            close_connection(client_socket)
            print("Connection closed.")


if __name__ == "__main__":
    main()