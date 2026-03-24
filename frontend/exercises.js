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

// Add CSS for exercise cards
const style = document.createElement('style');
style.textContent = `
    .exercise-categories {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
        gap: 25px;
    }
    .exercise-card {
        background: #f8f9fa;
        padding: 25px;
        border-radius: 10px;
        text-align: center;
        transition: transform 0.3s;
    }
    .exercise-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
    }
    .exercise-card h4 {
        color: #667eea;
        margin-bottom: 15px;
        font-size: 20px;
    }
    .exercise-card p {
        color: #666;
        margin-bottom: 10px;
    }
    .exercise-card ul {
        color: #555;
        line-height: 1.8;
    }
`;
document.head.appendChild(style);
