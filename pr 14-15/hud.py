import pygame

class HUD:
    def __init__(self):
        self.hp = 100
        self.hp_max = 100
        self.score = 0
        self.time = 0

        self.font = pygame.font.Font(None, 28)
        self.cached_score = None
        self.cached_timer = None

    def reset(self):
        self.hp = 100
        self.score = 0
        self.time = 0

    def update(self, dt):
        self.time += dt

    def draw(self, surface):
        ratio = self.hp / self.hp_max
        pygame.draw.rect(surface, (150,0,0), (20,20,200,20))
        pygame.draw.rect(surface, (0,200,0), (20,20,200*ratio,20))

        if self.cached_score != self.score:
            self.score_surf = self.font.render(f"Score: {self.score}", True, (255,255,255))
            self.cached_score = self.score
        surface.blit(self.score_surf, (20,50))

        m = int(self.time // 60)
        s = int(self.time % 60)
        text = f"{m:02}:{s:02}"

        if self.cached_timer != text:
            self.timer_surf = self.font.render(text, True, (255,255,255))
            self.cached_timer = text

        surface.blit(self.timer_surf, (20,75))