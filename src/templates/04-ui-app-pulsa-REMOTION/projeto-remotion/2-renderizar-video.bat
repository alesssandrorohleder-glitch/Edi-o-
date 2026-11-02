@echo off
cd /d "%~dp0"
if not exist out mkdir out
del /q out\render.done 2>nul
echo Renderizando o video final...
call npm run render > out\log-render.txt 2>&1
echo ok > out\render.done
echo Pronto! O video esta em out\PortfolioUI.mp4
pause
