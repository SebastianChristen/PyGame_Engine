package com.example.tileengine.game.content;

import com.example.tileengine.engine.items.SimpleItem;

public final class DefaultItems {
    private DefaultItems() {}

    public static SimpleItem createStone() {
        return new SimpleItem("stone", "stone", "/assets/item.png");
    }
}
