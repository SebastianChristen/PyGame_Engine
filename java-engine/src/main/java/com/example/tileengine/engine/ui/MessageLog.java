package com.example.tileengine.engine.ui;

import java.util.ArrayDeque;
import java.util.Deque;
import java.util.List;

public final class MessageLog {
    private final Deque<String> messages = new ArrayDeque<>();
    private final int maxEntries;

    public MessageLog(int maxEntries) {
        this.maxEntries = maxEntries;
    }

    public void push(String message) {
        messages.addFirst(message);
        while (messages.size() > maxEntries) {
            messages.removeLast();
        }
    }

    public List<String> messages() {
        return List.copyOf(messages);
    }
}
