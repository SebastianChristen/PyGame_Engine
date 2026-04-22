package com.example.tileengine.engine.entities;

import com.example.tileengine.engine.items.ItemDefinition;

import java.util.ArrayList;
import java.util.List;

public final class Inventory {
    private final List<ItemDefinition> items = new ArrayList<>();

    public void add(ItemDefinition item) {
        items.add(item);
    }

    public boolean isEmpty() {
        return items.isEmpty();
    }

    public List<ItemDefinition> items() {
        return List.copyOf(items);
    }
}
