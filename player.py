import pygame

MOVE_SPEED = 7
JUMP_POWER = 10
GRAVITY = 0.35
RUN_ANIMATION_SPEED = 0.08
IDLE_BLINK_SPEED = 0.12
IDLE_WAIT_MS = 3000


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
        self.last_activity_time = pygame.time.get_ticks()
        self.is_blinking = False

    def load_animations(self):
        scale = 0.8

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
        self.idle_frames = self.normalize_frames(self.idle_frames)

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

    def normalize_frames(self, frames):
        max_w = max(frame.get_width() for frame in frames)
        max_h = max(frame.get_height() for frame in frames)
        normalized = []

        for frame in frames:
            canvas = pygame.Surface((max_w, max_h), pygame.SRCALPHA)
            x = (max_w - frame.get_width()) // 2
            y = max_h - frame.get_height()
            canvas.blit(frame, (x, y))
            normalized.append(canvas)

        return normalized

    def update(self, left, right, up, platforms, force_run=False):
        now = pygame.time.get_ticks()
        previous_state = self.state
        was_on_ground = self.onGround

        if up and was_on_ground:
            self.yvel = -JUMP_POWER

        # --- Рух і напрямок ---
        if left:
            self.xvel = -MOVE_SPEED
            if not force_run:
                self.facing = "left"
        elif right:
            self.xvel = MOVE_SPEED
            if not force_run:
                self.facing = "right"
        else:
            self.xvel = 0

        # Гравітація
        if not was_on_ground:
            self.yvel += GRAVITY

        self.onGround = False

        self.rect.y += self.yvel
        self.collide(0, self.yvel, platforms)

        self.rect.x += self.xvel
        self.collide(self.xvel, 0, platforms)

        # Перевірка стану
        if self.yvel == 0:
            self.rect.y += 1
            self.onGround = any(pygame.sprite.collide_rect(self, p) for p in platforms)
            self.rect.y -= 1

        if not self.onGround:
            self.state = "jump"
        elif self.xvel != 0 or force_run:
            self.state = "run"
        else:
            self.state = "idle"

        if self.state != previous_state:
            self.frame_index = 0
            self.animation_timer = 0

        if abs(self.xvel) < 0.1:
            self.xvel = 0

        if left or right or up or self.state != "idle":
            self.last_activity_time = now
            self.is_blinking = False
            if self.state != "run":
                self.frame_index = 0

        self.animate()

    def animate(self):
        if self.state == "idle":
            frames = self.idle_frames
            now = pygame.time.get_ticks()
            inactive_ms = now - self.last_activity_time

            if not self.is_blinking and inactive_ms < IDLE_WAIT_MS:
                self.frame_index = 0
                self.animation_timer = 0
                frame = frames[0]
            else:
                if not self.is_blinking:
                    self.is_blinking = True
                    self.frame_index = 0
                    self.animation_timer = 0

                self.animation_timer += IDLE_BLINK_SPEED
                if self.animation_timer >= 1:
                    self.animation_timer = 0
                    self.frame_index += 1

                if self.frame_index >= len(frames):
                    self.is_blinking = False
                    self.last_activity_time = now
                    self.frame_index = 0

                frame = frames[self.frame_index]

        elif self.state == "run":
            frames = self.run_frames
            self.animation_timer += RUN_ANIMATION_SPEED

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
                    self.xvel = 0
                if xvel < 0:
                    self.rect.left = p.rect.right
                    self.xvel = 0
                if yvel > 0:
                    self.rect.bottom = p.rect.top
                    self.onGround = True
                    self.yvel = 0
                if yvel < 0:
                    self.rect.top = p.rect.bottom
                    self.yvel = 0
