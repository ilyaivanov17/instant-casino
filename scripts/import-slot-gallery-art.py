#!/usr/bin/env python3
"""Download game artwork and create consistent wide WebP covers without cropping the artwork."""
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
    "bigger-bass-bonanza-cover.webp": "https://assets.midnite.com/cms/500x500_29_1a1ea82635.png",
    "bonanza-cover.webp": "https://images.squarespace-cdn.com/content/v1/60aedd95a74c4c4033f9d064/1624241048032-Y1JGMZ3I0U9BM5DBV981/Bonanza_Rectangular_1600x755.jpg",
    "book-of-dead-cover.webp": "https://media.leovegas.com/images/games/book-of-dead/book-of-dead-square.jpg",
    "dragons-luck-cover.webp": "https://media.leovegas.com/images/games/dragons-luck/dragons-luck-tile.jpg",
    "fruit-party-cover.webp": "https://cdn.casinofever.ca/pics/news/fruit-party-pragmatic-play.jpg?auto=format",
}


def download(url: str) -> bytes:
    request = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; InstantCasinoSlotGallery/1.0)",
            "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
            "Referer": "https://instant.slot-reviews.com/",
        },
    )
    with urlopen(request, timeout=45) as response:
        content_type = response.headers.get("Content-Type", "")
        data = response.read()
    if not content_type.startswith("image/"):
        raise RuntimeError(f"Expected image from {url}, received {content_type!r}")
    if len(data) < 12_000:
        raise RuntimeError(f"Downloaded image is unexpectedly small ({len(data)} bytes): {url}")
    return data


def compose_without_cropping(source: Image.Image) -> Image.Image:
    source = ImageOps.exif_transpose(source).convert("RGB")
    if source.width < 400 or source.height < 350:
        raise RuntimeError(f"Source image is too small: {source.width}x{source.height}")

    # Use a soft, darkened crop only as a decorative background. The actual
    # game artwork is separately contained in the foreground and never cropped.
    background = ImageOps.fit(
        source,
        CANVAS,
        method=Image.Resampling.LANCZOS,
        centering=(0.5, 0.5),
    ).filter(ImageFilter.GaussianBlur(radius=34))
    background = ImageEnhance.Brightness(background).enhance(0.38)

    artwork = ImageOps.contain(source, ART_MAX, method=Image.Resampling.LANCZOS)
    x = (CANVAS[0] - artwork.width) // 2
    y = (CANVAS[1] - artwork.height) // 2

    background.paste(artwork, (x, y))
    return background


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for filename, url in SOURCES.items():
        raw = download(url)
        with Image.open(BytesIO(raw)) as source:
            final = compose_without_cropping(source)
            target = OUTPUT / filename
            final.save(target, "WEBP", quality=86, method=6)
        print(
            f"{filename}: saved {final.width}x{final.height}, "
            f"{(OUTPUT / filename).stat().st_size:,} bytes"
        )


if __name__ == "__main__":
    main()
