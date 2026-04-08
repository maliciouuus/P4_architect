#!/usr/bin/env python3
"""Génère le support de présentation DataShare au format PowerPoint."""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.util import Inches, Pt

# Palette DataShare
ORANGE = RGBColor(0xFF, 0x81, 0x2D)
ORANGE_DARK = RGBColor(0xDE, 0x62, 0x62)
DARK = RGBColor(0x1A, 0x1A, 0x1A)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY = RGBColor(0xF5, 0xF5, 0xF5)
GRAY = RGBColor(0x75, 0x75, 0x75)
ACCENT = RGBColor(0xFF, 0xB8, 0x8C)

prs = Presentation()
prs.slide_width = Inches(13.33)
prs.slide_height = Inches(7.5)

BLANK = prs.slide_layouts[6]  # Layout vide


def add_rect(slide, left, top, width, height, color, transparency=0):
    shape = slide.shapes.add_shape(1, Inches(left), Inches(top), Inches(width), Inches(height))
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()
    return shape


def add_text(slide, text, left, top, width, height,
             font_size=18, bold=False, color=DARK,
             align=PP_ALIGN.LEFT, italic=False):
    txBox = slide.shapes.add_textbox(
        Inches(left), Inches(top), Inches(width), Inches(height)
    )
    tf = txBox.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    run = p.add_run()
    run.text = text
    run.font.size = Pt(font_size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.color.rgb = color
    return txBox


def gradient_bg(slide):
    """Fond dégradé simulé avec deux rectangles."""
    add_rect(slide, 0, 0, 13.33, 7.5, ACCENT)
    shape = slide.shapes.add_shape(1, Inches(0), Inches(0), Inches(13.33), Inches(7.5))
    shape.fill.gradient()
    shape.fill.gradient_angle = 90
    stops = shape.fill.gradient_stops
    stops[0].position = 0
    stops[0].color.rgb = RGBColor(0xFF, 0xB8, 0x8C)
    stops[1].position = 1
    stops[1].color.rgb = RGBColor(0xDE, 0x62, 0x62)
    shape.line.fill.background()


def white_card(slide, left, top, width, height):
    shape = slide.shapes.add_shape(1, Inches(left), Inches(top), Inches(width), Inches(height))
    shape.fill.solid()
    shape.fill.fore_color.rgb = WHITE
    shape.line.color.rgb = RGBColor(0xE0, 0xE0, 0xE0)
    shape.line.width = Pt(0.5)
    # Arrondi simulé avec ombre légère
    shadow = shape.shadow
    shadow.inherit = False
    return shape


def bullet_list(slide, items, left, top, width, font_size=13, color=DARK):
    txBox = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(5))
    tf = txBox.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        if i == 0:
            p = tf.paragraphs[0]
        else:
            p = tf.add_paragraph()
        p.space_before = Pt(4)
        run = p.add_run()
        run.text = item
        run.font.size = Pt(font_size)
        run.font.color.rgb = color


# ── SLIDE 1 — Page de garde ───────────────────────────────────────────────────
slide = prs.slides.add_slide(BLANK)
gradient_bg(slide)

# Titre principal
add_text(slide, "DataShare", 1, 1.5, 11, 1.5, font_size=60, bold=True, color=DARK, align=PP_ALIGN.CENTER)
add_rect(slide, 4.5, 3.1, 4.33, 0.06, ORANGE)
add_text(slide, "Plateforme de transfert sécurisé de fichiers", 1, 3.3, 11, 0.8,
         font_size=20, color=DARK, align=PP_ALIGN.CENTER)
add_text(slide, "MVP — Démonstration investisseurs | Avril 2026", 1, 4.2, 11, 0.6,
         font_size=14, color=DARK, align=PP_ALIGN.CENTER, italic=True)
add_text(slide, "Copyright DataShare© 2025", 0.5, 7.0, 12, 0.4,
         font_size=10, color=WHITE, align=PP_ALIGN.CENTER)


# ── SLIDE 2 — Contexte & besoin ───────────────────────────────────────────────
slide = prs.slides.add_slide(BLANK)
gradient_bg(slide)
white_card(slide, 0.5, 0.4, 12.3, 6.6)

