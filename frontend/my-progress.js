const API_BASE_URL = 'http://127.0.0.1:8000';

const token = localStorage.getItem('access_token');
if (!token) {
    window.location.href = 'index.html';
}

document.getElementById('logoutBtn').addEventListener('click', async () => {
    try {
        await fetch(`${API_BASE_URL}/api/auth/logout`, {
            method: 'POST',
            headers: { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' }
        });
    } catch (e) {}
    localStorage.removeItem('access_token');
    window.location.href = 'index.html';
});

function showTab(tabName, el) {
    document.querySelectorAll('.tab-content').forEach(t => t.classList.remove('active'));
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    document.getElementById(tabName).classList.add('active');
    el.classList.add('active');
    if (tabName === 'history') loadHistory();
    else if (tabName === 'difficulty') loadDifficulty();
    else if (tabName === 'streak') loadStreak();
    else if (tabName === 'insights') loadInsights();
}

async function loadStatistics() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/progress/statistics?days=30&t=${Date.now()}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (response.status === 401) { localStorage.removeItem('access_token'); window.location.href = 'index.html'; return; }
        if (response.ok) {
            const data = await response.json();
            document.getElementById('totalSessions').textContent = data.total_sessions;
            document.getElementById('practiceTime').textContent = data.total_practice_time + ' min';
            document.getElementById('avgScore').textContent = data.average_score + '%';
            document.getElementById('bestScore').textContent = data.best_score + '%';
            document.getElementById('improvement').textContent = data.improvement_rate + '%';
        }
    } catch (e) { console.error('Error loading statistics:', e); }
}

