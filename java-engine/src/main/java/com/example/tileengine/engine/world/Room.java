package com.example.tileengine.engine.world;

import com.example.tileengine.engine.entities.ItemEntity;

import java.util.ArrayList;
import java.util.List;
import java.util.Optional;

public final class Room {
    private final String id;
    private final String name;
    private final List<String> tileRows;
    private final RoomDescriptionProvider descriptionProvider;
    private final List<ItemEntity> items = new ArrayList<>();

    public Room(String id, String name, List<String> tileRows, RoomDescriptionProvider descriptionProvider) {
        this.id = id;
        this.name = name;
        this.tileRows = List.copyOf(tileRows);
        this.descriptionProvider = descriptionProvider;
        validateRectangular();
    }

    private void validateRectangular() {
        if (tileRows.isEmpty()) {
            return;
        }
        int width = tileRows.getFirst().length();
        for (String row : tileRows) {
            if (row.length() != width) {
                throw new IllegalArgumentException("Room tilemap must be rectangular.");
            }
        }
    }

    public String id() {
        return id;
    }

    public String name() {
        return name;
    }

    public int width() {
        return tileRows.isEmpty() ? 0 : tileRows.getFirst().length();
    }

    public int height() {
        return tileRows.size();
    }

    public String describe(World world) {
        return descriptionProvider.describe(world, this);
    }

    public boolean inBounds(Position position) {
        return position.x() >= 0 && position.x() < width() && position.y() >= 0 && position.y() < height();
    }

    public Tile tileAt(Position position, TileRegistry registry) {
        if (!inBounds(position)) {
            return null;
        }
        return registry.get(tileRows.get(position.y()).charAt(position.x()));
    }

    public void addItem(ItemEntity item) {
        items.add(item);
    }

    public void removeItem(ItemEntity item) {
        items.remove(item);
    }

    public List<ItemEntity> items() {
        return List.copyOf(items);
    }

    public Optional<ItemEntity> itemAt(Position position) {
        return items.stream().filter(item -> item.position().equals(position)).findFirst();
    }
}
