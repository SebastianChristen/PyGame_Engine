package com.example.tileengine.engine.input;

import java.util.EnumSet;
import java.util.Set;

public final class InputState {
    private final Set<InputCommand> queuedCommands = EnumSet.noneOf(InputCommand.class);

    public synchronized void push(InputCommand command) {
        queuedCommands.add(command);
    }

    public synchronized Set<InputCommand> drain() {
        Set<InputCommand> snapshot = EnumSet.copyOf(queuedCommands);
        queuedCommands.clear();
        return snapshot;
    }
}
