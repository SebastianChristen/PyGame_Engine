package com.example.tileengine.engine.systems;

import com.example.tileengine.engine.core.GameContext;
import com.example.tileengine.engine.core.GameModule;
import com.example.tileengine.engine.input.InputCommand;
import com.example.tileengine.engine.input.InputState;
import com.example.tileengine.engine.world.Direction;

public final class InputProcessingModule implements GameModule {
    private final InputState inputState;
    private final MovementSystem movementSystem;
    private final InteractionSystem interactionSystem;

    public InputProcessingModule(InputState inputState, MovementSystem movementSystem, InteractionSystem interactionSystem) {
        this.inputState = inputState;
        this.movementSystem = movementSystem;
        this.interactionSystem = interactionSystem;
    }

    @Override
    public void initialize(GameContext context) {
        context.messageLog().push("Use WASD to move, E to pick up, TAB for inventory, SPACE for room text.");
    }

    @Override
    public void update(GameContext context, double deltaTimeSeconds) {
        for (InputCommand command : inputState.drain()) {
            switch (command) {
                case MOVE_UP -> movementSystem.move(context, Direction.UP);
                case MOVE_DOWN -> movementSystem.move(context, Direction.DOWN);
                case MOVE_LEFT -> movementSystem.move(context, Direction.LEFT);
                case MOVE_RIGHT -> movementSystem.move(context, Direction.RIGHT);
                case INTERACT -> interactionSystem.collectItemAtPlayerPosition(context);
                case SHOW_INVENTORY -> interactionSystem.showInventory(context);
                case SHOW_ROOM_DESCRIPTION -> context.messageLog().push(context.world().currentRoom().describe(context.world()));
            }
        }
    }
}
