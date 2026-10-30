#!/usr/bin/env python3
"""Download four Pexels photos and prepare local, responsive guide-card images.

Source photos are published under the Pexels License (free commercial use).
The originals are kept remote only as download sources; the generated WebP files
are committed into static/images/guides/ and served from the site's own domain.
"""
from __future__ import annotations

from io import BytesIO
from pathlib import Path
from urllib.request import Request, urlopen

from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "static" / "images" / "guides"
SIZE = (1440, 810)

PHOTOS = {
    "slots-casino.webp": (
        "https://images.pexels.com/photos/24643920/pexels-photo-24643920.jpeg?auto=compress&cs=tinysrgb&w=2400",
        "Elizabeth Ferreira",
        "https://www.pexels.com/photo/interior-of-a-casino-24643920/",
    ),
    "bonuses-casino.webp": (
        "https://images.pexels.com/photos/4677402/pexels-photo-4677402.jpeg?auto=compress&cs=tinysrgb&w=2400",
        "Aidan Howe",
        "https://www.pexels.com/photo/casino-table-in-close-up-view-4677402/",
    ),
    "payments-casino.webp": (
        "https://images.pexels.com/photos/7594588/pexels-photo-7594588.jpeg?auto=compress&cs=tinysrgb&w=2400",
        "Pavel Danilyuk",
        "https://www.pexels.com/photo/a-cashier-handing-a-tray-of-chips-to-the-player-7594588/",
    ),
    "security-casino.webp": (
        "https://images.pexels.com/photos/7364948/pexels-photo-7364948.jpeg?auto=compress&cs=tinysrgb&w=2400",
        "Łukasz Klimkiewicz",
        "https://www.pexels.com/photo/a-white-cctv-7364948/",
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
                centering=(0.5, 0.48),
            )
            target = OUTPUT / filename
            image.save(target, "WEBP", quality=84, method=6)
        print(
            f"Saved {target.relative_to(ROOT)} "
            f"({target.stat().st_size:,} bytes); photo by {author}; {source_page}"
        )


if __name__ == "__main__":
    main()
