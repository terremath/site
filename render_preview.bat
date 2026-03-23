@echo off
:: Preview rapide d'une scene (basse qualite, ouvre la video automatiquement)
:: Usage : render_preview.bat Scene05_OndeEau
::         render_preview.bat              (scene par defaut : Scene01_Titre)

set SCENE=%1
if "%SCENE%"=="" set SCENE=Scene01_Titre

echo Rendu preview : %SCENE%
python -m manim -pql --frame_rate 30 -r 1080,1920 jesus_water.py %SCENE%
