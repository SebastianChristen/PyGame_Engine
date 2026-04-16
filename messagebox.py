# messagebox.py
import pygame

BOX_HEIGHT = 120
BOX_PADDING = 12
TEXT_PADDING = 8

BOX_BACKGROUND_COLOR = (20, 20, 20)
BOX_BORDER_COLOR = (200, 200, 200)
TEXT_COLOR = (255, 255, 255)

FONT_SIZE = 24


class MessageBox:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.rect = pygame.Rect(
            0,
            screen_height - BOX_HEIGHT,
            screen_width,
            BOX_HEIGHT,
        )

        self.font = pygame.font.Font(None, FONT_SIZE)
        self.current_message = ""

    def show_message(self, text):
        self.current_message = text

    def clear(self):
        self.current_message = ""

    def draw(self, surface):
        pygame.draw.rect(surface, BOX_BACKGROUND_COLOR, self.rect)
        pygame.draw.rect(surface, BOX_BORDER_COLOR, self.rect, 2)

        if not self.current_message:
            return

        text_surface = self.font.render(self.current_message, True, TEXT_COLOR)
        text_x = self.rect.x + BOX_PADDING
        text_y = self.rect.y + TEXT_PADDING
        surface.blit(text_surface, (text_x, text_y))