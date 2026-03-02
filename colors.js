/**
 * colors.js — Palette & fonts centralisées de TerreMathématiques
 * Modifier ce fichier suffit pour changer l'apparence de tout le site.
 */
(function () {

  // ── PALETTE DE COULEURS ───────────────────────────────────────────
  //
  //  "AUBERGINE & SABLÉ"
  //  Fonds   → aubergine profond (#130E1C) + violet sombre (#221B35)
  //  Textes  → sable crème (#F5EDE0) + sable chaud (#C8BBA8)
  //  Accents → or cuivré (#D4A478)
  //
  //  Pour changer l'accent : modifier --green ET --green-rgb
  //  Pour changer les fonds : modifier --sand + --white
  //
  const palette = {
    // ── Accent : or cuivré ────────────────────────────────────────
    '--green':      '#D4A478',           // or cuivré — CTAs, liens, highlights
    '--green-rgb':  '212, 164, 120',     // composantes R,G,B de --green
    '--green-light':'#E8C090',           // or plus clair
    '--green-soft': 'rgba(var(--green-rgb), 0.12)',

    // ── Fonds : deux tons aubergine ───────────────────────────────
    '--sand':       '#130E1C',           // aubergine profond — fond principal
    '--sand-rgb':   '19, 14, 28',        // composantes R,G,B de --sand (pour dropdowns, drawer)
    '--sand-dark':  'rgba(240,235,230,0.09)', // bordures subtiles
    '--white':      '#221B35',           // violet sombre — sections alternantes

    // ── Textes : sable & crème ────────────────────────────────────
    '--ink':        '#F5EDE0',           // sable crème — titres
    '--ink-rgb':    '245, 237, 224',     // composantes R,G,B de --ink
    '--ink-light':  '#D8C8B0',           // sable doré — sous-titres
    '--text':       '#C8BBA8',           // sable chaud — corps de texte
    '--text-muted': 'rgba(200,185,164,0.6)',
  };

  // ── FONTS GOOGLE ──────────────────────────────────────────────────
  const FONTS_URL =
    'https://fonts.googleapis.com/css2?family=Fraunces:ital,opsz,wght@0,9..144,300;0,9..144,600;0,9..144,800;1,9..144,400&family=Outfit:wght@300;400;500&display=swap';

  // Injection du lien Google Fonts
  const link = document.createElement('link');
  link.rel  = 'stylesheet';
  link.href = FONTS_URL;
  document.head.appendChild(link);

  // Injection des variables CSS
  const vars = Object.entries(palette)
    .map(([prop, val]) => `  ${prop}: ${val};`)
    .join('\n');

  const style = document.createElement('style');
  style.textContent = `:root {\n${vars}\n}`;
  document.head.appendChild(style);

})();
