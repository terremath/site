(function() {
  const STORAGE_KEY = 'tmLang';
  const LANGS = ['fr', 'en'];

  const en = {
    'Obayda Assaad - Terre Mathématiques': 'Obayda Assaad - Terre Mathematics',
    'Terre Mathématiques': 'Terre Mathematics',
    'Terre': 'Terre',
    'Mathématiques': 'Mathematics',
    'Accueil': 'Home',
    'Terre Mathématiques ▾': 'Terre Mathematics ▾',
    'Ma philosophie': 'My Philosophy',
    'Ma méthode': 'My Method',
    'Qui suis-je ?': 'About',
    'Recherche': 'Research',
    'Contact': 'Contact',
    'Formations': 'Programs',
    'Réserver un appel': 'Book a Call',
    'Mentions légales': 'Legal Notice',
    'Confidentialité': 'Privacy',
    'Cookies': 'Cookies',
    'CGV': 'Terms of Sale',
    'Tous droits réservés.': 'All rights reserved.',
    'Excellence & Grandes Écoles': 'Excellence & Top Schools',
    'Choix de la langue': 'Language selection',

    'Chercheur en probabilités': 'Researcher in Probability',
    'Obayda Assaad': 'Obayda Assaad',
    'Docteur en mathématiques': 'PhD in Mathematics',
    'Recherche en probabilités, équations stochastiques et analyse fine des phénomènes aléatoires.': 'Research in probability, stochastic equations, and the fine analysis of random phenomena.',
    'Découvrir son parcours': 'Discover His Path',
    'Google Scholar ↗': 'Google Scholar ↗',
    'TESTE-TOI': 'TEST YOURSELF',
    'QCM original et créatif': 'An original and creative quiz',
    'Commencer le test →': 'Start the quiz →',
    'Test gratuit · Sans inscription': 'Free quiz · No sign-up',
    'Teste-toi en maths et en physique': 'Test Yourself in Math and Physics',
    '21 questions folles pour un petit génie…': '21 wild questions for a sharp mind...',
    'Non merci, pas maintenant': 'No thanks, not now',
    'Nouvel article · arXiv math.PR': 'New Paper · arXiv math.PR',
    'Soumis le 12 août 2026': 'Submitted on August 12, 2026',
    'Primitive-Fock Classification and Hilbert-Stein Extraction : une contribution récente autour des limites faibles du chaos de Wiener et des structures de Fock associées.': 'Primitive-Fock Classification and Hilbert-Stein Extraction: a recent contribution on weak limits of Wiener chaos and the associated Fock structures.',
    'Lire sur arXiv →': 'Read on arXiv →',
    'Plus tard': 'Later',
    'Articles scientifiques': 'Scientific Articles',
    "Une sélection de travaux autour des processus stochastiques, des équations aux dérivées partielles stochastiques, de l'estimation de paramètres et des approximations normales quantitatives.": 'A selection of works on stochastic processes, stochastic partial differential equations, parameter estimation, and quantitative normal approximations.',
    'Lire sur arXiv': 'Read on arXiv',

    'Recherche - Obayda Assaad': 'Research - Obayda Assaad',
    'Probabilités, chaos de Wiener et équations stochastiques': 'Probability, Wiener Chaos, and Stochastic Equations',
    'Probabilités, chaos et équations stochastiques': 'Probability, Chaos, and Stochastic Equations',
    'Probabilités, chaos et': 'Probability, Chaos, and',
    'équations stochastiques': 'Stochastic Equations',
    'Mes travaux portent sur l’analyse fine des phénomènes aléatoires : processus non gaussiens, chaos de Wiener, équations aux dérivées partielles stochastiques, estimation de paramètres et théorèmes limites quantitatifs.': 'My work focuses on the fine analysis of random phenomena: non-Gaussian processes, Wiener chaos, stochastic partial differential equations, parameter estimation, and quantitative limit theorems.',
    "Mes travaux portent sur l'analyse fine des phénomènes aléatoires : processus non gaussiens, chaos de Wiener, équations aux dérivées partielles stochastiques, estimation de paramètres et théorèmes limites quantitatifs.": 'My work focuses on the fine analysis of random phenomena: non-Gaussian processes, Wiener chaos, stochastic partial differential equations, parameter estimation, and quantitative limit theorems.',
    'Un espace consacré aux objets aléatoires, aux limites faibles, aux équations stochastiques et aux structures analytiques qui permettent de comprendre leur géométrie profonde.': 'A space devoted to random objects, weak limits, stochastic equations, and the analytic structures that reveal their deeper geometry.',
    'Domaine de recherche': 'Research Area',
    'Domaine': 'Field',
    "Comprendre ce que l'aléatoire laisse voir": 'Understanding What Randomness Lets Us See',
    "Un même fil traverse ces travaux : extraire une structure mesurable à partir d'objets aléatoires complexes. Les trajectoires, variations, moyennes spatiales et projections de chaos deviennent alors des outils pour identifier des paramètres, décrire des limites et mesurer la part gaussienne cachée dans un système.": 'A single thread runs through these works: extracting measurable structure from complex random objects. Paths, variations, spatial averages, and chaos projections then become tools for identifying parameters, describing limits, and measuring the hidden Gaussian component of a system.',
    "Le travail d'Obayda Assaad se situe à l'intersection des probabilités modernes, de l'analyse stochastique et des équations aux dérivées partielles aléatoires.": "Obayda Assaad's work lies at the intersection of modern probability, stochastic analysis, and random partial differential equations.",
    'Axes principaux': 'Main Directions',
    'Processus stochastiques et mémoire longue': 'Stochastic Processes and Long Memory',
    "Étude de processus fractionnaires ou hermitiens, souvent non gaussiens, où la dépendance à long terme modifie profondément les méthodes classiques d'estimation et de convergence.": 'Study of fractional or Hermitian processes, often non-Gaussian, where long-range dependence deeply changes classical estimation and convergence methods.',
    'EDP stochastiques': 'Stochastic PDEs',
    "Analyse d'équations de Burgers, de la chaleur ou des ondes perturbées par du bruit, avec un intérêt particulier pour les variations, les moyennes spatiales et les paramètres de dérive.": 'Analysis of Burgers, heat, or wave equations perturbed by noise, with special attention to variations, spatial averages, and drift parameters.',
    'Chaos de Wiener et limites faibles': 'Wiener Chaos and Weak Limits',
    "Comprendre comment des objets aléatoires complexes convergent vers des lois limites, et quelles structures cachées gouvernent cette convergence.": 'Understanding how complex random objects converge toward limiting laws, and which hidden structures govern that convergence.',
    'Classification des limites, décomposition des composantes primitives et extraction de facteurs gaussiens dans des suites de variables vivant dans des chaos de Wiener.': 'Classification of limits, decomposition of primitive components, and extraction of Gaussian factors in sequences of variables living in Wiener chaoses.',
    'Équations stochastiques': 'Stochastic Equations',
    "Analyse d'équations d'évolution soumises à des bruits irréguliers : chaleur, onde, Burgers, phénomènes fractionnaires et bruit blanc.": 'Analysis of evolution equations driven by irregular noises: heat, wave, Burgers, fractional phenomena, and white noise.',
    'Estimation de paramètres': 'Parameter Estimation',
    'Développer des méthodes statistiques pour identifier les paramètres de modèles aléatoires à mémoire longue ou à régularité faible.': 'Developing statistical methods to identify parameters in random models with long memory or low regularity.',
    'Travaux en préparation': 'Work in Preparation',
    'Deux prochains axes à formaliser': 'Two Next Directions to Formalize',
    "Cette zone prépare l'arrivée des deux prochains articles. Chaque bloc contient déjà sa place pour le titre définitif, l'abstract en français et une simulation associée. Les visuels actuels sont des canevas de travail.": 'This area prepares the arrival of the next two papers. Each block already contains space for the final title, the abstract in French, and an associated simulation. The current visuals are working drafts.',
    "Deux chantiers sont préparés ici comme des espaces vivants : titre, résumé, simulation, puis intégration dans une vision géométrique plus globale.": 'Two projects are being prepared here as living spaces: title, abstract, simulation, then integration into a broader geometric vision.',
    'Torelli · brouillon': 'Torelli · Draft',
    'Hermite · brouillon': 'Hermite · Draft',
    'Titre à préciser': 'Title to Be Specified',
    "Préparer une géométrie globale à partir d'invariants analytiques : périodes, signatures reconstructives, formes primitives et passage d'un objet local à une reconstruction globale.": 'Preparing a global geometry from analytic invariants: periods, reconstructive signatures, primitive forms, and the passage from a local object to a global reconstruction.',
    'Préparer le terrain autour des processus hermitiens : mémoire longue, transformations de Hermite, non-gaussianité, variations et estimation de paramètres.': 'Preparing the ground around Hermitian processes: long memory, Hermite transformations, non-Gaussianity, variations, and parameter estimation.',
    'Titre : à préciser.': 'Title: to be specified.',
    'Titre :': 'Title:',
    'Titre : ': 'Title:',
    'Abstract :': 'Abstract:',
    'Abstract : ': 'Abstract:',
    'Simulation :': 'Simulation:',
    'Simulation : ': 'Simulation:',
    'à remplacer par le titre officiel.': 'to be replaced by the official title.',
    'à intégrer dès que le résumé sera stabilisé.': 'to be inserted as soon as the abstract is stabilized.',
    'Abstract : zone préparée pour le résumé scientifique.': 'Abstract: space prepared for the scientific abstract.',
    "Simulation : canevas provisoire autour d'une géométrie de type Torelli.": 'Simulation: provisional framework around a Torelli-type geometry.',
    'Simulation : canevas provisoire autour des structures hermitiennes et non gaussiennes.': 'Simulation: provisional framework around Hermitian and non-Gaussian structures.',
    "canevas provisoire autour d'une géométrie de type Torelli.": 'provisional framework around a Torelli-type geometry.',
    'canevas provisoire autour de chaos hermitiens.': 'provisional framework around Hermitian chaoses.',
    'Publications': 'Publications',
    'Résumé': 'Abstract',
    'Chaque article peut être ouvert pour lire un résumé en français et accéder à la source officielle.': 'Each paper can be opened to read an abstract and access the official source.',
    'Résumé à enrichir à partir de la version définitive de l’article.': 'Abstract to be enriched from the final version of the article.',
    'Voir la source': 'View Source',
    'Voir la publication': 'View Publication',
    'Lire le résumé': 'Read Abstract',
    "L'article caractérise les limites faibles de vecteurs bornés dans un chaos de Wiener fixe lorsque les espaces de Hilbert gaussiens peuvent varier. Il décrit une classification par polynômes de Wiener pondérés, construit une extraction positive de type Hilbert-Stein et relie les projections primitives à la part gaussienne indépendante détectable par contractions.": 'The paper characterizes weak limits of bounded vectors in a fixed Wiener chaos when the underlying Gaussian Hilbert spaces may vary. It gives a classification by weighted Wiener polynomials, constructs a positive Hilbert-Stein type extraction, and connects primitive projections with the independent Gaussian part detected by contractions.',
    "Le travail utilise l'analyse sur les chaos de Wiener pour étudier les variations quadratiques du processus d'Ornstein-Uhlenbeck hermitien, défini comme solution d'une équation de Langevin conduite par un processus d'Hermite. Ces résultats servent ensuite à identifier le paramètre de Hurst du modèle.": 'This work uses analysis on Wiener chaoses to study the quadratic variations of the Hermite Ornstein-Uhlenbeck process, defined as the solution of a Langevin equation driven by a Hermite process. These results are then used to identify the Hurst parameter of the model.',
    "L'article analyse la solution de l'équation de Burgers stochastique avec bruit blanc espace-temps additif. La solution est décomposée en une partie liée à l'équation de la chaleur stochastique et une partie plus régulière, puis cette structure est exploitée pour estimer le paramètre de dérive à partir de variations en temps et en espace.": 'The paper analyzes the solution of the stochastic Burgers equation with additive space-time white noise. The solution is decomposed into a component related to the stochastic heat equation and a more regular component, and this structure is used to estimate the drift parameter from temporal and spatial variations.',
    "À l'aide du calcul de Malliavin, l'article étudie le comportement limite des variations par ondelettes associées à une équation des ondes stochastique. Il propose un estimateur par ondelettes du paramètre de Hurst et établit ses propriétés asymptotiques.": 'Using Malliavin calculus, the paper studies the limiting behavior of wavelet variations associated with a stochastic wave equation. It proposes a wavelet estimator for the Hurst parameter and establishes its asymptotic properties.',
    "Ce travail établit un théorème central limite quantitatif pour l'équation de la chaleur fractionnaire stochastique avec bruit gaussien multiplicatif. Les moyennes spatiales, correctement renormalisées, convergent vers une limite gaussienne en distance de variation totale, avec une version fonctionnelle du résultat.": 'This work establishes a quantitative central limit theorem for the stochastic fractional heat equation with multiplicative Gaussian noise. Properly normalized spatial averages converge to a Gaussian limit in total variation distance, with a functional version of the result.',
    "L'article étudie les variations quadratiques, en temps et en espace, de la solution de l'équation des ondes stochastique conduite par un bruit blanc espace-temps. Après renormalisation, ces variations satisfont un théorème central limite et permettent de construire des estimateurs pour le paramètre de dérive.": 'The paper studies temporal and spatial quadratic variations of the solution to the stochastic wave equation driven by space-time white noise. After renormalization, these variations satisfy a central limit theorem and make it possible to construct estimators for the drift parameter.',
    "Le texte étudie des propriétés du processus d'Hermite généralisé, un processus auto-similaire non gaussien. Il définit une intégrale de Wiener associée à ce processus, puis l'utilise pour construire et analyser un processus d'Ornstein-Uhlenbeck non gaussien et rugueux.": 'The paper studies properties of the generalized Hermite process, a non-Gaussian self-similar process. It defines a Wiener integral associated with this process, then uses it to construct and analyze a rough non-Gaussian Ornstein-Uhlenbeck process.',

    'Ma': 'My',
    'méthode': 'method',
    'Que signifie Terre Mathématiques ?': 'What Does Terre Mathematics Mean?',
    "Mon travail consiste à semer une graine : l'essence de l'art de la connaissance.": 'My work consists in planting a seed: the essence of the art of knowledge.',
    "Cette graine, une fois plantée, permet de faire grandir un arbre : l'arbre des idées.": 'Once planted, that seed allows a tree to grow: the tree of ideas.',
    'Sur cet arbre': 'On this tree',
    'chaque branche correspond à un concept, chaque lien à un raisonnement, chaque fruit à une possibilité.': 'each branch corresponds to a concept, each link to a line of reasoning, each fruit to a possibility.',
    "Mon rôle n'est pas de choisir le fruit à votre place, mais de vous donner les moyens de vous déplacer librement dans cet arbre, d'en comprendre la structure et de choisir, en conscience, ce que vous souhaitez explorer et récolter.": 'My role is not to choose the fruit for you, but to give you the means to move freely through this tree, understand its structure, and consciously choose what you wish to explore and harvest.',

    'philosophie': 'philosophy',
    "Du baccalauréat à la thèse, il ne s'agit pas seulement de réussir. Il s'agit d'apprendre à penser.": 'From the baccalaureate to the PhD, the point is not only to succeed. It is to learn how to think.',
    "Du baccalauréat à la thèse, il ne s'agit pas seulement de réussir.": 'From the baccalaureate to the PhD, the point is not only to succeed.',
    "Il s'agit d'apprendre à penser.": 'It is to learn how to think.',
    'Penser avec rigueur. Penser avec autonomie. Penser au-delà des formules.': 'To think with rigor. To think independently. To think beyond formulas.',
    'Penser avec rigueur.': 'To think with rigor.',
    'Penser avec autonomie.': 'To think independently.',
    'Penser au-delà des formules.': 'To think beyond formulas.',
    "Mon travail n'est pas simplement de transmettre un cours, mais de former des esprits capables de comprendre la structure profonde des raisonnements, de relier les idées entre elles, et d'en voir les prolongements réels : en physique, en robotique, en IA, en finance.": 'My work is not simply to deliver a course, but to train minds capable of understanding the deep structure of arguments, connecting ideas, and seeing their real extensions in physics, robotics, AI, and finance.',
    'Car la vérité est simple : 95 % des idées mathématiques sont les mêmes, à tous les niveaux. Mais presque personne ne vous apprend à les reconnaître.': 'Because the truth is simple: 95% of mathematical ideas are the same at every level. But almost no one teaches you how to recognize them.',
    "Ici, c'est précisément ce que vous apprendrez.": 'Here, this is precisely what you will learn.',

    'Qui suis-je': 'Who am I',
    'Enseignant, chercheur, passeur.': 'Teacher, researcher, bridge-builder.',
    "Je forme des élèves et des étudiants, du lycée jusqu'à l'université, mais aussi des amatéurs adultes en quête scientifique, autour d'une conviction simple : les mathématiques ne sont pas une accumulation de formules. Elles constituent un langage cohérent, intelligible par lui-même, dont les raisonnements fondamentaux sont souvent plus simples, plus logiques et plus profonds qu'on ne l'imagine.": 'I train pupils and students, from high school to university, as well as adult learners driven by scientific curiosity, around a simple conviction: mathematics is not an accumulation of formulas. It is a coherent language, intelligible in itself, whose fundamental arguments are often simpler, more logical, and deeper than one imagines.',
    "Mon travail ne consiste pas seulement à transmettre un programme ou à préparer une échéance. Il consiste à former l'esprit : apprendre à raisonner, à structurer une pensée, à comprendre pourquoi une idée fonctionne, comment elle s'inscrit dans un ensemble plus vaste, et comment elle retrouve sa fécondité dans d'autres domaines.": 'My work is not only to teach a syllabus or prepare a deadline. It is to train the mind: learning to reason, structure thought, understand why an idea works, how it belongs to a wider whole, and how it becomes fruitful again in other domains.',
    "Ce que je fais en recherche nourrit directement ce que j'enseigne. Ainsi, certains de mes élèves découvrent différentes géométries dès le collège, à travers des exemples concrets, pratiques et rigoureux. D'autres rencontrent, bien avant les études supérieures, des applications techniques que l'on imagine souvent hors de portée à leur âge : la cryptographie, la relativité, la théorie des ensembles.": 'What I do in research directly nourishes what I teach. Some of my students encounter different geometries as early as middle school through concrete, practical, and rigorous examples. Others meet, long before higher education, technical applications often thought out of reach at their age: cryptography, relativity, set theory.',
    'Non pour impressionner, ni pour compliquer, mais pour éclairer autrement les notions du programme, en révéler la structure, et montrer que les mathématiques parlent déjà du réel.': 'Not to impress or complicate, but to illuminate the curriculum differently, reveal its structure, and show that mathematics already speaks about reality.',
    'Ma conviction': 'My Conviction',
    "On n'échoue pas en mathématiques par manque d'intelligence. On échoue le plus souvent parce qu'on n'a jamais appris à en comprendre le langage.": 'People do not fail at mathematics for lack of intelligence. Most often, they fail because they were never taught to understand its language.',
    "On apprend trop souvent à appliquer des formules, des techniques, des recettes, sans jamais accéder aux idées qui les rendent nécessaires. Or ce sont précisément ces idées qui donnent de la clarté, de l'autonomie et de la puissance.": 'Too often, one learns to apply formulas, techniques, and recipes without ever reaching the ideas that make them necessary. Yet precisely those ideas give clarity, autonomy, and power.',
    'Mon rôle': 'My Role',
    'Former l’esprit, et pas seulement préparer une échéance.': 'Training the mind, not merely preparing for a deadline.',
    "J'accompagne celles et ceux qui veulent comprendre en profondeur, progresser avec exigence, et réussir par surcroît — à travers une véritable formation, un suivi individuel, et une manière de penser qui dépasse largement le cadre d'un simple cours.": 'I support those who want to understand deeply, progress with high standards, and succeed as a consequence, through genuine training, individual guidance, and a way of thinking that goes far beyond a simple lesson.',
    'Accéder à mes articles': 'Access My Articles',

    'Contact — TerreMathématiques': 'Contact — Terre Mathematics',
    'Contact': 'Contact',
    'Écris-moi': 'Write to Me',
    "Une question, un projet, une demande d'accompagnement ou de collaboration scientifique ?": 'A question, a project, a request for guidance, or a scientific collaboration?',
    'Envoyer un message': 'Send a Message',
    'Prénom': 'First Name',
    'Nom': 'Last Name',
    'Email': 'Email',
    'Sujet': 'Subject',
    'Message': 'Message',
    'Envoyer': 'Send',
    'Informations': 'Information',
    'Ton prénom': 'Your first name',
    'Ton adresse email': 'Your email address',

    'Newsletter': 'Newsletter',
    'Reçois mes conseils maths': 'Receive My Math Notes',
    'Méthodes, exercices et stratégies pour progresser — directement dans ta boîte mail. Tu seras aussi notifié(e) en avant-première à chaque nouvelle formation.': 'Methods, exercises, and strategies to make progress, delivered directly to your inbox. You will also be notified first whenever a new program launches.',
    "S'inscrire →": 'Subscribe →',
    'Pas de spam. Désinscription en un clic à tout moment.': 'No spam. Unsubscribe in one click at any time.',

    'Bientôt disponible': 'Coming Soon',
    'Cette page est en cours de préparation.': 'This page is being prepared.',
    'Retour à l’accueil': 'Back to Home',
    "Retour à l'accueil": 'Back to Home',
    "← Retour à l'accueil": '← Back to Home',
    'Découvrir →': 'Discover →',
    'Voir toutes les formations →': 'View All Programs →',
    'Résultats': 'Results',
    'Tes résultats — Terre Mathématiques': 'Your Results — Terre Mathematics',
    'QCM Terre Mathématiques — Es-tu fait pour les maths ?': 'Terre Mathematics Quiz — Are You Made for Math?',
    'Précédente': 'Previous',
    'Suivante →': 'Next →',
    '← Précédente': '← Previous',
    'Recevoir ma correction →': 'Receive My Correction →',
    'Formations - TerreMathématiques': 'Programs - Terre Mathematics',
    'Apprendre à penser, pas seulement à calculer.': 'Learn to Think, Not Merely to Calculate.',
    'Apprendre à penser,': 'Learn to Think,',
    'pas seulement à calculer.': 'Not Merely to Calculate.',
    'Formation Bac Éclair': 'Bac Éclair Program',
    'Formation Élite': 'Elite Program',
    'Formation à venir — TerreMathématiques': 'Upcoming Program — Terre Mathematics',
    'La formation arrive bientôt.': 'The Program Is Coming Soon.',
    'La formation arrive': 'The Program Is Coming',
    'bientôt.': 'Soon.',
    'Être averti·e — La Formation · Terre Mathématique': 'Get Notified — The Program · Terre Mathematics',
    'Je veux être averti': 'Notify Me',
    'Rester connecté': 'Stay Connected',
    'TerreMathématique - Vers les Profondeurs': 'Terre Mathematics - Toward the Depths',
    'Vers les Profondeurs': 'Toward the Depths',
    'Comprendre, pas mémoriser': 'Understand, Do Not Memorize',
    'Sept arcs vers la maîtrise': 'Seven Arcs Toward Mastery',
    "Une pédagogie d'architecte": "An Architect's Pedagogy",
    'Une bibliothèque personnelle': 'A Personal Library',
    'À la fin de ce parcours, vous ne regarderez plus le monde de la même façon': 'At the End of This Path, You Will No Longer See the World the Same Way',
    'Terre Mathématiques - Bac Éclair': 'Terre Mathematics - Bac Éclair',
    'Nos vidéos': 'Our Videos',
    'Tu travailles. Mais les notes ne suivent pas.': 'You Work. But the Grades Do Not Follow.',
    'Tu travailles.': 'You Work.',
    'Mais les notes ne suivent pas.': 'But the Grades Do Not Follow.',
    'Une formation qui avance avec toi.': 'A Program That Moves With You.',
    'Une formation': 'A Program',
    'qui avance avec toi.': 'That Moves With You.',
    'Deux formules': 'Two Plans',
    'Rejoindre le programme': 'Join the Program',
    'Rejoindre Bac Éclair': 'Join Bac Éclair',
    'Rejoindre Terre Mathématiques': 'Join Terre Mathematics',
    'Précédent': 'Previous',
    'Suivant': 'Next',
    'Mentions Légales - Terre Mathématiques': 'Legal Notice - Terre Mathematics',
    'Mentions Légales': 'Legal Notice',
    '1. Éditeur du site': '1. Site Publisher',
    '2. Directeur de la publication': '2. Publication Director',
    '3. Hébergeur du site': '3. Hosting Provider',
    '4. Propriété intellectuelle': '4. Intellectual Property',
    '5. Limitation de responsabilité': '5. Limitation of Liability',
    '6. Liens hypertextes': '6. Hyperlinks',
    '7. Droit applicable': '7. Applicable Law',
    'Politique de Confidentialité — Terre Mathématiques': 'Privacy Policy — Terre Mathematics',
    'Politique de Confidentialité': 'Privacy Policy',
    '1. Responsable du traitement': '1. Data Controller',
    '2. Données collectées': '2. Data Collected',
    '3. Finalités du traitement': '3. Purposes of Processing',
    '4. Destinataires des données': '4. Data Recipients',
    '5. Durée de conservation': '5. Retention Period',
    '6. Vos droits': '6. Your Rights',
    '7. Sécurité des données': '7. Data Security',
    '8. Transfert de données hors UE': '8. Data Transfer Outside the EU',
    '9. Modification de la politique': '9. Changes to This Policy',
    'Politique de Cookies - Terre Mathématiques': 'Cookie Policy - Terre Mathematics',
    'Politique de Cookies': 'Cookie Policy',
    "1. Qu'est-ce qu'un cookie ?": '1. What Is a Cookie?',
    '2. Les cookies que nous utilisons': '2. Cookies We Use',
    '3. Durée de conservation des cookies': '3. Cookie Retention Period',
    '4. Votre consentement': '4. Your Consent',
    '5. Comment gérer les cookies ?': '5. How to Manage Cookies?',
    '6. Cookies tiers': '6. Third-Party Cookies',
    '7. Modification de la politique de cookies': '7. Changes to the Cookie Policy',
    'Conditions générales de vente': 'Terms and Conditions of Sale',
    'Conditions Générales de Vente - Terre Mathématiques': 'Terms and Conditions of Sale - Terre Mathematics',
    'Conditions Générales de Vente': 'Terms and Conditions of Sale',
    '1. Identification du vendeur': '1. Seller Identification',
    '2. Objet': '2. Purpose',
    '3. Produits et services': '3. Products and Services',
    '4. Prix': '4. Prices',
    '5. Commande': '5. Order',
    '6. Paiement': '6. Payment',
    '7. Droit de rétractation': '7. Right of Withdrawal',
    '8. Durée et résiliation (abonnements)': '8. Duration and Termination (Subscriptions)',
    '9. Livraison des prestations': '9. Delivery of Services',
    '10. Obligations du client': '10. Customer Obligations',
    '11. Responsabilité': '11. Liability',
    '12. Propriété intellectuelle': '12. Intellectual Property',
    '13. Protection des données personnelles': '13. Personal Data Protection',
    '14. Médiation et litiges': '14. Mediation and Disputes',
    '15. Droit applicable': '15. Applicable Law',
    'Politique de confidentialité': 'Privacy Policy',
    'Politique de cookies': 'Cookie Policy'
  };

  const originals = new WeakMap();
  const attrOriginals = new WeakMap();
  let currentLang = LANGS.includes(localStorage.getItem(STORAGE_KEY)) ? localStorage.getItem(STORAGE_KEY) : 'fr';
  let applying = false;
  let queued = false;

  function ensureFloatingSwitch() {
    if (document.querySelector('[data-lang-switch]')) return;
    if (!document.getElementById('tm-floating-lang-style')) {
      const style = document.createElement('style');
      style.id = 'tm-floating-lang-style';
      style.textContent = `
.tm-floating-lang {
  position: fixed;
  top: 16px;
  right: 16px;
  z-index: 10000;
  display: inline-flex;
  gap: 3px;
  padding: 3px;
  border: 1px solid rgba(45,27,51,0.18);
  border-radius: 999px;
  background: rgba(255,255,255,0.82);
  backdrop-filter: blur(10px);
  box-shadow: 0 10px 30px rgba(0,0,0,0.12);
}
.tm-floating-lang button {
  min-width: 34px;
  height: 28px;
  padding: 0 9px;
  border: 0;
  border-radius: 999px;
  background: transparent;
  color: #2D1B33;
  font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
  font-size: 0.72rem;
  font-weight: 800;
  letter-spacing: 0.08em;
  cursor: pointer;
}
.tm-floating-lang button.is-active {
  background: #C9A84C;
  color: #2D1B33;
}`;
      document.head.appendChild(style);
    }
    const switcher = document.createElement('div');
    switcher.className = 'tm-floating-lang';
    switcher.setAttribute('aria-label', 'Choix de la langue');
    switcher.innerHTML = `
      <button type="button" data-lang-switch="fr" class="is-active">FR</button>
      <button type="button" data-lang-switch="en">EN</button>`;
    document.body.appendChild(switcher);
  }

  function normalize(text) {
    return String(text)
      .replace(/\u00a0/g, ' ')
      .replace(/\s+/g, ' ')
      .trim();
  }

  function withOuterWhitespace(original, translated) {
    const before = String(original).match(/^\s*/)[0];
    const after = String(original).match(/\s*$/)[0];
    return before + translated + after;
  }

  function translateString(text, lang) {
    if (lang === 'fr') return text;
    const key = normalize(text);
    if (en[key]) return en[key];
    const noThinSpace = key.replace(/\s+([?!:;])/g, '$1');
    return en[noThinSpace] || text;
  }

  function translateTextNode(node, lang) {
    if (!normalize(node.nodeValue)) return;
    if (!originals.has(node)) originals.set(node, node.nodeValue);
    const original = originals.get(node);
    const translated = translateString(original, lang);
    node.nodeValue = withOuterWhitespace(original, translated);
  }

  function translateAttributes(el, lang) {
    ['placeholder', 'aria-label', 'alt', 'title', 'value'].forEach(attr => {
      if (!el.hasAttribute(attr)) return;
      if (attr === 'value' && !['BUTTON', 'INPUT'].includes(el.tagName)) return;
      let map = attrOriginals.get(el);
      if (!map) {
        map = {};
        attrOriginals.set(el, map);
      }
      if (!map[attr]) map[attr] = el.getAttribute(attr);
      el.setAttribute(attr, translateString(map[attr], lang));
    });
  }

  function shouldSkip(el) {
    return ['SCRIPT', 'STYLE', 'NOSCRIPT', 'CODE', 'PRE', 'TEXTAREA'].includes(el.tagName);
  }

  function apply(root = document.body) {
    if (!root || applying) return;
    applying = true;
    ensureFloatingSwitch();

    document.documentElement.lang = currentLang;
    const originalTitle = document.documentElement.dataset.i18nTitle || document.title;
    document.documentElement.dataset.i18nTitle = originalTitle;
    document.title = translateString(originalTitle, currentLang);

    document.querySelectorAll('[data-lang-switch]').forEach(btn => {
      btn.classList.toggle('is-active', btn.dataset.langSwitch === currentLang);
      btn.setAttribute('aria-pressed', String(btn.dataset.langSwitch === currentLang));
    });

    const start = root.nodeType === Node.ELEMENT_NODE ? root : document.body;
    if (!shouldSkip(start)) {
      if (start.nodeType === Node.ELEMENT_NODE) translateAttributes(start, currentLang);
      const walker = document.createTreeWalker(start, NodeFilter.SHOW_ELEMENT | NodeFilter.SHOW_TEXT, {
        acceptNode(node) {
          if (node.nodeType === Node.ELEMENT_NODE && shouldSkip(node)) return NodeFilter.FILTER_REJECT;
          return NodeFilter.FILTER_ACCEPT;
        }
      });
      let node = walker.currentNode;
      while (node) {
        if (node.nodeType === Node.TEXT_NODE) translateTextNode(node, currentLang);
        if (node.nodeType === Node.ELEMENT_NODE) translateAttributes(node, currentLang);
        node = walker.nextNode();
      }
    }
    applying = false;
  }

  function setLanguage(lang) {
    if (!LANGS.includes(lang)) return;
    currentLang = lang;
    localStorage.setItem(STORAGE_KEY, lang);
    apply();
  }

  document.addEventListener('click', event => {
    const btn = event.target.closest('[data-lang-switch]');
    if (!btn) return;
    setLanguage(btn.dataset.langSwitch);
  });

  document.addEventListener('DOMContentLoaded', () => {
    apply();
    const observer = new MutationObserver(() => {
      if (applying || queued) return;
      queued = true;
      requestAnimationFrame(() => {
        queued = false;
        apply();
      });
    });
    observer.observe(document.body, { childList: true, subtree: true });
  });

  window.TM_I18N = { apply, setLanguage, getLanguage: () => currentLang };
})();
