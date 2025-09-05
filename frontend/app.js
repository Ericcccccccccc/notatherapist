document.addEventListener('DOMContentLoaded', function() {
    // Check authentication first
    checkAuthentication();
    
    const navbar = document.querySelector('.navbar');
    const navLinks = document.querySelectorAll('.nav-link');
    const contactForm = document.getElementById('contactForm');
    const featureCards = document.querySelectorAll('.feature-card');
    
    async function checkAuthentication() {
        try {
            const response = await fetch('/api/llm/auth/check', {
                method: 'GET',
                credentials: 'include'
            });
            
            if (!response.ok) {
                // Not authenticated, redirect to login
                window.location.href = '/login.html';
                return;
            }
            
            const data = await response.json();
            if (!data.authenticated) {
                window.location.href = '/login.html';
                return;
            }
            
            // User is authenticated, show greeting
            displayUserGreeting(data.name);
            
        } catch (error) {
            console.error('Auth check failed:', error);
            window.location.href = '/login.html';
        }
    }
    
    function displayUserGreeting(name) {
        const navContainer = document.querySelector('.nav-container');
        const navMenu = document.querySelector('.nav-menu');
        
        // Create user info element
        const userInfo = document.createElement('div');
        userInfo.className = 'user-info';
        userInfo.style.display = 'flex';
        userInfo.style.alignItems = 'center';
        userInfo.style.marginLeft = 'auto';
        
        const greeting = document.createElement('span');
        greeting.className = 'user-greeting';
        greeting.textContent = `Hi, ${name}!`;
        
        const logoutLink = document.createElement('a');
        logoutLink.href = '#';
        logoutLink.className = 'logout-link';
        logoutLink.textContent = 'Logout';
        logoutLink.onclick = async function(e) {
            e.preventDefault();
            await logout();
        };
        
        userInfo.appendChild(greeting);
        userInfo.appendChild(logoutLink);
        
        // Insert after nav menu
        navMenu.parentNode.insertBefore(userInfo, navMenu.nextSibling);
    }
    
    async function logout() {
        try {
            const response = await fetch('/api/llm/auth/logout', {
                method: 'POST',
                credentials: 'include'
            });
            
            if (response.ok) {
                sessionStorage.clear();
                window.location.href = '/login.html';
            }
        } catch (error) {
            console.error('Logout failed:', error);
        }
    }
    
    let lastScrollTop = 0;
    window.addEventListener('scroll', function() {
        let scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        if (scrollTop > 100) {
            navbar.style.background = 'rgba(255, 255, 255, 0.95)';
            navbar.style.backdropFilter = 'blur(10px)';
            navbar.style.boxShadow = '0 5px 30px rgba(0, 0, 0, 0.1)';
        } else {
            navbar.style.background = 'var(--white)';
            navbar.style.backdropFilter = 'none';
            navbar.style.boxShadow = '0 2px 10px rgba(0, 0, 0, 0.05)';
        }
        
        if (scrollTop > lastScrollTop && scrollTop > 200) {
            navbar.style.transform = 'translateY(-100%)';
        } else {
            navbar.style.transform = 'translateY(0)';
        }
        
        lastScrollTop = scrollTop;
    });
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            if (targetSection) {
                const offsetTop = targetSection.offsetTop - 80;
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
            }
            
            navLinks.forEach(l => l.classList.remove('active'));
            this.classList.add('active');
        });
    });
    
    const observerOptions = {
        threshold: 0.5,
        rootMargin: '0px 0px -100px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const id = entry.target.getAttribute('id');
                navLinks.forEach(link => {
                    link.classList.remove('active');
                    if (link.getAttribute('href') === `#${id}`) {
                        link.classList.add('active');
                    }
                });
            }
        });
    }, observerOptions);
    
    document.querySelectorAll('section[id]').forEach(section => {
        observer.observe(section);
    });
    
    const fadeObserver = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                fadeObserver.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });
    
    featureCards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        fadeObserver.observe(card);
    });
    
    featureCards.forEach((card, index) => {
        card.addEventListener('mouseenter', function() {
            this.style.transition = 'all 0.3s ease';
        });
        
        setTimeout(() => {
            card.style.transition = 'all 0.6s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
    
    const chatInput = document.getElementById('chatInput');
    const sendButton = document.getElementById('sendButton');
    const responseArea = document.getElementById('responseArea');
    
    async function sendMessage() {
        const message = chatInput.value.trim();
        
        if (!message) return;
        
        // Show loading state
        responseArea.classList.add('active', 'loading');
        responseArea.innerHTML = '<div class="loading-dots">Thinking<span>.</span><span>.</span><span>.</span></div>';
        
        sendButton.disabled = true;
        sendButton.style.opacity = '0.6';
        chatInput.value = '';
        
        try {
            // Send to LLM Gateway at port 5004
            const response = await fetch('/api/llm/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    conversation_id: sessionStorage.getItem('conversation_id') || generateConversationId()
                })
            });
            
            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }
            
            const data = await response.json();
            
            // Display the response
            responseArea.classList.remove('loading');
            responseArea.textContent = data.response || data.message || 'I received your message but had trouble processing it.';
            
            // Store conversation ID if provided
            if (data.conversation_id) {
                sessionStorage.setItem('conversation_id', data.conversation_id);
            }
            
        } catch (error) {
            console.error('Error sending message:', error);
            responseArea.classList.remove('loading');
            responseArea.innerHTML = `
                <div class="error-message">
                    <strong>Connection Error:</strong> Unable to reach the AI service. 
                    <br><small>The backend service might not be running yet.</small>
                </div>
            `;
        } finally {
            sendButton.disabled = false;
            sendButton.style.opacity = '1';
        }
    }
    
    function generateConversationId() {
        return 'conv_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
    }
    
    sendButton.addEventListener('click', sendMessage);
    
    chatInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    
    
    contactForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const name = document.getElementById('name').value;
        const email = document.getElementById('email').value;
        const message = document.getElementById('message').value;
        
        const submitButton = this.querySelector('.submit-button');
        const originalText = submitButton.textContent;
        
        submitButton.textContent = 'Sending...';
        submitButton.disabled = true;
        submitButton.style.opacity = '0.7';
        
        setTimeout(() => {
            submitButton.textContent = 'Message Sent!';
            submitButton.style.background = 'linear-gradient(135deg, #10B981, #059669)';
            
            this.reset();
            
            setTimeout(() => {
                submitButton.textContent = originalText;
                submitButton.disabled = false;
                submitButton.style.opacity = '1';
                submitButton.style.background = 'linear-gradient(135deg, var(--primary-color), var(--secondary-color))';
            }, 2000);
        }, 1500);
    });
    
    let mouseX = 0;
    let mouseY = 0;
    let currentX = 0;
    let currentY = 0;
    
    document.addEventListener('mousemove', function(e) {
        mouseX = e.clientX;
        mouseY = e.clientY;
    });
    
    function animateCursor() {
        const hero = document.querySelector('.hero');
        const rect = hero.getBoundingClientRect();
        
        if (mouseY < rect.bottom) {
            currentX += (mouseX - currentX) * 0.1;
            currentY += (mouseY - currentY) * 0.1;
            
            const moveX = (currentX - window.innerWidth / 2) * 0.01;
            const moveY = (currentY - window.innerHeight / 2) * 0.01;
            
            hero.style.transform = `translate(${moveX}px, ${moveY}px)`;
        }
        
        requestAnimationFrame(animateCursor);
    }
    
    animateCursor();
    
    console.log('NotATherapist App Initialized');
});