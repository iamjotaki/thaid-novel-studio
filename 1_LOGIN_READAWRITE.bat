@echo off
title ReadAWrite Setup
echo ========================================================
echo   Launching Chrome for ReadAWrite Login...
echo ========================================================
echo.
echo   1. Please login to your ReadAWrite account.
echo   2. When done, you can close Chrome.
echo.
echo ========================================================
start "" "C:\Program Files\Google\Chrome\Application\chrome.exe" --user-data-dir="c:\ReadAWrite\chrome_profile" --no-first-run --no-default-browser-check "https://www.readawrite.com/?action=main_manage_article"
echo.
pause
