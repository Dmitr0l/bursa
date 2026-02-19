import pygame
from common.constants import PLATFORM_WIDTH, PLATFORM_HEIGHT

level_map = [
    "                                                                          ",
    "                  ----                                   -----            ",
    "                                       -----                              ",
    "                                ----           -----                      ",
    "       -----                                                              ",
    "--------------------------------------------------------------------------"
]

def get_colliders():
    platforms = []
    for y, row in enumerate(level_map):
        for x, col in enumerate(row):
            if col == "-":
                platforms.append(pygame.Rect(x * PLATFORM_WIDTH, y * PLATFORM_HEIGHT, PLATFORM_WIDTH, PLATFORM_HEIGHT))
    return platforms

SPAWN_POINTS = [(100, 200), (600, 200), (400, 100)]