add_text(slide, "Le problème métier", 0.8, 0.6, 12, 0.8, font_size=28, bold=True, color=DARK)
add_rect(slide, 0.8, 1.35, 1.5, 0.05, ORANGE)

add_text(slide, "DataShare permet aux freelances et petites entreprises d'envoyer "
         "des fichiers simplement, sans compte email ni FTP, avec un lien sécurisé "
         "à durée limitée.",
         0.8, 1.55, 11.5, 1, font_size=14, color=GRAY)

# 3 colonnes besoin
cols = [
    ("📤", "Envoyer", "Un fichier sans\ninfrastructure complexe"),
    ("🔗", "Partager", "Un lien unique avec\nexpiration automatique"),
    ("🔒", "Contrôler", "Accès par mot de passe\net historique personnel"),
]
for i, (icon, titre, desc) in enumerate(cols):
    x = 0.8 + i * 4.0
    add_rect(slide, x, 2.7, 3.5, 2.5, RGBColor(0xFF, 0xF3, 0xEB))
    add_text(slide, icon, x + 1.2, 2.85, 1, 0.6, font_size=28, align=PP_ALIGN.CENTER)
    add_text(slide, titre, x + 0.1, 3.5, 3.3, 0.5, font_size=16, bold=True,
             color=ORANGE, align=PP_ALIGN.CENTER)
    add_text(slide, desc, x + 0.1, 4.0, 3.3, 0.8, font_size=12, color=GRAY,
             align=PP_ALIGN.CENTER)

add_text(slide, "Périmètre MVP (4 semaines) :", 0.8, 5.4, 11, 0.4, font_size=13, bold=True, color=DARK)
bullet_list(slide,
    ["✅  Création de compte et connexion sécurisée (JWT)",
     "✅  Upload de fichiers jusqu'à 50 Mo avec progression",
     "✅  Lien de partage unique avec expiration configurable (24h / 3j / 1 semaine)",
     "✅  Protection optionnelle par mot de passe  •  Historique et suppression"],
    0.8, 5.8, 11.5, font_size=12, color=DARK)


# ── SLIDE 3 — Choix technologiques ───────────────────────────────────────────
slide = prs.slides.add_slide(BLANK)
gradient_bg(slide)
white_card(slide, 0.5, 0.4, 12.3, 6.6)

add_text(slide, "Choix technologiques", 0.8, 0.6, 12, 0.8, font_size=28, bold=True, color=DARK)
add_rect(slide, 0.8, 1.35, 2, 0.05, ORANGE)

rows = [
    ("Back-end", "Django 5.2 + DRF", "Batteries incluses, ORM robuste, productivité maximale pour un MVP"),
    ("Authentification", "JWT (simplejwt)", "Stateless, compatible SPA, standard API REST"),
    ("Front-end", "Vue.js 3 + Vite", "Composition API puissante, Pinia natif, écosystème cohérent"),
    ("Base de données", "PostgreSQL 16", "UUID natif, standard professionnel, robustesse"),
    ("Stockage", "Disque local", "Suffisant pour le prototype — migration S3 prévue en prod"),
    ("Infrastructure", "Docker Compose", "Reproductibilité totale, installation en 1 commande"),
]

headers = ["Composant", "Technologie", "Justification"]
col_w = [2.5, 2.5, 6.8]
col_x = [0.7, 3.2, 5.7]

# En-têtes
for j, (h, w, x) in enumerate(zip(headers, col_w, col_x)):
    add_rect(slide, x, 1.55, w - 0.05, 0.45, ORANGE)
    add_text(slide, h, x + 0.1, 1.6, w - 0.15, 0.35,
             font_size=12, bold=True, color=WHITE)

