import pygame
import random
from player import Player

WIDTH, HEIGHT = 800, 600
FPS = 60

WORLD_WIDTH = 3000
WORLD_HEIGHT = 3000

BG_COLOR = (30, 30, 30)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Практична 7–8")
    clock = pygame.time.Clock()

    player = Player(WORLD_WIDTH // 2, WORLD_HEIGHT // 2)

    tree_img = pygame.image.load("assets/tree.png").convert_alpha()
    tree_img = pygame.transform.scale(tree_img, (120, 120))

    trees = []
    for _ in range(50):
        x = random.randint(0, WORLD_WIDTH - 120)
        y = random.randint(0, WORLD_HEIGHT - 120)
        trees.append((x, y))

    running = True
    while running:
        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        player.update(dt, keys, WORLD_WIDTH, WORLD_HEIGHT)

        offset_x = player.world_x - WIDTH // 2
        offset_y = player.world_y - HEIGHT // 2

        offset_x = max(0, min(WORLD_WIDTH - WIDTH, offset_x))
        offset_y = max(0, min(WORLD_HEIGHT - HEIGHT, offset_y))

        screen.fill(BG_COLOR)

        for tree_x, tree_y in trees:
            screen.blit(
                tree_img,
                (tree_x - offset_x, tree_y - offset_y)
            )

        player.draw(screen, WIDTH, HEIGHT)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()