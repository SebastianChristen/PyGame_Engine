package com.example.tileengine.engine.entities;

import com.example.tileengine.engine.world.Position;

import java.util.UUID;

public abstract class Entity {
    private final String id = UUID.randomUUID().toString();
    private Position position;

    protected Entity(Position position) {
        this.position = position;
    }

    public String id() {
        return id;
    }

    public Position position() {
        return position;
    }

    public void setPosition(Position position) {
        this.position = position;
    }
}
