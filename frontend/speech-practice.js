const API_BASE_URL = 'http://127.0.0.1:8000';
const token = localStorage.getItem('access_token');
if (!token) { window.location.href = 'index.html'; }

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

let mediaRecorder, audioChunks = [], recognition, recognizedText = '';
let excelSentences = [];

const recordBtn = document.getElementById('recordBtn');
const stopBtn = document.getElementById('stopBtn');
const recordingStatus = document.getElementById('recordingStatus');
const audioPlayback = document.getElementById('audioPlayback');
const feedbackCard = document.getElementById('feedbackCard');
const feedbackContent = document.getElementById('feedbackContent');

if ('webkitSpeechRecognition' in window || 'SpeechRecognition' in window) {
    const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
    recognition = new SR();
    recognition.continuous = true;
    recognition.interimResults = false;
    recognition.lang = 'en-US';
    recognition.onresult = (event) => {
        recognizedText = '';
        for (let i = 0; i < event.results.length; i++) recognizedText += event.results[i][0].transcript + ' ';
        recognizedText = recognizedText.trim().toLowerCase();
    };
    recognition.onerror = (e) => console.error('SR error:', e.error);
}

async function loadSentences() {
    try {
        const res = await fetch(`${API_BASE_URL}/api/speech/practice-sentences`, {
            headers: { 'Authorization': `Bearer ${token}` }
        });
        if (res.ok) { const d = await res.json(); excelSentences = d.sentences || []; }
    } catch (e) { console.error(e); }
    loadNewSentence();
}

function loadNewSentence() {
    if (!excelSentences.length) { document.getElementById('practiceSentence').textContent = 'Loading...'; return; }
    const s = excelSentences[Math.floor(Math.random() * excelSentences.length)];
    document.getElementById('practiceSentence').textContent = '"' + s + '"';
}

function getCurrentSentence() {
    return document.getElementById('practiceSentence').textContent.replace(/"/g, '').trim();
}

recordBtn.addEventListener('click', async () => {
    const sentence = getCurrentSentence();
    if (!sentence || sentence === 'Loading...') { alert('Sentence not loaded yet. Please wait.'); return; }
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        audioChunks = []; recognizedText = '';
        if (recognition) recognition.start();
        mediaRecorder.ondataavailable = (e) => audioChunks.push(e.data);
        mediaRecorder.onstop = async () => {
            if (recognition) recognition.stop();
            const audioBlob = new Blob(audioChunks, { type: 'audio/wav' });
            audioPlayback.src = URL.createObjectURL(audioBlob);
            audioPlayback.style.display = 'block';
            feedbackCard.style.display = 'block';
            feedbackContent.innerHTML = `<div style="text-align:center;padding:30px;">
                <p style="font-size:48px;"></p>
                <h3 style="color:#2e7d32;">Recording Complete!</h3>
                <p style="color:#666;margin-bottom:25px;">Listen above, then click below for feedback.</p>
                <button id="getFeedbackBtn" class="btn btn-primary" style="font-size:18px;padding:15px 40px;"> Get Feedback</button>
            </div>`;
            document.getElementById('getFeedbackBtn').addEventListener('click', () => {
                setTimeout(() => analyzeAudio(audioBlob, recognizedText), 500);
            });
        };
        mediaRecorder.start();
        recordBtn.disabled = true; stopBtn.disabled = false;
        recordingStatus.textContent = ' Recording... Speak clearly!';
        recordingStatus.style.color = '#f44336';
        feedbackCard.style.display = 'none';
    } catch (err) {
        recordingStatus.textContent = ' Could not access microphone.';
        recordingStatus.style.color = '#f44336';
    }
});

stopBtn.addEventListener('click', () => {
    if (mediaRecorder && mediaRecorder.state === 'recording') {
        mediaRecorder.stop();
        mediaRecorder.stream.getTracks().forEach(t => t.stop());
        recordBtn.disabled = false; stopBtn.disabled = true;
        recordingStatus.textContent = ' Recording completed!';
        recordingStatus.style.color = '#4caf50';
    }
});

async function analyzeAudio(audioBlob, spokenText) {
    feedbackContent.innerHTML = `<div style="text-align:center;padding:30px;"><p style="font-size:48px;"></p><p>Analyzing...</p></div>`;
    const sentence = getCurrentSentence();
    if (!spokenText || spokenText.length < 2) {
        feedbackContent.innerHTML = `<div style="text-align:center;padding:30px;color:#f44336;">
            <p style="font-size:48px;"></p><p><strong>No Speech Detected</strong></p>
            <p>Speak louder and clearly. Use Chrome or Edge.</p>
            <button onclick="location.reload()" class="btn btn-primary" style="margin-top:20px;"> Try Again</button>
        </div>`;
        return;
    }
    const analysis = analyzePronunciation(sentence, spokenText);
    showFeedback(analysis);
    try {
        const fd = new FormData();
        fd.append('audio', audioBlob, 'recording.wav');
        fd.append('sentence', sentence);
        fd.append('clarity_score', analysis.clarity_score);
        fd.append('accuracy_score', analysis.accuracy_score);
        fd.append('pronunciation', analysis.pronunciation);
        await fetch(`${API_BASE_URL}/api/speech/save-session`, {
            method: 'POST', headers: { 'Authorization': `Bearer ${token}` }, body: fd
        });
    } catch (e) { console.error('Save error:', e); }
}

