# How to Start the Backend Server

## Quick Start

1. **Open a terminal/command prompt**

2. **Navigate to the backend folder:**
   ```bash
   cd backend
   ```

3. **Install dependencies (if not already installed):**
   ```bash
   pip install -r requirements.txt
   ```

4. **Make sure MongoDB is running:**
   - MongoDB should be running on `localhost:27017`
   - If not installed, download from: https://www.mongodb.com/try/download/community

5. **Seed the database (optional, first time only):**
   ```bash
   python seed_data.py
   ```

6. **Start the Flask server:**
   ```bash
   python app.py
   ```

7. **You should see:**
   ```
   Starting EaseStay Flask Server...
   MongoDB URI: mongodb://localhost:27017/easestay
   API endpoints available at http://localhost:5000/api
   * Running on http://0.0.0.0:5000
   ```

8. **Keep this terminal window open** - the server must be running for the frontend to work!

## Using the Batch File (Windows)

Simply double-click `start_backend.bat` in the project root folder.

## Troubleshooting

- **"Cannot connect to server" error**: Make sure the backend server is running (step 6)
- **MongoDB connection error**: Make sure MongoDB is installed and running
- **Port 5000 already in use**: Close any other application using port 5000, or change the port in `backend/app.py`

## Verify Backend is Running

Open your browser and go to: http://localhost:5000/api/health

You should see:
```json
{
  "status": "healthy",
  "message": "EaseStay API is running",
  "database": "connected"
}
```

