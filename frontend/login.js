const API_BASE_URL = 'http://127.0.0.1:8000';

document.getElementById('loginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const messageDiv = document.getElementById('loginMessage');
    
    // Clear previous messages
    messageDiv.className = 'message';
    messageDiv.textContent = '';
    
    try {
        // Create form data for OAuth2 password flow
        const formData = new URLSearchParams();
        formData.append('username', username);
        formData.append('password', password);
        
        const response = await fetch(`${API_BASE_URL}/api/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: formData
        });
        
        const data = await response.json();
        
        if (response.ok) {
            // Store token in localStorage
            localStorage.setItem('access_token', data.access_token);
            
            messageDiv.className = 'message success';
            messageDiv.textContent = 'Login successful! Redirecting...';
            
            // Redirect to dashboard after 1 second
            setTimeout(() => {
                window.location.href = 'dashboard.html';
            }, 1000);
        } else {
            messageDiv.className = 'message error';
            messageDiv.textContent = data.detail || 'Login failed. Please check your credentials.';
        }
    } catch (error) {
        messageDiv.className = 'message error';
        messageDiv.textContent = 'Unable to connect. Please check your credentials and try again.';
        console.error('Error:', error);
    }
});
