#!/usr/bin/env sh
set -eu

OUT_DIR="${1:-public}"
if [ ! -d "$OUT_DIR" ]; then
  echo "ERROR: build output directory '$OUT_DIR' does not exist." >&2
  exit 1
fi
if [ ! -f "$OUT_DIR/index.html" ]; then
  echo "ERROR: '$OUT_DIR/index.html' is missing; this does not look like a built Hugo site." >&2
  exit 1
fi
for required in _headers _redirects; do
  if [ ! -f "$OUT_DIR/$required" ]; then
    echo "ERROR: '$OUT_DIR/$required' is missing. Check that static/$required exists." >&2
    exit 1
  fi
done

# Fail the deployment build if likely private/source artifacts leaked into the public output.
LEAKS=$(find "$OUT_DIR" \
  \( -type d -name '.git' -o -type f \( \
    -name '.env' -o -name '.env.*' -o -name '.DS_Store' -o -name '.htaccess' -o \
    -name '*.pem' -o -name '*.key' -o -name '*.p12' -o -name '*.pfx' -o \
    -name '*.toml' -o -name '*.sql' -o -name '*.dump' -o -name '*.zip' -o \
    -name '*.7z' -o -name '*.rar' -o -name '*.tar' -o -name '*.tar.gz' -o \
    -name '*.bak' -o -name '*.backup' -o -name '*.old' -o -name '*.map' \
  \) \) -print)
if [ -n "$LEAKS" ]; then
  echo "ERROR: possible private/source artifacts found in '$OUT_DIR':" >&2
  printf '%s\n' "$LEAKS" >&2
  exit 1
fi

# Protect source markdown and build configuration from accidental static copying.
LEAKS=$(find "$OUT_DIR" -type f \( -name '*.md' -o -name 'hugo.toml' -o -name 'wrangler.toml' -o -name 'wrangler.jsonc' \) -print)
if [ -n "$LEAKS" ]; then
  echo "ERROR: source documentation/configuration found in '$OUT_DIR':" >&2
  printf '%s\n' "$LEAKS" >&2
  exit 1
fi

# Fail the deployment build if any rendered anchor points to another website.
python3 - "$OUT_DIR" <<'PY'
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import sys

root = Path(sys.argv[1])
allowed_host = "instant.slot-reviews.com"
violations = []

class AnchorAudit(HTMLParser):
    def __init__(self, page):
        super().__init__(convert_charrefs=True)
        self.page = page

    def handle_starttag(self, tag, attrs):
        if tag.lower() != "a":
            return
        href = dict(attrs).get("href")
        if not href:
            return
        value = href.strip()
        parsed = urlsplit(value)
        is_web_url = parsed.scheme.lower() in {"http", "https"} or value.startswith("//")
        host = (parsed.hostname or "").lower()
        if is_web_url and host and host != allowed_host:
            violations.append((self.page, value))

for page in root.rglob("*.html"):
    try:
        parser = AnchorAudit(page.relative_to(root))
        parser.feed(page.read_text(encoding="utf-8"))
        parser.close()
    except (OSError, UnicodeError) as exc:
        print(f"ERROR: could not inspect {page}: {exc}", file=sys.stderr)
        raise SystemExit(1)

if violations:
    print("ERROR: rendered pages contain links to external websites; only same-site links and /go/bonus are allowed:", file=sys.stderr)
    for page, href in violations:
        print(f"  {page}: {href}", file=sys.stderr)
    raise SystemExit(1)

print("OK: rendered anchors do not link to external websites (the /go/bonus redirect remains same-site).")
PY

echo "OK: '$OUT_DIR' contains a site index, Cloudflare Pages security files, and no checked source/secret artifacts."
