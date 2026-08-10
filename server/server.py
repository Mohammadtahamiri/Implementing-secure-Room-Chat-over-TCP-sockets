import socket
import ssl
import threading
from database import init_db, register_user, authenticate_user, log_message

HOST = '127.0.0.1'
PORT = 12345

clients = {}

def handle_client(client_socket, client_address):
    current_user = None
    try:
        client_socket.sendall(b"AUTH_REQUIRED\n")
        
        while not current_user:
            data = client_socket.recv(1024).decode('utf-8').strip()
            if not data:
                return
            
            parts = data.split()
            cmd = parts[0].upper()
            
            if cmd == "REGISTER" and len(parts) == 3:
                username, password = parts[1], parts[2]
                if register_user(username, password):
                    client_socket.sendall(b"REGISTER_SUCCESS\n")
                else:
                    client_socket.sendall(b"REGISTER_FAILED\n")
                    
            elif cmd == "LOGIN" and len(parts) == 3:
                username, password = parts[1], parts[2]
                if authenticate_user(username, password):
                    current_user = username
                    clients[current_user] = client_socket
                    client_socket.sendall(b"LOGIN_SUCCESS\n")
                else:
                    client_socket.sendall(b"LOGIN_FAILED\n")
            else:
                client_socket.sendall(b"INVALID_COMMAND\n")

        while True:
            msg = client_socket.recv(1024).decode('utf-8')
            if not msg:
                break
            
            log_message(current_user, msg.strip())
            broadcast_msg = f"[{current_user}]: {msg}"
            
            for user, sock in list(clients.items()):
                if user != current_user:
                    try:
                        sock.sendall(broadcast_msg.encode('utf-8'))
                    except:
                        sock.close()
                        del clients[user]

    except Exception:
        pass
    finally:
        if current_user and current_user in clients:
            del clients[current_user]
        client_socket.close()

def start_server():
    init_db()
    
    context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
    context.load_cert_chain(certfile="certs/server.crt", keyfile="certs/server.key")

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    
    ssl_socket = context.wrap_socket(server_socket, server_side=True)
    print(f"[+] Secure Server listening on {HOST}:{PORT}...")

    while True:
        client_sock, addr = ssl_socket.accept()
        thread = threading.Thread(target=handle_client, args=(client_sock, addr))
        thread.start()

if __name__ == "__main__":
    start_server()