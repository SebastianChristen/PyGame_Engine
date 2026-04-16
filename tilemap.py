# tilemap.py
from tiles import WallTile, CarpetTile, TILE_SIZE

SYMBOL_TO_TILE_CLASS = {
    "W": WallTile,
    "c": CarpetTile,
}


class TileMap:
    def __init__(self, grid):
        self.grid = grid
        self.height = len(grid)
        self.width = len(grid[0]) if grid else 0

    def get_tile(self, x, y):
        if not self._in_bounds(x, y):
            return None
        return self.grid[y][x]

    def is_walkable(self, x, y):
        tile = self.get_tile(x, y)
        return tile is not None and tile.walkable

    def _in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def draw(self, surface):
        for y, row in enumerate(self.grid):
            for x, tile in enumerate(row):
                px = x * TILE_SIZE
                py = y * TILE_SIZE
                surface.blit(tile.surface, (px, py))


def load_map_from_file(path):
    with open(path, "r") as f:
        rows = [line.rstrip("\n") for line in f if line.strip()]

    grid = []
    for y, row in enumerate(rows):
        grid_row = []
        for x, symbol in enumerate(row):
            tile_class = SYMBOL_TO_TILE_CLASS.get(symbol)
            if tile_class is None:
                raise ValueError(f"Unknown tile symbol '{symbol}' at ({x},{y})")

            # instantiate HERE (after pygame is initialized)
            grid_row.append(tile_class())

        grid.append(grid_row)

    return grid


def create_map_from_file(path="./levels/house_interior.txt"):
    return TileMap(load_map_from_file(path))