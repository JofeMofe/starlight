# Starlight – Klio goes Fairy · Game Design Document (lebend)

> Verbindliche Vision: `CLAUDE.md` (= AGENTS.md). Dieses Dokument hält fest, **was tatsächlich
> umgesetzt ist** und welche Designentscheidungen dabei getroffen wurden. Status-Markierungen:
> ✅ umgesetzt & verifiziert · 🟡 Gerüst/teilweise · ⬜ geplant.

## 1. Spielfantasie

„Ich bin Klio. Ich werde über Nacht zur Fee, finde in einem verschlafenen Tal ein neues Zuhause,
schenke vernachlässigten Tieren Liebe und bringe so die Magie des Tals zurück.“

Cozy-Prinzipien: kein Tod, keine Kämpfe, kein Game Over, kein FOMO, Feenglanz begrenzt sanft.

## 2. Heldin: Klio 🟡 (M1 Prototyp ✅, Endqualität M6)

Feste Hauptfigur, keine Charaktererstellung. Lange braune Haare, Brille in jeder Darstellung,
Feenflügel nach der Verwandlung. Garderobe statt Editor. Details: CLAUDE.md §5.1.

**M1-Stand:** Menschengröße 32×48 in 3 Ansichten (rechts = gespiegelt): Stehen (6 Frames: Atmen,
Blinzeln), Laufen (8 Frames, Körper federt 1 px), Reitpose. Lange Haare als eigene Ebene mit
5 Schwungstufen, gesteuert von einer gedämpften Feder (Steifigkeit 90, Dämpfung 9): Sie wehen
beim Laufen nach hinten und schwingen beim Anhalten nach. Brille auch von hinten (Bügel) und im
Profil sichtbar. Feengröße 16×20 mit 1-px-Brille + Glanzpunkt, Blütenkranz, Sternenlicht-Kleid,
Flügel als eigene Ebene (6-Frame-Schleife mit schnellem Abschlag: 70/40/50/70/60/60 ms).
Offen bis M6: Signature-Animationen (Brille zurechtschieben, Haare hinters Ohr …), Portraits, Endqualität.

## 2a. Größenwandel ✅ (M1)

| Regel | Wert |
|---|---|
| Kapitel 1 | nur an Feenringen |
| ab Kapitel 2 | überall, 5 Feenglanz (am Feenring immer gratis) |
| ab Kapitel 4 | überall gratis |
| Dauer | 0,4 s; Gestaltwechsel bei 0,2 s |
| Rückmeldung | Flackern zwischen beiden Gestalten (0,08–0,32 s, alle 40 ms), Lichtblitz (Maximum bei 0,2 s), 26 Funken im Wirbel (Orbit-Geschwindigkeit), „Pling“-Arpeggio (zur Fee aufwärts und hoch, zum Menschen abwärts und tief), Kamera-Puls 1 px |
| Kein Platz für Menschengröße | Verwandlung abgelehnt: Wackeln (±1 px, 0,3 s), gedämpftes „Boing“, Hinweis |

Der Test-Prototyp (Wiese) startet in Kapitel 2, damit man überall probieren kann.
**Abweichung von §6.3:** Statt eines echten Kamera-Zooms (nicht-ganzzahliger Zoom erzeugt
Mixels, verboten nach §8.4) gibt es einen 1-px-Kamerastoß plus Lichtblitz. Mit
„Bildschirmwackeln aus“ entfällt der Stoß.

## 2b. Bewegung & Gefühl ✅ (M1) – Werte in `data/config/movement.tres`

| | Tempo | Anfahren | Bremsen | Besonderheit |
|---|---|---|---|---|
| Klio Mensch | 82 px/s (2,6 Kacheln/s) | 760 px/s² → volle Fahrt in 0,11 s | 1050 px/s² → Stand in 0,08 s | direkt, kein Rutschen |
| Fee schwebend | 70 px/s | 430 px/s² (0,16 s) | 520 px/s² | weiches Gleiten, Schweben ±1,5 px mit 1,1 Hz |
| Fee fliegend (Leertaste halten) | 98 px/s | dito | dito | steigt 10 px, ignoriert Zäune/Büsche/Wasser; Flugkraft −32/s, +55/s nach 0,35 s Pause; über Hindernis leer → schwebt weiter bis freier Boden (nie Absturz) |
| Hund folgt | 62 px/s, ab 90 px Abstand 128 px/s | 600 px/s² | | Abstand 30 px, setzt sich nach 2,5 s |
| Hund geritten (Fee) | 150 px/s | 820 px/s² | | schneller als die fliegende Fee |
| Pferd Schritt / Trab / Galopp | 52 / 108 / 172 px/s | 170 px/s² (träge, schwer) | 230 px/s² | Wendigkeit 420 / 230 / 150 °/s → Galopp braucht Wendekreis |
| Pferdesprung | 0,46 s, 11 px hoch | | | nur aus vollem Galopp, nur wenn die Landestelle frei ist (sonst schnaubt es und bleibt) |

