@echo off
echo ========================================
echo   Algo Trading MVP - Quick Deploy
echo ========================================
echo.
echo Step 1: GitHub pe jao
start https://github.com/new?name=algo-trading-mvp
echo.
echo Step 2: Repo banao
echo    - "uploading an existing file" click karo
echo    - ZIP extract karo: %CD%\..\algo-trading-mvp-deploy.zip
echo    - algo-trading-mvp folder ka andar ka sab drag-drop karo
echo.
echo Step 3: Render deploy
start https://render.com
echo.
echo Render me: New - Web Service - GitHub connect - algo-trading-mvp select - Deploy
echo.
echo 5-10 min baad link milega!
echo.
pause
