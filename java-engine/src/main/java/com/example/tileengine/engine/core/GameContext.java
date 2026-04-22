package com.example.tileengine.engine.core;

import com.example.tileengine.engine.assets.AssetManager;
import com.example.tileengine.engine.events.GameEventBus;
import com.example.tileengine.engine.ui.MessageLog;
import com.example.tileengine.engine.world.World;

public final class GameContext {
    private final GameConfig config;
    private final World world;
    private final AssetManager assetManager;
    private final GameEventBus eventBus;
    private final MessageLog messageLog;

    public GameContext(
            GameConfig config,
            World world,
            AssetManager assetManager,
            GameEventBus eventBus,
            MessageLog messageLog
    ) {
        this.config = config;
        this.world = world;
        this.assetManager = assetManager;
        this.eventBus = eventBus;
        this.messageLog = messageLog;
    }

    public GameConfig config() {
        return config;
    }

    public World world() {
        return world;
    }

    public AssetManager assetManager() {
        return assetManager;
    }

    public GameEventBus eventBus() {
        return eventBus;
    }

    public MessageLog messageLog() {
        return messageLog;
    }
}
