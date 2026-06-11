@echo off
setlocal enableextensions
cd /d "%~dp0"
title Deploy Quran Root Explorer

REM ---- clear a stale git lock left by an interrupted run / GitHub Desktop ----
if exist ".git\index.lock" (
  echo Removing stale .git\index.lock ...
  del /f /q ".git\index.lock"
)

REM ---- locate git, even if it is not on PATH ----
set "GIT="
where git >nul 2>&1 && set "GIT=git"
if not defined GIT if exist "%ProgramFiles%\Git\cmd\git.exe" set "GIT=%ProgramFiles%\Git\cmd\git.exe"
if not defined GIT if exist "%ProgramFiles(x86)%\Git\cmd\git.exe" set "GIT=%ProgramFiles(x86)%\Git\cmd\git.exe"
if not defined GIT if exist "%LocalAppData%\Programs\Git\cmd\git.exe" set "GIT=%LocalAppData%\Programs\Git\cmd\git.exe"
if not defined GIT (
  echo.
  echo ERROR: Git was not found on this PC's PATH.
  echo Open "Git Bash" instead and run these three lines:
  echo     git add -A
  echo     git commit -m "deploy"
  echo     git push origin main ^&^& git push hf main
  echo.
  pause
  exit /b 1
)

echo Using git: %GIT%
"%GIT%" --version
echo.

echo === Changes to deploy ===
"%GIT%" status --short
echo.

echo === Staging all changes ===
"%GIT%" add -A

echo === Committing ===
"%GIT%" commit -m "auto update %DATE% %TIME%"
echo.

echo === Pushing to GitHub (origin/main) ===
"%GIT%" push origin main
echo.

echo === Pushing to Hugging Face (hf/main) ===
"%GIT%" push hf main
echo.

echo ================================================================
echo  FINISHED. Read the lines above:
echo   - "main -^> main" under each push = SUCCESS.
echo   - "Authentication failed" / "could not read Username" = sign-in needed.
echo   - "Everything up-to-date" = nothing new to send.
echo ================================================================
echo.
pause
