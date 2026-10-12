# Decap CMS — instrukcja uruchomienia (one-time, ~5 min)

## 0. GitHub OAuth App (wykonaj sam)

1. https://github.com/settings/developers → New OAuth App
2. Application name: `highpres-decap`
3. Homepage URL: `https://highpres-decap-oauth.przestrzendobra.workers.dev`
4. Authorization callback URL (dokładnie):
   `https://highpres-decap-oauth.przestrzendobra.workers.dev/callback`
5. Create → skopiuj **Client ID** i **Client Secret**

## 1. Zaloguj wrangler — już zrobione (konto przestrzendobra)

## 2. Deploy

```bash
cd ~/high-pres.pl/oauth-bridge
npx wrangler deploy
```

Oczekiwany output:
```
Published highpres-decap-oauth (1.2x sec)
  https://highpres-decap-oauth.przestrzendobra.workers.dev
```

## 3. Dodaj sekrety

```bash
npx wrangler secret put GITHUB_CLIENT_ID      # wklej z kroku 0
npx wrangler secret put GITHUB_CLIENT_SECRET  # wklej z kroku 0
```

## 4. Werifikacja

```bash
curl -sI "https://highpres-decap-oauth.przestrzendobra.workers.dev/auth" | head -3
```

Oczekiwane: `HTTP/2 302` z `location: https://github.com/login/oauth/authorize?...`

## 5. Push na GitHub + test

```bash
cd ~/high-pres.pl
git add -A && git commit -m "Decap CMS + OAuth bridge" && git push
```

Po deployu GH Pages otwórz:
https://michalgazda.github.io/high-pres.pl/admin/
→ Login with GitHub → autoryzuj

## Lokalnie (Docker)

```bash
cd ~/high-pres.pl
# uruchom preview na :8891
npm run preview -- --port 8891
# lub przez Astro dev:
npm run dev -- --port 8891
```

Panel: http://127.0.0.1:8891/admin/ (już dodane do ALLOWED_ORIGINS)