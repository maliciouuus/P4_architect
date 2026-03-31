<template>
  <div class="gradient-page">
    <header class="guest-header">
      <span class="brand">DataShare</span>
      <router-link to="/login" class="btn-dark">Se connecter</router-link>
    </header>

    <div class="page-body">
      <div class="card dl-card">
        <h1 class="card-title">Télécharger un fichier</h1>

        <div v-if="loading" class="state-msg">Chargement…</div>

        <div v-else-if="notFound" class="badge badge-error">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
          Ce fichier n'existe pas ou le lien est invalide.
        </div>

        <template v-else-if="fileInfo">
          <!-- File row -->
          <div class="file-row">
            <svg class="file-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
              <polyline points="14 2 14 8 20 8"/>
            </svg>
            <div>
              <p class="file-name">{{ fileInfo.original_name }}</p>
              <p class="file-size">{{ formatSize(fileInfo.size) }}</p>
            </div>
          </div>

          <!-- Expiry badge -->
          <div v-if="fileInfo.is_expired" class="badge badge-error">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
            Ce fichier n'est plus disponible en téléchargement car il a expiré.
          </div>
          <div v-else-if="daysLeft <= 1" class="badge badge-warning">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            Ce fichier expirera demain.
          </div>
          <div v-else class="badge badge-info">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><polyline points="12 6 12 12 16 14"/></svg>
            Ce fichier expirera dans {{ daysLeft }} jours.
          </div>

          <template v-if="!fileInfo.is_expired">
            <!-- Password field (si protégé) -->
            <div v-if="fileInfo.is_password_protected" class="field">
              <label>Mot de passe</label>
              <input
                v-model="password"
                type="password"
                placeholder="Saisissez le mot de passe..."
                @keyup.enter="doDownload"
              />
            </div>

            <!-- Erreur mot de passe -->
            <div v-if="passwordError" class="badge badge-error">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="12" y1="8" x2="12" y2="12"/><line x1="12" y1="16" x2="12.01" y2="16"/></svg>
              {{ passwordError }}
            </div>

            <!-- Bouton télécharger -->
            <button
              class="dl-btn"
              :class="{ disabled: fileInfo.is_password_protected && !password }"
              :disabled="fileInfo.is_password_protected && !password"
              @click="doDownload"
            >
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6">
                <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
                <polyline points="7 10 12 15 17 10"/>
                <line x1="12" y1="15" x2="12" y2="3"/>
              </svg>
              Télécharger
            </button>
          </template>
        </template>
      </div>
    </div>

    <footer class="page-footer">Copyright DataShare© 2025</footer>
  </div>
</template>

<script setup>
/**
 * Page publique de téléchargement — accessible sans compte via un lien de partage.
 *
 * Au chargement, on récupère les infos publiques du fichier (nom, taille, expiration)
 * sans déclencher le téléchargement. Si le fichier est protégé par un mot de passe,
 * l'utilisateur doit le saisir avant que le téléchargement ne démarre.
 */
import { computed, onMounted, ref } from 'vue'
import { useRoute } from 'vue-router'

import api from '../api/client'

const route = useRoute()

// Token de partage extrait de l'URL (/download/:token)
const token = route.params.token

// États de chargement et d'erreur
const loading = ref(true)
const notFound = ref(false)

// Métadonnées publiques du fichier chargées depuis l'API
const fileInfo = ref(null)

// Mot de passe saisi par l'utilisateur (uniquement si le fichier est protégé)
const password = ref('')

// Message d'erreur affiché si le mot de passe est incorrect
const passwordError = ref('')

/**
 * Calcule le nombre de jours restants avant expiration.
 * Retourne 0 si les infos ne sont pas encore chargées.
 */
const daysLeft = computed(() => {
  if (!fileInfo.value) return 0
  const diff = new Date(fileInfo.value.expires_at) - new Date()
  return Math.ceil(diff / (1000 * 60 * 60 * 24))
})

// Au montage du composant, on charge les infos publiques du fichier
onMounted(async () => {
  try {
    const { data } = await api.get(`/files/share/${token}/`)
    fileInfo.value = data
  } catch {
    // Token inconnu ou supprimé — on affiche un message d'erreur
    notFound.value = true
  } finally {
    loading.value = false
  }
})

