package com.example.tileengine.game.rules;

import com.example.tileengine.engine.core.GameContext;
import com.example.tileengine.engine.events.FlagChangedEvent;
import com.example.tileengine.engine.events.ItemCollectedEvent;
import com.example.tileengine.engine.world.WorldFlag;

public final class StoneCollapseRule {
    public void register(GameContext context) {
        context.eventBus().subscribe(ItemCollectedEvent.class, event -> {
            if (!"stone".equals(event.item().itemDefinition().id())) {
                return;
            }
            context.messageLog().push("The ground trembles...");
            context.world().setFlag(WorldFlag.HOUSE_COLLAPSED);
            context.eventBus().publish(new FlagChangedEvent(WorldFlag.HOUSE_COLLAPSED));
        });
    }
}