for i, (comp, tech, just) in enumerate(rows):
    y = 2.05 + i * 0.62
    bg = LIGHT_GRAY if i % 2 == 0 else WHITE
    for w, x in zip(col_w, col_x):
        add_rect(slide, x, y, w - 0.05, 0.55, bg)
    add_text(slide, comp, col_x[0] + 0.1, y + 0.05, col_w[0] - 0.15, 0.5, font_size=11, bold=True, color=DARK)
    add_text(slide, tech, col_x[1] + 0.1, y + 0.05, col_w[1] - 0.15, 0.5, font_size=11, color=ORANGE, bold=True)
    add_text(slide, just, col_x[2] + 0.1, y + 0.05, col_w[2] - 0.15, 0.5, font_size=10, color=GRAY)


# ── SLIDE 4 — Architecture ────────────────────────────────────────────────────
slide = prs.slides.add_slide(BLANK)
gradient_bg(slide)
white_card(slide, 0.5, 0.4, 12.3, 6.6)

add_text(slide, "Architecture de la solution", 0.8, 0.6, 12, 0.8, font_size=28, bold=True, color=DARK)
add_rect(slide, 0.8, 1.35, 2.5, 0.05, ORANGE)

# Boîtes architecture
boxes = [
    (0.7, 1.6, 3.6, 1.4, "🌐  Navigateur", "Vue.js 3 + Pinia\nVue Router — 5 pages\nAxios (client API)", ACCENT),
    (4.9, 1.6, 3.5, 1.4, "⚙️  API REST", "Django 5.2 + DRF\n/auth/  /files/\nJWT + validation", RGBColor(0xFF, 0xD9, 0xBC)),
    (8.9, 1.6, 3.5, 1.4, "🗄️  Stockage", "PostgreSQL 16\n+ Disque local\n/media/uploads/", RGBColor(0xFF, 0xD9, 0xBC)),
]
for x, y, w, h, titre, desc, col in boxes:
    add_rect(slide, x, y, w, h, col)
    add_text(slide, titre, x + 0.15, y + 0.1, w - 0.3, 0.45, font_size=13, bold=True, color=DARK)
    add_text(slide, desc, x + 0.15, y + 0.55, w - 0.3, 0.75, font_size=11, color=DARK)

# Flèches texte
add_text(slide, "HTTP/JSON\nJWT →", 4.3, 2.0, 0.7, 0.8, font_size=9, color=GRAY, align=PP_ALIGN.CENTER)
add_text(slide, "ORM\nSQL →", 8.3, 2.0, 0.7, 0.8, font_size=9, color=GRAY, align=PP_ALIGN.CENTER)

# Flux principaux
add_text(slide, "Flux principaux", 0.8, 3.25, 12, 0.45, font_size=14, bold=True, color=DARK)
add_rect(slide, 0.8, 3.68, 11.5, 0.04, RGBColor(0xE0, 0xE0, 0xE0))

flux = [
    ("🔐  Authentification", "Login → JWT access (1h) + refresh (7j) → stocké localStorage → injecté dans chaque requête"),
    ("📤  Upload", "Sélection fichier → validation taille (50 Mo) → envoi multipart → stockage disque → UUID token généré"),
    ("🔗  Partage", "Lien /download/<uuid> → infos publiques → saisie MDP si protégé → téléchargement natif"),
]
for i, (titre, desc) in enumerate(flux):
    y = 3.85 + i * 0.9
    add_text(slide, titre, 0.8, y, 3.2, 0.45, font_size=12, bold=True, color=ORANGE)
    add_text(slide, desc, 4.0, y, 8.5, 0.45, font_size=11, color=GRAY)


# ── SLIDE 5 — Modèle de données ───────────────────────────────────────────────
slide = prs.slides.add_slide(BLANK)
gradient_bg(slide)
white_card(slide, 0.5, 0.4, 12.3, 6.6)

add_text(slide, "Modèle de données", 0.8, 0.6, 12, 0.8, font_size=28, bold=True, color=DARK)
add_rect(slide, 0.8, 1.35, 2, 0.05, ORANGE)

# Table User
add_rect(slide, 0.8, 1.6, 4.5, 0.45, ORANGE)
add_text(slide, "USER  (Django built-in)", 0.9, 1.65, 4.3, 0.35, font_size=13, bold=True, color=WHITE)
user_fields = [("id", "INTEGER PK"), ("username", "VARCHAR(150)"),
               ("email", "VARCHAR(254)"), ("password", "VARCHAR(128) — PBKDF2")]
