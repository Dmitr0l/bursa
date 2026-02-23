import pygame


class Inventory:
    def __init__(self):
        self.cols = 6
        self.rows = 4
        self.slots = [None] * (self.cols * self.rows)

        self.open_progress = 0
        self.opening = False
        self.closing = False

        self.font = pygame.font.Font(None, 24)
        self.drag_index = None

    # ---------------- OPEN / CLOSE ----------------

    def open(self):
        self.opening = True
        self.closing = False

    def close(self):
        self.closing = True
        self.opening = False

    # 🔥 ВИПРАВЛЕНО
    def is_closed(self):
        return self.open_progress <= 0

    # ---------------- ADD ITEM ----------------

    def add_item(self, item_id, amount=1):
        for slot in self.slots:
            if slot and slot["id"] == item_id:
                slot["count"] += amount
                return

        for i in range(len(self.slots)):
            if self.slots[i] is None:
                self.slots[i] = {"id": item_id, "count": amount}
                return

    def clear(self):
        self.slots = [None] * (self.cols * self.rows)

    # ---------------- UPDATE ----------------

    def update(self, dt):
        speed = 4

        if self.opening:
            self.open_progress += speed * dt
            if self.open_progress >= 1:
                self.open_progress = 1
                self.opening = False

        if self.closing:
            self.open_progress -= speed * dt
            if self.open_progress <= 0:
                self.open_progress = 0
                self.closing = False

    # ---------------- EVENTS ----------------

    def handle_event(self, event):
        mouse = pygame.mouse.get_pos()

        if event.type == pygame.MOUSEBUTTONDOWN:
            idx = self.get_slot_index(mouse)
            if idx is not None:
                self.drag_index = idx

        if event.type == pygame.MOUSEBUTTONUP:
            idx = self.get_slot_index(mouse)
            if idx is not None and self.drag_index is not None:
                self.slots[idx], self.slots[self.drag_index] = \
                    self.slots[self.drag_index], self.slots[idx]
            self.drag_index = None

    # ---------------- SLOT LOGIC ----------------

    def get_slot_index(self, mouse):
        panel = self.get_panel_rect()
        size = 60
        pad = 10

        for i in range(len(self.slots)):
            col = i % self.cols
            row = i // self.cols

            x = panel.x + pad + col * (size + pad)
            y = panel.y + pad + row * (size + pad)

            rect = pygame.Rect(x, y, size, size)

            if rect.collidepoint(mouse):
                return i

        return None

    def get_panel_rect(self):
        height = 320
        y_offset = (1 - self.open_progress) * height
        return pygame.Rect(100, 60 + y_offset, 600, height)

    # ---------------- DRAW ----------------

    def draw(self, surface):
        panel = self.get_panel_rect()

        pygame.draw.rect(surface, (50, 50, 70), panel)
        pygame.draw.rect(surface, (150, 150, 200), panel, 3)

        size = 60
        pad = 10
        mouse = pygame.mouse.get_pos()

        for i, item in enumerate(self.slots):
            col = i % self.cols
            row = i // self.cols

            x = panel.x + pad + col * (size + pad)
            y = panel.y + pad + row * (size + pad)

            rect = pygame.Rect(x, y, size, size)

            pygame.draw.rect(surface, (120, 120, 120), rect)
            pygame.draw.rect(surface, (200, 200, 200), rect, 2)

            if item:
                txt = self.font.render(item["id"], True, (255, 255, 255))
                surface.blit(txt, (x + 5, y + 5))

                count_txt = self.font.render(
                    str(item["count"]), True, (255, 255, 0)
                )
                surface.blit(count_txt, (x + 40, y + 40))

                if rect.collidepoint(mouse):
                    tooltip = self.font.render(
                        f'{item["id"]} x{item["count"]}',
                        True,
                        (255, 255, 0)
                    )
                    surface.blit(tooltip, (mouse[0] + 10, mouse[1]))