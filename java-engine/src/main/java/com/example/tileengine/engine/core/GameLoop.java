package com.example.tileengine.engine.core;

import java.util.function.DoubleConsumer;

public final class GameLoop {
    private final int targetFps;
    private final DoubleConsumer updateCallback;

    public GameLoop(int targetFps, DoubleConsumer updateCallback) {
        this.targetFps = targetFps;
        this.updateCallback = updateCallback;
    }

    public void start() {
        Thread loopThread = new Thread(this::runLoop, "game-loop");
        loopThread.setDaemon(true);
        loopThread.start();
    }

    private void runLoop() {
        long previousTime = System.nanoTime();
        long frameDurationNanos = 1_000_000_000L / Math.max(targetFps, 1);

        while (true) {
            long now = System.nanoTime();
            double deltaSeconds = (now - previousTime) / 1_000_000_000.0;
            previousTime = now;

            updateCallback.accept(deltaSeconds);

            long elapsed = System.nanoTime() - now;
            long sleepNanos = frameDurationNanos - elapsed;
            if (sleepNanos > 0) {
                try {
                    Thread.sleep(sleepNanos / 1_000_000L, (int) (sleepNanos % 1_000_000L));
                } catch (InterruptedException interruptedException) {
                    Thread.currentThread().interrupt();
                    return;
                }
            }
        }
    }
}
