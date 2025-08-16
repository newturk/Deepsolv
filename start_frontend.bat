@echo off
echo Starting Shopify Insights Frontend...
echo.
cd frontend
echo Installing dependencies...
npm install
echo.
echo Starting development server on http://localhost:5173
echo Press Ctrl+C to stop the server
echo.
npm run dev
pause
