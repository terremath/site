#!/bin/bash
# ═══════════════════════════════════════════════════════
#  Render toutes les scènes + concaténation ffmpeg
#  Usage: chmod +x render_all.sh && ./render_all.sh
# ═══════════════════════════════════════════════════════

SCENES=(
    Scene01_Titre
    Scene02_ConditionMecanique
    Scene03_ModeleImpact
    Scene04_ForcesAnimees
    Scene05_OndeEau
    Scene06_VitesseImpossible
    Scene07_GrapheGravite
    Scene08_Basilic
    Scene09_ForceDivine
    Scene10_Conclusion
    Scene11_CTA
)

QUALITY="-qh"           # haute qualité (-ql pour preview rapide)
FPS="--frame_rate 30"
RES="-r 1080,1920"       # Format TikTok 9:16
FILE="jesus_water.py"
OUTDIR="media/videos/jesus_water/1080p30"

echo "══════════════════════════════════════"
echo "  Rendu de ${#SCENES[@]} scènes"
echo "══════════════════════════════════════"

for scene in "${SCENES[@]}"; do
    echo ""
    echo "→ Rendu $scene..."
    manim $QUALITY $FPS $RES "$FILE" "$scene"

    if [ $? -ne 0 ]; then
        echo "✗ ERREUR sur $scene"
        exit 1
    fi
    echo "✓ $scene OK"
done

echo ""
echo "══════════════════════════════════════"
echo "  Concaténation avec ffmpeg"
echo "══════════════════════════════════════"

LISTFILE="filelist.txt"
> "$LISTFILE"

for scene in "${SCENES[@]}"; do
    echo "file '${OUTDIR}/${scene}.mp4'" >> "$LISTFILE"
done

ffmpeg -y -f concat -safe 0 -i "$LISTFILE" -c copy "marcher_sur_eau_FINAL.mp4"

if [ $? -eq 0 ]; then
    echo ""
    echo "══════════════════════════════════════"
    echo "  ✓ TERMINÉ !"
    echo "  → marcher_sur_eau_FINAL.mp4"
    echo "  → Scènes individuelles dans $OUTDIR/"
    echo "══════════════════════════════════════"
    echo ""
    echo "  Pour DaVinci Resolve :"
    echo "  - Importer les scènes individuelles depuis $OUTDIR/"
    echo "  - Timeline : 1080×1920, 30fps"
    echo "  - Ajouter sound design, transitions, overlays"
else
    echo "✗ Erreur ffmpeg"
    exit 1
fi

rm -f "$LISTFILE"
