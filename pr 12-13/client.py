import pygame
import socket
import threading
import json

from player import Player
from blocks import Platform
from Main import level, PLATFORM_WIDTH, PLATFORM_HEIGHT, WIN_WIDTH, WIN_HEIGHT

HOST = "127.0.0.1"
PORT = 5555

pygame.init()

# ✅ Спочатку створюємо вікно!
screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Multiplayer Client")
clock = pygame.time.Clock()

# ---------------- NETWORK ----------------

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((HOST, PORT))

player_id = None
snapshot_data = {}

def receive_data():
    global snapshot_data, player_id
    while True:
        try:
            data = client.recv(4096).decode()
            if not data:
                break

            msg = json.loads(data)

            if msg["type"] == "id":
                player_id = msg["id"]
                print("My ID:", player_id)

            if msg["type"] == "snapshot":
                snapshot_data = msg["players"]

        except:
            break

threading.Thread(target=receive_data, daemon=True).start()

# ---------------- WORLD ----------------

def build_platforms():
    platforms = []
    y = 0
    for row in level:
        x = 0
        for col in row:
            if col == "-":
                platforms.append(Platform(x, y))
            x += PLATFORM_WIDTH
        y += PLATFORM_HEIGHT
    return platforms

# ✅ Тепер можна створювати платформи
platforms = build_platforms()

# ---------------- GAME LOOP ----------------

players = {}
left = right = up = False
running = True

while running:
    clock.tick(60)

    for e in pygame.event.get():
        if e.type == pygame.QUIT:
            running = False

        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_a:
                left = True
            if e.key == pygame.K_d:
                right = True
            if e.key == pygame.K_w:
                up = True

        if e.type == pygame.KEYUP:
            if e.key == pygame.K_a:
                left = False
            if e.key == pygame.K_d:
                right = False
            if e.key == pygame.K_w:
                up = False

    # ---- SEND INPUT ----
    if player_id is not None:
        msg = {
            "type": "input",
            "data": {
                "left": left,
                "right": right,
                "up": up
            }
        }
        try:
            client.send(json.dumps(msg).encode())
        except:
            pass

    # ---- APPLY SNAPSHOT ----
    for pid, pdata in snapshot_data.items():
        pid = int(pid)

        if pid not in players:
            players[pid] = Player(0, 0)

        players[pid].rect.x = pdata["x"]
        players[pid].rect.y = pdata["y"]
        players[pid].state = pdata["state"]
        players[pid].facing = pdata["facing"]
        players[pid].animate()

    # ---- DRAW ----
    screen.fill((30, 30, 50))

    for platform in platforms:
        screen.blit(platform.image, platform.rect)

    for pid, player in players.items():
        screen.blit(player.image, player.rect)

    pygame.display.flip()

pygame.quit()