"""Lädt Fremd-Pakete, die nicht ins (öffentliche) Repository dürfen, nach vendor/.

Sunnyside World (Daniel Diggle) ist kostenlos, auch kommerziell nutzbar, darf aber
nicht als Paket weiterverbreitet werden. Deshalb liegen im Repository nur die
daraus zugeschnittenen Spielgrafiken; die Quelle lädt dieses Skript bei Bedarf
direkt von itch.io (kostenloser Download, kein Konto nötig).

Aufruf: python tools/pipeline/fetch_vendor.py
"""
from __future__ import annotations

import http.cookiejar
import io
import json
import re
import sys
import urllib.parse
import urllib.request
import zipfile
from pathlib import Path

VENDOR = Path(__file__).resolve().parent / "vendor"
PACKS = {
    "sunnyside": ("https://danieldiggle.itch.io/sunnyside", "Sunnyside_World_ASSET_PACK_V2.1.zip"),
}
UA = {"User-Agent": "Mozilla/5.0 (Starlight asset fetch)"}


def _opener() -> urllib.request.OpenerDirector:
    return urllib.request.build_opener(urllib.request.HTTPCookieProcessor(http.cookiejar.CookieJar()))


def _get(op: urllib.request.OpenerDirector, url: str) -> bytes:
    with op.open(urllib.request.Request(url, headers=UA), timeout=120) as r:
        return r.read()


def _post_json(op: urllib.request.OpenerDirector, url: str, data: dict[str, str]) -> dict:
    body = urllib.parse.urlencode(data).encode()
    req = urllib.request.Request(url, data=body, headers={**UA, "X-Requested-With": "XMLHttpRequest"})
    with op.open(req, timeout=120) as r:
        return json.loads(r.read().decode())


def _csrf(html: str) -> str:
    m = re.search(r'name="csrf_token" value="([^"]+)"', html)
    return m.group(1) if m else ""


def fetch_itch(game_url: str, file_name: str) -> bytes:
    """Kostenloser itch.io-Download (Preis 0) ohne Konto."""
    op = _opener()
    page = _get(op, game_url).decode("utf-8", "replace")
    token = _csrf(page)
    dl = _post_json(op, game_url.rstrip("/") + "/download_url", {"csrf_token": token})["url"]
    dpage = _get(op, dl).decode("utf-8", "replace")
    token = _csrf(dpage) or token
    for uid, name in re.findall(r'data-upload_id="(\d+)".*?<strong title="([^"]+)" class="name"', dpage, re.S):
        if name == file_name:
            url = _post_json(op, f"{game_url.rstrip('/')}/file/{uid}?source=game_download",
                             {"csrf_token": token})["url"]
            return _get(op, url)
    raise RuntimeError(f"{file_name} nicht auf {game_url} gefunden")


def ensure(name: str) -> Path:
    """Stellt sicher, dass vendor/<name> vorhanden ist, und gibt den Pfad zurück."""
    target = VENDOR / name
    if target.exists() and any(target.iterdir()):
        return target
    url, file_name = PACKS[name]
    print(f"Lade {file_name} von {url} …")
    data = fetch_itch(url, file_name)
    target.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(io.BytesIO(data)) as z:
        for info in z.infolist():
            if info.filename.startswith("__MACOSX") or info.is_dir():
                continue
            out = target / info.filename
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(z.read(info))
    return target


def main() -> int:
    for name in PACKS:
        print(f"{name}: {ensure(name)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
