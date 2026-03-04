import pygame
import random
from player import Player
from blocks import Platform

WIN_WIDTH = 800
WIN_HEIGHT = 600

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32

BG_COLOR = (0, 0, 0)

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pygame.display.set_caption("Miku 🐧")
    clock = pygame.time.Clock()

    entities = pygame.sprite.Group()
    platforms = []

    hero = Player(200, 450)
    entities.add(hero)

    world_shift = 5
    last_platform_x = WIN_WIDTH

    # Початкова підлога
    for i in range(0, WIN_WIDTH, PLATFORM_WIDTH):
        ground = Platform(i, 500)
        entities.add(ground)
        platforms.append(ground)

    running = True
    left = right = up = False

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

        # --- Рух героя + камера ---
        if right:
            if hero.rect.x < 200:
                hero.update(left, right, up, platforms)
            else:
                # Біг на місці для анімації
                hero.update(True, False, up, platforms, force_run=True)
                for entity in entities:
                    if entity != hero:
                        entity.rect.x -= world_shift
                last_platform_x -= world_shift

        elif left:
            if hero.rect.x > 200:
                hero.update(left, right, up, platforms)
            else:
                hero.update(False, True, up, platforms, force_run=True)
                for entity in entities:
                    if entity != hero:
                        entity.rect.x += world_shift
                last_platform_x += world_shift
        else:
            hero.update(False, False, up, platforms)

        # Генерація платформ
        if last_platform_x < WIN_WIDTH:
            width = random.randint(2, 6)
            height = random.randint(250, 500)

            for i in range(width):
                pf = Platform(WIN_WIDTH + i * PLATFORM_WIDTH, height)
                entities.add(pf)
                platforms.append(pf)

            last_platform_x = WIN_WIDTH + width * PLATFORM_WIDTH

        # Видалення платформ
        for pf in platforms[:]:
            if pf.rect.right < 0:
                platforms.remove(pf)
                entities.remove(pf)

        screen.fill(BG_COLOR)
        entities.draw(screen)
        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
