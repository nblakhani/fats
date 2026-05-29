const CACHE = 'fieldlog-v1';
const OFFLINE_QUEUE_KEY = 'fieldlog-offline-queue';

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(c => c.addAll([
      '/pwa/index.html',
      '/pwa/manifest.json',
    ]))
  );
  self.skipWaiting();
});

self.addEventListener('activate', e => {
  e.waitUntil(clients.claim());
});

self.addEventListener('fetch', e => {
  if (e.request.url.includes('/api/')) {
    // Network first for API calls
    e.respondWith(
      fetch(e.request).catch(() => {
        // If offline and it's a POST, queue it
        if (e.request.method === 'POST') {
          return e.request.clone().json().then(body => {
            queueOfflineRequest(e.request.url, body);
            return new Response(JSON.stringify({
              queued: true,
              message: 'Saved offline — will sync when connected'
            }), { headers: { 'Content-Type': 'application/json' } });
          });
        }
        return new Response(JSON.stringify({ error: 'offline' }),
          { status: 503, headers: { 'Content-Type': 'application/json' } });
      })
    );
  } else {
    // Cache first for static assets
    e.respondWith(
      caches.match(e.request).then(cached => cached || fetch(e.request))
    );
  }
});

async function queueOfflineRequest(url, body) {
  const clients = await self.clients.matchAll();
  clients.forEach(c => c.postMessage({ type: 'QUEUE_OFFLINE', url, body }));
}

// Sync offline queue when back online
self.addEventListener('sync', e => {
  if (e.tag === 'sync-visits') {
    e.waitUntil(syncOfflineQueue());
  }
});

async function syncOfflineQueue() {
  const clients = await self.clients.matchAll();
  clients.forEach(c => c.postMessage({ type: 'SYNC_NOW' }));
}
