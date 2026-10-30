#!/usr/bin/env python3
"""Fetch 21 game artwork assets and make consistent, uncropped WebP catalogue covers.

The artwork remains copyright of its respective game publisher/rightsholder.
Source URLs are documented in IMAGE-SOURCES.md. This import process does not
grant or imply redistribution permission.
"""
from __future__ import annotations

from io import BytesIO
from pathlib import Path
from urllib.request import Request, urlopen

from PIL import Image, ImageEnhance, ImageFilter, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "static" / "images" / "slots"
CANVAS = (1440, 810)
ART_MAX = (1180, 690)

SOURCES = {
    "catalog-starburst.webp": (
        "https://media.slotboss.co.uk/images/games/starburst/starburst-square.jpg",
        "https://www.slotboss.co.uk/games/starburst",
    ),
    "catalog-the-dog-house.webp": (
        "https://media.leovegas.com/lv/games/54EAb9QDp/ZX4mytrgJGKREL.jpg",
        "https://www.leovegas.com/en-ca/game/the-dog-house",
    ),
    "catalog-legacy-of-dead.webp": (
        "https://media.betmgm.co.uk/images/games/legacy-of-dead/legacy-of-dead-square.jpg",
        "https://www.betmgm.co.uk/games/providers/pragmatic-play",
    ),
    "catalog-reactoonz.webp": (
        "https://media.leovegas.com/images/games/reactoonz/reactoonz-icon.jpg",
        "https://www.leovegas.es/juegos/reactoonz",
    ),
    "catalog-wild-west-gold.webp": (
        "https://content.hollywoodbets.net/Wild_West_Gold_1000x600_e6b82dca9e.webp",
        "https://www.hollywoodbets.net/gaming/games/wild-west-gold",
    ),
    "catalog-starlight-princess.webp": (
        "https://monkeytilt.com/images/media/images/games/pgp_starlightprincess.png?f=webp&q=60&w=400",
        "https://monkeytilt.com/casino/game/starlight-princess/",
    ),
    "catalog-buffalo-king-megaways.webp": (
        "https://assets.rizk.com/cdn-cgi/image/format%3Dauto%2Cwidth%3Dauto%2Cheight%3Dauto%2Cquality%3D85%2Cfit%3Dcover/game-assets/desktop-original/22173.jpg",
        "https://rizk.com/ca/casino/buffalo-king-megaways/22173",
    ),
    "catalog-mega-fortune.webp": (
        "https://www.usgamblingsites.com/wp-content/uploads/2019/08/mega-fortune-logo-1024x576.jpg",
        "https://www.usgamblingsites.com/news/mega-fortune-a-review-of-netents-classic/",
    ),
    "catalog-dead-or-alive-2.webp": (
        "https://mediumrare.imgix.net/936b5873cf4399122da17b8bb38ad9b0b0cdc9a6398f11e945c2607ea3a54949?q=85",
        "https://stake.com/casino/games/netent-dead-or-alive-2",
    ),
    "catalog-twin-spin.webp": (
        "https://mediumrare.imgix.net/d69d54006a897482b44b1bca4fbb2e10a686a15022f3732f4e70fb8260a2ea76",
        "https://stake.com/casino/games/netent-twin-spin",
    ),
    "catalog-hand-of-anubis.webp": (
        "https://img.mrq.com/flicker-test/sharing_graphic_hand_of_anubis_5b06d9fc72.jpg",
        "https://mrq.com/slots-and-games/hand-of-anubis",
    ),
    "catalog-sugar-rush.webp": (
        "https://aws.die-spielbank.de/sachsen/images/en/sugar-rush_die-spielbank_600x600.webp",
        "https://www.die-spielbank.de/de/slots/sugar-rush",
    ),
    "catalog-immortal-romance.webp": (
        "https://cdn.quigioco.it/external_cms/QUIGIOCO/newsite/MICROGAMING/17190.jpg",
        "https://www.quigioco.it/slot-casino/immortal-romance",
    ),
    "catalog-5-lions-megaways.webp": (
        "https://storage.googleapis.com/kickthe/assets/images/games/5-lions-megaways-pragmaticplay/gb/gbp/tile_large.jpg",
        "https://lottomart.com/en-gb/games/5-lions-megaways",
    ),
    "catalog-le-bandit.webp": (
        "https://media.leovegas.com/images/games/le-bandit/le-bandit-tile.jpg?tr=w-1920",
        "https://www.leovegas.nl/game/le-bandit",
    ),
    "catalog-wanted-dead-or-a-wild.webp": (
        "https://img.netbet.com.mx/gms/games/mobile_casino_new/preview/18313-wanted-dead-or-a-wild.jpg",
        "https://casino.netbet.com.mx/game/wanted-dead-or-a-wild",
    ),
    "catalog-money-train-3.webp": (
        "https://media.royalpanda.com/images/games/money-train-3/money-train-3-square.jpg",
        "https://www.royalpanda.com/en-ca/game/money-train-3",
    ),
    "catalog-money-train-4.webp": (
        "https://clientarea.relax-gaming.com/gameassets/moneytrain4/thumbnail2x/7cUSU32cCdZNPZNmFuBC/Thumbnail_MoneyTrain4_600x600.png",
        "https://www.relax-gaming.com/products/casino/moneytrain4",
    ),
    "catalog-thunderstruck-ii.webp": (
        "https://media.pinkcasino.co.uk/images/games/thunderstruck-ii/thunderstruck-ii-square.jpg",
        "https://www.pinkcasino.co.uk/games/thunderstruck-ii",
    ),
    "catalog-fruit-party-2.webp": (
        "https://content.hollywoodbets.net/Fruit_Party_2_1000x600_1_2e62af8a62.webp",
        "https://www.hollywoodbets.net/gaming/games/fruit-party-2",
    ),
    "catalog-gates-of-olympus.webp": (
        "https://assets-ch-itw.kc-usercontent.com/7d02c07e-0e83-3f6f-84b1-2a9fa0e2f51a/8b7c40ef-708c-4894-8c2b-605eeae7c015/gates_of_olympus_slot.png?fm=webp&lossless=false&q=75&w=3840",
        "https://www.interwetten.es/es/blog/pragmatic-play-gates-of-olympus",
    ),
}


