# Starlight – Klio goes Fairy · Game Design Document (lebend)

> Verbindliche Vision: `CLAUDE.md` (= AGENTS.md). Dieses Dokument hält fest, **was tatsächlich
> umgesetzt ist** und welche Designentscheidungen dabei getroffen wurden. Status-Markierungen:
> ✅ umgesetzt & verifiziert · 🟡 Gerüst/teilweise · ⬜ geplant.

## 1. Spielfantasie

„Ich bin Klio. Ich werde über Nacht zur Fee, finde in einem verschlafenen Tal ein neues Zuhause,
schenke vernachlässigten Tieren Liebe und bringe so die Magie des Tals zurück.“

Cozy-Prinzipien: kein Tod, keine Kämpfe, kein Game Over, kein FOMO, Feenglanz begrenzt sanft.

## 2. Heldin: Klio ⬜ (M1 Prototyp, M6 Endqualität)

Feste Hauptfigur, keine Charaktererstellung. Lange braune Haare, Brille in jeder Darstellung,
Feenflügel nach der Verwandlung. Garderobe statt Editor. Details: CLAUDE.md §5.1.

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
| Interagieren | E / rechte Maustaste | A |
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

Pferde, Hunde, Größenwandel, Dorf, Garten, Tränke, Maestro Moon, Rhythmus-Minispiel, Feste,
Sternenbuch, Fotomodus: ⬜ – Umsetzung laut Meilensteinplan (CLAUDE.md §14).
