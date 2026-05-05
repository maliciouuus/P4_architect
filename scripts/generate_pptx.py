#!/usr/bin/env python3
"""Génère le support de présentation DataShare au format PowerPoint."""

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

txt(slide, "DataShare", 1, 1.2, 11, 1.6,
    size=72, bold=True, color=DARK, align=PP_ALIGN.CENTER)
rect(slide, 4.2, 2.95, 4.9, 0.07, WHITE)
txt(slide, "Plateforme de transfert sécurisé de fichiers",
    1, 3.1, 11, 0.8, size=20, color=DARK, align=PP_ALIGN.CENTER)
txt(slide, "MVP · Référent technique senior · Avril 2026",
    1, 4.0, 11, 0.6, size=14, color=DARK, align=PP_ALIGN.CENTER, italic=True)

for i, (label, val) in enumerate([
    ("Tests", "38 ✓"), ("Couverture", "99 %"), ("Vulnérabilités", "0")
]):
    x = 2.5 + i * 3.0
    rect(slide, x, 5.0, 2.5, 1.1, RGBColor(0x00, 0x00, 0x00))
    s = slide.shapes.add_shape(1, Inches(x), Inches(5.0),
                                Inches(2.5), Inches(1.1))
    s.fill.solid(); s.fill.fore_color.rgb = RGBColor(0x00, 0x00, 0x00)
    s.fill.transparency = 0.25; s.line.fill.background()
    txt(slide, val,   x+0.1, 5.05, 2.3, 0.6, size=22, bold=True,
        color=WHITE, align=PP_ALIGN.CENTER)
    txt(slide, label, x+0.1, 5.65, 2.3, 0.4, size=10,
        color=ACCENT, align=PP_ALIGN.CENTER)

txt(slide, "© DataShare 2026", 0.5, 7.1, 12, 0.35,
    size=9, color=WHITE, align=PP_ALIGN.CENTER)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 2 — Contexte & besoin
# ═══════════════════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
gradient_bg(slide)
card(slide, 0.4, 0.15, 12.5, 7.15)
slide_header(slide, "Contexte & besoin",
             "Pourquoi DataShare ? Quel problème résout-on ?")

txt(slide, "Le problème", 0.7, 1.35, 6, 0.45, size=14, bold=True, color=ORANGE)
bullets(slide, [
    "Envoyer un fichier lourd par email → pièce jointe refusée (limite 25 Mo)",
    "WeTransfer / Dropbox → compte obligatoire, lenteur, publicité",
    "FTP / serveur partagé → configuration complexe, pas accessible à tous",
    "Google Drive → dépendance Google, interface lourde pour un simple envoi",
], 0.7, 1.82, 5.8, size=12, color=DARK)

txt(slide, "La solution DataShare", 7.0, 1.35, 5.8, 0.45, size=14, bold=True, color=ORANGE)
bullets(slide, [
    "Dépôt en 3 clics, lien prêt en secondes",
    "Lien unique non prédictible (UUID v4)",
    "Expiration automatique (jusqu'à 7 jours)",
    "Protection optionnelle par mot de passe",
    "Historique personnel pour les comptes",
    "Installation autonome en 1 commande Docker",
], 7.0, 1.82, 5.8, size=12, color=DARK)

rect(slide, 0.6, 4.15, 12.1, 0.05, RGBColor(0xE8, 0xE8, 0xE8))
txt(slide, "Périmètre MVP — User Stories implémentées",
    0.6, 4.25, 12, 0.4, size=13, bold=True, color=DARK)

us_items = [
    ("US01", "Upload avec compte", GREEN),
    ("US02", "Téléchargement via lien", GREEN),
    ("US03", "Création de compte", GREEN),
    ("US04", "Connexion utilisateur", GREEN),
    ("US05", "Historique des fichiers", GREEN),
    ("US06", "Suppression fichier", GREEN),
    ("US09", "Mot de passe fichier", GREEN),
    ("US10", "Expiration auto", GREEN),
]
for i, (code, label, color) in enumerate(us_items):
    col = i % 4
    row = i // 4
    x = 0.6 + col * 3.05
    y = 4.75 + row * 0.85
    rect(slide, x, y, 2.8, 0.65, GREEN_L, GREEN, 0.8)
    txt(slide, f"✅ {code}", x+0.12, y+0.05, 1.0, 0.3,
        size=10, bold=True, color=GREEN_DARK)
    txt(slide, label, x+0.12, y+0.33, 2.55, 0.28, size=10, color=DARK)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 3 — Pourquoi Python / Django ?
