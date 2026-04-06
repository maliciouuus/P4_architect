"""Tests E2E — Authentification (inscription et connexion).

Parcours testés :
1. Affichage de la page d'accueil
2. Inscription d'un nouvel utilisateur
3. Connexion avec les identifiants créés
4. Déconnexion
5. Redirection vers /login si non connecté
"""

import pytest
from playwright.sync_api import Page, expect


BASE_URL = "http://localhost:5173"


def test_home_page_displays(page: Page):
    """La page d'accueil affiche la tagline et l'icône d'upload."""
    page.goto(BASE_URL)
    expect(page).to_have_url(f"{BASE_URL}/")
    expect(page.locator("text=Tu veux partager un fichier")).to_be_visible()


def test_register_new_user(page: Page, credentials):
    """Un nouvel utilisateur peut créer un compte et est redirigé vers le dashboard."""
    page.goto(f"{BASE_URL}/register")

    page.fill('input[autocomplete="email"]', credentials["email"])
    page.fill('input[autocomplete="new-password"]', credentials["password"])
    page.locator('input[type="password"]').nth(1).fill(credentials["password"])
    page.click("button:has-text('Créer mon compte')")

    expect(page).to_have_url(f"{BASE_URL}/dashboard", timeout=8000)
    # Cibler le titre h2 spécifiquement pour éviter l'ambiguïté avec le bouton sidebar
    expect(page.locator("h2.section-title")).to_be_visible()


def test_logout(page: Page, credentials):
    """L'utilisateur peut se déconnecter et est redirigé vers /login."""
    page.goto(f"{BASE_URL}/login")
    page.fill('input[autocomplete="username"]', credentials["username"])
    page.fill('input[autocomplete="current-password"]', credentials["password"])
    page.click("button:has-text('Connexion')")
    expect(page).to_have_url(f"{BASE_URL}/dashboard", timeout=8000)

    page.click("button:has-text('Déconnexion')")
    expect(page).to_have_url(f"{BASE_URL}/login", timeout=5000)


def test_login_wrong_password(page: Page, credentials):
    """Une connexion avec un mauvais mot de passe affiche un message d'erreur."""
    page.goto(f"{BASE_URL}/login")
    page.fill('input[autocomplete="username"]', credentials["username"])
    page.fill('input[autocomplete="current-password"]', "MauvaisMotDePasse!")
    page.click("button:has-text('Connexion')")

    expect(page.locator("text=Identifiants incorrects")).to_be_visible(timeout=5000)
    expect(page).to_have_url(f"{BASE_URL}/login")


def test_dashboard_redirects_unauthenticated(page: Page):
    """Accéder au dashboard sans être connecté redirige vers /login."""
    page.goto(BASE_URL)
    page.evaluate("localStorage.clear()")
    page.goto(f"{BASE_URL}/dashboard")
    expect(page).to_have_url(f"{BASE_URL}/login", timeout=5000)


def test_login_success(page: Page, credentials):
    """Un utilisateur existant peut se connecter et accéder au dashboard."""
    page.goto(f"{BASE_URL}/login")
    page.fill('input[autocomplete="username"]', credentials["username"])
    page.fill('input[autocomplete="current-password"]', credentials["password"])
    page.click("button:has-text('Connexion')")

    expect(page).to_have_url(f"{BASE_URL}/dashboard", timeout=8000)
    expect(page.locator("h2.section-title")).to_be_visible()
    expect(page.locator("button:has-text('Ajouter des fichiers')")).to_be_visible()
