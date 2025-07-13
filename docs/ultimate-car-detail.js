/**
 * Ultimate Car Detail JavaScript 2025
 * Performance Optimized for Core Web Vitals
 * รองรับทุกอุปกรณ์ + PWA Ready
 */

class UltimateCarDetailManager {
    constructor() {
        this.isLoaded = false;
        this.performanceMetrics = {};
        this.init();
    }

    init() {
        // Critical path optimization
        this.preloadCriticalResources();
        this.initializeComponents();
        this.startPerformanceMonitoring();
        
        // DOM ready optimization
        if (document.readyState === 'loading') {
            document.addEventListener('DOMContentLoaded', () => this.onDOMReady());
        } else {
            this.onDOMReady();
        }
    }

    preloadCriticalResources() {
        // Preload next likely images
        const thumbnails = document.querySelectorAll('.thumbnail');
        thumbnails.forEach((thumb, index) => {
            if (index < 3) { // Preload first 3 images
                const link = document.createElement('link');
                link.rel = 'preload';
                link.as = 'image';
                link.href = thumb.src;
                document.head.appendChild(link);
            }
        });
    }

    onDOMReady() {
        this.setupImageGallery();
        this.setupLazyLoading();
        this.setupContactButtons();
        this.setupLoadingAnimations();
        this.setupAccessibility();
        this.setupPWAFeatures();
        this.isLoaded = true;
        
        // Dispatch custom event
        window.dispatchEvent(new CustomEvent('carDetailLoaded', {
            detail: { manager: this }
        }));
    }

    setupImageGallery() {
        const mainImage = document.getElementById('mainImage');
        const thumbnails = document.querySelectorAll('.thumbnail');
        
        if (!mainImage || !thumbnails.length) return;

        // Enhanced image switching with preloading
        thumbnails.forEach((thumbnail, index) => {
            thumbnail.addEventListener('click', (e) => {
                e.preventDefault();
                this.changeMainImage(thumbnail.src, thumbnails);
                
                // Preload next image
                const nextIndex = (index + 1) % thumbnails.length;
                this.preloadImage(thumbnails[nextIndex].src);
            });

            // Keyboard navigation
            thumbnail.addEventListener('keydown', (e) => {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    thumbnail.click();
                }
            });
        });

        // Touch/swipe support for mobile
        this.setupTouchGallery(mainImage, thumbnails);
        
