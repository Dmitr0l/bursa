import pygame

PLATFORM_WIDTH = 32
PLATFORM_HEIGHT = 32

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.image = pygame.image.load("assets/block.png").convert_alpha()
        self.image = pygame.transform.scale(
            self.image, (PLATFORM_WIDTH, PLATFORM_HEIGHT)
        )

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)