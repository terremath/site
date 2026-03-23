@echo off
setlocal enabledelayedexpansion

set FILE=jesus_water.py
set OUTDIR=media\videos\jesus_water\1920p30
set QUALITY=-qh
set RES=-r 1080,1920
set FPS=--frame_rate 30

set SCENES=Scene01_Titre Scene02_ConditionMecanique Scene03_ModeleImpact Scene04_ForcesAnimees Scene05_OndeEau Scene06_VitesseImpossible Scene07_GrapheGravite Scene08_Basilic Scene09_ForceDivine Scene10_Conclusion Scene11_CTA

echo ======================================
echo   Rendu de toutes les scenes Manim
echo ======================================

for %%S in (%SCENES%) do (
    echo.
    echo --^> Rendu %%S...
    python -m manim %QUALITY% %FPS% %RES% %FILE% %%S
    if errorlevel 1 (
        echo X ERREUR sur %%S
        exit /b 1
    )
    echo OK %%S
)

echo.
echo ======================================
echo   Concatenation avec ffmpeg
echo ======================================

if exist filelist.txt del filelist.txt

for %%S in (%SCENES%) do (
    echo file '%OUTDIR%\%%S.mp4' >> filelist.txt
)

ffmpeg -y -f concat -safe 0 -i filelist.txt -c copy marcher_sur_eau_FINAL.mp4

if errorlevel 1 (
    echo X Erreur ffmpeg
    exit /b 1
)

del filelist.txt
echo.
echo ======================================
echo   OK - marcher_sur_eau_FINAL.mp4
echo   Scenes individuelles : %OUTDIR%\
echo ======================================