        // Image zoom functionality
        this.setupImageZoom(mainImage);
    }

    changeMainImage(imageUrl, thumbnails) {
        const mainImage = document.getElementById('mainImage');
        if (!mainImage) return;

        // Smooth transition
        mainImage.style.opacity = '0.7';
        
        // Preload new image
        const newImage = new Image();
        newImage.onload = () => {
            mainImage.src = imageUrl;
            mainImage.style.opacity = '1';
            
            // Update active thumbnail
            thumbnails.forEach(thumb => {
                thumb.classList.remove('active');
                if (thumb.src === imageUrl) {
                    thumb.classList.add('active');
                }
            });
        };
        newImage.src = imageUrl;
    }

    setupTouchGallery(mainImage, thumbnails) {
        let startX = 0;
        let currentIndex = 0;

        mainImage.addEventListener('touchstart', (e) => {
            startX = e.touches[0].clientX;
        }, { passive: true });

        mainImage.addEventListener('touchend', (e) => {
            const endX = e.changedTouches[0].clientX;
            const diff = startX - endX;

            if (Math.abs(diff) > 50) { // Minimum swipe distance
                if (diff > 0) {
                    // Swipe left - next image
                    currentIndex = (currentIndex + 1) % thumbnails.length;
                } else {
                    // Swipe right - previous image
                    currentIndex = (currentIndex - 1 + thumbnails.length) % thumbnails.length;
                }
                thumbnails[currentIndex].click();
            }
        }, { passive: true });
    }

    setupImageZoom(mainImage) {
        mainImage.addEventListener('click', () => {
            this.openImageModal(mainImage.src);
        });

        // Double tap zoom on mobile
        let lastTap = 0;
        mainImage.addEventListener('touchend', (e) => {
            const currentTime = new Date().getTime();
            const tapLength = currentTime - lastTap;
            if (tapLength < 500 && tapLength > 0) {
                this.openImageModal(mainImage.src);
            }
            lastTap = currentTime;
        });
    }

    openImageModal(imageSrc) {
        // Create modal overlay
        const modal = document.createElement('div');
        modal.className = 'image-modal';
        modal.innerHTML = `
            <div class="modal-overlay" onclick="this.parentElement.remove()">
                <div class="modal-content" onclick="event.stopPropagation()">
                    <img src="${imageSrc}" alt="Car Image Zoom" class="zoomed-image">
                    <button class="close-modal" onclick="this.closest('.image-modal').remove()">
                        ✕
                    </button>
                </div>
            </div>
        `;

        // Add modal styles
        const modalStyles = `
            <style>
                .image-modal {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    z-index: 10000;
                    animation: fadeIn 0.3s ease;
                }
                .modal-overlay {
                    background: rgba(0,0,0,0.9);
                    width: 100%;
                    height: 100%;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    cursor: pointer;
                }
                .modal-content {
                    position: relative;
                    max-width: 90vw;
                    max-height: 90vh;
                    cursor: default;
                }
                .zoomed-image {
                    max-width: 100%;
                    max-height: 100%;
                    object-fit: contain;
                    border-radius: 8px;
                    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                }
                .close-modal {
                    position: absolute;
                    top: -40px;
                    right: 0;
                    background: rgba(255,255,255,0.9);
                    border: none;
                    width: 30px;
                    height: 30px;
                    border-radius: 50%;
                    cursor: pointer;
                    font-size: 18px;
                    color: #333;
                    transition: all 0.3s;
                }
                .close-modal:hover {
                    background: white;
                    transform: scale(1.1);
                }
                @keyframes fadeIn {
                    from { opacity: 0; }
                    to { opacity: 1; }
                }
            </style>
        `;

        document.head.insertAdjacentHTML('beforeend', modalStyles);
        document.body.appendChild(modal);

        // Close on escape key
        const handleEscape = (e) => {
            if (e.key === 'Escape') {
                modal.remove();
                document.removeEventListener('keydown', handleEscape);
            }
        };
        document.addEventListener('keydown', handleEscape);
    }

    setupLazyLoading() {
        // Enhanced intersection observer for images
        const imageObserver = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    this.loadImage(img);
                    imageObserver.unobserve(img);
                }
            });
        }, {
            root: null,
            rootMargin: '50px',
            threshold: 0.1
        });

        // Observe all lazy images
        document.querySelectorAll('img[loading="lazy"]').forEach(img => {
            imageObserver.observe(img);
        });
    }

    loadImage(img) {
        // Add loading skeleton
        img.classList.add('skeleton');
        
        const tempImg = new Image();
        tempImg.onload = () => {
            img.src = tempImg.src;
            img.classList.remove('skeleton');
            img.style.opacity = '1';
        };
        tempImg.onerror = () => {
            img.classList.remove('skeleton');
            img.alt = 'รูปภาพไม่สามารถโหลดได้';
        };
        tempImg.src = img.dataset.src || img.src;
    }

    preloadImage(src) {
        const img = new Image();
        img.src = src;
    }

    setupContactButtons() {
        const contactButtons = document.querySelectorAll('.contact-button');
        
        contactButtons.forEach(button => {
            // Enhanced click tracking
            button.addEventListener('click', (e) => {
                this.trackContactClick(button.textContent);
                
                // Add ripple effect
                this.addRippleEffect(button, e);
            });

            // Phone number formatting and validation
            if (button.textContent.includes('โทร')) {
                const phoneMatch = button.textContent.match(/[\d-]+/);
                if (phoneMatch) {
                    const formattedPhone = this.formatPhoneNumber(phoneMatch[0]);
                    button.href = `tel:${formattedPhone}`;
                }
            }
        });
    }

    addRippleEffect(button, event) {
        const ripple = document.createElement('span');
        const rect = button.getBoundingClientRect();
        const size = Math.max(rect.width, rect.height);
        const x = event.clientX - rect.left - size / 2;
        const y = event.clientY - rect.top - size / 2;
        
        ripple.style.cssText = `
            position: absolute;
            border-radius: 50%;
            background: rgba(255,255,255,0.6);
            transform: scale(0);
            animation: ripple 0.6s linear;
            left: ${x}px;
            top: ${y}px;
            width: ${size}px;
            height: ${size}px;
            pointer-events: none;
        `;
        
        // Add ripple animation
        if (!document.querySelector('#ripple-style')) {
            const style = document.createElement('style');
            style.id = 'ripple-style';
            style.textContent = `
                @keyframes ripple {
                    to {
                        transform: scale(4);
                        opacity: 0;
                    }
                }
            `;
            document.head.appendChild(style);
        }
        
        button.style.position = 'relative';
        button.style.overflow = 'hidden';
        button.appendChild(ripple);
        
        setTimeout(() => ripple.remove(), 600);
    }

    formatPhoneNumber(phone) {
        return phone.replace(/\D/g, '');
    }

    trackContactClick(buttonText) {
        // Analytics tracking
        if (typeof gtag !== 'undefined') {
            gtag('event', 'contact_click', {
                'contact_method': buttonText,
                'page_url': window.location.href
            });
        }
        
        console.log('Contact clicked:', buttonText);
    }

    setupLoadingAnimations() {
        // Animate loading elements
        const loadingElements = document.querySelectorAll('.loading');
        
        const animationObserver = new IntersectionObserver((entries) => {
            entries.forEach((entry, index) => {
                if (entry.isIntersecting) {
                    setTimeout(() => {
                        entry.target.style.opacity = '1';
                        entry.target.style.transform = 'translateY(0)';
                    }, index * 100);
                    animationObserver.unobserve(entry.target);
                }
            });
        }, { threshold: 0.1 });

        loadingElements.forEach(el => {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            el.style.transition = 'all 0.6s cubic-bezier(0.4, 0, 0.2, 1)';
            animationObserver.observe(el);
        });
    }

    setupAccessibility() {
        // Enhanced keyboard navigation
        const focusableElements = document.querySelectorAll(
            'a, button, input, select, textarea, [tabindex]:not([tabindex="-1"])'
        );

        focusableElements.forEach(el => {
            el.addEventListener('focus', (e) => {
                e.target.style.outline = '2px solid #f47b20';
                e.target.style.outlineOffset = '2px';
            });

            el.addEventListener('blur', (e) => {
                e.target.style.outline = '';
                e.target.style.outlineOffset = '';
            });
        });

        // ARIA labels for images
        document.querySelectorAll('.thumbnail').forEach((thumb, index) => {
            thumb.setAttribute('aria-label', `รูปรถยนต์ที่ ${index + 1}`);
            thumb.setAttribute('role', 'button');
            thumb.setAttribute('tabindex', '0');
        });
    }

    setupPWAFeatures() {
        // Register service worker if available
        if ('serviceWorker' in navigator) {
            navigator.serviceWorker.register('/sw.js').catch(console.log);
        }

        // Add to home screen prompt
        let deferredPrompt;
        window.addEventListener('beforeinstallprompt', (e) => {
            e.preventDefault();
            deferredPrompt = e;
            this.showInstallButton();
        });
    }

    showInstallButton() {
        const installButton = document.createElement('button');
        installButton.textContent = '📱 เพิ่มในหน้าจอหลัก';
        installButton.className = 'install-button';
        installButton.style.cssText = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: var(--primary);
            color: white;
            border: none;
            padding: 12px 16px;
            border-radius: 8px;
            font-weight: 600;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            z-index: 1000;
            transition: all 0.3s;
        `;

        installButton.addEventListener('click', async () => {
            if (deferredPrompt) {
                deferredPrompt.prompt();
                const result = await deferredPrompt.userChoice;
                if (result.outcome === 'accepted') {
                    installButton.remove();
                }
                deferredPrompt = null;
            }
        });

        document.body.appendChild(installButton);
        
        // Auto-hide after 10 seconds
        setTimeout(() => {
            installButton.style.opacity = '0';
            setTimeout(() => installButton.remove(), 300);
        }, 10000);
    }

    initializeComponents() {
        // Initialize any additional components
        this.setupShareButton();
        this.setupPrintButton();
        this.setupFavorites();
    }

    setupShareButton() {
        if (navigator.share) {
            const shareButton = document.createElement('button');
            shareButton.textContent = '🔗 แชร์';
            shareButton.className = 'share-button contact-button';
            
            shareButton.addEventListener('click', async () => {
                try {
                    await navigator.share({
                        title: document.title,
                        text: document.querySelector('meta[name="description"]').content,
                        url: window.location.href
                    });
                } catch (err) {
                    console.log('Error sharing:', err);
                }
            });

            const contactCard = document.querySelector('.contact-card');
            if (contactCard) {
                contactCard.appendChild(shareButton);
            }
        }
    }

    setupPrintButton() {
        const printButton = document.createElement('button');
        printButton.textContent = '🖨️ พิมพ์';
        printButton.className = 'print-button contact-button';
        
        printButton.addEventListener('click', () => {
            window.print();
        });

        const contactCard = document.querySelector('.contact-card');
        if (contactCard) {
            contactCard.appendChild(printButton);
        }
    }

    setupFavorites() {
        const favButton = document.createElement('button');
        favButton.textContent = '❤️ เพิ่มในรายการโปรด';
        favButton.className = 'favorite-button contact-button';
        
        const carHandle = window.location.pathname.split('/').pop().replace('.html', '');
        const isInFavorites = this.getFavorites().includes(carHandle);
        
        if (isInFavorites) {
            favButton.textContent = '💔 ลบจากรายการโปรด';
            favButton.style.background = '#e74c3c';
        }

        favButton.addEventListener('click', () => {
            this.toggleFavorite(carHandle);
        });

        const contactCard = document.querySelector('.contact-card');
        if (contactCard) {
            contactCard.appendChild(favButton);
        }
    }

    getFavorites() {
        return JSON.parse(localStorage.getItem('carFavorites') || '[]');
    }

    toggleFavorite(carHandle) {
        let favorites = this.getFavorites();
        const favButton = document.querySelector('.favorite-button');
        
        if (favorites.includes(carHandle)) {
            favorites = favorites.filter(h => h !== carHandle);
            favButton.textContent = '❤️ เพิ่มในรายการโปรด';
            favButton.style.background = '';
        } else {
            favorites.push(carHandle);
            favButton.textContent = '💔 ลบจากรายการโปรด';
            favButton.style.background = '#e74c3c';
        }
        
        localStorage.setItem('carFavorites', JSON.stringify(favorites));
    }

    startPerformanceMonitoring() {
        // Core Web Vitals monitoring
        if ('PerformanceObserver' in window) {
            // LCP monitoring
            new PerformanceObserver((list) => {
                for (const entry of list.getEntries()) {
                    this.performanceMetrics.lcp = entry.startTime;
                    console.log('LCP:', entry.startTime);
                }
            }).observe({entryTypes: ['largest-contentful-paint']});

            // FID monitoring
            new PerformanceObserver((list) => {
                for (const entry of list.getEntries()) {
                    this.performanceMetrics.fid = entry.processingStart - entry.startTime;
                    console.log('FID:', this.performanceMetrics.fid);
                }
            }).observe({entryTypes: ['first-input']});

            // CLS monitoring
            new PerformanceObserver((list) => {
                let clsValue = 0;
                for (const entry of list.getEntries()) {
                    if (!entry.hadRecentInput) {
                        clsValue += entry.value;
                    }
                }
                this.performanceMetrics.cls = clsValue;
                console.log('CLS:', clsValue);
            }).observe({entryTypes: ['layout-shift']});
        }
    }

    getPerformanceMetrics() {
        return this.performanceMetrics;
    }
}

// Initialize when script loads
const carDetailManager = new UltimateCarDetailManager();

// Global functions for backwards compatibility
window.changeMainImage = function(imageUrl) {
    const thumbnails = document.querySelectorAll('.thumbnail');
    carDetailManager.changeMainImage(imageUrl, thumbnails);
};

// Export for module usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = UltimateCarDetailManager;
}
