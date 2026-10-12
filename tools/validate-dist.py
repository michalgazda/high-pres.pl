from pathlib import Path
from html.parser import HTMLParser

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"

class PageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.urls = []
        self.canonicals = []
        self.tels = []
        self.h1 = 0
        self.title = 0
        self.description = 0

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag in {"a", "img", "script", "link"}:
            url = attrs.get("href") or attrs.get("src")
            if url:
                self.urls.append(url)
        if tag == "link" and attrs.get("rel") == "canonical":
            self.canonicals.append(attrs.get("href", ""))
        if tag == "a" and attrs.get("href", "").startswith("tel:"):
            self.tels.append(attrs["href"] or "")
        if tag == "h1": self.h1 += 1
        if tag == "title": self.title += 1
        if tag == "meta" and attrs.get("name") == "description": self.description += 1

errors = []
for page in sorted(DIST.rglob("*.html")):
    parser = PageParser()
    parser.feed(page.read_text(errors="replace"))
    if parser.title != 1: errors.append(f"{page}: expected one title")
    if parser.description != 1: errors.append(f"{page}: expected one description")
    if parser.h1 != 1: errors.append(f"{page}: expected one h1")
    if len(parser.canonicals) != 1 or "//high-pres.pl//" in parser.canonicals[0]:
        errors.append(f"{page}: malformed canonical")
    if any("*" in value for value in parser.tels):
        errors.append(f"{page}: invalid telephone URI")
    for url in parser.urls:
        if not url.startswith("/high-pres.pl/"):
            continue
        target = DIST / url[len("/high-pres.pl/"):].split("#", 1)[0].split("?", 1)[0]
        if target.is_dir(): target /= "index.html"
        if not target.exists(): errors.append(f"{page}: missing {url}")

if errors:
    print("\n".join(errors))
    raise SystemExit(1)
print(f"validated {len(list(DIST.rglob('*.html')))} HTML pages")
