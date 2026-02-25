import pygame
import socket
import threading
import json

from player import Player
from blocks import Platform
from ui import Button
from hud import HUD
from inventory import Inventory
from coin import Coin
from level_data import level, PLATFORM_WIDTH, PLATFORM_HEIGHT

WIN_WIDTH = 800
WIN_HEIGHT = 640

STATE_MENU = "menu"
STATE_GAME = "game"
STATE_PAUSE = "pause"
STATE_INVENTORY = "inventory"
STATE_GAME_OVER = "game_over"

HOST = "127.0.0.1"
PORT = 5555

world_width = len(level[0]) * PLATFORM_WIDTH
world_height = len(level) * PLATFORM_HEIGHT


# ================= NETWORK =================

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

            if msg["type"] == "snapshot":
                snapshot_data = msg["players"]

        except:
            break

threading.Thread(target=receive_data, daemon=True).start()


# ================= WORLD =================

def build_world():
    entities = pygame.sprite.Group()
    platforms = []
    coins = pygame.sprite.Group()

    y = 0
    for row in level:
        x = 0
        for col in row:
            if col == "-":
                pf = Platform(x, y)
                entities.add(pf)
                platforms.append(pf)
            if col == "C":
                coin = Coin(x, y)
                entities.add(coin)
                coins.add(coin)
            x += PLATFORM_WIDTH
        y += PLATFORM_HEIGHT

    return entities, platforms, coins


# ================= MAIN =================

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Multiplayer Platformer")
    clock = pygame.time.Clock()

    sky = pygame.image.load("assets/sky.jpg").convert()
    sky = pygame.transform.scale(sky, (WIN_WIDTH, WIN_HEIGHT))

    state = STATE_MENU

    entities, platforms, coins = build_world()
    hud = HUD()
    inventory = Inventory()

    players = {}

    btn_play = Button(300, 250, 200, 60, "Грати")
    btn_exit = Button(300, 330, 200, 60, "Вийти")

    btn_resume = Button(300, 250, 200, 60, "Продовжити")
    btn_menu = Button(300, 330, 200, 60, "В меню")
    btn_quit = Button(300, 410, 200, 60, "Вийти")

    btn_restart = Button(300, 250, 200, 60, "Почати знову")
    btn_menu_dead = Button(300, 330, 200, 60, "В меню")

    left = right = up = False
    camera_x = 0
    camera_y = 0

    running = True
    while running:
        dt = clock.tick(60) / 1000

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                running = False

            if state == STATE_MENU:
                if btn_play.handle_event(e):
                    state = STATE_GAME
                if btn_exit.handle_event(e):
                    running = False

            elif state == STATE_GAME:
                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_ESCAPE:
                        state = STATE_PAUSE
                    if e.key == pygame.K_i:
                        state = STATE_INVENTORY
                        inventory.open()
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

            elif state == STATE_PAUSE:
                if btn_resume.handle_event(e):
                    state = STATE_GAME
                if btn_menu.handle_event(e):
                    state = STATE_MENU
                if btn_quit.handle_event(e):
                    running = False

            elif state == STATE_INVENTORY:
                inventory.handle_event(e)
                if e.type == pygame.KEYDOWN and e.key == pygame.K_i:
                    inventory.close()

            elif state == STATE_GAME_OVER:
                if btn_restart.handle_event(e):
                    state = STATE_GAME
                if btn_menu_dead.handle_event(e):
                    state = STATE_MENU

        # ===== SEND INPUT =====
        if player_id is not None and state == STATE_GAME:
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

        # ===== APPLY SNAPSHOT =====
        for pid, pdata in snapshot_data.items():
            pid = int(pid)
            if pid not in players:
                players[pid] = Player(0, 0)

            players[pid].rect.x = pdata["x"]
            players[pid].rect.y = pdata["y"]
            players[pid].state = pdata["state"]
            players[pid].facing = pdata["facing"]
            players[pid].animate()

        # ===== CAMERA =====
        if player_id in players:
            hero = players[player_id]
            camera_x = hero.rect.centerx - WIN_WIDTH // 2
            camera_y = hero.rect.centery - WIN_HEIGHT // 2

        # ===== DRAW =====
        screen.blit(sky, (0, 0))

        if state in (STATE_GAME, STATE_PAUSE, STATE_INVENTORY):
            for entity in entities:
                screen.blit(
                    entity.image,
                    (entity.rect.x - camera_x, entity.rect.y - camera_y)
                )

            for pid, player in players.items():
                screen.blit(
                    player.image,
                    (player.rect.x - camera_x, player.rect.y - camera_y)
                )

            hud.draw(screen)

        if state == STATE_MENU:
            btn_play.draw(screen)
            btn_exit.draw(screen)

        if state == STATE_PAUSE:
            overlay = pygame.Surface((WIN_WIDTH, WIN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))
            btn_resume.draw(screen)
            btn_menu.draw(screen)
            btn_quit.draw(screen)

        if state == STATE_INVENTORY:
            inventory.draw(screen)

        if state == STATE_GAME_OVER:
            overlay = pygame.Surface((WIN_WIDTH, WIN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))
            screen.blit(overlay, (0, 0))
            btn_restart.draw(screen)
            btn_menu_dead.draw(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()