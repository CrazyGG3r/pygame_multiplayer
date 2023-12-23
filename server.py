import socket
import threading
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# Server setup
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(('127.0.0.1', 5555))
server.listen()

clients = []
positions = {}
player_count = 0

def broadcast_positions():
    """Broadcast the positions to all clients."""
    for client in clients:
        try:
            client.sendall(str(positions).encode())
        except:
            logging.error("Error in broadcasting to a client", exc_info=True)
            client.close()
            clients.remove(client)

def client_thread(conn, addr, player_number):
    global positions
    logging.info(f"Player {player_number} connected from {addr}")
    while True:
        try:
            data = conn.recv(1024).decode()
            if data:
                positions[player_number] = data
                broadcast_positions()
        except:
            logging.error("Error with a client connection", exc_info=True)
            conn.close()
            if player_number in positions:
                del positions[player_number]
            break

while True:
    conn, addr = server.accept()
    player_count += 1
    clients.append(conn)
    threading.Thread(target=client_thread, args=(conn, addr, player_count)).start()
