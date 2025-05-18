document.addEventListener('DOMContentLoaded', () => {
    const themeToggle = document.getElementById('theme-toggle');
    const body = document.body;
    const heroBackground = document.querySelector('.hero-background');
    const currentYearSpan = document.getElementById('current-year');
    const mainHeader = document.getElementById('main-header'); // Get header element
    const mobileMenuToggle = document.getElementById('mobile-menu-toggle'); // Hamburger button
    const navRightGroup = document.querySelector('.nav-right-group'); // Nav links + theme toggle container
    const navLinks = document.querySelectorAll('.nav-links a[href^="#"]'); // Links for smooth scroll & menu close

    // --- Theme Toggle ---
    const userPrefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    const savedTheme = localStorage.getItem('theme');
    const heroButton = document.querySelector('.hero-button');

    function applyTheme(theme) {
        const isDark = theme === 'dark';
        // body.classList.toggle('dark-mode', isDark);
        document.documentElement.classList.toggle('dark-mode', isDark);
        const icon = themeToggle.querySelector('i');
        if (isDark) {
            icon.classList.remove('fa-moon'); icon.classList.add('fa-sun');
            themeToggle.setAttribute('aria-label', 'Switch to light mode');
            themeToggle.setAttribute('title', 'Switch to light mode');
        } else {
            icon.classList.remove('fa-sun'); icon.classList.add('fa-moon');
            themeToggle.setAttribute('aria-label', 'Switch to dark mode');
            themeToggle.setAttribute('title', 'Switch to dark mode');
        }
    }

    // let currentTheme = savedTheme || (userPrefersDark ? 'dark' : 'light');
    let currentTheme = 'dark'
    applyTheme(currentTheme);

    themeToggle.addEventListener('click', () => {
        // const newTheme = body.classList.contains('dark-mode') ? 'light' : 'dark';
        const newTheme = document.documentElement.classList.contains('dark-mode') ? 'light' : 'dark';

        localStorage.setItem('theme', newTheme);
        applyTheme(newTheme);
    });

    // --- Header Style on Scroll ---
    function handleHeaderScroll() {
        if (window.scrollY > 50) { // Add class after scrolling 50px
            mainHeader.classList.add('scrolled');
        } else {
            mainHeader.classList.remove('scrolled');
        }
    }
    window.addEventListener('scroll', handleHeaderScroll, { passive: true });
    handleHeaderScroll(); // Initial check


    // --- Hero Background Fade on Scroll ---
    function handleHeroFade() {
        if (!heroBackground) return;
        const scrollY = window.scrollY;
        const fadeEnd = window.innerHeight * 0.6; // Fade out over 60% of viewport height
        let opacity = Math.max(0, 1 - (scrollY / fadeEnd));
        heroBackground.style.opacity = opacity;
        // --- Apply opacity to the button ---
        if (heroButton) {
            heroButton.style.opacity = opacity;
            // Optional: Make button unclickable when mostly faded
            heroButton.style.pointerEvents = opacity <= 0.1 ? 'none' : 'auto';
        }
    }
    window.addEventListener('scroll', handleHeroFade, { passive: true });
    handleHeroFade(); // Initial check


    // --- Mobile Menu Toggle ---
    mobileMenuToggle.addEventListener('click', () => {
        const isOpened = body.classList.toggle('mobile-nav-open');
        mobileMenuToggle.setAttribute('aria-expanded', isOpened);
        // Optional: Change hamburger icon to 'X' when open
        const icon = mobileMenuToggle.querySelector('i');
        if(isOpened) {
            icon.classList.remove('fa-bars');
            icon.classList.add('fa-xmark');
            mobileMenuToggle.setAttribute('aria-label', 'Close navigation menu');
        } else {
             icon.classList.remove('fa-xmark');
             icon.classList.add('fa-bars');
             mobileMenuToggle.setAttribute('aria-label', 'Open navigation menu');
        }
    });

    // --- Smooth Scrolling & Close Mobile Menu on Link Click ---
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);

            if (targetElement) {
                const headerOffset = mainHeader.offsetHeight;
                // Use offsetHeight of the scrolled state if header is scrolled for accuracy
                const scrolledNavHeight = mainHeader.classList.contains('scrolled') ? mainHeader.querySelector('nav').offsetHeight + 16 : headerOffset; // +16 approx margin
                const elementPosition = targetElement.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - scrolledNavHeight;

                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });

                // Close mobile menu if it's open
                if (body.classList.contains('mobile-nav-open')) {
                    body.classList.remove('mobile-nav-open');
                    mobileMenuToggle.setAttribute('aria-expanded', 'false');
                    const icon = mobileMenuToggle.querySelector('i');
                    icon.classList.remove('fa-xmark');
                    icon.classList.add('fa-bars');
                    mobileMenuToggle.setAttribute('aria-label', 'Open navigation menu');
                }
            }
        });
    });

    // --- Update Footer Year ---
    if (currentYearSpan) {
        currentYearSpan.textContent = new Date().getFullYear();
    }

}); // End DOMContentLoaded