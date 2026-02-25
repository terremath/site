/**
 * ═══════════════════════════════════════════════════════════
 *  TERRE MATHÉMATIQUES — Bandeau Cookies (Conforme CNIL)
 * ═══════════════════════════════════════════════════════════
 * 
 *  INSTALLATION :
 *  1. Placez ce fichier (cookie-consent.js) à la racine de votre site
 *  2. Ajoutez cette ligne AVANT </body> sur TOUTES vos pages :
 *     <script src="cookie-consent.js"></script>
 * 
 *  3. IMPORTANT : Supprimez votre balise Google Analytics existante
 *     (celle qui commence par <!-- Google tag (gtag.js) --> ou <script async src="https://www.googletagmanager.com/gtag/js...)
 *     Ce script chargera Analytics automatiquement SI l'utilisateur accepte.
 * 
 *  4. Remplacez l'ID ci-dessous par votre vrai ID Google Analytics :
 */

const COOKIE_CONFIG = {
  // ⬇️ REMPLACEZ PAR VOTRE ID GOOGLE ANALYTICS (ex: "G-V6CFTZP0ME")
  googleAnalyticsId: "G-V6CFTZP0ME",
  
  // Durée de mémorisation du choix (en jours) — CNIL recommande 6 mois max
  consentDuration: 182,
  
  // Nom du cookie de consentement
  cookieName: "tm_cookie_consent",
};

// ═══════════════════════════════════════════════════════════
//  NE RIEN MODIFIER EN DESSOUS (sauf si vous savez ce que vous faites)
// ═══════════════════════════════════════════════════════════

