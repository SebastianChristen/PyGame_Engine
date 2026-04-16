# movement_module.py
import pygame
from tilemap import create_map_from_file
from messagebox import MessageBox
from logpanel import LogPanel

# =========================
# CONFIG
# =========================
FPS = 60

TILE_SIZE = 40

PLAYER_COLOR = (255, 255, 255)
BACKGROUND_COLOR = (0, 0, 0)

MOVE_DELAY = 200  # ms between steps


# =========================
# INPUT
# =========================
class InputHandler:
    def __init__(self):
        self.direction = (0, 0)

    def update(self):
        keys = pygame.key.get_pressed()

        dx = keys[pygame.K_d] - keys[pygame.K_a]
        dy = keys[pygame.K_s] - keys[pygame.K_w]

        # enforce 4-directional movement
        if dx != 0:
            dy = 0

        self.direction = (dx, dy)


# =========================
# ENTITY
# =========================
class Player:
    def __init__(self, grid_pos):
        self.grid_x, self.grid_y = grid_pos
        self._last_move_time = 0

    def update(self, direction, tilemap, game_context):
        now = pygame.time.get_ticks()

        if now - self._last_move_time < MOVE_DELAY:
            return

        dx, dy = direction
        if dx == 0 and dy == 0:
            return

        new_x = self.grid_x + dx
        new_y = self.grid_y + dy

        target_tile = tilemap.get_tile(new_x, new_y)
        if target_tile is None:
            return

        if target_tile.walkable:
            self.grid_x = new_x
            self.grid_y = new_y
            target_tile.on_enter(self, game_context)
            self._last_move_time = now
        else:
            target_tile.on_enter(self, game_context)
            self._last_move_time = now

    def draw(self, surface):
        px = self.grid_x * TILE_SIZE
        py = self.grid_y * TILE_SIZE

        rect = pygame.Rect(px, py, TILE_SIZE, TILE_SIZE)
        pygame.draw.rect(surface, PLAYER_COLOR, rect)


# =========================
# GAME
# =========================
class Game:
    def __init__(self):
        pygame.init()

        info = pygame.display.Info()
        self.screen_width = info.current_w
        self.screen_height = info.current_h

        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height),
            pygame.FULLSCREEN
        )
        pygame.display.set_caption("Tile Movement")

        self.clock = pygame.time.Clock()
        self.running = True

        self.input = InputHandler()
        self.tilemap = create_map_from_file()
        self.player = Player((2, 2))
        self.message_box = MessageBox(self.screen_width, self.screen_height)
        self.log_panel = LogPanel(self.screen_width, self.screen_height)

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            self._handle_events()
            self._update()
            self._render()

        pygame.quit()

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.log_panel.scroll_up()
                elif event.key == pygame.K_DOWN:
                    self.log_panel.scroll_down()

    def _update(self):
        self.input.update()
        self.player.update(self.input.direction, self.tilemap, self)

    def _render(self):
        self.screen.fill(BACKGROUND_COLOR)
        self.tilemap.draw(self.screen)
        self.player.draw(self.screen)

        self.message_box.draw(self.screen)
        self.log_panel.draw(self.screen)
        
        pygame.display.flip()


def run_game():
    Game().run()


if __name__ == "__main__":
    run_game()
