/**
 * colors.js — Palette & fonts centralisées de TerreMathématiques
 * Modifier ce fichier suffit pour changer l'apparence de tout le site.
 */
(function () {

  // ── PALETTE DE COULEURS ───────────────────────────────────────────
  //
  //  "AUBERGINE & SABLÉ — THÈME MIXTE"
  //  Sections sombres  → aubergine profond (#130E1C) + aubergine (#2A1020)
  //  Sections claires  → sable chaud (#F5EAD6) + crème (#FAF6EE)
  //  Textes sombres    → sable crème (#F5EDE0) + sable chaud (#C8BBA8)
  //  Textes clairs     → via classe .section--light (aubergine profond)
  //  Accents           → or cuivré (#D4A478)
  //
  //  Pour changer l'accent : modifier --green ET --green-rgb
  //  Pour les sections claires : ajouter class="section--light" + background: var(--sand-warm)
  //
  const palette = {
    // ── Accent : or cuivré ────────────────────────────────────────
    '--green':      '#D4A478',           // or cuivré — CTAs, liens, highlights
    '--green-rgb':  '212, 164, 120',     // composantes R,G,B de --green
    '--green-light':'#E8C090',           // or plus clair
    '--green-soft': 'rgba(var(--green-rgb), 0.12)',

    // ── Aubergine accent (bordure logo) ──────────────────────────
    '--aubergine':      '#8B4D7F',       // aubergine moyen — bordures logo
    '--aubergine-rgb':  '139, 77, 127',  // composantes R,G,B de --aubergine

    // ── Fonds sombres ─────────────────────────────────────────────
    '--sand':       '#130E1C',           // aubergine profond — fond principal / body
    '--sand-rgb':   '19, 14, 28',        // composantes R,G,B de --sand
    '--sand-dark':  'rgba(240,235,230,0.09)', // bordures subtiles (sections sombres)
    '--white':      '#2A1020',           // aubergine — sections alternantes sombres, cards

    // ── Fonds clairs ──────────────────────────────────────────────
    '--sand-warm':  '#F5EAD6',           // sable chaud — sections lumineuses (+ class section--light)
    '--cream':      '#FAF6EE',           // crème — le plus clair (cards dans sections lumineuses)

    // ── Textes (fond sombre) : sable & crème ──────────────────────
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

  // CSS pour sections claires : cascade les textes sombres + overrides cards
  const lightSection = `
.section--light {
  --ink: #2A0A2E;
  --ink-rgb: 42, 10, 46;
  --ink-light: #6B2D5B;
  --text: #5A2A50;
  --text-muted: rgba(74, 25, 66, 0.55);
  --sand-dark: rgba(74, 25, 66, 0.15);
  --white: var(--cream);
}`;

  const style = document.createElement('style');
  style.textContent = `:root {\n${vars}\n}${lightSection}`;
  document.head.appendChild(style);

})();