for i, (f, t) in enumerate(user_fields):
    bg = LIGHT_GRAY if i % 2 == 0 else WHITE
    add_rect(slide, 0.8, 2.05 + i * 0.42, 4.5, 0.4, bg)
    add_text(slide, f, 0.95, 2.1 + i * 0.42, 1.8, 0.35, font_size=11, bold=True, color=DARK)
    add_text(slide, t, 2.75, 2.1 + i * 0.42, 2.4, 0.35, font_size=11, color=GRAY)

# Flèche relation
add_text(slide, "1 ──── N", 5.4, 2.8, 1.3, 0.5, font_size=12, bold=True, color=ORANGE, align=PP_ALIGN.CENTER)

# Table SharedFile
add_rect(slide, 6.8, 1.6, 5.8, 0.45, ORANGE)
add_text(slide, "SHAREDFILE", 6.9, 1.65, 5.6, 0.35, font_size=13, bold=True, color=WHITE)
sf_fields = [
    ("id", "UUID PK — non devinable"),
    ("owner_id", "FK → User (CASCADE)"),
    ("original_name", "VARCHAR(255)"),
    ("file", "FileField — chemin disque"),
    ("size", "BIGINT — en octets"),
    ("share_token", "UUID UNIQUE — lien partage"),
    ("expires_at", "DATETIME — expiration"),
    ("password_hash", "VARCHAR — PBKDF2 ou vide"),
    ("created_at", "DATETIME — auto"),
]
for i, (f, t) in enumerate(sf_fields):
    bg = LIGHT_GRAY if i % 2 == 0 else WHITE
    add_rect(slide, 6.8, 2.05 + i * 0.42, 5.8, 0.4, bg)
    add_text(slide, f, 6.95, 2.1 + i * 0.42, 2.2, 0.35, font_size=10, bold=True, color=DARK)
    add_text(slide, t, 9.15, 2.1 + i * 0.42, 3.2, 0.35, font_size=10, color=GRAY)


# ── SLIDE 6 — Démonstration ───────────────────────────────────────────────────
slide = prs.slides.add_slide(BLANK)
gradient_bg(slide)
white_card(slide, 0.5, 0.4, 12.3, 6.6)

add_text(slide, "Démonstration — Parcours utilisateur", 0.8, 0.6, 12, 0.8, font_size=28, bold=True, color=DARK)
add_rect(slide, 0.8, 1.35, 3.5, 0.05, ORANGE)

steps = [
    ("1", "Page d'accueil", "Fond dégradé corail · tagline · icône d'upload cliquable"),
    ("2", "Inscription / Connexion", "Formulaire centré · validation côté client et serveur · JWT stocké"),
    ("3", "Dashboard — Mon espace", "Sidebar gradient · liste des fichiers · filtres Tous / Actifs / Expiré"),
    ("4", "Upload d'un fichier", "Glisser-déposer · mot de passe optionnel · choix d'expiration · progression"),
    ("5", "Lien de partage", "Affiché après upload · copie en 1 clic · format /download/<uuid>"),
    ("6", "Page de téléchargement", "Badge expiration · saisie MDP si protégé · erreur claire si expiré"),
]
for i, (num, titre, desc) in enumerate(steps):
    y = 1.55 + i * 0.82
    add_rect(slide, 0.7, y, 0.55, 0.55, ORANGE)
    add_text(slide, num, 0.7, y + 0.05, 0.55, 0.45, font_size=18, bold=True,
             color=WHITE, align=PP_ALIGN.CENTER)
    add_text(slide, titre, 1.4, y + 0.02, 3.5, 0.35, font_size=13, bold=True, color=DARK)
    add_text(slide, desc, 1.4, y + 0.35, 10.8, 0.35, font_size=11, color=GRAY)


# ── SLIDE 7 — Qualité & Tests ─────────────────────────────────────────────────
slide = prs.slides.add_slide(BLANK)
gradient_bg(slide)
white_card(slide, 0.5, 0.4, 12.3, 6.6)

