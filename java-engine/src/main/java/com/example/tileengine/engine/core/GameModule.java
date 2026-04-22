package com.example.tileengine.engine.core;

public interface GameModule {
    void initialize(GameContext context);
    void update(GameContext context, double deltaTimeSeconds);
}
