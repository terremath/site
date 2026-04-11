@echo off
setlocal enabledelayedexpansion

:: Concatene uniquement les .mp4 deja rendus (pas de manim).
:: Usage : concat_only.bat [fichier.py]
:: Defaut : jesus_water.py

if "%~1"=="" (
    set "PYFILE=jesus_water.py"
    set "MODULE=jesus_water"
) else (
    set "PYFILE=%~1"
    set "MODULE=%~n1"
)

pushd "%~dp0"

for /f "delims=" %%V in ('python -c "import %MODULE%; print(' '.join(%MODULE%.SCENES))"') do set SCENES=%%V
for /f "delims=" %%V in ('python -c "import %MODULE%; print(%MODULE%.OUTPUT_NAME)"') do set OUTNAME=%%V
for /f "delims=" %%V in ('python -c "import %MODULE%; print(%MODULE%.OUTPUT_DIR)"') do set OUTDIR=%%V

if "!SCENES!"=="" ( echo ERREUR : SCENES introuvable dans %PYFILE% & popd & exit /b 1 )
if "!OUTNAME!"=="" ( echo ERREUR : OUTPUT_NAME introuvable & popd & exit /b 1 )
if "!OUTDIR!"==""  ( echo ERREUR : OUTPUT_DIR introuvable & popd & exit /b 1 )

echo ======================================
echo   Concat seulement : %MODULE%
echo   Sortie : !OUTNAME!
echo ======================================

if exist filelist.txt del filelist.txt
for %%S in (!SCENES!) do (
    if not exist "!OUTDIR!\%%S.mp4" (
        echo X Fichier manquant : !OUTDIR!\%%S.mp4
        echo Lancez d'abord render_all.bat %PYFILE% pour cette scene.
        del filelist.txt 2>nul
        popd
        exit /b 1
    )
    echo file '!OUTDIR!\%%S.mp4' >> filelist.txt
)

set "STAGE=!OUTNAME!.new.mp4"
if exist "!STAGE!" del "!STAGE!"

ffmpeg -y -f concat -safe 0 -i filelist.txt -c copy "!STAGE!"
if errorlevel 1 (
    echo X Erreur ffmpeg
    if exist "!STAGE!" del "!STAGE!"
    del filelist.txt
    popd
    exit /b 1
)

del filelist.txt

move /Y "!STAGE!" "!OUTNAME!" >nul 2>&1
if errorlevel 1 (
    echo AVERTISSEMENT : impossible d'ecraser !OUTNAME! ^(fichier ouvert ?^).
    echo Video dans : !STAGE!
    popd
    exit /b 0
)

echo OK - !OUTNAME!
popd
exit /b 0
