"""
Quick test to verify the speech analysis endpoint is working
"""
import requests
import io

API_BASE_URL = 'http://127.0.0.1:8000'

# First, login to get a token
print("🔐 Logging in...")
login_response = requests.post(
    f"{API_BASE_URL}/api/auth/login",
    data={
        "username": "Mounika",
        "password": "your_password_here"  # Replace with actual password
    }
)

if login_response.status_code == 200:
    token = login_response.json()["access_token"]
    print("✅ Login successful!")
    
    # Create a dummy audio file
    print("\n🎤 Testing speech analysis...")
    audio_data = b"dummy audio data for testing" * 1000  # Simulate audio
    
    files = {
        'audio': ('test.wav', io.BytesIO(audio_data), 'audio/wav')
    }
    data = {
        'sentence': 'The quick brown fox jumps over the lazy dog'
    }
    headers = {
        'Authorization': f'Bearer {token}'
    }
    
    analyze_response = requests.post(
        f"{API_BASE_URL}/api/speech/analyze",
        files=files,
        data=data,
        headers=headers
    )
    
    if analyze_response.status_code == 200:
        result = analyze_response.json()
        print("✅ Speech analysis successful!")
        print(f"   Clarity Score: {result['analysis']['clarity_score']}%")
        print(f"   Pronunciation: {result['analysis']['pronunciation']}")
        print(f"   Session ID: {result['analysis']['session_id']}")
        
        # Check progress
        print("\n📊 Checking progress...")
        progress_response = requests.get(
            f"{API_BASE_URL}/api/speech/progress",
            headers=headers
        )
        
        if progress_response.status_code == 200:
            progress = progress_response.json()
            print("✅ Progress data retrieved!")
            print(f"   Total Sessions: {progress['total_sessions']}")
            print(f"   Practice Hours: {progress['practice_hours']}")
            print(f"   Average Score: {progress['average_score']}%")
            print(f"   Streak Days: {progress['streak_days']}")
            print(f"\n🎉 Everything is working correctly!")
        else:
            print(f"❌ Progress check failed: {progress_response.text}")
    else:
        print(f"❌ Speech analysis failed: {analyze_response.text}")
else:
    print(f"❌ Login failed: {login_response.text}")
    print("\n💡 Please update the password in test_fix.py and run again")