add_text(slide, "Qualité & Tests", 0.8, 0.6, 12, 0.8, font_size=28, bold=True, color=DARK)
add_rect(slide, 0.8, 1.35, 1.8, 0.05, ORANGE)

# Métriques clés
metrics = [("38", "tests\nunitaires\n+ intégration"), ("10", "tests E2E\nPlaywright"), ("100%", "couverture\nde code"), ("0", "vulnérabilité\napplicative")]
for i, (val, label) in enumerate(metrics):
    x = 0.7 + i * 3.0
    add_rect(slide, x, 1.55, 2.8, 1.4, RGBColor(0xFF, 0xF3, 0xEB))
    add_text(slide, val, x + 0.1, 1.65, 2.6, 0.7, font_size=34, bold=True,
             color=ORANGE, align=PP_ALIGN.CENTER)
    add_text(slide, label, x + 0.1, 2.35, 2.6, 0.55, font_size=10, color=GRAY,
             align=PP_ALIGN.CENTER)

# 2 colonnes : unitaires/intégration | E2E
add_text(slide, "Tests unitaires & intégration (pytest)", 0.8, 3.1, 5.8, 0.4, font_size=12, bold=True, color=ORANGE)
bullet_list(slide, [
    "Inscription, connexion, profil, isolation utilisateur",
    "Upload (taille, MDP, expiration custom, sans fichier)",
    "Suppression (propre fichier / fichier d'autrui → 404)",
    "Téléchargement (valide, expiré 410, MDP 403, 404)",
    "Modèle : is_expired, is_password_protected, hachage",
], 0.8, 3.52, 5.8, font_size=11)

add_text(slide, "Tests E2E — Playwright (navigateur réel)", 6.8, 3.1, 5.8, 0.4, font_size=12, bold=True, color=ORANGE)
bullet_list(slide, [
    "Page d'accueil — tagline et icône visibles",
    "Inscription → redirection dashboard",
    "Connexion correcte / mauvais MDP → erreur",
    "Déconnexion → retour /login",
    "Upload fichier → lien de partage généré",
    "Lien partage → page téléchargement publique",
    "Suppression → fichier retiré de la liste",
], 6.8, 3.52, 5.8, font_size=11)

add_text(slide, "Scan sécurité pip-audit : 0 vulnérabilité applicative  •  Bundle prod : 139 Ko JS (54 Ko gzip)  •  Build : 1.2s",
         0.8, 6.85, 11.5, 0.4, font_size=10, color=GRAY, italic=True)


# ── SLIDE 8 — Utilisation de l'IA ────────────────────────────────────────────
slide = prs.slides.add_slide(BLANK)
gradient_bg(slide)
white_card(slide, 0.5, 0.4, 12.3, 6.6)

add_text(slide, "Utilisation de l'IA dans le développement", 0.8, 0.6, 12, 0.8, font_size=24, bold=True, color=DARK)
add_rect(slide, 0.8, 1.35, 4, 0.05, ORANGE)

add_text(slide, "Posture : copilote technique assigné à une User Story précise — pas du vibe coding",
         0.8, 1.5, 11.5, 0.45, font_size=13, color=GRAY, italic=True)

# 2 colonnes
add_text(slide, "Tâches confiées à l'IA", 0.8, 2.05, 5.5, 0.45, font_size=14, bold=True, color=ORANGE)
bullet_list(slide, [
    "Modèle SharedFile (hachage MDP, propriétés)",
    "Sérialiseurs DRF (upload, download, public)",
    "Vues API (upload, download, info publique)",
    "Store Pinia files.js + composants Vue.js",
    "Suite de tests pytest (38 tests)",
    "Documentation (README, TESTING, SECURITY…)",
], 0.8, 2.5, 5.5, font_size=11)

