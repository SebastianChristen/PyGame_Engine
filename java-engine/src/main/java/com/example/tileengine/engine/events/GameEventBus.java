package com.example.tileengine.engine.events;

import java.util.ArrayList;
import java.util.List;
import java.util.function.Consumer;

public final class GameEventBus {
    private final List<Subscription<?>> subscriptions = new ArrayList<>();

    public <T extends GameEvent> void subscribe(Class<T> eventType, Consumer<T> consumer) {
        subscriptions.add(new Subscription<>(eventType, consumer));
    }

    @SuppressWarnings("unchecked")
    public void publish(GameEvent event) {
        for (Subscription<?> subscription : subscriptions) {
            if (subscription.eventType.isInstance(event)) {
                ((Consumer<GameEvent>) subscription.consumer).accept(event);
            }
        }
    }

    private record Subscription<T extends GameEvent>(Class<T> eventType, Consumer<T> consumer) {
    }
}
