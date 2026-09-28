# Bekannte Probleme & Platzhalter

Format: **[Bereich] Beschreibung** – Auswirkung – geplante Lösung (Meilenstein).

## Offen

- **[Grafik] Platzhalter-Grastile** (`assets/tilesets/mooswiesen/placeholder_grass.png`): wirkt beim
  Kacheln diagonal gemustert. – Nur Testszene. – Ersetzt durch echtes Mooswiesen-Tileset mit
  Varianten und Autotiling (M2).
- **[UI] Nur eine Schriftgröße**: Glimmer (12 px Zeilenhöhe). Überschriften- und
  Barrierefreiheits-Variante fehlen noch. – Keine. – M2 (HUD/Menüs) bzw. M6 (Barrierefreiheit).
- **[Eingabe] Glyphen als Text**: `InputGlyphs` liefert Tastenbezeichnungen als Text statt als
  Pixel-Icons. – Hinweise sind lesbar, aber nicht hübsch. – Glyphen-Sprites (M2).
- **[Eingabe] Keine Belegungs-UI**: Umbelegen geht bisher nur per `Settings.rebind()` im Code. – M2 (Einstellungsmenü).
- **[Audio] Keine Audio-Assets**: AudioManager und Bus-Layout existieren, aber noch keine Sounds/Musik. – M1 (erste SFX), M2 (Musik).
- **[Szenen] SceneRouter-Blende** ist eine einfache Farbblende; der Feenstaub-Wipe-Shader folgt in M2.
- **[Dialog] DialogueManager ist ein Gerüst** (Laden, Bedingungen, Zeilenfolge, Zeitpause); Auswahlmöglichkeiten,
  Tippgeräusche und die Dialogbox folgen in M4.
- **[Build] Erster Godot-Import eines frischen Klons** meldet einmalig, dass das Projekt-Theme die Schrift
  nicht laden kann (Theme wird vor dem Import der Schrift geladen). Ab dem zweiten Start ist alles sauber;
  `run_all_checks` importiert deshalb zweimal und wertet nur den zweiten Lauf aus.
- **[Build] rcedit wird für Icon/Versionsinfo der Windows-Exe benötigt** (Godot 4.4). Ohne rcedit
  exportiert Godot mit Warnung und Standard-Icon. Unter Linux nur mit Wine und UTF-8-Locale korrekt.
- **[Umgebung] Windows-Build wurde unter Wine getestet**, nicht auf echtem Windows 11. Bitte einmal auf
  echter Hardware starten (siehe „Bitte testen“ im M0-Bericht).

## Erledigt

(noch nichts)
