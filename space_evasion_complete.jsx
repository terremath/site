import React, { useState, useEffect, useRef, useCallback } from 'react';

const SpaceEvasionComplete = () => {
  const canvasRef = useRef(null);
  const [currentPart, setCurrentPart] = useState(0);
  const [currentScene, setCurrentScene] = useState(0);
  const [isPlaying, setIsPlaying] = useState(false);
  const [sceneTime, setSceneTime] = useState(0);
  const [playbackSpeed, setPlaybackSpeed] = useState(1);
  const animationRef = useRef(null);
  const stateRef = useRef({});

  const FPS = 30;

  // ============================================================
  // STRUCTURE COMPLÈTE DE LA VIDÉO
  // ============================================================
  const videoStructure = [
    // ========== PARTIE 0 : LE PROBLÈME ==========
    {
      part: 0,
      title: "Le problème",
      scenes: [
        {
          id: "0.1",
          duration: 30,
          subtitles: [
            { start: 0, end: 8, text: "Un vaisseau doit traverser cette zone." },
            { start: 8, end: 16, text: "Il y a des astéroïdes — des obstacles fixes." },
            { start: 16, end: 24, text: "Et des missiles — des menaces mobiles." },
            { start: 24, end: 30, text: "Le carburant est limité. Comment traverser en dépensant le moins possible ?" }
          ],
          setup: 'intro_problem'
        }
      ]
    },
    // ========== PARTIE 1 : LES ZONES INTERDITES ==========
    {
      part: 1,
      title: "Les zones interdites",
      scenes: [
        {
          id: "1.1",
          duration: 25,
          subtitles: [
            { start: 0, end: 8, text: "Autour de chaque astéroïde, on définit une zone interdite." },
            { start: 8, end: 16, text: "Une bulle dans laquelle le vaisseau ne doit pas entrer." },
            { start: 16, end: 25, text: "Pourquoi ? Trop près, c'est la collision. On prend une marge de sécurité." }
          ],
          equation: { text: "‖r − r_ast‖ ≥ R + d_séc", label: "Contrainte d'évitement", appearAt: 8 },
          setup: 'bubble_asteroid'
        },
        {
          id: "1.2",
          duration: 22,
          subtitles: [
            { start: 0, end: 8, text: "Même logique pour les missiles." },
            { start: 8, end: 15, text: "Mais attention : leur bulle bouge avec eux." },
            { start: 15, end: 22, text: "À chaque instant, il y a des endroits où le vaisseau ne peut pas être." }
          ],
          equation: { text: "‖r(t) − r_k(t)‖ ≥ d_mis", label: "Contrainte mobile", appearAt: 8 },
          setup: 'bubble_missile'
        },
        {
          id: "1.3",
          duration: 28,
          subtitles: [
            { start: 0, end: 10, text: "L'espace où le vaisseau peut aller, c'est le complémentaire de l'union de toutes ces bulles." },
            { start: 10, end: 20, text: "Cet espace change à chaque instant, parce que les missiles bougent." },
            { start: 20, end: 28, text: "Naviguer, c'est trouver un chemin qui reste toujours dans cet espace libre." }
          ],
          setup: 'navigable_space'
        }
      ]
    },
    // ========== PARTIE 2 : LE COÛT DU MOUVEMENT ==========
    {
      part: 2,
      title: "Le coût du mouvement",
      scenes: [
        {
          id: "2.1",
          duration: 25,
          subtitles: [
            { start: 0, end: 8, text: "Le vaisseau subit deux forces." },
            { start: 8, end: 16, text: "La gravité des astéroïdes — il la subit, il ne la contrôle pas." },
            { start: 16, end: 25, text: "Et sa propre poussée — c'est ce que le pilote décide." }
          ],
          equation: { text: "m r̈ = F − m∇Φ", label: "Équation du mouvement", appearAt: 10 },
          setup: 'forces_display'
        },
        {
          id: "2.2",
          duration: 30,
          subtitles: [
            { start: 0, end: 8, text: "Chaque poussée consomme du carburant." },
            { start: 8, end: 16, text: "Plus on pousse fort, plus ça coûte." },
            { start: 16, end: 24, text: "On veut minimiser le total dépensé." },
            { start: 24, end: 30, text: "Le carré pénalise les grosses poussées. Deux petites corrections coûtent moins qu'un gros coup de frein." }
          ],
          equation: { text: "J = ∫₀ᵀ ‖F(t)‖² dt", label: "Coût à minimiser", appearAt: 8 },
          setup: 'fuel_cost'
        },
        {
          id: "2.3",
          duration: 22,
          subtitles: [
            { start: 0, end: 8, text: "Mais la gravité, elle, est gratuite." },
            { start: 8, end: 16, text: "Si un astéroïde dévie ma trajectoire, je n'ai rien dépensé." },
            { start: 16, end: 22, text: "Première idée : utiliser les astéroïdes pour tourner sans carburant." }
          ],
          setup: 'gravity_free'
        }
      ]
    },
    // ========== PARTIE 3 : LE PRIX DE LA DÉVIATION ==========
    {
      part: 3,
      title: "Le prix de la déviation",
      scenes: [
        {
          id: "3.1",
          duration: 30,
          subtitles: [
            { start: 0, end: 10, text: "Regardons ce qui se passe quand on passe près d'un astéroïde." },
            { start: 10, end: 20, text: "À l'approche, la gravité nous attire — on accélère." },
            { start: 20, end: 30, text: "En s'éloignant, elle nous retient — on ralentit." }
          ],
          setup: 'flyby_approach'
        },
        {
          id: "3.2",
          duration: 28,
          subtitles: [
            { start: 0, end: 10, text: "Si l'astéroïde était fixé dans l'espace, ces deux effets se compenseraient." },
            { start: 10, end: 18, text: "Mais l'astéroïde n'est pas fixé. Il est libre." },
            { start: 18, end: 28, text: "Pendant qu'on l'approche, lui aussi est attiré vers nous. Il se met en mouvement." }
          ],
          setup: 'asteroid_moves'
        },
        {
          id: "3.3",
          duration: 32,
          subtitles: [
            { start: 0, end: 10, text: "L'énergie totale est conservée." },
            { start: 10, end: 20, text: "Si l'astéroïde gagne de l'énergie cinétique, le vaisseau en perd." },
            { start: 20, end: 32, text: "Chaque déviation a un coût. Plus on tourne, plus on perd." }
          ],
          equation: { text: "ΔK = −m²M/(m+M)² × v₀²(1−cosθ)", label: "Transfert d'énergie", appearAt: 10 },
          setup: 'energy_transfer'
        },
        {
          id: "3.4",
          duration: 35,
          subtitles: [
            { start: 0, end: 12, text: "Mais si l'astéroïde se déplace dans le bon sens — s'il arrive vers nous —" },
            { start: 12, end: 22, text: "le transfert s'inverse. On peut gagner de l'énergie sans carburant." },
            { start: 22, end: 35, text: "C'est l'assistance gravitationnelle. Les sondes spatiales l'utilisent pour accélérer." }
          ],
          setup: 'gravity_assist'
        }
      ]
    },
    // ========== PARTIE 4 : LES MISSILES ==========
    {
      part: 4,
      title: "Les missiles",
      scenes: [
        {
          id: "4.1",
          duration: 30,
          subtitles: [
            { start: 0, end: 10, text: "Premier cas : le missile balistique." },
            { start: 10, end: 20, text: "Une fois lancé, il ne corrige pas sa course. Il suit les lois de la mécanique." },
            { start: 20, end: 30, text: "Sa trajectoire est entièrement prévisible. On peut calculer exactement où il sera." }
          ],
          setup: 'ballistic_missile'
        },
        {
          id: "4.2",
          duration: 22,
          subtitles: [
            { start: 0, end: 8, text: "Deuxième cas : le missile guidé." },
            { start: 8, end: 16, text: "Celui-ci observe le vaisseau et corrige sa trajectoire en permanence." },
            { start: 16, end: 22, text: "On ne peut plus calculer sa trajectoire à l'avance — elle dépend de nous." }
          ],
          setup: 'guided_missile_intro'
        },
        {
          id: "4.3",
          duration: 25,
          subtitles: [
            { start: 0, end: 10, text: "Pour comprendre comment il fonctionne, introduisons la ligne de visée." },
            { start: 10, end: 18, text: "C'est le segment qui relie le missile au vaisseau." },
            { start: 18, end: 25, text: "Cette ligne a deux propriétés : sa longueur — la distance — et sa direction." }
          ],
          setup: 'line_of_sight'
        },
        {
          id: "4.4",
          duration: 40,
          subtitles: [
            { start: 0, end: 12, text: "Observons deux cas. Ici, la ligne de visée tourne — le missile passe à côté." },
            { start: 12, end: 24, text: "Là, elle garde la même direction — collision." },
            { start: 24, end: 34, text: "C'est une propriété géométrique : si la ligne de visée ne tourne pas, les deux mobiles se rencontrent." },
            { start: 34, end: 40, text: "Retenez bien ça. C'est la clé de tout ce qui suit." }
          ],
          setup: 'los_demonstration'
        },
        {
          id: "4.5",
          duration: 28,
          subtitles: [
            { start: 0, end: 10, text: "Le missile le sait. Sa stratégie : mesurer la vitesse de rotation de la ligne de visée." },
            { start: 10, end: 20, text: "Et pousser pour l'annuler." },
            { start: 20, end: 28, text: "S'il réussit à maintenir la ligne fixe, c'est la collision garantie." }
          ],
          equation: { text: "F_missile ∝ σ̇⊥", label: "Navigation proportionnelle", appearAt: 10 },
          setup: 'proportional_nav'
        },
        {
          id: "4.6",
          duration: 32,
          subtitles: [
            { start: 0, end: 10, text: "Donc notre objectif est clair : faire tourner cette ligne." },
            { start: 10, end: 20, text: "Comment ? En poussant perpendiculairement." },
            { start: 20, end: 32, text: "Une poussée parallèle change la distance. Une poussée perpendiculaire change la direction — c'est ça qui déroute le missile." }
          ],
          equation: { text: "d‖σ‖/dt = (σ·σ̇)/‖σ‖", label: "Seule la composante ∥ change la distance", appearAt: 15 },
          setup: 'perpendicular_thrust'
        }
      ]
    },
    // ========== PARTIE 5 : TROUVER UN CHEMIN ==========
    {
      part: 5,
      title: "Trouver un chemin",
      scenes: [
        {
          id: "5.1",
          duration: 30,
          subtitles: [
            { start: 0, end: 12, text: "Récapitulons. On doit trouver une trajectoire qui reste toujours dans l'espace libre." },
            { start: 12, end: 22, text: "Qui minimise le carburant dépensé." },
            { start: 22, end: 30, text: "Et qui tient compte de la réaction des missiles à nos mouvements." }
          ],
          setup: 'complete_problem'
        },
        {
          id: "5.2",
          duration: 28,
          subtitles: [
            { start: 0, end: 10, text: "Les contraintes sont : éviter les astéroïdes — contrainte fixe." },
            { start: 10, end: 18, text: "Éviter les missiles — contrainte mobile." },
            { start: 18, end: 28, text: "Ne pas dépasser la poussée maximale. Et arriver de l'autre côté." }
          ],
          setup: 'constraints_list'
        },
        {
          id: "5.3",
          duration: 30,
          subtitles: [
            { start: 0, end: 12, text: "Ce qui rend le problème difficile : l'espace libre change à chaque instant." },
            { start: 12, end: 22, text: "Un chemin valide maintenant peut devenir interdit dans deux secondes." },
            { start: 22, end: 30, text: "Et nos actions influencent les missiles, qui influencent l'espace libre. C'est couplé." }
          ],
          setup: 'dynamic_space'
        }
      ]
    },
    // ========== PARTIE 6 : LES TROIS PRINCIPES ==========
    {
      part: 6,
      title: "Les trois principes tactiques",
      scenes: [
        {
          id: "6.1",
          duration: 35,
          subtitles: [
            { start: 0, end: 10, text: "Premier principe : face à un missile, pousser perpendiculairement à la ligne de visée." },
            { start: 10, end: 22, text: "Pousser pour s'éloigner ? Le missile accélère et compense." },
            { start: 22, end: 35, text: "Pousser sur le côté ? La ligne tourne, le missile doit corriger — ça lui coûte du temps." }
          ],
          setup: 'principle_perpendicular'
        },
        {
          id: "6.2",
          duration: 35,
          subtitles: [
            { start: 0, end: 10, text: "Deuxième principe : manœuvrer tard." },
            { start: 10, end: 22, text: "Une manœuvre précoce donne au missile le temps de corriger. On doit re-manœuvrer." },
            { start: 22, end: 35, text: "Une manœuvre tardive le prend de court. Il n'a plus le temps de réagir. Risqué, mais efficace." }
          ],
          setup: 'principle_timing'
        },
        {
          id: "6.3",
          duration: 40,
          subtitles: [
            { start: 0, end: 12, text: "Troisième principe : utiliser les astéroïdes comme pièges." },
            { start: 12, end: 22, text: "L'astéroïde a une zone de capture — le rayon en dessous duquel la gravité piège tout objet." },
            { start: 22, end: 32, text: "Le vaisseau passe juste à l'extérieur — il est dévié, sans carburant." },
            { start: 32, end: 40, text: "Le missile, qui suit, passe plus près — il est capturé et s'écrase." }
          ],
          equation: { text: "b_cap = R√(1 + 2GM/Rv²∞)", label: "Rayon de capture", appearAt: 14 },
          setup: 'principle_trap'
        }
      ]
    },
    // ========== PARTIE 7 : LA FLOTTE ==========
    {
      part: 7,
      title: "La flotte",
      scenes: [
        {
          id: "7.1",
          duration: 35,
          subtitles: [
            { start: 0, end: 12, text: "Avec plusieurs vaisseaux, les interactions se multiplient." },
            { start: 12, end: 24, text: "Les vaisseaux s'attirent mutuellement — effet de peloton gravitationnel." },
            { start: 24, end: 35, text: "Un vaisseau peut servir de leurre, attirant un missile pendant que les autres s'échappent." }
          ],
          setup: 'fleet_dynamics'
        }
      ]
    },
    // ========== PARTIE 8 : SYNTHÈSE ==========
    {
      part: 8,
      title: "Synthèse",
      scenes: [
        {
          id: "8.1",
          duration: 35,
          subtitles: [
            { start: 0, end: 12, text: "Récapitulons. Chaque obstacle définit une bulle interdite." },
            { start: 12, end: 22, text: "Naviguer, c'est rester dans l'espace libre — qui change à chaque instant." },
            { start: 22, end: 35, text: "Les déviations coûtent de l'énergie, sauf si on exploite l'assistance gravitationnelle." }
          ],
          setup: 'synthesis_all'
        },
        {
          id: "8.2",
          duration: 30,
          subtitles: [
            { start: 0, end: 12, text: "Contre un missile guidé : pousser perpendiculairement, manœuvrer tard, utiliser les astéroïdes." },
            { start: 12, end: 22, text: "Survivre ne suffit pas." },
            { start: 22, end: 30, text: "La différence entre un bon pilote et un pilote optimal : ce qu'il reste dans le réservoir." }
          ],
          setup: 'conclusion'
        }
      ]
    }
  ];

  // ============================================================
  // FONCTIONS UTILITAIRES
  // ============================================================
  
  const getCurrentSceneData = () => {
    if (currentPart >= videoStructure.length) return null;
    const part = videoStructure[currentPart];
    if (currentScene >= part.scenes.length) return null;
    return part.scenes[currentScene];
  };

  const getTimeInSeconds = () => sceneTime / FPS;

  const getCurrentSubtitle = () => {
    const sceneData = getCurrentSceneData();
    if (!sceneData) return null;
    const time = getTimeInSeconds();
    return sceneData.subtitles.find(s => time >= s.start && time < s.end);
  };

  const shouldShowEquation = () => {
    const sceneData = getCurrentSceneData();
    if (!sceneData?.equation) return false;
    return getTimeInSeconds() >= sceneData.equation.appearAt;
  };

  const getTotalDuration = () => {
    return videoStructure.reduce((sum, part) => 
      sum + part.scenes.reduce((s, scene) => s + scene.duration, 0), 0);
  };

  const getCurrentTotalTime = () => {
    let time = 0;
    for (let p = 0; p < currentPart; p++) {
      time += videoStructure[p].scenes.reduce((s, scene) => s + scene.duration, 0);
    }
    for (let s = 0; s < currentScene; s++) {
      time += videoStructure[currentPart].scenes[s].duration;
    }
    return time + getTimeInSeconds();
  };

  const formatTime = (seconds) => {
    const m = Math.floor(seconds / 60);
    const s = Math.floor(seconds % 60);
    return `${m}:${s.toString().padStart(2, '0')}`;
  };

  // ============================================================
  // INITIALISATION DES SCÈNES
  // ============================================================
  
  const initScene = useCallback((setup) => {
    const state = stateRef.current;
    
    // Reset commun
    state.particles = [];
    state.trail = [];
    state.showBubbles = false;
    state.showForces = false;
    state.showLOS = false;
    state.showCapture = false;
    state.showPrediction = false;
    state.showNavigableSpace = false;
    state.showEnergyBars = false;
    state.showComparison = false;
    state.comparisonPhase = 0;
    state.fuel = 100;
    state.asteroids = [];
    state.missiles = [];
    state.otherShips = [];
    state.demoMode = null;
    state.asteroidVelocity = { x: 0, y: 0 };
    state.initialEnergy = { ship: 100, asteroid: 0 };
    state.currentEnergy = { ship: 100, asteroid: 0 };
    
    switch(setup) {
      // PARTIE 0
      case 'intro_problem':
        state.ship = { x: 60, y: 300, vx: 0.6, vy: 0, thrust: { x: 0, y: 0 } };
        state.asteroids = [
          { x: 250, y: 180, r: 40, mass: 55 },
          { x: 400, y: 400, r: 50, mass: 70 },
          { x: 320, y: 300, r: 32, mass: 42 }
        ];
        state.missiles = [
          { x: 600, y: 150, vx: -0.4, vy: 0.15, active: true, guided: true },
          { x: 620, y: 450, vx: -0.35, vy: -0.1, active: true, guided: true }
        ];
        break;

      // PARTIE 1 - Zones interdites
      case 'bubble_asteroid':
        state.ship = { x: 500, y: 300, vx: 0, vy: 0, thrust: { x: 0, y: 0 } };
        state.asteroids = [{ x: 300, y: 300, r: 50, mass: 70 }];
        state.showBubbles = true;
        state.bubbleGrowth = 0;
        state.demoMode = 'growBubble';
        break;

      case 'bubble_missile':
        state.ship = { x: 150, y: 300, vx: 0, vy: 0, thrust: { x: 0, y: 0 } };
        state.missiles = [{ x: 500, y: 300, vx: -0.8, vy: 0, active: true, guided: false }];
        state.showBubbles = true;
        break;

      case 'navigable_space':
        state.ship = { x: 80, y: 300, vx: 0.5, vy: 0, thrust: { x: 0, y: 0 } };
        state.asteroids = [
          { x: 250, y: 200, r: 38, mass: 50 },
          { x: 380, y: 420, r: 45, mass: 60 }
        ];
        state.missiles = [
          { x: 550, y: 250, vx: -0.5, vy: 0.2, active: true, guided: false }
        ];
        state.showBubbles = true;
        state.showNavigableSpace = true;
        break;

      // PARTIE 2 - Coût du mouvement
      case 'forces_display':
        state.ship = { x: 200, y: 300, vx: 0.4, vy: 0, thrust: { x: 0.05, y: -0.02 } };
        state.asteroids = [{ x: 450, y: 320, r: 55, mass: 85 }];
        state.showForces = true;
        break;

      case 'fuel_cost':
        state.ship = { x: 100, y: 300, vx: 0.8, vy: 0, thrust: { x: 0, y: 0 } };
        state.asteroids = [
          { x: 300, y: 220, r: 35, mass: 45 },
          { x: 450, y: 400, r: 40, mass: 55 }
        ];
        state.showForces = true;
        state.demoMode = 'fuelDemo';
        break;

      case 'gravity_free':
        state.ship = { x: 120, y: 350, vx: 1.2, vy: -0.3, thrust: { x: 0, y: 0 } };
        state.asteroids = [{ x: 350, y: 280, r: 50, mass: 90 }];
        state.showForces = true;
        state.demoMode = 'gravityFree';
        break;

      // PARTIE 3 - Prix de la déviation
      case 'flyby_approach':
        state.ship = { x: 100, y: 380, vx: 1.5, vy: -0.4, thrust: { x: 0, y: 0 } };
        state.asteroids = [{ x: 350, y: 300, r: 45, mass: 80, fixed: true }];
        state.showForces = true;
        state.demoMode = 'flyby';
        break;

      case 'asteroid_moves':
        state.ship = { x: 100, y: 380, vx: 1.5, vy: -0.4, thrust: { x: 0, y: 0 } };
        state.asteroids = [{ x: 350, y: 300, r: 45, mass: 80, vx: 0, vy: 0 }];
        state.showForces = true;
        state.demoMode = 'asteroidMoves';
        break;

      case 'energy_transfer':
        state.ship = { x: 100, y: 380, vx: 1.5, vy: -0.4, thrust: { x: 0, y: 0 } };
        state.asteroids = [{ x: 350, y: 300, r: 45, mass: 80, vx: 0, vy: 0 }];
        state.showEnergyBars = true;
        state.initialEnergy = { ship: 100, asteroid: 0 };
        state.currentEnergy = { ship: 100, asteroid: 0 };
        state.demoMode = 'energyTransfer';
        break;

      case 'gravity_assist':
        state.ship = { x: 150, y: 400, vx: 1, vy: -0.5, thrust: { x: 0, y: 0 } };
        state.asteroids = [{ x: 400, y: 300, r: 45, mass: 80, vx: -0.8, vy: 0 }];
        state.showEnergyBars = true;
        state.initialEnergy = { ship: 80, asteroid: 20 };
        state.currentEnergy = { ship: 80, asteroid: 20 };
        state.demoMode = 'gravityAssist';
        break;

      // PARTIE 4 - Les missiles
      case 'ballistic_missile':
        state.ship = { x: 120, y: 300, vx: 0.5, vy: 0, thrust: { x: 0, y: 0 } };
        state.missiles = [{ x: 600, y: 180, vx: -1.2, vy: 0.4, active: true, ballistic: true }];
        state.asteroids = [{ x: 380, y: 380, r: 40, mass: 60 }];
        state.showPrediction = true;
        break;

      case 'guided_missile_intro':
        state.ship = { x: 150, y: 300, vx: 0.4, vy: 0, thrust: { x: 0, y: 0 } };
        state.missiles = [{ x: 550, y: 300, vx: -0.8, vy: 0, active: true, guided: true }];
        break;

      case 'line_of_sight':
        state.ship = { x: 180, y: 300, vx: 0.3, vy: 0.1, thrust: { x: 0, y: 0 } };
        state.missiles = [{ x: 520, y: 300, vx: -0.6, vy: 0, active: true, guided: true }];
        state.showLOS = true;
        state.demoMode = 'showLOS';
        break;

      case 'los_demonstration':
        state.ship = { x: 150, y: 300, vx: 0, vy: 0, thrust: { x: 0, y: 0 } };
        state.missiles = [{ x: 550, y: 300, vx: -1.2, vy: 0, active: true, guided: false }];
        state.showLOS = true;
        state.showComparison = true;
        state.comparisonPhase = 0;
        state.demoMode = 'losComparison';
        break;

      case 'proportional_nav':
        state.ship = { x: 180, y: 300, vx: 0.3, vy: 0.2, thrust: { x: 0, y: 0 } };
        state.missiles = [{ x: 550, y: 320, vx: -1, vy: 0, active: true, guided: true }];
        state.showLOS = true;
        state.demoMode = 'propNav';
        break;

      case 'perpendicular_thrust':
        state.ship = { x: 180, y: 300, vx: 0.2, vy: 0, thrust: { x: 0, y: 0 } };
        state.missiles = [{ x: 520, y: 300, vx: -1, vy: 0, active: true, guided: true }];
        state.showLOS = true;
        state.showForces = true;
        state.demoMode = 'perpThrust';
        break;

      // PARTIE 5 - Trouver un chemin
      case 'complete_problem':
        state.ship = { x: 80, y: 300, vx: 0.5, vy: 0, thrust: { x: 0, y: 0 } };
        state.asteroids = [
          { x: 240, y: 200, r: 35, mass: 50 },
          { x: 380, y: 400, r: 42, mass: 60 }
        ];
        state.missiles = [
          { x: 550, y: 180, vx: -0.6, vy: 0.2, active: true, guided: true },
          { x: 580, y: 420, vx: -0.5, vy: -0.15, active: true, guided: true }
        ];
        state.showBubbles = true;
        state.showNavigableSpace = true;
        break;

      case 'constraints_list':
        state.ship = { x: 80, y: 300, vx: 0.4, vy: 0, thrust: { x: 0, y: 0 } };
        state.asteroids = [
          { x: 260, y: 220, r: 38, mass: 52 },
          { x: 400, y: 380, r: 44, mass: 62 }
        ];
        state.missiles = [{ x: 560, y: 280, vx: -0.5, vy: 0.1, active: true, guided: true }];
        state.showBubbles = true;
        break;

      case 'dynamic_space':
        state.ship = { x: 100, y: 300, vx: 0.6, vy: 0, thrust: { x: 0, y: 0 } };
        state.asteroids = [
          { x: 280, y: 240, r: 36, mass: 48 }
        ];
        state.missiles = [
          { x: 500, y: 200, vx: -0.4, vy: 0.3, active: true, guided: true },
          { x: 520, y: 400, vx: -0.45, vy: -0.25, active: true, guided: true }
        ];
        state.showBubbles = true;
        state.showNavigableSpace = true;
        break;

      // PARTIE 6 - Les trois principes
      case 'principle_perpendicular':
        state.ship = { x: 180, y: 300, vx: 0.2, vy: 0, thrust: { x: 0, y: 0 } };
        state.missiles = [{ x: 520, y: 300, vx: -1.2, vy: 0, active: true, guided: true }];
        state.showLOS = true;
        state.showForces = true;
        state.demoMode = 'principlePerp';
        break;

      case 'principle_timing':
        state.ship = { x: 140, y: 300, vx: 0.3, vy: 0, thrust: { x: 0, y: 0 } };
        state.missiles = [{ x: 580, y: 300, vx: -1.4, vy: 0, active: true, guided: true }];
        state.showLOS = true;
        state.showForces = true;
        state.demoMode = 'principleTiming';
        break;

      case 'principle_trap':
        state.ship = { x: 80, y: 260, vx: 1.3, vy: 0.3, thrust: { x: 0, y: 0 } };
        state.missiles = [{ x: 100, y: 340, vx: 1.4, vy: 0.2, active: true, guided: true }];
        state.asteroids = [{ x: 380, y: 300, r: 50, mass: 120 }];
        state.showLOS = true;
        state.showCapture = true;
        break;

      // PARTIE 7 - La flotte
      case 'fleet_dynamics':
        state.ship = { x: 160, y: 300, vx: 0.7, vy: 0, thrust: { x: 0, y: 0 } };
        state.otherShips = [
          { x: 110, y: 240, vx: 0.7, vy: 0, mass: 22 },
          { x: 110, y: 360, vx: 0.7, vy: 0, mass: 22 },
          { x: 70, y: 300, vx: 0.7, vy: 0, mass: 40 }
        ];
        state.missiles = [{ x: 580, y: 280, vx: -1, vy: 0.05, active: true, guided: true }];
        state.asteroids = [{ x: 420, y: 380, r: 38, mass: 55 }];
        break;

      // PARTIE 8 - Synthèse
      case 'synthesis_all':
        state.ship = { x: 80, y: 300, vx: 0.8, vy: 0, thrust: { x: 0, y: 0 } };
        state.asteroids = [
          { x: 260, y: 220, r: 38, mass: 58 },
          { x: 400, y: 400, r: 45, mass: 72 }
        ];
        state.missiles = [
          { x: 520, y: 150, vx: -0.8, vy: 0.4, active: true, guided: true },
          { x: 550, y: 450, vx: -0.7, vy: -0.35, active: true, guided: true }
        ];
        state.showBubbles = true;
        state.showLOS = true;
        state.showCapture = true;
        state.showForces = true;
        break;

      case 'conclusion':
        state.ship = { x: 80, y: 300, vx: 1, vy: 0, thrust: { x: 0, y: 0 } };
        state.asteroids = [
          { x: 280, y: 240, r: 40, mass: 60 },
          { x: 420, y: 380, r: 48, mass: 75 }
        ];
        state.missiles = [
          { x: 500, y: 160, vx: -0.9, vy: 0.5, active: true, guided: true }
        ];
        state.showForces = true;
        state.showLOS = true;
        state.showCapture = true;
        break;

      default:
        state.ship = { x: 100, y: 300, vx: 0.5, vy: 0, thrust: { x: 0, y: 0 } };
        break;
    }
  }, []);

  // ============================================================
  // PHYSIQUE
  // ============================================================
  
  const calculateGravity = (obj, asteroids, otherShips = []) => {
    let fx = 0, fy = 0;
    const G = 35;
    
    const bodies = [...asteroids, ...otherShips];
    bodies.forEach(body => {
      const mass = body.mass || 20;
      const minDist = body.r ? body.r + 5 : 15;
      const dx = body.x - obj.x;
      const dy = body.y - obj.y;
      const dist = Math.sqrt(dx * dx + dy * dy);
      if (dist > minDist) {
        const force = G * mass / (dist * dist);
        fx += force * dx / dist;
        fy += force * dy / dist;
      }
    });
    
    return { fx, fy };
  };

  const calculateEvasion = (ship, missiles, asteroids, state) => {
    let thrustX = 0, thrustY = 0;
    const maxThrust = 0.07;

    // Modes de démonstration spécifiques
    if (state.demoMode === 'gravityFree' || state.demoMode === 'flyby' || 
        state.demoMode === 'asteroidMoves' || state.demoMode === 'energyTransfer' ||
        state.demoMode === 'gravityAssist') {
      return { x: 0, y: 0 }; // Pas de poussée dans ces démos
    }

    if (state.demoMode === 'fuelDemo') {
      // Poussée périodique pour montrer la consommation
      const t = sceneTime / FPS;
      if (t > 5 && t < 8) {
        thrustX = 0.05;
        thrustY = -0.03;
      } else if (t > 12 && t < 14) {
        thrustX = 0.04;
        thrustY = 0.02;
      }
      return { x: thrustX, y: thrustY };
    }

    if (state.demoMode === 'principleTiming') {
      // Attendre avant de manœuvrer
      const closestMissile = missiles.find(m => m.active);
      if (closestMissile) {
        const dist = Math.sqrt((ship.x - closestMissile.x) ** 2 + (ship.y - closestMissile.y) ** 2);
        if (dist < 120) { // Manœuvre tardive
          const dx = ship.x - closestMissile.x;
          const dy = ship.y - closestMissile.y;
          const perpX = -dy / dist;
          const perpY = dx / dist;
          return { x: perpX * maxThrust * 1.5, y: perpY * maxThrust * 1.5 };
        }
      }
      return { x: 0, y: 0 };
    }

    // Évitement standard
    missiles.forEach(m => {
      if (!m.active) return;
      const dx = ship.x - m.x;
      const dy = ship.y - m.y;
      const dist = Math.sqrt(dx * dx + dy * dy);
      
      if (dist < 300) {
        const perpX = -dy / dist;
        const perpY = dx / dist;
        const side = (ship.vy * dx - ship.vx * dy) > 0 ? 1 : -1;
        let urgency = Math.max(0, 1 - dist / 300);
        
        thrustX += side * perpX * urgency * maxThrust;
        thrustY += side * perpY * urgency * maxThrust;
      }
    });

    asteroids.forEach(ast => {
      const dx = ship.x - ast.x;
      const dy = ship.y - ast.y;
      const dist = Math.sqrt(dx * dx + dy * dy);
      if (dist < ast.r + 100) {
        const urgency = Math.max(0, 1 - (dist - ast.r) / 100);
        thrustX += dx / dist * urgency * maxThrust * 0.2;
        thrustY += dy / dist * urgency * maxThrust * 0.2;
      }
    });

    const mag = Math.sqrt(thrustX * thrustX + thrustY * thrustY);
    if (mag > maxThrust) {
      thrustX = thrustX / mag * maxThrust;
      thrustY = thrustY / mag * maxThrust;
    }

    return { x: thrustX, y: thrustY };
  };

  // ============================================================
  // MISE À JOUR SIMULATION
  // ============================================================
  
  const updateSimulation = useCallback(() => {
    const state = stateRef.current;
    if (!state.ship) return;

    const { ship, missiles = [], asteroids = [], particles = [], trail = [], otherShips = [] } = state;

    // Croissance de la bulle (démo)
    if (state.demoMode === 'growBubble') {
      state.bubbleGrowth = Math.min(1, (state.bubbleGrowth || 0) + 0.015);
    }

    // Démonstration LOS comparison
    if (state.demoMode === 'losComparison') {
      const t = getTimeInSeconds();
      if (t < 12) {
        state.comparisonPhase = 0; // Ligne qui tourne
        ship.vy = 0.8;
      } else if (t < 24) {
        state.comparisonPhase = 1; // Ligne fixe
        ship.vy = 0;
        ship.y = 300;
      } else {
        state.comparisonPhase = 2; // Explication
      }
    }

    // Gravité sur le vaisseau
    const gravity = calculateGravity(ship, asteroids, otherShips);
    const thrust = calculateEvasion(ship, missiles, asteroids, state);
    ship.thrust = thrust;
    
    ship.vx += gravity.fx * 0.007 + thrust.x;
    ship.vy += gravity.fy * 0.007 + thrust.y;
    ship.x += ship.vx;
    ship.y += ship.vy;
    
    // Carburant
    const thrustMag = Math.sqrt(thrust.x * thrust.x + thrust.y * thrust.y);
    if (thrustMag > 0.003) {
      state.fuel = Math.max(0, state.fuel - thrustMag * 1.2);
      
      // Particules de poussée
      particles.push({
        x: ship.x,
        y: ship.y,
        vx: -thrust.x * 12 + (Math.random() - 0.5) * 1.5,
        vy: -thrust.y * 12 + (Math.random() - 0.5) * 1.5,
        life: 28,
        maxLife: 28
      });
    }

    // Trail
    trail.push({ x: ship.x, y: ship.y, age: 0 });
    if (trail.length > 100) trail.shift();
    trail.forEach(t => t.age++);

    // Mise à jour des astéroïdes mobiles
    asteroids.forEach(ast => {
      if (ast.fixed) return;
      if (ast.vx !== undefined) {
        // Gravité du vaisseau sur l'astéroïde
        const dx = ship.x - ast.x;
        const dy = ship.y - ast.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist > 20) {
          const G = 35;
          const force = G * 30 / (dist * dist); // masse du vaisseau = 30
          ast.vx += force * dx / dist * 0.001;
          ast.vy += force * dy / dist * 0.001;
        }
        ast.x += ast.vx;
        ast.y += ast.vy;
        
        // Mise à jour des barres d'énergie
        if (state.showEnergyBars) {
          const astSpeed = Math.sqrt(ast.vx * ast.vx + ast.vy * ast.vy);
          const shipSpeed = Math.sqrt(ship.vx * ship.vx + ship.vy * ship.vy);
          state.currentEnergy.asteroid = Math.min(100, astSpeed * 50);
          state.currentEnergy.ship = Math.max(0, 100 - state.currentEnergy.asteroid);
        }
      }
    });

    // Autres vaisseaux
    otherShips.forEach(s => {
      const g = calculateGravity(s, asteroids, []);
      s.vx += g.fx * 0.005;
      s.vy += g.fy * 0.005;
      s.x += s.vx;
      s.y += s.vy;
    });

    // Missiles
    missiles.forEach(m => {
      if (!m.active) return;

      if (m.guided) {
        const dx = ship.x - m.x;
        const dy = ship.y - m.y;
        const dist = Math.sqrt(dx * dx + dy * dy);
        if (dist > 10) {
          m.vx += dx / dist * 0.018;
          m.vy += dy / dist * 0.018;
        }
      }

      const mGrav = calculateGravity(m, asteroids, []);
      m.vx += mGrav.fx * 0.009;
      m.vy += mGrav.fy * 0.009;

      m.x += m.vx;
      m.y += m.vy;

      // Collision avec astéroïde
      asteroids.forEach(ast => {
        const d = Math.sqrt((m.x - ast.x) ** 2 + (m.y - ast.y) ** 2);
        if (d < ast.r + 8) {
          m.active = false;
          for (let i = 0; i < 35; i++) {
            const angle = Math.random() * Math.PI * 2;
            const speed = Math.random() * 5 + 2;
            particles.push({
              x: m.x, y: m.y,
              vx: Math.cos(angle) * speed,
              vy: Math.sin(angle) * speed,
              life: 45, maxLife: 45, explosion: true
            });
          }
        }
      });

      if (m.x < -80 || m.x > 780 || m.y < -80 || m.y > 680) {
        m.active = false;
      }
    });

    // Particules
    for (let i = particles.length - 1; i >= 0; i--) {
      const p = particles[i];
      p.x += p.vx;
      p.y += p.vy;
      p.vx *= 0.96;
      p.vy *= 0.96;
      p.life--;
      if (p.life <= 0) particles.splice(i, 1);
    }

    // Reset si sortie d'écran
    if (ship.x > 780 || ship.x < -80 || ship.y < -80 || ship.y > 680) {
      const sceneData = getCurrentSceneData();
      if (sceneData) initScene(sceneData.setup);
    }
  }, [sceneTime, initScene]);

  // ============================================================
  // RENDU
  // ============================================================
  
  const draw = useCallback(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;
    const ctx = canvas.getContext('2d');
    const state = stateRef.current;

    // Fond spatial
    const gradient = ctx.createLinearGradient(0, 0, 0, 600);
    gradient.addColorStop(0, '#050515');
    gradient.addColorStop(1, '#0d0520');
    ctx.fillStyle = gradient;
    ctx.fillRect(0, 0, 700, 600);

    // Étoiles
    for (let i = 0; i < 60; i++) {
      const x = (i * 71 + sceneTime * 0.03) % 700;
      const y = (i * 131) % 600;
      ctx.fillStyle = `rgba(255,255,255,${0.12 + (i % 5) * 0.08})`;
      ctx.beginPath();
      ctx.arc(x, y, (i % 3) * 0.3 + 0.3, 0, Math.PI * 2);
      ctx.fill();
    }

    if (!state.ship) return;

    const { ship, missiles = [], asteroids = [], particles = [], trail = [], otherShips = [] } = state;

    // Espace navigable (fond)
    if (state.showNavigableSpace) {
      ctx.fillStyle = 'rgba(0, 80, 40, 0.12)';
      ctx.fillRect(0, 0, 700, 600);
    }

    // Trail
    trail.forEach(t => {
      const alpha = 1 - t.age / 100;
      ctx.fillStyle = `rgba(0, 150, 255, ${alpha * 0.3})`;
      ctx.beginPath();
      ctx.arc(t.x, t.y, 2 * alpha + 0.5, 0, Math.PI * 2);
      ctx.fill();
    });

    // Astéroïdes
    asteroids.forEach(ast => {
      // Champ gravitationnel
      for (let r = ast.r + 10; r < ast.r + 80; r += 14) {
        ctx.strokeStyle = `rgba(100, 110, 160, ${0.08 * (1 - (r - ast.r) / 80)})`;
        ctx.lineWidth = 1;
        ctx.beginPath();
        ctx.arc(ast.x, ast.y, r, 0, Math.PI * 2);
        ctx.stroke();
      }

      // Bulle interdite
      if (state.showBubbles) {
        const bubbleR = ast.r + 25;
        const growth = state.bubbleGrowth !== undefined ? state.bubbleGrowth : 1;
        ctx.fillStyle = 'rgba(255, 60, 60, 0.08)';
        ctx.beginPath();
        ctx.arc(ast.x, ast.y, bubbleR * growth, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = 'rgba(255, 100, 100, 0.5)';
        ctx.lineWidth = 2;
        ctx.setLineDash([6, 4]);
        ctx.stroke();
        ctx.setLineDash([]);
        
        if (growth > 0.8) {
          ctx.fillStyle = 'rgba(255, 150, 150, 0.7)';
          ctx.font = '10px sans-serif';
          ctx.fillText('zone interdite', ast.x - 32, ast.y - bubbleR - 8);
        }
      }

      // Zone de capture
      if (state.showCapture) {
        const captureR = ast.r * 1.6;
        ctx.fillStyle = 'rgba(255, 150, 50, 0.08)';
        ctx.beginPath();
        ctx.arc(ast.x, ast.y, captureR, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = 'rgba(255, 180, 80, 0.5)';
        ctx.lineWidth = 1.5;
        ctx.setLineDash([4, 4]);
        ctx.stroke();
        ctx.setLineDash([]);
        
        ctx.fillStyle = 'rgba(255, 200, 120, 0.7)';
        ctx.font = '9px sans-serif';
        ctx.fillText('capture', ast.x - 18, ast.y + captureR + 12);
      }

      // Astéroïde lui-même
      const astGrad = ctx.createRadialGradient(
        ast.x - ast.r * 0.3, ast.y - ast.r * 0.3, 0,
        ast.x, ast.y, ast.r
      );
      astGrad.addColorStop(0, '#9a8a78');
      astGrad.addColorStop(1, '#4a4540');
      ctx.fillStyle = astGrad;
      ctx.beginPath();
      ctx.arc(ast.x, ast.y, ast.r, 0, Math.PI * 2);
      ctx.fill();

      // Cratères
      ctx.fillStyle = 'rgba(0,0,0,0.18)';
      ctx.beginPath();
      ctx.arc(ast.x + ast.r * 0.22, ast.y - ast.r * 0.12, ast.r * 0.14, 0, Math.PI * 2);
      ctx.fill();
    });

    // Bulles des missiles
    if (state.showBubbles) {
      missiles.forEach(m => {
        if (!m.active) return;
        const bubbleR = 35;
        ctx.fillStyle = 'rgba(255, 50, 50, 0.1)';
        ctx.beginPath();
        ctx.arc(m.x, m.y, bubbleR, 0, Math.PI * 2);
        ctx.fill();
        ctx.strokeStyle = 'rgba(255, 80, 80, 0.6)';
        ctx.lineWidth = 2;
        ctx.setLineDash([5, 3]);
        ctx.stroke();
        ctx.setLineDash([]);
      });
    }

    // Particules
    particles.forEach(p => {
      const alpha = p.life / p.maxLife;
      if (p.explosion) {
        ctx.fillStyle = `rgba(255, ${70 + 180 * alpha}, 15, ${alpha})`;
        ctx.beginPath();
        ctx.arc(p.x, p.y, 4 * alpha, 0, Math.PI * 2);
        ctx.fill();
      } else {
        ctx.fillStyle = `rgba(0, 220, 255, ${alpha * 0.65})`;
        ctx.beginPath();
        ctx.arc(p.x, p.y, 1.8, 0, Math.PI * 2);
        ctx.fill();
      }
    });

    // Trajectoire prédite (missile balistique)
    if (state.showPrediction) {
      missiles.forEach(m => {
        if (!m.active || !m.ballistic) return;
        ctx.strokeStyle = 'rgba(255, 200, 100, 0.4)';
        ctx.setLineDash([5, 4]);
        ctx.lineWidth = 1.5;
        ctx.beginPath();
        let px = m.x, py = m.y, pvx = m.vx, pvy = m.vy;
        ctx.moveTo(px, py);
        for (let t = 0; t < 150; t++) {
          const g = calculateGravity({ x: px, y: py }, asteroids, []);
          pvx += g.fx * 0.007;
          pvy += g.fy * 0.007;
          px += pvx;
          py += pvy;
          ctx.lineTo(px, py);
        }
        ctx.stroke();
        ctx.setLineDash([]);
        
        ctx.fillStyle = 'rgba(255, 220, 140, 0.65)';
        ctx.font = '10px sans-serif';
        ctx.fillText('trajectoire prédite', m.x - 5, m.y - 18);
      });
    }

    // Ligne de visée
    if (state.showLOS) {
      missiles.forEach(m => {
        if (!m.active) return;
        
        // Ligne
        ctx.strokeStyle = 'rgba(255, 80, 80, 0.5)';
        ctx.setLineDash([8, 6]);
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(m.x, m.y);
        ctx.lineTo(ship.x, ship.y);
        ctx.stroke();
        ctx.setLineDash([]);
        
        // Label σ
        const midX = (m.x + ship.x) / 2;
        const midY = (m.y + ship.y) / 2;
        ctx.fillStyle = 'rgba(255, 140, 140, 0.8)';
        ctx.font = 'italic 14px serif';
        ctx.fillText('σ', midX + 12, midY - 8);
        
        // Direction de la ligne (flèche)
        const angle = Math.atan2(ship.y - m.y, ship.x - m.x);
        const arrowX = midX + 30 * Math.cos(angle);
        const arrowY = midY + 30 * Math.sin(angle);
        ctx.fillStyle = 'rgba(255, 100, 100, 0.7)';
        ctx.beginPath();
        ctx.moveTo(arrowX, arrowY);
        ctx.lineTo(arrowX - 8 * Math.cos(angle - 0.4), arrowY - 8 * Math.sin(angle - 0.4));
        ctx.lineTo(arrowX - 8 * Math.cos(angle + 0.4), arrowY - 8 * Math.sin(angle + 0.4));
        ctx.closePath();
        ctx.fill();
      });
    }

    // Comparaison LOS
    if (state.showComparison && state.comparisonPhase !== undefined) {
      ctx.fillStyle = 'rgba(0, 0, 0, 0.7)';
      ctx.fillRect(10, 10, 200, 50);
      ctx.fillStyle = '#fff';
      ctx.font = '12px sans-serif';
      if (state.comparisonPhase === 0) {
        ctx.fillText('La ligne TOURNE', 20, 30);
        ctx.fillStyle = '#8f8';
        ctx.fillText('→ Le missile passe à côté', 20, 48);
      } else if (state.comparisonPhase === 1) {
        ctx.fillText('La ligne est FIXE', 20, 30);
        ctx.fillStyle = '#f88';
        ctx.fillText('→ COLLISION', 20, 48);
      }
    }

    // Missiles
    missiles.forEach(m => {
      if (!m.active) return;

      // Trainée
      ctx.strokeStyle = 'rgba(255, 50, 50, 0.5)';
      ctx.lineWidth = 2.5;
      ctx.beginPath();
      ctx.moveTo(m.x, m.y);
      ctx.lineTo(m.x - m.vx * 15, m.y - m.vy * 15);
      ctx.stroke();

      // Corps
      const angle = Math.atan2(m.vy, m.vx);
      ctx.save();
      ctx.translate(m.x, m.y);
      ctx.rotate(angle);

      ctx.fillStyle = '#e83030';
      ctx.beginPath();
      ctx.moveTo(16, 0);
      ctx.lineTo(-12, -7);
      ctx.lineTo(-8, 0);
      ctx.lineTo(-12, 7);
      ctx.closePath();
      ctx.fill();

      ctx.fillStyle = '#ffaa00';
      ctx.beginPath();
      ctx.moveTo(-8, -4);
      ctx.lineTo(-22 - Math.random() * 8, 0);
      ctx.lineTo(-8, 4);
      ctx.closePath();
      ctx.fill();

      ctx.restore();
    });

    // Autres vaisseaux
    otherShips.forEach(s => {
      ctx.save();
      ctx.translate(s.x, s.y);
      ctx.rotate(Math.atan2(s.vy, s.vx));

      ctx.fillStyle = '#50a050';
      ctx.beginPath();
      ctx.moveTo(14, 0);
      ctx.lineTo(-10, -9);
      ctx.lineTo(-6, 0);
      ctx.lineTo(-10, 9);
      ctx.closePath();
      ctx.fill();

      ctx.restore();
    });

    // Vaisseau principal
    ctx.save();
    ctx.translate(ship.x, ship.y);
    ctx.rotate(Math.atan2(ship.vy || 0.1, ship.vx || 1));

    ctx.fillStyle = '#3085e0';
    ctx.beginPath();
    ctx.moveTo(26, 0);
    ctx.lineTo(-16, -15);
    ctx.lineTo(-10, 0);
    ctx.lineTo(-16, 15);
    ctx.closePath();
    ctx.fill();

    ctx.fillStyle = '#80c0ff';
    ctx.beginPath();
    ctx.ellipse(8, 0, 9, 5.5, 0, 0, Math.PI * 2);
    ctx.fill();

    const thrustMag = Math.sqrt(ship.thrust.x ** 2 + ship.thrust.y ** 2);
    if (thrustMag > 0.003) {
      ctx.fillStyle = '#00eeff';
      const flameLen = 10 + thrustMag * 200 + Math.random() * 12;
      ctx.beginPath();
      ctx.moveTo(-10, -6);
      ctx.lineTo(-10 - flameLen, 0);
      ctx.lineTo(-10, 6);
      ctx.closePath();
      ctx.fill();
    }

    ctx.restore();

    // Vecteurs de force
    if (state.showForces) {
      // Poussée F
      if (thrustMag > 0.002) {
        ctx.strokeStyle = '#00ffff';
        ctx.lineWidth = 2.5;
        ctx.beginPath();
        ctx.moveTo(ship.x, ship.y);
        const endX = ship.x + ship.thrust.x * 600;
        const endY = ship.y + ship.thrust.y * 600;
        ctx.lineTo(endX, endY);
        ctx.stroke();

        const arrowAngle = Math.atan2(ship.thrust.y, ship.thrust.x);
        ctx.fillStyle = '#00ffff';
        ctx.beginPath();
        ctx.moveTo(endX, endY);
        ctx.lineTo(endX - 10 * Math.cos(arrowAngle - 0.35), endY - 10 * Math.sin(arrowAngle - 0.35));
        ctx.lineTo(endX - 10 * Math.cos(arrowAngle + 0.35), endY - 10 * Math.sin(arrowAngle + 0.35));
        ctx.closePath();
        ctx.fill();

        ctx.font = 'bold 16px sans-serif';
        ctx.fillText('F', endX + 10, endY - 10);
      }

      // Gravité −∇Φ
      const grav = calculateGravity(ship, asteroids, []);
      const gravMag = Math.sqrt(grav.fx * grav.fx + grav.fy * grav.fy);
      if (gravMag > 0.03) {
        ctx.strokeStyle = '#ffaa44';
        ctx.lineWidth = 2;
        ctx.beginPath();
        ctx.moveTo(ship.x, ship.y);
        const gEndX = ship.x + grav.fx * 5;
        const gEndY = ship.y + grav.fy * 5;
        ctx.lineTo(gEndX, gEndY);
        ctx.stroke();

        ctx.fillStyle = '#ffaa44';
        ctx.font = 'bold 13px sans-serif';
        ctx.fillText('−∇Φ', gEndX + 8, gEndY);
      }
    }

    // Barres d'énergie
    if (state.showEnergyBars) {
      const barX = 20, barY = 500, barW = 120, barH = 18;
      
      // Fond
      ctx.fillStyle = 'rgba(0,0,0,0.7)';
      ctx.fillRect(barX - 5, barY - 25, barW + 10, 75);
      
      // Titre
      ctx.fillStyle = '#fff';
      ctx.font = '11px sans-serif';
      ctx.fillText('Énergie cinétique', barX, barY - 8);
      
      // Barre vaisseau
      ctx.fillStyle = '#333';
      ctx.fillRect(barX, barY, barW, barH);
      ctx.fillStyle = '#4488ff';
      ctx.fillRect(barX, barY, barW * state.currentEnergy.ship / 100, barH);
      ctx.fillStyle = '#fff';
      ctx.font = '10px sans-serif';
      ctx.fillText('Vaisseau', barX + barW + 5, barY + 13);
      
      // Barre astéroïde
      ctx.fillStyle = '#333';
      ctx.fillRect(barX, barY + 25, barW, barH);
      ctx.fillStyle = '#aa8866';
      ctx.fillRect(barX, barY + 25, barW * state.currentEnergy.asteroid / 100, barH);
      ctx.fillStyle = '#fff';
      ctx.fillText('Astéroïde', barX + barW + 5, barY + 38);
    }

    // Jauge de carburant
    const fuelH = 130, fuelW = 16, fuelX = 668, fuelY = 440;
    
    ctx.fillStyle = 'rgba(0,0,0,0.65)';
    ctx.beginPath();
    ctx.roundRect(fuelX - 6, fuelY - 22, fuelW + 12, fuelH + 42, 5);
    ctx.fill();
    
    ctx.fillStyle = '#1a1a1a';
    ctx.fillRect(fuelX, fuelY, fuelW, fuelH);
    
    const fuelLevel = (state.fuel / 100) * fuelH;
    const fuelGrad = ctx.createLinearGradient(0, fuelY + fuelH - fuelLevel, 0, fuelY + fuelH);
    fuelGrad.addColorStop(0, state.fuel > 20 ? '#00cc66' : '#ff3030');
    fuelGrad.addColorStop(1, state.fuel > 20 ? '#008844' : '#aa0000');
    ctx.fillStyle = fuelGrad;
    ctx.fillRect(fuelX, fuelY + fuelH - fuelLevel, fuelW, fuelLevel);
    
    ctx.fillStyle = '#888';
    ctx.font = '9px sans-serif';
    ctx.textAlign = 'center';
    ctx.fillText('Carburant', fuelX + fuelW/2, fuelY - 8);
    ctx.fillStyle = state.fuel > 20 ? '#8f8' : '#f88';
    ctx.font = 'bold 11px sans-serif';
    ctx.fillText(`${Math.round(state.fuel)}%`, fuelX + fuelW/2, fuelY + fuelH + 16);
    ctx.textAlign = 'left';

  }, [sceneTime]);

  // ============================================================
  // BOUCLE PRINCIPALE
  // ============================================================
  
  const gameLoop = useCallback(() => {
    if (isPlaying) {
      updateSimulation();
      draw();
      setSceneTime(t => t + playbackSpeed);
      animationRef.current = requestAnimationFrame(gameLoop);
    }
  }, [isPlaying, playbackSpeed, updateSimulation, draw]);

  // Transitions de scène
  useEffect(() => {
    const sceneData = getCurrentSceneData();
    if (sceneData && getTimeInSeconds() >= sceneData.duration) {
      const part = videoStructure[currentPart];
      if (currentScene < part.scenes.length - 1) {
        setCurrentScene(s => s + 1);
        setSceneTime(0);
      } else if (currentPart < videoStructure.length - 1) {
        setCurrentPart(p => p + 1);
        setCurrentScene(0);
        setSceneTime(0);
      } else {
        setIsPlaying(false);
      }
    }
  }, [sceneTime, currentPart, currentScene]);

  useEffect(() => {
    const sceneData = getCurrentSceneData();
    if (sceneData) initScene(sceneData.setup);
  }, [currentPart, currentScene, initScene]);

  useEffect(() => { draw(); }, [draw]);

  useEffect(() => {
    if (isPlaying) {
      animationRef.current = requestAnimationFrame(gameLoop);
    }
    return () => { if (animationRef.current) cancelAnimationFrame(animationRef.current); };
  }, [isPlaying, gameLoop]);

  const togglePlay = () => {
    const sceneData = getCurrentSceneData();
    if (!isPlaying && currentPart >= videoStructure.length - 1 && 
        currentScene >= videoStructure[videoStructure.length - 1].scenes.length - 1 &&
        sceneData && getTimeInSeconds() >= sceneData.duration) {
      setCurrentPart(0);
      setCurrentScene(0);
      setSceneTime(0);
    }
    setIsPlaying(!isPlaying);
  };

  const goToScene = (partIndex, sceneIndex) => {
    setCurrentPart(partIndex);
    setCurrentScene(sceneIndex);
    setSceneTime(0);
    setIsPlaying(false);
  };

  const sceneData = getCurrentSceneData();
  const subtitle = getCurrentSubtitle();
  const showEq = shouldShowEquation();

  return (
    <div className="flex flex-col items-center bg-gray-950 min-h-screen p-3" style={{ fontFamily: 'system-ui, sans-serif' }}>
      
      {/* Header */}
      <div className="w-full max-w-4xl mb-2">
        <h1 className="text-base font-bold text-white text-center">
          Évitement optimal dans un champ d'astéroïdes
        </h1>
        <div className="flex justify-center items-center gap-3 mt-1">
          <span className="text-cyan-400 text-xs font-medium px-2 py-0.5 bg-cyan-900/40 rounded">
            {currentPart + 1}. {videoStructure[currentPart]?.title}
          </span>
          <span className="text-gray-500 text-xs">
            {formatTime(getCurrentTotalTime())} / {formatTime(getTotalDuration())}
          </span>
        </div>
      </div>

      {/* Zone vidéo */}
      <div className="relative rounded-lg overflow-hidden shadow-2xl border border-gray-800" style={{ width: 700, height: 600 }}>
        <canvas ref={canvasRef} width={700} height={600} className="block" />

        {/* Sous-titre */}
        {subtitle && (
          <div className="absolute bottom-28 left-6 right-6">
            <div 
              className="text-white text-lg text-center leading-relaxed px-5 py-3 rounded-lg"
              style={{
                background: 'rgba(0,0,0,0.85)',
                backdropFilter: 'blur(6px)',
                textShadow: '0 1px 3px rgba(0,0,0,0.9)'
              }}
            >
              {subtitle.text}
            </div>
          </div>
        )}

        {/* Équation */}
        {showEq && sceneData?.equation && (
          <div 
            className="absolute top-16 left-5 right-5 p-3 rounded-lg"
            style={{
              background: 'linear-gradient(135deg, rgba(0,20,45,0.94) 0%, rgba(0,45,65,0.94) 100%)',
              border: '1px solid rgba(0,160,220,0.4)',
              boxShadow: '0 0 25px rgba(0,100,180,0.25)'
            }}
          >
            <div className="text-cyan-300 text-xs font-semibold mb-1.5 tracking-wider uppercase">
              {sceneData.equation.label}
            </div>
            <div 
              className="text-white text-2xl font-mono text-center"
              style={{ textShadow: '0 0 18px rgba(0,180,255,0.45)' }}
            >
              {sceneData.equation.text}
            </div>
          </div>
        )}

        {/* Timeline de scène */}
        <div className="absolute bottom-3 left-4 right-4">
          <div className="flex justify-between text-gray-500 text-xs mb-1 px-0.5">
            <span>{formatTime(getTimeInSeconds())}</span>
            <span className="text-gray-600">{sceneData?.id}</span>
            <span>{formatTime(sceneData?.duration || 0)}</span>
          </div>
          <div className="h-1.5 bg-gray-800 rounded-full overflow-hidden">
            <div 
              className="h-full bg-gradient-to-r from-cyan-500 to-blue-500 transition-all duration-75"
              style={{ width: `${(getTimeInSeconds() / (sceneData?.duration || 1)) * 100}%` }}
            />
          </div>
        </div>

        {/* Indicateurs de partie */}
        <div className="absolute top-3 right-3 space-y-1">
          {videoStructure.map((part, i) => (
            <div key={i} className="flex gap-0.5 justify-end">
              {part.scenes.map((_, j) => (
                <div
                  key={j}
                  onClick={() => goToScene(i, j)}
                  className={`w-2 h-2 rounded-full cursor-pointer transition-all hover:scale-125 ${
                    i < currentPart || (i === currentPart && j < currentScene)
                      ? 'bg-cyan-500' 
                      : i === currentPart && j === currentScene
                        ? 'bg-white ring-1 ring-cyan-400'
                        : 'bg-gray-700 hover:bg-gray-600'
                  }`}
                  title={`${i+1}.${j+1}`}
                />
              ))}
            </div>
          ))}
        </div>
      </div>

      {/* Contrôles */}
      <div className="flex items-center gap-2 mt-3">
        <button
          onClick={() => { setCurrentPart(0); setCurrentScene(0); setSceneTime(0); setIsPlaying(false); }}
          className="p-2 rounded bg-gray-800 text-white hover:bg-gray-700 transition text-sm"
        >⏮</button>
        
        <button
          onClick={() => {
            if (currentScene > 0) {
              setCurrentScene(s => s - 1);
            } else if (currentPart > 0) {
              setCurrentPart(p => p - 1);
              setCurrentScene(videoStructure[currentPart - 1].scenes.length - 1);
            }
            setSceneTime(0);
          }}
          className="p-2 rounded bg-gray-800 text-white hover:bg-gray-700 transition text-sm"
        >⏪</button>
        
        <button
          onClick={togglePlay}
          className="px-8 py-2.5 rounded-lg font-bold transition-all shadow-lg"
          style={{
            background: isPlaying 
              ? 'linear-gradient(135deg, #e83030 0%, #a00 100%)'
              : 'linear-gradient(135deg, #00bbff 0%, #0080cc 100%)',
            color: 'white'
          }}
        >
          {isPlaying ? '⏸ Pause' : '▶ Lecture'}
        </button>

        <button
          onClick={() => {
            const part = videoStructure[currentPart];
            if (currentScene < part.scenes.length - 1) {
              setCurrentScene(s => s + 1);
            } else if (currentPart < videoStructure.length - 1) {
              setCurrentPart(p => p + 1);
              setCurrentScene(0);
            }
            setSceneTime(0);
          }}
          className="p-2 rounded bg-gray-800 text-white hover:bg-gray-700 transition text-sm"
        >⏩</button>

        <div className="flex items-center gap-1.5 ml-3 text-gray-400 text-xs">
          <span>Vitesse:</span>
          {[0.5, 1, 1.5, 2].map(speed => (
            <button
              key={speed}
              onClick={() => setPlaybackSpeed(speed)}
              className={`px-1.5 py-0.5 rounded text-xs transition ${
                playbackSpeed === speed ? 'bg-cyan-600 text-white' : 'bg-gray-800 hover:bg-gray-700'
              }`}
            >
              {speed}x
            </button>
          ))}
        </div>
      </div>

      {/* Chapitres */}
      <div className="mt-3 w-full max-w-4xl">
        <div className="flex flex-wrap justify-center gap-1.5">
          {videoStructure.map((part, i) => (
            <button
              key={i}
              onClick={() => goToScene(i, 0)}
              className={`px-2 py-1 rounded text-xs transition ${
                i === currentPart 
                  ? 'bg-cyan-600 text-white shadow-lg' 
                  : i < currentPart
                    ? 'bg-gray-700 text-gray-400'
                    : 'bg-gray-800 text-gray-500 hover:bg-gray-700'
              }`}
            >
              {i}. {part.title}
            </button>
          ))}
        </div>
      </div>

      {/* Légende */}
      <div className="mt-3 flex flex-wrap justify-center gap-x-4 gap-y-1 text-xs text-gray-500">
        <span className="flex items-center gap-1"><span className="w-2.5 h-2.5 rounded bg-blue-500"></span>Vaisseau</span>
        <span className="flex items-center gap-1"><span className="w-2.5 h-2.5 rounded bg-red-500"></span>Missiles</span>
        <span className="flex items-center gap-1"><span className="w-2.5 h-2.5 rounded-full bg-gray-500"></span>Astéroïdes</span>
        <span className="flex items-center gap-1"><span className="w-2.5 h-0.5 bg-cyan-400"></span>Poussée F</span>
        <span className="flex items-center gap-1"><span className="w-2.5 h-0.5 bg-orange-400"></span>Gravité</span>
        <span className="flex items-center gap-1"><span className="w-2.5 border-t border-dashed border-red-400"></span>Ligne de visée</span>
        <span className="flex items-center gap-1"><span className="w-2.5 h-2.5 rounded border border-dashed border-red-400 bg-red-500/20"></span>Zone interdite</span>
      </div>

      {/* Script voix off */}
      <details className="mt-4 text-gray-500 text-xs w-full max-w-3xl">
        <summary className="cursor-pointer hover:text-gray-300 text-center">📝 Script complet pour voix off ({formatTime(getTotalDuration())})</summary>
        <div className="mt-2 bg-gray-900 p-3 rounded-lg text-gray-300 text-xs leading-relaxed max-h-72 overflow-y-auto">
          {videoStructure.map((part, pi) => (
            <div key={pi} className="mb-4">
              <div className="text-cyan-400 font-bold mb-1 text-sm">{pi}. {part.title}</div>
              {part.scenes.map((scene, si) => (
                <div key={si} className="mb-2 pl-3 border-l border-gray-700">
                  <div className="text-gray-500 mb-0.5">Scène {scene.id} ({scene.duration}s)</div>
                  {scene.subtitles.map((sub, i) => (
                    <div key={i} className="mb-0.5">
                      <span className="text-gray-600 mr-1">[{sub.start}s→{sub.end}s]</span>
                      <span className="text-gray-300">{sub.text}</span>
                    </div>
                  ))}
                  {scene.equation && (
                    <div className="text-cyan-600 mt-1">📐 Équation à {scene.equation.appearAt}s : {scene.equation.text}</div>
                  )}
                </div>
              ))}
            </div>
          ))}
        </div>
      </details>
    </div>
  );
};

export default SpaceEvasionComplete;
