# =========================
# IMPORTS
# =========================
from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, List, Tuple, Optional

import pygame


# =========================
# CONFIG
# =========================
TILE_SIZE: int = 48
FPS: int = 60

COLOR_BG = (20, 20, 20)
COLOR_FLOOR = (90, 90, 90)
COLOR_WALL = (45, 45, 45)
COLOR_PLAYER = (255, 255, 255)
COLOR_ITEM = (220, 180, 40)


# =========================
# FLAGS
# =========================
class WorldFlag(Enum):
    HOUSE_COLLAPSED = auto()


# =========================
# GAME
# =========================
class Game:
    def __init__(self) -> None:
        self.flags: set[WorldFlag] = set()

    def set_flag(self, flag: WorldFlag) -> None:
        self.flags.add(flag)

    def has_flag(self, flag: WorldFlag) -> bool:
        return flag in self.flags


game = Game()


# =========================
# TILE SYSTEM
# =========================
class Tile:
    symbol: str = "?"
    walkable: bool = True
    color: Tuple[int, int, int] = COLOR_FLOOR

    def on_step(self, player: Player) -> None:
        pass

    @classmethod
    def create_registry(cls) -> Dict[str, Tile]:
        return {
            FloorTile.symbol: FloorTile(),
            WallTile.symbol: WallTile(),
        }


class FloorTile(Tile):
    symbol = "."
    walkable = True
    color = COLOR_FLOOR
    
    def on_step(self, player: Player) -> None:
        print("You hear a soft footstep.")


class WallTile(Tile):
    symbol = "W"
    walkable = False
    color = COLOR_WALL


TILE_REGISTRY: Dict[str, Tile] = Tile.create_registry()


# =========================
# DATA
# =========================
@dataclass
class PositionedItem:
    item: Item
    x: int
    y: int


# =========================
# ROOM
# =========================
class Room:
    def __init__(
        self,
        name: str,
        description: str,
        tilemap: List[str]
    ) -> None:
        self.name = name
        self.description = description
        self.tilemap = tilemap
        self.items: List[PositionedItem] = []

        self.height: int = len(tilemap)
        self.width: int = len(tilemap[0]) if tilemap else 0

    def get_description(self) -> str:
        return self.description

    def add_item(self, item: Item, x: int, y: int) -> None:
        self.items.append(PositionedItem(item, x, y))

    def remove_item(self, item: Item) -> None:
        self.items = [i for i in self.items if i.item != item]

    def get_items(self) -> List[PositionedItem]:
        return self.items

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def get_tile(self, x: int, y: int) -> Optional[Tile]:
        if not self.in_bounds(x, y):
            return None

        symbol = self.tilemap[y][x]
        return TILE_REGISTRY.get(symbol)

    def is_walkable(self, x: int, y: int) -> bool:
        tile = self.get_tile(x, y)
        return tile.walkable if tile else False


class WhiteHouse(Room):
    def get_description(self) -> str:
        if game.has_flag(WorldFlag.HOUSE_COLLAPSED):
            return "You are standing on ruins. The house has collapsed."
        return self.description


# =========================
# ITEM
# =========================
class Item:
    def __init__(self, name: str) -> None:
        self.name = name

    def on_take(self, player: Player) -> None:
        player.inventory.append(self)
        player.current_room.remove_item(self)
        print(f"You take the {self.name}.")


class Stone(Item):
    def on_take(self, player: Player) -> None:
        super().on_take(player)
        print("The ground trembles...")
        game.set_flag(WorldFlag.HOUSE_COLLAPSED)


# =========================
# PLAYER
# =========================
class Player:
    def __init__(self, starting_room: Room) -> None:
        self.current_room: Room = starting_room
        self.inventory: List[Item] = []
        self.position: Tuple[int, int] = (1, 1)

    def take(self) -> None:
        px, py = self.position

        for positioned in self.current_room.get_items():
            if (positioned.x, positioned.y) == (px, py):
                positioned.item.on_take(self)
                return

        print("There is nothing here to take.")

    def show_inventory(self) -> None:
        if not self.inventory:
            print("Your inventory is empty.")
        else:
            print("You have:", ", ".join(i.name for i in self.inventory))


# =========================
# RENDERER
# =========================
class Renderer:
    def __init__(self, room: Room) -> None:
        pygame.init()

        self.screen_width = room.width * TILE_SIZE
        self.screen_height = room.height * TILE_SIZE

        self.screen = pygame.display.set_mode(
            (self.screen_width, self.screen_height)
        )
        pygame.display.set_caption("Tile Engine")

        self.clock = pygame.time.Clock()

    def render_room(self, player: Player) -> None:
        room = player.current_room
        self.screen.fill(COLOR_BG)

        # draw tiles
        for y in range(room.height):
            for x in range(room.width):
                tile = room.get_tile(x, y)
                if tile is None:
                    continue

                rect = pygame.Rect(
                    x * TILE_SIZE,
                    y * TILE_SIZE,
                    TILE_SIZE,
                    TILE_SIZE
                )

                pygame.draw.rect(self.screen, tile.color, rect)

        # draw items
        for positioned in room.get_items():
            rect = pygame.Rect(
                positioned.x * TILE_SIZE + 12,
                positioned.y * TILE_SIZE + 12,
                TILE_SIZE - 24,
                TILE_SIZE - 24
            )
            pygame.draw.rect(self.screen, COLOR_ITEM, rect)

        # draw player
        px, py = player.position
        rect = pygame.Rect(
            px * TILE_SIZE + 8,
            py * TILE_SIZE + 8,
            TILE_SIZE - 16,
            TILE_SIZE - 16
        )
        pygame.draw.rect(self.screen, COLOR_PLAYER, rect)

        pygame.display.flip()
        self.clock.tick(FPS)


# =========================
# MOVEMENT
# =========================
class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


def handle_movement(direction: Direction, player: Player) -> None:
    x, y = player.position

    dx, dy = {
        Direction.UP: (0, -1),
        Direction.DOWN: (0, 1),
        Direction.LEFT: (-1, 0),
        Direction.RIGHT: (1, 0),
    }[direction]

    new_x = x + dx
    new_y = y + dy

    tile = player.current_room.get_tile(new_x, new_y)

    if tile and tile.walkable:
        player.position = (new_x, new_y)
        tile.on_step(player)


# =========================
# INPUT
# =========================
def handle_events(player: Player) -> bool:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return False

            elif event.key == pygame.K_w:
                handle_movement(Direction.UP, player)

            elif event.key == pygame.K_s:
                handle_movement(Direction.DOWN, player)

            elif event.key == pygame.K_a:
                handle_movement(Direction.LEFT, player)

            elif event.key == pygame.K_d:
                handle_movement(Direction.RIGHT, player)

            elif event.key == pygame.K_e:
                player.take()

            elif event.key == pygame.K_TAB:
                player.show_inventory()

    return True


# =========================
# SETUP
# =========================
house_map = [
    "WWWWWWWWWW",
    "W........W",
    "W........W",
    "W........W",
    "W........W",
    "W........W",
    "W........W",
    "WWWWWWWWWW",
]

house = WhiteHouse(
    name="White House",
    description="You are standing in front of a white house.",
    tilemap=house_map
)

stone = Stone("stone")
house.add_item(stone, 4, 3)

player = Player(house)
renderer = Renderer(house)


# =========================
# GAME LOOP
# =========================
running = True

while running:
    running = handle_events(player)
    renderer.render_room(player)

pygame.quit()