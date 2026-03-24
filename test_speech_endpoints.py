"""
Test script to verify speech endpoints work
"""
import requests
import io

API_BASE_URL = "http://127.0.0.1:8000"

print("=" * 60)
print("TESTING SPEECH ENDPOINTS")
print("=" * 60)

# First, login to get a token
print("\n1. Logging in...")
print("   Please enter your password for user 'Mounika'")
password = input("   Password: ")

login_response = requests.post(
    f"{API_BASE_URL}/api/auth/login",
    data={
        "username": "Mounika",
        "password": password
    }
)

if login_response.status_code == 200:
    token = login_response.json()["access_token"]
    print("✅ Login successful!")
    print(f"Token: {token[:50]}...")
else:
    print(f"❌ Login failed: {login_response.json()}")
    exit()

# Test progress endpoint
print("\n2. Testing progress endpoint...")
headers = {"Authorization": f"Bearer {token}"}
progress_response = requests.get(
    f"{API_BASE_URL}/api/speech/progress",
    headers=headers
)

if progress_response.status_code == 200:
    data = progress_response.json()
    print("✅ Progress endpoint works!")
    print(f"   Total Sessions: {data['total_sessions']}")
    print(f"   Practice Hours: {data['practice_hours']}")
    print(f"   Average Score: {data['average_score']}")
    print(f"   Streak Days: {data['streak_days']}")
else:
    print(f"❌ Progress endpoint failed: {progress_response.json()}")

# Test analyze endpoint with dummy audio
print("\n3. Testing analyze endpoint...")
# Create a small dummy audio file
dummy_audio = b'\x00' * 50000  # 50KB of dummy data
files = {'audio': ('test.wav', io.BytesIO(dummy_audio), 'audio/wav')}
data = {'sentence': 'Test sentence'}

analyze_response = requests.post(
    f"{API_BASE_URL}/api/speech/analyze",
    headers=headers,
    files=files,
    data=data
)

if analyze_response.status_code == 200:
    result = analyze_response.json()
    print("✅ Analyze endpoint works!")
    print(f"   Clarity Score: {result['analysis']['clarity_score']}")
    print(f"   Pronunciation: {result['analysis']['pronunciation']}")
    print(f"   Session saved with ID: {result['analysis']['session_id']}")
else:
    print(f"❌ Analyze endpoint failed: {analyze_response.json()}")

# Check progress again
print("\n4. Checking progress after practice...")
progress_response2 = requests.get(
    f"{API_BASE_URL}/api/speech/progress",
    headers=headers
)

if progress_response2.status_code == 200:
    data = progress_response2.json()
    print("✅ Progress updated!")
    print(f"   Total Sessions: {data['total_sessions']}")
    print(f"   Achievements: {len(data['achievements'])}")
    if data['achievements']:
        for achievement in data['achievements']:
            print(f"      {achievement['icon']} {achievement['name']}")
else:
    print(f"❌ Progress check failed")

print("\n" + "=" * 60)
print("✅ TEST COMPLETE!")
print("=" * 60)
