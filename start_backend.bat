@echo off
echo ============================================
echo Starting EaseStay Backend Server
echo ============================================
echo.
cd backend
echo Starting Flask server on http://localhost:5000
echo.
echo IMPORTANT: Keep this window open while using the application!
echo Press Ctrl+C to stop the server
echo.
python app.py
pause
