import pygame

PLAYER_SPEED = 250
PLAYER_SIZE = 50


def load_and_scale(path):
    img = pygame.image.load(path).convert_alpha()
    return pygame.transform.scale(img, (PLAYER_SIZE, PLAYER_SIZE))


class Player:
    def __init__(self, x, y):
        self.world_x = x
        self.world_y = y

        self.idle_frames = [
            load_and_scale("assets/idle1.png"),
            load_and_scale("assets/idle2.png"),
            load_and_scale("assets/idle3.png"),
            load_and_scale("assets/idle4.png"),
        ]

        self.run_frames = [
            load_and_scale("assets/run1.png"),
            load_and_scale("assets/run2.png"),
            load_and_scale("assets/run3.png"),
            load_and_scale("assets/run4.png"),
            load_and_scale("assets/run5.png"),
        ]

        self.current_frame = 0
        self.direction = "right"
        self.is_moving = False

    def update(self, dt, keys, world_w, world_h):
        self.is_moving = False

        if keys[pygame.K_a]:
            self.world_x -= PLAYER_SPEED * dt
            self.direction = "left"
            self.is_moving = True

        if keys[pygame.K_d]:
            self.world_x += PLAYER_SPEED * dt
            self.direction = "right"
            self.is_moving = True

        if keys[pygame.K_w]:
            self.world_y -= PLAYER_SPEED * dt
            self.is_moving = True

        if keys[pygame.K_s]:
            self.world_y += PLAYER_SPEED * dt
            self.is_moving = True

        self.world_x = max(0, min(world_w - PLAYER_SIZE, self.world_x))
        self.world_y = max(0, min(world_h - PLAYER_SIZE, self.world_y))

        if self.is_moving:
            self.current_frame += 0.2
            if self.current_frame >= len(self.run_frames):
                self.current_frame = 0
        else:
            self.current_frame += 0.1
            if self.current_frame >= len(self.idle_frames):
                self.current_frame = 0

    def draw(self, screen, screen_w, screen_h):
        if self.is_moving:
            frame = self.run_frames[int(self.current_frame)]
        else:
            frame = self.idle_frames[int(self.current_frame)]

        if self.direction == "left":
            frame = pygame.transform.flip(frame, True, False)

        screen.blit(
            frame,
            (
                screen_w // 2 - PLAYER_SIZE // 2,
                screen_h // 2 - PLAYER_SIZE // 2
            )
        )