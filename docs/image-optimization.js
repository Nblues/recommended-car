
// Image Optimization JavaScript
document.addEventListener('DOMContentLoaded', function() {
  
  // Intersection Observer สำหรับ Lazy Loading
  const imageObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const img = entry.target;
        img.classList.add('loaded');
        observer.unobserve(img);
      }
    });
  }, {
    rootMargin: '50px 0px'
  });

  // Observe ทุกรูปที่ lazy load
  document.querySelectorAll('img[loading="lazy"]').forEach(img => {
    imageObserver.observe(img);
  });

  // Performance monitoring
  if ('PerformanceObserver' in window) {
    const perfObserver = new PerformanceObserver((list) => {
      for (const entry of list.getEntries()) {
        if (entry.name.includes('LCP')) {
          console.log('LCP:', entry.startTime);
        }
      }
    });
    
    try {
      perfObserver.observe({entryTypes: ['largest-contentful-paint']});
    } catch (e) {
      // Fallback for older browsers
    }
  }

  // Preload next images
  const preloadNextImages = () => {
    const visibleImages = document.querySelectorAll('img[loading="lazy"]');
    visibleImages.forEach((img, index) => {
      if (index < 3) { // Preload next 3 images
        const link = document.createElement('link');
        link.rel = 'prefetch';
        link.href = img.src;
        document.head.appendChild(link);
      }
    });
  };

  // Preload after page load
  window.addEventListener('load', () => {
    setTimeout(preloadNextImages, 2000);
  });

});
