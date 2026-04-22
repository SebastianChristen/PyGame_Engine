package com.example.tileengine.engine.input;

import javax.swing.JComponent;
import javax.swing.KeyStroke;
import java.awt.event.ActionEvent;

public final class KeyboardController {
    private final InputState inputState;

    public KeyboardController(InputState inputState) {
        this.inputState = inputState;
    }

    public void bind(JComponent component) {
        bind(component, "W", InputCommand.MOVE_UP);
        bind(component, "S", InputCommand.MOVE_DOWN);
        bind(component, "A", InputCommand.MOVE_LEFT);
        bind(component, "D", InputCommand.MOVE_RIGHT);
        bind(component, "E", InputCommand.INTERACT);
        bind(component, "TAB", InputCommand.SHOW_INVENTORY);
        bind(component, "SPACE", InputCommand.SHOW_ROOM_DESCRIPTION);
    }

    private void bind(JComponent component, String key, InputCommand command) {
        String actionKey = "action_" + command.name();
        component.getInputMap(JComponent.WHEN_IN_FOCUSED_WINDOW).put(KeyStroke.getKeyStroke(key), actionKey);
        component.getActionMap().put(actionKey, new javax.swing.AbstractAction() {
            @Override
            public void actionPerformed(ActionEvent e) {
                inputState.push(command);
            }
        });
    }
}
