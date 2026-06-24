# 🍾 Bár Leltár PWA — Telepítési és Használati Útmutató

## 📱 Mi ez?
Egy **Progressive Web App (PWA)**, amelyet kifejezetten vendéglátóipari egységek, kocsmák italos üveg standolásának (leltározásának) megkönnyítésére fejlesztettünk ki. 

- **Intelligens AI kameraolvasás** — Fotózz le egy üveget, és a saját, egyedileg tanított neurális hálónk automatikusan megbecsüli a benne lévő folyadék szintjét.
- **PWA architektúra** — Mobilra natív appként telepíthető a kezdőképernyőre.
- **Modern Backend integráció** — A szintbecslést egy dedikált szerver végzi a háttérben, nincs szükség kliensoldali API kulcsokra vagy bonyolult konfigurációra.
- **Offline működés** — A Service Workernek köszönhetően az alapfunkciók hálózati kapcsolat nélkül is elérhetőek.

---

## 🚀 Telepítés és Hosztolás

Mivel az alkalmazás egy tiszta frontend PWA kliens (a szerverkapcsolat és a modellkezelés be van ágyazva a kódba), **nincs szükség helyi Python szerverre vagy egyéb háttérprogram futtatására** a telepítéshez. Csak a statikus fájlokat kell közzétenni.

### 1. Szükséges fájlok
A projekt működéséhez az alábbi fájlokat kell feltöltened a választott tárhelyre:
```text
index.html      - A teljes felhasználói felület és logika
manifest.json   - A PWA telepíthetőségi beállításai
sw.js           - A Service Worker az offline működésért és cache-elésért
icon-192.png    - Alkalmazásikon (mobil felületre)
icon-512.png    - Alkalmazásikon (indítóképernyőre)

---

## Technikai adatok
- **AI:** Google Gemini 2.5 Flash (vision)
- **Adattárolás:** LocalStorage (eszközön marad, nem tölt fel semmit)
- **PWA:** Service Worker + Web App Manifest
- **Kamera:** MediaDevices API (hátsó kamera preferált)