def fetch(url: str, source_page: str) -> bytes:
    request = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; InstantCasinoSlotCatalogue/1.0)",
            "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
            "Referer": source_page,
        },
    )
    with urlopen(request, timeout=60) as response:
        content_type = response.headers.get("Content-Type", "")
        data = response.read()
    if not content_type.lower().startswith("image/"):
        raise RuntimeError(f"Expected image from {url}; received {content_type!r}")
    if len(data) < 10_000:
        raise RuntimeError(f"Downloaded file is unexpectedly small ({len(data)} bytes): {url}")
    return data


def compose_without_cropping(source: Image.Image) -> Image.Image:
    source = ImageOps.exif_transpose(source).convert("RGB")
    if source.width < 300 or source.height < 250:
        raise RuntimeError(f"Source is too small: {source.width}x{source.height}")

    background = ImageOps.fit(
        source,
        CANVAS,
        method=Image.Resampling.LANCZOS,
        centering=(0.5, 0.5),
    ).filter(ImageFilter.GaussianBlur(radius=32))
    background = ImageEnhance.Brightness(background).enhance(0.34)

    artwork = ImageOps.contain(source, ART_MAX, method=Image.Resampling.LANCZOS)
    x = (CANVAS[0] - artwork.width) // 2
    y = (CANVAS[1] - artwork.height) // 2
    background.paste(artwork, (x, y))
    return background


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    failures: list[str] = []
    for filename, (url, source_page) in SOURCES.items():
        try:
            raw = fetch(url, source_page)
            with Image.open(BytesIO(raw)) as source:
                image = compose_without_cropping(source)
                target = OUTPUT / filename
                image.save(target, "WEBP", quality=86, method=6)
            print(f"OK {filename}: {target.stat().st_size:,} bytes; source {source_page}")
        except Exception as exc:
            failures.append(f"{filename}: {exc}")
            print(f"FAIL {filename}: {exc}")

    if failures:
        raise RuntimeError("Some source images could not be imported:\n" + "\n".join(failures))


if __name__ == "__main__":
    main()
