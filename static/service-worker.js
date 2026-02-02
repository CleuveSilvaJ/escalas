self.addEventListener('install', function(event) {
  event.waitUntil(
    caches.open('escala-cache').then(function(cache) {
      return cache.addAll([
        '/',
        '/static/style.css',
        '/static/icon.png'
      ]);
    })
  );
});

self.addEventListener('fetch', function(event) {
  event.respondWith(
    caches.match(event.request).then(function(response) {
      return response || fetch(event.request);
    })
  );
});
