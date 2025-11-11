@echo off
echo ====================================
echo   E-Voting System - Starting Server
echo ====================================
echo.
echo Installing dependencies (if needed)...
pip install -q Flask
echo.
echo Starting server on http://localhost:5000
echo Open your browser and navigate to: http://localhost:5000
echo.
echo Press Ctrl+C to stop the server
echo.
python app.py
pause

