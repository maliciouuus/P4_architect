#!/usr/bin/env python3
"""Génère le support de présentation DataShare v2 (NestJS) au format PowerPoint."""

from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

# ── Palette DataShare ─────────────────────────────────────────────────────────
ORANGE      = RGBColor(0xFF, 0x81, 0x2D)
ORANGE_DARK = RGBColor(0xDE, 0x62, 0x62)
DARK        = RGBColor(0x1A, 0x1A, 0x1A)
WHITE       = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT_GRAY  = RGBColor(0xF5, 0xF5, 0xF5)
GRAY        = RGBColor(0x75, 0x75, 0x75)
ACCENT      = RGBColor(0xFF, 0xB8, 0x8C)
GREEN       = RGBColor(0x16, 0xA3, 0x4A)
GREEN_L     = RGBColor(0xD4, 0xED, 0xDA)
GREEN_DARK  = RGBColor(0x15, 0x5A, 0x24)
RED         = RGBColor(0xDC, 0x26, 0x26)
RED_L       = RGBColor(0xFE, 0xE2, 0xE2)
BLUE        = RGBColor(0x25, 0x63, 0xEB)
BLUE_L      = RGBColor(0xDB, 0xEA, 0xFE)
CARD_BG     = RGBColor(0xFF, 0xF3, 0xEB)
PURPLE      = RGBColor(0x7C, 0x3A, 0xED)
PURPLE_L    = RGBColor(0xED, 0xE9, 0xFE)
YELLOW_L    = RGBColor(0xFF, 0xF9, 0xC4)
YELLOW      = RGBColor(0xF5, 0x9E, 0x0B)

prs = Presentation()
prs.slide_width  = Inches(13.33)
prs.slide_height = Inches(7.5)
BLANK = prs.slide_layouts[6]


# ── Helpers ───────────────────────────────────────────────────────────────────
def rect(slide, left, top, width, height, color, border_color=None, border_pt=0):
    s = slide.shapes.add_shape(1,
        Inches(left), Inches(top), Inches(width), Inches(height))
    s.fill.solid()
    s.fill.fore_color.rgb = color
    if border_color and border_pt:
        s.line.color.rgb = border_color
        s.line.width = Pt(border_pt)
    else:
        s.line.fill.background()
    return s


def txt(slide, text, left, top, width, height,
        size=14, bold=False, color=DARK, align=PP_ALIGN.LEFT, italic=False):
    tb = slide.shapes.add_textbox(
        Inches(left), Inches(top), Inches(width), Inches(height))
    tf = tb.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    r = p.add_run()
    r.text = text
    r.font.size = Pt(size)
    r.font.bold = bold
    r.font.italic = italic
    r.font.color.rgb = color
    return tb


def bullets(slide, items, left, top, width, size=12, color=DARK, spacing=4):
    tb = slide.shapes.add_textbox(
        Inches(left), Inches(top), Inches(width), Inches(5))
    tf = tb.text_frame
    tf.word_wrap = True
    for i, item in enumerate(items):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.space_before = Pt(spacing)
        r = p.add_run()
        r.text = item
        r.font.size = Pt(size)
        r.font.color.rgb = color


def gradient_bg(slide):
    s = slide.shapes.add_shape(1, Inches(0), Inches(0),
                                Inches(13.33), Inches(7.5))
    s.fill.gradient()
    s.fill.gradient_angle = 135
    stops = s.fill.gradient_stops
    stops[0].position = 0
    stops[0].color.rgb = RGBColor(0xFF, 0xB8, 0x8C)
    stops[1].position = 1
    stops[1].color.rgb = RGBColor(0xDE, 0x62, 0x62)
    s.line.fill.background()


def card(slide, left, top, width, height):
    s = rect(slide, left, top, width, height, WHITE,
             RGBColor(0xE0, 0xE0, 0xE0), 0.5)
    return s


def slide_header(slide, title, subtitle=None):
    txt(slide, title, 0.6, 0.25, 12, 0.75,
        size=26, bold=True, color=DARK)
    rect(slide, 0.6, 0.98, 1.8, 0.055, ORANGE)
    if subtitle:
        txt(slide, subtitle, 0.6, 1.08, 12, 0.45,
            size=12, color=GRAY, italic=True)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 1 — Page de garde
# ═══════════════════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
gradient_bg(slide)

txt(slide, "DataShare", 1, 1.0, 11, 1.6,
    size=72, bold=True, color=DARK, align=PP_ALIGN.CENTER)
rect(slide, 4.0, 2.85, 5.3, 0.07, WHITE)
txt(slide, "Plateforme de transfert de fichiers sécurisé",
    1, 3.0, 11, 0.8, size=20, color=DARK, align=PP_ALIGN.CENTER)
txt(slide, "Prototype MVP — Mai 2026",
    1, 3.85, 11, 0.6, size=14, color=DARK, align=PP_ALIGN.CENTER, italic=True)

for i, (label, val) in enumerate([
    ("Backend", "NestJS"), ("Tests", "32 ✓"), ("Couverture", "78 %")
]):
    x = 2.5 + i * 3.0
    s = slide.shapes.add_shape(1, Inches(x), Inches(4.9),
                                Inches(2.5), Inches(1.1))
    s.fill.solid()
    s.fill.fore_color.rgb = RGBColor(0x00, 0x00, 0x00)
    s.fill.transparency = 0.25
    s.line.fill.background()
    txt(slide, val,   x+0.1, 4.95, 2.3, 0.6, size=20, bold=True,
        color=WHITE, align=PP_ALIGN.CENTER)
    txt(slide, label, x+0.1, 5.55, 2.3, 0.4, size=10,
        color=ACCENT, align=PP_ALIGN.CENTER)

txt(slide, "© DataShare 2026", 0.5, 7.1, 12, 0.35,
    size=9, color=WHITE, align=PP_ALIGN.CENTER)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 2 — Contexte & Problème
# ═══════════════════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
gradient_bg(slide)
card(slide, 0.4, 0.15, 12.5, 7.15)
slide_header(slide, "Contexte & Problème",
             "Pourquoi DataShare ? Quel besoin concret ?")

