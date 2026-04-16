class Room:
    def __init__(self, name="", description=""):
        self.name = name
        self.description = description
        self.items = []

    def set_name(self, name):
        self.name = name

    def set_description(self, description):
        self.description = description

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description
    

    def add_item(self, item):
        self.items.add(item)

    def on_enter(self, game_context):
        pass

    def update(self, game_context):
        pass


class Item:
    def on_take(self):
        player.inventory.append(self)

        game_context.message_box.show_message("You take the stone.")
        game_context.log_panel.add("You take the stone.")

class Player:
    current_room = xyz      


class WorldFlags:
    HOUSE_COLLAPSED = "house_collapsed"
    BRIDGE_DESTROYED = "bridge_destroyed"


class EventFlags:
    HOUSE_COLLAPSE_SHOWN = "house_collapse_shown"


class NPCFlags:
    GUARD_HOSTILE = "guard_hostile"



//setup
house = Room(name="white house", description="you are standing infront of a white house")
player = player(current_room=house)


@Loop {

    command = commandmodule.getInput()

  

    if currentroom = house {

    if WorldFlags.HOUSE_COLLAPSED:
        house.description = "you are standing on a ruin that was once a house"

    }


}