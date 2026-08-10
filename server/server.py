import socket
import ssl
import threading
import time
from database import init_db, register_user, authenticate_user, log_message, log_connection, get_admin_logs

HOST = '127.0.0.1'
PORT = 12345
CLIENT_TIMEOUT = 120
SPAM_LIMIT_SECONDS = 0.5

clients = {}

def broadcast(message, sender_user=None):
    for user, sock in list(clients.items()):
        if user != sender_user:
            try:
                sock.sendall((message + "\n").encode('utf-8'))
            except:
                sock.close()
                del clients[user]

def handle_client(client_socket, client_address):
    client_ip = client_address[0]
    current_user = None
    last_msg_time = 0
    
    client_socket.settimeout(CLIENT_TIMEOUT)

    try:
        client_socket.sendall(b"AUTH_REQUIRED\n")
        
        while not current_user:
            try:
                data = client_socket.recv(1024).decode('utf-8').strip()
            except socket.timeout:
                client_socket.sendall(b"TIMEOUT: Authentication timed out.\n")
                return

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
                    
                    log_connection(current_user, client_ip, "LOGIN")
                    broadcast(f"[SYSTEM]: {current_user} joined the chat.", current_user)
                else:
                    client_socket.sendall(b"LOGIN_FAILED\n")
            else:
                client_socket.sendall(b"INVALID_COMMAND\n")

        while True:
            try:
                msg = client_socket.recv(1024).decode('utf-8')
                if not msg:
                    break
                
                msg_str = msg.strip()

                current_time = time.time()
                if current_time - last_msg_time < SPAM_LIMIT_SECONDS:
                    client_socket.sendall(b"[SYSTEM WARNING]: You are sending messages too fast! (Anti-Spam)\n")
                    continue
                last_msg_time = current_time

                if msg_str.upper() == "LIST":
                    active_users = ", ".join(clients.keys())
                    client_socket.sendall(f"[SYSTEM]: Online Users: {active_users}\n".encode('utf-8'))
                    continue

                if msg_str.upper() == "ADMIN_LOGS":
                    if current_user == "admin":
                        logs = get_admin_logs()
                        log_res = "\n--- ADMIN LOGS ---\n" + "\n".join([str(l) for l in logs]) + "\n"
                        client_socket.sendall(log_res.encode('utf-8'))
                    else:
                        client_socket.sendall(b"[SYSTEM]: Access Denied. Admin only.\n")
                    continue

                log_message(current_user, msg_str)
                broadcast(f"[{current_user}]: {msg_str}", current_user)

            except socket.timeout:
                print(f"[-] Client {current_user} timed out due to inactivity.")
                client_socket.sendall(b"[SYSTEM]: Disconnected due to inactivity (Timeout).\n")
                break

    except Exception as e:
        print(f"Error: {e}")
    finally:
        if current_user and current_user in clients:
            del clients[current_user]
            log_connection(current_user, client_ip, "LOGOUT")
            broadcast(f"[SYSTEM]: {current_user} left the chat.")
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