txt(slide, "Le problème", 0.7, 1.35, 5.8, 0.45, size=14, bold=True, color=ORANGE)
bullets(slide, [
    "Freelances et PME ont besoin de partager des fichiers volumineux facilement",
    "WeTransfer → dépendance externe, publicité, limite gratuite faible",
    "Dropbox → compte obligatoire, coût abonnement, données hébergées à l'étranger",
    "Google Drive → interface lourde pour un simple partage ponctuel",
    "FTP / serveur partagé → configuration complexe, non accessible à tous",
], 0.7, 1.82, 5.8, size=11, color=DARK)

txt(slide, "DataShare — La réponse", 7.0, 1.35, 5.8, 0.45, size=14, bold=True, color=ORANGE)
bullets(slide, [
    "Solution souveraine : données hébergées chez vous",
    "Auto-hébergeable en 1 commande Docker",
    "Sécurisée : JWT, bcrypt, UUID v4 non prédictibles",
    "Simple : partage en 3 clics, lien prêt en secondes",
    "Expiration automatique jusqu'à 7 jours",
    "Protection par mot de passe optionnelle",
], 7.0, 1.82, 5.8, size=11, color=DARK)

rect(slide, 0.6, 4.3, 12.1, 0.05, RGBColor(0xE8, 0xE8, 0xE8))
txt(slide, "Cible principale", 0.6, 4.42, 12, 0.4, size=13, bold=True, color=DARK)

targets = [
    ("Freelances", "Partage client rapide sans compte tiers"),
    ("PME", "Souveraineté des données, conformité RGPD"),
    ("Équipes tech", "Auto-hébergement, Docker, open source"),
    ("Agences", "Livraison de fichiers volumineux aux clients"),
]
for i, (titre, desc) in enumerate(targets):
    x = 0.6 + i * 3.1
    rect(slide, x, 4.9, 2.9, 1.3, CARD_BG, ORANGE, 0.8)
    txt(slide, titre, x+0.15, 4.98, 2.6, 0.35, size=12, bold=True, color=ORANGE)
    txt(slide, desc,  x+0.15, 5.35, 2.6, 0.8,  size=10, color=DARK)

txt(slide, "© DataShare 2026", 0.4, 7.1, 12.5, 0.32, size=9, color=GRAY, align=PP_ALIGN.CENTER)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 3 — Architecture technique
# ═══════════════════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
gradient_bg(slide)
card(slide, 0.4, 0.15, 12.5, 7.15)
slide_header(slide, "Architecture technique",
             "3-tier découplé · Docker Compose · Vue.js 3 + NestJS + PostgreSQL")

boxes = [
    (0.65, 1.45, 3.2, 2.2, "Frontend",
     "Vue.js 3 SPA\nVue Router\nPinia (state)\nAxios (HTTP)", BLUE_L, BLUE),
    (4.4, 1.45, 4.4, 2.2, "Backend API",
     "NestJS (TypeScript)\n/auth  /files\nJWT · CORS · Guards\nclass-validator", CARD_BG, ORANGE),
    (9.35, 1.45, 3.3, 2.2, "Persistance",
     "PostgreSQL 16\nTypeORM\nLocal Filesystem\nVolumes Docker", GREEN_L, GREEN),
]
for x, y, w, h, titre, desc, bg, border in boxes:
    rect(slide, x, y, w, h, bg, border, 1.5)
    rect(slide, x, y, w, 0.42, border)
    txt(slide, titre, x+0.15, y+0.06, w-0.3, 0.3, size=13, bold=True, color=WHITE)
    txt(slide, desc,  x+0.15, y+0.52, w-0.3, 1.55, size=10, color=DARK)

txt(slide, "HTTP/JSON\nJWT Bearer →", 3.88, 2.05, 0.6, 0.9, size=9, color=GRAY, align=PP_ALIGN.CENTER)
txt(slide, "TypeORM\nSQL →",          8.82, 2.05, 0.6, 0.9, size=9, color=GRAY, align=PP_ALIGN.CENTER)

rect(slide, 0.55, 3.75, 12.3, 0.06, RGBColor(0xE0, 0xE0, 0xE0))
txt(slide, "Docker Compose — réseau interne · volumes persistants postgres_data & uploads_data",
    0.55, 3.88, 12.3, 0.38, size=10, color=GRAY, italic=True, align=PP_ALIGN.CENTER)

txt(slide, "Flux d'un upload — de l'interface au disque", 0.6, 4.35, 12, 0.4, size=13, bold=True, color=DARK)

steps = [
    ("1. Clic", "Utilisateur\nsélectionne\nle fichier"),
    ("2. Axios", "POST /api/files\n/upload\n(multipart)"),
    ("3. Guard JWT", "JwtAuthGuard\nvalide le\nBearer token"),
    ("4. Service", "Valide extension\net taille, génère\nUUID shareToken"),
    ("5. Disque", "Fichier stocké\nuploads/<id>/\n<uuid>_nom"),
    ("6. BDD", "SharedFile créé\nen PostgreSQL\n(TypeORM)"),
]
for i, (num, desc) in enumerate(steps):
    x = 0.6 + i * 2.1
    col = ORANGE if i % 2 == 0 else BLUE
    rect(slide, x, 4.85, 1.95, 1.8, LIGHT_GRAY, col, 1.2)
    txt(slide, num,  x+0.1, 4.92, 1.75, 0.35, size=10, bold=True, color=col)
    txt(slide, desc, x+0.1, 5.28, 1.75, 1.3,  size=9,  color=DARK)
    if i < 5:
        txt(slide, "→", x+1.9, 5.5, 0.2, 0.4, size=14, bold=True, color=GRAY)

txt(slide, "© DataShare 2026", 0.4, 7.1, 12.5, 0.32, size=9, color=GRAY, align=PP_ALIGN.CENTER)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — Stack technologique
# ═══════════════════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
gradient_bg(slide)
card(slide, 0.4, 0.15, 12.5, 7.15)
slide_header(slide, "Stack technologique",
             "Choix modernes, maintenables et éprouvés en production")

stack = [
    ("Frontend",        "Vue.js 3 + Pinia + Vite",       "Composition API, bundle ~67 Ko gzip, HMR instantané"),
    ("Backend",         "NestJS (TypeScript)",            "Architecture modulaire, DI native, décorateurs, Guard/Strategy"),
    ("Base de données", "PostgreSQL 16",                  "UUID natif, ACID, index sur owner_id, standard professionnel"),
    ("Auth",            "JWT + bcrypt coût 12",           "Stateless, Guard NestJS, hash résistant brute-force"),
    ("Stockage",        "Système de fichiers local",      "Suffisant MVP, chemin non devinable, migration S3 documentée"),
    ("Tests",           "Jest 32 tests · Playwright E2E", "78% couverture globale · 11 scénarios E2E passants"),
    ("Déploiement",     "Docker + Docker Compose",        "Reproductibilité totale, 3 services, 1 commande"),
]