# ═══════════════════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
gradient_bg(slide)
card(slide, 0.4, 0.15, 12.5, 7.15)
slide_header(slide, "Pourquoi Python / Django ?",
             "Choix argumenté face aux stacks de référence du cahier des charges")

# Intro
txt(slide,
    "Le cahier des charges liste Spring Boot, .NET Core, NestJS et PHP à titre d'exemples. "
    "Python / Django a été retenu car il satisfait tous les critères techniques — et va au-delà.",
    0.7, 1.25, 12, 0.55, size=11, color=GRAY, italic=True)

# Comparaison Django vs NestJS (le plus proche)
headers_cmp = ["Critère", "NestJS (TypeScript)", "Django (Python) ✓"]
col_w_cmp   = [3.5, 3.8, 4.3]
col_x_cmp   = [0.6, 4.1, 7.9]

for j, (h, w, x) in enumerate(zip(headers_cmp, col_w_cmp, col_x_cmp)):
    bg = ORANGE if j > 0 else RGBColor(0x37, 0x41, 0x51)
    rect(slide, x, 1.9, w - 0.05, 0.42, bg)
    txt(slide, h, x+0.12, 1.95, w-0.2, 0.32,
        size=11, bold=True, color=WHITE)

rows_cmp = [
    ("Architecture REST",        "✓ NestJS Controllers",         "✓ DRF ViewSets — plus mature (2011)"),
    ("Authentification JWT",     "✓ @nestjs/jwt",                "✓ simplejwt — 10M+ installs/mois"),
    ("ORM & migrations",         "TypeORM (config lourde)",      "✓ Django ORM intégré — zéro config"),
    ("Tests intégrés",           "Jest (setup manuel)",          "✓ pytest-django — fixtures natives"),
    ("Sécurité by default",      "À configurer manuellement",    "✓ CSRF, XSS, SQLi protégés nativement"),
    ("Utilisé en production par","ADP, Adidas",                  "✓ Instagram, Pinterest, Mozilla, NASA"),
    ("Maturité",                 "2017 — 7 ans",                 "✓ 2005 — 20 ans de battle-testing"),
]

for i, (crit, nest, django) in enumerate(rows_cmp):
    y = 2.37 + i * 0.56
    bg = LIGHT_GRAY if i % 2 == 0 else WHITE
    for w, x in zip(col_w_cmp, col_x_cmp):
        rect(slide, x, y, w-0.05, 0.52, bg)
    txt(slide, crit,   col_x_cmp[0]+0.12, y+0.08, col_w_cmp[0]-0.2, 0.36, size=10, bold=True, color=DARK)
    txt(slide, nest,   col_x_cmp[1]+0.12, y+0.08, col_w_cmp[1]-0.2, 0.36, size=10, color=GRAY)
    txt(slide, django, col_x_cmp[2]+0.12, y+0.08, col_w_cmp[2]-0.2, 0.36, size=10, color=GREEN_DARK, bold=True)

txt(slide,
    "Conclusion : Django répond à 100 % des exigences techniques du cahier des charges "
    "avec une productivité supérieure pour un MVP sous contrainte de temps.",
    0.6, 7.0, 12.1, 0.4, size=10, bold=True, color=ORANGE, italic=True)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 4 — Choix technologiques (tableau complet)
# ═══════════════════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
gradient_bg(slide)
card(slide, 0.4, 0.15, 12.5, 7.15)
slide_header(slide, "Choix technologiques justifiés")

headers_t = ["Composant", "Technologie", "Alternative écartée", "Justification clé"]
col_w_t   = [2.0, 2.2, 2.2, 5.7]
col_x_t   = [0.55, 2.55, 4.75, 6.95]

for j, (h, w, x) in enumerate(zip(headers_t, col_w_t, col_x_t)):
    rect(slide, x, 1.2, w-0.05, 0.42, ORANGE)
    txt(slide, h, x+0.1, 1.25, w-0.15, 0.32, size=11, bold=True, color=WHITE)

