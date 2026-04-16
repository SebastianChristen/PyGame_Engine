# tiles.py
import os
import pygame

TILE_SIZE = 40
ASSET_PATH = "./tiles/"


class Tile:
    symbol = "?"
    image_name = None
    walkable = True

    def __init__(self):
        self.surface = self._load_surface()

    def _load_surface(self):
        if self.image_name is None:
            raise ValueError(f"{self.__class__.__name__} has no image_name")

        image_path = os.path.join(ASSET_PATH, self.image_name)
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Missing tile image: {image_path}")

        surface = pygame.image.load(image_path).convert_alpha()
        surface = pygame.transform.scale(surface, (TILE_SIZE, TILE_SIZE))
        return surface

    def on_enter(self, player, game_context):
        pass

    def on_interact(self, player, game_context):
        pass


class WallTile(Tile):
    symbol = "W"
    image_name = "wall_1.png"
    walkable = False

    def on_enter(self, player, game_context):
        msg =  "Ouch. You somehow noclipped into a wall."
        game_context.message_box.show_message(msg)
        game_context.log_panel.add(msg)
        


class CarpetTile(Tile):
    symbol = "c"
    image_name = "carpet_1.png"
    walkable = True

    def on_enter(self, player, game_context):
        msg = "Soft carpet underfoot."
        game_context.message_box.show_message(msg)
        game_context.log_panel.add(msg)