headers = ["Composant", "Technologie", "Justification"]
col_w   = [2.4, 3.5, 6.1]
col_x   = [0.55, 2.95, 6.45]

for j, (h, w, x) in enumerate(zip(headers, col_w, col_x)):
    rect(slide, x, 1.35, w-0.08, 0.42, ORANGE)
    txt(slide, h, x+0.12, 1.4, w-0.2, 0.32, size=11, bold=True, color=WHITE)

for i, (comp, tech, just) in enumerate(stack):
    y = 1.82 + i * 0.62
    bg = LIGHT_GRAY if i % 2 == 0 else WHITE
    for w, x in zip(col_w, col_x):
        rect(slide, x, y, w-0.08, 0.58, bg)
    txt(slide, comp, col_x[0]+0.12, y+0.1, col_w[0]-0.2, 0.38, size=11, bold=True, color=DARK)
    txt(slide, tech, col_x[1]+0.12, y+0.1, col_w[1]-0.2, 0.38, size=11, bold=True, color=ORANGE)
    txt(slide, just, col_x[2]+0.12, y+0.1, col_w[2]-0.2, 0.38, size=10, color=DARK)

txt(slide, "© DataShare 2026", 0.4, 7.1, 12.5, 0.32, size=9, color=GRAY, align=PP_ALIGN.CENTER)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — Fonctionnalités MVP
# ═══════════════════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
gradient_bg(slide)
card(slide, 0.4, 0.15, 12.5, 7.15)
slide_header(slide, "Fonctionnalités MVP",
             "8 User Stories livrées dont 2 bonus — toutes validées")

txt(slide, "User Stories de base", 0.65, 1.3, 6.0, 0.4, size=13, bold=True, color=DARK)
us_core = [
    ("US01", "Upload connecté",           "Fichier jusqu'à 1 Go, MDP optionnel, expiration 1-7j"),
    ("US02", "Téléchargement via lien",   "UUID v4 non prédictible · 410 Gone si expiré"),
    ("US03", "Création de compte",        "Email unique · bcrypt coût 12 · validation class-validator"),
    ("US04", "Connexion JWT",             "Access token 7j · stateless · Guard NestJS"),
    ("US05", "Historique des fichiers",   "Nom, taille, date, statut · isolation utilisateur"),
    ("US06", "Suppression",               "Suppression physique + BDD · 404 si fichier d'autrui"),
]
for i, (code, label, detail) in enumerate(us_core):
    y = 1.76 + i * 0.68
    rect(slide, 0.65, y, 5.9, 0.6, GREEN_L, GREEN, 0.8)
    txt(slide, "✅ " + code, 0.78, y+0.06, 1.0, 0.3, size=10, bold=True, color=GREEN_DARK)
    txt(slide, label,  1.8,  y+0.04, 2.0, 0.28, size=11, bold=True, color=DARK)
    txt(slide, detail, 1.8,  y+0.3,  4.6, 0.26, size=9,  color=GRAY, italic=True)

txt(slide, "User Stories bonus", 6.8, 1.3, 6.0, 0.4, size=13, bold=True, color=DARK)
us_bonus = [
    ("US07", "Upload anonyme",              "Partage sans compte · UUID v4 · expiration auto"),
    ("US09", "Protection par mot de passe", "bcrypt coût 12 · vérification côté serveur"),
    ("US10", "Expiration automatique",      "Cron 24h · purge fichier physique + BDD"),
]
for i, (code, label, detail) in enumerate(us_bonus):
    y = 1.76 + i * 0.68
    rect(slide, 6.8, y, 5.9, 0.6, CARD_BG, ORANGE, 0.8)
    txt(slide, "✅ " + code, 6.93, y+0.06, 1.0, 0.3, size=10, bold=True, color=ORANGE)
    txt(slide, label,  7.95, y+0.04, 2.5, 0.28, size=11, bold=True, color=DARK)
    txt(slide, detail, 7.95, y+0.3,  4.6, 0.26, size=9,  color=GRAY, italic=True)

rect(slide, 0.6, 6.45, 12.1, 0.65, ORANGE)
txt(slide, "9 User Stories livrées · Toutes les US de base + 3 bonus · MVP 100% fonctionnel",
    0.6, 6.53, 12.1, 0.5, size=13, bold=True, color=WHITE, align=PP_ALIGN.CENTER)

txt(slide, "© DataShare 2026", 0.4, 7.1, 12.5, 0.32, size=9, color=WHITE, align=PP_ALIGN.CENTER)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 6 — Sécurité
# ═══════════════════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
gradient_bg(slide)
card(slide, 0.4, 0.15, 12.5, 7.15)
slide_header(slide, "Sécurité",
             "Défense en profondeur — chaque couche protégée indépendamment")

sec_cols = [
    ("Authentification JWT", [
        "JWT stateless — 7 jours, HS256",
        "Guard NestJS sur toutes les routes protégées",
        "Header Authorization: Bearer",
        "Aucune session serveur à gérer",
    ]),
    ("Hashage & mots de passe", [
        "bcrypt coût 12 — résistant brute-force",
        "MDP utilisateur et fichier jamais en clair",
        "Jamais loggé ni exposé en API",
        "Validation class-validator côté serveur",
    ]),
    ("Accès & isolation", [
        "UUID v4 tokens — 128 bits non prédictibles",
        "Isolation utilisateur garantie (owner FK)",
        "Extensions interdites : .exe, .bat, .sh...",
        "CORS strict — origines explicites uniquement",
    ]),
    ("Infrastructure", [
        "Validation taille fichier côté serveur (1 Go)",
        "class-validator sur tous les DTOs NestJS",
        "Docker Compose — réseau interne isolé",
        "Variables sensibles en .env (hors dépôt)",
    ]),
]

