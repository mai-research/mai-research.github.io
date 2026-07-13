document.addEventListener('DOMContentLoaded', () => {
    const body = document.body;
    const heroBackground = document.querySelector('.hero-background');
    const heroButton = document.querySelector('.hero-button');
    const currentYearSpan = document.getElementById('current-year');
    const mainHeader = document.getElementById('main-header');
    const mobileMenuToggle = document.getElementById('mobile-menu-toggle');
    const navRightGroup = document.querySelector('.nav-right-group');
    const navLinks = document.querySelectorAll('.nav-links a[href^="#"]');
    const firstNavLink = navLinks[0];
    let pendingNavFocusHandler = null;
    const prefersReducedMotion = window.matchMedia
        && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

    function setupThemeToggle() {
        const themeToggle = document.getElementById('theme-toggle');
        if (!themeToggle) return;

        const icon = themeToggle.querySelector('i');
        if (!icon) return;

        function applyTheme(theme) {
            const isDark = theme === 'dark';
            document.documentElement.classList.toggle('dark-mode', isDark);
            icon.classList.toggle('fa-moon', !isDark);
            icon.classList.toggle('fa-sun', isDark);
            const label = isDark ? 'Switch to light mode' : 'Switch to dark mode';
            themeToggle.setAttribute('aria-label', label);
            themeToggle.setAttribute('title', label);
        }

        applyTheme('dark');

        themeToggle.addEventListener('click', () => {
            const newTheme = document.documentElement.classList.contains('dark-mode')
                ? 'light'
                : 'dark';
            localStorage.setItem('theme', newTheme);
            applyTheme(newTheme);
        });
    }

    setupThemeToggle();

    function handleHeaderScroll() {
        if (!mainHeader) return;
        mainHeader.classList.toggle('scrolled', window.scrollY > 50);
    }

    if (mainHeader) {
        window.addEventListener('scroll', handleHeaderScroll, { passive: true });
        handleHeaderScroll();
    }

    function handleHeroFade() {
        if (!heroBackground) return;
        const fadeEnd = window.innerHeight * 0.6;
        const opacity = Math.max(0, 1 - (window.scrollY / fadeEnd));
        heroBackground.style.opacity = opacity;

        if (heroButton) {
            heroButton.style.opacity = opacity;
            heroButton.style.pointerEvents = opacity <= 0.1 ? 'none' : 'auto';
        }
    }

    if (heroBackground) {
        window.addEventListener('scroll', handleHeroFade, { passive: true });
        handleHeroFade();
    }

    function setMobileMenuState(isOpen) {
        body.classList.toggle('mobile-nav-open', isOpen);
        if (!isOpen && navRightGroup && pendingNavFocusHandler) {
            navRightGroup.removeEventListener('transitionend', pendingNavFocusHandler);
            pendingNavFocusHandler = null;
        }
        if (!mobileMenuToggle) return;

        mobileMenuToggle.setAttribute('aria-expanded', String(isOpen));
        mobileMenuToggle.setAttribute(
            'aria-label',
            isOpen ? 'Close navigation menu' : 'Open navigation menu'
        );

        const icon = mobileMenuToggle.querySelector('i');
        if (icon) {
            icon.classList.toggle('fa-bars', !isOpen);
            icon.classList.toggle('fa-xmark', isOpen);
        }
    }

    function focusFirstNavLinkAfterOpen() {
        if (!firstNavLink) return;
        if (!navRightGroup) {
            firstNavLink.focus();
            return;
        }

        pendingNavFocusHandler = () => {
            pendingNavFocusHandler = null;
            if (body.classList.contains('mobile-nav-open')) {
                firstNavLink.focus();
            }
        };
        navRightGroup.addEventListener('transitionend', pendingNavFocusHandler, { once: true });
    }

    if (mobileMenuToggle) {
        mobileMenuToggle.addEventListener('click', () => {
            const isOpen = !body.classList.contains('mobile-nav-open');
            setMobileMenuState(isOpen);
            if (isOpen) {
                focusFirstNavLinkAfterOpen();
            }
        });

        document.addEventListener('keydown', event => {
            if (event.key === 'Escape' && body.classList.contains('mobile-nav-open')) {
                setMobileMenuState(false);
                mobileMenuToggle.focus();
            }
        });
    }

    function handleViewportResize() {
        if (window.innerWidth > 768 && body.classList.contains('mobile-nav-open')) {
            setMobileMenuState(false);
        }
    }

    window.addEventListener('resize', handleViewportResize);

    navLinks.forEach(link => {
        link.addEventListener('click', event => {
            const targetId = link.getAttribute('href');
            const targetElement = targetId ? document.querySelector(targetId) : null;
            if (!targetElement) return;

            event.preventDefault();
            const headerOffset = mainHeader ? mainHeader.offsetHeight : 0;
            const elementPosition = targetElement.getBoundingClientRect().top;
            const offsetPosition = elementPosition + window.pageYOffset - headerOffset;

            window.scrollTo({
                top: offsetPosition,
                behavior: prefersReducedMotion ? 'auto' : 'smooth'
            });

            if (body.classList.contains('mobile-nav-open')) {
                setMobileMenuState(false);
            }
        });
    });

    if (currentYearSpan) {
        currentYearSpan.textContent = new Date().getFullYear();
    }
});
