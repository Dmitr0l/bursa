import pygame
from player import Player
from blocks import Platform
from ui import Button
from hud import HUD
from inventory import Inventory

WIN_WIDTH = 800
WIN_HEIGHT = 640

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32

STATE_MENU = "menu"
STATE_GAME = "game"
STATE_PAUSE = "pause"
STATE_INVENTORY = "inventory"


level = [
    "                                                                          ",
    "                                                                          ",
    "                                                                          ",
    "                                                                          ",
    "                  ----                                   -----            ",
    "                                       -----                              ",
    "                                                                          ",
    "                                ----           -----                      ",
    "       -----                                                              ",
    "                                                            -----         ",
    "                                                                          ",
    "              -----      -----                                            ",
    "                                                     -----                ",
    "                                                                          ",
    "                                      -----                               ",
    "                                                                          ",
    "      ---------------                                                     ",
    "                         -                                                ",
    "                         -          ----                                  ",
    "--------------------------------------------------------------------------"
]

world_width = len(level[0]) * PLATFORM_WIDTH
world_height = len(level) * PLATFORM_HEIGHT


def build_world():
    entities = pygame.sprite.Group()
    platforms = []

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
            x += PLATFORM_WIDTH
        y += PLATFORM_HEIGHT

    return hero, entities, platforms


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Практична 14-15")
    clock = pygame.time.Clock()

    sky = pygame.image.load("assets/sky.jpg").convert()
    sky = pygame.transform.scale(sky, (WIN_WIDTH, WIN_HEIGHT))

    state = STATE_MENU

    hero, entities, platforms = build_world()

    hud = HUD()
    inventory = Inventory()

    btn_play = Button(300, 250, 200, 60, "Грати")
    btn_exit = Button(300, 330, 200, 60, "Вийти")

    btn_resume = Button(300, 250, 200, 60, "Продовжити")
    btn_menu = Button(300, 330, 200, 60, "В меню")
    btn_quit = Button(300, 410, 200, 60, "Вийти")

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
                    hero, entities, platforms = build_world()

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

                    if e.key == pygame.K_h:
                        hud.hp = max(0, hud.hp - 10)

                    if e.key == pygame.K_j:
                        hud.hp = min(hud.hp_max, hud.hp + 10)

                    if e.key == pygame.K_SPACE:
                        hud.score += 1

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

        # -------- UPDATE --------
        if state == STATE_GAME:
            hero.update(left, right, up, platforms)
            hud.update(dt)

            camera_x = hero.rect.x - WIN_WIDTH // 2
            camera_y = hero.rect.y - WIN_HEIGHT // 2

            if camera_y < 0:
                camera_y = 0
            if camera_y > world_height - WIN_HEIGHT:
                camera_y = world_height - WIN_HEIGHT

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

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()