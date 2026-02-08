import pygame
import random

WIDTH, HEIGHT = 800, 600
FPS = 60

WORLD_WIDTH = 3000
WORLD_HEIGHT = 3000

PLAYER_SPEED = 250
PLAYER_SIZE = 199

BG_COLOR = (30, 30, 30)


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Практична 7–8")
    clock = pygame.time.Clock()

    mario_img = pygame.image.load("mario.png").convert_alpha()
    mario_img = pygame.transform.scale(mario_img, (PLAYER_SIZE, PLAYER_SIZE))

    walk_right = [mario_img, mario_img, mario_img, mario_img]
    current_frame = 0.0

    player_world_x = WORLD_WIDTH // 2
    player_world_y = WORLD_HEIGHT // 2

    trees = []
    for _ in range(50):
        x = random.randint(0, WORLD_WIDTH)
        y = random.randint(0, WORLD_HEIGHT)
        trees.append((x, y))

    running = True
    while running:
        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        is_moving = False
        direction = "right"

        # --- РУХ ГРАВЦЯ ---
        if keys[pygame.K_a]:
            player_world_x -= PLAYER_SPEED * dt
            is_moving = True
            direction = "left"

        if keys[pygame.K_d]:
            player_world_x += PLAYER_SPEED * dt
            is_moving = True
            direction = "right"

        if keys[pygame.K_w]:
            player_world_y -= PLAYER_SPEED * dt
            is_moving = True

        if keys[pygame.K_s]:
            player_world_y += PLAYER_SPEED * dt
            is_moving = True

        player_world_x = max(0, min(WORLD_WIDTH - PLAYER_SIZE, player_world_x))
        player_world_y = max(0, min(WORLD_HEIGHT - PLAYER_SIZE, player_world_y))

        offset_x = player_world_x - WIDTH // 2
        offset_y = player_world_y - HEIGHT // 2

        offset_x = max(0, min(WORLD_WIDTH - WIDTH, offset_x))
        offset_y = max(0, min(WORLD_HEIGHT - HEIGHT, offset_y))

        if is_moving:
            current_frame += 0.1
            if current_frame >= len(walk_right):
                current_frame = 0
        else:
            current_frame = 0

        frame = walk_right[int(current_frame)]

        if direction == "left":
            frame = pygame.transform.flip(frame, True, False)

        screen.fill(BG_COLOR)

        for tree_x, tree_y in trees:
            pygame.draw.circle(
                screen,
                (0, 150, 0),
                (tree_x - offset_x, tree_y - offset_y),
                20
            )

        screen.blit(
            frame,
            (WIDTH // 2 - PLAYER_SIZE // 2, HEIGHT // 2 - PLAYER_SIZE // 2)
        )

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