for i, (titre, items) in enumerate(sec_cols):
    col = i % 2
    row = i // 2
    x = 0.6 + col * 6.2
    y = 1.35 + row * 2.85
    rect(slide, x, y, 5.9, 2.65, LIGHT_GRAY, RGBColor(0xE0, 0xE0, 0xE0), 0.8)
    rect(slide, x, y, 5.9, 0.42, ORANGE)
    txt(slide, titre, x+0.15, y+0.06, 5.6, 0.3, size=12, bold=True, color=WHITE)
    bullets(slide, ["• " + it for it in items],
            x+0.2, y+0.52, 5.5, size=11, color=DARK, spacing=4)

txt(slide,
    "MVP conscient : localStorage (XSS) → prod : cookies httpOnly · Pas de rate limiting → prod : middleware Express",
    0.6, 7.08, 12.1, 0.38, size=10, color=GRAY, italic=True)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 7 — Tests unitaires
# ═══════════════════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
gradient_bg(slide)
card(slide, 0.4, 0.15, 12.5, 7.15)
slide_header(slide, "Tests unitaires — Jest",
             "32 tests · 7 suites · 78% couverture globale · 0 régression")

metrics = [
    ("32", "tests\nunitaires", ORANGE),
    ("78 %", "couverture\nglobale", GREEN),
    ("7", "suites\nde tests", BLUE),
    ("0", "vulnérabilités\nnpm audit", GREEN),
]
for i, (val, label, color) in enumerate(metrics):
    x = 0.9 + i * 2.9
    rect(slide, x, 1.35, 2.6, 1.3, CARD_BG, color, 1)
    txt(slide, val,   x+0.1, 1.45, 2.4, 0.65, size=26, bold=True, color=color, align=PP_ALIGN.CENTER)
    txt(slide, label, x+0.1, 2.1,  2.4, 0.5,  size=9,  color=GRAY, align=PP_ALIGN.CENTER)

txt(slide, "Fichiers testés", 0.6, 2.85, 12, 0.4, size=12, bold=True, color=DARK)

suites = [
    ("auth.service.spec.ts",      "7 tests", "register(), login() — bcrypt, JWT, email dupliqué",     ORANGE),
    ("files.service.spec.ts",     "11 tests","upload, download, delete, expiration, isolation",        BLUE),
    ("auth.controller.spec.ts",   "3 tests", "register/login/me — délégation au service vérifiée",    ORANGE),
    ("files.controller.spec.ts",  "6 tests", "list, upload, uploadAnonymous, delete, share, download", BLUE),
    ("jwt.strategy.spec.ts",      "2 tests", "validate() — payload JWT → { id, email }",              PURPLE),
    ("files.cron.spec.ts",        "3 tests", "purge 60s, log count, résistance aux erreurs DB",        GREEN),
]
for i, (name, count, desc, color) in enumerate(suites):
    col = i % 2
    row = i // 2
    x = 0.55 + col * 6.3
    y = 3.35 + row * 1.0
    rect(slide, x, y, 6.1, 0.85, LIGHT_GRAY, color, 0.8)
    txt(slide, f"✅ {name}", x+0.15, y+0.05, 3.8, 0.3, size=10, bold=True, color=color)
    txt(slide, count, x+4.0, y+0.05, 1.9, 0.3, size=10, bold=True, color=GRAY, align=PP_ALIGN.RIGHT)
    txt(slide, desc,  x+0.15, y+0.38, 5.8, 0.4, size=9, color=DARK)

txt(slide,
    "Stratégie : mocks TypeORM + bcrypt + fs — aucun accès BDD réelle — tests reproductibles en < 7s",
    0.6, 6.42, 12.1, 0.4, size=10, bold=True, color=ORANGE, align=PP_ALIGN.CENTER)

txt(slide, "© DataShare 2026", 0.4, 7.1, 12.5, 0.32, size=9, color=GRAY, align=PP_ALIGN.CENTER)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 8 — Tests E2E (Playwright) — slide défense
# ═══════════════════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
gradient_bg(slide)
card(slide, 0.4, 0.15, 12.5, 7.15)
slide_header(slide, "Tests End-to-End — Playwright",
             "11 scénarios · navigateur réel · parcours utilisateur complets")

# Définition
rect(slide, 0.6, 1.3, 12.1, 0.42, BLUE)
txt(slide, "C'est quoi un test E2E ?", 0.75, 1.35, 12, 0.3, size=13, bold=True, color=WHITE)
txt(slide,
    "Un test E2E (End-to-End) simule un vrai utilisateur dans un vrai navigateur. "
    "Contrairement aux tests unitaires qui testent une fonction isolée, "
    "le test E2E fait tourner l'application complète (frontend + backend + BDD) "
    "et vérifie que tous les composants fonctionnent ensemble.",
    0.6, 1.78, 12.1, 0.7, size=10, color=DARK)

# Différence unitaire vs E2E
txt(slide, "Unitaire vs E2E", 0.6, 2.58, 5.8, 0.35, size=12, bold=True, color=DARK)
rect(slide, 0.6, 2.95, 5.7, 1.55, LIGHT_GRAY, BLUE, 0.8)
txt(slide, "🔬 Test unitaire", 0.75, 3.0, 5.4, 0.3, size=11, bold=True, color=BLUE)
bullets(slide, [
    "• Teste une seule fonction en isolation",
    "• Dépendances remplacées par des mocks",
    "• Rapide (< 1s), pas de serveur lancé",
    "• Exemple : register() lève 409 si email dupliqué",
], 0.75, 3.32, 5.4, size=9, color=DARK, spacing=3)

rect(slide, 6.6, 2.95, 5.7, 1.55, LIGHT_GRAY, GREEN, 0.8)
txt(slide, "🌐 Test E2E (Playwright)", 6.75, 3.0, 5.4, 0.3, size=11, bold=True, color=GREEN)
bullets(slide, [
    "• Simule l'utilisateur dans Chromium headless",
    "• Application complète lancée (Docker)",
    "• Plus lent (30-60s), mais 100% réaliste",
    "• Exemple : cliquer 'Créer mon compte', vérifier /dashboard",
], 6.75, 3.32, 5.4, size=9, color=DARK, spacing=3)

# Scénarios
txt(slide, "11 scénarios implémentés", 0.6, 4.62, 12, 0.35, size=12, bold=True, color=DARK)

