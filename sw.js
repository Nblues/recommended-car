// Service Worker for Car Widget Performance
// Handles caching, offline support, and performance optimization

const CACHE_NAME = 'car-widget-v1';
const CACHE_STATIC_NAME = 'car-widget-static-v1';
const CACHE_DYNAMIC_NAME = 'car-widget-dynamic-v1';

// Files to cache immediately
const STATIC_CACHE_ASSETS = [
  '/',
  '/index.html',
  '/style.css',
  '/car-widget-fixed.html',
  '/car-widget-minimal.html',
  '/car-widget-clean.html',
  '/docs/image-optimization.css',
  '/docs/image-optimization.js',
  'https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;600;700;800&display=swap',
  'https://fonts.googleapis.com/css2?family=Kanit:wght@300;400;500;600;700&display=swap'
];

// Dynamic cache patterns
const CACHE_PATTERNS = {
  images: /\.(jpg|jpeg|png|gif|webp|avif)$/i,
  fonts: /\.(woff|woff2|ttf|eot)$/i,
  api: /\/api\//,
  cdn: /cdn\.shopify\.com/
};

// Cache durations
const CACHE_DURATIONS = {
  static: 24 * 60 * 60 * 1000, // 24 hours
  images: 7 * 24 * 60 * 60 * 1000, // 7 days
  api: 30 * 60 * 1000, // 30 minutes
  fonts: 30 * 24 * 60 * 60 * 1000 // 30 days
};

// Install event - cache static assets
self.addEventListener('install', (event) => {
  console.log('SW: Installing service worker');
  
  event.waitUntil(
    Promise.all([
      caches.open(CACHE_STATIC_NAME).then((cache) => {
        console.log('SW: Caching static assets');
        return cache.addAll(STATIC_CACHE_ASSETS).catch((error) => {
          console.warn('SW: Failed to cache some static assets:', error);
          // Continue even if some assets fail to cache
        });
      }),
      self.skipWaiting()
    ])
  );
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
  console.log('SW: Activating service worker');
  
  event.waitUntil(
    Promise.all([
      // Clean up old caches
      caches.keys().then((cacheNames) => {
        return Promise.all(
          cacheNames
            .filter((cacheName) => {
              return cacheName !== CACHE_STATIC_NAME && 
                     cacheName !== CACHE_DYNAMIC_NAME &&
                     cacheName.startsWith('car-widget-');
            })
            .map((cacheName) => {
              console.log('SW: Deleting old cache:', cacheName);
              return caches.delete(cacheName);
            })
        );
      }),
      self.clients.claim()
    ])
  );
});

// Fetch event - handle requests with caching strategy
self.addEventListener('fetch', (event) => {
  const request = event.request;
  const url = new URL(request.url);
  
  // Skip non-GET requests
  if (request.method !== 'GET') {
    return;
  }
  
  // Skip chrome-extension and other non-http protocols
  if (!request.url.startsWith('http')) {
    return;
  }
  
  // Handle different types of requests
  if (isStaticAsset(request)) {
    event.respondWith(handleStaticAsset(request));
  } else if (isImage(request)) {
    event.respondWith(handleImage(request));
  } else if (isAPI(request)) {
    event.respondWith(handleAPI(request));
  } else if (isFont(request)) {
    event.respondWith(handleFont(request));
  } else {
    event.respondWith(handleDefault(request));
  }
});

// Check if request is for static asset
function isStaticAsset(request) {
  const url = new URL(request.url);
  return STATIC_CACHE_ASSETS.some(asset => 
    request.url.includes(asset) || url.pathname === asset
  );
}

// Check if request is for image
function isImage(request) {
  return CACHE_PATTERNS.images.test(request.url);
}

// Check if request is for API
function isAPI(request) {
  return CACHE_PATTERNS.api.test(request.url) || 
         request.url.includes('products.json') ||
         request.url.includes('cars.json');
}

// Check if request is for font
function isFont(request) {
  return CACHE_PATTERNS.fonts.test(request.url) ||
         request.url.includes('fonts.googleapis.com');
}

// Handle static assets - Cache First strategy
async function handleStaticAsset(request) {
  try {
    const cache = await caches.open(CACHE_STATIC_NAME);
    const cachedResponse = await cache.match(request);
    
    if (cachedResponse) {
      // Check if cache is still valid
      const cacheTime = await getCacheTime(cache, request);
      if (Date.now() - cacheTime < CACHE_DURATIONS.static) {
        return cachedResponse;
      }
    }
    
    // Fetch from network and update cache
    const networkResponse = await fetch(request);
    if (networkResponse.ok) {
      await cache.put(request, networkResponse.clone());
      await setCacheTime(cache, request);
    }
    return networkResponse;
    
  } catch (error) {
    console.warn('SW: Static asset fetch failed:', error);
    // Return cached version even if expired
    const cache = await caches.open(CACHE_STATIC_NAME);
    const cachedResponse = await cache.match(request);
    return cachedResponse || new Response('Offline', { status: 503 });
  }
}

