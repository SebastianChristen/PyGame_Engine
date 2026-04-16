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


game = Game()  # create early so classes can use it


# =========================
# ROOM
# =========================
class Room:
    def __init__(self, name="", description=""):
        self.name = name
        self.description = description
        self.items = []

    def get_description(self):
        return self.description

    # HERE
    def add_item(self, item, psotion x, psotion_y):
        self.items.append(item)

    def remove_item(self, item):
        if item in self.items:
            self.items.remove(item)

    def get_items(self):
        return self.items

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
        # HERE
        self.position_within_room = 0,0

    

    def take(self, item_name):
        for item in self.current_room.get_items():
            if item.name.lower() == item_name.lower():
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
    def render_room(self, room):
        print("\n" + room.get_description())
        # HERE
        print("you are on postion" player.position_in_room
        items = room.get_items()
        if items:
            # HERE
            print("You see: " + ", ".join(item.name for item in items; in position x and y))
        else:
            print("There is nothing in this room...")


# =========================
# SETUP
# =========================
house = WhiteHouse(
    name="White House",
    description="You are standing in front of a white house."
)

stone = Stone("stone")
house.add_item(stone)

player = Player(house)
renderer = Renderer()


# =========================
# GAME LOOP
# =========================
print("Welcome.\n")

running = True

while running:
    renderer.render_room(player.current_room)

    # HERE
    movement_module():
            according to keyboad input, move player.position_within_room

    




    if command == "quit":
        running = False

    elif command.startswith("take "):
        item_name = command.replace("take ", "")
        player.take(item_name)

    elif command == "inventory":
        player.show_inventory()

    else:
        print("Unknown command.")