package com.example.tileengine.engine.events;

import com.example.tileengine.engine.world.WorldFlag;

public record FlagChangedEvent(WorldFlag flag) implements GameEvent {
}
