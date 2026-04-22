package com.example.tileengine.engine.world;

public final class Tile {
    private final String id;
    private final char symbol;
    private final boolean walkable;
    private final String spritePath;
    private final TileStepBehavior onStep;

    public Tile(String id, char symbol, boolean walkable, String spritePath, TileStepBehavior onStep) {
        this.id = id;
        this.symbol = symbol;
        this.walkable = walkable;
        this.spritePath = spritePath;
        this.onStep = onStep;
    }

    public String id() {
        return id;
    }

    public char symbol() {
        return symbol;
    }

    public boolean walkable() {
        return walkable;
    }

    public String spritePath() {
        return spritePath;
    }

    public TileStepBehavior onStep() {
        return onStep;
    }
}
