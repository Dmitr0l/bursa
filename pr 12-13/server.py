import socket
import threading
import json
import pygame
from player import Player
from level_data import level, PLATFORM_WIDTH, PLATFORM_HEIGHT

HOST = "127.0.0.1"
PORT = 5555
TICK = 30

pygame.init()

players = {}
inputs = {}
clients = {}

def build_world():
    platforms = []
    y = 0
    for row in level:
        x = 0
        for col in row:
            if col == "-":
                platforms.append(pygame.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT))
            x += PLATFORM_WIDTH
        y += PLATFORM_HEIGHT
    return platforms

platforms = build_world()

def client_thread(conn, addr, pid):
    print("Connected:", addr)

    players[pid] = Player(200 + pid * 100, 200, server_mode=True)
    inputs[pid] = {"left": False, "right": False, "up": False}

    conn.send(json.dumps({"type": "id", "id": pid}).encode())

    while True:
        try:
            data = conn.recv(2048).decode()
            msg = json.loads(data)
            if msg["type"] == "input":
                inputs[pid] = msg["data"]
        except:
            break

def game_loop():
    clock = pygame.time.Clock()
    while True:
        clock.tick(TICK)

        for pid, player in players.items():
            inp = inputs[pid]
            player.update(inp["left"], inp["right"], inp["up"], platforms)

        snapshot = {
            "type": "snapshot",
            "players": {
                pid: {
                    "x": p.rect.x,
                    "y": p.rect.y,
                    "state": p.state,
                    "facing": p.facing
                }
                for pid, p in players.items()
            }
        }

        for conn in clients.values():
            try:
                conn.send(json.dumps(snapshot).encode())
            except:
                pass

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    print("Server started")

    threading.Thread(target=game_loop, daemon=True).start()

    pid = 0
    while True:
        conn, addr = s.accept()
        clients[pid] = conn
        threading.Thread(target=client_thread, args=(conn, addr, pid), daemon=True).start()
        pid += 1

if __name__ == "__main__":
    main()