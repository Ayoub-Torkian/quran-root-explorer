@echo off
cd /d "%~dp0"
echo ============================================
echo  Quran Root Explorer - GitHub setup (one-time)
echo ============================================
echo.

git --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: git is not installed. Install from https://git-scm.com/download/win
    pause & exit /b 1
)

if exist ".git" (
    echo A git repo already exists here - skipping init.
) else (
    git init -b main
    git add -A
    git commit -m "v2.0 - re-spine, Lens Lab, live lenses, ayah hero + mask, design system (full snapshot)"
    echo.
    echo Local repository created with the v2.0 snapshot.
)

echo.
echo NEXT STEP - connect to GitHub (pick one):
echo.
echo  A) If you have GitHub CLI (gh):
echo       gh auth login
echo       gh repo create quran-root-explorer --private --source . --push
echo.
echo  B) Manual: create an empty PRIVATE repo named quran-root-explorer
echo     at https://github.com/new  then run:
echo       git remote add origin https://github.com/YOUR_USERNAME/quran-root-explorer.git
echo       git push -u origin main
echo.
echo From then on, after each work session just run:  git add -A ^&^& git commit -m "..." ^&^& git push
pause