scenarios = [
    ("test_auth.py — 6 tests", [
        "✅ Page d'accueil affiche la tagline",
        "✅ Inscription → redirection /dashboard",
        "✅ Déconnexion → retour /login",
        "✅ Mauvais MDP → message d'erreur",
        "✅ /dashboard sans token → redirige /login",
        "✅ Connexion valide → accès dashboard",
    ], ORANGE),
    ("test_files.py — 4 tests", [
        "✅ Upload → lien de partage généré",
        "✅ Lien public → page téléchargement",
        "✅ Fichier visible dans l'historique",
        "✅ Suppression + confirmation modale",
        "",
        "",
    ], BLUE),
]
for i, (title, items, color) in enumerate(scenarios):
    x = 0.6 + i * 6.3
    rect(slide, x, 5.0, 6.1, 0.32, color)
    txt(slide, title, x+0.15, 5.04, 5.8, 0.24, size=10, bold=True, color=WHITE)
    bullets(slide, items, x+0.15, 5.35, 5.8, size=9, color=DARK, spacing=2)

txt(slide, "© DataShare 2026", 0.4, 7.1, 12.5, 0.32, size=9, color=GRAY, align=PP_ALIGN.CENTER)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 9 — Compromis MVP vs Production
# ═══════════════════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
gradient_bg(slide)
card(slide, 0.4, 0.15, 12.5, 7.15)
slide_header(slide, "Compromis MVP vs Production",
             "Décisions conscientes — chemin de migration documenté")

rect(slide, 0.6, 1.28, 12.1, 0.38, DARK)
for j, h in enumerate(["Sujet", "Choix MVP", "Pourquoi acceptable", "En production"]):
    xh = [0.62, 2.5, 5.5, 9.2][j]
    wh = [1.8, 2.9, 3.6, 3.5][j]
    txt(slide, h, xh, 1.32, wh, 0.28, size=10, bold=True, color=WHITE)

rows = [
    ("Stockage JWT",      "localStorage",          "MVP : pas de XSS attendu sur prototype",  "Cookies httpOnly; Secure; SameSite"),
    ("Schéma BDD",        "synchronize: true",     "Crée les tables auto au démarrage",        "synchronize: false + migrations TypeORM"),
    ("Rate limiting",     "Aucun",                 "Trafic faible en démo investisseurs",      "Middleware express-rate-limit sur /auth"),
    ("Stockage fichiers", "Disque local",           "Suffisant pour 1 Go, facile à déboguer",  "AWS S3 + URLs signées temporaires"),
    ("HTTPS",             "HTTP en localhost",      "Pas de domaine sur prototype local",       "Nginx reverse proxy + Let's Encrypt"),
    ("Scan antivirus",    "Aucun",                  "Extensions interdites (.exe, .bat…)",     "ClamAV + scan à l'upload"),
]

for i, (sujet, mvp, why, prod) in enumerate(rows):
    y = 1.72 + i * 0.82
    bg = LIGHT_GRAY if i % 2 == 0 else WHITE
    rect(slide, 0.62, y, 12.06, 0.78, bg)
    txt(slide, sujet, 0.75, y+0.18, 1.7,  0.4, size=10, bold=True, color=DARK)
    rect(slide, 2.5, y+0.14, 2.85, 0.42, YELLOW_L, YELLOW, 0.8)
    txt(slide, mvp,   2.62, y+0.2,  2.65, 0.3, size=9, bold=True, color=YELLOW)
    txt(slide, why,   5.52, y+0.18, 3.55, 0.4, size=9,  color=GRAY, italic=True)
    rect(slide, 9.2,  y+0.14, 3.35, 0.42, GREEN_L, GREEN, 0.8)
    txt(slide, prod,  9.32, y+0.2,  3.15, 0.3, size=9, bold=True, color=GREEN_DARK)

txt(slide,
    "Ces compromis sont documentés dans SECURITY.md et MAINTENANCE.md — migration planifiée, pas ignorée.",
    0.6, 7.06, 12.1, 0.38, size=10, bold=True, color=ORANGE, italic=True)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 10 — Utilisation de l'IA
# ═══════════════════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
gradient_bg(slide)
card(slide, 0.4, 0.15, 12.5, 7.15)
slide_header(slide, "Utilisation de l'IA",
             "Outil de support — pas de substitution au raisonnement architectural")

rect(slide, 0.6, 1.28, 12.1, 0.38, DARK)
txt(slide, "Le code métier a été écrit par le développeur. L'IA a été utilisée sur les tâches périphériques.",
    0.75, 1.32, 12, 0.3, size=11, bold=True, color=WHITE)

used = [
    ("✅ Tests unitaires",     "Squelettes de tests Jest pour controllers et stratégie JWT"),
    ("✅ Commandes terminal",  "Docker Compose, scripts TypeORM, génération PDF, commandes npm complexes"),
    ("✅ Débogage",            "Identification des erreurs TypeScript, incompatibilités modules NestJS"),
    ("✅ Documentation",       "Rédaction TESTING.md, SECURITY.md, PERF.md, MAINTENANCE.md"),
]
not_used = [
    ("❌ Logique métier",      "AuthService, FilesService — écrits et compris par le développeur"),
    ("❌ Architecture",        "Choix NestJS/Vue/PostgreSQL, découpage en modules, entités"),
    ("❌ Sécurité",            "Décisions bcrypt coût 12, CORS, isolation ownerId, UUID v4"),
    ("❌ Interface utilisateur","Toutes les vues Vue.js, router, stores Pinia"),
]

txt(slide, "Délégué à l'IA", 0.6, 1.78, 5.9, 0.35, size=12, bold=True, color=GREEN)
for i, (label, desc) in enumerate(used):
    y = 2.18 + i * 0.72
    rect(slide, 0.6, y, 5.9, 0.65, GREEN_L, GREEN, 0.5)
    txt(slide, label, 0.75, y+0.06, 2.5, 0.28, size=10, bold=True, color=GREEN_DARK)
    txt(slide, desc,  0.75, y+0.34, 5.6, 0.26, size=9,  color=DARK)

txt(slide, "Pas délégué à l'IA", 6.8, 1.78, 5.9, 0.35, size=12, bold=True, color=RED)
for i, (label, desc) in enumerate(not_used):
    y = 2.18 + i * 0.72
    rect(slide, 6.8, y, 5.9, 0.65, RED_L, RED, 0.5)
    txt(slide, label, 6.95, y+0.06, 2.5, 0.28, size=10, bold=True, color=RED)
    txt(slide, desc,  6.95, y+0.34, 5.6, 0.26, size=9,  color=DARK)

