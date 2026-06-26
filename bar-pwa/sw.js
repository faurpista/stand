const CACHE = 'bar-leltár-v2';
const ASSETS = [
  './',
  './index.html',
  './manifest.json'
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(c => c.addAll(ASSETS)).then(() => self.skipWaiting())
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys =>
      Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)))
    ).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  // AI API hívásokat nem cache-eljük
  if (e.request.url.includes('googleapis.com') || e.request.url.includes('generativelanguage')) {
    return;
  }

  e.respondWith(
    // Először megpróbáljuk a hálózatról letölteni
    fetch(e.request)
      .then(response => {
        // Ha sikeres a letöltés és statikus fájlról van szó, frissítjük a cache-t a háttérben
        if (response.status === 200 && e.request.method === 'GET') {
          const responseClone = response.clone();
          caches.open(CACHE).then(cache => {
            cache.put(e.request, responseClone);
          });
        }
        return response;
      })
      .catch(() => {
        // Ha nincs internet (offline), akkor nézzük meg a cache-ben
        return caches.match(e.request).then(r => r || caches.match('./index.html'));
      })
  );
});

