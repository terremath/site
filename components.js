/* ═══════════════════════════════════════════════════════════
   TERRE MATHÉMATIQUES — Web Components (Header + Footer)
   Fichier unique : components.js
   Usage :
     <script src="components.js"></script>
     <tm-header></tm-header>    — navbar animée (pages principales)
     <tm-header-simple></tm-header-simple> — navbar simple (pages légales)
     <tm-footer></tm-footer>
════════════════════════════════════════════════════════════ */

/* ─────────────────────────────────────────────
   FOOTER (identique partout)
───────────────────────────────────────────── */
class TmFooter extends HTMLElement {
  connectedCallback() {
    this.innerHTML = `
<footer>
  <div class="footer-inner">
    <a href="https://www.terremathematiques.com/" class="footer-left">
      <img src="logo.jpg" alt="Terre Mathématiques">
      <div class="footer-brand">
        <span>Terre</span>
        <span>Mathématiques</span>
        <p class="footer-copy">&copy; 2026 — Tous droits réservés.</p>
      </div>
    </a>
    <div class="footer-right">
      <div class="footer-legal">
        <a href="/mentions-legales.html">Mentions légales</a>
        <a href="/politique-confidentialite.html">Confidentialité</a>
        <a href="/politique-cookies.html">Cookies</a>
        <a href="/conditions-generales-vente.html">CGV</a>
      </div>
      <div class="footer-socials">
        <a href="https://www.instagram.com/terremathematiques?igsh=bWlreDlha3J5ZzY1" target="_blank" rel="noopener" aria-label="Instagram">
          <svg viewBox="0 0 24 24"><path d="M12 2.163c3.204 0 3.584.012 4.85.07 3.252.148 4.771 1.691 4.919 4.919.058 1.265.069 1.645.069 4.849 0 3.205-.012 3.584-.069 4.849-.149 3.225-1.664 4.771-4.919 4.919-1.266.058-1.644.07-4.85.07-3.204 0-3.584-.012-4.849-.07-3.26-.149-4.771-1.699-4.919-4.92-.058-1.265-.07-1.644-.07-4.849 0-3.204.013-3.583.07-4.849.149-3.227 1.664-4.771 4.919-4.919 1.266-.057 1.645-.069 4.849-.069zM12 0C8.741 0 8.333.014 7.053.072 2.695.272.273 2.69.073 7.052.014 8.333 0 8.741 0 12c0 3.259.014 3.668.072 4.948.2 4.358 2.618 6.78 6.98 6.98C8.333 23.986 8.741 24 12 24c3.259 0 3.668-.014 4.948-.072 4.354-.2 6.782-2.618 6.979-6.98.059-1.28.073-1.689.073-4.948 0-3.259-.014-3.667-.072-4.947-.196-4.354-2.617-6.78-6.979-6.98C15.668.014 15.259 0 12 0zm0 5.838a6.162 6.162 0 100 12.324 6.162 6.162 0 000-12.324zM12 16a4 4 0 110-8 4 4 0 010 8zm6.406-11.845a1.44 1.44 0 100 2.881 1.44 1.44 0 000-2.881z"/></svg>
        </a>
        <a href="https://www.facebook.com/share/1AfXwdGbxo/?mibextid=wwXIfr" target="_blank" rel="noopener" aria-label="Facebook">
          <svg viewBox="0 0 24 24"><path d="M24 12.073c0-6.627-5.373-12-12-12s-12 5.373-12 12c0 5.99 4.388 10.954 10.125 11.854v-8.385H7.078v-3.47h3.047V9.43c0-3.007 1.792-4.669 4.533-4.669 1.312 0 2.686.235 2.686.235v2.953H15.83c-1.491 0-1.956.925-1.956 1.874v2.25h3.328l-.532 3.47h-2.796v8.385C19.612 23.027 24 18.062 24 12.073z"/></svg>
        </a>
        <a href="https://www.tiktok.com/@terremathematiques?_r=1" target="_blank" rel="noopener" aria-label="TikTok">
          <svg viewBox="0 0 24 24"><path d="M12.525.02c1.31-.02 2.61-.01 3.91-.02.08 1.53.63 3.09 1.75 4.17 1.12 1.11 2.7 1.62 4.24 1.79v4.03c-1.44-.05-2.89-.35-4.2-.97-.57-.26-1.1-.59-1.62-.93-.01 2.92.01 5.84-.02 8.75-.08 1.4-.54 2.79-1.35 3.94-1.31 1.92-3.58 3.17-5.91 3.21-1.43.08-2.86-.31-4.08-1.03-2.02-1.19-3.44-3.37-3.65-5.71-.02-.5-.03-1-.01-1.49.18-1.9 1.12-3.72 2.58-4.96 1.66-1.44 3.98-2.13 6.15-1.72.02 1.48-.04 2.96-.04 4.44-.99-.32-2.15-.23-3.02.37-.63.41-1.11 1.04-1.36 1.75-.21.51-.15 1.07-.14 1.61.24 1.64 1.82 3.02 3.5 2.87 1.12-.01 2.19-.66 2.77-1.61.19-.33.4-.67.41-1.06.1-1.79.06-3.57.07-5.36.01-4.03-.01-8.05.02-12.07z"/></svg>
        </a>
        <a href="https://www.youtube.com/@TerreMathematiques" target="_blank" rel="noopener" aria-label="YouTube">
          <svg viewBox="0 0 24 24"><path d="M23.498 6.186a3.016 3.016 0 00-2.122-2.136C19.505 3.545 12 3.545 12 3.545s-7.505 0-9.377.505A3.017 3.017 0 00.502 6.186C0 8.07 0 12 0 12s0 3.93.502 5.814a3.016 3.016 0 002.122 2.136c1.871.505 9.376.505 9.376.505s7.505 0 9.377-.505a3.015 3.015 0 002.122-2.136C24 15.93 24 12 24 12s0-3.93-.502-5.814zM9.545 15.568V8.432L15.818 12l-6.273 3.568z"/></svg>
        </a>
      </div>
    </div>
  </div>
</footer>`;
  }
}
customElements.define('tm-footer', TmFooter);