rows_t = [
    ("Back-end",        "Python 3.12\n+ Django 5.2",  "NestJS, Spring",   "Batteries incluses, ORM natif, 20 ans de maturité, productivité ×3 sur un MVP"),
    ("API REST",        "Django REST\nFramework",      "FastAPI",          "Le plus utilisé avec Django (10M+ téléch/mois), sérialiseurs + permissions intégrés"),
    ("Authentification","JWT simplejwt", "Sessions, OAuth2", "Stateless, compatible SPA, rotation automatique du refresh token"),
    ("Front-end",       "Vue.js 3 + Vite","React, Angular",  "Composition API puissante, Pinia natif, bundle 139 Ko, courbe d'apprentissage douce"),
    ("Base de données", "PostgreSQL 16", "MySQL, SQLite",    "UUID natif, JSONB, transactions ACID, standard professionnel, Docker officiel"),
    ("Stockage fichiers","Disque local", "AWS S3",           "Suffisant pour le MVP, migration S3 documentée et prévue pour la production"),
    ("Infrastructure",  "Docker Compose","Déploiement manuel","Reproductibilité totale, installation en 1 commande, isolation des services"),
    ("Tests back",      "pytest + pytest-django","unittest", "Syntaxe concise, fixtures puissantes, plugins Django, couverture HTML intégrée"),
]

for i, (comp, tech, alt, just) in enumerate(rows_t):
    y = 1.67 + i * 0.615
    bg = LIGHT_GRAY if i % 2 == 0 else WHITE
    for w, x in zip(col_w_t, col_x_t):
        rect(slide, x, y, w-0.05, 0.59, bg)
    txt(slide, comp, col_x_t[0]+0.1, y+0.06, col_w_t[0]-0.15, 0.48, size=10, bold=True, color=DARK)
    txt(slide, tech, col_x_t[1]+0.1, y+0.06, col_w_t[1]-0.15, 0.48, size=10, bold=True, color=ORANGE)
    txt(slide, alt,  col_x_t[2]+0.1, y+0.06, col_w_t[2]-0.15, 0.48, size=10, color=GRAY, italic=True)
    txt(slide, just, col_x_t[3]+0.1, y+0.06, col_w_t[3]-0.15, 0.48, size=10, color=DARK)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 5 — Architecture
# ═══════════════════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
gradient_bg(slide)
card(slide, 0.4, 0.15, 12.5, 7.15)
slide_header(slide, "Architecture de la solution",
             "Client-serveur découplé · Docker Compose · 3 services")

boxes = [
    (0.55, 1.45, 3.5, 2.1, "Navigateur",
     "Vue.js 3 SPA\nVue Router — 5 pages\nPinia (state)\nAxios (HTTP client)", BLUE_L, BLUE),
    (4.85, 1.45, 3.7, 2.1, "API REST",
     "Django 5.2 + DRF\n/api/auth/  /api/files/\nJWT · CORS · PBKDF2\nLogging structuré", CARD_BG, ORANGE),
    (9.25, 1.45, 3.6, 2.1, "Stockage",
     "PostgreSQL 16\nTables : users + files\nDisque local /media/\nVolumes Docker", GREEN_L, GREEN),
]
for x, y, w, h, titre, desc, bg, border in boxes:
    rect(slide, x, y, w, h, bg, border, 1.5)
    txt(slide, titre, x+0.15, y+0.08, w-0.3, 0.38,
        size=13, bold=True, color=DARK)
    txt(slide, desc,  x+0.15, y+0.5,  w-0.3, 1.5,
        size=10, color=DARK)

# Flèches
txt(slide, "HTTP/JSON\nJWT Bearer →", 4.0, 2.0, 0.9, 0.8, size=9, color=GRAY, align=PP_ALIGN.CENTER)
txt(slide, "ORM Django\nSQL →",        8.6, 2.0, 0.7, 0.8, size=9, color=GRAY, align=PP_ALIGN.CENTER)

# Bande Docker
rect(slide, 0.55, 3.7, 12.3, 0.06, RGBColor(0xE0, 0xE0, 0xE0))
txt(slide, "Docker Compose — réseau interne · volumes persistants postgres_data & media_data",
    0.55, 3.82, 12.3, 0.38, size=10, color=GRAY, italic=True, align=PP_ALIGN.CENTER)

# Flux
txt(slide, "Flux principaux", 0.6, 4.3, 12, 0.4, size=13, bold=True, color=DARK)
flux = [
    ("Authentification",
     "POST /api/auth/login/ → access token 1h + refresh 7j → localStorage → injecté dans chaque requête via intercepteur Axios"),
    ("Upload",
     "Sélection fichier (max 1 Go) → validation client + serveur → multipart POST → stockage disque → UUID token → share_url retourné"),
    ("Partage / Téléchargement",
     "Lien /download/<uuid> → GET infos publiques → saisie MDP si protégé → GET download → Content-Disposition natif"),
]
for i, (titre, desc) in enumerate(flux):
    y = 4.75 + i * 0.75
    rect(slide, 0.6, y, 2.5, 0.55, CARD_BG, ORANGE, 0.8)
    txt(slide, titre, 0.7, y+0.08, 2.3, 0.38, size=10, bold=True, color=ORANGE)
    txt(slide, desc,  3.2, y+0.08, 9.7, 0.48, size=10, color=DARK)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 6 — Modèle de données
