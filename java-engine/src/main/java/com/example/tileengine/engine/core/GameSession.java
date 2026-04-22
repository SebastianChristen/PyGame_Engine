package com.example.tileengine.engine.core;

import com.example.tileengine.engine.ui.GamePanel;

import java.util.List;

public record GameSession(
        GameContext context,
        List<GameModule> modules,
        GamePanel panel
) {
}
