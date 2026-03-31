<template>
  <div class="dashboard-layout">

    <!-- Sidebar (desktop) -->
    <aside class="sidebar">
      <div class="sidebar-brand">DataShare</div>
      <nav class="sidebar-nav">
        <button
          class="sidebar-item active"
          @click="activeTab = 'files'"
        >Mes fichiers</button>
      </nav>
      <div class="sidebar-footer">Copyright DataShare© 2025</div>
    </aside>

    <!-- Main panel -->
    <div class="main-panel">

      <!-- Top action bar -->
      <div class="action-bar">
        <div class="action-bar-inner">
          <div class="action-bar-btns">
            <button class="btn-dark" @click="showUploadModal = true">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
              Ajouter des fichiers
            </button>
            <button class="btn-orange-outline" @click="handleLogout">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
              Déconnexion
            </button>
          </div>
        </div>
      </div>

      <!-- Content -->
      <div class="panel-content">
        <h2 class="section-title">Mes fichiers</h2>

        <!-- Filter tabs -->
        <div class="tabs-wrap">
          <div class="tabs">
            <button
              v-for="t in tabs"
              :key="t.key"
              class="tab"
              :class="{ active: currentTab === t.key }"
              @click="currentTab = t.key"
            >{{ t.label }}</button>
          </div>
        </div>

        <!-- File list -->
        <div v-if="store.loading" class="state-msg">Chargement…</div>
        <div v-else-if="store.error" class="alert alert-error">{{ store.error }}</div>
        <div v-else-if="filteredFiles.length === 0" class="state-msg">Aucun fichier.</div>
        <div v-else class="file-list">
          <div v-for="file in filteredFiles" :key="file.id" class="file-row">
            <svg class="file-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
              <polyline points="14 2 14 8 20 8"/>
            </svg>

            <div class="file-info">
              <span class="file-name">{{ file.original_name }}</span>
              <span class="file-expiry" :class="{ expired: file.is_expired }">
                {{ file.is_expired ? 'Expiré' : expiryLabel(file) }}
              </span>
              <span v-if="file.is_expired" class="expired-msg">
                Ce fichier a expiré, il n'est plus stocké chez nous
              </span>
            </div>

            <div class="file-actions">
              <svg v-if="!file.is_expired" class="lock-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
              </svg>
              <template v-if="!file.is_expired">
                <button class="btn-orange-outline btn-sm" @click="confirmDelete(file)">
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14H6L5 6"/><path d="M10 11v6M14 11v6"/><path d="M9 6V4h6v2"/></svg>
                  Supprimer
                </button>
                <button class="btn-orange-outline btn-sm" @click="copyLink(file.share_url)">
                  Accéder
                  <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
                </button>
              </template>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Upload modal -->
    <div v-if="showUploadModal" class="modal-overlay" @click.self="closeUploadModal">
      <div class="card upload-modal">
        <h2 class="upload-title">Ajouter un fichier</h2>

        <!-- File row (selected) -->
        <div v-if="selectedFile" class="selected-file-row">
          <div class="selected-file-left">
            <svg class="file-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
            <div>
              <p class="sel-name">{{ selectedFile.name }}</p>
              <p class="sel-size" :class="{ 'sel-size-error': selectedFile.size > 52_428_800 }">
                {{ formatSize(selectedFile.size) }}
              </p>
            </div>
          </div>
          <button class="btn-orange-outline btn-sm" @click="fileInput.click()">Changer</button>
        </div>
        <div v-else class="drop-zone" @click="fileInput.click()" @dragover.prevent="dragging=true" @dragleave.prevent="dragging=false" @drop.prevent="onDrop" :class="{dragging}">
          <svg width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#B3B3B3" stroke-width="1.5"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
          <p>Glissez un fichier ou <strong>cliquez ici</strong></p>
        </div>
        <input ref="fileInput" type="file" hidden @change="onFileChange" />

        <p v-if="selectedFile && selectedFile.size > 52_428_800" class="size-error">
          La taille des fichiers est limitée à 50 Mo
        </p>

        <!-- Fields -->
        <div class="upload-fields">
          <div class="field">
            <label>Mot de passe</label>
            <input type="password" v-model="filePassword" placeholder="Optionnel" />
          </div>
          <div class="field">
            <label>Expiration</label>
            <select v-model="expiryHours">
              <option :value="24">Une journée</option>
              <option :value="72">3 jours</option>
              <option :value="168">Une semaine</option>
            </select>
          </div>
        </div>

        <!-- Progress -->
        <div v-if="uploadProgress !== null" class="progress-wrap">
          <div class="progress-bar" :style="{ width: uploadProgress + '%' }"></div>
        </div>

        <!-- Share link after upload -->
        <template v-if="lastUpload">
          <p class="success-text">
            Félicitations, ton fichier sera conservé chez nous pendant
            {{ expiryHours === 24 ? 'une journée' : expiryHours === 72 ? '3 jours' : 'une semaine' }} !
          </p>
          <div class="share-box" @click="copyLink(lastUpload.share_url)">
            <span class="share-url">{{ lastUpload.share_url }}</span>
          </div>
          <button class="btn-orange-outline" style="width:100%;justify-content:center" @click="copyLink(lastUpload.share_url)">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>
            {{ copied ? '✓ Copié !' : 'Copier le lien' }}
          </button>
        </template>

        <div v-if="uploadError" class="alert alert-error">{{ uploadError }}</div>

        <button
          class="btn-orange-solid"
          :disabled="!selectedFile || uploading || (selectedFile && selectedFile.size > 52_428_800)"
          @click="doUpload"
          style="margin-top:8px"
        >
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
          {{ uploading ? 'Envoi…' : 'Téléverser' }}
        </button>
      </div>
    </div>

    <!-- Delete confirm modal -->
    <div v-if="fileToDelete" class="modal-overlay" @click.self="fileToDelete = null">
      <div class="card delete-modal">
        <h3>Supprimer le fichier ?</h3>
        <p>« {{ fileToDelete.original_name }} » sera définitivement supprimé.</p>
        <div class="modal-actions">
          <button class="btn-orange-outline" @click="fileToDelete = null">Annuler</button>
          <button class="btn-dark" @click="doDelete">Supprimer</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
