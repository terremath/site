@echo off
setlocal enabledelayedexpansion

:: ─── Paramètre obligatoire ──────────────────────────────────────────────────
if "%~1"=="" (
    echo Usage : render_all.bat ^<fichier.py^>
    echo Exemple: render_all.bat jesus_water.py
    exit /b 1
)

set PYFILE=%~1
set MODULE=%~n1

:: ─── Lecture des métadonnées depuis le fichier Python ───────────────────────
for /f "delims=" %%V in ('python -c "import %MODULE%; print(' '.join(%MODULE%.SCENES))"') do set SCENES=%%V
for /f "delims=" %%V in ('python -c "import %MODULE%; print(%MODULE%.OUTPUT_NAME)"') do set OUTNAME=%%V
for /f "delims=" %%V in ('python -c "import %MODULE%; print(%MODULE%.OUTPUT_DIR)"') do set OUTDIR=%%V

if "!SCENES!"=="" ( echo ERREUR : impossible de lire SCENES dans %PYFILE% & exit /b 1 )
if "!OUTNAME!"=="" ( echo ERREUR : impossible de lire OUTPUT_NAME dans %PYFILE% & exit /b 1 )
if "!OUTDIR!"==""  ( echo ERREUR : impossible de lire OUTPUT_DIR dans %PYFILE% & exit /b 1 )

:: ─── Paramètres Manim ───────────────────────────────────────────────────────
set QUALITY=-qh
set RES=-r 1080,1920
set FPS=--frame_rate 30

echo ======================================
echo   Projet  : %MODULE%
echo   Sortie  : !OUTNAME!
echo ======================================

:: ─── Rendu des scènes ────────────────────────────────────────────────────────
for %%S in (!SCENES!) do (
    echo.
    echo --^> Rendu %%S...
    python -m manim %QUALITY% %FPS% %RES% %PYFILE% %%S
    if errorlevel 1 (
        echo X ERREUR sur %%S
        exit /b 1
    )
    echo OK %%S
)

:: ─── Concaténation ffmpeg ────────────────────────────────────────────────────
echo.
echo ======================================
echo   Concatenation avec ffmpeg
echo ======================================

if exist filelist.txt del filelist.txt

for %%S in (!SCENES!) do (
    echo file '!OUTDIR!\%%S.mp4' >> filelist.txt
)

:: Fichier temporaire : évite "Permission denied" si !OUTNAME! est ouvert
:: (lecteur vidéo, navigateur, aperçu Cursor, OneDrive, etc.)
set "STAGE=!OUTNAME!.new.mp4"
if exist "!STAGE!" del "!STAGE!"

ffmpeg -y -f concat -safe 0 -i filelist.txt -c copy "!STAGE!"

if errorlevel 1 (
    echo X Erreur ffmpeg
    if exist "!STAGE!" del "!STAGE!"
    del filelist.txt
    exit /b 1
)

del filelist.txt

move /Y "!STAGE!" "!OUTNAME!" >nul 2>&1
if errorlevel 1 (
    echo.
    echo AVERTISSEMENT : impossible d'ecraser !OUTNAME! ^(fichier verrouille / ouvert ailleurs^).
    echo La video complete est dans : !STAGE!
    echo Fermez lecteur, onglet video ou l'onglet du .mp4 dans l'IDE, puis :
    echo   del !OUTNAME! ^&^& move /Y !STAGE! !OUTNAME!
    echo.
    echo ======================================
    echo   OK ^(staging^) - !STAGE!
    echo   Scenes individuelles : !OUTDIR!\
    echo ======================================
    exit /b 0
)

echo.
echo ======================================
echo   OK - !OUTNAME!
echo   Scenes individuelles : !OUTDIR!\
echo ======================================

start "" "!OUTNAME!"
