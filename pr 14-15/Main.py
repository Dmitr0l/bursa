import pygame
from player import Player
from blocks import Platform
from ui import Button
from hud import HUD
from inventory import Inventory
from coin import Coin 

WIN_WIDTH = 800
WIN_HEIGHT = 640

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32

STATE_MENU = "menu"
STATE_GAME = "game"
STATE_PAUSE = "pause"
STATE_INVENTORY = "inventory"
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
    pygame.display.set_caption("Практична 14-15")
    clock = pygame.time.Clock()

    sky = pygame.image.load("assets/sky.jpg").convert()
    sky = pygame.transform.scale(sky, (WIN_WIDTH, WIN_HEIGHT))

    state = STATE_MENU

    hero, entities, platforms, coins = build_world()
    hud = HUD()
    inventory = Inventory()

    # MENU
    btn_play = Button(300, 250, 200, 60, "Грати")
    btn_exit = Button(300, 330, 200, 60, "Вийти")

    # PAUSE
    btn_resume = Button(300, 250, 200, 60, "Продовжити")
    btn_menu = Button(300, 330, 200, 60, "В меню")
    btn_quit = Button(300, 410, 200, 60, "Вийти")

    # GAME OVER
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

            # ---------------- MENU ----------------
            if state == STATE_MENU:
                if btn_play.handle_event(e):
                    state = STATE_GAME
                    hud.reset()
                    hero, entities, platforms, coins = build_world()
                    inventory.clear()
                    left = right = up = False

                if btn_exit.handle_event(e):
                    running = False

            # ---------------- GAME ----------------
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

            # ---------------- PAUSE ----------------
            elif state == STATE_PAUSE:
                if btn_resume.handle_event(e):
                    state = STATE_GAME
                if btn_menu.handle_event(e):
                    state = STATE_MENU
                if btn_quit.handle_event(e):
                    running = False

            # ---------------- INVENTORY ----------------
            elif state == STATE_INVENTORY:
                inventory.handle_event(e)

                if e.type == pygame.KEYDOWN:
                    if e.key == pygame.K_i:
                        inventory.close()

            # ---------------- GAME OVER ----------------
            elif state == STATE_GAME_OVER:
                if btn_restart.handle_event(e):
                    state = STATE_GAME
                    hud.reset()
                    hero, entities, platforms, coins = build_world()
                    inventory.clear()
                    left = right = up = False

                if btn_menu_dead.handle_event(e):
                    state = STATE_MENU

        # -------- UPDATE --------
        if state == STATE_GAME:

            hero.update(left, right, up, platforms)
            hud.update(dt)

            # 💀 смерть якщо впав
            if hero.rect.top > world_height:
                state = STATE_GAME_OVER
                left = right = up = False

            # 🪙 збір монет
            collected = pygame.sprite.spritecollide(hero, coins, True)
            for coin in collected:
                hud.score += 1
                inventory.add_item("Coin", 1)
                entities.remove(coin)

            # 🎥 камера
            camera_x = hero.rect.centerx - WIN_WIDTH // 2
            camera_y = hero.rect.centery - WIN_HEIGHT // 2

        if state == STATE_INVENTORY:
            inventory.update(dt)
            if inventory.is_closed():
                state = STATE_GAME

        # -------- DRAW --------
        screen.blit(sky, (0, 0))

        if state in (STATE_GAME, STATE_PAUSE, STATE_INVENTORY):
            for entity in entities:
                screen.blit(
                    entity.image,
                    (entity.rect.x - camera_x, entity.rect.y - camera_y)
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