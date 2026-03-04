import pygame

MOVE_SPEED = 7
JUMP_POWER = 10
GRAVITY = 0.35
RUN_ANIMATION_SPEED = 0.08
IDLE_BLINK_SPEED = 0.12
IDLE_WAIT_MS = 3000


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, server_mode=False):
        super().__init__()

        self.server_mode = server_mode

        if not self.server_mode:
            self.load_animations()
            self.image = self.idle_frames[0]
        else:
            self.image = pygame.Surface((40, 60))
            self.image.fill((255, 0, 0))

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.xvel = 0
        self.yvel = 0
        self.onGround = False

        self.state = "idle"
        self.frame_index = 0
        self.animation_timer = 0
        self.facing = "right"
        self.last_activity_time = pygame.time.get_ticks()
        self.is_blinking = False

    def load_animations(self):
        scale = 0.45

        def load_and_scale(path):
            img = pygame.image.load(path).convert_alpha()
            w = int(img.get_width() * scale)
            h = int(img.get_height() * scale)
            return pygame.transform.scale(img, (w, h))

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

        self.jump_frames = [
            load_and_scale("assets/jump1.png"),
            load_and_scale("assets/jump2.png"),
            load_and_scale("assets/jump3.png"),
            load_and_scale("assets/jump4.png"),
            load_and_scale("assets/jump5.png"),
        ]

    def update(self, left, right, up, platforms):
        if up and self.onGround:
            self.yvel = -JUMP_POWER

        if left:
            self.xvel = -MOVE_SPEED
            self.facing = "left"
        elif right:
            self.xvel = MOVE_SPEED
            self.facing = "right"
        else:
            self.xvel = 0

        self.yvel += GRAVITY
        self.onGround = False

        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)

        if not self.onGround:
            self.state = "jump"
        elif self.xvel != 0:
            self.state = "run"
        else:
            self.state = "idle"

        if not self.server_mode:
            self.animate()

    def animate(self):
        if self.state == "idle":
            frame = self.idle_frames[0]
        elif self.state == "run":
            frame = self.run_frames[self.frame_index % len(self.run_frames)]
            self.frame_index += 1
        else:
            frame = self.jump_frames[0]

        if self.facing == "left":
            frame = pygame.transform.flip(frame, True, False)

        self.image = frame

    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if self.rect.colliderect(p):
                if xvel > 0:
                    self.rect.right = p.left
                if xvel < 0:
                    self.rect.left = p.right
                if yvel > 0:
                    self.rect.bottom = p.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.bottom
                    self.yvel = 0