rect(slide, 0.6, 5.1, 12.1, 0.06, RGBColor(0xE0, 0xE0, 0xE0))
txt(slide, "Exemple concret de supervision", 0.6, 5.22, 12, 0.35, size=12, bold=True, color=DARK)
rect(slide, 0.6, 5.6, 12.1, 1.25, YELLOW_L, YELLOW, 0.8)
txt(slide,
    "L'IA a généré un test qui importait bcrypt directement → erreur native node-gyp (module C++) au runtime.\n"
    "Le développeur a identifié la cause (chaîne d'imports transitifs) et décidé la stratégie :\n"
    "jest.mock('bcrypt') + jest.mock('typeorm') au niveau module → problème résolu. Couverture : 45% → 78%.",
    0.75, 5.65, 11.8, 1.1, size=10, color=DARK)

txt(slide, "© DataShare 2026", 0.4, 7.1, 12.5, 0.32, size=9, color=GRAY, align=PP_ALIGN.CENTER)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 11 — Documentation API + Postman
# ═══════════════════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
gradient_bg(slide)
card(slide, 0.4, 0.15, 12.5, 7.15)
slide_header(slide, "Documentation API — 9 Endpoints",
             "REST · JWT Bearer · Collection Postman fournie avec tests automatisés")

rect(slide, 0.55, 1.28, 12.1, 0.38, DARK)
for j, h in enumerate(["Méthode", "Endpoint", "Auth", "Corps / Params", "Réponses clés"]):
    xh = [0.58, 1.55, 5.55, 6.85, 9.85][j]
    wh = [0.9,  3.9,  1.2,  2.9,  2.9][j]
    txt(slide, h, xh, 1.32, wh, 0.28, size=9, bold=True, color=WHITE)

endpoints = [
    ("POST",   "/auth/register",         "Non", "email, username, password",       "201 profil · 409 email dupliqué · 400 validation"),
    ("POST",   "/auth/login",            "Non", "email, password",                 "200 {access_token, user} · 401 identifiants"),
    ("GET",    "/auth/me",               "JWT", "—",                               "200 profil · 401 sans token"),
    ("GET",    "/files",                 "JWT", "—",                               "200 [] fichiers · 401 sans token"),
    ("POST",   "/files/upload",          "JWT", "file (multipart), expiry_hours, password", "201 share_url · 403 extension interdite"),
    ("POST",   "/files/upload/anonymous","Non", "file (multipart), expiry_hours",  "201 share_url · 403 extension interdite"),
    ("GET",    "/files/share/:token",    "Non", "token (URL param)",               "200 métadonnées · 404 token inconnu"),
    ("GET",    "/files/download/:token", "Non", "token (URL), password (query)",   "200 fichier binaire · 410 expiré · 403 mdp"),
    ("DELETE", "/files/:id",             "JWT", "id (URL param)",                  "200 supprimé · 404 pas propriétaire · 401"),
]

METHOD_COLORS = {"GET": BLUE, "POST": GREEN, "DELETE": RED}

