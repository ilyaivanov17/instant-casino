#!/usr/bin/env bash
set -Eeuo pipefail
cd "$(dirname "${BASH_SOURCE[0]}")/.."

if ! command -v hugo >/dev/null 2>&1; then
  echo "ERROR: Hugo is not installed. Install Hugo Extended, then retry." >&2
  exit 127
fi

hugo --cleanDestinationDir --minify --environment production --printPathWarnings
python3 scripts/check-sitemap.py
python3 scripts/check-rendered-seo.py
./scripts/check-public-output.sh public
printf '\nProduction build complete: ./public/\n'
