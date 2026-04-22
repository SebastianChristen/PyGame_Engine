package com.example.tileengine.engine.ui;

import com.example.tileengine.engine.core.GameContext;
import com.example.tileengine.engine.render.GameRenderer;

import javax.swing.JPanel;
import java.awt.Dimension;
import java.awt.Graphics;

public final class GamePanel extends JPanel {
    private final GameContext context;
    private final GameRenderer renderer;

    public GamePanel(GameContext context, GameRenderer renderer) {
        this.context = context;
        this.renderer = renderer;
        setPreferredSize(new Dimension(context.config().windowWidth(), context.config().windowHeight()));
        setFocusable(true);
        setDoubleBuffered(true);
    }

    @Override
    protected void paintComponent(Graphics graphics) {
        super.paintComponent(graphics);
        renderer.render(context, graphics);
    }
}
