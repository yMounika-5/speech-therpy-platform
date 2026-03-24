const API_BASE_URL = 'http://127.0.0.1:8000';

// Check if user is logged in
const token = localStorage.getItem('access_token');
if (!token) {
    window.location.href = 'index.html';
}

// Logout functionality
document.getElementById('logoutBtn').addEventListener('click', async () => {
    try {
        await fetch(`${API_BASE_URL}/api/auth/logout`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });
    } catch (error) {
        console.error('Logout error:', error);
    }
    localStorage.removeItem('access_token');
    window.location.href = 'index.html';
});

// Fetch user details
async function loadUserProfile() {
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
            document.getElementById('userName').textContent = user.username;
            document.getElementById('userFullName').textContent = user.full_name || 'Not provided';
            document.getElementById('userUsername').textContent = user.username;
            document.getElementById('userEmail').textContent = user.email;
            document.getElementById('userStatus').textContent = user.is_active ? 'Active' : 'Inactive';
            
            if (user.created_at) {
                const date = new Date(user.created_at);
                document.getElementById('userCreated').textContent = date.toLocaleDateString('en-US', {
                    year: 'numeric',
                    month: 'long',
                    day: 'numeric'
                });
            }
        } else {
            document.getElementById('dashboardMessage').textContent = 'Failed to load user data';
            document.getElementById('dashboardMessage').className = 'message error';
        }
    } catch (error) {
        console.error('Error:', error);
        document.getElementById('dashboardMessage').textContent = 'Network error. Please try again.';
        document.getElementById('dashboardMessage').className = 'message error';
    }
}

loadUserProfile();
