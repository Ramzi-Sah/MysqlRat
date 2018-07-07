@echo off
cls
color b
cd Build
pyinstaller --onefile --clean ../CompileCfg.spec
pause