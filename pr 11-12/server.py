import socket
import threading
import pickle

HOST = "127.0.0.1"
PORT = 5555

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

print("Алах воскрес")

players = {}
current_id = 0


def handle_client(conn, player_id):
    global players

    conn.send(pickle.dumps(player_id))

    players[player_id] = {
        "x": 200,
        "y": 200,
        "facing": "right",
        "state": "idle"
    }

    while True:
        try:
            data = pickle.loads(conn.recv(4096))
            players[player_id] = data

            conn.send(pickle.dumps(players))
        except:
            break

    print("Disconnected:", player_id)
    del players[player_id]
    conn.close()


while True:
    conn, addr = server.accept()
    print("Connected:", addr)

    threading.Thread(
        target=handle_client,
        args=(conn, current_id)
    ).start()

    current_id += 1