(function () {
  "use strict";

  // ─── STYLES ───
  const styles = document.createElement("style");
  styles.textContent = `
    /* ═══ Cookie Banner ═══ */
    .tm-cookie-overlay {
      position: fixed;
      inset: 0;
      background: rgba(0, 0, 0, 0.5);
      backdrop-filter: blur(4px);
      -webkit-backdrop-filter: blur(4px);
      z-index: 99998;
      opacity: 0;
      transition: opacity 0.4s ease;
    }

    .tm-cookie-overlay.visible {
      opacity: 1;
    }

    .tm-cookie-banner {
      position: fixed;
      bottom: 0;
      left: 0;
      right: 0;
      z-index: 99999;
      background: #111118;
      border-top: 1px solid rgba(255, 255, 255, 0.08);
      box-shadow: 0 -8px 40px rgba(0, 0, 0, 0.5);
      padding: 0;
      transform: translateY(100%);
      transition: transform 0.5s cubic-bezier(0.16, 1, 0.3, 1);
      font-family: 'DM Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    }

    .tm-cookie-banner.visible {
      transform: translateY(0);
    }

    .tm-cookie-inner {
      max-width: 1100px;
      margin: 0 auto;
      padding: 1.5rem 2rem;
      display: flex;
      align-items: center;
      gap: 2rem;
      flex-wrap: wrap;
    }

    .tm-cookie-icon {
      flex-shrink: 0;
      width: 44px;
      height: 44px;
      background: rgba(201, 162, 39, 0.12);
      border: 1px solid rgba(201, 162, 39, 0.2);
      border-radius: 12px;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 22px;
    }

    .tm-cookie-text {
      flex: 1;
      min-width: 280px;
    }

    .tm-cookie-text h3 {
      font-family: 'Playfair Display', Georgia, serif;
      font-size: 1.05rem;
      font-weight: 700;
      color: #e8e6e3;
      margin: 0 0 0.3rem 0;
    }

    .tm-cookie-text p {
      font-size: 0.85rem;
      color: #9a9a9a;
      line-height: 1.6;
      margin: 0;
    }

    .tm-cookie-text a {
      color: #c9a227;
      text-decoration: none;
      border-bottom: 1px solid rgba(201, 162, 39, 0.3);
      transition: border-color 0.3s;
    }

    .tm-cookie-text a:hover {
      border-bottom-color: #c9a227;
    }

    .tm-cookie-actions {
      display: flex;
      gap: 0.75rem;
      flex-shrink: 0;
      flex-wrap: wrap;
    }

    .tm-cookie-btn {
      padding: 0.65rem 1.4rem;
      border-radius: 8px;
      font-size: 0.88rem;
      font-weight: 600;
      font-family: inherit;
      cursor: pointer;
      transition: all 0.3s ease;
      border: none;
      white-space: nowrap;
    }

    /* CNIL : le bouton refuser doit être aussi visible que accepter */
    .tm-cookie-btn-refuse {
      background: rgba(255, 255, 255, 0.06);
      border: 1px solid rgba(255, 255, 255, 0.12);
      color: #e8e6e3;
    }

    .tm-cookie-btn-refuse:hover {
      background: rgba(255, 255, 255, 0.1);
      border-color: rgba(255, 255, 255, 0.2);
    }

    .tm-cookie-btn-accept {
      background: #c9a227;
      color: #0a0a0f;
    }

    .tm-cookie-btn-accept:hover {
      background: #d4ad2e;
      transform: translateY(-1px);
      box-shadow: 0 4px 20px rgba(201, 162, 39, 0.25);
    }

    .tm-cookie-btn-customize {
      background: transparent;
      color: #9a9a9a;
      font-size: 0.8rem;
      padding: 0.5rem 0.8rem;
      font-weight: 500;
    }

    .tm-cookie-btn-customize:hover {
      color: #e8e6e3;
    }

    /* ═══ Panneau de personnalisation ═══ */
    .tm-cookie-panel {
      display: none;
      margin-top: 1rem;
      padding-top: 1rem;
      border-top: 1px solid rgba(255, 255, 255, 0.06);
      width: 100%;
    }

    .tm-cookie-panel.open {
      display: block;
      animation: tmSlideDown 0.3s ease;
    }

    @keyframes tmSlideDown {
      from { opacity: 0; transform: translateY(-10px); }
      to { opacity: 1; transform: translateY(0); }
    }

    .tm-cookie-category {
      display: flex;
      align-items: center;
      justify-content: space-between;
      padding: 0.8rem 1rem;
      margin-bottom: 0.5rem;
      background: rgba(255, 255, 255, 0.03);
      border: 1px solid rgba(255, 255, 255, 0.05);
      border-radius: 10px;
    }

    .tm-cookie-category-info h4 {
      font-size: 0.9rem;
      color: #e8e6e3;
      margin: 0 0 0.15rem;
      font-weight: 600;
    }

    .tm-cookie-category-info p {
      font-size: 0.78rem;
      color: #6a6a6a;
      margin: 0;
      line-height: 1.4;
    }

    /* Toggle switch */
    .tm-toggle {
      position: relative;
      width: 44px;
      height: 24px;
      flex-shrink: 0;
    }

    .tm-toggle input {
      opacity: 0;
      width: 0;
      height: 0;
    }

    .tm-toggle-slider {
      position: absolute;
      inset: 0;
      background: rgba(255, 255, 255, 0.1);
      border-radius: 24px;
      cursor: pointer;
      transition: background 0.3s;
    }

    .tm-toggle-slider::before {
      content: '';
      position: absolute;
      width: 18px;
      height: 18px;
      left: 3px;
      bottom: 3px;
      background: #9a9a9a;
      border-radius: 50%;
      transition: all 0.3s;
    }

    .tm-toggle input:checked + .tm-toggle-slider {
      background: rgba(201, 162, 39, 0.3);
    }

    .tm-toggle input:checked + .tm-toggle-slider::before {
      transform: translateX(20px);
      background: #c9a227;
    }

    .tm-toggle input:disabled + .tm-toggle-slider {
      opacity: 0.5;
      cursor: not-allowed;
    }

    .tm-toggle input:disabled + .tm-toggle-slider::before {
      background: #c9a227;
    }

    .tm-cookie-panel-actions {
      display: flex;
      justify-content: flex-end;
      gap: 0.75rem;
      margin-top: 1rem;
    }

    /* ═══ Petit bouton "Gérer les cookies" (toujours visible) ═══ */
    .tm-cookie-reopen {
      position: fixed;
      bottom: 1rem;
      left: 1rem;
      z-index: 99990;
      background: #111118;
      border: 1px solid rgba(255, 255, 255, 0.08);
      color: #9a9a9a;
      padding: 0.5rem 0.9rem;
      border-radius: 8px;
      font-size: 0.78rem;
      font-family: 'DM Sans', -apple-system, sans-serif;
      cursor: pointer;
      transition: all 0.3s;
      display: none;
      align-items: center;
      gap: 0.4rem;
      box-shadow: 0 2px 12px rgba(0, 0, 0, 0.3);
    }

    .tm-cookie-reopen:hover {
      color: #c9a227;
      border-color: rgba(201, 162, 39, 0.3);
    }

    .tm-cookie-reopen.visible {
      display: flex;
    }

    /* ═══ Responsive ═══ */
    @media (max-width: 768px) {
      .tm-cookie-inner {
        padding: 1.2rem 1rem;
        gap: 1rem;
      }

      .tm-cookie-icon { display: none; }

      .tm-cookie-actions {
        width: 100%;
      }

      .tm-cookie-btn-refuse,
      .tm-cookie-btn-accept {
        flex: 1;
      }

      .tm-cookie-btn-customize {
        width: 100%;
        text-align: center;
      }
    }
  `;
  document.head.appendChild(styles);

  // ─── COOKIE HELPERS ───
  function setCookie(name, value, days) {
    const d = new Date();
    d.setTime(d.getTime() + days * 86400000);
    document.cookie = name + "=" + value + ";expires=" + d.toUTCString() + ";path=/;SameSite=Lax";
  }

  function getCookie(name) {
    const v = document.cookie.match("(^|;)\\s*" + name + "\\s*=\\s*([^;]+)");
    return v ? v.pop() : null;
  }

  function deleteCookiesStartingWith(prefix) {
    document.cookie.split(";").forEach(function (c) {
      const name = c.split("=")[0].trim();
      if (name.startsWith(prefix)) {
        document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT;path=/";
      }
    });
  }

  // ─── GOOGLE ANALYTICS ───
  function loadGoogleAnalytics() {
    if (document.getElementById("tm-ga-script")) return;
    const s = document.createElement("script");
    s.id = "tm-ga-script";
    s.async = true;
    s.src = "https://www.googletagmanager.com/gtag/js?id=" + COOKIE_CONFIG.googleAnalyticsId;
    document.head.appendChild(s);

    window.dataLayer = window.dataLayer || [];
    function gtag() { window.dataLayer.push(arguments); }
    window.gtag = gtag;
    gtag("js", new Date());
    gtag("config", COOKIE_CONFIG.googleAnalyticsId, { anonymize_ip: true });
  }

  function removeGoogleAnalytics() {
    const s = document.getElementById("tm-ga-script");
    if (s) s.remove();
    deleteCookiesStartingWith("_ga");
    deleteCookiesStartingWith("_gid");
    deleteCookiesStartingWith("_gat");
  }

  // ─── CONSENT LOGIC ───
  function getConsent() {
    const raw = getCookie(COOKIE_CONFIG.cookieName);
    if (!raw) return null;
    try { return JSON.parse(decodeURIComponent(raw)); } catch (e) { return null; }
  }

  function saveConsent(analytics) {
    const consent = { analytics: analytics, date: new Date().toISOString() };
    setCookie(COOKIE_CONFIG.cookieName, encodeURIComponent(JSON.stringify(consent)), COOKIE_CONFIG.consentDuration);
    applyConsent(consent);
  }

  function applyConsent(consent) {
    if (consent && consent.analytics) {
      loadGoogleAnalytics();
    } else {
      removeGoogleAnalytics();
    }
  }

  // ─── BUILD BANNER ───
  function createBanner() {
    // Overlay
    const overlay = document.createElement("div");
    overlay.className = "tm-cookie-overlay";
    overlay.id = "tm-cookie-overlay";

    // Banner
    const banner = document.createElement("div");
    banner.className = "tm-cookie-banner";
    banner.id = "tm-cookie-banner";
    banner.setAttribute("role", "dialog");
    banner.setAttribute("aria-label", "Gestion des cookies");

    banner.innerHTML = `
      <div class="tm-cookie-inner">
        <div class="tm-cookie-icon">🍪</div>
        <div class="tm-cookie-text">
          <h3>Votre vie privée compte</h3>
          <p>Nous utilisons des cookies pour analyser le trafic de notre site (Google Analytics). 
          Aucun cookie publicitaire n'est utilisé. Vous pouvez accepter, refuser ou personnaliser vos choix. 
          <a href="/politique-cookies.html">En savoir plus</a></p>
        </div>
        <div class="tm-cookie-actions">
          <button class="tm-cookie-btn tm-cookie-btn-refuse" id="tm-refuse">Tout refuser</button>
          <button class="tm-cookie-btn tm-cookie-btn-accept" id="tm-accept">Tout accepter</button>
          <button class="tm-cookie-btn tm-cookie-btn-customize" id="tm-customize">Personnaliser</button>
        </div>

        <!-- Panneau de personnalisation (caché par défaut) -->
        <div class="tm-cookie-panel" id="tm-panel">
          <div class="tm-cookie-category">
            <div class="tm-cookie-category-info">
              <h4>🔒 Cookies essentiels</h4>
              <p>Nécessaires au fonctionnement du site. Toujours actifs.</p>
            </div>
            <label class="tm-toggle">
              <input type="checkbox" checked disabled>
              <span class="tm-toggle-slider"></span>
            </label>
          </div>

          <div class="tm-cookie-category">
            <div class="tm-cookie-category-info">
              <h4>📊 Cookies analytiques</h4>
              <p>Google Analytics — Mesure d'audience avec IP anonymisée.</p>
            </div>
            <label class="tm-toggle">
              <input type="checkbox" id="tm-toggle-analytics">
              <span class="tm-toggle-slider"></span>
            </label>
          </div>

          <div class="tm-cookie-panel-actions">
            <button class="tm-cookie-btn tm-cookie-btn-refuse" id="tm-panel-refuse">Tout refuser</button>
            <button class="tm-cookie-btn tm-cookie-btn-accept" id="tm-panel-save">Enregistrer mes choix</button>
          </div>
        </div>
      </div>
    `;

    document.body.appendChild(overlay);
    document.body.appendChild(banner);

    // Reopen button (petit bouton persistant)
    const reopen = document.createElement("button");
    reopen.className = "tm-cookie-reopen";
    reopen.id = "tm-cookie-reopen";
    reopen.innerHTML = "🍪 Gérer les cookies";
    reopen.setAttribute("aria-label", "Gérer les cookies");
    document.body.appendChild(reopen);

    // ─── EVENTS ───
    const show = function () {
      banner.classList.add("visible");
      overlay.classList.add("visible");
      reopen.classList.remove("visible");
    };

    const hide = function () {
      banner.classList.remove("visible");
      overlay.classList.remove("visible");
      reopen.classList.add("visible");
    };

    // Accept all
    document.getElementById("tm-accept").addEventListener("click", function () {
      saveConsent(true);
      hide();
    });

    // Refuse all
    document.getElementById("tm-refuse").addEventListener("click", function () {
      saveConsent(false);
      hide();
    });

    // Customize toggle
    document.getElementById("tm-customize").addEventListener("click", function () {
      document.getElementById("tm-panel").classList.toggle("open");
    });

    // Panel: refuse all
    document.getElementById("tm-panel-refuse").addEventListener("click", function () {
      saveConsent(false);
      hide();
    });

    // Panel: save choices
    document.getElementById("tm-panel-save").addEventListener("click", function () {
      var analytics = document.getElementById("tm-toggle-analytics").checked;
      saveConsent(analytics);
      hide();
    });

    // Reopen
    reopen.addEventListener("click", function () {
      // Pre-fill toggle with current consent
      var consent = getConsent();
      if (consent) {
        document.getElementById("tm-toggle-analytics").checked = consent.analytics;
      }
      document.getElementById("tm-panel").classList.remove("open");
      show();
    });

    return { show: show, hide: hide };
  }

  // ─── INIT ───
  function init() {
    var consent = getConsent();
    var banner = createBanner();

    if (consent === null) {
      // Première visite : afficher le bandeau
      // Petit délai pour l'animation d'entrée
      setTimeout(function () { banner.show(); }, 500);
    } else {
      // Choix déjà fait : appliquer et montrer le bouton "Gérer"
      applyConsent(consent);
      document.getElementById("tm-cookie-reopen").classList.add("visible");
    }
  }

  // Lancer quand le DOM est prêt
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
