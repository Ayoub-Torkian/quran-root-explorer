@echo off
REM Double-click to deploy: stages all changes, commits, pushes to GitHub + Hugging Face.
cd /d "%~dp0"
echo === Changes to deploy ===
git status --short
echo.
set /p MSG="Commit message (Enter for default): "
if "%MSG%"=="" set MSG=update app
git add -A
git commit -m "%MSG%"
echo.
echo === Pushing to GitHub (origin) ===
git push origin main
echo === Pushing to Hugging Face (hf) ===
git push hf main
echo.
echo Done. Live app rebuilds in ~1-2 min.
pause
