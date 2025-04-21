/**
 * Gpgram Documentation - Documentation JavaScript
 * Handles interactive elements and functionality for documentation pages
 */

document.addEventListener('DOMContentLoaded', function() {
    // API Search functionality
    const searchInput = document.getElementById('api-search');
    if (searchInput) {
        const sidebarLinks = document.querySelectorAll('.sidebar-nav a');
        
        searchInput.addEventListener('input', function() {
            const searchTerm = this.value.toLowerCase();
            
            if (searchTerm.length === 0) {
                // Show all sections and links if search is empty
                document.querySelectorAll('.sidebar-section').forEach(section => {
                    section.style.display = 'block';
                });
                
                sidebarLinks.forEach(link => {
                    link.style.display = 'block';
                });
                
                return;
            }
            
            // Hide all sections initially
            document.querySelectorAll('.sidebar-section').forEach(section => {
                section.style.display = 'none';
            });
            
            // Filter links based on search term
            let hasResults = false;
            
            sidebarLinks.forEach(link => {
                const linkText = link.textContent.toLowerCase();
                const shouldShow = linkText.includes(searchTerm);
                
                link.style.display = shouldShow ? 'block' : 'none';
                
                if (shouldShow) {
                    hasResults = true;
                    // Show the parent section
                    const section = link.closest('.sidebar-section');
                    if (section) {
                        section.style.display = 'block';
                    }
                }
            });
            
            // Show a message if no results
            const noResultsMessage = document.getElementById('no-results-message');
            if (!hasResults) {
                if (!noResultsMessage) {
                    const message = document.createElement('div');
                    message.id = 'no-results-message';
                    message.textContent = 'No results found';
                    message.style.padding = '10px';
                    message.style.color = 'var(--text-light)';
                    message.style.fontStyle = 'italic';
                    
                    const sidebarNav = document.querySelector('.sidebar-nav');
                    sidebarNav.appendChild(message);
                }
            } else if (noResultsMessage) {
                noResultsMessage.remove();
            }
        });
    }
    
    // Table of Contents generation
    const generateTOC = () => {
        const content = document.querySelector('.api-details');
        const tocContainer = document.querySelector('.toc');
        
        if (!content || !tocContainer) return;
        
        const headings = content.querySelectorAll('h2, h3');
        if (headings.length === 0) return;
        
        const tocList = document.createElement('ul');
        
        headings.forEach((heading, index) => {
            // Add ID to the heading if it doesn't have one
            if (!heading.id) {
                heading.id = `heading-${index}`;
            }
            
            const listItem = document.createElement('li');
            const link = document.createElement('a');
            
            link.href = `#${heading.id}`;
            link.textContent = heading.textContent;
            
            // Add indentation for h3
            if (heading.tagName === 'H3') {
                listItem.style.paddingLeft = '20px';
            }
            
            listItem.appendChild(link);
            tocList.appendChild(listItem);
        });
        
        tocContainer.appendChild(tocList);
    };
    
    // Call TOC generation
    generateTOC();
    
    // Smooth scrolling for TOC links
    document.querySelectorAll('.toc a').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                const headerHeight = document.querySelector('header').offsetHeight;
                const targetPosition = targetElement.getBoundingClientRect().top + window.pageYOffset - headerHeight - 20;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // Highlight current section in sidebar
    const highlightCurrentSection = () => {
        const currentPath = window.location.pathname;
        const filename = currentPath.substring(currentPath.lastIndexOf('/') + 1);
        
        document.querySelectorAll('.sidebar-nav a').forEach(link => {
            const linkPath = link.getAttribute('href');
            const linkFilename = linkPath.substring(linkPath.lastIndexOf('/') + 1);
            
            if (linkFilename === filename) {
                link.classList.add('active');
            }
        });
    };
    
    // Call highlight function
    highlightCurrentSection();
    
    // Copy code blocks functionality
    const addCopyButtons = () => {
        document.querySelectorAll('.api-signature, pre code').forEach(block => {
            const container = block.tagName === 'CODE' ? block.parentElement : block;
            
            if (!container.querySelector('.copy-button')) {
                const copyButton = document.createElement('button');
                copyButton.className = 'copy-button';
                copyButton.textContent = 'Copy';
                
                copyButton.addEventListener('click', () => {
                    const code = block.textContent;
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
                
                container.style.position = 'relative';
                container.appendChild(copyButton);
            }
        });
    };
    
    // Call copy buttons function
    addCopyButtons();
    
    // Mobile sidebar toggle
    const createMobileSidebarToggle = () => {
        const sidebar = document.querySelector('.docs-sidebar');
        
        if (sidebar && window.innerWidth <= 1024 && !document.querySelector('.sidebar-toggle')) {
            const toggle = document.createElement('button');
            toggle.className = 'sidebar-toggle';
            toggle.innerHTML = 'Menu <span>&#9776;</span>';
            toggle.setAttribute('aria-label', 'Toggle sidebar');
            
            toggle.addEventListener('click', () => {
                sidebar.classList.toggle('active');
                toggle.classList.toggle('active');
            });
            
            const container = document.querySelector('.docs-container');
            container.insertBefore(toggle, container.firstChild);
            
            // Close sidebar when clicking outside
            document.addEventListener('click', (e) => {
                if (!sidebar.contains(e.target) && !toggle.contains(e.target) && sidebar.classList.contains('active')) {
                    sidebar.classList.remove('active');
                    toggle.classList.remove('active');
                }
            });
        } else if (window.innerWidth > 1024) {
            const toggle = document.querySelector('.sidebar-toggle');
            if (toggle) {
                toggle.remove();
                sidebar.classList.remove('active');
            }
        }
    };
    
    // Call on load and resize
    createMobileSidebarToggle();
    window.addEventListener('resize', createMobileSidebarToggle);
});

// Add CSS for elements created by JavaScript
const docStyle = document.createElement('style');
docStyle.textContent = `
    /* Copy Button */
    .copy-button {
        position: absolute;
        top: 0.5rem;
        right: 0.5rem;
        padding: 0.25rem 0.5rem;
        font-size: 0.8rem;
        background-color: rgba(255, 255, 255, 0.1);
        color: var(--text-color);
        border: none;
        border-radius: 3px;
        cursor: pointer;
        transition: all 0.2s ease;
    }
    
    .copy-button:hover {
        background-color: rgba(255, 255, 255, 0.2);
    }
    
    /* Mobile Sidebar Toggle */
    .sidebar-toggle {
        display: none;
    }
    
    @media (max-width: 1024px) {
        .sidebar-toggle {
            display: block;
            margin-bottom: var(--spacing-md);
            padding: var(--spacing-sm) var(--spacing-md);
            background-color: var(--primary-color);
            color: white;
            border: none;
            border-radius: var(--border-radius);
            cursor: pointer;
            font-weight: 600;
        }
        
        .sidebar-toggle span {
            margin-left: var(--spacing-sm);
        }
        
        .docs-sidebar {
            display: none;
        }
        
        .docs-sidebar.active {
            display: block;
        }
    }
`;

document.head.appendChild(docStyle);
