from __future__ import annotations
from dataclasses import dataclass
from enum import Enum, auto
from typing import Dict, List, Tuple, Optional


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

    def on_step(self, player: Player) -> None:
        print("You hear a soft footstep.")


class WallTile(Tile):
    symbol = "W"
    walkable = False


TILE_REGISTRY: Dict[str, Tile] = Tile.create_registry()


# =========================
# DATA STRUCTURES
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

        if symbol not in TILE_REGISTRY:
            raise ValueError(f"Unknown tile symbol: {symbol}")

        return TILE_REGISTRY[symbol]

    def is_walkable(self, x: int, y: int) -> bool:
        tile = self.get_tile(x, y)
        return tile.walkable if tile else False

    def update(self) -> None:
        pass


# =========================
# SPECIAL ROOM
# =========================
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

    def take(self, item_name: str) -> None:
        px, py = self.position

        for positioned in self.current_room.get_items():
            if (
                positioned.item.name.lower() == item_name.lower()
                and (positioned.x, positioned.y) == (px, py)
            ):
                positioned.item.on_take(self)
                return

        print("There is no such item here.")

    def show_inventory(self) -> None:
        if not self.inventory:
            print("Your inventory is empty.")
        else:
            print("You have:", ", ".join(i.name for i in self.inventory))


# =========================
# RENDERER
# =========================
class Renderer:
    def render_room(self, player: Player) -> None:
        room = player.current_room

        print("\n" + room.get_description())

        px, py = player.position
        print(f"Position: ({px}, {py})\n")

        grid = [list(row) for row in room.tilemap]

        for positioned in room.get_items():
            if room.in_bounds(positioned.x, positioned.y):
                grid[positioned.y][positioned.x] = "I"

        if room.in_bounds(px, py):
            grid[py][px] = "P"

        for row in grid:
            print("".join(row))

        if room.get_items():
            for p in room.get_items():
                print(f"You see: {p.item.name} at ({p.x}, {p.y})")
        else:
            print("There is nothing in this room...")


# =========================
# MOVEMENT
# =========================
class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


INPUT_MAP: Dict[str, Direction] = {
    "w": Direction.UP,
    "s": Direction.DOWN,
    "a": Direction.LEFT,
    "d": Direction.RIGHT,
}


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
    else:
        print("You bump into something.")


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
renderer = Renderer()


# =========================
# GAME LOOP
# =========================
print("Welcome.\n")

running = True

while running:
    renderer.render_room(player)

    command = input("\n> ").strip().lower()

    if command == "quit":
        running = False

    elif command in INPUT_MAP:
        handle_movement(INPUT_MAP[command], player)

    elif command.startswith("take "):
        player.take(command.replace("take ", ""))

    elif command == "inventory":
        player.show_inventory()

    else:
        print("Unknown command.")