# ═══════════════════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
gradient_bg(slide)
card(slide, 0.4, 0.15, 12.5, 7.15)
slide_header(slide, "Modèle de données",
             "2 tables · relation 1-N · sécurité by design")

# USER
rect(slide, 0.6, 1.35, 4.6, 0.45, BLUE)
txt(slide, "USER  (Django built-in)",
    0.7, 1.4, 4.4, 0.35, size=12, bold=True, color=WHITE)

user_f = [
    ("id",          "INTEGER PK"),
    ("username",    "VARCHAR(150)"),
    ("email",       "VARCHAR(254) — unique"),
    ("password",    "VARCHAR(128) — PBKDF2+SHA256"),
    ("date_joined", "DATETIME — auto"),
    ("is_active",   "BOOLEAN"),
]
for i, (f, t) in enumerate(user_f):
    bg = LIGHT_GRAY if i % 2 == 0 else WHITE
    rect(slide, 0.6, 1.82+i*0.46, 4.6, 0.44, bg)
    txt(slide, f, 0.75, 1.88+i*0.46, 1.8, 0.32, size=10, bold=True, color=DARK)
    txt(slide, t, 2.55, 1.88+i*0.46, 2.5, 0.32, size=10, color=GRAY)

txt(slide, "1 ──── N", 5.35, 3.2, 1.4, 0.55,
    size=13, bold=True, color=ORANGE, align=PP_ALIGN.CENTER)

# SHAREDFILE
rect(slide, 6.85, 1.35, 6.0, 0.45, ORANGE)
txt(slide, "SHAREDFILE",
    6.95, 1.4, 5.8, 0.35, size=12, bold=True, color=WHITE)

sf_f = [
    ("id",            "UUID PK",          "Identifiant interne non exposé"),
    ("owner_id",      "FK → User",        "Isolation stricte par propriétaire"),
    ("original_name", "VARCHAR(255)",     "Nom conservé pour téléchargement"),
    ("file",          "FileField",        "uploads/<uid>/<uuid>_<name>"),
    ("size",          "BIGINT",           "En octets, affiché côté client"),
    ("content_type",  "VARCHAR(100)",     "MIME type → header Content-Type"),
    ("share_token",   "UUID UNIQUE",      "128 bits — non devinable par brute force"),
    ("expires_at",    "DATETIME",         "Défaut : J+7, max 7 jours"),
    ("password_hash", "VARCHAR(255)",     "PBKDF2 ou vide si pas de protection"),
    ("created_at",    "DATETIME auto",    "Timestamp upload"),
]
for i, (f, t, role) in enumerate(sf_f):
    bg = LIGHT_GRAY if i % 2 == 0 else WHITE
    rect(slide, 6.85, 1.82+i*0.46, 6.0, 0.44, bg)
    txt(slide, f,    6.98, 1.88+i*0.46, 2.0, 0.32, size=10, bold=True, color=DARK)
    txt(slide, t,    8.98, 1.88+i*0.46, 1.5, 0.32, size=10, color=ORANGE)
    txt(slide, role, 10.5, 1.88+i*0.46, 2.2, 0.32, size=9,  color=GRAY, italic=True)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 7 — Sécurité
# ═══════════════════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
gradient_bg(slide)
card(slide, 0.4, 0.15, 12.5, 7.15)
slide_header(slide, "Sécurité — défense en profondeur",
             "Chaque couche est protégée indépendamment")

