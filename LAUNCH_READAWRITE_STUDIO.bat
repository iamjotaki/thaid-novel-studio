@echo off
title Thai Novel Studio Pro - ReadAWrite
cd /d "c:\ReadAWrite"
python readawrite_studio.py
if errorlevel 1 (
    echo.
    echo [ERROR] An error occurred while launching Thai Novel Studio Pro.
    pause
)
