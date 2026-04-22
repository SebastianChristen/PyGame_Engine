package com.example.tileengine.engine.world;

import java.util.HashMap;
import java.util.Map;

public final class TileRegistry {
    private final Map<Character, Tile> tilesBySymbol = new HashMap<>();

    public void register(Tile tile) {
        tilesBySymbol.put(tile.symbol(), tile);
    }

    public Tile get(char symbol) {
        Tile tile = tilesBySymbol.get(symbol);
        if (tile == null) {
            throw new IllegalArgumentException("No tile registered for symbol: " + symbol);
        }
        return tile;
    }
}