add_text(slide, "Supervision & corrections apportées", 6.5, 2.05, 6, 0.45, font_size=14, bold=True, color=ORANGE)
bullet_list(slide, [
    "✏️  Filtre owner=request.user manquant sur suppression",
    "✏️  share_url corrigé → frontend Vue plutôt qu'API",
    "✏️  Refresh token dans intercepteur Axios incomplet",
    "✏️  Layout desktop login card disparaissait (flexbox)",
    "✅  Aucune intégration sans tests passants",
    "✅  Revue systématique de chaque bloc de code",
], 6.5, 2.5, 6, font_size=11)

add_rect(slide, 0.8, 5.5, 11.5, 0.05, RGBColor(0xE0, 0xE0, 0xE0))
add_text(slide, "Apport mesuré : ×3 sur la vitesse d'implémentation des vues et sérialiseurs  "
         "—  Limite : supervision indispensable sur la sécurité et les cas limites",
         0.8, 5.65, 11.5, 0.6, font_size=11, color=GRAY, italic=True)


# ── SLIDE 9 — Conclusion ──────────────────────────────────────────────────────
slide = prs.slides.add_slide(BLANK)
gradient_bg(slide)
white_card(slide, 0.5, 0.4, 12.3, 6.6)

add_text(slide, "Ce qui a été livré", 0.8, 0.6, 12, 0.8, font_size=28, bold=True, color=DARK)
add_rect(slide, 0.8, 1.35, 2, 0.05, ORANGE)

livrables = [
    ("✅", "Application web fonctionnelle", "Toutes les US MVP implémentées et testées"),
    ("✅", "Architecture découplée professionnelle", "Vue.js + Django REST API + PostgreSQL + Docker"),
    ("✅", "Sécurité solide", "JWT, PBKDF2, isolation utilisateur, UUID v4, CORS strict"),
    ("✅", "38 tests, 100% de couverture", "pytest — tests unitaires et d'intégration"),
    ("✅", "Documentation complète", "README, OpenAPI, TESTING, SECURITY, PERF, MAINTENANCE"),
    ("✅", "Installation en 1 commande", "docker compose up -d"),
]
for i, (check, titre, desc) in enumerate(livrables):
    y = 1.6 + i * 0.75
    add_rect(slide, 0.75, y, 0.5, 0.5, RGBColor(0xD4, 0xED, 0xDA))
    add_text(slide, check, 0.75, y + 0.05, 0.5, 0.4, font_size=14, align=PP_ALIGN.CENTER, color=RGBColor(0x15, 0x5A, 0x24))
    add_text(slide, titre, 1.4, y + 0.02, 4, 0.35, font_size=13, bold=True, color=DARK)
    add_text(slide, desc, 5.4, y + 0.02, 7.2, 0.35, font_size=12, color=GRAY)

add_text(slide, "Prochaines étapes post-MVP :", 0.8, 6.15, 12, 0.35, font_size=12, bold=True, color=ORANGE)
add_text(slide, "Stockage S3  •  Rate limiting  •  httpOnly cookies  •  Envoi par email  •  App mobile",
         0.8, 6.5, 11.5, 0.4, font_size=11, color=GRAY)


# ── SLIDE 10 — Questions ──────────────────────────────────────────────────────
slide = prs.slides.add_slide(BLANK)
gradient_bg(slide)

add_text(slide, "DataShare", 1, 2.0, 11, 1.2, font_size=72, bold=True,
         color=DARK, align=PP_ALIGN.CENTER)
add_rect(slide, 4, 3.3, 5.33, 0.07, WHITE)
add_text(slide, "Questions ?", 1, 3.5, 11, 0.9, font_size=32, color=WHITE,
         align=PP_ALIGN.CENTER)
add_text(slide, "Démo live : http://localhost:5173", 1, 4.5, 11, 0.6,
         font_size=16, color=WHITE, align=PP_ALIGN.CENTER, italic=True)
add_text(slide, "Copyright DataShare© 2025", 0.5, 7.0, 12, 0.4,
         font_size=10, color=WHITE, align=PP_ALIGN.CENTER)


# ── Export ────────────────────────────────────────────────────────────────────
output = "docs/presentation_datashare.pptx"
prs.save(output)
print(f"✅ PowerPoint généré : {output}")
