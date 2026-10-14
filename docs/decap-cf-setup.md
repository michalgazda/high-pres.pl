# Decap CMS — instrukcja uruchomienia (one-time)

Worker OAuth dla tej strony stoi na **prywatnym koncie Cloudflare** (michalgazda.workers.dev),
tak samo jak annamatejska.pl — NIE na koncie Fundacji Przestrzeń Dobra.

## 0. GitHub OAuth App (jedyny krok wymagający klikania w UI)

1. https://github.com/settings/developers → **New OAuth App**
2. Application name: `highpres-decap`
3. Homepage URL: `https://highpres-decap-oauth.michalgazda.workers.dev`
4. Authorization callback URL (dokładnie, bez trailing slash):
   `https://highpres-decap-oauth.michalgazda.workers.dev/callback`
5. Create → skopiuj **Client ID** i **Client Secret**

## 1. Zaloguj wrangler na konto prywatne

```bash
cd ~/high-pres.pl/oauth-bridge
npx wrangler login --device --browser=false
```

Otwórz podany URL, wpisz kod, zatwierdź — **na prywatnym koncie** (michalgazda.workers.dev).
Sprawdź potem: `npx wrangler whoami`.

## 2. Deploy

```bash
npx wrangler deploy
```

Oczekiwany output:
```
Published highpres-decap-oauth (1.2 sec)
  https://highpres-decap-oauth.michalgazda.workers.dev
```

Jeśli subdomena w outputcie jest inna — zaktualizuj `base_url` w `public/admin/config.yml`
oraz callback w GitHub OAuth App (krok 0).

## 3. Sekrety

```bash
npx wrangler secret put GITHUB_CLIENT_ID      # wklej z kroku 0
npx wrangler secret put GITHUB_CLIENT_SECRET  # wklej z kroku 0
```

## 4. Weryfikacja workera

```bash
curl -s -w "\n%{http_code} -> %{redirect_url}\n" "https://highpres-decap-oauth.michalgazda.workers.dev/auth"
```

Oczekiwane: `302 -> https://github.com/login/oauth/authorize?...`
(503 = brak sekretów; 404 na `/` jest normalne.)

## 5. Panel

https://michalgazda.github.io/high-pres.pl/admin/ → **Login with GitHub**

Zaloguj się kontem GitHub, które ma **Write** na repo `michalgazda/high-pres.pl`.

## Lokalnie

```bash
cd ~/high-pres.pl
npm run preview -- --port 8891
```

Panel: http://127.0.0.1:8891/admin/ (origin jest w `ALLOWED_ORIGINS` workera)

## Zawartość panelu

Kolekcje w `public/admin/config.yml` — wszystko z `src/data/*.json`:

| Kolekcja | Plik |
|---|---|
| Dane firmy | `src/data/site.json` |
| Strona główna | `src/data/homepage.json` |
| Technologia | `src/data/technologia.json` |
| Usługi | `src/data/uslugi.json` |
| Wyceny | `src/data/wyceny.json` |
| Kontakt | `src/data/kontakt.json` |

Publikacja: `publish_mode: editorial_workflow` — zapis tworzy PR/draft, potem publikacja.