// Handle images - Cache First with longer duration
async function handleImage(request) {
  try {
    const cache = await caches.open(CACHE_DYNAMIC_NAME);
    const cachedResponse = await cache.match(request);
    
    if (cachedResponse) {
      const cacheTime = await getCacheTime(cache, request);
      if (Date.now() - cacheTime < CACHE_DURATIONS.images) {
        return cachedResponse;
      }
    }
    
    const networkResponse = await fetch(request, {
      mode: 'cors',
      credentials: 'omit'
    });
    
    if (networkResponse.ok) {
      await cache.put(request, networkResponse.clone());
      await setCacheTime(cache, request);
    }
    return networkResponse;
    
  } catch (error) {
    console.warn('SW: Image fetch failed:', error);
    
    // Return cached version or placeholder
    const cache = await caches.open(CACHE_DYNAMIC_NAME);
    const cachedResponse = await cache.match(request);
    
    if (cachedResponse) {
      return cachedResponse;
    }
    
    // Return placeholder image
    return fetch('https://via.placeholder.com/300x200?text=Error+Loading+Image')
      .catch(() => new Response('Image not available', { status: 503 }));
  }
}

// Handle API requests - Network First with short cache
async function handleAPI(request) {
  try {
    const networkResponse = await fetch(request, {
      headers: {
        'Cache-Control': 'no-cache'
      }
    });
    
    if (networkResponse.ok) {
      const cache = await caches.open(CACHE_DYNAMIC_NAME);
      await cache.put(request, networkResponse.clone());
      await setCacheTime(cache, request);
    }
    return networkResponse;
    
  } catch (error) {
    console.warn('SW: API fetch failed, using cache:', error);
    
    // Fallback to cache
    const cache = await caches.open(CACHE_DYNAMIC_NAME);
    const cachedResponse = await cache.match(request);
    
    if (cachedResponse) {
      const cacheTime = await getCacheTime(cache, request);
      if (Date.now() - cacheTime < CACHE_DURATIONS.api) {
        return cachedResponse;
      }
    }
    
    return new Response(
      JSON.stringify({ 
        error: 'API temporarily unavailable', 
        products: [] 
      }), 
      { 
        status: 503,
        headers: { 'Content-Type': 'application/json' }
      }
    );
  }
}

// Handle fonts - Cache First with long duration
async function handleFont(request) {
  try {
    const cache = await caches.open(CACHE_STATIC_NAME);
    const cachedResponse = await cache.match(request);
    
    if (cachedResponse) {
      const cacheTime = await getCacheTime(cache, request);
      if (Date.now() - cacheTime < CACHE_DURATIONS.fonts) {
        return cachedResponse;
      }
    }
    
    const networkResponse = await fetch(request, {
      mode: 'cors'
    });
    
    if (networkResponse.ok) {
      await cache.put(request, networkResponse.clone());
      await setCacheTime(cache, request);
    }
    return networkResponse;
    
  } catch (error) {
    console.warn('SW: Font fetch failed:', error);
    const cache = await caches.open(CACHE_STATIC_NAME);
    const cachedResponse = await cache.match(request);
    return cachedResponse || new Response('Font not available', { status: 503 });
  }
}

// Handle default requests - Network First
async function handleDefault(request) {
  try {
    const networkResponse = await fetch(request);
    
    if (networkResponse.ok) {
      const cache = await caches.open(CACHE_DYNAMIC_NAME);
      await cache.put(request, networkResponse.clone());
      await setCacheTime(cache, request);
    }
    return networkResponse;
    
  } catch (error) {
    console.warn('SW: Default fetch failed:', error);
    const cache = await caches.open(CACHE_DYNAMIC_NAME);
    const cachedResponse = await cache.match(request);
    return cachedResponse || new Response('Resource not available', { status: 503 });
  }
}

// Helper functions for cache timestamps
async function setCacheTime(cache, request) {
  const timeRequest = new Request(request.url + '?timestamp');
  const timeResponse = new Response(Date.now().toString());
  await cache.put(timeRequest, timeResponse);
}

async function getCacheTime(cache, request) {
  const timeRequest = new Request(request.url + '?timestamp');
  const timeResponse = await cache.match(timeRequest);
  if (timeResponse) {
    const timeText = await timeResponse.text();
    return parseInt(timeText);
  }
  return 0;
}

// Background sync for failed requests
self.addEventListener('sync', (event) => {
  if (event.tag === 'background-sync') {
    console.log('SW: Background sync triggered');
    event.waitUntil(handleBackgroundSync());
  }
});

async function handleBackgroundSync() {
  // Re-attempt failed API calls when connection is restored
  try {
    const cache = await caches.open(CACHE_DYNAMIC_NAME);
    const keys = await cache.keys();
    
    for (const request of keys) {
      if (isAPI(request)) {
        const cacheTime = await getCacheTime(cache, request);
        if (Date.now() - cacheTime > CACHE_DURATIONS.api) {
          try {
            const response = await fetch(request);
            if (response.ok) {
              await cache.put(request, response.clone());
              await setCacheTime(cache, request);
            }
          } catch (error) {
            console.warn('SW: Background sync failed for:', request.url);
          }
        }
      }
    }
  } catch (error) {
    console.warn('SW: Background sync error:', error);
  }
}

// Message handling for cache management
self.addEventListener('message', (event) => {
  if (event.data && event.data.type) {
    switch (event.data.type) {
      case 'CLEAR_CACHE':
        clearAllCaches().then(() => {
          event.ports[0]?.postMessage({ success: true });
        });
        break;
      case 'UPDATE_CACHE':
        updateCache().then(() => {
          event.ports[0]?.postMessage({ success: true });
        });
        break;
    }
  }
});

async function clearAllCaches() {
  const cacheNames = await caches.keys();
  await Promise.all(
    cacheNames.map(cacheName => caches.delete(cacheName))
  );
  console.log('SW: All caches cleared');
}

async function updateCache() {
  const cache = await caches.open(CACHE_STATIC_NAME);
  await cache.addAll(STATIC_CACHE_ASSETS);
  console.log('SW: Cache updated');
}