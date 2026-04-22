package com.example.tileengine.engine.world;

import com.example.tileengine.engine.core.GameContext;
import com.example.tileengine.engine.entities.PlayerEntity;

@FunctionalInterface
public interface TileStepBehavior {
    void onStep(GameContext context, PlayerEntity player, Tile tile);
}
