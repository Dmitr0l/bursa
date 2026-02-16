import pygame

MOVE_SPEED = 7
JUMP_POWER = 10
GRAVITY = 0.35
ANIMATION_SPEED = 0.05


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        self.load_animations()

        self.image = self.idle_frames[0]
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.xvel = 0
        self.yvel = 0
        self.onGround = False

        self.state = "idle"
        self.frame_index = 0
        self.animation_timer = 0
        self.facing = "right"

    def load_animations(self):
        scale = 0.3

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

        previous_state = self.state

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

        if not self.onGround:
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

        if self.state != previous_state:
            self.frame_index = 0
            self.animation_timer = 0

        if abs(self.xvel) < 0.1:
            self.xvel = 0

        self.animate()

    def animate(self):
        if self.state == "idle":
            frames = self.idle_frames
            self.animation_timer += ANIMATION_SPEED

            if self.animation_timer >= 1:
                self.animation_timer = 0
                self.frame_index = (self.frame_index + 1) % len(frames)

            frame = frames[self.frame_index]

        elif self.state == "run":
            frames = self.run_frames
            self.animation_timer += ANIMATION_SPEED

            if self.animation_timer >= 1:
                self.animation_timer = 0
                self.frame_index = (self.frame_index + 1) % len(frames)

            frame = frames[self.frame_index]

        else:
            if self.yvel < -2:
                frame = self.jump_frames[0] 
            elif -2 <= self.yvel <= 2:
                frame = self.jump_frames[2]
            else:
                frame = self.jump_frames[-1]

        if self.facing == "left":
            frame = pygame.transform.flip(frame, True, False)

        self.image = frame



    def collide(self, xvel, yvel, platforms):
        for p in platforms:
            if pygame.sprite.collide_rect(self, p):

                if xvel > 0:
                    self.rect.right = p.rect.left

                if xvel < 0:
                    self.rect.left = p.rect.right

                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0

                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0

                if xvel > 0:
                    self.rect.right = p.rect.left
                    self.xvel = 0

                if xvel < 0:
                    self.rect.left = p.rect.right
                    self.xvel = 0