/* ─────────────────────────────────────────────
   NAVBAR CSS — injecté une seule fois dans <head>
───────────────────────────────────────────── */
(function injectNavCSS() {
  if (document.getElementById('tm-nav-styles')) return;
  const style = document.createElement('style');
  style.id = 'tm-nav-styles';
  style.textContent = `
.tm-nav {
  --nav-h: 130px;
  position: relative;
  width: 100%;
  height: var(--nav-h);
  background: #0a0805;
  box-sizing: border-box;
  font-family: 'Cormorant Garamond', Georgia, serif;
  overflow: visible;
  z-index: 100;
}
.tm-nav::after {
  content: '';
  position: absolute;
  bottom: 0; left: 0; right: 0; height: 1px;
  background: linear-gradient(90deg,
    transparent 0%, rgba(201,168,76,0.3) 20%,
    rgba(201,168,76,0.6) 50%, rgba(201,168,76,0.3) 80%, transparent 100%);
  z-index: 20; pointer-events: none;
}

/* ── Formulas — continuous breathing + drifting ── */
.tm-inner {
  position: absolute; inset: 0;
  overflow: hidden; pointer-events: none;
}
.tm-f {
  position: absolute;
  font-family: 'EB Garamond', Georgia, serif;
  font-style: italic; font-weight: 500;
  color: rgba(201,168,76,0.7);
  white-space: nowrap;
  text-shadow: 0 0 20px rgba(201,168,76,0.5), 0 0 44px rgba(201,168,76,0.15);
  animation:
    tm-breathe var(--dur) ease-in-out var(--delay) infinite,
    tm-drift var(--drift) ease-in-out var(--delay) infinite;
  will-change: opacity, transform;
}
@keyframes tm-breathe {
  0%, 100% { opacity: 0; }
  20%      { opacity: 0.65; }
  50%      { opacity: 0.3; }
  80%      { opacity: 0.65; }
}
@keyframes tm-drift {
  0%, 100% { transform: translate(0, 0); }
  25%      { transform: translate(var(--dx), var(--dy)); }
  50%      { transform: translate(calc(var(--dx) * -0.6), calc(var(--dy) * 1.3)); }
  75%      { transform: translate(calc(var(--dx) * 0.8), calc(var(--dy) * -0.7)); }
}

/* ── Logo — visible immediately, bottom-left ── */
.tm-left-logo {
  position: absolute; bottom: 12px; left: 22px;
  z-index: 15;
  display: flex; align-items: center; gap: 12px;
  text-decoration: none;
  opacity: 0;
  animation: tm-fadein 0.6s ease 0.1s forwards;
}
.tm-left-logo img {
  width: 48px; height: 48px; border-radius: 50%;
  border: 1.5px solid rgba(201,168,76,0.5);
  box-shadow: 0 0 16px rgba(201,168,76,0.25);
  object-fit: cover; flex-shrink: 0;
}
.tm-left-logo .tm-ltitle {
  display: flex; flex-direction: column; line-height: 1.15;
}
.tm-left-logo .tm-ltitle span {
  font-family: 'Cormorant Garamond', serif;
  font-weight: 700; font-size: 0.88rem;
  color: rgba(201,168,76,0.88); letter-spacing: 4.5px;
  text-transform: uppercase;
  text-shadow: 0 0 12px rgba(201,168,76,0.3);
}
@keyframes tm-fadein { from { opacity:0; transform: translateX(-6px); } to { opacity:1; transform: translateX(0); } }

/* ── Menu — visible immediately, bottom-right ── */
.tm-menu {
  position: absolute; bottom: 18px; right: 22px;
  z-index: 200;
  display: flex; align-items: center; gap: 0;
  opacity: 0;
  animation: tm-fadein-menu 0.6s ease 0.15s forwards;
}
@keyframes tm-fadein-menu { from { opacity:0; } to { opacity:1; } }

.tm-menu > a, .tm-dd > a {
  font-family: 'Cormorant Garamond', serif;
  font-weight: 600; font-size: 0.84rem;
  color: rgba(201,168,76,0.75);
  text-decoration: none; letter-spacing: 2.5px;
  text-transform: uppercase;
  padding: 6px 11px;
  border-radius: 2px;
  transition: color 0.3s, text-shadow 0.3s;
  white-space: nowrap; display: inline-block;
  position: relative;
}
.tm-menu > a::after, .tm-dd > a::after {
  content: '';
  position: absolute;
  bottom: 2px; left: 11px; right: 11px;
  height: 1px;
  background: rgba(201,168,76,0);
  transition: background 0.3s ease;
}
.tm-menu > a:hover, .tm-dd:hover > a {
  color: #e2c06a;
  text-shadow: 0 0 10px rgba(201,168,76,0.4);
}
.tm-menu > a:hover::after, .tm-dd:hover > a::after {
  background: rgba(201,168,76,0.4);
}
.tm-menu > a.tm-active {
  color: #e2c06a;
  text-shadow: 0 0 10px rgba(201,168,76,0.4);
}
.tm-menu > a.tm-active::after {
  background: rgba(201,168,76,0.4);
}

/* ── Dropdowns ── */
.tm-dd { position: relative; }
.tm-dd-panel {
  display: none; position: absolute; top: calc(100% + 6px); left: 50%;
  transform: translateX(-50%);
  min-width: 210px; background: rgba(10,8,5,0.97);
  backdrop-filter: blur(14px);
  border: 1px solid rgba(201,168,76,0.15);
  border-top: 1.5px solid rgba(201,168,76,0.45);
  padding: 6px 0; z-index: 9999;
  box-shadow: 0 10px 32px rgba(0,0,0,0.6);
  border-radius: 4px;
}
.tm-dd:hover .tm-dd-panel { display: block; }
.tm-dd-panel a {
  display: block; font-family: 'Cormorant Garamond', serif;
  font-weight: 600; font-size: 0.78rem;
  letter-spacing: 2px; text-transform: uppercase;
  text-decoration: none; padding: 10px 18px;
  color: rgba(201,168,76,0.6);
  transition: color 0.2s, background 0.2s, padding-left 0.2s;
}
.tm-dd-panel a:hover { color: #e2c06a; background: rgba(201,168,76,0.05); padding-left: 22px; }

/* ── Hamburger (mobile) ── */
#tm-toggle { display: none; }
.tm-hamburger {
  display: none; position: absolute;
  top: 50%; right: 18px; transform: translateY(-50%);
  z-index: 300; cursor: pointer; padding: 8px;
  flex-direction: column; gap: 5px;
}
.tm-hamburger span {
  display: block; width: 24px; height: 1.5px;
  background: rgba(201,168,76,0.8); border-radius: 2px;
  transition: transform 0.3s, opacity 0.3s;
  transform-origin: center;
}

/* Hamburger animation via JS class */
.tm-nav.drawer-open .tm-hamburger span:nth-child(1) { transform: translateY(6.5px) rotate(45deg); }
.tm-nav.drawer-open .tm-hamburger span:nth-child(2) { opacity: 0; }
.tm-nav.drawer-open .tm-hamburger span:nth-child(3) { transform: translateY(-6.5px) rotate(-45deg); }

/* Also support the checkbox sibling method */
#tm-toggle:checked ~ tm-header .tm-nav .tm-hamburger span:nth-child(1),
#tm-toggle:checked ~ .tm-nav .tm-hamburger span:nth-child(1) { transform: translateY(6.5px) rotate(45deg); }
#tm-toggle:checked ~ tm-header .tm-nav .tm-hamburger span:nth-child(2),
#tm-toggle:checked ~ .tm-nav .tm-hamburger span:nth-child(2) { opacity: 0; }
#tm-toggle:checked ~ tm-header .tm-nav .tm-hamburger span:nth-child(3),
#tm-toggle:checked ~ .tm-nav .tm-hamburger span:nth-child(3) { transform: translateY(-6.5px) rotate(-45deg); }

/* ── Mobile drawer ── */
.tm-drawer {
  position: absolute; top: 100%; left: 0; right: 0;
  background: rgba(10,8,5,0.98);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid rgba(201,168,76,0.15);
  z-index: 25; max-height: 0; overflow: hidden;
  transition: max-height 0.4s ease;
}
.tm-nav.drawer-open .tm-drawer { max-height: 600px; }
#tm-toggle:checked ~ tm-header .tm-nav .tm-drawer,
#tm-toggle:checked ~ .tm-nav .tm-drawer { max-height: 600px; }
.tm-drawer-inner { padding: 8px 0 20px; }
.tm-drawer a {
  display: block; font-family: 'Cormorant Garamond', serif;
  font-weight: 600; font-size: 0.95rem;
  color: rgba(201,168,76,0.75); text-decoration: none;
  letter-spacing: 2.5px; text-transform: uppercase;
  padding: 11px 24px;
  border-bottom: 1px solid rgba(201,168,76,0.05);
  transition: color 0.2s, background 0.2s;
}
.tm-drawer a:hover { color: #e2c06a; background: rgba(201,168,76,0.04); }
.tm-drawer-section {
  font-family: 'EB Garamond', serif; font-style: italic;
  font-size: 0.68rem; color: rgba(201,168,76,0.3);
  letter-spacing: 3px; text-transform: uppercase;
  padding: 14px 24px 3px;
}
.tm-drawer .tm-sub {
  padding-left: 40px; font-size: 0.82rem;
  letter-spacing: 2px; color: rgba(201,168,76,0.55);
}
@media (max-width: 768px) {
  .tm-nav { --nav-h: 64px; }
  .tm-menu  { display: none !important; }
  .tm-hamburger { display: flex; }
  .tm-left-logo { bottom: 8px; }
  .tm-left-logo img { width: 38px; height: 38px; }
  .tm-left-logo .tm-ltitle span { font-size: 0.74rem; letter-spacing: 3px; }
  .tm-f { display: none; }
}
@media (min-width: 769px) {
  .tm-hamburger { display: none !important; }
  .tm-drawer    { display: none !important; }
  #tm-toggle    { display: none !important; }
}
`;
  document.head.appendChild(style);
})();


