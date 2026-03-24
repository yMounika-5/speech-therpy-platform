import requests
import json

BASE_URL = "http://127.0.0.1:8000"

print("=" * 60)
print("Testing Speech Therapy API Endpoints")
print("=" * 60)

# Test 1: Root endpoint
print("\n1. Testing Root Endpoint (GET /)")
try:
    response = requests.get(f"{BASE_URL}/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200
    print("✓ Root endpoint working!")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 2: Health check
print("\n2. Testing Health Check (GET /health)")
try:
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 200
    print("✓ Health check working!")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 3: Register a new user
print("\n3. Testing User Registration (POST /api/auth/register)")
user_data = {
    "email": "testuser@example.com",
    "username": "testuser",
    "password": "Test123456",
    "full_name": "Test User"
}
try:
    response = requests.post(f"{BASE_URL}/api/auth/register", json=user_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 201
    print("✓ User registration working!")
except Exception as e:
    print(f"✗ Error: {e}")
    if response.status_code == 400:
        print("Note: User might already exist, continuing tests...")

# Test 4: Login
print("\n4. Testing User Login (POST /api/auth/login)")
login_data = {
    "username": "testuser",
    "password": "Test123456"
}
try:
    response = requests.post(
        f"{BASE_URL}/api/auth/login",
        data=login_data
    )
    print(f"Status Code: {response.status_code}")
    response_data = response.json()
    print(f"Response: {json.dumps(response_data, indent=2)}")
    assert response.status_code == 200
    assert "access_token" in response_data
    access_token = response_data["access_token"]
    print("✓ User login working!")
    print(f"Access Token: {access_token[:50]}...")
except Exception as e:
    print(f"✗ Error: {e}")
    access_token = None

# Test 5: Get current user details
if access_token:
    print("\n5. Testing Get Current User (GET /api/auth/me)")
    headers = {"Authorization": f"Bearer {access_token}"}
    try:
        response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        assert response.status_code == 200
        print("✓ Get current user working!")
    except Exception as e:
        print(f"✗ Error: {e}")

    # Test 6: Logout
    print("\n6. Testing User Logout (POST /api/auth/logout)")
    try:
        response = requests.post(f"{BASE_URL}/api/auth/logout", headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        assert response.status_code == 200
        print("✓ User logout working!")
    except Exception as e:
        print(f"✗ Error: {e}")

    # Test 7: Try to access protected endpoint with blacklisted token
    print("\n7. Testing Access with Blacklisted Token (GET /api/auth/me)")
    try:
        response = requests.get(f"{BASE_URL}/api/auth/me", headers=headers)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        assert response.status_code == 401
        print("✓ Token blacklisting working!")
    except Exception as e:
        print(f"✗ Error: {e}")

# Test 8: Test invalid login
print("\n8. Testing Invalid Login (POST /api/auth/login)")
invalid_login = {
    "username": "wronguser",
    "password": "wrongpassword"
}
try:
    response = requests.post(f"{BASE_URL}/api/auth/login", data=invalid_login)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 401
    print("✓ Invalid login handling working!")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 9: Test duplicate registration
print("\n9. Testing Duplicate Registration (POST /api/auth/register)")
try:
    response = requests.post(f"{BASE_URL}/api/auth/register", json=user_data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    assert response.status_code == 400
    print("✓ Duplicate registration prevention working!")
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "=" * 60)
print("All endpoint tests completed!")
print("=" * 60)
