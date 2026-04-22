# Modular Tile Engine (Java)

Dieses Projekt ist eine saubere Neuarchitektur des Python-Prototyps als modulares Java-Projekt.

## Starten

```bash
./run.sh
```

## Bauen

```bash
./build.sh
```

Die kompilierten Klassen landen in `out/`.

## Steuerung

- `WASD`: Bewegung
- `E`: Item aufnehmen
- `TAB`: Inventar anzeigen
- `SPACE`: Raum-Beschreibung erneut anzeigen

## Architektur

- `engine.core`: Anwendung, Game Loop, Context, Modul-Schnittstellen
- `engine.world`: Welt, Räume, Tiles, Positionen, Flags
- `engine.entities`: Spieler, Items, Inventar, Basisklassen
- `engine.items`: Item-Definitionen
- `engine.systems`: Bewegung, Interaktion, Input-Verarbeitung
- `engine.events`: Event-Bus für lose Kopplung
- `engine.render`: Rendering
- `engine.assets`: Laden von Sprites mit Fallback-Platzhaltern
- `engine.ui`: Panel und Message Log
- `game.content`: konkrete Spielinhalte
- `game.rules`: spiel-spezifische Regeln, die auf Events reagieren

## Wichtige Verbesserungen gegenüber dem Prototypen

1. Kein globaler `game`-Singleton mehr. Zustand steckt im `GameContext` und in `World`.
2. Keine Vermischung von Engine und Spielinhalt. Die Engine kennt nur generische Systeme, Tiles, Räume, Events usw.
3. Spielregeln sind event-getrieben. Beispiel: `StoneCollapseRule` reagiert auf `ItemCollectedEvent`.
4. Rendering hängt nicht an Dateien. Fehlende Assets werden automatisch durch Platzhalter ersetzt.
5. Keine Monolith-Datei. Stattdessen klare Packages mit Verantwortlichkeiten.
6. Raum-Beschreibungen sind Strategien statt harter Vererbung. Das ist flexibler als spezielle `WhiteHouse`-Klassen.
7. Items im Raum sind Entities mit Definitionen. Das lässt sich später auf NPCs, Türen, Trigger, Container usw. erweitern.
8. Input ist als Command-Queue modelliert und kann später durch Gamepad, AI oder Netzwerkinput ersetzt werden.

## Sinnvolle nächste Ausbaustufen

- Raumwechsel/Portale
- NPCs und Dialogsystem
- Datengetriebene Inhalte (JSON/YAML)
- Save/Load-System
- Animationen
- Kollisionslayer / Triggerzonen
- Sound-System
- Quest-/Skript-System
- ECS oder komponentenbasierte Entities für komplexere Spiele
