$(document).ready(function() {
    const body = $('body');
    const themeToggle = $('#theme-toggle');
    
    // Theme icons
    const icons = {
        light: '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg>',
        dark: '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"></path></svg>',
        system: '<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg>'
    };

    // Get system preference and saved theme
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)');
    const savedTheme = localStorage.getItem('theme') || 'system';
    
    function updateTheme(theme) {
        localStorage.setItem('theme', theme);
        
        if (theme === 'system') {
            body.removeClass('light-mode dark-mode').addClass(prefersDark.matches ? 'dark-mode' : 'light-mode');
            themeToggle.html(icons.system);
        } else if (theme === 'dark') {
            body.removeClass('light-mode dark-mode').addClass('dark-mode');
            themeToggle.html(icons.dark);
        } else {
            body.removeClass('light-mode dark-mode').addClass('light-mode');
            themeToggle.html(icons.light);
        }
    }

    // Initialize theme
    updateTheme(savedTheme);

    // Theme menu handlers
    const themeMenu = $('<div class="theme-menu">').insertAfter(themeToggle);
    themeMenu.html(`
        <div class="theme-option" data-theme="light">
            ${icons.light}
            <span>Light</span>
        </div>
        <div class="theme-option" data-theme="dark">
            ${icons.dark}
            <span>Dark</span>
        </div>
        <div class="theme-option" data-theme="system">
            ${icons.system}
            <span>System</span>
        </div>
    `);

    themeToggle.on('click', function(e) {
        e.stopPropagation();
        themeMenu.toggleClass('show');
    });

    $('.theme-option').on('click', function() {
        const newTheme = $(this).data('theme');
        updateTheme(newTheme);
        themeMenu.removeClass('show');
    });

    $(document).on('click', function(e) {
        if (!$(e.target).closest('.theme-menu').length) {
            themeMenu.removeClass('show');
        }
    });

    prefersDark.addEventListener('change', (e) => {
        if (localStorage.getItem('theme') === 'system') {
            updateTheme('system');
        }
    });
}); 