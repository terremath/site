/* avis.js — Carrousel de témoignages TerreMathématiques */
(function () {
  'use strict';

  const AVIS = [
    {
      nom: 'Lila',
      date: '11 sept. 2025',
      etoiles: 5,
      texte: 'Mon fils vient de commencer un suivi avec Obayda Julien et pour le moment tout se passe bien. La motivation est déjà au rendez-vous pour mon fils alors que ce n\u2019était pas gagné\u00a0! Il a déjà l\u2019impression d\u2019être plus à l\u2019aise avec certaines notions. La suite est donc bien prometteuse. Merci Professeur.'
    },
    {
      nom: 'Gregory',
      date: '10 sept. 2025',
      etoiles: 5,
      texte: 'Obayda enseigne à mes deux enfants avec une excellente pédagogie. Ses cours sont motivants, efficaces et très appréciés. Les progrès sont visibles. Je le recommande vivement\u00a0!'
    },
    {
      nom: 'Camy',
      date: '3 nov. 2025',
      etoiles: 5,
      texte: 'Excellent professeur, les cours sont très bien expliqués\u00a0, c\u2019est une véritable aide pour mon fils'
    },
    {
      nom: 'Myriam',
      date: '2 déc. 2025',
      etoiles: 5,
      texte: 'Obayda est un excellent professeur de mathématiques. Il est très pédagogue, patient et sait s\u2019adapter aux difficultés de chaque élève. Grâce à son accompagnement, mon fils a repris confiance en lui et a réellement progressé en mathématiques, là où d\u2019autres méthodes n\u2019avaient pas fonctionné. C\u2019est un enseignant sérieux, investi et à l\u2019écoute, que je recommande sans hésitation à tous les parents cherchant un professeur capable d\u2019aider efficacement leur enfant.'
    },
    {
      nom: 'AGATHE',
      date: '13 sept. 2025',
      etoiles: 5,
      texte: 'SUPER\u00a0!!!!!!!!!!!'
    },
    {
      nom: 'hanane',
      date: '5 déc. 2025',
      etoiles: 5,
      texte: 'Très bon prof, à l\u2019écoute d\u2019un ado de 17 ans qui passe son bac spécialité math cette année Patient et disponible. Top'
    },
    {
      nom: 'Emelle',
      date: '21 déc. 2025',
      etoiles: 5,
      texte: 'Mr Obayda est un très bon professeur. Il a permis à ma fille de se sentir plus à l\u2019aise en maths. Je vous le conseille.'
    },
    {
      nom: 'Ethan',
      date: '14 oct. 2025',
      etoiles: 5,
      texte: 'Obayda est un excellent tuteur avec une connaissance approfondie et des méthodes d\u2019enseignement exceptionnelles. Il est très professionnel et patient, et tous ses cours sont bien préparés. Hautement recommandé\u00a0!'
    },
    {
      nom: 'Nourdine',
      date: '15 oct. 2025',
      etoiles: 5,
      texte: 'Ma fille a récemment commencé les cours et elle reprend goût aux maths. Elle est enthousiaste à chaque fin de séance et retrouve peu à peu confiance. C\u2019est juste génial\u00a0!'
    },
    {
      nom: 'Paul',
      date: '2 nov. 2025',
      etoiles: 5,
      texte: "Ma fille a commencé à avoir des difficultés avec ses leçons de mathématiques à l'école et à prendre du retard. Elle a eu quelques leçons avec Obayda et comprend déjà plus qu'auparavant. Elle se sent très à l'aise avec lui et apprécie ses leçons, surtout lorsqu'elle vérifie ses devoirs avec lui. Nous recommandons définitivement Obayda en tant qu'enseignant."
    },
    {
      nom: 'Amine',
      date: '9 nov. 2025',
      etoiles: 5,
      texte: 'Obayda est un enseignant d\u2019exception. Il est à la fois le professeur de mon fils en classe de seconde et mon professeur dans un cours de géométrie différentielle. Sa maîtrise des sujets est impressionnante, il allie une compréhension profonde des concepts à une remarquable capacité à les rendre accessibles et intuitifs. Sa pédagogie se distingue par la clarté de ses explications et la rigueur de son approche. Il sait instaurer un climat agréable qui donne véritablement envie d\u2019apprendre. Ma recommandation est absolue.'
    },
    {
      nom: 'Basak',
      date: '2 oct. 2025',
      etoiles: 5,
      texte: 'Julien est génial\u00a0! Il enseigne à mon fils depuis quelques semaines maintenant. Il n\u2019est jamais en retard, ne annule jamais et est très patient\u00a0! Je le recommande vivement\u00a0!'
    },
    {
      nom: 'Dominique',
      date: '21 nov. 2025',
      etoiles: 5,
      texte: 'En deuxième année de prépa, il est difficile de trouver un tuteur en maths qui ait du temps, les connaissances nécessaires et de la pédagogie. Obayda Julien coche toutes les cases. Ma meilleure expérience sur ce site.'
    },
    {
      nom: 'Elaine',
      date: '24 nov. 2025',
      etoiles: 5,
      texte: "Excellent tuteur de mathématiques. Mon fils a beaucoup appris de lui et dit qu'il l'a aidé à maîtriser ses concepts de mathématiques avancés de 7e année."
    },
    {
      nom: 'Julie',
      date: '25 oct. 2025',
      etoiles: 5,
      texte: 'Obayda est un très bon prof, avec une super méthodologie. Il m\u2019aide à reprendre les bases en maths dans le cadre de ma formation d\u2019ingénieur. Les cours sont personnalisés, clairs et agréables. Grâce à ses exercices adaptés en devoirs maison, j\u2019ai vraiment l\u2019impression d\u2019avancer.'
    },
    {
      nom: 'jennifer',
      date: '18 nov. 2025',
      etoiles: 5,
      texte: 'Merci à Julien, mon fils a fait un grand pas grâce à son enseignement intéressant.'
    },
    {
      nom: 'Violetta',
      date: '8 nov. 2025',
      etoiles: 5,
      texte: 'Le professeur qui sera toujours derrière vous et vous aidera à comprendre les mathématiques plus facilement. J\u2019avais des difficultés avec mes mathématiques universitaires, mais il m\u2019aide à les surmonter.'
    },
    {
      nom: 'Mina',
      date: '16 janv. 2026',
      etoiles: 5,
      texte: 'Professeur très sérieux. Les cours en ligne sont clairs, bien structurés et adaptés au niveau de l\u2019élève. Ma fille a gagné en confiance en elle. Je recommande vivement.'
    },
    {
      nom: 'Arina',
      date: '5 févr. 2026',
      etoiles: 5,
      texte: 'Obayda est très sérieux, ponctuel, patient et positif. Les cours se déroulent dans une ambiance agréable. Je sens que je comprends mieux avec lui. Je recommande\u00a0!'
    },
    {
      nom: 'Aminata',
      date: '16 nov. 2025',
      etoiles: 5,
      texte: 'Les cours de Julien sont parfaitement adaptés à mon fils qui est en classe de 5e. Il maîtrise parfaitement les différents sujets et sait toujours expliquer les notions avec précision. Mon fils apprécie particulièrement sa manière de donner du sens aux concepts en les reliant à des situations de la vie quotidienne. Sa passion pour les mathématiques est évidente et il parvient à la transmettre, ce qui rend les séances captivantes. Il est sympathique, encourageant et toujours disponible pour répondre aux questions. Je recommande vivement ses cours\u00a0!'
    },
    {
      nom: 'Natalia',
      date: '7 déc. 2025',
      etoiles: 5,
      texte: 'Obayda explique les problèmes rapidement et clairement, montrant une compréhension approfondie de chaque sujet. Ses leçons sont efficaces, utiles et rendent le matériel difficile facile à comprendre. Hautement recommandé\u00a0!'
    },
    {
      nom: 'Fédora',
      date: '10 déc. 2025',
      etoiles: 5,
      texte: 'Très contente des cours avec Julien. Il s\u2019adapte à ton niveau et à ton rythme ses explications sont claires. Il est très ponctuel, fiable et ne reprogramme pas ses cours sans arrêt\u00a0( contrairement à certain sur cette plateforme). Je recommande vivement.'
    },
    {
      nom: 'Anne-Laure',
      date: '30 nov. 2025',
      etoiles: 5,
      texte: 'Obayda Julien m a aidée a comprendre mieux ma leçon\u00a0+ a m\u2019entrainer avec mes exercices'
    },
    {
      nom: 'Matija',
      date: '20 déc. 2025',
      etoiles: 5,
      texte: 'Julien est très compétent, pédagogue et à l\u2019écoute. Il s\u2019adapte parfaitement au niveau et aux besoins de l\u2019élève, en prenant le temps d\u2019expliquer de manière claire et structurée. Un professeur investi et bienveillant que je recommande sans hésiter.'
    },
    {
      nom: 'Lily',
      date: '2 févr. 2026',
      etoiles: 5,
      texte: 'Un excellent prof que je recommande, très à l\u00a0écoute, pédagogue et disponible. Ma fille apprécie ses cours et a déjà progressé.'
    },
    {
      nom: 'Chic Marbella',
      date: '28 déc. 2025',
      etoiles: 5,
      texte: 'très utile et bonne explication'
    },
    {
      nom: 'Lina',
      date: '22 janv. 2026',
      etoiles: 5,
      texte: 'Super'
    },
    {
      nom: 'Marie',
      date: '26 oct. 2025',
      etoiles: 5,
      texte: 'Excellent professeur\u00a0! Obayda prend le temps d\u2019expliquer et donne des explications très claires. Il m\u2019accompagne pour la préparation du Tage Mage depuis plusieurs semaines, et il m\u2019aide à faire de vrais progrès. Je recommande\u00a0!'
    },
    {
      nom: 'Daniel',
      date: '26 oct. 2025',
      etoiles: 5,
      texte: 'Tout simplement génial'
    },
    {
      nom: 'Moses',
      date: '22 août 2025',
      etoiles: 5,
      texte: 'Obayda m\u2019aide avec la théorie des probabilités. C\u2019est un tuteur très compétent.'
    },
    {
      nom: 'Jade',
      date: '1 oct. 2025',
      etoiles: 5,
      texte: 'Très utile, je recommande.'
    },
    {
      nom: 'Ahmad',
      date: '16 oct. 2025',
      etoiles: 5,
      texte: 'J\u2019ai eu une expérience incroyable en apprenant les mathématiques avec Obayda. Il a expliqué en 30 minutes ce que mon professeur d\u2019université n\u2019a pas pu expliquer en deux semaines. Ses leçons sont claires, ciblées et faciles à suivre. Il est patient, soutenant et rend même les sujets difficiles simples à comprendre. Je le recommande vivement à quiconque souhaite progresser de manière professionnelle et efficace en mathématiques.'
    },
    {
      nom: 'Lohane',
      date: '2 janv. 2026',
      etoiles: 5,
      texte: 'Très bien\u00a0!'
    },
    {
      nom: 'Jessica',
      date: '12 oct. 2025',
      etoiles: 5,
      texte: 'Obayda est un enseignant exceptionnel avec une connaissance approfondie et une manière d\u2019expliquer très claire. Il m\u2019a aidé avec des sujets complexes de mon programme de master, et il n\u2019y avait rien qu\u2019il ne pouvait expliquer\u00a0! Il remarquait toujours les domaines dans lesquels je devais m\u2019améliorer et donnait des retours utiles à chaque cours. Il se soucie vraiment du progrès de ses étudiants.'
    },
    {
      nom: 'Alice',
      date: '23 nov. 2025',
      etoiles: 5,
      texte: 'Classe incroyable\u00a0! Très claire et intéressante\u00a0! Merci beaucoup pour votre aide en mathématiques niveau master\u00a0!'
    },
    {
      nom: 'Laurence',
      date: '25 nov. 2025',
      etoiles: 5,
      texte: 'Julien est bienveillant, consciencieux et professionnel. Mon fils apprécie les cours donnés et les conseils apportés.'
    },
    {
      nom: 'Meyssa',
      date: '27 août 2025',
      etoiles: 5,
      texte: 'Il a le don d\u2019enseigner, il est très pédagogue et ses cours sont structurés. Je recommande grandement Mr Obayda.'
    },
    {
      nom: 'Mohammed Yassine',
      date: '20 déc. 2025',
      etoiles: 5,
      texte: 'Super Prof, à l\u2019écoute, pédagogique et ponctuel. Il a su détecter les points faibles de mon fils en Tle spé maths pour travailler dessus.'
    },
    {
      nom: 'Josh',
      date: '23 janv. 2026',
      etoiles: 5,
      texte: 'Cours bien structuré, il prête une attention particulière aux besoins des étudiants et se concentre sur les points faibles de vos connaissances. Super gars, j\u2019ai vraiment apprécié travailler avec lui.'
    }
  ];

  /* ── Styles ─────────────────────────────────────────────────── */
  const styleEl = document.createElement('style');
  styleEl.textContent = `
    .avis-scroll-wrap {
      position: relative;
      margin-top: 56px;
      overflow: hidden;
      cursor: grab;
      user-select: none;
      -webkit-user-select: none;
      -webkit-mask-image: linear-gradient(
        to right, transparent 0%, black 7%, black 93%, transparent 100%
      );
      mask-image: linear-gradient(
        to right, transparent 0%, black 7%, black 93%, transparent 100%
      );
    }
    .avis-scroll-wrap.dragging { cursor: grabbing; }

    .avis-track {
      display: flex;
      gap: 28px;
      width: max-content;
      padding: 8px 0 24px;
      will-change: transform;
    }

    .avis-card {
      width: 340px;
      flex-shrink: 0;
      padding: 30px 28px 24px;
      background: var(--white);
      border: 1px solid var(--sand-dark);
      border-radius: 14px;
      display: flex;
      flex-direction: column;
      transition: border-color 0.3s ease;
    }
    .avis-card:hover { border-color: rgba(var(--green-rgb), 0.3); }

    .avis-stars {
      color: var(--green);
      font-size: 1rem;
      letter-spacing: 3px;
      margin-bottom: 14px;
    }

    .avis-texte {
      font-size: 1rem;
      color: var(--text);
      line-height: 1.75;
      font-style: italic;
      font-family: 'Fraunces', serif;
      margin-bottom: 8px;
      display: -webkit-box;
      -webkit-line-clamp: 4;
      -webkit-box-orient: vertical;
      overflow: hidden;
    }

    /* "Voir plus" caché par défaut, affiché seulement si tronqué */
    .avis-voir-plus {
      display: none;
      background: none;
      border: none;
      color: var(--green-light);
      font-size: 0.82rem;
      font-family: 'Outfit', sans-serif;
      font-weight: 500;
      cursor: pointer;
      padding: 0;
      margin-bottom: 14px;
      text-align: left;
      text-decoration: underline;
      text-underline-offset: 3px;
      transition: color 0.2s;
    }
    .avis-voir-plus.show { display: inline; }
    .avis-voir-plus:hover { color: var(--green); }

    .avis-footer {
      display: flex;
      align-items: baseline;
      justify-content: space-between;
      gap: 8px;
      padding-top: 14px;
      border-top: 1px solid var(--sand-dark);
      margin-top: auto;
    }

    .avis-nom {
      font-size: 0.9rem;
      font-weight: 600;
      color: var(--green);
      font-family: 'Outfit', sans-serif;
    }

    .avis-date {
      font-size: 0.78rem;
      color: var(--text-muted);
      font-family: 'Outfit', sans-serif;
      white-space: nowrap;
    }

    .avis-badge {
      position: absolute;
      top: 50%;
      left: 50%;
      transform: translate(-50%, -50%);
      background: rgba(var(--ink-rgb), 0.82);
      color: var(--white);
      font-family: 'Outfit', sans-serif;
      font-size: 0.85rem;
      font-weight: 500;
      padding: 10px 24px;
      border-radius: 100px;
      pointer-events: none;
      opacity: 0;
      transition: opacity 0.25s ease;
      white-space: nowrap;
      backdrop-filter: blur(6px);
      -webkit-backdrop-filter: blur(6px);
      z-index: 2;
    }
    .avis-badge.visible { opacity: 1; }

    /* ── Modal ── */
    .avis-modal-overlay {
      position: fixed;
      inset: 0;
      background: rgba(var(--ink-rgb), 0.5);
      display: flex;
      align-items: center;
      justify-content: center;
      z-index: 1000;
      padding: 24px;
      backdrop-filter: blur(4px);
      -webkit-backdrop-filter: blur(4px);
      opacity: 0;
      transition: opacity 0.2s ease;
      pointer-events: none;
    }
    .avis-modal-overlay.open { opacity: 1; pointer-events: all; }

    .avis-modal {
      background: var(--white);
      border-radius: 16px;
      padding: 44px 40px 36px;
      max-width: 560px;
      width: 100%;
      max-height: 85vh;
      overflow-y: auto;
      position: relative;
      transform: translateY(12px);
      transition: transform 0.2s ease;
    }
    .avis-modal-overlay.open .avis-modal { transform: translateY(0); }

    .avis-modal-close {
      position: absolute;
      top: 14px;
      right: 16px;
      background: none;
      border: none;
      font-size: 1.3rem;
      line-height: 1;
      cursor: pointer;
      color: var(--text-muted);
      padding: 4px 8px;
      border-radius: 6px;
      transition: color 0.2s, background 0.2s;
    }
    .avis-modal-close:hover { color: var(--ink); background: var(--sand-dark); }

    .avis-modal-stars {
      color: var(--green);
      font-size: 1.05rem;
      letter-spacing: 3px;
      margin-bottom: 18px;
    }

    .avis-modal-texte {
      font-size: 1.05rem;
      color: var(--text);
      line-height: 1.8;
      font-style: italic;
      font-family: 'Fraunces', serif;
      margin-bottom: 24px;
    }

    .avis-modal-footer {
      display: flex;
      align-items: baseline;
      gap: 10px;
      padding-top: 18px;
      border-top: 1px solid var(--sand-dark);
    }

    .avis-modal-nom {
      font-size: 0.95rem;
      font-weight: 600;
      color: var(--green);
      font-family: 'Outfit', sans-serif;
    }

    .avis-modal-date {
      font-size: 0.82rem;
      color: var(--text-muted);
      font-family: 'Outfit', sans-serif;
    }
  `;
  document.head.appendChild(styleEl);

  /* ── DOM ────────────────────────────────────────────────────── */
  const container = document.getElementById('avis-container');
  if (!container) return;

  const wrap = document.createElement('div');
  wrap.className = 'avis-scroll-wrap';

  const track = document.createElement('div');
  track.className = 'avis-track';

  const badge = document.createElement('div');
  badge.className = 'avis-badge';

  const overlay = document.createElement('div');
  overlay.className = 'avis-modal-overlay';
  overlay.innerHTML = `
    <div class="avis-modal">
      <button class="avis-modal-close" aria-label="Fermer">&#x2715;</button>
      <div class="avis-modal-stars"></div>
      <p class="avis-modal-texte"></p>
      <div class="avis-modal-footer">
        <span class="avis-modal-nom"></span>
        <span class="avis-modal-date"></span>
      </div>
    </div>
  `;
  document.body.appendChild(overlay);

  /* ── État ───────────────────────────────────────────────────── */
  let x = 0;
  let halfWidth = 0;
  const SPEED = 0.5;           // px / frame (~30 px/s à 60fps)
  let paused = false;
  let pausedBeforeModal = false;
  let badgeTimer;
  let isDragging = false;
  let didDrag = false;
  let dragStartX = 0;
  let dragStartScrollX = 0;
  let isWheeling = false;
  let wheelTimer;

  /* ── Pause / reprise ────────────────────────────────────────── */
  function setPaused(val, showBadge) {
    paused = val;
    if (!showBadge) return;
    clearTimeout(badgeTimer);
    if (paused) {
      badge.textContent = '⏸ En pause · cliquer pour reprendre';
      badge.classList.add('visible');
    } else {
      badge.textContent = '▶ Reprise';
      badge.classList.add('visible');
      badgeTimer = setTimeout(() => badge.classList.remove('visible'), 1000);
    }
  }

  /* ── Modal ──────────────────────────────────────────────────── */
  function openModal(a) {
    pausedBeforeModal = paused;
    setPaused(true, false);
    badge.classList.remove('visible');
    overlay.querySelector('.avis-modal-stars').textContent = '★ '.repeat(a.etoiles).trim();
    overlay.querySelector('.avis-modal-texte').textContent = '« ' + a.texte + ' »';
    overlay.querySelector('.avis-modal-nom').textContent = a.nom;
    overlay.querySelector('.avis-modal-date').textContent = a.date;
    overlay.classList.add('open');
  }

  function closeModal() {
    overlay.classList.remove('open');
    if (!pausedBeforeModal) setPaused(false, false);
  }

  overlay.querySelector('.avis-modal-close').addEventListener('click', closeModal);
  overlay.addEventListener('click', e => { if (e.target === overlay) closeModal(); });
  document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModal(); });

  /* ── Créer une carte ────────────────────────────────────────── */
  const cardRefs = [];

  function makeCard(a) {
    const el = document.createElement('div');
    el.className = 'avis-card';

    const stars = document.createElement('div');
    stars.className = 'avis-stars';
    stars.textContent = '★ '.repeat(a.etoiles).trim();

    const texte = document.createElement('p');
    texte.className = 'avis-texte';
    texte.textContent = '« ' + a.texte + ' »';

    const btnVoir = document.createElement('button');
    btnVoir.className = 'avis-voir-plus';
    btnVoir.textContent = 'Voir plus →';
    btnVoir.addEventListener('click', e => {
      e.stopPropagation();
      openModal(a);
    });

    const footer = document.createElement('div');
    footer.className = 'avis-footer';
    footer.innerHTML =
      `<span class="avis-nom">${a.nom}</span>` +
      `<span class="avis-date">${a.date}</span>`;

    el.appendChild(stars);
    el.appendChild(texte);
    el.appendChild(btnVoir);
    el.appendChild(footer);

    cardRefs.push({ texte, btnVoir });
    return el;
  }

  [...AVIS, ...AVIS].forEach(a => track.appendChild(makeCard(a)));

  wrap.appendChild(track);
  wrap.appendChild(badge);
  container.appendChild(wrap);

  /* Mesure après insertion dans le DOM */
  halfWidth = track.scrollWidth / 2;

  /* Afficher "Voir plus" uniquement sur les cartes réellement tronquées */
  cardRefs.forEach(({ texte, btnVoir }) => {
    if (texte.scrollHeight > texte.clientHeight) {
      btnVoir.classList.add('show');
    }
  });

  /* ── Boucle d'animation RAF ─────────────────────────────────── */
  function normalizeX() {
    while (x > 0)          x -= halfWidth;
    while (x <= -halfWidth) x += halfWidth;
  }

  (function tick() {
    if (!paused && !isDragging && !isWheeling) {
      x -= SPEED;
      if (x <= -halfWidth) x += halfWidth;
    }
    track.style.transform = `translateX(${x}px)`;
    requestAnimationFrame(tick);
  })();

  /* ── Trackpad (molette horizontale) ────────────────────────── */
  wrap.addEventListener('wheel', e => {
    // Intercepter uniquement le glissement horizontal
    if (Math.abs(e.deltaX) <= Math.abs(e.deltaY)) return;
    e.preventDefault();
    x -= e.deltaX;
    normalizeX();
    isWheeling = true;
    clearTimeout(wheelTimer);
    wheelTimer = setTimeout(() => { isWheeling = false; }, 400);
  }, { passive: false });

  /* ── Drag souris ────────────────────────────────────────────── */
  wrap.addEventListener('mousedown', e => {
    if (e.button !== 0) return;
    isDragging = true;
    didDrag = false;
    dragStartX = e.clientX;
    dragStartScrollX = x;
    wrap.classList.add('dragging');
  });

  document.addEventListener('mousemove', e => {
    if (!isDragging) return;
    const delta = e.clientX - dragStartX;
    if (Math.abs(delta) > 4) didDrag = true;
    x = dragStartScrollX + delta;
    normalizeX();
  });

  document.addEventListener('mouseup', () => {
    if (!isDragging) return;
    isDragging = false;
    wrap.classList.remove('dragging');
  });

  /* ── Drag tactile ───────────────────────────────────────────── */
  wrap.addEventListener('touchstart', e => {
    isDragging = true;
    didDrag = false;
    dragStartX = e.touches[0].clientX;
    dragStartScrollX = x;
  }, { passive: true });

  document.addEventListener('touchmove', e => {
    if (!isDragging) return;
    const delta = e.touches[0].clientX - dragStartX;
    if (Math.abs(delta) > 4) didDrag = true;
    x = dragStartScrollX + delta;
    normalizeX();
  }, { passive: true });

  document.addEventListener('touchend', () => { isDragging = false; });

  /* ── Clic = pause/reprise (ignoré après un drag) ────────────── */
  wrap.addEventListener('click', () => {
    if (didDrag) return;
    setPaused(!paused, true);
  });
})();
