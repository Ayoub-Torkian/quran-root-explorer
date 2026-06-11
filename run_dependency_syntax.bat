@echo off
REM One-click runner for MODALITY #47 (dependency-syntax).
REM Double-click this file, or run it from a terminal in this folder.
cd /d "%~dp0"
echo === Modality #47: dependency-syntax local run ===
python run_dependency_syntax.py
echo.
echo Done. See evidence_47_results.txt in this folder.
pause
