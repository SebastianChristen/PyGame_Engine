package com.example.tileengine.engine.world;

import com.example.tileengine.engine.entities.PlayerEntity;

import java.util.HashMap;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;

public final class World {
    private final TileRegistry tileRegistry;
    private final Map<String, Room> roomsById = new HashMap<>();
    private final Set<WorldFlag> flags = new HashSet<>();
    private PlayerEntity player;
    private String currentRoomId;

    public World(TileRegistry tileRegistry) {
        this.tileRegistry = tileRegistry;
    }

    public void addRoom(Room room) {
        roomsById.put(room.id(), room);
    }

    public TileRegistry tileRegistry() {
        return tileRegistry;
    }

    public Room currentRoom() {
        return roomsById.get(currentRoomId);
    }

    public void setCurrentRoom(String roomId) {
        if (!roomsById.containsKey(roomId)) {
            throw new IllegalArgumentException("Unknown room id: " + roomId);
        }
        currentRoomId = roomId;
    }

    public PlayerEntity player() {
        return player;
    }

    public void setPlayer(PlayerEntity player) {
        this.player = player;
    }

    public void setFlag(WorldFlag flag) {
        flags.add(flag);
    }

    public boolean hasFlag(WorldFlag flag) {
        return flags.contains(flag);
    }
}
