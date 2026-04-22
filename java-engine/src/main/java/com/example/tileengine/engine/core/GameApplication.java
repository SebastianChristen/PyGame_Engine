package com.example.tileengine.engine.core;

import javax.swing.JFrame;
import javax.swing.SwingUtilities;

public final class GameApplication {
    private final GameConfig config;
    private final GameInitializer initializer;

    public GameApplication(GameConfig config, GameInitializer initializer) {
        this.config = config;
        this.initializer = initializer;
    }

    public void start() {
        SwingUtilities.invokeLater(() -> {
            GameSession session = initializer.createSession(config);
            JFrame frame = new JFrame(config.title());
            frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
            frame.setResizable(false);
            frame.setContentPane(session.panel());
            frame.pack();
            frame.setLocationRelativeTo(null);
            frame.setVisible(true);

            session.modules().forEach(module -> module.initialize(session.context()));
            session.panel().requestFocusInWindow();

            new GameLoop(config.targetFps(), delta -> {
                session.modules().forEach(module -> module.update(session.context(), delta));
                session.panel().repaint();
            }).start();
        });
    }
}
