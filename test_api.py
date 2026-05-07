#!/usr/bin/env python3
"""
Test complet de l'API DataShare.
Lance tous les endpoints dans l'ordre et vérifie les réponses.

Usage :
    python3 test_api.py

Prérequis :
    - L'application doit tourner (bash start.sh)
    - pip install requests
"""

import sys
import os
import tempfile
import requests

BASE = "http://localhost:8000/api"
OK    = "\033[92m✅\033[0m"
FAIL  = "\033[91m❌\033[0m"
SEP   = "\033[90m" + "─" * 52 + "\033[0m"

passed = 0
failed = 0

def check(label, condition, got=None):
    global passed, failed
    if condition:
        print(f"  {OK} {label}")
        passed += 1
    else:
        print(f"  {FAIL} {label}" + (f" — reçu : {got}" if got is not None else ""))
        failed += 1

def section(title):
    print(f"\n{SEP}")
    print(f"  {title}")
    print(SEP)


# ── Variables partagées entre les tests ───────────────────────────────────────
token       = None
file_id     = None
share_token = None
anon_token  = None


# ═══════════════════════════════════════════════════════════════════════════════
# AUTH
# ═══════════════════════════════════════════════════════════════════════════════

section("1. POST /auth/register")
r = requests.post(f"{BASE}/auth/register", json={
    "email":    "pytest_api@datashare.com",
    "username": "pytest_api",
    "password": "motdepasse123"
})
check("Status 201 ou 409",     r.status_code in (201, 409), r.status_code)
if r.status_code == 201:
    check("Retourne id + email", "id" in r.json() and "email" in r.json())
    check("Pas de mot de passe dans la réponse", "password" not in r.json())


section("2. POST /auth/register — email dupliqué → 409")
r = requests.post(f"{BASE}/auth/register", json={
    "email":    "pytest_api@datashare.com",
    "username": "autre",
    "password": "motdepasse123"
})
check("Status 409 Conflict", r.status_code == 409, r.status_code)


section("3. POST /auth/register — mot de passe trop court → 400")
r = requests.post(f"{BASE}/auth/register", json={
    "email":    "court@datashare.com",
    "username": "court",
    "password": "abc"
})
check("Status 400 Bad Request", r.status_code == 400, r.status_code)


section("4. POST /auth/login — identifiants valides")
r = requests.post(f"{BASE}/auth/login", json={
    "email":    "pytest_api@datashare.com",
    "password": "motdepasse123"
})
check("Status 200",            r.status_code == 200, r.status_code)
check("access_token présent",  "access_token" in r.json())
check("user présent",          "user" in r.json())
if "access_token" in r.json():
    token = r.json()["access_token"]


section("5. POST /auth/login — mauvais mot de passe → 401")
r = requests.post(f"{BASE}/auth/login", json={
    "email":    "pytest_api@datashare.com",
    "password": "mauvaismdp"
})
check("Status 401",            r.status_code == 401, r.status_code)
check("Message générique",     "invalides" in r.json().get("message", "").lower())


section("6. POST /auth/login — email inconnu → 401")
r = requests.post(f"{BASE}/auth/login", json={
    "email":    "inconnu@datashare.com",
    "password": "motdepasse123"
})
check("Status 401",            r.status_code == 401, r.status_code)


section("7. GET /auth/me — avec token valide")
headers = {"Authorization": f"Bearer {token}"}
r = requests.get(f"{BASE}/auth/me", headers=headers)
check("Status 200",            r.status_code == 200, r.status_code)
check("Pas de mot de passe",   "password" not in r.json())
check("Email correct",         r.json().get("email") == "pytest_api@datashare.com")


section("8. GET /auth/me — sans token → 401")
r = requests.get(f"{BASE}/auth/me")
check("Status 401",            r.status_code == 401, r.status_code)


# ═══════════════════════════════════════════════════════════════════════════════
# FICHIERS
# ═══════════════════════════════════════════════════════════════════════════════

section("9. GET /files — liste (authentifié)")
headers = {"Authorization": f"Bearer {token}"}
r = requests.get(f"{BASE}/files", headers=headers)
check("Status 200",            r.status_code == 200, r.status_code)
check("Retourne un tableau",   isinstance(r.json(), list))


section("10. GET /files — sans token → 401")
r = requests.get(f"{BASE}/files")
check("Status 401",            r.status_code == 401, r.status_code)


section("11. POST /files/upload — fichier valide (authentifié)")
with tempfile.NamedTemporaryFile(suffix=".txt", delete=False, mode="w") as f:
    f.write("Contenu test DataShare API")
    tmp = f.name

headers = {"Authorization": f"Bearer {token}"}
with open(tmp, "rb") as f:
    r = requests.post(f"{BASE}/files/upload",
        headers=headers,
        files={"file": ("test_datashare.txt", f, "text/plain")},
        data={"expiry_hours": "24"}
    )
os.unlink(tmp)

check("Status 201",              r.status_code == 201, r.status_code)
check("share_url présent",       "share_url" in r.json())
check("is_expired = false",      r.json().get("is_expired") == False)
check("is_password_protected",   r.json().get("is_password_protected") == False)
if "share_token" in r.json():
    share_token = r.json()["share_token"]
    file_id     = r.json()["id"]


section("12. POST /files/upload — extension interdite → 403")
with tempfile.NamedTemporaryFile(suffix=".exe", delete=False, mode="w") as f:
    f.write("virus")
    tmp = f.name

headers = {"Authorization": f"Bearer {token}"}
with open(tmp, "rb") as f:
    r = requests.post(f"{BASE}/files/upload",
        headers=headers,
        files={"file": ("malware.exe", f, "application/octet-stream")},
    )
