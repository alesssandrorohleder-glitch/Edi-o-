@echo off
cd /d "%~dp0"
if not exist out mkdir out
del /q out\*.done 2>nul
echo Instalando dependencias (so na primeira vez)...
call npm install > out\log-install.txt 2>&1
echo Gerando quadros de conferencia...
call npm run stills > out\log-stills.txt 2>&1
echo ok > out\stills.done
echo Pronto. Pode fechar esta janela.
