package com.example.tileengine.engine.systems;

import com.example.tileengine.engine.core.GameContext;
import com.example.tileengine.engine.entities.PlayerEntity;
import com.example.tileengine.engine.world.Direction;
import com.example.tileengine.engine.world.Position;
import com.example.tileengine.engine.world.Room;
import com.example.tileengine.engine.world.Tile;

public final class MovementSystem {
    public void move(GameContext context, Direction direction) {
        PlayerEntity player = context.world().player();
        Room room = context.world().currentRoom();
        Position target = player.position().translate(direction);

        Tile tile = room.tileAt(target, context.world().tileRegistry());
        if (tile == null || !tile.walkable()) {
            context.messageLog().push("You cannot move there.");
            return;
        }

        player.setPosition(target);
        tile.onStep().onStep(context, player, tile);
    }
}
