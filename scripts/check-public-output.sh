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

# External editorial links are allowed when they use HTTPS and open safely.
# Affiliate links must be explicitly authored as same-site /go/bonus routes.
python3 - "$OUT_DIR" <<'PY'
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit
import sys

root = Path(sys.argv[1])
violations = []
external_links = []

class AnchorAudit(HTMLParser):
    def __init__(self, page):
        super().__init__(convert_charrefs=True)
        self.page = page

    def handle_starttag(self, tag, attrs):
        if tag.lower() != "a":
            return
        attrs = dict(attrs)
        href = (attrs.get("href") or "").strip()
        if not href:
            return
        parsed = urlsplit(href)
        is_web_url = parsed.scheme.lower() in {"http", "https"} or href.startswith("//")
        host = (parsed.hostname or "").lower()
        if not is_web_url or not host or host == "instant.slot-reviews.com":
            return
        external_links.append((self.page, href))
        if parsed.scheme.lower() != "https":
            violations.append((self.page, href, "external links must use HTTPS"))
        if attrs.get("target", "").lower() == "_blank":
            rel = set((attrs.get("rel") or "").lower().split())
            if not {"noopener", "noreferrer"}.issubset(rel):
                violations.append((self.page, href, 'target="_blank" links must include rel="noopener noreferrer"'))

for page in root.rglob("*.html"):
    try:
        parser = AnchorAudit(page.relative_to(root))
        parser.feed(page.read_text(encoding="utf-8"))
        parser.close()
    except (OSError, UnicodeError) as exc:
        print(f"ERROR: could not inspect {page}: {exc}", file=sys.stderr)
        raise SystemExit(1)

expected_author_links = {
    "https://uk.linkedin.com/in/arthur-mustoe-6051a477",
    "https://casinoreviews.com/",
    "https://www.linkedin.com/in/coreylevitan",
    "https://corey-levitan-merklin.medium.com/",
    "https://ro.linkedin.com/in/cristina-tudose-b1b925168",
    "https://cristinatudose.ro/",
    "https://www.linkedin.com/in/danmichalski",
    "https://muckrack.com/dan-michalski",
    "https://medium.com/@glowingwolf3930",
    "https://substack.com/@dominicfield1",
    "https://cleobetraslots.wordpress.com/",
    "https://medium.com/@JonPill",
    "https://lcb.org/",
    "https://www.casino.guru/team/jon-pill",
    "https://cl.linkedin.com/in/ibarram94/en",
    "https://marco-ibarra.com/",
}

for lang in ("de", "en", "pl", "es", "pt", "ja"):
    relative = "authors/index.html" if lang == "de" else f"{lang}/authors/index.html"
    page = root / relative
    if not page.is_file():
        violations.append((relative, "", "author directory page is missing"))
        continue
    parser = AnchorAudit(Path(relative))
    parser.feed(page.read_text(encoding="utf-8"))
    found = {href for _, href in external_links if _ == Path(relative)}
    missing = sorted(expected_author_links - found)
    for href in missing:
        violations.append((relative, href, "expected public author profile link is missing"))

if violations:
    print("ERROR: external-link audit failed:", file=sys.stderr)
    for page, href, reason in violations:
        print(f"  {page}: {href or '(no URL)'} — {reason}", file=sys.stderr)
    raise SystemExit(1)

print(f"OK: {len(external_links)} external HTTPS links retain safe attributes; all 16 author profile links appear in all six localized directories.")
PY

echo "OK: '$OUT_DIR' contains a site index, Cloudflare Pages security files, and no checked source/secret artifacts."