Kamera: pixelfest auf Klio, weicher Vorausblick in Laufrichtung (max. 22 px, gleitet mit
Rate 2,6/s nach), 18 px über den Füßen. Physik-Interpolation für Monitore mit mehr als 60 Hz.

## 3. Zeit & Kalender ✅ (Logik, M0)

| Regel | Wert | Quelle |
|---|---|---|
| Tagesablauf | 06:00 – 02:00 | `data/config/time.tres` |
| Echtzeit pro Tag | 14 min (0,7 s pro Spielminute) | dito |
| Einschlafen um 02:00 | ohne Strafe; Aufwachen 07:00, 80 % Feenglanz | `passout_wake_minute`, `passout_glow_ratio` |
| Entspannter Modus | Zeit × 0,5 bzw. Pause in Innenräumen | `relaxed_mode_factor`, Einstellungen |
| Jahreszeiten | 4 × 28 Tage | |
| Woche | 7 Tage, Tag 1 = Montag | |
| Mondphasen | 8 Phasen, Längen 1/6/1/6/1/6/1/6 Tage | eine Vollmondnacht je Jahreszeit (Tag 15) = Maestro-Moon-Nacht |

Designentscheidung Mond: Mit gleich langen Phasen (3,5 Tage) gäbe es mehrere „Vollmondtage“; die
Hauptphasen (Neu-, Voll-, Viertelmonde) dauern deshalb genau einen Tag, die Zwischenphasen sechs.
So ist die Vollmondnacht ein klares, planbares Ereignis.

## 4. Wetter ✅ (Logik, M0) · Darstellung ⬜ (M2)

Typen: sonnig, bewölkt, Regen, Gewitter, Nebel, Wind, Schnee (nur Winter), Sternschnuppennacht (selten).
Gewichte pro Jahreszeit in `data/config/weather.json`; erster Tag jeder Jahreszeit immer sonnig.
Wetter ist deterministisch aus Welt-Seed + Tag → 3-Tage-Vorschau stimmt immer.

## 5. Speichern ✅ (M0)

3 Slots + Autosave beim Schlafengehen, JSON mit Versionsfeld und Migrationen, atomisches Schreiben
mit Backup. Meta (Name, Hof, Tag, Jahreszeit, Spielzeit) und Thumbnail (160 × 90) je Slot.

## 6. Steuerung ✅ (Belegung, M0)

| Aktion | Tastatur/Maus | Gamepad (Xbox-Bezeichnung) |
|---|---|---|
| Bewegen | WASD / Pfeiltasten | linker Stick / Steuerkreuz |
| Interagieren (Streicheln, Hund aufsitzen, Absteigen, am Feenring verwandeln) | E / rechte Maustaste | A |
| Pferd aufsteigen (wenn der Hinweis erscheint) · beim Reiten schneller · im Galopp springen | Leertaste | B |
| Hilfe ein/aus · Bildrate | F1 · F3 | – |
| Werkzeug benutzen | linke Maustaste / C | RB |
| Größe wechseln | Q | Y |
| Fliegen / Springen / Galopp | Leertaste | B |
| Inventar | Tab / I | Menu (Start) |
| Pause | Esc | View (Back) |
| Hund rufen | F | X |
| Pferd pfeifen | R | LB |
| Werkzeugleiste | 1–0, Mausrad | LT / RT |
| Fotomodus | P | – |

Frei belegbar über `Settings.rebind()` (UI folgt in M2).

## 7. Weitere Systeme

**Hund (M1-Prototyp ✅):** Border-Collie-Mix „Funke“ folgt per Navigation (läuft um Zäune herum,
durchs Tor), setzt sich, kommt auf Zuruf (F) mit Bellen, lässt sich streicheln (Herzchen), trägt
die Fee. Rassen, Werte, Fähigkeiten: M3.

**Pferd (M1-Prototyp ✅):** Fuchs „Holunder“ mit Flachsmähne und Blesse. Streicheln (Schnauben,
Herzchen), Pfiff (R) → trabt per Navigation herbei, Reiten wie oben. Hufschlag synchron zum
Gangbild (Schritt 4 Schläge, Trab 2, Galopp 3). Pflege, Werte, Genetik: M3.

Dorf, Garten, Tränke, Maestro Moon, Rhythmus-Minispiel, Feste, Sternenbuch, Fotomodus: ⬜ – laut
Meilensteinplan (CLAUDE.md §14).