sec_cols = [
    ("Authentification JWT", [
        "Access token : 1h · HS256",
        "Refresh token : 7j · rotation",
        "Header Authorization: Bearer",
        "Aucun token en cookie → simplifié",
        "Prod : migration httpOnly cookie prévue",
    ]),
    ("Données & mots de passe", [
        "MDP utilisateur : PBKDF2-SHA256",
        "MDP fichier : PBKDF2-SHA256",
        "Jamais stocké en clair — jamais loggé",
        "8 validateurs Django activés",
        "Rejet MDP trop courts ou courants",
    ]),
    ("Accès & isolation", [
        "owner=request.user sur TOUTES les vues",
        "UUID v4 pour share_token (128 bits)",
        "410 Gone sur lien expiré",
        "403 sur mauvais MDP fichier",
        "CORS : origines explicites, pas de *",
    ]),
    ("Infrastructure", [
        "Limite upload : 1 Go côté serveur",
        "X-Content-Type-Options activé",
        "X-Frame-Options activé",
        "pip-audit : 0 vulnérabilité applicative",
        "Dépendances : 9 alertes système hôte seulement",
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
            x+0.2, y+0.52, 5.5, size=11, color=DARK, spacing=3)

txt(slide,
    "Prochain niveau prod : HTTPS + HSTS · httpOnly cookies · Rate limiting sur /auth/ · Stockage S3 avec URLs signées",
    0.6, 7.08, 12.1, 0.38, size=10, color=GRAY, italic=True)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 8 — Conformité aux specs
# ═══════════════════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
gradient_bg(slide)
card(slide, 0.4, 0.15, 12.5, 7.15)
slide_header(slide, "Conformité au cahier des charges",
             "Toutes les exigences MVP + bonus vérifiés")

conformite = [
    # (exigence, statut, détail)
    ("US01 Upload avec compte",         True,  "Fichier jusqu'à 1 Go · MDP optionnel · expiration 1-7j"),
    ("US02 Téléchargement via lien",    True,  "UUID v4 · métadonnées publiques · 410 si expiré"),
    ("US03 Création de compte",         True,  "Email unique · PBKDF2 · 8 validateurs"),
    ("US04 Connexion JWT",              True,  "Access 1h + refresh 7j · rotation activée"),
    ("US05 Historique fichiers",        True,  "Nom, taille, date, état · isolation utilisateur"),
    ("US06 Suppression fichier",        True,  "Physique + BDD · confirmation front · 404 si fichier d'autrui"),
    ("US09 Mot de passe fichier",       True,  "PBKDF2 · min 6 car. · jamais en clair"),
    ("US10 Expiration automatique",     True,  "Défaut 7j · configurable 1-7j · 410 à expiration"),
    ("Architecture REST API",           True,  "DRF · OpenAPI 3.0 · JSON"),
    ("Authentification JWT",            True,  "simplejwt · stateless · compatible SPA"),
    ("Tests unitaires (objectif 70%)",  True,  "38 tests · 99% de couverture backend"),
    ("Tests E2E (2-3 scénarios min.)",  True,  "10 tests Playwright sur navigateur Chromium réel"),
    ("TESTING / SECURITY / PERF / MAINTENANCE", True, "4 fichiers présents et documentés"),
    ("Installation Docker",             True,  "docker compose up -d · migrations auto"),
    ("Conventional commits",            True,  "feat / fix / docs / test / chore"),
]

for i, (label, ok, detail) in enumerate(conformite):
    col = i % 2
    row = i // 2
    x = 0.55 + col * 6.2
    y = 1.3 + row * 0.73
    bg = GREEN_L if ok else RED_L
    border = GREEN if ok else RED
    rect(slide, x, y, 6.0, 0.65, bg, border, 0.7)
    icon = "✅" if ok else "❌"
    txt(slide, icon,   x+0.1,  y+0.08, 0.5, 0.48, size=12, align=PP_ALIGN.CENTER)
    txt(slide, label,  x+0.65, y+0.04, 3.5, 0.28, size=10, bold=True, color=DARK)
    txt(slide, detail, x+0.65, y+0.32, 5.2, 0.28, size=9,  color=GRAY, italic=True)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 9 — Qualité & Tests
# ═══════════════════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
gradient_bg(slide)
card(slide, 0.4, 0.15, 12.5, 7.15)
slide_header(slide, "Qualité & Tests",
             "Pyramide de tests · objectif 70% → atteint 99%")

# Métriques
metrics = [
    ("38", "tests unitaires\n& intégration", ORANGE),
    ("10", "tests E2E\nPlaywright", BLUE),
    ("99 %", "couverture\nbackend", GREEN),
    ("0", "vulnérabilité\napplicative", GREEN),
    ("139 Ko", "bundle JS\nprod gzip 54 Ko", ORANGE),
]
for i, (val, label, color) in enumerate(metrics):
    x = 0.5 + i * 2.45
    rect(slide, x, 1.35, 2.25, 1.3, CARD_BG, color, 1)
    txt(slide, val,   x+0.1, 1.45, 2.05, 0.65, size=26, bold=True, color=color, align=PP_ALIGN.CENTER)
    txt(slide, label, x+0.1, 2.1,  2.05, 0.5,  size=9,  color=GRAY, align=PP_ALIGN.CENTER)

# 2 colonnes tests
txt(slide, "Tests unitaires & intégration (pytest)", 0.6, 2.85, 5.8, 0.4, size=12, bold=True, color=ORANGE)
bullets(slide, [
    "Inscription : succès / MDP faible / doublon / champs invalides",
    "Connexion : succès / mauvais MDP / utilisateur inconnu",
    "Upload : succès / trop grand / sans fichier / avec MDP / expiration custom",
    "Suppression : propre fichier (204) / fichier d'autrui (404)",
    "Téléchargement : valide / expiré (410) / MDP incorrect (403) / 404",
    "Modèle SharedFile : is_expired, is_password_protected, hachage, __str__",
    "Isolation : filtre owner=request.user vérifié sur chaque endpoint protégé",
], 0.6, 3.28, 5.9, size=10, color=DARK, spacing=3)

txt(slide, "Tests E2E — Playwright (Chromium réel)", 6.8, 2.85, 5.8, 0.4, size=12, bold=True, color=BLUE)
bullets(slide, [
    "Page d'accueil — tagline et icône upload visibles",
    "Inscription → redirection automatique /dashboard",
    "Connexion valide → dashboard affiché",
    "Mauvais MDP → message d'erreur visible",
    "Déconnexion → retour /login",
    "Accès /dashboard sans token → redirection /login",
    "Upload fichier → lien /download/<uuid> généré",
    "Navigation lien → page téléchargement publique",
    "Fichier dans .file-row après upload",
    "Suppression → comptage -1 après confirmation",
], 6.8, 3.28, 5.9, size=10, color=DARK, spacing=3)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 10 — Performance
# ═══════════════════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
gradient_bg(slide)
card(slide, 0.4, 0.15, 12.5, 7.15)
slide_header(slide, "Performance & observabilité",
             "Métriques réelles mesurées en environnement Docker dev")

# Métriques back
txt(slide, "Back-end — temps de réponse (curl, 10 appels)", 0.6, 1.3, 6.5, 0.4,
    size=13, bold=True, color=ORANGE)

perf_back = [
    ("POST /api/auth/login/",    "227 ms",  "Intentionnel — hachage PBKDF2 anti-brute-force"),
    ("GET  /api/files/",         " 13 ms",  "Liste paginable, filtre owner côté serveur"),
    ("POST /api/files/upload/",  " 59 ms",  "Fichier 1 Mo — I/O disque inclus"),
    ("GET  /api/files/download/","  8 ms",  "Lecture disque + header Content-Disposition"),
]
for i, (ep, val, note) in enumerate(perf_back):
    y = 1.75 + i * 0.57
    bg = LIGHT_GRAY if i % 2 == 0 else WHITE
    rect(slide, 0.6, y, 6.0, 0.53, bg)
    txt(slide, ep,   0.72, y+0.07, 3.2, 0.38, size=10, bold=True, color=DARK)
    txt(slide, val,  3.9,  y+0.07, 0.9, 0.38, size=11, bold=True, color=ORANGE, align=PP_ALIGN.CENTER)
    txt(slide, note, 4.8,  y+0.07, 1.7, 0.38, size=9,  color=GRAY, italic=True)

# Front-end
txt(slide, "Front-end — budget de performance", 7.2, 1.3, 5.8, 0.4,
    size=13, bold=True, color=ORANGE)
perf_front = [
    ("Bundle JS prod",    "139 Ko", "54 Ko gzip — sous le seuil 200 Ko recommandé"),
    ("Bundle CSS prod",   "  8 Ko", "Tailwind purgé"),
    ("Build Vite",        "  1.2s", "Cold build production"),
    ("First Paint",       " ~180ms","Localhost — mesuré DevTools"),
    ("Largest Content.",  " ~320ms","LCP — seuil Good < 2500ms"),
]
for i, (label, val, note) in enumerate(perf_front):
    y = 1.75 + i * 0.57
    bg = LIGHT_GRAY if i % 2 == 0 else WHITE
    rect(slide, 7.2, y, 5.7, 0.53, bg)
    txt(slide, label, 7.32, y+0.07, 2.4, 0.38, size=10, bold=True, color=DARK)
    txt(slide, val,   9.72, y+0.07, 0.9, 0.38, size=11, bold=True, color=ORANGE, align=PP_ALIGN.CENTER)
    txt(slide, note,  10.6, y+0.07, 2.2, 0.38, size=9,  color=GRAY, italic=True)

# Observabilité
rect(slide, 0.6, 4.55, 12.1, 0.05, RGBColor(0xE0, 0xE0, 0xE0))
txt(slide, "Observabilité — logs structurés Django", 0.6, 4.65, 12, 0.4,
    size=13, bold=True, color=ORANGE)
bullets(slide, [
    "Format : [2026-04-24T14:32:10] INFO files: Fichier rapport.pdf uploadé — 2.5 Mo — user=alice — expires=2026-05-01",
    "Niveau WARNING sur mot de passe de fichier incorrect · niveau ERROR sur exception inattendue",
    "Deux loggers : files et accounts — console Docker, redirectibles vers ELK/Datadog en prod",
], 0.6, 5.1, 12.1, size=10, color=DARK, spacing=4)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 11 — IA dans le développement
# ═══════════════════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
gradient_bg(slide)
card(slide, 0.4, 0.15, 12.5, 7.15)
slide_header(slide, "Utilisation de l'IA dans le développement",
             "Posture : référent technique supervisant un copilote IA — pas du vibe coding")

txt(slide,
    "L'IA (Claude — Anthropic) a été utilisée comme junior technique assigné à des User Stories précises. "
    "Chaque bloc de code généré a été relu, testé et ajusté avant intégration.",
    0.6, 1.3, 12, 0.5, size=11, color=GRAY, italic=True)

txt(slide, "Tâches confiées à l'IA", 0.6, 1.92, 5.8, 0.4, size=13, bold=True, color=ORANGE)
bullets(slide, [
    "Modèle SharedFile (password_hash, set_password, check_password)",
    "Sérialiseurs DRF : upload, download, infos publiques",
    "Vues API avec gestion des cas d'erreur (410, 403, 413)",
    "Store Pinia files.js + composants DashboardView, DownloadView",
    "Suite pytest : 38 tests unitaires et d'intégration",
    "Diagramme d'architecture matplotlib (PNG haute résolution)",
    "Documentation : README, TESTING, SECURITY, PERF, MAINTENANCE",
], 0.6, 2.38, 5.8, size=11, color=DARK, spacing=4)

txt(slide, "Supervision & corrections apportées", 6.8, 1.92, 6.0, 0.4, size=13, bold=True, color=ORANGE)
bullets(slide, [
    "✏️  Filtre owner=request.user manquant sur FileDeleteView",
    "✏️  share_url corrigé → frontend /download/ pas /api/files/",
    "✏️  Refresh token absent de l'intercepteur Axios",
    "✏️  Layout desktop login : flex-direction mal appliqué",
    "✏️  Tests E2E : conflit plugin web3 → venv isolé e2e/",
    "✅  Zéro intégration sans tests passants",
    "✅  Revue systématique de chaque bloc de code",
], 6.8, 2.38, 6.0, size=11, color=DARK, spacing=4)

rect(slide, 0.6, 5.55, 12.1, 0.06, RGBColor(0xE0, 0xE0, 0xE0))
# Tableau apports/limites
headers_ia = ["Aspect", "Observation"]
col_w_ia = [3.0, 9.0]
col_x_ia = [0.6, 3.6]
for j, (h, w, x) in enumerate(zip(headers_ia, col_w_ia, col_x_ia)):
    rect(slide, x, 5.65, w-0.05, 0.38, ORANGE)
    txt(slide, h, x+0.1, 5.7, w-0.15, 0.28, size=10, bold=True, color=WHITE)
rows_ia = [
    ("Gain de temps", "×3 sur l'implémentation des vues, sérialiseurs et tests — estimé 3 jours économisés"),
    ("Qualité", "Bonne sur le code standard · supervision obligatoire sur sécurité et cas limites"),
    ("Limites constatées", "Oublis d'isolation utilisateur · URLs hardcodées · gestion refresh token incomplète"),
]
for i, (asp, obs) in enumerate(rows_ia):
    y = 6.06 + i * 0.42
    bg = LIGHT_GRAY if i % 2 == 0 else WHITE
    rect(slide, col_x_ia[0], y, col_w_ia[0]-0.05, 0.4, bg)
    rect(slide, col_x_ia[1], y, col_w_ia[1]-0.05, 0.4, bg)
    txt(slide, asp, col_x_ia[0]+0.1, y+0.06, col_w_ia[0]-0.2, 0.28, size=10, bold=True, color=DARK)
    txt(slide, obs, col_x_ia[1]+0.1, y+0.06, col_w_ia[1]-0.2, 0.28, size=10, color=GRAY)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 12 — Ce qui a été livré
# ═══════════════════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
gradient_bg(slide)
card(slide, 0.4, 0.15, 12.5, 7.15)
slide_header(slide, "Ce qui a été livré",
             "Application complète, testée, documentée et déployable")

livrables = [
    ("Application web fonctionnelle",
     "Toutes les US MVP + US09 + US10 — 8 User Stories livrées"),
    ("Architecture découplée professionnelle",
     "Vue.js 3 SPA + Django REST API + PostgreSQL 16 + Docker Compose"),
    ("Sécurité solide",
     "JWT rotation · PBKDF2 · isolation owner · UUID v4 · CORS strict · pip-audit 0 CVE"),
    ("Couverture de tests 99%",
     "38 tests pytest unitaires/intégration + 10 tests E2E Playwright"),
    ("Documentation complète",
     "README · OpenAPI 3.0 · TESTING · SECURITY · PERF · MAINTENANCE · doc technique PDF"),
    ("Observabilité",
     "Logs structurés Django · timestamps · niveaux INFO/WARNING/ERROR"),
    ("Installation en 1 commande",
     "docker compose up -d — migrations automatiques au démarrage"),
]

for i, (titre, desc) in enumerate(livrables):
    y = 1.35 + i * 0.72
    rect(slide, 0.6, y, 0.55, 0.55, GREEN_L, GREEN, 0.8)
    txt(slide, "✅", 0.6, y+0.05, 0.55, 0.45, size=14, align=PP_ALIGN.CENTER, color=GREEN_DARK)
    txt(slide, titre, 1.3, y+0.03, 4.5, 0.3,  size=12, bold=True, color=DARK)
    txt(slide, desc,  1.3, y+0.32, 11.2, 0.3, size=10, color=GRAY)

rect(slide, 0.6, 6.55, 12.1, 0.06, ORANGE)
txt(slide, "Prochaines étapes post-MVP :  "
    "Stockage S3 · Rate limiting · httpOnly cookies · Email de partage · App mobile React Native",
    0.6, 6.68, 12.1, 0.38, size=10, color=GRAY, italic=True)


# ═══════════════════════════════════════════════════════════════════════════════
# SLIDE 13 — Questions
# ═══════════════════════════════════════════════════════════════════════════════
slide = prs.slides.add_slide(BLANK)
gradient_bg(slide)

txt(slide, "DataShare", 1, 1.6, 11, 1.4,
    size=72, bold=True, color=DARK, align=PP_ALIGN.CENTER)
rect(slide, 3.8, 3.15, 5.7, 0.08, WHITE)
txt(slide, "Questions ?", 1, 3.35, 11, 0.9,
    size=34, color=WHITE, align=PP_ALIGN.CENTER, bold=True)
txt(slide, "Démo live disponible : http://localhost:5173",
    1, 4.4, 11, 0.6, size=15, color=DARK, align=PP_ALIGN.CENTER, italic=True)

for i, (label, val) in enumerate([
    ("User Stories", "8 / 8"),
    ("Tests", "48 (38 + 10 E2E)"),
    ("Couverture", "99 %"),
]):
    x = 2.3 + i * 3.0
    s = slide.shapes.add_shape(1, Inches(x), Inches(5.3), Inches(2.6), Inches(1.0))
    s.fill.solid(); s.fill.fore_color.rgb = RGBColor(0x00, 0x00, 0x00)
    s.fill.transparency = 0.3; s.line.fill.background()
    txt(slide, val,   x+0.1, 5.35, 2.4, 0.5, size=20, bold=True,
        color=WHITE, align=PP_ALIGN.CENTER)
    txt(slide, label, x+0.1, 5.82, 2.4, 0.38, size=10,
        color=ACCENT, align=PP_ALIGN.CENTER)

txt(slide, "© DataShare 2026", 0.5, 7.1, 12, 0.35,
    size=9, color=WHITE, align=PP_ALIGN.CENTER)


# ── Export ────────────────────────────────────────────────────────────────────
output = "docs/presentation_datashare.pptx"
prs.save(output)
print(f"✅ PowerPoint généré : {output}")
