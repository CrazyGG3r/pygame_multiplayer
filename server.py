import socket
import threading
import logging
import json
# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

# Server setup
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = '26.1.98.217'
port = 5555
server.bind((ip, 5555))
server.listen()
logging.info("Server listening at: {}:{}".format(ip,port))

clients = []
positions = {}
global player_count 
player_count = 0


def broadcast_positions():
    logging.info("Broadcasting positions")
    # Ensure that positions is a dictionary of dictionaries
    aggregated_data = json.dumps(positions)  # Convert the aggregated data to JSON
    for client in clients:
        try:
            client.sendall(aggregated_data.encode())  # Send the JSON string
        except Exception as e:
            logging.error("Error in broadcasting to a client: {}".format(e), exc_info=True)
            client.close()
            clients.remove(client)

def client_thread(conn, addr, player_number):
    global positions
    logging.info(f"Player {player_number} connected from {addr}")

    while True:
        try:
            data = conn.recv(65536).decode()
            logging.info(f"Player {player_number} moved")
            buffer = ""
            if data:
                buffer += data
                while '\n' in buffer:
                    message, _, buffer = buffer.partition('\n')
                    player_data = json.loads(message)
                    positions[player_number] = player_data
                    broadcast_positions()
                    
        except json.JSONDecodeError as e:
            logging.error("JSON Decode error for player {}: {}".format(player_number, e))
            break
        except Exception as e:
            logging.error("Error with player {}: {}".format(player_number, e), exc_info=True)
            break
        except Exception as e:
            logging.error("Error with player {}: {}".format(player_number, e), exc_info=True)
            conn.close()
            if player_number in positions:
                del positions[player_number]
            break

while True:
    conn, addr = server.accept()
    player_count += 1
    clients.append(conn)
    threading.Thread(target=client_thread, args=(conn, addr, player_count)).start()
