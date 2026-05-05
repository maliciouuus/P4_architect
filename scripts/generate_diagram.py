#!/usr/bin/env python3
"""Génère le diagramme d'architecture DataShare en PNG haute résolution."""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import matplotlib.patheffects as pe

fig, ax = plt.subplots(1, 1, figsize=(16, 9))
ax.set_xlim(0, 16)
ax.set_ylim(0, 9)
ax.axis('off')
fig.patch.set_facecolor('#FAFAFA')

# ── Couleurs ──────────────────────────────────────────────────────────────────
C_ORANGE   = '#FF812D'
C_PEACH    = '#FFE0CC'
C_BLUE     = '#2563EB'
C_BLUE_L   = '#DBEAFE'
C_GREEN    = '#16A34A'
C_GREEN_L  = '#DCFCE7'
C_PURPLE   = '#7C3AED'
C_PURPLE_L = '#EDE9FE'
C_GRAY     = '#6B7280'
C_GRAY_L   = '#F3F4F6'
C_DARK     = '#1F2937'
C_WHITE    = '#FFFFFF'
C_RED_L    = '#FEE2E2'
C_RED      = '#DC2626'


def box(ax, x, y, w, h, color, text, subtext=None,
        fontsize=11, radius=0.3, border=None, text_color=C_DARK):
    border_color = border or color
    rect = FancyBboxPatch(
        (x - w/2, y - h/2), w, h,
        boxstyle=f"round,pad=0,rounding_size={radius}",
        facecolor=color, edgecolor=border_color, linewidth=1.5, zorder=3
    )
    ax.add_patch(rect)
    if subtext:
        ax.text(x, y + 0.18, text, ha='center', va='center',
                fontsize=fontsize, fontweight='bold', color=text_color, zorder=4)
        ax.text(x, y - 0.25, subtext, ha='center', va='center',
                fontsize=fontsize - 2, color=C_GRAY, zorder=4)
    else:
        ax.text(x, y, text, ha='center', va='center',
                fontsize=fontsize, fontweight='bold', color=text_color, zorder=4)


def arrow(ax, x1, y1, x2, y2, label='', color=C_GRAY, dashed=False):
    style = 'dashed' if dashed else 'solid'
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(
                    arrowstyle='->', color=color, lw=1.8,
                    linestyle=style,
                    connectionstyle='arc3,rad=0.0'
                ), zorder=2)
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx + 0.1, my + 0.15, label, ha='center', va='center',
                fontsize=8, color=color,
                bbox=dict(boxstyle='round,pad=0.2', facecolor='white',
                          edgecolor='none', alpha=0.9))


def section_bg(ax, x, y, w, h, color, title):
    rect = FancyBboxPatch(
        (x, y), w, h,
        boxstyle="round,pad=0,rounding_size=0.4",
        facecolor=color, edgecolor='#E5E7EB', linewidth=1, zorder=1, alpha=0.5
    )
    ax.add_patch(rect)
    ax.text(x + 0.25, y + h - 0.3, title, ha='left', va='center',
            fontsize=9, color=C_GRAY, fontstyle='italic', zorder=2)


# ── Titre ─────────────────────────────────────────────────────────────────────
ax.text(8, 8.6, 'Architecture — DataShare MVP',
        ha='center', va='center', fontsize=18, fontweight='bold', color=C_DARK)
ax.text(8, 8.2, 'Architecture client-serveur découplée · Docker Compose',
        ha='center', va='center', fontsize=11, color=C_GRAY)

# ── Zone Navigateur ───────────────────────────────────────────────────────────
section_bg(ax, 0.4, 4.8, 4.8, 3.0, C_BLUE_L, 'Navigateur (port 5173)')

box(ax, 2.8, 7.1, 3.8, 0.7, C_BLUE, 'Vue.js 3 SPA',
    text_color=C_WHITE, fontsize=12)

box(ax, 1.5, 6.1, 1.6, 0.65, C_BLUE_L, 'Vue Router', '5 pages',
    fontsize=10, border=C_BLUE)
box(ax, 2.8, 6.1, 1.2, 0.65, C_BLUE_L, 'Pinia', 'stores',
    fontsize=10, border=C_BLUE)
box(ax, 4.1, 6.1, 1.2, 0.65, C_BLUE_L, 'Axios', 'client API',
    fontsize=10, border=C_BLUE)

ax.text(2.8, 5.25, 'Home · Login · Register · Dashboard · Download',
        ha='center', va='center', fontsize=8.5, color=C_GRAY,
        style='italic')

# ── Zone API REST ─────────────────────────────────────────────────────────────
section_bg(ax, 5.8, 3.8, 4.5, 4.0, C_ORANGE + '22',
           'API REST — Django 5.2 + DRF (port 8000)')

box(ax, 8.05, 7.1, 3.8, 0.7, C_ORANGE, 'Django REST Framework',
    text_color=C_WHITE, fontsize=12)

box(ax, 6.8, 6.1, 1.6, 0.65, '#FFF3E8', '/api/auth/', 'register · login · me',
    fontsize=9, border=C_ORANGE)
