// service-worker.js

self.addEventListener('install', (event) => {
    event.waitUntil(
      caches.open('cfmms-cache').then((cache) => {
        return cache.addAll([
          '/',
          '/static/css/admin_styles.css', // Add paths to all your CSS, JavaScript, images, etc.
          '/static/js/app.js',
          '/static/icons/icon-192x192.png',
          '/static/icons/icon-512x512.png',
            // Add paths you want to work offline
          // Include any additional offline resources as needed
        ]);
      })
    );
  });
  
  self.addEventListener('fetch', (event) => {
    event.respondWith(
      caches.match(event.request).then((response) => {
        return response || fetch(event.request);
      })
    );
  });
  

 