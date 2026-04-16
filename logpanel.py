# logpanel.py
import pygame

PANEL_WIDTH = 300
PADDING = 8

BG_COLOR = (15, 15, 15)
BORDER_COLOR = (200, 200, 200)
TEXT_COLOR = (220, 220, 220)

FONT_SIZE = 18
MAX_MESSAGES = 300


class LogPanel:
    def __init__(self, screen_width, screen_height):
        self.rect = pygame.Rect(
            screen_width - PANEL_WIDTH,
            0,
            PANEL_WIDTH,
            screen_height,
        )

        self.font = pygame.font.Font(None, FONT_SIZE)
        self.messages = []
        self.scroll_offset = 0

        self.line_height = self.font.get_height()

    # =========================
    # DATA
    # =========================
    def add(self, text):
        self.messages.append(text)

        if len(self.messages) > MAX_MESSAGES:
            self.messages.pop(0)

        self.scroll_offset = -4  # auto-scroll to newest

    # =========================
    # SCROLLING
    # =========================
    def scroll_up(self):
        max_offset = max(0, len(self.messages) - self._visible_lines())
        self.scroll_offset = min(self.scroll_offset + 1, max_offset)

    def scroll_down(self):
        self.scroll_offset = max(self.scroll_offset - 1, -4)

    def _visible_lines(self):
        return self.rect.height // self.line_height

    # =========================
    # RENDER
    # =========================
    def draw(self, surface):
        pygame.draw.rect(surface, BG_COLOR, self.rect)
        pygame.draw.rect(surface, BORDER_COLOR, self.rect, 2)

        visible_lines = self._visible_lines()

        start_index = max(
            0,
            len(self.messages) - visible_lines - self.scroll_offset
        )
        end_index = start_index + visible_lines

        visible = self.messages[start_index:end_index]

        y = self.rect.y + PADDING

        for msg in visible:
            text_surface = self.font.render(msg, True, TEXT_COLOR)
            surface.blit(text_surface, (self.rect.x + PADDING, y))
            y += self.line_height