box(ax, 8.7, 6.1, 2.3, 0.65, '#FFF3E8', '/api/files/', 'upload · list · delete · share · download',
    fontsize=8.5, border=C_ORANGE)

box(ax, 6.8, 5.0, 1.6, 0.65, '#FFF3E8', 'JWT Auth', 'simplejwt · 1h/7j',
    fontsize=9, border=C_ORANGE)
box(ax, 8.7, 5.0, 2.3, 0.65, '#FFF3E8', 'Sécurité', 'isolation · UUID · PBKDF2 · CORS',
    fontsize=9, border=C_ORANGE)

ax.text(8.05, 4.2, 'Python 3.12 · ORM Django · Logs structurés',
        ha='center', va='center', fontsize=8.5, color=C_GRAY, style='italic')

# ── Zone Stockage ─────────────────────────────────────────────────────────────
section_bg(ax, 11.1, 4.5, 4.3, 3.3, C_GREEN_L, 'Stockage')

box(ax, 13.25, 7.1, 3.5, 0.7, C_GREEN, 'PostgreSQL 16',
    text_color=C_WHITE, fontsize=12)
box(ax, 13.25, 6.1, 3.5, 0.65, C_GREEN_L, 'Tables', 'users · shared_files',
    fontsize=10, border=C_GREEN)
box(ax, 13.25, 5.15, 3.5, 0.65, C_GREEN_L, 'Disque local', '/media/uploads/<uid>/<uuid>_<name>',
    fontsize=9, border=C_GREEN)

ax.text(13.25, 4.7, 'Volume Docker persistant',
        ha='center', va='center', fontsize=8.5, color=C_GRAY, style='italic')

# ── Zone Docker Compose ───────────────────────────────────────────────────────
section_bg(ax, 0.4, 0.4, 15.0, 3.5, C_GRAY_L, 'Docker Compose')

box(ax, 2.5, 2.5, 3.2, 0.65, C_WHITE, 'Service frontend',
    'Node 20 · Vite dev server', fontsize=10, border=C_BLUE)
box(ax, 7.5, 2.5, 3.2, 0.65, C_WHITE, 'Service backend',
    'Python 3.12 · runserver', fontsize=10, border=C_ORANGE)
box(ax, 12.5, 2.5, 3.2, 0.65, C_WHITE, 'Service db',
    'postgres:16-alpine · port 5432', fontsize=10, border=C_GREEN)

box(ax, 2.5, 1.5, 2.5, 0.55, C_GRAY_L, ':5173 → 5173', fontsize=9, border=C_GRAY)
box(ax, 7.5, 1.5, 2.5, 0.55, C_GRAY_L, ':8000 → 8000', fontsize=9, border=C_GRAY)
box(ax, 12.5, 1.5, 2.5, 0.55, C_GRAY_L, ':5433 → 5432', fontsize=9, border=C_GRAY)

ax.text(8, 0.75, 'Réseau interne Docker · Volumes persistants : postgres_data · media_data',
        ha='center', va='center', fontsize=9, color=C_GRAY)

# ── Flèches principales ───────────────────────────────────────────────────────
# Navigateur → API
arrow(ax, 5.2, 6.5, 5.8, 6.5, 'HTTP/JSON\nJWT Bearer', C_ORANGE)
arrow(ax, 5.8, 6.2, 5.2, 6.2, '', C_ORANGE)

# API → PostgreSQL
arrow(ax, 10.3, 6.5, 11.1, 6.5, 'ORM\nDjango', C_GREEN)
arrow(ax, 11.1, 6.2, 10.3, 6.2, '', C_GREEN)

# API → Disque
arrow(ax, 10.3, 5.2, 11.1, 5.2, 'FileField\nwrite/read', C_GREEN, dashed=True)

# Docker services → ports
arrow(ax, 2.5, 2.17, 2.5, 1.78, '', C_GRAY)
arrow(ax, 7.5, 2.17, 7.5, 1.78, '', C_GRAY)
arrow(ax, 12.5, 2.17, 12.5, 1.78, '', C_GRAY)

# ── Légende ───────────────────────────────────────────────────────────────────
legend_items = [
    (C_BLUE, 'Frontend Vue.js'),
    (C_ORANGE, 'Backend Django'),
    (C_GREEN, 'Stockage'),
    (C_GRAY, 'Infrastructure Docker'),
]
for i, (color, label) in enumerate(legend_items):
    x = 1.5 + i * 3.2
    rect = mpatches.Patch(facecolor=color, edgecolor='none', label=label)
    ax.add_patch(FancyBboxPatch((x - 0.15, 0.08), 0.3, 0.25,
                                boxstyle="round,pad=0", facecolor=color,
                                edgecolor='none', zorder=3))
    ax.text(x + 0.25, 0.2, label, va='center', fontsize=8.5, color=C_DARK)

plt.tight_layout(pad=0.2)
output = 'docs/architecture_diagram.png'
plt.savefig(output, dpi=180, bbox_inches='tight',
            facecolor='#FAFAFA', edgecolor='none')
plt.close()
print(f"✅ Diagramme généré : {output}")
