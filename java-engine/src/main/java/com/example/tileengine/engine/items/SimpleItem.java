package com.example.tileengine.engine.items;

import com.example.tileengine.engine.core.GameContext;
import com.example.tileengine.engine.entities.PlayerEntity;

public class SimpleItem implements ItemDefinition {
    private final String id;
    private final String displayName;
    private final String spritePath;

    public SimpleItem(String id, String displayName, String spritePath) {
        this.id = id;
        this.displayName = displayName;
        this.spritePath = spritePath;
    }

    @Override
    public String id() {
        return id;
    }

    @Override
    public String displayName() {
        return displayName;
    }

    @Override
    public String spritePath() {
        return spritePath;
    }

    @Override
    public void onCollect(GameContext context, PlayerEntity player) {
        context.messageLog().push("You take the " + displayName + ".");
    }
}
