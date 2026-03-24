import requests
import json
from datetime import datetime

API_BASE_URL = "http://127.0.0.1:8000"

def print_section(title):
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_registration():
    print_section("TEST 1: User Registration")
    
    # Generate unique username with timestamp
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    user_data = {
        "email": f"testuser{timestamp}@example.com",
        "username": f"testuser{timestamp}",
        "password": "Test123456",
        "full_name": "Test User"
    }
    
    print(f"Registering user: {user_data['username']}")
    
    response = requests.post(
        f"{API_BASE_URL}/api/auth/register",
        json=user_data
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 201:
        print("✓ Registration successful!")
        return user_data
    else:
        print("✗ Registration failed!")
        return None

def test_login(username, password):
    print_section("TEST 2: User Login")
    
    print(f"Logging in as: {username}")
    
    response = requests.post(
        f"{API_BASE_URL}/api/auth/login",
        data={
            "username": username,
            "password": password
        }
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        token = response.json()["access_token"]
        print("✓ Login successful!")
        print(f"Token (first 50 chars): {token[:50]}...")
        return token
    else:
        print("✗ Login failed!")
        return None

def test_get_user_details(token):
    print_section("TEST 3: Get Current User Details")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(
        f"{API_BASE_URL}/api/auth/me",
        headers=headers
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print("✓ Successfully retrieved user details!")
        return True
    else:
        print("✗ Failed to retrieve user details!")
        return False

def test_logout(token):
    print_section("TEST 4: User Logout")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.post(
        f"{API_BASE_URL}/api/auth/logout",
        headers=headers
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 200:
        print("✓ Logout successful!")
        return True
    else:
        print("✗ Logout failed!")
        return False

def test_access_after_logout(token):
    print_section("TEST 5: Access After Logout (Should Fail)")
    
    headers = {
        "Authorization": f"Bearer {token}"
    }
    
    response = requests.get(
        f"{API_BASE_URL}/api/auth/me",
        headers=headers
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 401:
        print("✓ Token correctly invalidated!")
        return True
    else:
        print("✗ Token should have been invalidated!")
        return False

def test_duplicate_registration(user_data):
    print_section("TEST 6: Duplicate Registration (Should Fail)")
    
    print(f"Attempting to register duplicate user: {user_data['username']}")
    
    response = requests.post(
        f"{API_BASE_URL}/api/auth/register",
        json=user_data
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 400:
        print("✓ Duplicate registration correctly rejected!")
        return True
    else:
        print("✗ Duplicate registration should have been rejected!")
        return False

def test_invalid_login():
    print_section("TEST 7: Invalid Login (Should Fail)")
    
    response = requests.post(
        f"{API_BASE_URL}/api/auth/login",
        data={
            "username": "nonexistentuser",
            "password": "wrongpassword"
        }
    )
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    
    if response.status_code == 401:
        print("✓ Invalid login correctly rejected!")
        return True
    else:
        print("✗ Invalid login should have been rejected!")
        return False

def main():
    print("\n" + "🚀 "*20)
    print("  SPEECH THERAPY API - COMPLETE FLOW TEST")
    print("🚀 "*20)
    
    try:
        # Test 1: Registration
        user_data = test_registration()
        if not user_data:
            print("\n❌ Test suite failed at registration!")
            return
        
        # Test 2: Login
        token = test_login(user_data["username"], user_data["password"])
        if not token:
            print("\n❌ Test suite failed at login!")
            return
        
        # Test 3: Get user details
        if not test_get_user_details(token):
            print("\n❌ Test suite failed at getting user details!")
            return
        
        # Test 4: Logout
        if not test_logout(token):
            print("\n❌ Test suite failed at logout!")
            return
        
        # Test 5: Access after logout
        if not test_access_after_logout(token):
            print("\n❌ Test suite failed at post-logout access check!")
            return
        
        # Test 6: Duplicate registration
        if not test_duplicate_registration(user_data):
            print("\n❌ Test suite failed at duplicate registration check!")
            return
        
        # Test 7: Invalid login
        if not test_invalid_login():
            print("\n❌ Test suite failed at invalid login check!")
            return
        
        # All tests passed
        print("\n" + "✅ "*20)
        print("  ALL TESTS PASSED SUCCESSFULLY!")
        print("✅ "*20)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to the API server!")
        print("Make sure the server is running at http://127.0.0.1:8000")
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")

if __name__ == "__main__":
    main()
