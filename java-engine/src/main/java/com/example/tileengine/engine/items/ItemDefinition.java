package com.example.tileengine.engine.items;

import com.example.tileengine.engine.core.GameContext;
import com.example.tileengine.engine.entities.PlayerEntity;

public interface ItemDefinition {
    String id();
    String displayName();
    String spritePath();
    void onCollect(GameContext context, PlayerEntity player);
}
