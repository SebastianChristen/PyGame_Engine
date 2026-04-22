package com.example.tileengine.engine.entities;

import com.example.tileengine.engine.world.Position;

public final class PlayerEntity extends Entity {
    private final Inventory inventory = new Inventory();

    public PlayerEntity(Position position) {
        super(position);
    }

    public Inventory inventory() {
        return inventory;
    }
}
