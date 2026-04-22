package com.example.tileengine.game.content;

import com.example.tileengine.engine.world.Room;
import com.example.tileengine.engine.world.WorldFlag;

import java.util.List;

public final class DefaultRooms {
    private DefaultRooms() {}

    public static Room createWhiteHouse() {
        return new Room(
                "white_house",
                "White House",
                List.of(
                        "WWWWWWWWWW",
                        "W........W",
                        "W........W",
                        "W........W",
                        "W........W",
                        "W........W",
                        "W........W",
                        "WWWWWWWWWW"
                ),
                (world, room) -> world.hasFlag(WorldFlag.HOUSE_COLLAPSED)
                        ? "You are standing on ruins. The house has collapsed."
                        : "You are standing in front of a white house."
        );
    }
}
