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

// Add CSS for metric cards
const style = document.createElement('style');
style.textContent = `
    .metric-card {
        background: #f8f9fa;
        padding: 25px;
        border-radius: 10px;
        text-align: center;
    }
    .metric-card h4 {
        color: #666;
        margin-bottom: 15px;
        font-size: 16px;
    }
    .metric-value {
        font-size: 42px;
        color: #667eea;
        font-weight: bold;
        margin: 10px 0;
    }
    .metric-trend {
        color: #4caf50;
        font-size: 14px;
        font-weight: 600;
    }
`;
document.head.appendChild(style);
