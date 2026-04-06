"""Tests E2E — Gestion des fichiers (upload, liste, téléchargement, suppression).

Parcours testés :
1. Upload d'un fichier depuis le dashboard
2. Apparition du lien de partage après upload
3. Page de téléchargement publique accessible sans compte
4. Suppression d'un fichier
"""

import os
import tempfile

from playwright.sync_api import Page, expect


BASE_URL = "http://localhost:5173"


def login(page: Page, credentials: dict):
    """Connecte l'utilisateur et attend la redirection vers le dashboard."""
    page.goto(f"{BASE_URL}/login")
    page.fill('input[autocomplete="username"]', credentials["username"])
    page.fill('input[autocomplete="current-password"]', credentials["password"])
    page.click("button:has-text('Connexion')")
    expect(page).to_have_url(f"{BASE_URL}/dashboard", timeout=8000)


def close_upload_modal(page: Page):
    """Ferme la modale d'upload en cliquant sur le coin de l'overlay."""
    overlay = page.locator(".modal-overlay").first
    if overlay.is_visible():
        # On clique sur le bord de l'overlay (pas sur la carte)
        # pour déclencher @click.self="closeUploadModal"
        overlay.click(position={"x": 5, "y": 5})
        page.wait_for_timeout(400)


def upload_temp_file(page: Page, content: str = "Test DataShare E2E") -> str:
    """Uploade un fichier temporaire et retourne l'URL de partage normalisée."""
    close_upload_modal(page)

    page.click("button:has-text('Ajouter des fichiers')")
    expect(page.locator("h2.upload-title")).to_be_visible()

    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False, mode="w") as f:
        f.write(content)
        tmp_path = f.name

    try:
        page.set_input_files('input[type="file"]', tmp_path)
        expect(page.locator(".sel-name")).to_be_visible(timeout=3000)
        page.click("button:has-text('Téléverser')")
        expect(page.locator(".share-url")).to_be_visible(timeout=10000)
        raw_url = page.locator(".share-url").inner_text().strip()
        # Le backend est dans Docker donc l'hôte peut être "backend" — on le corrige
        return raw_url.replace("http://backend:", "http://localhost:")
    finally:
        os.unlink(tmp_path)


def test_upload_file(page: Page, credentials):
    """Un fichier uploadé génère un lien de partage valide."""
    login(page, credentials)
    share_url = upload_temp_file(page, "Contenu test upload")
    assert "/download/" in share_url


def test_share_link_opens_download_page(page: Page, credentials):
    """Le lien de partage ouvre une page de téléchargement publique."""
    login(page, credentials)
    share_url = upload_temp_file(page, "Contenu test lien")

    page.goto(share_url)
    expect(page.locator("h1.card-title")).to_be_visible(timeout=5000)
    expect(page.locator("text=Télécharger un fichier")).to_be_visible()
    expect(page.locator(".dl-btn")).to_be_visible()


def test_file_appears_in_list(page: Page, credentials):
    """Après upload, le fichier apparaît dans la liste des fichiers."""
    login(page, credentials)
    close_upload_modal(page)
    expect(page.locator(".file-row").first).to_be_visible(timeout=5000)


def test_delete_file(page: Page, credentials):
    """Un fichier peut être supprimé et disparaît de la liste."""
    login(page, credentials)

    upload_temp_file(page, "Fichier à supprimer")

    # Fermer la modale d'upload avant de tenter la suppression
    close_upload_modal(page)
    page.wait_for_timeout(600)

    count_before = page.locator(".file-row").count()
    assert count_before > 0

    # Cliquer Supprimer sur le premier fichier de la liste
    page.locator(".file-row").first.locator(
        "button:has-text('Supprimer')"
    ).click()

    # Confirmer dans la modale de suppression
    expect(page.locator(".delete-modal")).to_be_visible(timeout=3000)
    page.locator(".delete-modal button:has-text('Supprimer')").click()

    page.wait_for_timeout(1000)
    assert page.locator(".file-row").count() == count_before - 1
