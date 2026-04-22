package com.example.tileengine.engine.assets;

import javax.imageio.ImageIO;
import java.awt.Color;
import java.awt.Graphics2D;
import java.awt.image.BufferedImage;
import java.io.InputStream;
import java.util.HashMap;
import java.util.Map;

public final class AssetManager {
    private final Map<String, BufferedImage> cache = new HashMap<>();
    private final int tileSize;

    public AssetManager(int tileSize) {
        this.tileSize = tileSize;
    }

    public BufferedImage loadSprite(String path, Color fallbackColor, String label) {
        return cache.computeIfAbsent(path + "|" + fallbackColor.getRGB() + "|" + label, ignored -> loadOrFallback(path, fallbackColor, label));
    }

    private BufferedImage loadOrFallback(String path, Color fallbackColor, String label) {
        if (path != null && !path.isBlank()) {
            try (InputStream inputStream = getClass().getResourceAsStream(path)) {
                if (inputStream != null) {
                    return ImageIO.read(inputStream);
                }
            } catch (Exception ignored) {
                // Fall through to generated placeholder.
            }
        }

        BufferedImage image = new BufferedImage(tileSize, tileSize, BufferedImage.TYPE_INT_ARGB);
        Graphics2D graphics = image.createGraphics();
        graphics.setColor(fallbackColor);
        graphics.fillRect(0, 0, tileSize, tileSize);
        graphics.setColor(Color.BLACK);
        graphics.drawRect(0, 0, tileSize - 1, tileSize - 1);
        graphics.drawString(label, Math.max(4, tileSize / 5), tileSize / 2);
        graphics.dispose();
        return image;
    }
}
