document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    const nameInput = document.getElementById('name');
    const passwordInput = document.getElementById('password');
    const loginButton = document.getElementById('loginButton');
    const loginMessage = document.getElementById('loginMessage');
    const nameError = document.getElementById('nameError');
    const passwordError = document.getElementById('passwordError');
    
    // Check if already logged in
    checkAuthStatus();
    
    async function checkAuthStatus() {
        try {
            const response = await fetch('/api/llm/auth/check', {
                method: 'GET',
                credentials: 'include'
            });
            
            if (response.ok) {
                const data = await response.json();
                if (data.authenticated) {
                    // Already logged in, redirect to main page
                    window.location.href = '/';
                }
            }
        } catch (error) {
            console.error('Error checking auth status:', error);
        }
    }
    
    loginForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Clear previous errors
        nameError.textContent = '';
        passwordError.textContent = '';
        loginMessage.textContent = '';
        loginMessage.className = 'login-message';
        
        // Get and trim values
        const name = nameInput.value.trim();
        const password = passwordInput.value.trim();
        
        // Validate inputs
        let hasError = false;
        
        if (!name) {
            nameError.textContent = 'Please enter your name';
            hasError = true;
        }
        
        if (!password) {
            passwordError.textContent = 'Please enter the password';
            hasError = true;
        }
        
        if (hasError) {
            return;
        }
        
        // Disable form during submission
        loginButton.disabled = true;
        loginButton.textContent = 'Logging in...';
        nameInput.disabled = true;
        passwordInput.disabled = true;
        
        try {
            const response = await fetch('/api/llm/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                credentials: 'include',
                body: JSON.stringify({
                    name: name,
                    password: password
                })
            });
            
            const data = await response.json();
            
            if (response.ok) {
                loginMessage.className = 'login-message success';
                loginMessage.textContent = 'Login successful! Redirecting...';
                
                // Store user info in session storage
                sessionStorage.setItem('userName', data.name);
                
                // Redirect to main page after a short delay
                setTimeout(() => {
                    window.location.href = '/';
                }, 1000);
            } else {
                // Show appropriate error message
                loginMessage.className = 'login-message error';
                
                if (response.status === 401) {
                    // Wrong password
                    loginMessage.textContent = 'Incorrect password. Please type "password" in the password field.';
                } else {
                    // Other errors
                    loginMessage.textContent = data.detail || 'Login failed. Please try again.';
                }
                
                // Re-enable form
                loginButton.disabled = false;
                loginButton.textContent = 'Login';
                nameInput.disabled = false;
                passwordInput.disabled = false;
                
                // Focus on password field for retry
                passwordInput.focus();
                passwordInput.select();
            }
        } catch (error) {
            console.error('Login error:', error);
            loginMessage.className = 'login-message error';
            loginMessage.textContent = 'Connection error. Please try again.';
            
            // Re-enable form
            loginButton.disabled = false;
            loginButton.textContent = 'Login';
            nameInput.disabled = false;
            passwordInput.disabled = false;
        }
    });
    
    // Handle Enter key in name field
    nameInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            e.preventDefault();
            passwordInput.focus();
        }
    });
    
    // Auto-focus on name input
    nameInput.focus();
});