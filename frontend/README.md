# Speech Therapy Frontend

A simple, responsive frontend for the Speech Therapy application with user authentication.

## Features

- User Registration
- User Login
- User Dashboard with profile information
- Logout functionality
- Responsive design
- Modern UI with gradient backgrounds

## Pages

1. **index.html** - Login page
2. **register.html** - Registration page
3. **dashboard.html** - User dashboard (protected, requires authentication)

## How to Run

### Option 1: Using Python's Built-in Server

```bash
# Navigate to the frontend directory
cd frontend

# Start a simple HTTP server
python -m http.server 8080
```

Then open your browser and go to: `http://localhost:8080`

### Option 2: Using Live Server (VS Code Extension)

1. Install "Live Server" extension in VS Code
2. Right-click on `index.html`
3. Select "Open with Live Server"

### Option 3: Direct File Access

Simply open `index.html` in your web browser. However, note that some browsers may have CORS restrictions when accessing files directly.

## Usage Flow

1. **First Time Users**:
   - Open `index.html` (Login page)
   - Click "Register here" link
   - Fill in registration form
   - After successful registration, you'll be redirected to login

2. **Existing Users**:
   - Open `index.html` (Login page)
   - Enter username and password
   - Click "Login"
   - You'll be redirected to the dashboard

3. **Dashboard**:
   - View your profile information
   - See available speech therapy features
   - Click "Logout" to end your session

## Important Notes

- Make sure the backend server is running at `http://127.0.0.1:8000`
- The frontend uses localStorage to store JWT tokens
- Tokens are automatically included in API requests
- Session expires after 30 minutes (configurable in backend)

## API Configuration

The API base URL is configured in each JavaScript file:
```javascript
const API_BASE_URL = 'http://127.0.0.1:8000';
```

If your backend runs on a different port, update this value in:
- `login.js`
- `register.js`
- `dashboard.js`

## Browser Compatibility

- Chrome (recommended)
- Firefox
- Edge
- Safari

## Security Features

- Password confirmation on registration
- Minimum password length validation
- JWT token-based authentication
- Automatic redirect on session expiry
- Token stored securely in localStorage
