# =========================
# FLAGS
# =========================
class WorldFlags:
    HOUSE_COLLAPSED = "house_collapsed"


# =========================
# GAME
# =========================
class Game:
    def __init__(self):
        self.flags = {}

    def set_flag(self, key, value=True):
        self.flags[key] = value

    def get_flag(self, key):
        return self.flags.get(key, False)


game = Game()


# =========================
# TILE DEFINITIONS
# =========================
TILES = {
    "W": {"name": "wall", "walkable": False},
    ".": {"name": "floor", "walkable": True},
}


# =========================
# ROOM
# =========================
class Room:
    def __init__(self, name="", description="", tilemap=None):
        self.name = name
        self.description = description
        self.items = []
        self.tilemap = tilemap or []

        self.height = len(self.tilemap)
        self.width = len(self.tilemap[0]) if self.tilemap else 0

    def get_description(self):
        return self.description

    def add_item(self, item, x, y):
        self.items.append((item, x, y))

    def remove_item(self, item):
        self.items = [(i, x, y) for (i, x, y) in self.items if i != item]

    def get_items(self):
        return self.items

    # ---------- TILE LOGIC ----------
    def in_bounds(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def get_tile(self, x, y):
        if not self.in_bounds(x, y):
            return None
        return self.tilemap[y][x]

    def is_walkable(self, x, y):
        tile = self.get_tile(x, y)
        if tile is None:
            return False
        return TILES[tile]["walkable"]

    def on_enter(self):
        pass

    def update(self):
        pass


# =========================
# SPECIAL ROOM
# =========================
class WhiteHouse(Room):
    def get_description(self):
        if game.get_flag(WorldFlags.HOUSE_COLLAPSED):
            return "You are standing on ruins. The house has collapsed."
        return self.description


# =========================
# ITEM
# =========================
class Item:
    def __init__(self, name):
        self.name = name

    def on_take(self, player):
        player.inventory.append(self)
        player.current_room.remove_item(self)

        print(f"You take the {self.name}.")

# Special item with effect
class Stone(Item):
    def on_take(self, player):
        super().on_take(player)

        print("The ground trembles...")
        game.set_flag(WorldFlags.HOUSE_COLLAPSED)


# =========================
# PLAYER
# =========================
class Player:
    def __init__(self, starting_room):
        self.current_room = starting_room
        self.inventory = []
        self.position_within_room = (1, 1)

    
    # TODO: Replace with a generic "interact", and make sure player facing direction matterns, instaed of standing ontop of the item.
    def take(self, item_name):
        player_x, player_y = self.position_within_room

        for (item, item_x, item_y) in self.current_room.get_items():
            if item.name.lower() == item_name.lower() and (item_x, item_y) == (player_x, player_y):
                item.on_take(self)
                return

        print("There is no such item here.")

    def show_inventory(self):
        if not self.inventory:
            print("Your inventory is empty.")
        else:
            print("You have: " + ", ".join(item.name for item in self.inventory))


# =========================
# RENDERER
# =========================
class Renderer:
    def render_room(self, player):
        room = player.current_room

        print("\n" + room.get_description())

        px, py = player.position_within_room
        print(f"Position: ({px}, {py})\n")

        # build grid copy
        grid = [list(row) for row in room.tilemap]

        # draw items
        for (item, x, y) in room.get_items():
            if room.in_bounds(x, y):
                grid[y][x] = "I"

        # draw player
        if room.in_bounds(px, py):
            grid[py][px] = "P"

        # render grid
        for row in grid:
            print("".join(row))

        # list items (debug-style)
        items = room.get_items()

        if items:
            for (item, x, y) in items:
                print(f"You see: {item.name} at ({x}, {y})")
        else:
            print("There is nothing in this room...")


# =========================
# MOVEMENT (WITH COLLISION)
# =========================
def handle_movement(command, player):
    x, y = player.position_within_room

    dx, dy = 0, 0

    if command == "w":
        dy = -1
    elif command == "s":
        dy = 1
    elif command == "a":
        dx = -1
    elif command == "d":
        dx = 1
    else:
        return

    new_x = x + dx
    new_y = y + dy

    if player.current_room.is_walkable(new_x, new_y):
        player.position_within_room = (new_x, new_y)
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

    elif command in ["w", "a", "s", "d"]:
        handle_movement(command, player)

    elif command.startswith("take "):
        item_name = command.replace("take ", "")
        player.take(item_name)

    elif command == "inventory":
        player.show_inventory()

    else:
        print("Unknown command.")
