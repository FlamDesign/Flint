#!/usr/bin/env bash
# Downloads every product image into ./images so the site no longer depends on
# the image CDN, then rebuilds the pages to point at the local copies.
# Run from the repo root:  bash scripts/fetch-images.sh
set -euo pipefail
cd "$(dirname "$0")/.."
mkdir -p images/min
while IFS=$'\t' read -r _ key url; do
  [ -z "$key" ] && continue
  echo "-> $key"
  curl -fsSL "$url" -o "images/$key.png"
  curl -fsSL "${url%.png}_min.webp" -o "images/min/$key.webp" || true
done < images.tsv
python3 build.py
echo "Done. Commit the images/ folder along with the rebuilt pages."