/**
 * Tableau de bord principal — espace personnel de l'utilisateur connecté.
 *
 * Cette vue est accessible uniquement aux utilisateurs authentifiés.
 * Elle présente :
 * - une sidebar de navigation (desktop)
 * - une barre d'actions avec "Ajouter des fichiers" et "Déconnexion"
 * - la liste des fichiers filtrée par onglet (Tous / Actifs / Expiré)
 * - une modale d'upload avec choix du mot de passe et de l'expiration
 * - une modale de confirmation de suppression
 */
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'

import { useAuthStore } from '../stores/auth'
import { useFilesStore } from '../stores/files'

const store = useFilesStore()
const auth = useAuthStore()
const router = useRouter()

// Onglet actif dans la liste — 'all', 'active' ou 'expired'
const currentTab = ref('all')
const tabs = [
  { key: 'all', label: 'Tous' },
  { key: 'active', label: 'Actifs' },
  { key: 'expired', label: 'Expiré' },
]

// Liste filtrée selon l'onglet sélectionné
const filteredFiles = computed(() => {
  if (currentTab.value === 'active') return store.files.filter(f => !f.is_expired)
  if (currentTab.value === 'expired') return store.files.filter(f => f.is_expired)
  return store.files
})

// Contrôle de la modale d'upload
const showUploadModal = ref(false)

// Référence vers l'input file caché (déclenché programmatiquement)
const fileInput = ref(null)

// Vrai quand l'utilisateur survole la zone de dépôt avec un fichier
const dragging = ref(false)

// Fichier sélectionné, en attente d'envoi
const selectedFile = ref(null)

// Options d'upload
const filePassword = ref('')
const expiryHours = ref(24)

// État de l'upload en cours
const uploading = ref(false)
const uploadProgress = ref(null)
const uploadError = ref('')

// Résultat du dernier upload réussi (pour afficher le lien de partage)
const lastUpload = ref(null)

// Feedback visuel "Copié !" pendant 2 secondes après copie du lien
const copied = ref(false)

// Fichier en attente de suppression (déclenche la modale de confirmation)
const fileToDelete = ref(null)

// Onglet actif dans la sidebar
const activeTab = ref('files')

// On charge la liste des fichiers dès que la page est affichée
onMounted(() => store.fetchFiles())

/** Déconnecte l'utilisateur et redirige vers la page de login. */
function handleLogout() {
  auth.logout()
  router.push('/login')
}

/** Réinitialise tous les états de la modale d'upload à la fermeture. */
function closeUploadModal() {
  showUploadModal.value = false
  selectedFile.value = null
  lastUpload.value = null
  uploadError.value = ''
  uploadProgress.value = null
}