/**
 * Déclenche le téléchargement du fichier.
 *
 * Si le fichier est protégé, on vérifie d'abord le mot de passe via l'API
 * avant de déclencher le téléchargement natif du navigateur. Cela permet
 * d'afficher un message d'erreur propre plutôt qu'un téléchargement
 * qui retournerait du JSON d'erreur au lieu du fichier.
 */
async function doDownload() {
  if (fileInfo.value.is_password_protected && !password.value) return
  passwordError.value = ''

  const passwordParam = encodeURIComponent(password.value)
  const url = fileInfo.value.is_password_protected
    ? `/api/files/download/${token}/?password=${passwordParam}`
    : `/api/files/download/${token}/`

  // Pour les fichiers protégés, on fait une pré-vérification via Axios
  // afin d'intercepter le 403 et afficher un message d'erreur clair
  if (fileInfo.value.is_password_protected) {
    try {
      await api.get(`/files/download/${token}/?password=${passwordParam}`, {
        responseType: 'blob',
      })
    } catch (e) {
      if (e.response?.status === 403) {
        passwordError.value = 'Mot de passe incorrect.'
        return
      }
    }
  }

  // Téléchargement natif : on crée un lien temporaire et on le clique
  // pour déclencher le dialogue de sauvegarde du navigateur
  const a = document.createElement('a')
  a.href = url
  a.download = fileInfo.value.original_name
  document.body.appendChild(a)
  a.click()
  document.body.removeChild(a)
}

function formatSize(bytes) {
  if (bytes < 1024) return bytes + ' o'
  if (bytes < 1_048_576) return (bytes / 1024).toFixed(1) + ' Ko'
  return (bytes / 1_048_576).toFixed(1) + ' Mo'
}
</script>

<style scoped>
.gradient-page { min-height: 100vh; background: var(--gradient); display: flex; flex-direction: column; }
.guest-header { display: flex; align-items: center; justify-content: space-between; padding: 16px; height: 72px; flex-shrink: 0; }
.brand { font-family: 'DM Sans', sans-serif; font-size: 32px; font-weight: 700; color: #000; }
.page-body { flex: 1; display: flex; align-items: center; justify-content: center; padding: 24px 16px; }
.dl-card { width: 100%; max-width: 440px; display: flex; flex-direction: column; gap: 16px; }
.card-title { font-family: 'DM Sans', sans-serif; font-size: 28px; font-weight: 700; text-align: center; }
.state-msg { text-align: center; color: var(--text-secondary); padding: 16px 0; }
.page-footer { padding: 16px 24px; font-family: 'Inter', sans-serif; font-size: 16px; color: #fff; flex-shrink: 0; }

.file-row { display: flex; align-items: center; gap: 12px; }
.file-icon { width: 24px; height: 24px; flex-shrink: 0; color: #555; }
.file-name { font-family: 'Inter', sans-serif; font-size: 16px; word-break: break-all; }
.file-size { font-family: 'DM Sans', sans-serif; font-size: 14px; color: var(--text-secondary); }

.badge {
  display: flex; align-items: center; gap: 8px;
  padding: 8px 12px; border-radius: 8px;
  font-family: 'Inter', sans-serif; font-size: 14px; width: 100%;
}
.badge-info { background: rgba(99,179,237,.15); border: 1px solid #63B3ED; color: #2B6CB0; }
.badge-warning { background: rgba(237,137,54,.15); border: 1px solid #ED8936; color: #C05621; }
.badge-error { background: rgba(245,101,101,.15); border: 1px solid #F56565; color: #C53030; }

.dl-btn {
  display: flex; align-items: center; justify-content: center; gap: 8px;
  width: 100%; padding: 12px; border-radius: var(--radius-btn);
  border: 1px solid var(--orange-outline-stroke);
  color: var(--orange-outline-text);
  background: transparent;
  font-family: 'DM Sans', sans-serif; font-size: 16px;
  cursor: pointer; transition: background .15s;
}
.dl-btn:hover:not(.disabled) { background: rgba(255,129,45,.08); }
.dl-btn.disabled { border-color: #D9D9D9; color: var(--text-placeholder); cursor: not-allowed; }
</style>
