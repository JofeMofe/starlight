# Bekannte Probleme & Platzhalter

Format: **[Bereich] Beschreibung** – Auswirkung – geplante Lösung (Meilenstein).

## Offen

### Aus M1
- **[Grafik] Klio, Pferd und Hund im Sunnyside-Stil sind eine erste Fassung** (eigene Pixelkarten):
  Signature-Animationen (Brille zurechtschieben, Haare hinters Ohr, Hüpfen), Portraits, Pferde-Idle
  (Grasen, Schweifschlagen, Ohrenspiel) und Hunde-Idle (Kratzen, Gähnen) fehlen noch. – M3/M6.
- **[Grafik] Pferd und Hund nur 4 Richtungen** (8 empfohlen). – M3.
- **[Grafik] Wasser nicht animiert** (Sunnyside hat Glitzer-Sprites, noch nicht eingebaut). – M2.
- **[Grafik] Wo Weg und Wasser direkt aneinanderstoßen**, gewinnt im Dual Grid das Wasser (kleine
  Kerbe im Weg). Karten so gestalten, dass Wege nicht direkt ans Wasser grenzen, oder Steg bauen. – M2.
- **[Build] Sunnyside World muss für einen Neuaufbau der Welt-Grafiken geladen werden**
  (`tools/pipeline/fetch_vendor.py`, Internet nötig). Ohne Netz bleiben die eingecheckten Grafiken gültig.
- **[Recht] Klio ist einer realen Person nachempfunden** (auf Wunsch des Nutzers, nur nach
  Beschreibung): vor einer öffentlichen Veröffentlichung Einverständnis der Person einholen (§5.1).
- **[Audio] Hund- und Pferdelaute sind synthetisch und stilisiert** (Bellen, Schnauben); ich kann sie
  nicht selbst anhören. – Durch CC0-Aufnahmen oder bessere Synthese ersetzen (M3), Nutzer-Feedback erbeten.
- **[Mechanik] Fee sinkt nicht automatisch über hohen Objekten ab** (§6.1): Bäume/Steine blockieren
  die Fee stattdessen einfach. – Prüfen, ob das Absinken spielerisch nötig ist (M2/M6).
- **[Eingabe] Gamepad nicht auf echter Hardware getestet** (Container hat keins). Belegung ist
  vollständig, Analogstick wird stufenlos ausgewertet.
- **[Test] Bildrate im Fenster nicht messbar**: Die Cloud-Maschine rendert per Software (llvmpipe);
  echte FPS: im Spiel F3.
- **[Spec] Interne Auflösung 480 × 270 statt 640 × 360 (§4.1)** – bewusste Abweichung wegen des
  16-px-Sunnyside-Rasters (Figuren sonst zu klein); Integer-Scaling bleibt (1080p = ×4).

### Aus M0

- **[Grafik] Platzhalter-Grastile** (`assets/tilesets/mooswiesen/placeholder_grass.png`) nur noch in
  der M0-Testszene (`scenes/main/m0_test_scene.tscn`, noch für 640 × 360 angelegt).
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
