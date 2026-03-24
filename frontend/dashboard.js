const API_BASE_URL = 'http://127.0.0.1:8000';

// Check if user is logged in
const token = localStorage.getItem('access_token');
if (!token) {
    window.location.href = 'index.html';
}

// Fetch user details on page load
async function loadUserDetails() {
    const messageDiv = document.getElementById('dashboardMessage');
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/auth/me`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });
        
        if (response.ok) {
            const user = await response.json();
            
            // Update UI with user details - only update elements that exist
            const userNameEl = document.getElementById('userName');
            if (userNameEl) {
                userNameEl.textContent = user.username;
            }
            
            // These elements are on the profile page, not dashboard
            const userFullNameEl = document.getElementById('userFullName');
            const userUsernameEl = document.getElementById('userUsername');
            const userEmailEl = document.getElementById('userEmail');
            const userStatusEl = document.getElementById('userStatus');
            const userCreatedEl = document.getElementById('userCreated');
            
            if (userFullNameEl) userFullNameEl.textContent = user.full_name || 'N/A';
            if (userUsernameEl) userUsernameEl.textContent = user.username;
            if (userEmailEl) userEmailEl.textContent = user.email;
            if (userStatusEl) userStatusEl.textContent = user.is_active ? 'Active' : 'Inactive';
            
            if (userCreatedEl) {
                const createdDate = new Date(user.created_at);
                userCreatedEl.textContent = createdDate.toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric'
                });
            }
        } else if (response.status === 401) {
            // Token expired or invalid - redirect to login
            localStorage.removeItem('access_token');
            window.location.href = 'index.html';
        } else {
            // Other errors - redirect to login
            localStorage.removeItem('access_token');
            window.location.href = 'index.html';
        }
    } catch (error) {
        // Network error or server not running - redirect to login
        console.error('Error:', error);
        localStorage.removeItem('access_token');
        window.location.href = 'index.html';
    }
}

// Logout functionality
document.getElementById('logoutBtn').addEventListener('click', async () => {
    const messageDiv = document.getElementById('dashboardMessage');
    
    try {
        const response = await fetch(`${API_BASE_URL}/api/auth/logout`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });
        
        if (response.ok) {
            messageDiv.className = 'message success';
            messageDiv.textContent = 'Logged out successfully! Redirecting...';
            
            // Clear token and redirect
            localStorage.removeItem('access_token');
            
            setTimeout(() => {
                window.location.href = 'index.html';
            }, 1000);
        } else {
            // Even if logout fails on server, clear local token
            localStorage.removeItem('access_token');
            window.location.href = 'index.html';
        }
    } catch (error) {
        // On network error, still clear token and redirect
        localStorage.removeItem('access_token');
        window.location.href = 'index.html';
    }
});

// Load user details when page loads
loadUserDetails();
