package com.example.tileengine.app;

import com.example.tileengine.engine.core.GameApplication;
import com.example.tileengine.engine.core.GameConfig;
import com.example.tileengine.game.content.GameBootstrap;

public final class Main {
    private Main() {}

    public static void main(String[] args) {
        GameConfig config = new GameConfig(
                "Modular Tile Engine",
                48,
                60,
                960,
                720
        );

        GameApplication application = new GameApplication(config, GameBootstrap.create());
        application.start();
    }
}
