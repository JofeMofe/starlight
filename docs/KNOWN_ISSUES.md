# Bekannte Probleme & Platzhalter

Format: **[Bereich] Beschreibung** – Auswirkung – geplante Lösung (Meilenstein).

## Offen

### Aus M1
- **[Grafik] Klio basiert auf LPC-Vorlagen**: Stil der Vorlagen, noch ohne Signature-Animationen
  (Brille zurechtschieben, Haare hinters Ohr, Hüpfen), ohne Portraits und ohne Blinzeln; die Brille
  ist rundlich statt eckig. Reiten nutzt die LPC-Sitzpose (Beine nach vorn), nicht eine echte
  Reitpose. – LPC-Reitposen (opengameart.org, derzeit gesperrt) bzw. eigene Frames, M3/M6.
- **[Netzwerk] opengameart.org, itch.io, kenney.nl gesperrt** (Umgebungsrichtlinie). Der Hund
  bleibt Eigenbau, bis LPC-Hunde geladen werden können. – Nutzer um Freigabe gebeten.
- **[Grafik] Zaun** ist noch Eigenbau und passt stilistisch nicht ganz zur LPC-Welt. – LPC-Zaun
  (ElizaWy `Structure/Fences`) einbauen.
- **[Recht] Klio ist einer realen Person nachempfunden** (auf Wunsch des Nutzers, nur nach
  Beschreibung): vor einer öffentlichen Veröffentlichung Einverständnis der Person einholen (§5.1).
- **[Grafik] Hund wirkt unbeholfen** (Nutzer-Feedback „derpy“). – Ersatz durch LPC-Hund, sobald
  opengameart.org erreichbar ist.
- **[Grafik] Pferd und Hund nur 4 Richtungen** (8 empfohlen), Pferd ohne Idle-Varianten (Grasen,
  Wälzen …), Hund ohne Kratzen/Gähnen/Schmetterlinge. – M3.
- **[Grafik] Wasser nicht animiert** (Ufer sind seit Sitzung 5 rund, Dual Grid). – M2.
- **[Audio] Hund- und Pferdelaute sind synthetisch und stilisiert** (Bellen, Schnauben); ich kann sie
  nicht selbst anhören. – Durch CC0-Aufnahmen oder bessere Synthese ersetzen (M3), Nutzer-Feedback erbeten.
- **[Mechanik] Fee sinkt nicht automatisch über hohen Objekten ab** (§6.1): Bäume/Steine blockieren
  die Fee stattdessen einfach. – Prüfen, ob das Absinken spielerisch nötig ist (M2/M6).
- **[Mechanik] Reiten in der Ansicht von vorn**: Klio sitzt hinter dem Pferdekopf, der Oberkörper
  ragt darüber – bewusst so, wirkt aber noch nicht ganz stimmig. – Eigene Reiter-Frames in M3.
- **[Eingabe] Gamepad nicht auf echter Hardware getestet** (Container hat keins). Belegung ist
  vollständig, Analogstick wird stufenlos ausgewertet.
- **[Test] Bildrate im Fenster nicht messbar**: Die Cloud-Maschine rendert per Software (llvmpipe);
  gemessen wurde die Spiel-Logik headless (Ø 2,7 ms). Echte FPS: im Spiel F3.

### Aus M0

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

## Erledigt

- **[Umgebung] Windows-Build nur unter Wine getestet** – 2026-09-28 im Nutzertest auf echtem
  Windows bestätigt: Start, Schärfe, Sprachwechsel (F2), Integer-Skalierung im maximierten Fenster,
  Screenshot (F12) und Programm-Infos funktionieren.