/* ─────────────────────────────────────────────
   HEADER ANIMÉ (pages principales)
───────────────────────────────────────────── */
class TmHeader extends HTMLElement {
  connectedCallback() {
    // Injecter le checkbox toggle juste avant ce composant
    if (!document.getElementById('tm-toggle')) {
      const toggle = document.createElement('input');
      toggle.type = 'checkbox';
      toggle.id = 'tm-toggle';
      this.parentNode.insertBefore(toggle, this);
    }

    this.innerHTML = `
<nav class="tm-nav" id="tmNav">
  <div class="tm-inner">
    <div class="tm-formulas" style="position:absolute;inset:0;pointer-events:none;">
      <!-- Row 1: top zone (5%-30%) — safe from bottom menu -->
      <div class="tm-f" style="top:6%;  left:3%;  font-size:0.82rem; --dur:9s;  --delay:0s;   --drift:16s; --dx:10px; --dy:-5px">𝐹 = 𝑑𝐴 + 𝐴 ∧ 𝐴</div>
      <div class="tm-f" style="top:22%; left:8%;  font-size:0.75rem; --dur:11s; --delay:3s;   --drift:18s; --dx:-7px; --dy:6px">κ = ‖𝛾″(𝑠)‖</div>
      <div class="tm-f" style="top:10%; left:20%; font-size:0.78rem; --dur:10s; --delay:1.5s; --drift:14s; --dx:8px;  --dy:-8px">∀𝑥 ¬Bew(⌜𝜑⌝)</div>
      <div class="tm-f" style="top:28%; left:15%; font-size:0.72rem; --dur:12s; --delay:5s;   --drift:20s; --dx:-6px; --dy:4px">𝒲 = Tr𝒫 exp∮𝐴</div>
      <div class="tm-f" style="top:8%;  left:34%; font-size:0.8rem;  --dur:8s;  --delay:2s;   --drift:15s; --dx:9px;  --dy:-7px">𝐷ₕ = 𝑑 + [𝐴,·]</div>
      <div class="tm-f" style="top:25%; left:30%; font-size:0.76rem; --dur:13s; --delay:6.5s; --drift:17s; --dx:-8px; --dy:5px">𝔭 ⊩ ∃𝑓: ℵ₀ → 2ℵ₀</div>
      <div class="tm-f" style="top:12%; left:48%; font-size:0.84rem; --dur:10s; --delay:4s;   --drift:19s; --dx:7px;  --dy:-6px">Hol(∇) ⊆ 𝐺</div>
      <div class="tm-f" style="top:5%;  left:56%; font-size:0.72rem; --dur:9s;  --delay:0.5s; --drift:13s; --dx:-9px; --dy:7px">∇ₐ𝐹 = 0</div>
      <div class="tm-f" style="top:20%; left:52%; font-size:0.78rem; --dur:11s; --delay:7s;   --drift:16s; --dx:6px;  --dy:-4px">𝒵 = ∫𝑒⁻ˢ𝒟𝐴</div>
      <div class="tm-f" style="top:8%;  left:68%; font-size:0.8rem;  --dur:12s; --delay:2.5s; --drift:18s; --dx:-7px; --dy:8px">ℛμν − ½𝑔μν ℛ = 𝑇μν</div>
      <div class="tm-f" style="top:26%; left:65%; font-size:0.7rem;  --dur:8.5s;--delay:8s;   --drift:14s; --dx:10px; --dy:-5px">𝔼[∇𝐹] = 0</div>
      <div class="tm-f" style="top:14%; left:78%; font-size:0.76rem; --dur:10s; --delay:1s;   --drift:15s; --dx:-8px; --dy:6px">𝒲(𝒞) = Tr𝒫 exp∮꜀𝐴</div>
      <div class="tm-f" style="top:6%;  left:88%; font-size:0.74rem; --dur:13s; --delay:4.5s; --drift:20s; --dx:5px;  --dy:-7px">𝐹 = 𝑑𝐴+𝐴∧𝐴</div>
      <div class="tm-f" style="top:24%; left:82%; font-size:0.68rem; --dur:9.5s;--delay:9s;   --drift:17s; --dx:-6px; --dy:5px">Con(ZFC) → Con(ZFC+¬CH)</div>
      <!-- Row 2: mid zone (38%-55%) — still above menu line -->
      <div class="tm-f" style="top:40%; left:5%;  font-size:0.7rem;  --dur:11s; --delay:3.5s; --drift:16s; --dx:8px;  --dy:-4px">∫𝛿𝐹·𝐷𝑥 = 𝔼[∇𝐹]</div>
      <div class="tm-f" style="top:45%; left:25%; font-size:0.74rem; --dur:9s;  --delay:6s;   --drift:14s; --dx:-7px; --dy:6px">𝒟ₘ = 𝛿 + 𝛿* + 𝒯</div>
      <div class="tm-f" style="top:38%; left:42%; font-size:0.68rem; --dur:12s; --delay:1.8s; --drift:19s; --dx:9px;  --dy:-5px">𝔼[𝐹(𝑥+𝜀ℎ)]</div>
      <div class="tm-f" style="top:48%; left:58%; font-size:0.72rem; --dur:10s; --delay:7.5s; --drift:15s; --dx:-6px; --dy:7px">𝐷ₕ = 𝑑+[𝐴,·]</div>
      <div class="tm-f" style="top:42%; left:78%; font-size:0.76rem; --dur:8s;  --delay:5.5s; --drift:18s; --dx:7px;  --dy:-6px">∀𝑥 ¬Bew(⌜𝜑⌝) → 𝜑</div>
    </div>
  </div>
  <a href="https://www.terremathematiques.com/" class="tm-left-logo">
    <img src="logo.jpg" alt="Terre Mathématiques">
    <div class="tm-ltitle">
      <span>Terre</span>
      <span>Mathématiques</span>
    </div>
  </a>
  <div class="tm-menu">
    <a href="https://www.terremathematiques.com/">Accueil</a>
    <div class="tm-dd">
      <a href="#">Terre Mathématiques ▾</a>
      <div class="tm-dd-panel">
        <a href="philosophie.html">Ma philosophie</a>
        <a href="methode.html">Ma méthode</a>
      </div>
    </div>
    <div class="tm-dd">
      <a href="#">Formations ▾</a>
      <div class="tm-dd-panel">
        <a href="bac.html">BAC</a>
        <a href="https://www.terremathematiques.com/encours">Trading</a>
        <a href="https://www.terremathematiques.com/encours">IA</a>
        <a href="#">Voir toutes les formations →</a>
      </div>
    </div>
    <div class="tm-dd">
      <a href="#">Fiches Interactives ▾</a>
      <div class="tm-dd-panel">
        <a href="frenet-animation.html">Repère de Frenet</a>
        <a href="analyse-carte-interactive.html">Carte Interactive Analyse</a>
        <a href="chemin-craie-luxe.html">Chemin de Craie</a>
        <a href="decouvrir-courbe-gauss.html">Courbe de Gauss</a>
      </div>
    </div>
    <a href="qui-suis-je.html">Qui suis-je ?</a>
    <a href="#">Contact</a>
  </div>
  <label class="tm-hamburger" for="tm-toggle" aria-label="Menu">
    <span></span><span></span><span></span>
  </label>
  <div class="tm-drawer">
    <div class="tm-drawer-inner">
      <a href="https://www.terremathematiques.com/">Accueil</a>
      <div class="tm-drawer-section">Terre Mathématiques</div>
      <a class="tm-sub" href="philosophie.html">Ma philosophie</a>
      <a class="tm-sub" href="methode.html">Ma méthode</a>
      <div class="tm-drawer-section">Formations</div>
      <a class="tm-sub" href="bac.html">BAC</a>
      <a class="tm-sub" href="https://www.terremathematiques.com/encours">Trading</a>
      <a class="tm-sub" href="https://www.terremathematiques.com/encours">IA</a>
      <div class="tm-drawer-section">Fiches Interactives</div>
      <a class="tm-sub" href="frenet-animation.html">Repère de Frenet</a>
      <a class="tm-sub" href="analyse-carte-interactive.html">Carte Interactive Analyse</a>
      <a class="tm-sub" href="chemin-craie-luxe.html">Chemin de Craie</a>
      <a class="tm-sub" href="decouvrir-courbe-gauss.html">Courbe de Gauss</a>
      <a href="qui-suis-je.html">Qui suis-je</a>
      <a href="#">Contact</a>
    </div>
  </div>
</nav>`;

    // Gérer le toggle mobile via JS (remplace le CSS sibling selector)
    const toggle = document.getElementById('tm-toggle');
    const nav = this.querySelector('.tm-nav');
    if (toggle && nav) {
      toggle.addEventListener('change', () => {
        if (toggle.checked) {
          nav.classList.add('drawer-open');
        } else {
          nav.classList.remove('drawer-open');
        }
      });
    }

    // Marquer le lien actif automatiquement selon la page courante
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    this.querySelectorAll('.tm-menu > a, .tm-menu .tm-dd-panel a').forEach(link => {
      const href = link.getAttribute('href');
      if (href && href.includes(currentPage) && currentPage !== '') {
        link.classList.add('tm-active');
      }
    });
  }
}
customElements.define('tm-header', TmHeader);


