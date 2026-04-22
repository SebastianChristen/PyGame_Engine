package com.example.tileengine.game.content;

import com.example.tileengine.engine.world.Tile;
import com.example.tileengine.engine.world.TileRegistry;

public final class DefaultTiles {
    private DefaultTiles() {}

    public static TileRegistry createRegistry() {
        TileRegistry registry = new TileRegistry();

        registry.register(new Tile(
                "floor.basic",
                '.',
                true,
                "/assets/tiles/carpet_1.png",
                (context, player, tile) -> context.messageLog().push("You hear a soft footstep.")
        ));

        registry.register(new Tile(
                "wall.basic",
                'W',
                false,
                "/assets/tiles/wall_1.png",
                (context, player, tile) -> { }
        ));

        return registry;
    }
}