os.unlink(tmp)
check("Status 403 extension interdite", r.status_code == 403, r.status_code)


section("13. POST /files/upload — avec mot de passe")
with tempfile.NamedTemporaryFile(suffix=".txt", delete=False, mode="w") as f:
    f.write("Fichier protégé")
    tmp = f.name

headers = {"Authorization": f"Bearer {token}"}
with open(tmp, "rb") as f:
    r = requests.post(f"{BASE}/files/upload",
        headers=headers,
        files={"file": ("protege.txt", f, "text/plain")},
        data={"password": "secret123", "expiry_hours": "48"}
    )
os.unlink(tmp)
check("Status 201",                 r.status_code == 201, r.status_code)
check("is_password_protected = true", r.json().get("is_password_protected") == True)


section("14. POST /files/upload — mot de passe trop court → 400")
with tempfile.NamedTemporaryFile(suffix=".txt", delete=False, mode="w") as f:
    f.write("test")
    tmp = f.name

headers = {"Authorization": f"Bearer {token}"}
with open(tmp, "rb") as f:
    r = requests.post(f"{BASE}/files/upload",
        headers=headers,
        files={"file": ("test.txt", f, "text/plain")},
        data={"password": "abc"}
    )
os.unlink(tmp)
check("Status 400 mdp trop court",  r.status_code == 400, r.status_code)


section("15. POST /files/upload/anonymous — sans compte")
with tempfile.NamedTemporaryFile(suffix=".txt", delete=False, mode="w") as f:
    f.write("Upload anonyme test")
    tmp = f.name

with open(tmp, "rb") as f:
    r = requests.post(f"{BASE}/files/upload/anonymous",
        files={"file": ("anon.txt", f, "text/plain")},
        data={"expiry_hours": "24"}
    )
os.unlink(tmp)
check("Status 201",            r.status_code == 201, r.status_code)
check("share_url présent",     "share_url" in r.json())
if "share_token" in r.json():
    anon_token = r.json()["share_token"]


section("16. GET /files/share/:token — métadonnées publiques")
if share_token:
    r = requests.get(f"{BASE}/files/share/{share_token}")
    check("Status 200",             r.status_code == 200, r.status_code)
    check("original_name présent",  "original_name" in r.json())
    check("Pas de file_path",       "file_path" not in r.json())
    check("Pas de password_hash",   "password_hash" not in r.json())
else:
    check("Token disponible",       False, "upload précédent a échoué")


section("17. GET /files/share/:token — token inconnu → 404")
r = requests.get(f"{BASE}/files/share/token-qui-nexiste-pas")
check("Status 404",            r.status_code == 404, r.status_code)


section("18. GET /files/download/:token — téléchargement")
if share_token:
    r = requests.get(f"{BASE}/files/download/{share_token}")
    check("Status 200",                    r.status_code == 200, r.status_code)
    check("Content-Disposition présent",   "content-disposition" in r.headers)
    check("Contenu non vide",              len(r.content) > 0)
else:
    check("Token disponible",              False, "upload précédent a échoué")


section("19. GET /files/download/:token — token inconnu → 404")
r = requests.get(f"{BASE}/files/download/token-qui-nexiste-pas")
check("Status 404",            r.status_code == 404, r.status_code)


section("20. DELETE /files/:id — suppression (propriétaire)")
if file_id:
    headers = {"Authorization": f"Bearer {token}"}
    r = requests.delete(f"{BASE}/files/{file_id}", headers=headers)
    check("Status 200",        r.status_code == 200, r.status_code)
else:
    check("ID disponible",     False, "upload précédent a échoué")


section("21. DELETE /files/:id — sans token → 401")
r = requests.delete(f"{BASE}/files/un-id-quelconque")
check("Status 401",            r.status_code == 401, r.status_code)


section("22. DELETE /files/:id — fichier d'un autre → 404")
if file_id:
    # Créer un second compte
    requests.post(f"{BASE}/auth/register", json={
        "email": "autre_pytest@datashare.com",
        "username": "autre_pytest",
        "password": "motdepasse123"
    })
    r2 = requests.post(f"{BASE}/auth/login", json={
        "email": "autre_pytest@datashare.com",
        "password": "motdepasse123"
    })
    token2 = r2.json().get("access_token", "")

    # Uploader un fichier avec compte 1, tenter de supprimer avec compte 2
    with tempfile.NamedTemporaryFile(suffix=".txt", delete=False, mode="w") as f:
        f.write("Fichier compte 1")
        tmp = f.name

    h1 = {"Authorization": f"Bearer {token}"}
    with open(tmp, "rb") as f:
        r_up = requests.post(f"{BASE}/files/upload",
            headers=h1,
            files={"file": ("compte1.txt", f, "text/plain")},
        )
    os.unlink(tmp)

    fid2 = r_up.json().get("id", "")
    h2 = {"Authorization": f"Bearer {token2}"}
    r = requests.delete(f"{BASE}/files/{fid2}", headers=h2)
    check("Status 404 (pas propriétaire)", r.status_code == 404, r.status_code)

    # Nettoyage
    requests.delete(f"{BASE}/files/{fid2}", headers=h1)


# ═══════════════════════════════════════════════════════════════════════════════
# RÉSUMÉ
# ═══════════════════════════════════════════════════════════════════════════════

total = passed + failed
print(f"\n{SEP}")
print(f"  RÉSULTAT : {passed}/{total} tests passants")
if failed == 0:
    print(f"  {OK} Tous les endpoints fonctionnent correctement")
else:
    print(f"  {FAIL} {failed} test(s) échoué(s)")
print(SEP)

sys.exit(0 if failed == 0 else 1)
