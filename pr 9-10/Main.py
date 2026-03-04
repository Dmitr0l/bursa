import pygame
from player import Player
from blocks import Platform

WIN_WIDTH = 800
WIN_HEIGHT = 640

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32

BG_COLOR = (0, 0, 0)

level = [
    "-------------------------",
    "-                       -",
    "-                       -",
    "-                       -",
    "-            --         -",
    "-                       -",
    "-                       -",
    "-                 --    -",
    "-    ---                -",
    "-                       -",
    "-                       -",
    "-            ---        -",
    "-                       -",
    "--                      -",
    "-                   --- -",
    "-                       -",
    "-   -----------         -",
    "-                -      -",
    "-                   --  -",
    "-------------------------"
]

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Miku 🐧")
    clock = pygame.time.Clock()

    entities = pygame.sprite.Group()
    platforms = []

    hero = Player(55, 55)
    entities.add(hero)

    # створення рівня
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

    left = right = up = False

    while True:
        clock.tick(60)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit()
                return

            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_LEFT:
                    left = True
                if e.key == pygame.K_RIGHT:
                    right = True
                if e.key == pygame.K_UP:
                    up = True

            if e.type == pygame.KEYUP:
                if e.key == pygame.K_LEFT:
                    left = False
                if e.key == pygame.K_RIGHT:
                    right = False
                if e.key == pygame.K_UP:
                    up = False

        screen.fill(BG_COLOR)

        hero.update(left, right, up, platforms)

        entities.draw(screen)
        pygame.display.update()


if __name__ == "__main__":
    main()
