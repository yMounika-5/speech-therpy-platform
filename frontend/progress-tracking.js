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

// Load progress data
async function loadProgressData() {
    console.log('Loading progress data...');
    try {
        const response = await fetch(`${API_BASE_URL}/api/speech/progress`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });
        
        console.log('Progress response status:', response.status);
        
        if (response.ok) {
            const data = await response.json();
            console.log('Progress data received:', data);
            updateProgressUI(data);
        } else {
            const error = await response.json();
            console.error('Failed to load progress data:', error);
        }
    } catch (error) {
        console.error('Error loading progress:', error);
    }
}

function updateProgressUI(data) {
    // Update statistics
    document.getElementById('totalSessions').textContent = data.total_sessions;
    document.getElementById('practiceHours').textContent = data.practice_hours;
    document.getElementById('averageScore').textContent = data.average_score > 0 ? `${data.average_score}%` : '-';
    document.getElementById('streakDays').textContent = data.streak_days;
    
    // Update recent activity
    const activityList = document.getElementById('activityList');
    if (data.recent_activity.length > 0) {
        activityList.innerHTML = data.recent_activity.map(activity => `
            <div class="activity-item">
                <span>${activity.activity}</span>
                <span style="color: #666;">${activity.time}</span>
            </div>
        `).join('');
    } else {
        activityList.innerHTML = `
            <div style="text-align: center; padding: 30px; color: #999;">
                <p style="font-size: 48px;">📝</p>
                <p>No activity yet. Start practicing to see your progress!</p>
            </div>
        `;
    }
    
    // Update achievements
    const achievementsList = document.getElementById('achievementsList');
    if (data.achievements.length > 0) {
        achievementsList.innerHTML = data.achievements.map(achievement => `
            <div style="text-align: center; padding: 15px; background: rgba(255,255,255,0.2); border-radius: 8px;">
                <div style="font-size: 40px;">${achievement.icon}</div>
                <div>${achievement.name}</div>
            </div>
        `).join('');
    } else {
        achievementsList.innerHTML = `
            <div style="text-align: center; padding: 30px; color: rgba(255,255,255,0.7);">
                <p style="font-size: 48px;">🏆</p>
                <p>Complete your first session to unlock achievements!</p>
            </div>
        `;
    }
}

// Add CSS for activity items
const style = document.createElement('style');
style.textContent = `
    .stat-card {
        background: #f8f9fa;
        padding: 25px;
        border-radius: 8px;
        text-align: center;
    }
    .stat-card h4 {
        color: #666;
        margin-bottom: 10px;
        font-size: 16px;
    }
    .activity-item {
        display: flex;
        justify-content: space-between;
        padding: 15px 0;
        border-bottom: 1px solid #e0e0e0;
    }
    .activity-item:last-child {
        border-bottom: none;
    }
`;
document.head.appendChild(style);

// Load data on page load
loadProgressData();
