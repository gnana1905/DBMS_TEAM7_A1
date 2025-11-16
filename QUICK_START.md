# Quick Start Guide

## ⚠️ IMPORTANT: Start the Backend Server First!

The backend server **MUST** be running for the application to work.

### Option 1: Double-Click (Easiest)
1. **Double-click `START_BACKEND.bat`** in the project root folder
2. A terminal window will open showing the server starting
3. **Keep this window open** - don't close it!
4. You should see: `* Running on http://0.0.0.0:5000`

### Option 2: Manual Start
1. Open **Command Prompt** or **PowerShell**
2. Navigate to the project folder:
   ```bash
   cd C:\Users\Gnana\Desktop\EaseStay
   ```
3. Go to backend folder:
   ```bash
   cd backend
   ```
4. Start the server:
   ```bash
   python app.py
   ```
5. **Keep the terminal window open!**

### Verify Server is Running
Open your browser and go to: **http://localhost:5000/api/health**

You should see:
```json
{
  "status": "healthy",
  "message": "EaseStay API is running",
  "database": "connected"
}
```

### Troubleshooting

**Error: "Cannot connect to server"**
- ✅ Make sure the backend server is running (see above)
- ✅ Check that MongoDB is running on `localhost:27017`
- ✅ Verify the terminal window with the server is still open

**Error: "Module not found"**
- Run: `pip install -r backend/requirements.txt`

**Error: "Port 5000 already in use"**
- Close any other application using port 5000
- Or change the port in `backend/app.py` (line 186)

### Test Credentials
- **Admin**: admin@easestay.com / admin123
- **Staff**: staff@easestay.com / staff123
- **Guest**: guest@easestay.com / guest123

