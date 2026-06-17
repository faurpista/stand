# 🍾 Bár Leltár PWA — Telepítési útmutató

## Mi ez?
Egy Progressive Web App (PWA) kocsmák italos üveg standolásához.
- Üvegek töltöttségi szintjének nyilvántartása
- **AI kameraolvasás** — fotóz le egy üveget, a Gemini AI megbecsüli a szintet
- Offline is működik (Service Worker)
- Telepíthető mobilra kezdőképernyőre

---

## Telepítés

### 1. Fájlok elhelyezése
A következő fájlokat töltsd fel egy webszerverre (vagy nyisd meg lokálisan):
```
index.html
manifest.json
sw.js
icon-192.png
icon-512.png
```

> **Fontos:** A kamera és a Service Worker csak HTTPS kapcsolaton működik!
> Lokális teszteléshez `localhost` is megfelelő.

### 2. Egyszerű lokális szerver (opcionális)
Ha van Python telepítve:
```bash
python3 -m http.server 8080
```
Majd böngészőben: `http://localhost:8080`

### 3. Ingyenes tárhely opciók
- **GitHub Pages** — ingyen, HTTPS automatikus
- **Netlify** — drag & drop deploy, ingyen
- **Vercel** — ingyen, gyors

---

## Google Gemini API kulcs megszerzése

1. Menj: https://aistudio.google.com/app/apikey
2. Jelentkezz be Google fiókkal
3. Kattints: **Create API key**
4. Másold be a kulcsot az appba → **AI Scan** fül → API kulcs mező

> Az ingyenes tier havonta 1 millió tokent tartalmaz (bőven elég standoláshoz).

---

## Használat

### Leltár fül
- Üvegek listázása, szerkesztése
- `−` / `+` gombokkal 5%-onként állítható a szint
- Közvetlenül beírható a százalék
- `🤖` gomb: gyors AI scan az adott üveghez

### AI Scan fül
1. Add meg a Gemini API kulcsot
2. Válaszd ki, melyik üveghez rendelod az eredményt
3. **Kamera** gombbal indítsd el a kamerát (hátsó kamera automatikusan)
4. Vagy **Kép** gombbal tölts fel meglévő fotót
5. **Elemzés** → az AI megbecsüli a töltöttségi szintet
6. **Alkalmaz** → frissíti az üveg szintjét a leltárban

### PWA telepítés mobilra
- **Android (Chrome):** Menüben → "Hozzáadás a kezdőképernyőhöz"
- **iOS (Safari):** Megosztás → "Hozzáadás a főképernyőre"
- **Desktop Chrome:** Cím sávban a telepítés ikon

---

## Tippek az AI pontosságához
- Jó megvilágítás sokat segít
- Tartsd a kamerát merőlegesen az üvegre
- Az üveg teljes magassága látszódjon
- Háttér ne legyen teli üvegekkel

---

## Technikai adatok
- **AI:** Google Gemini 1.5 Flash (vision)
- **Adattárolás:** LocalStorage (eszközön marad, nem tölt fel semmit)
- **PWA:** Service Worker + Web App Manifest
- **Kamera:** MediaDevices API (hátsó kamera preferált)
