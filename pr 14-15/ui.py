import pygame

class Button:
    def __init__(self, x, y, w, h, text):
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.font = pygame.font.Font(None, 36)
        self.hover = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(pygame.mouse.get_pos())

        if event.type == pygame.MOUSEBUTTONUP:
            if self.rect.collidepoint(pygame.mouse.get_pos()):
                return True
        return False

    def draw(self, surface):
        color = (200, 200, 200) if self.hover else (150, 150, 150)
        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, (255, 255, 0), self.rect, 3)

        text_surf = self.font.render(self.text, True, (0, 0, 0))
        surface.blit(text_surf, text_surf.get_rect(center=self.rect.center))