/* ─────────────────────────────────────────────
   HEADER SIMPLE (pages légales)
───────────────────────────────────────────── */
class TmHeaderSimple extends HTMLElement {
  connectedCallback() {
    this.innerHTML = `
<nav class="navbar">
  <a href="https://www.terremathematiques.com/" class="navbar-logo">
    <div class="navbar-logo-placeholder">T</div>
    <div class="navbar-logo-text">
      Terre Mathématiques
      <span>Excellence &amp; Grandes Écoles</span>
    </div>
  </a>
  <ul class="navbar-links">
    <li><a href="https://www.terremathematiques.com/">Accueil</a></li>
    <li><a href="https://www.terremathematiques.com/philosophie">Ma philosophie</a></li>
    <li><a href="https://www.terremathematiques.com/methode">Ma méthode</a></li>
    <li><a href="https://www.terremathematiques.com/bac">Formations</a></li>
    <li><a href="https://www.terremathematiques.com/qui-suis-je">Qui suis-je ?</a></li>
  </ul>
  <a href="https://www.terremathematiques.com/#pricing" class="navbar-cta">Réserver un appel</a>
  <button class="mobile-toggle" aria-label="Menu">☰</button>
</nav>`;

    // Toggle mobile menu
    const btn = this.querySelector('.mobile-toggle');
    const links = this.querySelector('.navbar-links');
    if (btn && links) {
      btn.addEventListener('click', () => links.classList.toggle('show'));
    }
  }
}
customElements.define('tm-header-simple', TmHeaderSimple);