
/**
 * Ultimate Car Detail Service Worker 2025
 * PWA + Offline Support + Performance Boost
 */

const CACHE_NAME = 'car-detail-v2025.1';
const STATIC_CACHE = 'static-v2025.1';
const DYNAMIC_CACHE = 'dynamic-v2025.1';
const IMAGE_CACHE = 'images-v2025.1';

// Files to cache for offline support
const STATIC_ASSETS = [
    '/',
    '/docs/',
    '/docs/index.html',
    '/docs/ultimate-car-detail-style.css',
    '/docs/ultimate-car-detail.js',
    '/docs/style.css',
    '/docs/image-optimization.css',
    '/docs/manifest.json',
    'https://fonts.googleapis.com/css2?family=Prompt:wght@300;400;600;700;800&display=swap'
];

// Install event - cache static assets
self.addEventListener('install', (event) => {
    console.log('🚀 Service Worker Installing...');
    
    event.waitUntil(
        caches.open(STATIC_CACHE)
            .then((cache) => {
                console.log('📦 Caching static assets...');
                return cache.addAll(STATIC_ASSETS);
            })
            .catch((error) => {
                console.error('❌ Failed to cache static assets:', error);
            })
    );
    
    self.skipWaiting();
});

// Activate event - clean up old caches
self.addEventListener('activate', (event) => {
    console.log('✅ Service Worker Activated');
    
    event.waitUntil(
        caches.keys().then((cacheNames) => {
            return Promise.all(
                cacheNames.map((cacheName) => {
                    if (cacheName !== STATIC_CACHE && 
                        cacheName !== DYNAMIC_CACHE && 
                        cacheName !== IMAGE_CACHE) {
                        console.log('🗑️ Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
    
    event.waitUntil(self.clients.claim());
});

// Fetch event - handle all network requests
self.addEventListener('fetch', (event) => {
    const { request } = event;
    const url = new URL(request.url);
    
    if (request.method !== 'GET') return;
    if (!url.protocol.startsWith('http')) return;
    
    if (isImageRequest(request)) {
        event.respondWith(imageStrategy(request));
    } else if (isStaticAsset(request)) {
        event.respondWith(cacheFirstStrategy(request, STATIC_CACHE));
    } else {
        event.respondWith(staleWhileRevalidateStrategy(request, DYNAMIC_CACHE));
    }
});

// Cache strategies
async function cacheFirstStrategy(request, cacheName) {
    try {
        const cachedResponse = await caches.match(request);
        if (cachedResponse) return cachedResponse;
        
        const networkResponse = await fetch(request);
        if (networkResponse.ok) {
            const cache = await caches.open(cacheName);
            cache.put(request, networkResponse.clone());
        }
        return networkResponse;
    } catch (error) {
        return await caches.match('/docs/index.html') || 
               new Response('Offline', { status: 503 });
    }
}

async function staleWhileRevalidateStrategy(request, cacheName) {
    const cache = await caches.open(cacheName);
    const cachedResponse = await cache.match(request);
    
    const fetchPromise = fetch(request).then((networkResponse) => {
        if (networkResponse.ok) {
            cache.put(request, networkResponse.clone());
        }
        return networkResponse;
    }).catch(() => cachedResponse);
    
    return cachedResponse || await fetchPromise;
}

async function imageStrategy(request) {
    const cache = await caches.open(IMAGE_CACHE);
    const cachedResponse = await cache.match(request);
    if (cachedResponse) return cachedResponse;
    
    try {
        const networkResponse = await fetch(request);
        if (networkResponse.ok) {
            cache.put(request, networkResponse.clone());
        }
        return networkResponse;
    } catch (error) {
        return new Response(`<svg width="400" height="300" xmlns="http://www.w3.org/2000/svg">
            <rect width="100%" height="100%" fill="#f0f0f0"/>
            <text x="50%" y="50%" text-anchor="middle" dy=".3em" font-size="16" fill="#999">
                รูปภาพไม่สามารถโหลดได้
            </text>
        </svg>`, { headers: { 'Content-Type': 'image/svg+xml' } });
    }
}

function isStaticAsset(request) {
    const url = new URL(request.url);
    return url.pathname.endsWith('.css') ||
           url.pathname.endsWith('.js') ||
           url.pathname.endsWith('.woff2') ||
           url.hostname.includes('fonts.g');
}

function isImageRequest(request) {
    const url = new URL(request.url);
    return url.pathname.match(/\.(jpg|jpeg|png|gif|webp|svg|ico)$/i) ||
           url.hostname === 'cdn.shopify.com';
}

console.log('🎉 Ultimate Car Detail Service Worker 2025 Loaded!');
