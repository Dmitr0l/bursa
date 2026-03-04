import pygame
from player import Player
from blocks import Platform
from ui import Button
from hud import HUD
from coin import Coin
from network import Network

WIN_WIDTH = 800
WIN_HEIGHT = 640

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32

STATE_MENU = "menu"
STATE_GAME = "game"
STATE_PAUSE = "pause"
STATE_GAME_OVER = "game_over"


level = [
    "                                                                          ",
    "                                                                          ",
    "                                                                          ",
    "                    C                                      C              ",
    "                  ----                                   -----            ",
    "                                       -----                              ",
    "                                                                          ",
    "                                ----           -----                      ",
    "       -----                                                              ",
    "                                                            -----         ",
    "                C                                                         ",
    "              -----      -----                         C                  ",
    "                                                     -----                ",
    "                                        C                                 ",
    "                                      -----                               ",
    "             C                                                            ",
    "      ---------------                                                     ",
    "                         -                                                ",
    "                         -          ----                         C        ",
    "--------------------------------------------------------------------------"
]

world_width = len(level[0]) * PLATFORM_WIDTH
world_height = len(level) * PLATFORM_HEIGHT


def build_world():
    entities = pygame.sprite.Group()
    platforms = []
    coins = pygame.sprite.Group()

    hero = Player(200, 200)
    entities.add(hero)

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

    return hero, entities, platforms, coins


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Praktichka 11-12")
    clock = pygame.time.Clock()

    net = Network()
    player_id = net.player_id

    sky = pygame.image.load("assets/sky.jpg").convert()
    sky = pygame.transform.scale(sky, (WIN_WIDTH, WIN_HEIGHT))

    state = STATE_MENU

    hero, entities, platforms, coins = build_world()
    hud = HUD()

    # словник інших гравців
    other_players = {}

    # MENU
    btn_play = Button(300, 250, 200, 60, "Грати")
    btn_exit = Button(300, 330, 200, 60, "Вийти")

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
                    hud.reset()
                    hero, entities, platforms, coins = build_world()
                    other_players.clear()
                    left = right = up = False

                if btn_exit.handle_event(e):
                    running = False

            elif state == STATE_GAME:

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

        # ================= UPDATE =================
        if state == STATE_GAME:

            hero.update(left, right, up, platforms)
            hud.update(dt)

            if hero.rect.top > world_height:
                state = STATE_GAME_OVER

            collected = pygame.sprite.spritecollide(hero, coins, True)
            for coin in collected:
                hud.score += 1
                entities.remove(coin)

            # ---- ВІДПРАВЛЯЄМО ПОВНИЙ СТАН ----
            data = {
                "x": hero.rect.x,
                "y": hero.rect.y,
                "facing": hero.facing,
                "state": hero.state
            }

            players = net.send(data)

            if players:

                # --- створення нових гравців ---
                for pid, pdata in players.items():

                    if pid == player_id:
                        continue

                    if pid not in other_players:
                        new_player = Player(pdata["x"], pdata["y"])
                        other_players[pid] = new_player
                        entities.add(new_player)

                # --- видалення відключених ---
                for pid in list(other_players.keys()):
                    if pid not in players:
                        entities.remove(other_players[pid])
                        del other_players[pid]

                # --- оновлення ---
                for pid, pdata in players.items():

                    if pid == player_id:
                        continue

                    p = other_players[pid]

                    p.rect.x = pdata["x"]
                    p.rect.y = pdata["y"]

                    if p.state != pdata["state"]:
                        p.state = pdata["state"]
                        p.frame_index = 0
                        p.animation_timer = 0

                    p.facing = pdata["facing"]

                    # плавна анімація
                    p.animation_timer += 0.15
                    if p.animation_timer >= 1:
                        p.animation_timer = 0
                        p.frame_index = (p.frame_index + 1) % 4

                    p.animate()

            camera_x = hero.rect.centerx - WIN_WIDTH // 2
            camera_y = hero.rect.centery - WIN_HEIGHT // 2

        # ================= DRAW =================
        screen.blit(sky, (0, 0))

        if state == STATE_GAME:
            for entity in entities:
                screen.blit(
                    entity.image,
                    (entity.rect.x - camera_x,
                     entity.rect.y - camera_y)
                )
            hud.draw(screen)

        if state == STATE_MENU:
            btn_play.draw(screen)
            btn_exit.draw(screen)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()