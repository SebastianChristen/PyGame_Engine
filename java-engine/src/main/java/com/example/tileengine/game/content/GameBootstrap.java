package com.example.tileengine.game.content;

import com.example.tileengine.engine.assets.AssetManager;
import com.example.tileengine.engine.core.GameConfig;
import com.example.tileengine.engine.core.GameContext;
import com.example.tileengine.engine.core.GameInitializer;
import com.example.tileengine.engine.core.GameModule;
import com.example.tileengine.engine.core.GameSession;
import com.example.tileengine.engine.entities.ItemEntity;
import com.example.tileengine.engine.entities.PlayerEntity;
import com.example.tileengine.engine.events.GameEventBus;
import com.example.tileengine.engine.input.InputState;
import com.example.tileengine.engine.input.KeyboardController;
import com.example.tileengine.engine.render.GameRenderer;
import com.example.tileengine.engine.systems.InputProcessingModule;
import com.example.tileengine.engine.systems.InteractionSystem;
import com.example.tileengine.engine.systems.MovementSystem;
import com.example.tileengine.engine.ui.GamePanel;
import com.example.tileengine.engine.ui.MessageLog;
import com.example.tileengine.engine.world.Position;
import com.example.tileengine.engine.world.Room;
import com.example.tileengine.engine.world.TileRegistry;
import com.example.tileengine.engine.world.World;
import com.example.tileengine.game.rules.StoneCollapseRule;

import java.util.List;

public final class GameBootstrap implements GameInitializer {
    private GameBootstrap() {}

    public static GameBootstrap create() {
        return new GameBootstrap();
    }

    @Override
    public GameSession createSession(GameConfig config) {
        TileRegistry registry = DefaultTiles.createRegistry();
        World world = new World(registry);

        Room whiteHouse = DefaultRooms.createWhiteHouse();
        whiteHouse.addItem(new ItemEntity(new Position(4, 3), DefaultItems.createStone()));
        world.addRoom(whiteHouse);
        world.setCurrentRoom(whiteHouse.id());

        PlayerEntity player = new PlayerEntity(new Position(1, 1));
        world.setPlayer(player);

        AssetManager assetManager = new AssetManager(config.tileSize());
        GameEventBus eventBus = new GameEventBus();
        MessageLog messageLog = new MessageLog(4);
        GameContext context = new GameContext(config, world, assetManager, eventBus, messageLog);

        new StoneCollapseRule().register(context);

        InputState inputState = new InputState();
        GamePanel panel = new GamePanel(context, new GameRenderer());
        new KeyboardController(inputState).bind(panel);

        List<GameModule> modules = List.of(
                new InputProcessingModule(inputState, new MovementSystem(), new InteractionSystem())
        );

        return new GameSession(context, modules, panel);
    }
}
