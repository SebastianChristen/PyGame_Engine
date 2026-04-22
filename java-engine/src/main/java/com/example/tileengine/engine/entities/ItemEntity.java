package com.example.tileengine.engine.entities;

import com.example.tileengine.engine.items.ItemDefinition;
import com.example.tileengine.engine.world.Position;

public final class ItemEntity extends Entity {
    private final ItemDefinition itemDefinition;

    public ItemEntity(Position position, ItemDefinition itemDefinition) {
        super(position);
        this.itemDefinition = itemDefinition;
    }

    public ItemDefinition itemDefinition() {
        return itemDefinition;
    }
}