function analyzePronunciation(expectedSentence, spokenText) {
    const expWords = expectedSentence.toLowerCase().trim().split(/\s+/);
    const recWords = spokenText.toLowerCase().trim().split(/\s+/);
    let correct = 0, difficult = [];
    expWords.forEach((w, i) => {
        if (recWords[i] === w) { correct += 1; }
        else if (recWords.includes(w)) { correct += 0.7; }
        else {
            const sim = recWords.find(r => r.length > 2 && (r.startsWith(w.substring(0,3)) || w.startsWith(r.substring(0,3))));
            correct += sim ? 0.3 : 0;
            difficult.push({ word: w, recognized: sim || null });
        }
    });
    const accuracy_score = Math.min(100, Math.round((correct / expWords.length) * 100));
    const clarity_score = Math.min(95, accuracy_score + 3);
    let pronunciation, pronunciation_color;
    if (accuracy_score >= 85) { pronunciation = 'Excellent'; pronunciation_color = '#2e7d32'; }
    else if (accuracy_score >= 70) { pronunciation = 'Good'; pronunciation_color = '#558b2f'; }
    else if (accuracy_score >= 50) { pronunciation = 'Fair'; pronunciation_color = '#f57c00'; }
    else { pronunciation = 'Needs Improvement'; pronunciation_color = '#d32f2f'; }
    const suggestions = [];
    if (difficult.length) suggestions.push('Practice: ' + difficult.slice(0,3).map(d => '"'+d.word+'"').join(', '));
    if (accuracy_score < 70) suggestions.push('Read the sentence slowly before recording');
    suggestions.push('Try again to beat your score!');
    return { accuracy_score, clarity_score, pronunciation, pronunciation_color, suggestions, difficult_words: difficult, recognized_text: spokenText, expected_text: expectedSentence };
}

function showFeedback(a) {
    let overall = '';
    if (a.accuracy_score >= 85) overall = `Excellent! You scored ${a.accuracy_score}% — your speech was clear and easy to understand.`;
    else if (a.accuracy_score >= 70) overall = `Good effort! ${a.accuracy_score}% correct. Focus on highlighted words and try again.`;
    else if (a.accuracy_score >= 50) overall = `You scored ${a.accuracy_score}%. Try speaking more slowly and clearly.`;
    else overall = `Score: ${a.accuracy_score}%. Try reducing background noise and speaking louder.`;

    const expWords = a.expected_text.toLowerCase().replace(/"/g,'').trim().split(/\s+/);
    const recWords = a.recognized_text.toLowerCase().trim().split(/\s+/);
    const badges = expWords.map((w, i) => {
        const sp = recWords[i] || '';
        const ok = sp === w, found = !ok && recWords.includes(w);
        let bg, col, icon;
        if (ok) { bg='#e8f5e9'; col='#2e7d32'; icon=''; }
        else if (found) { bg='#fff8e1'; col='#f57c00'; icon='~'; }
        else { bg='#ffebee'; col='#c62828'; icon=''; }
        return `<span style="display:inline-block;padding:5px 12px;background:${bg};color:${col};border-radius:20px;font-weight:600;font-size:14px;border:1px solid ${col}40;margin:3px;">${icon} ${w}</span>`;
    }).join('');

    const wrong = expWords.map((w, i) => {
        const sp = recWords[i] || '';
        if (sp === w) return null;
        const found = recWords.includes(w);
        if (found) return `<li><strong>"${w}"</strong> — said out of order.</li>`;
        const syl = w.match(/[^aeiouy]*[aeiouy]+(?:[^aeiouy]*$|[^aeiouy](?=[^aeiouy]))?/gi) || [w];
        return `<li><strong>"${w}"</strong> — ${sp ? `you said <em>"${sp}"</em>` : 'not detected'}. Try: <strong>${syl.join('-')}</strong></li>`;
    }).filter(Boolean);

    feedbackContent.innerHTML = `
        <div style="margin-bottom:20px;padding:18px;background:linear-gradient(135deg,#667eea22,#764ba222);border-radius:10px;border-left:4px solid #667eea;">
            <strong> Overall Feedback:</strong>
            <p style="margin:10px 0 0;line-height:1.8;color:#333;font-size:15px;">${overall}</p>
        </div>
        <div style="display:grid;grid-template-columns:1fr 1fr;gap:15px;margin-bottom:20px;">
            <div style="background:white;padding:15px;border-radius:8px;text-align:center;border:2px solid #e0e0e0;">
                <p style="color:#666;font-size:13px;margin-bottom:5px;">Accuracy Score</p>
                <p style="color:${a.pronunciation_color};font-size:36px;font-weight:bold;margin:0;">${a.accuracy_score}%</p>
            </div>
            <div style="background:white;padding:15px;border-radius:8px;text-align:center;border:2px solid #e0e0e0;">
                <p style="color:#666;font-size:13px;margin-bottom:5px;">Pronunciation</p>
                <p style="color:${a.pronunciation_color};font-size:20px;font-weight:bold;margin:0;">${a.pronunciation}</p>
            </div>
        </div>
        <div style="margin-bottom:20px;padding:15px;background:#f5f5f5;border-radius:8px;">
            <strong> Word-by-Word:</strong>
            <div style="margin-top:12px;line-height:2.5;">${badges}</div>
            <div style="margin-top:10px;font-size:12px;color:#666;"> Correct &nbsp; ~ Out of order &nbsp;  Missed</div>
        </div>
        ${wrong.length ? `<div style="margin-bottom:20px;padding:15px;background:#fff3e0;border-radius:8px;border-left:4px solid #ff9800;">
            <strong> Words Needing Practice:</strong>
            <ul style="margin:10px 0 0 20px;line-height:2.2;">${wrong.join('')}</ul>
        </div>` : ''}
        <div style="padding:15px;background:#e3f2fd;border-radius:8px;border-left:4px solid #2196f3;">
            <strong> Tips:</strong>
            <ul style="margin:10px 0 0 20px;line-height:1.9;">${a.suggestions.map(s=>`<li>${s}</li>`).join('')}</ul>
        </div>`;
}

loadSentences();
