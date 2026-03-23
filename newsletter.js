/* ═══════════════════════════════════════════════════════════
   TERRE MATHÉMATIQUES — Web Component Newsletter
   Fichier : newsletter.js
   Usage :
     <script src="newsletter.js"></script>
     <tm-newsletter></tm-newsletter>
════════════════════════════════════════════════════════════ */


/* ─────────────────────────────────────────────
   CSS — injecté une seule fois dans <head>
───────────────────────────────────────────── */
(function injectNewsletterCSS() {
  if (document.getElementById('tm-newsletter-styles')) return;
  const style = document.createElement('style');
  style.id = 'tm-newsletter-styles';
  style.textContent = `
.tm-nl {
  background: var(--accent);
  padding: 80px 24px;
  text-align: center;
}
.tm-nl-inner {
  max-width: 560px;
  margin: 0 auto;
}
.tm-nl-eyebrow {
  display: inline-block;
  font-family: 'Outfit', sans-serif;
  font-size: 0.72rem;
  font-weight: 500;
  letter-spacing: 0.2em;
  text-transform: uppercase;
  color: rgba(var(--heading-rgb), 0.55);
  margin-bottom: 16px;
}
.tm-nl-title {
  font-family: 'Fraunces', serif;
  font-weight: 600;
  font-size: clamp(1.8rem, 4vw, 2.4rem);
  color: var(--heading);
  line-height: 1.2;
  margin-bottom: 12px;
}
.tm-nl-sub {
  font-family: 'Outfit', sans-serif;
  font-size: 1rem;
  color: rgba(var(--heading-rgb), 0.7);
  line-height: 1.6;
  margin-bottom: 36px;
}
.tm-nl-form {
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.tm-nl-fields {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
}
.tm-nl-fields input {
  flex: 1;
  min-width: 150px;
  padding: 14px 18px;
  border: 1px solid rgba(var(--heading-rgb), 0.25);
  border-radius: 8px;
  background: rgba(var(--heading-rgb), 0.1);
  color: var(--heading);
  font-family: 'Outfit', sans-serif;
  font-size: 0.95rem;
  outline: none;
  transition: border-color 0.2s, background 0.2s;
}
.tm-nl-fields input::placeholder {
  color: rgba(var(--heading-rgb), 0.45);
}
.tm-nl-fields input:focus {
  border-color: rgba(var(--heading-rgb), 0.6);
  background: rgba(var(--heading-rgb), 0.15);
}
.tm-nl-btn {
  width: 100%;
  padding: 15px 32px;
  background: var(--bg);
  color: var(--bg-light-alt);
  border: none;
  border-radius: 8px;
  font-family: 'Outfit', sans-serif;
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  letter-spacing: 0.03em;
  transition: opacity 0.2s, transform 0.2s;
}
.tm-nl-btn:hover {
  opacity: 0.92;
  transform: translateY(-1px);
}
.tm-nl-notice {
  font-family: 'Outfit', sans-serif;
  font-size: 0.72rem;
  color: rgba(var(--heading-rgb), 0.4);
  margin-top: 14px;
  line-height: 1.5;
}
@media (max-width: 480px) {
  .tm-nl-fields { flex-direction: column; }
  .tm-nl-fields input { min-width: unset; width: 100%; }
}
`;
  document.head.appendChild(style);
})();


/* ─────────────────────────────────────────────
   WEB COMPONENT <tm-newsletter>
───────────────────────────────────────────── */
class TmNewsletter extends HTMLElement {
  connectedCallback() {
    this.innerHTML = `
<section class="tm-nl section--light">
  <div class="tm-nl-inner">
    <span class="tm-nl-eyebrow">Newsletter</span>
    <h2 class="tm-nl-title">Reçois mes conseils maths</h2>
    <p class="tm-nl-sub">Méthodes, exercices et stratégies pour progresser — directement dans ta boîte mail.</p>

    <form method="post" action="https://systeme.io/embedded/38553227/subscription" class="tm-nl-form">
      <div class="tm-nl-fields">
        <input type="text"  name="surname" placeholder="Ton prénom"       required />
        <input type="email" name="email"   placeholder="Ton adresse email" required />
      </div>
      <button type="submit" class="tm-nl-btn">S'inscrire →</button>
    </form>

    <p class="tm-nl-notice">Pas de spam. Désinscription en un clic à tout moment.</p>
  </div>
</section>`;
  }
}
customElements.define('tm-newsletter', TmNewsletter);
