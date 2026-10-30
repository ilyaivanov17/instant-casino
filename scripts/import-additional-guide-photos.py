#!/usr/bin/env python3
"""Fetch Pexels originals, crop to the guide aspect ratio and save local WebP assets."""
from __future__ import annotations

from io import BytesIO
from pathlib import Path
from urllib.request import Request, urlopen

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "static" / "images" / "guides"
SIZE = (1440, 810)

PHOTOS = {
    "blackjack-casino.webp": (
        "https://images.pexels.com/photos/6664144/pexels-photo-6664144.jpeg?auto=compress&cs=tinysrgb&w=2400",
        "Anna Shvets",
        "https://www.pexels.com/photo/close-up-of-blackjack-table-and-croupier-hands-6664144/",
    ),
    "live-casino.webp": (
        "https://images.pexels.com/photos/7594313/pexels-photo-7594313.jpeg?auto=compress&cs=tinysrgb&w=2400",
        "Pavel Danilyuk",
        "https://www.pexels.com/photo/playing-poker-in-a-casino-7594313/",
    ),
    "privacy-documents.webp": (
        "https://images.pexels.com/photos/8441819/pexels-photo-8441819.jpeg?auto=compress&cs=tinysrgb&w=2400",
        "Kampus Production",
        "https://www.pexels.com/photo/a-laptop-and-documents-on-the-table-8441819/",
    ),
}


def download(url: str) -> bytes:
    request = Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0 (compatible; InstantCasinoAssetFetcher/1.0)",
            "Accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
        },
    )
    with urlopen(request, timeout=45) as response:
        content_type = response.headers.get("Content-Type", "")
        data = response.read()
    if not content_type.startswith("image/"):
        raise RuntimeError(f"Expected an image from {url}, received {content_type!r}")
    if len(data) < 20_000:
        raise RuntimeError(f"Downloaded image is unexpectedly small ({len(data)} bytes): {url}")
    return data


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for filename, (url, author, source_page) in PHOTOS.items():
        raw = download(url)
        with Image.open(BytesIO(raw)) as source:
            image = ImageOps.exif_transpose(source).convert("RGB")
            if image.width < 1200 or image.height < 700:
                raise RuntimeError(
                    f"{filename}: source resolution too small: {image.width}x{image.height}"
                )
            image = ImageOps.fit(
                image,
                SIZE,
                method=Image.Resampling.LANCZOS,
                centering=(0.5, 0.5),
            )
            target = OUTPUT / filename
            image.save(target, "WEBP", quality=84, method=6)
        print(
            f"Saved {target.relative_to(ROOT)} ({target.stat().st_size:,} bytes); "
            f"photo by {author}; {source_page}"
        )


if __name__ == "__main__":
    main()
