from pathlib import Path
import re
import requests

ROOT = Path(__file__).resolve().parents[1]
source = (ROOT / "src/data/galleries.ts").read_text()
blocks = dict(re.findall(r"export const (realizacje2d|realizacje3d|rozetyData) = \[\n(.*?)(?=\n\];)", source, re.S))
dirs = {
    "realizacje2d": ROOT / "public/images/realizacje-2d",
    "realizacje3d": ROOT / "public/images/realizacje-3d",
    "rozetyData": ROOT / "public/images/rozety",
}
base = "https://high-pres.pl/wp-content/uploads/2025/07/"
total = downloaded = skipped = 0
errors = []
for directory in dirs.values():
    directory.mkdir(parents=True, exist_ok=True)
for name, block in blocks.items():
    for filename in re.findall(r"'([^']+)'", block):
        total += 1
        target = dirs[name] / filename
        if target.exists() and target.stat().st_size > 1000:
            skipped += 1
            continue
        try:
            response = requests.get(base + filename, timeout=60)
            response.raise_for_status()
            target.write_bytes(response.content)
            downloaded += 1
        except Exception as exc:
            errors.append((name, filename, str(exc)))
print(f"gallery assets: total={total} downloaded={downloaded} skipped={skipped} errors={len(errors)}")
for error in errors:
    print("ERROR", *error)
if errors:
    raise SystemExit(1)
