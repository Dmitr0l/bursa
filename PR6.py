import pygame

WIDTH, HEIGHT = 800, 600
FPS = 60

BG_COLOR = (30, 30, 40)
PLAYER_COLOR = (80, 200, 120)

PLAYER_SIZE = 50
PLAYER_SPEED = 250 

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Практичка")
    clock = pygame.time.Clock()

    player = pygame.Rect(100, 100, PLAYER_SIZE, PLAYER_SIZE)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            player.x -= int(PLAYER_SPEED * dt)
        if keys[pygame.K_RIGHT]:
            player.x += int(PLAYER_SPEED * dt)
        if keys[pygame.K_UP]:
            player.y -= int(PLAYER_SPEED * dt)
        if keys[pygame.K_DOWN]:
            player.y += int(PLAYER_SPEED * dt)

        player.x = max(0, min(WIDTH - player.width, player.x))
        player.y = max(0, min(HEIGHT - player.height, player.y))

        screen.fill(BG_COLOR)
        pygame.draw.rect(screen, PLAYER_COLOR, player)
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()