/** Récupère le fichier déposé par glisser-déposer. */
function onDrop(e) {
  dragging.value = false
  selectedFile.value = e.dataTransfer.files[0] || null
}

/** Récupère le fichier sélectionné via le dialogue natif du navigateur. */
function onFileChange(e) {
  selectedFile.value = e.target.files[0] || null
  // On vide la valeur de l'input pour permettre de re-sélectionner le même fichier
  e.target.value = ''
  lastUpload.value = null
  uploadError.value = ''
}

/**
 * Lance l'upload du fichier sélectionné.
 * La taille est vérifiée côté client avant l'envoi pour un retour immédiat.
 * Après l'upload, le lien de partage est affiché directement dans la modale.
 */
async function doUpload() {
  if (!selectedFile.value || selectedFile.value.size > 52_428_800) return
  uploadError.value = ''
  lastUpload.value = null
  uploading.value = true
  uploadProgress.value = 0
  try {
    const result = await store.uploadFile(selectedFile.value, {
      password: filePassword.value,
      expiryHours: expiryHours.value,
      onProgress: (p) => { uploadProgress.value = p },
    })
    lastUpload.value = result
    selectedFile.value = null
  } catch (e) {
    uploadError.value = e.response?.data?.detail || 'Erreur lors de l\'envoi.'
  } finally {
    uploading.value = false
    uploadProgress.value = null
  }
}

/**
 * Copie l'URL de partage dans le presse-papier.
 * Affiche "Copié !" pendant 2 secondes comme confirmation visuelle.
 */
async function copyLink(url) {
  await navigator.clipboard.writeText(url)
  copied.value = true
  setTimeout(() => { copied.value = false }, 2000)
}

/** Ouvre la modale de confirmation de suppression pour le fichier donné. */
function confirmDelete(file) { fileToDelete.value = file }

/** Confirme la suppression et ferme la modale. */
async function doDelete() {
  await store.deleteFile(fileToDelete.value.id)
  fileToDelete.value = null
}

function expiryLabel(file) {
  const now = new Date()
  const exp = new Date(file.expires_at)
  const diff = Math.ceil((exp - now) / (1000 * 60 * 60 * 24))
  if (diff <= 0) return 'Expiré'
  if (diff === 1) return 'Expire demain'
  return `Expire dans ${diff} jours`
}

function formatSize(bytes) {
  if (bytes < 1024) return bytes + ' o'
  if (bytes < 1_048_576) return (bytes / 1024).toFixed(1) + ' Ko'
  return (bytes / 1_048_576).toFixed(1) + ' Mo'
}
</script>

<style scoped>
/* ─── Layout ──────────────────────────────────────── */
.dashboard-layout {
  display: flex;
  min-height: 100vh;
}

/* ─── Sidebar ─────────────────────────────────────── */
.sidebar {
  width: 259px;
  flex-shrink: 0;
  background: var(--gradient);
  border-right: 2px solid #623519;
  display: flex;
  flex-direction: column;
}
.sidebar-brand {
  font-family: 'DM Sans', sans-serif;
  font-size: 32px;
  font-weight: 700;
  color: #fff;
  padding: 16px 24px;
  height: 72px;
  display: flex;
  align-items: center;
}
.sidebar-nav {
  flex: 1;
  padding: 24px;
}
.sidebar-item {
  width: 100%;
  background: transparent;
  border: none;
  border-radius: 12px;
  padding: 8px 16px;
  font-family: 'DM Sans', sans-serif;
  font-size: 16px;
  font-weight: 600;
  color: var(--sidebar-item-active-text);
  cursor: pointer;
  text-align: left;
}
.sidebar-item.active {
  background: var(--sidebar-item-active-bg);
}
.sidebar-footer {
  padding: 16px 24px;
  font-family: 'Inter', sans-serif;
  font-size: 16px;
  color: #F0E8E1;
}

/* ─── Main panel ──────────────────────────────────── */
.main-panel {
  flex: 1;
  background: var(--panel-bg);
  display: flex;
  flex-direction: column;
  min-width: 0;
}

/* Action bar */
.action-bar {
  background: var(--panel-bar);
  border-bottom: 1px solid var(--panel-bar-stroke);
  height: 64px;
  display: flex;
  align-items: center;
}
.action-bar-inner {
  width: 100%;
  padding: 0 24px;
  display: flex;
  align-items: center;
  justify-content: flex-end;
}
.action-bar-btns {
  display: flex;
  align-items: center;
  gap: 16px;
}

