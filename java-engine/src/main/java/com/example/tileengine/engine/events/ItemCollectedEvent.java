package com.example.tileengine.engine.events;

import com.example.tileengine.engine.entities.ItemEntity;
import com.example.tileengine.engine.entities.PlayerEntity;

public record ItemCollectedEvent(PlayerEntity player, ItemEntity item) implements GameEvent {
}
