/**
 * colors.js — Palette & fonts centralisées de TerreMathématiques
 * Modifier ce fichier suffit pour changer l'apparence de tout le site.
 */
(function () {

  // ── PALETTE DE COULEURS ───────────────────────────────────────────
  //
  //  "AUBERGINE & SABLÉ — THÈME MIXTE"
  //  Fonds sombres   → --bg (#130E1C) + --bg-alt (#2A1020)
  //  Fonds clairs    → --bg-light (#F5EAD6) + --bg-light-alt (#FAF6EE)
  //  Textes sombres  → --heading (#F5EDE0) + --text (#C8BBA8)
  //  Textes clairs   → via classe .section--light (aubergine profond)
  //  Accent          → --accent (#D4A478) — or cuivré
  //
  //  Pour changer l'accent : modifier --accent ET --accent-rgb
  //  Pour les sections claires : ajouter class="section--light" + background: var(--bg-light)
  //
  const palette = {
    // ── Accent : or cuivré ────────────────────────────────────────
    '--accent':      '#D4A478',           // or cuivré — CTAs, liens, highlights, newsletter
    '--accent-rgb':  '212, 164, 120',     // composantes R,G,B de --accent
    '--accent-light':'#E8C090',           // or plus clair — dégradés boutons, hovers
    '--accent-soft': 'rgba(var(--accent-rgb), 0.12)',

    // ── Deep aubergine (bordure logo) ────────────────────────────
    '--deep':      '#2A1020',             // aubergine moyen — bordures logo
    '--deep-rgb':  '139, 77, 127',        // composantes R,G,B de --deep

    // ── Fonds sombres ─────────────────────────────────────────────
    '--bg':       '#130E1C',              // aubergine profond — fond principal / body
    '--bg-rgb':   '19, 14, 28',           // composantes R,G,B de --bg
    '--border':   'rgba(240,235,230,0.09)', // bordures subtiles (sections sombres)
    '--bg-alt':   '#2A1020',              // aubergine — sections alternantes sombres, cards

    // ── Fonds clairs ──────────────────────────────────────────────
    '--bg-light':     '#F5EAD6',          // sable chaud — sections lumineuses (+ class section--light)
    '--bg-light-alt': '#FAF6EE',          // crème — le plus clair (cards dans sections lumineuses)

    // ── Textes (fond sombre) : sable & crème ──────────────────────
    '--heading':      '#F5EDE0',          // sable crème — titres
    '--heading-rgb':  '245, 237, 224',    // composantes R,G,B de --heading
    '--heading-soft': '#D8C8B0',          // sable doré — sous-titres
    '--text':         '#C8BBA8',          // sable chaud — corps de texte
    '--text-muted':   'rgba(200,185,164,0.6)',
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
  --heading: #2A0A2E;
  --heading-rgb: 42, 10, 46;
  --heading-soft: #6B2D5B;
  --text: #5A2A50;
  --text-muted: rgba(74, 25, 66, 0.55);
  --border: rgba(74, 25, 66, 0.15);
  --bg-alt: var(--bg-light-alt);
}`;

  const style = document.createElement('style');
  style.textContent = `:root {\n${vars}\n}${lightSection}`;
  document.head.appendChild(style);

})();