/* Content */
.panel-content {
  padding: 24px;
}
.section-title {
  font-family: 'DM Sans', sans-serif;
  font-size: 28px;
  font-weight: 700;
  margin-bottom: 16px;
}

/* Tabs */
.tabs-wrap { margin-bottom: 16px; }
.tabs {
  display: inline-flex;
  background: var(--tab-bg);
  border: 1px solid var(--tab-stroke);
  border-radius: var(--radius-tab);
  overflow: hidden;
}
.tab {
  padding: 8px 16px;
  font-family: 'DM Sans', sans-serif;
  font-size: 16px;
  border: none;
  background: transparent;
  color: #000;
  cursor: pointer;
  transition: background .15s, color .15s;
}
.tab.active {
  background: var(--tab-active);
  color: #fff;
}

/* File list */
.state-msg { color: var(--text-secondary); padding: 40px 0; text-align: center; }
.file-list { display: flex; flex-direction: column; gap: 8px; }

.file-row {
  display: flex;
  align-items: center;
  gap: 16px;
  background: var(--file-row-bg);
  border: 1px solid var(--file-row-stroke);
  border-radius: var(--radius-btn);
  padding: 8px 16px;
}
.file-icon { width: 24px; height: 24px; flex-shrink: 0; color: #555; }
.file-info { flex: 1; min-width: 0; }
.file-name { font-family: 'DM Sans', sans-serif; font-size: 16px; font-weight: 600; display: block; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.file-expiry { font-family: 'DM Sans', sans-serif; font-size: 14px; color: var(--text); display: block; }
.file-expiry.expired { color: #C52020; }
.expired-msg { font-family: 'DM Sans', sans-serif; font-size: 14px; color: rgba(0,0,0,.5); display: block; }
.file-actions { display: flex; align-items: center; gap: 8px; flex-shrink: 0; }
.lock-icon { width: 16px; height: 16px; color: var(--text); }
.btn-sm { padding: 8px 12px; font-size: 14px; }

/* ─── Upload Modal ────────────────────────────────── */
.modal-overlay {
  position: fixed; inset: 0;
  background: rgba(0,0,0,.35);
  display: flex; align-items: center; justify-content: center;
  z-index: 100; padding: 24px;
}
.upload-modal {
  width: 100%;
  max-width: 480px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  padding: 24px 32px;
}
.upload-title {
  font-family: 'DM Sans', sans-serif;
  font-size: 28px;
  font-weight: 700;
  text-align: center;
}

/* Drop zone */
.drop-zone {
  border: 2px dashed #D9D9D9;
  border-radius: 8px;
  padding: 24px;
  text-align: center;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  color: var(--text-secondary);
  font-family: 'DM Sans', sans-serif;
  transition: border-color .2s;
}
.drop-zone.dragging { border-color: var(--orange); }

/* Selected file row */
.selected-file-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 8px 8px;
  gap: 16px;
  background: var(--panel-bg);
  border-radius: 8px;
}
.selected-file-left { display: flex; align-items: center; gap: 16px; flex: 1; min-width: 0; }
.sel-name { font-family: 'Inter', sans-serif; font-size: 16px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.sel-size { font-family: 'DM Sans', sans-serif; font-size: 14px; }
.sel-size-error { color: #F04343; }
.size-error { font-family: 'Inter', sans-serif; font-size: 16px; color: #F04343; }

/* Upload fields */
.upload-fields { display: flex; flex-direction: column; gap: 16px; }

/* Progress */
.progress-wrap { height: 6px; background: #F0E8E8; border-radius: 3px; overflow: hidden; }
.progress-bar { height: 100%; background: var(--orange); border-radius: 3px; transition: width .1s; }

/* Share box */
.success-text { font-family: 'Inter', sans-serif; font-size: 16px; }
.share-box {
  background: rgba(255, 93, 0, 0.03);
  border: 1px solid var(--orange-link-stroke);
  border-radius: var(--radius-btn);
  padding: 8px 16px;
  cursor: pointer;
  word-break: break-all;
}
.share-url { font-family: 'Inter', sans-serif; font-size: 16px; color: var(--orange-link-text); }

/* Delete modal */
.delete-modal { max-width: 360px; width: 100%; }
.delete-modal h3 { font-size: 20px; font-weight: 700; margin-bottom: 8px; }
.delete-modal p { color: var(--text-secondary); margin-bottom: 20px; }
.modal-actions { display: flex; gap: 12px; justify-content: flex-end; }

/* Mobile: hide sidebar */
@media (max-width: 767px) {
  .sidebar { display: none; }
}
</style>
