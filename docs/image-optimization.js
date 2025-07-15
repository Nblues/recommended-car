
// Image Optimization JavaScript with Enhanced Error Handling
document.addEventListener('DOMContentLoaded', function() {
  
  // Error tracking
  const errorTracker = {
    imageErrors: 0,
    maxErrors: 10,
    logError: function(message, details) {
      if (this.imageErrors < this.maxErrors) {
        console.warn('Image Error:', message, details);
        this.imageErrors++;
      }
    }
  };

  // CORS-friendly image loader
  function loadImageWithFallback(img, primarySrc, fallbackSrc) {
    return new Promise((resolve, reject) => {
      const tempImg = new Image();
      
      tempImg.onload = function() {
        img.src = primarySrc;
        img.classList.add('loaded');
        resolve(img);
      };
      
      tempImg.onerror = function() {
        errorTracker.logError('Primary image failed', {url: primarySrc});
        
        // Try fallback
        if (fallbackSrc && fallbackSrc !== primarySrc) {
          const fallbackImg = new Image();
          fallbackImg.onload = function() {
            img.src = fallbackSrc;
            img.classList.add('loaded', 'fallback');
            resolve(img);
          };
          fallbackImg.onerror = function() {
            errorTracker.logError('Fallback image failed', {url: fallbackSrc});
            img.src = 'https://via.placeholder.com/300x200?text=Error+Loading+Image';
            img.classList.add('loaded', 'error');
            resolve(img);
          };
          fallbackImg.src = fallbackSrc;
        } else {
          img.src = 'https://via.placeholder.com/300x200?text=Error+Loading+Image';
          img.classList.add('loaded', 'error');
          resolve(img);
        }
      };
      
      // Set crossOrigin for CORS support
      tempImg.crossOrigin = 'anonymous';
      tempImg.src = primarySrc;
    });
  }

  // Enhanced Intersection Observer with error handling
  let imageObserver;
  
  if ('IntersectionObserver' in window) {
    imageObserver = new IntersectionObserver((entries, observer) => {
      entries.forEach(entry => {
        if (entry.isIntersecting) {
          const img = entry.target;
          const primarySrc = img.dataset.src || img.src;
          const fallbackSrc = img.dataset.fallback;
          
          loadImageWithFallback(img, primarySrc, fallbackSrc)
            .then(() => {
              observer.unobserve(img);
            })
            .catch(error => {
              errorTracker.logError('Image loading failed', {error: error.message});
              observer.unobserve(img);
            });
        }
      });
    }, {
      rootMargin: '50px 0px',
      threshold: 0.1
    });
  } else {
    // Fallback for older browsers
    console.warn('IntersectionObserver not supported, using fallback');
    const images = document.querySelectorAll('img[loading="lazy"]');
    images.forEach(img => {
      const primarySrc = img.dataset.src || img.src;
      const fallbackSrc = img.dataset.fallback;
      loadImageWithFallback(img, primarySrc, fallbackSrc);
    });
  }

  // Observe lazy loading images
  if (imageObserver) {
    document.querySelectorAll('img[loading="lazy"]').forEach(img => {
      // Add fallback data attribute if not present
      if (!img.dataset.fallback) {
        img.dataset.fallback = 'https://via.placeholder.com/300x200?text=Loading...';
      }
      imageObserver.observe(img);
    });
  }

  // Performance monitoring with error handling
  if ('PerformanceObserver' in window) {
    try {
      const perfObserver = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          if (entry.entryType === 'largest-contentful-paint') {
            console.log('LCP:', entry.startTime + 'ms');
            
            // Alert if LCP is too slow
            if (entry.startTime > 2500) {
              console.warn('LCP is slow:', entry.startTime + 'ms');
            }
          }
        }
      });
      
      perfObserver.observe({entryTypes: ['largest-contentful-paint']});
      
      // Also observe layout shifts
      const clsObserver = new PerformanceObserver((list) => {
        for (const entry of list.getEntries()) {
          if (entry.entryType === 'layout-shift' && !entry.hadRecentInput) {
            console.log('CLS:', entry.value);
            if (entry.value > 0.1) {
              console.warn('High layout shift detected:', entry.value);
            }
          }
        }
      });
      
      clsObserver.observe({entryTypes: ['layout-shift']});
      
    } catch (e) {
      console.warn('Performance monitoring not available:', e.message);
    }
  }

  // Preload next images with error handling
  const preloadNextImages = () => {
    try {
      const visibleImages = document.querySelectorAll('img[loading="lazy"]:not(.loaded)');
      const preloadPromises = [];
      
      visibleImages.forEach((img, index) => {
        if (index < 3) { // Preload next 3 images
          const link = document.createElement('link');
          link.rel = 'prefetch';
          link.href = img.dataset.src || img.src;
          link.onerror = () => errorTracker.logError('Preload failed', {url: link.href});
          document.head.appendChild(link);
        }
      });
      
    } catch (e) {
      errorTracker.logError('Preload error', {error: e.message});
    }
  };

  // Image loading progress indicator
  function updateLoadingProgress() {
    const totalImages = document.querySelectorAll('img[loading="lazy"]').length;
    const loadedImages = document.querySelectorAll('img[loading="lazy"].loaded').length;
    
    if (totalImages > 0) {
      const progress = Math.round((loadedImages / totalImages) * 100);
      
      // Dispatch custom event for progress tracking
      const progressEvent = new CustomEvent('imageLoadingProgress', {
        detail: { progress, loaded: loadedImages, total: totalImages }
      });
      document.dispatchEvent(progressEvent);
    }
  }

  // Monitor image loading progress
  const progressInterval = setInterval(() => {
    updateLoadingProgress();
    
    const loadedImages = document.querySelectorAll('img[loading="lazy"].loaded').length;
    const totalImages = document.querySelectorAll('img[loading="lazy"]').length;
    
    if (loadedImages >= totalImages) {
      clearInterval(progressInterval);
      console.log('All images loaded successfully');
    }
  }, 1000);

  // Preload after page load with delay
  window.addEventListener('load', () => {
    setTimeout(preloadNextImages, 2000);
  });

  // Global error handler for uncaught image errors
  window.addEventListener('error', (event) => {
    if (event.target && event.target.tagName === 'IMG') {
      errorTracker.logError('Global image error', {
        src: event.target.src,
        message: event.message
      });
    }
  }, true);

  // Expose error stats for debugging
  window.imageErrorStats = errorTracker;
});

// Service Worker registration with error handling
if ('serviceWorker' in navigator) {
  navigator.serviceWorker.register('sw.js')
    .then(registration => {
      console.log('SW registered successfully');
      
      // Listen for updates
      registration.addEventListener('updatefound', () => {
        console.log('SW update found');
      });
    })
    .catch(error => {
      console.warn('SW registration failed:', error);
      // Continue without service worker
    });
}
