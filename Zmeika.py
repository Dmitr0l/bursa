import pygame
import time

pygame.init()

white = (205, 205, 205)
black = (0, 0, 0)
red = (250, 0, 0)
green = (0, 250, 0)
blue = (0, 0, 250)

dis_width = 600
dis_height = 400
dis = pygame.display.set_mode((dis_width, dis_height))
pygame.display.set_caption("Удав")


def game_loop():
    game_over = False
    x1 = dis_width / 2
    y1 = dis_height / 2

    x1_change = 0
    y1_change = 0

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:
                    x1_change = -10
                    y1_change = 0
                elif event.key == pygame.K_d:
                    x1_change = 10
                    y1_change = 0

                elif event.key == pygame.K_s:
                    x1_change = 0
                    y1_change = 10

                elif event.key == pygame.K_w:
                    x1_change = 0
                    y1_change = -10

        x1 += x1_change
        y1 += y1_change

        dis.fill(white)
        pygame.draw.rect(dis, black, [x1, y1, 10, 10])
        pygame.display.update()

        time.sleep(0.1)

    pygame.quit()
    quit()


game_loop()