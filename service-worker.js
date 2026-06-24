const CACHE_NAME = 'jobmeta-demo-v56';
const CORE_ASSETS = [
  './',
  './index.html',
  './app/index.html',
  './demo/index.html',
  './local/index.html',
  './offline.html',
  './static-api-shim.js',
  './data/static-api-data.json',
  './manifest.webmanifest',
  './version.json',
  './assets/favicon.ico',
  './assets/icon.svg',
  './assets/icon-32.png',
  './assets/icon-192.png',
  './assets/icon-512.png'
];

self.addEventListener('install', (event) => {
  event.waitUntil(caches.open(CACHE_NAME).then((cache) => cache.addAll(CORE_ASSETS)));
  self.skipWaiting();
});

self.addEventListener('activate', (event) => {
  event.waitUntil(
    caches.keys().then((keys) => Promise.all(keys.map((key) => key === CACHE_NAME ? null : caches.delete(key))))
  );
  self.clients.claim();
});

self.addEventListener('fetch', (event) => {
  if (event.request.method !== 'GET') return;
  event.respondWith(
    fetch(event.request).then((response) => {
      const copy = response.clone();
      caches.open(CACHE_NAME).then((cache) => cache.put(event.request, copy));
      return response;
    }).catch(async () => {
      const cached = await caches.match(event.request);
      if (cached) return cached;
      if (event.request.mode === 'navigate') return caches.match('./offline.html');
      return Response.error();
    })
  );
});
