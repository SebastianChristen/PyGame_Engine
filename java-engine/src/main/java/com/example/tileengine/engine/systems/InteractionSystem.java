package com.example.tileengine.engine.systems;

import com.example.tileengine.engine.core.GameContext;
import com.example.tileengine.engine.entities.ItemEntity;
import com.example.tileengine.engine.entities.PlayerEntity;
import com.example.tileengine.engine.events.ItemCollectedEvent;
import com.example.tileengine.engine.world.Room;

public final class InteractionSystem {
    public void collectItemAtPlayerPosition(GameContext context) {
        PlayerEntity player = context.world().player();
        Room room = context.world().currentRoom();
        ItemEntity item = room.itemAt(player.position()).orElse(null);

        if (item == null) {
            context.messageLog().push("There is nothing here to take.");
            return;
        }

        player.inventory().add(item.itemDefinition());
        room.removeItem(item);
        item.itemDefinition().onCollect(context, player);
        context.eventBus().publish(new ItemCollectedEvent(player, item));
    }

    public void showInventory(GameContext context) {
        if (context.world().player().inventory().isEmpty()) {
            context.messageLog().push("Your inventory is empty.");
            return;
        }

        String items = context.world().player().inventory().items().stream()
                .map(item -> item.displayName())
                .reduce((left, right) -> left + ", " + right)
                .orElse("empty");
        context.messageLog().push("Inventory: " + items);
    }
}
