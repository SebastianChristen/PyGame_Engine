package com.example.tileengine.engine.render;

import com.example.tileengine.engine.assets.AssetManager;
import com.example.tileengine.engine.core.GameContext;
import com.example.tileengine.engine.entities.ItemEntity;
import com.example.tileengine.engine.entities.PlayerEntity;
import com.example.tileengine.engine.world.Position;
import com.example.tileengine.engine.world.Room;
import com.example.tileengine.engine.world.Tile;

import java.awt.Color;
import java.awt.Font;
import java.awt.Graphics;
import java.awt.Graphics2D;
import java.awt.image.BufferedImage;

public final class GameRenderer {
    private static final Color BACKGROUND = new Color(20, 20, 20);
    private static final Color FLOOR_FALLBACK = new Color(110, 90, 70);
    private static final Color WALL_FALLBACK = new Color(70, 70, 80);
    private static final Color ITEM_FALLBACK = new Color(180, 170, 100);
    private static final Color PLAYER_FALLBACK = new Color(80, 180, 120);

    public void render(GameContext context, Graphics graphics) {
        Graphics2D g2d = (Graphics2D) graphics;
        g2d.setColor(BACKGROUND);
        g2d.fillRect(0, 0, context.config().windowWidth(), context.config().windowHeight());

        Room room = context.world().currentRoom();
        if (room == null) {
            return;
        }

        drawRoom(context, g2d, room);
        drawOverlay(context, g2d, room);
    }

    private void drawRoom(GameContext context, Graphics2D graphics, Room room) {
        AssetManager assets = context.assetManager();
        int tileSize = context.config().tileSize();

        for (int y = 0; y < room.height(); y++) {
            for (int x = 0; x < room.width(); x++) {
                Position position = new Position(x, y);
                Tile tile = room.tileAt(position, context.world().tileRegistry());
                Color tileColor = tile.walkable() ? FLOOR_FALLBACK : WALL_FALLBACK;
                BufferedImage tileSprite = assets.loadSprite(tile.spritePath(), tileColor, String.valueOf(tile.symbol()));
                graphics.drawImage(tileSprite, x * tileSize, y * tileSize, tileSize, tileSize, null);
            }
        }

        for (ItemEntity item : room.items()) {
            BufferedImage itemSprite = assets.loadSprite(item.itemDefinition().spritePath(), ITEM_FALLBACK, "I");
            graphics.drawImage(itemSprite, item.position().x() * tileSize, item.position().y() * tileSize, tileSize, tileSize, null);
        }

        PlayerEntity player = context.world().player();
        BufferedImage playerSprite = assets.loadSprite("/assets/player.png", PLAYER_FALLBACK, "P");
        graphics.drawImage(playerSprite, player.position().x() * tileSize, player.position().y() * tileSize, tileSize, tileSize, null);
    }

    private void drawOverlay(GameContext context, Graphics2D graphics, Room room) {
        int panelWidth = context.config().windowWidth();
        int panelHeight = context.config().windowHeight();
        int overlayHeight = 180;
        int yStart = panelHeight - overlayHeight;

        graphics.setColor(new Color(0, 0, 0, 180));
        graphics.fillRect(0, yStart, panelWidth, overlayHeight);

        graphics.setColor(Color.WHITE);
        graphics.setFont(new Font(Font.MONOSPACED, Font.BOLD, 16));
        graphics.drawString(room.name(), 16, yStart + 24);

        graphics.setFont(new Font(Font.MONOSPACED, Font.PLAIN, 14));
        graphics.drawString(room.describe(context.world()), 16, yStart + 48);

        String inventoryText = context.world().player().inventory().isEmpty()
                ? "Inventory: empty"
                : "Inventory: " + context.world().player().inventory().items().stream()
                    .map(item -> item.displayName())
                    .reduce((left, right) -> left + ", " + right)
                    .orElse("empty");
        graphics.drawString(inventoryText, 16, yStart + 74);

        int offsetY = yStart + 102;
        for (String message : context.messageLog().messages()) {
            graphics.drawString("- " + message, 16, offsetY);
            offsetY += 18;
        }
    }
}