for i, (method, path, auth, body, resp) in enumerate(endpoints):
    y = 1.72 + i * 0.575
    bg = LIGHT_GRAY if i % 2 == 0 else WHITE
    rect(slide, 0.55, y, 12.1, 0.55, bg)
    mc = METHOD_COLORS.get(method, ORANGE)
    rect(slide, 0.58, y+0.08, 0.88, 0.36, mc)
    txt(slide, method, 0.6, y+0.12, 0.84, 0.28, size=8, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    txt(slide, path,   1.55, y+0.12, 3.9,  0.34, size=8, bold=True, color=DARK)
    ac = GREEN if auth == "JWT" else GRAY
    txt(slide, auth,   5.55, y+0.12, 1.2,  0.34, size=8, bold=True, color=ac, align=PP_ALIGN.CENTER)
    txt(slide, body,   6.85, y+0.12, 2.9,  0.34, size=7, color=DARK)
    txt(slide, resp,   9.85, y+0.12, 2.9,  0.34, size=7, color=DARK)

rect(slide, 0.6, 7.0, 12.1, 0.06, RGBColor(0xE0, 0xE0, 0xE0))
txt(slide, "Collection Postman complète avec tests automatisés : docs/datashare.postman_collection.json",
    0.6, 7.06, 12.1, 0.35, size=9, bold=True, color=ORANGE, italic=True, align=PP_ALIGN.CENTER)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 12 — Questions pièges — Mentor sadique
# ═══════════════════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
gradient_bg(slide)
card(slide, 0.4, 0.15, 12.5, 7.15)
slide_header(slide, "Questions techniques — Soyez prêt",
             "Concepts que tout développeur senior doit maîtriser")

qa = [
    ("Pourquoi bcrypt coût 12 ?",
     "Coût = nombre d'itérations = 2^12 = 4096. Chaque +1 double le temps. "
     "Coût 12 ≈ 250ms/hash — trop lent pour brute-force (400k tentatives/jour max), imperceptible à l'humain."),
    ("C'est quoi un UUID v4 ?",
     "Identifiant universel unique de 128 bits généré aléatoirement. "
     "Probabilité de collision : 1 sur 5,3×10^36. Impossible à deviner ou itérer. "
     "Utilisé comme share_token pour les liens de partage."),
    ("Pourquoi JWT stateless ?",
     "Le serveur ne stocke aucune session. Chaque requête porte le token signé. "
     "Avantage : scalabilité horizontale (plusieurs serveurs). "
     "Inconvénient : révocation impossible avant expiration → durée 7j acceptable pour MVP."),
    ("C'est quoi un mock dans les tests ?",
     "Un faux objet qui simule le comportement d'une vraie dépendance. "
     "Ex : jest.fn() remplace le Repository TypeORM → pas besoin de BDD réelle. "
     "Avantage : tests rapides, reproductibles, isolés."),
    ("Différence test unitaire / intégration / E2E ?",
     "Unitaire : une fonction, tout mocké. Intégration : plusieurs composants, BDD réelle. "
     "E2E : application complète, navigateur réel, parcours utilisateur de bout en bout."),
    ("Pourquoi PostgreSQL plutôt que MongoDB ?",
     "Données structurées avec relations (User → SharedFile). "
     "PostgreSQL = ACID, UUID natif, index FK performants. "
     "MongoDB utile pour données non structurées ou schéma variable — pas notre cas."),
]

for i, (q, a) in enumerate(qa):
    col = i % 2
    row = i // 2
    x = 0.55 + col * 6.35
    y = 1.38 + row * 1.8
    rect(slide, x, y, 6.1, 1.65, LIGHT_GRAY, ORANGE, 0.8)
    rect(slide, x, y, 6.1, 0.35, ORANGE)
    txt(slide, q, x+0.12, y+0.05, 5.85, 0.26, size=9, bold=True, color=WHITE)
    txt(slide, a, x+0.12, y+0.42, 5.85, 1.15, size=9, color=DARK)

txt(slide, "© DataShare 2026", 0.4, 7.1, 12.5, 0.32, size=9, color=GRAY, align=PP_ALIGN.CENTER)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 13 — Questions Chef de Projet SI
# ═══════════════════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
gradient_bg(slide)
card(slide, 0.4, 0.15, 12.5, 7.15)
slide_header(slide, "Vos réponses — Chef de projet SI",
             "Livrables, traçabilité, onboarding, incidents")

qa_pm = [
    ("Comment un nouveau développeur prend-il le projet en main ?",
     "README détaillé : prérequis, docker compose up -d, accès http://localhost:5173. "
     "Entité, routes, variables d'env, procédures maintenance — tout documenté. "
     "Temps estimé d'onboarding : < 30 minutes."),
    ("Où est la documentation API ? Comment tester sans interface ?",
     "Collection Postman complète (docs/datashare.postman_collection.json) avec 10 requêtes "
     "et tests automatisés Postman. Importable en 1 clic, variable {{token}} auto-injectée."),
    ("Comment je sais que l'application fonctionne en production ?",
     "docker compose ps → état des 3 services. "
     "docker compose logs -f backend → logs NestJS temps réel. "
     "MAINTENANCE.md : procédures surveillance, sauvegardes, métriques."),
    ("Quelle est la stratégie de backup des données ?",
     "Base : pg_dump via docker compose exec → fichier SQL horodaté. "
     "Fichiers uploadés : volume Docker uploads_data → tar.gz. "
     "Procédure complète dans MAINTENANCE.md avec commandes prêtes à l'emploi."),
    ("Comment gérer une mise à jour de dépendance critique ?",
     "npm audit hebdomadaire (Dependabot recommandé). "
     "Patch : immédiat. Minor : mensuel. Major : trimestriel après tests sur branche dédiée. "
     "npm test après chaque mise à jour — 32 tests de régression."),
    ("Quel est le délai de prise en charge d'un incident ?",
     "MAINTENANCE.md définit les procédures. Logs accessibles immédiatement. "
     "Architecture Docker : redémarrage service en < 30s. "
     "Purge automatique des fichiers expirés toutes les 24h — opération transparente."),
]

for i, (q, a) in enumerate(qa_pm):
    col = i % 2
    row = i // 2
    x = 0.55 + col * 6.35
    y = 1.38 + row * 1.8
    rect(slide, x, y, 6.1, 1.65, LIGHT_GRAY, BLUE, 0.8)
    rect(slide, x, y, 6.1, 0.35, BLUE)
    txt(slide, q, x+0.12, y+0.05, 5.85, 0.26, size=9, bold=True, color=WHITE)
    txt(slide, a, x+0.12, y+0.42, 5.85, 1.15, size=9, color=DARK)

txt(slide, "© DataShare 2026", 0.4, 7.1, 12.5, 0.32, size=9, color=GRAY, align=PP_ALIGN.CENTER)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 14 — Questions Architecte logiciel
# ═══════════════════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
gradient_bg(slide)
card(slide, 0.4, 0.15, 12.5, 7.15)
slide_header(slide, "Vos réponses — Architecte logiciel",
             "Choix d'architecture, scalabilité, sécurité, dette technique")

qa_arch = [
    ("synchronize: true en prod c'est une bombe à retardement ?",
     "Oui, assumé. En dev : synchronize:true crée les tables automatiquement. "
     "En prod : synchronize:false + migrations TypeORM explicites. "
     "MAINTENANCE.md documente la procédure. Commandé dans la checklist prod."),
    ("Pas de pagination sur GET /files → problème à 10 000 fichiers ?",
     "Oui, limite identifiée. Pour le MVP, un utilisateur a en général < 50 fichiers actifs "
     "(expiration 7j). La pagination est documentée dans la roadmap court terme. "
     "Index sur owner_id en place pour la requête — latence actuelle : 7ms."),
    ("JWT 7 jours sans refresh token — si volé, 7 jours d'accès ?",
     "Risque accepté pour le MVP. Mitigations en place : bcrypt + validation stricte. "
     "En production : refresh token court (15min) + rotation JWT documentée dans SECURITY.md. "
     "localStorage → cookies httpOnly en prod pour limiter le vecteur XSS."),
    ("Disque local — single point of failure ?",
     "Oui, assumé pour un prototype local. Volume Docker uploads_data est persistant. "
     "Migration vers AWS S3 documentée dans PERF.md — UPLOAD_DIR isole cette dépendance. "
     "Changement = 1 variable d'env + 1 module NestJS, sans réécriture."),
    ("Pourquoi NestJS et pas Spring Boot ou .NET Core ?",
     "TypeScript full-stack = cohérence frontend/backend, un seul langage à maîtriser. "
     "NestJS = modules, DI, Guards, Decorators — architecture similaire à Spring. "
     "Écosystème npm : bcrypt, passport-jwt, typeorm — maturité prouvée en production."),
    ("CORS en dur sur localhost — comment passer en prod ?",
     "FRONTEND_URL est une variable d'environnement, pas hardcodée. "
     "En prod : FRONTEND_URL=https://datashare.mondomaine.com dans .env. "
     "Aucune modification de code requise — 12-factor app compliant."),
]

for i, (q, a) in enumerate(qa_arch):
    col = i % 2
    row = i // 2
    x = 0.55 + col * 6.35
    y = 1.38 + row * 1.8
    rect(slide, x, y, 6.1, 1.65, LIGHT_GRAY, PURPLE, 0.8)
    rect(slide, x, y, 6.1, 0.35, PURPLE)
    txt(slide, q, x+0.12, y+0.05, 5.85, 0.26, size=9, bold=True, color=WHITE)
    txt(slide, a, x+0.12, y+0.42, 5.85, 1.15, size=9, color=DARK)

txt(slide, "© DataShare 2026", 0.4, 7.1, 12.5, 0.32, size=9, color=GRAY, align=PP_ALIGN.CENTER)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 15 — Démo live
# ═══════════════════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
gradient_bg(slide)

txt(slide, "Démonstration en direct", 1, 1.3, 11, 1.2,
    size=42, bold=True, color=DARK, align=PP_ALIGN.CENTER)
rect(slide, 3.5, 2.7, 6.3, 0.07, WHITE)

txt(slide, "3 flows à parcourir ensemble",
    1, 2.88, 11, 0.6, size=18, color=DARK, align=PP_ALIGN.CENTER, italic=True)

flows = [
    ("1", "Inscription", "Créer un compte → dashboard"),
    ("2", "Upload",      "Déposer un fichier → obtenir le lien"),
    ("3", "Partage",     "Ouvrir le lien → télécharger le fichier"),
]
for i, (num, titre, desc) in enumerate(flows):
    x = 1.5 + i * 3.5
    s = slide.shapes.add_shape(1, Inches(x), Inches(3.6), Inches(2.9), Inches(1.8))
    s.fill.solid()
    s.fill.fore_color.rgb = RGBColor(0x00, 0x00, 0x00)
    s.fill.transparency = 0.25
    s.line.fill.background()
    txt(slide, num,   x+0.1, 3.65, 2.7, 0.55, size=28, bold=True,
        color=ORANGE, align=PP_ALIGN.CENTER)
    txt(slide, titre, x+0.1, 4.18, 2.7, 0.42, size=14, bold=True,
        color=WHITE,  align=PP_ALIGN.CENTER)
    txt(slide, desc,  x+0.1, 4.6,  2.7, 0.72, size=10,
        color=ACCENT, align=PP_ALIGN.CENTER)

txt(slide, "http://localhost:5173",
    1, 5.8, 11, 0.6, size=16, color=DARK, align=PP_ALIGN.CENTER, italic=True)

txt(slide, "© DataShare 2026", 0.5, 7.1, 12, 0.35,
    size=9, color=WHITE, align=PP_ALIGN.CENTER)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 16 — Roadmap & Vision
# ═══════════════════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
gradient_bg(slide)
card(slide, 0.4, 0.15, 12.5, 7.15)
slide_header(slide, "Roadmap & Vision",
             "Evolutions post-MVP — de l'auto-hébergement au SaaS")

rect(slide, 0.6, 1.4, 5.9, 0.42, ORANGE)
txt(slide, "Court terme (1-3 mois)", 0.72, 1.46, 5.7, 0.3, size=12, bold=True, color=WHITE)
bullets(slide, [
    "Rate limiting sur /auth — protection brute-force",
    "HTTPS + HSTS en production (Nginx + Let's Encrypt)",
    "Cookies httpOnly à la place de localStorage",
    "Notifications email à l'expiration des fichiers",
    "Interface admin pour gérer les utilisateurs",
], 0.6, 1.88, 5.9, size=11, color=DARK, spacing=4)

rect(slide, 6.8, 1.4, 5.9, 0.42, BLUE)
txt(slide, "Moyen terme (3-6 mois)", 6.92, 1.46, 5.7, 0.3, size=12, bold=True, color=WHITE)
bullets(slide, [
    "Stockage AWS S3 — scalabilité et fiabilité",
    "Chiffrement AES-256 des fichiers au repos",
    "Scan antivirus des uploads (ClamAV)",
    "API publique documentée (OpenAPI 3.0)",
    "Dashboard analytics pour les administrateurs",
], 6.8, 1.88, 5.9, size=11, color=DARK, spacing=4)

rect(slide, 0.6, 4.35, 12.1, 0.42, DARK)
txt(slide, "Vision long terme", 0.72, 4.41, 12, 0.3, size=12, bold=True, color=WHITE)
bullets(slide, [
    "Mode SaaS : facturation par usage, plans freemium / pro / entreprise",
    "Application mobile React Native — partage depuis smartphone",
    "Intégrations : Slack, Teams, Notion, Zapier",
    "Conformité SOC 2 / ISO 27001 pour les clients entreprise",
], 0.6, 4.83, 12.1, size=11, color=DARK, spacing=4)

txt(slide,
    "Architecture NestJS modulaire : chaque évolution s'ajoute comme un nouveau module sans réécriture",
    0.6, 7.05, 12.1, 0.4, size=10, bold=True, color=ORANGE, italic=True)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 17 — Conclusion
# ═══════════════════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
gradient_bg(slide)

txt(slide, "DataShare", 1, 0.9, 11, 1.4,
    size=62, bold=True, color=DARK, align=PP_ALIGN.CENTER)
rect(slide, 3.8, 2.4, 5.7, 0.07, WHITE)
txt(slide, "MVP fonctionnel livré",
    1, 2.6, 11, 0.7, size=26, bold=True, color=DARK, align=PP_ALIGN.CENTER)

conclusions = [
    ("MVP fonctionnel",         "9 User Stories · démo prête · Docker Compose"),
    ("Architecture extensible", "NestJS modulaire · prêt pour S3, microservices, SaaS"),
    ("Code documenté & testé",  "32 tests Jest · 78% couverture · 11 E2E Playwright"),
    ("Prêt investisseurs",      "Demo live · roadmap claire · compromis documentés"),
]
for i, (titre, desc) in enumerate(conclusions):
    col = i % 2
    row = i // 2
    x = 0.9 + col * 5.8
    y = 3.5 + row * 1.45
    s = slide.shapes.add_shape(1, Inches(x), Inches(y), Inches(5.4), Inches(1.25))
    s.fill.solid()
    s.fill.fore_color.rgb = RGBColor(0x00, 0x00, 0x00)
    s.fill.transparency = 0.25
    s.line.fill.background()
    txt(slide, "✅ " + titre, x+0.15, y+0.1, 5.1, 0.4, size=13, bold=True,
        color=WHITE, align=PP_ALIGN.LEFT)
    txt(slide, desc, x+0.15, y+0.55, 5.1, 0.6, size=10,
        color=ACCENT)

txt(slide, "© DataShare 2026 — Prototype MVP — Prêt pour investisseurs",
    0.5, 7.1, 12, 0.35, size=9, color=WHITE, align=PP_ALIGN.CENTER)


# ── Export ────────────────────────────────────────────────────────────────────
import os
output = "docs/presentation_datashare_v2.pptx"
os.makedirs("docs", exist_ok=True)
prs.save(output)
print(f"PowerPoint genere : {output}")
