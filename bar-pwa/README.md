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

- index.html      - A teljes felhasználói felület és logika
- manifest.json   - A PWA telepíthetőségi beállításai
- sw.js           - A Service Worker az offline működésért és cache-elésért
- icon-192.png    - Alkalmazásikon (mobil felületre)
- icon-512.png    - Alkalmazásikon (indítóképernyőre)

---

## Technikai adatok
- **AI:** Google Gemini 2.5 Flash (vision)
- **Adattárolás:** LocalStorage (eszközön marad, nem tölt fel semmit)
- **PWA:** Service Worker + Web App Manifest
- **Kamera:** MediaDevices API (hátsó kamera preferált)

---

## 🛠️ Használati Útmutató
### Leltár fül
Üvegek kezelése: Az aktuális italkészlet listázása és gyors áttekintése.

Manuális finomhangolás: A − és + gombokkal 5%-os lépésekben gyorsan korrigálható a szint, de a százalékos érték mezőbe közvetlenül is beírható a pontos szám.

Gyors AI gomb: A sorok végén található 🤖 ikonra kattintva az app azonnal átugrik az AI fülre, és automatikusan kijelöli az adott üveget az elemzéshez.

### AI Scan fül (Szintbecslés)
Üveg kiválasztása: Válaszd ki a legördülő listából, hogy melyik italt szeretnéd standolni.

### Képbevitel:

A Kamera gombbal indítsd el az élőképet (az app automatikusan a telefon hátlapi, autofókuszos kameráját fogja aktiválni).

A Fájl/Kép gombbal galériából vagy fájlrendszerből is feltölthetsz egy korábban készült fotót.

### Elemzés: Kattints a Szint becslése gombra. A háttérben futó szerverünk a saját mélytanulásos (Deep Learning) modellünk segítségével kielemzi a képet.

Alkalmazás: Ha az AI által becsült százalékos érték megfelelő, az Alkalmaz gombbal egyetlen kattintással frissítheted az üveg állapotát a leltárban.

### PWA Telepítés mobileszközökre
Nem kell App Store- vagy Google Play-fiók, az alkalmazást közvetlenül a böngészőből telepítheted:

Android (Google Chrome): Kattints a jobb felső sarokban található három pöttyre (Menü) → "Alkalmazás telepítése" vagy "Hozzáadás a kezdőképernyőhöz".

iOS / iPhone (Apple Safari): Kattints a képernyő alján lévő Megosztás ikonra (felfelé mutató nyíl egy négyzetben) → Görgess le és válaszd a "Hozzáadás a főképernyőre" lehetőséget.

Asztali PC/Laptop (Chrome/Edge): A címsor jobb szélén megjelenő telepítés ikonra kattintva külön ablakos appként futtatható.

---

## 📸 Tippek a tűpontos AI méréshez
A saját fejlesztésű neurális hálónk precíz munkájához érdemes betartani az alábbi fotózási szabályokat:

Merőleges perspektíva: A kamerát tartsd vízszintesen, pontosan az üveg középvonalával szemben. Ne fotózd az üveget felülről vagy alulról (békaperspektívából).

Teljes láthatóság: Az üvegnek a talpától a kupakjáig teljes egészében benne kell lennie a kijelölt keretben.

Tiszta háttér: Lehetőleg ne legyen a fotózott üveg mögött közvetlenül egy másik, teli üveg, mert ez megzavarhatja a modellt a folyadékszint detektálásakor.

Megfelelő fényviszonyok: Kerüld a pult alatti túl sötét sarkokat vagy a közvetlen, erős háttérfényt (pl. ablak előtt). A szórt, normál kocsmai megvilágítás a legoptimálisabb.


---
