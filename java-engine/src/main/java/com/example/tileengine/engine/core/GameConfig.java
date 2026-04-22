package com.example.tileengine.engine.core;

public record GameConfig(
        String title,
        int tileSize,
        int targetFps,
        int windowWidth,
        int windowHeight
) {
}