async function loadHistory() {
    const container = document.getElementById('historyContainer');
    try {
        const response = await fetch(`${API_BASE_URL}/api/progress/history?limit=50&t=${Date.now()}`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (response.status === 401) { localStorage.removeItem('access_token'); window.location.href = 'index.html'; return; }
        const data = await response.json();
        if (data.sessions.length === 0) {
            container.innerHTML = '<p style="text-align:center;padding:40px;color:#999;">No practice sessions yet. Start practicing!</p>';
            return;
        }
        let html = `<table class="history-table"><thead><tr>
            <th>Date & Time</th><th>Sentence</th><th>Score</th><th>Pronunciation</th><th>Feedback</th>
        </tr></thead><tbody>`;
        data.sessions.forEach(session => {
            const scoreColor = session.clarity_score >= 85 ? '#2e7d32' : session.clarity_score >= 70 ? '#f57c00' : '#d32f2f';
            const dateObj = new Date(session.date);
            const dateTimeStr = dateObj.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' })
                + ' ' + dateObj.toLocaleTimeString('en-US', { hour: '2-digit', minute: '2-digit' });
            let feedback = session.pronunciation === 'Excellent' ? '🌟 Outstanding! Keep it up!'
                : session.pronunciation === 'Good' ? '👍 Well done! Practice more.'
                : session.pronunciation === 'Fair' ? '💪 Good effort! Focus on clarity.'
                : '📚 Keep practicing!';
            html += `<tr>
                <td>${dateTimeStr}</td>
                <td>${session.sentence || 'Practice sentence'}</td>
                <td style="color:${scoreColor};font-weight:bold;">${session.clarity_score}%</td>
                <td>${session.pronunciation}</td>
                <td style="font-size:14px;">${feedback}</td>
            </tr>`;
        });
        html += '</tbody></table>';
        container.innerHTML = html;
    } catch (e) {
        container.innerHTML = '<p style="text-align:center;padding:40px;color:#f44336;">Unable to load history. Please refresh.</p>';
    }
}

async function loadDifficulty() {
    const container = document.getElementById('difficultyContainer');
    try {
        const res = await fetch(`${API_BASE_URL}/api/progress/difficulty`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!res.ok) return;
        const data = await res.json();

        if (data.stats.total_unique === 0 && data.stats.not_attempted_count === 0) {
            container.innerHTML = `<div style="text-align:center;padding:40px;color:#999;">
                <div style="font-size:60px;margin-bottom:15px;">🎤</div>
                <p style="font-size:18px;font-weight:600;color:#555;">No sessions yet!</p>
                <p>Practice some sentences to see your difficulty breakdown.</p>
            </div>`;
            return;
        }

        const { easy, medium, hard, not_attempted, stats } = data;
        const total = stats.total_unique;
        const ePct = total > 0 ? Math.round((stats.easy_count / total) * 100) : 0;
        const mPct = total > 0 ? Math.round((stats.medium_count / total) * 100) : 0;
        const hPct = total > 0 ? (100 - ePct - mPct) : 0;

        let html = `
        <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:16px;margin-bottom:24px;">
            <div style="background:white;border-radius:12px;padding:18px;text-align:center;border:2px solid #43a04740;box-shadow:0 4px 12px #43a04720;">
                <div style="font-size:32px;">🟢</div>
                <div style="font-size:28px;font-weight:800;color:#43a047;margin:6px 0;">${stats.easy_count}</div>
                <div style="font-size:13px;color:#555;font-weight:600;">Easy sentences</div>
                <div style="font-size:12px;color:#aaa;">avg ${stats.easy_avg}%</div>
            </div>
            <div style="background:white;border-radius:12px;padding:18px;text-align:center;border:2px solid #f57c0040;box-shadow:0 4px 12px #f57c0020;">
                <div style="font-size:32px;">🟡</div>
                <div style="font-size:28px;font-weight:800;color:#f57c00;margin:6px 0;">${stats.medium_count}</div>
                <div style="font-size:13px;color:#555;font-weight:600;">Medium sentences</div>
                <div style="font-size:12px;color:#aaa;">avg ${stats.medium_avg}%</div>
            </div>
            <div style="background:white;border-radius:12px;padding:18px;text-align:center;border:2px solid #e5393540;box-shadow:0 4px 12px #e5393520;">
                <div style="font-size:32px;">🔴</div>
                <div style="font-size:28px;font-weight:800;color:#e53935;margin:6px 0;">${stats.hard_count}</div>
                <div style="font-size:13px;color:#555;font-weight:600;">Hard sentences</div>
                <div style="font-size:12px;color:#aaa;">avg ${stats.hard_avg}%</div>
            </div>
            <div style="background:white;border-radius:12px;padding:18px;text-align:center;border:2px solid #90909040;box-shadow:0 4px 12px #90909020;">
                <div style="font-size:32px;">⬜</div>
                <div style="font-size:28px;font-weight:800;color:#888;margin:6px 0;">${stats.not_attempted_count}</div>
                <div style="font-size:13px;color:#555;font-weight:600;">Not attempted</div>
                <div style="font-size:12px;color:#aaa;">of ${stats.total_sentences} total</div>
            </div>
        </div>

        <div style="background:white;border-radius:12px;padding:18px;margin-bottom:24px;box-shadow:0 2px 8px rgba(0,0,0,0.06);">
            <div style="font-size:14px;font-weight:600;color:#555;margin-bottom:10px;">Distribution across ${total} unique sentence${total > 1 ? 's' : ''}</div>
            <div style="display:flex;border-radius:8px;overflow:hidden;height:22px;">
                ${ePct > 0 ? `<div style="width:${ePct}%;background:#43a047;display:flex;align-items:center;justify-content:center;color:white;font-size:11px;font-weight:700;">${ePct}%</div>` : ''}
                ${mPct > 0 ? `<div style="width:${mPct}%;background:#f57c00;display:flex;align-items:center;justify-content:center;color:white;font-size:11px;font-weight:700;">${mPct}%</div>` : ''}
                ${hPct > 0 ? `<div style="width:${hPct}%;background:#e53935;display:flex;align-items:center;justify-content:center;color:white;font-size:11px;font-weight:700;">${hPct}%</div>` : ''}
            </div>
            <div style="display:flex;gap:16px;margin-top:8px;font-size:12px;color:#888;">
                <span>🟢 Easy ≥85%</span><span>🟡 Medium 65–84%</span><span>🔴 Hard &lt;65%</span>
            </div>
        </div>`;

        const categories = [
            { label: '🔴 Hard — needs more practice', color: '#e53935', bg: '#fff5f5', list: hard },
            { label: '🟡 Medium — getting there',      color: '#f57c00', bg: '#fffbf0', list: medium },
            { label: '🟢 Easy — well mastered',        color: '#43a047', bg: '#f0fff4', list: easy },
        ];

        categories.forEach(cat => {
            if (cat.list.length === 0) return;
            html += `
            <div style="background:white;border-radius:12px;margin-bottom:20px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.06);">
                <div style="background:${cat.bg};padding:14px 18px;border-left:4px solid ${cat.color};">
                    <span style="font-weight:700;color:${cat.color};font-size:15px;">${cat.label}</span>
                    <span style="float:right;font-size:13px;color:#aaa;">${cat.list.length} sentence${cat.list.length > 1 ? 's' : ''}</span>
                </div>
                <table style="width:100%;border-collapse:collapse;">
                    <thead>
                        <tr style="background:#fafafa;font-size:13px;color:#888;">
                            <th style="padding:10px 16px;text-align:left;font-weight:600;">Sentence</th>
                            <th style="padding:10px 16px;text-align:center;font-weight:600;">Avg Score</th>
                            <th style="padding:10px 16px;text-align:center;font-weight:600;">Best</th>
                            <th style="padding:10px 16px;text-align:center;font-weight:600;">Attempts</th>
                            <th style="padding:10px 16px;text-align:center;font-weight:600;">Last Practiced</th>
                        </tr>
                    </thead>
                    <tbody>`;

            cat.list.forEach((s, i) => {
                html += `
                        <tr style="border-top:1px solid #f0f0f0;background:${i % 2 === 0 ? 'white' : '#fafafa'};">
                            <td style="padding:12px 16px;font-size:14px;color:#333;max-width:320px;">${s.sentence}</td>
                            <td style="padding:12px 16px;text-align:center;">
                                <div style="display:flex;align-items:center;gap:8px;justify-content:center;">
                                    <div style="width:60px;height:8px;background:#eee;border-radius:4px;overflow:hidden;">
                                        <div style="width:${s.avg_score}%;height:100%;background:${cat.color};border-radius:4px;"></div>
                                    </div>
                                    <span style="font-weight:700;color:${cat.color};font-size:14px;">${s.avg_score}%</span>
                                </div>
                            </td>
                            <td style="padding:12px 16px;text-align:center;font-size:14px;color:#43a047;font-weight:600;">${s.best_score}%</td>
                            <td style="padding:12px 16px;text-align:center;font-size:14px;color:#667eea;font-weight:600;">${s.attempts}x</td>
                            <td style="padding:12px 16px;text-align:center;font-size:13px;color:#aaa;">${s.last_date}</td>
                        </tr>`;
            });

            html += `</tbody></table></div>`;
        });

        if (hard.length > 0) {
            html += `<div style="background:#fff3e0;border-radius:12px;padding:16px 20px;border-left:4px solid #f57c00;margin-top:8px;">
                <strong style="color:#e65100;">💡 Tip:</strong>
                <span style="color:#555;font-size:14px;"> Focus on your ${hard.length} hard sentence${hard.length > 1 ? 's' : ''} — practice them slowly, one word at a time.</span>
            </div>`;
        }

        // Not attempted section
        if (not_attempted.length > 0) {
            html += `
            <div style="background:white;border-radius:12px;margin-top:20px;overflow:hidden;box-shadow:0 2px 8px rgba(0,0,0,0.06);">
                <div style="background:#f5f5f5;padding:14px 18px;border-left:4px solid #bbb;cursor:pointer;"
                     onclick="this.nextElementSibling.style.display=this.nextElementSibling.style.display==='none'?'block':'none'">
                    <span style="font-weight:700;color:#888;font-size:15px;">⬜ Not yet practiced</span>
                    <span style="float:right;font-size:13px;color:#aaa;">${not_attempted.length} sentence${not_attempted.length > 1 ? 's' : ''} — click to expand</span>
                </div>
                <div style="display:none;">
                    <table style="width:100%;border-collapse:collapse;">
                        <tbody>`;
            not_attempted.forEach((s, i) => {
                html += `<tr style="border-top:1px solid #f0f0f0;background:${i % 2 === 0 ? 'white' : '#fafafa'};">
                    <td style="padding:12px 16px;font-size:14px;color:#aaa;">${s.sentence}</td>
                    <td style="padding:12px 16px;text-align:center;font-size:13px;color:#ccc;">Not practiced</td>
                </tr>`;
            });
            html += `</tbody></table></div></div>`;
        }

        container.innerHTML = html;
    } catch (e) {
        container.innerHTML = '<p style="text-align:center;padding:40px;color:#f44336;">Unable to load difficulty data. Please refresh.</p>';
        console.error(e);
    }
}

async function loadStreak() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/progress/streak`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) return;
        const data = await response.json();
        document.getElementById('currentStreak').textContent = data.current_streak;
        document.getElementById('longestStreak').textContent = data.longest_streak;
        document.getElementById('totalPracticeDays').textContent = data.total_practice_days;
        const msg = document.getElementById('streakMessage');
        if (data.current_streak === 0) msg.textContent = 'Start practicing today to begin your streak!';
        else if (data.current_streak === 1) msg.textContent = 'Great start! Practice tomorrow to continue!';
        else if (data.current_streak < 7) msg.textContent = 'Amazing! Keep it up to reach a 7-day streak!';
        else if (data.current_streak < 30) msg.textContent = "Incredible! You're on fire! 🔥";
        else msg.textContent = "Legendary streak! You're a practice champion! 🏆";
    } catch (e) { console.error('Error loading streak:', e); }
}

async function loadInsights() {
    const container = document.getElementById('insightsContainer');
    try {
        const response = await fetch(`${API_BASE_URL}/api/progress/insights`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (!response.ok) return;
        const data = await response.json();
        let html = '<h4>💡 Insights</h4>';
        data.insights.forEach(i => { html += `<div class="insight-card">${i}</div>`; });
        html += '<h4 style="margin-top:30px;">📋 Recommendations</h4>';
        data.recommendations.forEach(r => { html += `<div class="insight-card" style="background:#fff3e0;border-left-color:#ff9800;">${r}</div>`; });
        container.innerHTML = html;
    } catch (e) { console.error('Error loading insights:', e); }
}

async function exportCSV() {
    try {
        const response = await fetch(`${API_BASE_URL}/api/progress/export/csv`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.href = url;
            a.download = `speech_sessions_${new Date().toISOString().split('T')[0]}.csv`;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        } else alert('Failed to export data');
    } catch (e) { alert('Error exporting data'); }
}

loadStatistics();
