/**
 * Gpgram Documentation - Main JavaScript
 * Handles interactive elements and UI functionality
 */

document.addEventListener('DOMContentLoaded', function() {
    // Tab functionality for examples section
    const tabButtons = document.querySelectorAll('.tab-button');
    const tabPanes = document.querySelectorAll('.tab-pane');
    
    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remove active class from all buttons and panes
            tabButtons.forEach(btn => btn.classList.remove('active'));
            tabPanes.forEach(pane => pane.classList.remove('active'));
            
            // Add active class to clicked button and corresponding pane
            button.classList.add('active');
            const tabId = button.getAttribute('data-tab');
            document.getElementById(tabId).classList.add('active');
        });
    });
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            if (targetId === '#') return;
            
            const targetElement = document.querySelector(targetId);
            if (targetElement) {
                const headerHeight = document.querySelector('header').offsetHeight;
                const targetPosition = targetElement.getBoundingClientRect().top + window.pageYOffset - headerHeight;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Mobile navigation toggle
    const createMobileNav = () => {
        const header = document.querySelector('header');
        const nav = document.querySelector('nav');
        
        if (window.innerWidth <= 768 && !document.querySelector('.mobile-nav-toggle')) {
            const mobileNavToggle = document.createElement('button');
            mobileNavToggle.classList.add('mobile-nav-toggle');
            mobileNavToggle.innerHTML = '<span></span><span></span><span></span>';
            mobileNavToggle.setAttribute('aria-label', 'Toggle navigation');
            
            header.insertBefore(mobileNavToggle, nav);
            
            nav.classList.add('mobile-nav');
            
            mobileNavToggle.addEventListener('click', () => {
                mobileNavToggle.classList.toggle('active');
                nav.classList.toggle('active');
            });
            
            // Close mobile nav when clicking outside
            document.addEventListener('click', (e) => {
                if (!nav.contains(e.target) && !mobileNavToggle.contains(e.target)) {
                    mobileNavToggle.classList.remove('active');
                    nav.classList.remove('active');
                }
            });
        } else if (window.innerWidth > 768) {
            const mobileNavToggle = document.querySelector('.mobile-nav-toggle');
            if (mobileNavToggle) {
                mobileNavToggle.remove();
                nav.classList.remove('mobile-nav', 'active');
            }
        }
    };
    
    // Call on load and resize
    createMobileNav();
    window.addEventListener('resize', createMobileNav);
    
    // Add active class to current section in navigation
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('nav a[href^="#"]');
    
    const highlightNavigation = () => {
        const scrollPosition = window.scrollY + 100; // Offset for header
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.offsetHeight;
            const sectionId = section.getAttribute('id');
            
            if (scrollPosition >= sectionTop && scrollPosition < sectionTop + sectionHeight) {
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${sectionId}`) {
                        link.classList.add('active');
                    }
                });
            }
        });
    };
    
    window.addEventListener('scroll', highlightNavigation);
    
    // Copy code blocks functionality
    const addCopyButtons = () => {
        document.querySelectorAll('pre').forEach(pre => {
            if (!pre.querySelector('.copy-button')) {
                const copyButton = document.createElement('button');
                copyButton.className = 'copy-button';
                copyButton.textContent = 'Copy';
                
                copyButton.addEventListener('click', () => {
                    const code = pre.querySelector('code').textContent;
                    navigator.clipboard.writeText(code).then(() => {
                        copyButton.textContent = 'Copied!';
                        setTimeout(() => {
                            copyButton.textContent = 'Copy';
                        }, 2000);
                    }).catch(err => {
                        console.error('Failed to copy: ', err);
                        copyButton.textContent = 'Error';
                        setTimeout(() => {
                            copyButton.textContent = 'Copy';
                        }, 2000);
                    });
                });
                
                pre.appendChild(copyButton);
            }
        });
    };
    
    // Call after Prism.js has processed code blocks
    if (typeof Prism !== 'undefined') {
        Prism.hooks.add('complete', addCopyButtons);
    } else {
        window.addEventListener('load', addCopyButtons);
    }
});

// Add CSS for elements created by JavaScript
const style = document.createElement('style');
style.textContent = `
    /* Mobile Navigation */
    .mobile-nav-toggle {
        display: none;
    }
    
    @media (max-width: 768px) {
        .mobile-nav-toggle {
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            width: 30px;
            height: 21px;
            background: transparent;
            border: none;
            cursor: pointer;
            padding: 0;
            z-index: 10;
        }
        
        .mobile-nav-toggle span {
            display: block;
            width: 100%;
            height: 3px;
            background-color: var(--text-color);
            border-radius: 3px;
            transition: all 0.3s ease;
        }
        
        .mobile-nav-toggle.active span:nth-child(1) {
            transform: translateY(9px) rotate(45deg);
        }
        
        .mobile-nav-toggle.active span:nth-child(2) {
            opacity: 0;
        }
        
        .mobile-nav-toggle.active span:nth-child(3) {
            transform: translateY(-9px) rotate(-45deg);
        }
        
        .mobile-nav {
            position: absolute;
            top: 100%;
            left: 0;
            right: 0;
            background-color: var(--bg-color);
            box-shadow: var(--shadow-md);
            padding: 1rem;
            display: none;
        }
        
        .mobile-nav.active {
            display: block;
        }
        
        .mobile-nav ul {
            flex-direction: column;
        }
        
        .mobile-nav li {
            margin: 0.5rem 0;
        }
    }
    
    /* Copy Code Button */
    .copy-button {
        position: absolute;
        top: 0.5rem;
        right: 0.5rem;
        padding: 0.25rem 0.5rem;
        font-size: 0.8rem;
        background-color: rgba(255, 255, 255, 0.1);
        color: #abb2bf;
        border: none;
        border-radius: 3px;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .copy-button:hover {
        background-color: rgba(255, 255, 255, 0.2);
    }
    
    pre {
        position: relative;
    }
    
    /* Active navigation link */
    nav a.active {
        background-color: var(--bg-light);
        font-weight: bold;
    }
`;

document.head.appendChild(style);
