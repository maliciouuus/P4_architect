<template>
  <div class="gradient-page">
    <header class="upload-header">
      <span class="brand">DataShare</span>
      <div class="header-actions">
        <button class="btn-dark" @click="handleLogout">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6">
            <path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/>
            <polyline points="16 17 21 12 16 7"/>
            <line x1="21" y1="12" x2="9" y2="12"/>
          </svg>
          Déconnexion
        </button>
      </div>
    </header>

    <div class="hero">
      <div class="card upload-card">
        <h1 class="upload-title">Ajouter un fichier</h1>

        <!-- ── Vue résultat (après upload) ── -->
        <template v-if="shareUrl">
          <div class="selected-file-row">
            <div class="selected-file-left">
              <svg class="file-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14 2 14 8 20 8"/>
              </svg>
              <div>
                <p class="sel-name">{{ uploadedName }}</p>
                <p class="sel-size">{{ uploadedSize }}</p>
              </div>
            </div>
          </div>

          <p class="success-text">
            Félicitations, ton fichier sera conservé chez nous pendant
            {{ expiryHours === 24 ? 'une journée' : expiryHours === 72 ? '3 jours' : 'une semaine' }} !
          </p>

          <button class="share-link-btn" @click="copyLink">
            {{ copied ? '✓ Copié !' : shareUrl }}
          </button>

          <button class="btn-orange-solid" @click="$router.push('/dashboard')">
            Téléverser
          </button>

          <button class="btn-ghost" @click="reset">Envoyer un autre fichier</button>
        </template>

        <!-- ── Vue formulaire ── -->
        <template v-else>
          <!-- Fichier sélectionné -->
          <div v-if="selectedFile" class="selected-file-row">
            <div class="selected-file-left">
              <svg class="file-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/>
                <polyline points="14 2 14 8 20 8"/>
              </svg>
              <div>
                <p class="sel-name">{{ selectedFile.name }}</p>
                <p class="sel-size">{{ formatSize(selectedFile.size) }}</p>
              </div>
            </div>
            <button class="btn-orange-outline btn-sm" @click="fileInput.click()">Changer</button>
          </div>
          <button v-else type="button" class="drop-zone" @click="fileInput.click()"
            @dragover.prevent="dragging=true" @dragleave.prevent="dragging=false"
            @drop.prevent="onDrop" :class="{ dragging }"
            aria-label="Sélectionner un fichier à envoyer">
            <svg aria-hidden="true" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#767676" stroke-width="1.5">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
              <polyline points="17 8 12 3 7 8"/>
              <line x1="12" y1="3" x2="12" y2="15"/>
            </svg>
            <p>Glissez un fichier ou <strong>cliquez ici</strong></p>
          </button>
          <input ref="fileInput" type="file" hidden aria-label="Sélectionner un fichier" @change="onFileChange" />

          <!-- Champs -->
          <div class="upload-fields">
            <div class="field">
              <label for="up-password">Mot de passe</label>
              <input id="up-password" type="password" v-model="password"
                placeholder="Optionnel — min. 6 caractères" />
            </div>
            <div class="field">
              <label for="up-expiry">Expiration</label>
              <select id="up-expiry" v-model="expiryHours">
                <option :value="24">Une journée</option>
                <option :value="72">3 jours</option>
                <option :value="168">Une semaine</option>
              </select>
            </div>
            <div class="field">
              <label for="up-tags">Tags (optionnel)</label>
              <input id="up-tags" type="text" v-model="tagsInput"
                placeholder="ex: client, facture, urgent"
                aria-describedby="tags-hint"
                @keydown.enter.prevent="addTag"
                @keydown.comma.prevent="addTag" />
              <div v-if="tags.length" class="tags-row">
                <span v-for="tag in tags" :key="tag" class="tag-chip">
                  {{ tag }}
                  <button class="tag-remove" @click="removeTag(tag)" :aria-label="'Supprimer le tag ' + tag">×</button>
                </span>
              </div>
              <p id="tags-hint" class="field-hint">Appuyez sur Entrée ou virgule pour ajouter</p>
            </div>
          </div>

          <!-- Progression -->
          <div v-if="progress !== null" class="progress-wrap">
            <div class="progress-bar" :style="{ width: progress + '%' }"></div>
          </div>

          <!-- Erreur -->
          <div v-if="uploadError" role="alert" class="alert alert-error">{{ uploadError }}</div>

          <button class="btn-orange-solid"
            :disabled="!selectedFile || uploading"
            @click="doUpload"
            style="margin-top: 4px">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6">
              <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
              <polyline points="17 8 12 3 7 8"/>
              <line x1="12" y1="3" x2="12" y2="15"/>
            </svg>
            {{ uploading ? 'Envoi…' : 'Téléverser' }}
          </button>
        </template>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useFilesStore } from '../stores/files'

const router = useRouter()
const auth = useAuthStore()
const store = useFilesStore()

const fileInput = ref(null)
const selectedFile = ref(null)
const dragging = ref(false)
const password = ref('')
const expiryHours = ref(24)
const tagsInput = ref('')
const tags = ref([])
const uploading = ref(false)
const progress = ref(null)
const uploadError = ref('')
const shareUrl = ref('')
const uploadedName = ref('')
const uploadedSize = ref('')
const copied = ref(false)

function handleLogout() {
  auth.logout()
  router.push('/login')
}

function onDrop(e) {
  dragging.value = false
  selectedFile.value = e.dataTransfer.files[0] || null
}

function onFileChange(e) {
  selectedFile.value = e.target.files[0] || null
  e.target.value = ''
  shareUrl.value = ''
  uploadError.value = ''
}

function addTag() {
  const val = tagsInput.value.trim().replace(/,$/, '')
  if (!val || val.length > 30 || tags.value.includes(val)) return
  tags.value.push(val)
  tagsInput.value = ''
}

function removeTag(tag) {
  tags.value = tags.value.filter(t => t !== tag)
}

async function doUpload() {
  if (!selectedFile.value) return
  if (password.value && password.value.length < 6) {
    uploadError.value = 'Le mot de passe doit faire au moins 6 caractères.'
    return
  }

  uploadError.value = ''
  uploading.value = true
  progress.value = 0

  try {
    const result = await store.uploadFile(selectedFile.value, {
      password: password.value,
      expiryHours: expiryHours.value,
      onProgress: (p) => { progress.value = p },
    })
    uploadedName.value = selectedFile.value.name
    uploadedSize.value = formatSize(selectedFile.value.size)
    shareUrl.value = result.share_url
    selectedFile.value = null
    password.value = ''
    tags.value = []
  } catch (e) {
    const msg = e.response?.data?.message
    if (Array.isArray(msg)) uploadError.value = msg[0]
    else uploadError.value = msg || 'Erreur lors de l\'envoi.'
  } finally {
    uploading.value = false
    progress.value = null
  }
}

async function copyLink() {
  await navigator.clipboard.writeText(shareUrl.value)
  copied.value = true
  setTimeout(() => { copied.value = false }, 2000)
}

function reset() {
  shareUrl.value = ''
  selectedFile.value = null
  uploadError.value = ''
  password.value = ''
  tags.value = []
}

function formatSize(bytes) {
  if (bytes < 1024) return bytes + ' o'
  if (bytes < 1_048_576) return (bytes / 1024).toFixed(1) + ' Ko'
  return (bytes / 1_048_576).toFixed(1) + ' Mo'
}
</script>

<style scoped>
.gradient-page { min-height: 100vh; background: var(--gradient); display: flex; flex-direction: column; }

.upload-header {
  display: flex; align-items: center; justify-content: space-between;
  padding: 16px 24px; height: 72px; flex-shrink: 0; gap: 12px;
}
.brand { font-family: 'DM Sans', sans-serif; font-size: 32px; font-weight: 700; color: #000; white-space: nowrap; }

@media (max-width: 480px) {
  .upload-header { padding: 12px 16px; height: auto; }
  .brand { font-size: 24px; }
}
.header-actions { display: flex; align-items: center; gap: 12px; }
.btn-ghost-header {
  display: flex; align-items: center; gap: 6px;
  background: none; border: none; cursor: pointer;
  font-family: 'DM Sans', sans-serif; font-size: 14px;
  color: #000; font-weight: 600;
}

.hero { flex: 1; display: flex; align-items: center; justify-content: center; padding: 24px; }

.upload-card { width: 100%; max-width: 520px; display: flex; flex-direction: column; gap: 16px; padding: 32px; }

/* Mobile : carte qui remonte depuis le bas sur fond gradient */
@media (max-width: 640px) {
  .gradient-page { justify-content: flex-end; }
  .upload-header { position: absolute; top: 0; left: 0; right: 0; }
  .hero { align-items: flex-end; justify-content: flex-end; padding: 0; width: 100%; }
  .upload-card {
    max-width: 100%;
    border-radius: 24px 24px 0 0;
    padding: 28px 20px 40px;
    box-shadow: 0 -4px 32px rgba(0,0,0,.12);
  }
}
.upload-title { font-family: 'DM Sans', sans-serif; font-size: 28px; font-weight: 700; text-align: center; }

.drop-zone {
  border: 2px dashed #D9D9D9; border-radius: 8px; padding: 32px 24px;
  text-align: center; cursor: pointer; display: flex; flex-direction: column;
  align-items: center; gap: 8px; color: #595959;
  background: #fff;
  font-family: 'DM Sans', sans-serif; transition: border-color .2s;
}
.drop-zone.dragging { border-color: var(--orange); }

.selected-file-row { display: flex; align-items: center; justify-content: space-between; padding: 10px 12px; gap: 12px; background: #f9f9f9; border-radius: 8px; }
.selected-file-left { display: flex; align-items: center; gap: 12px; flex: 1; min-width: 0; }
.file-icon { width: 24px; height: 24px; flex-shrink: 0; color: #555; }
.sel-name { font-family: 'Inter', sans-serif; font-size: 14px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 260px; }
.sel-size { font-family: 'DM Sans', sans-serif; font-size: 12px; color: #767676; }
.btn-sm { padding: 6px 12px; font-size: 13px; }

.upload-fields { display: flex; flex-direction: column; gap: 12px; }

.progress-wrap { height: 6px; background: #F0E8E8; border-radius: 3px; overflow: hidden; }
.progress-bar { height: 100%; background: var(--orange); border-radius: 3px; transition: width .1s; }

.success-text {
  font-family: 'Inter', sans-serif;
  font-size: 14px;
  color: var(--text-secondary);
  text-align: left;
}
.share-link-btn {
  background: none;
  border: none;
  cursor: pointer;
  font-family: 'Inter', sans-serif;
  font-size: 14px;
  color: var(--orange-link-text);
  text-align: left;
  word-break: break-all;
  padding: 0;
  text-decoration: underline;
}

.result-actions { display: flex; gap: 12px; }
.result-actions > * { flex: 1; justify-content: center; }

.btn-ghost { background: none; border: none; cursor: pointer; font-family: 'DM Sans', sans-serif; font-size: 13px; color: #767676; text-decoration: underline; padding: 4px 0; align-self: center; }

.tags-row { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 6px; }
.tag-chip { display: inline-flex; align-items: center; gap: 4px; background: #FFF3EB; border: 1px solid #B35400; color: #B35400; border-radius: 99px; padding: 2px 10px; font-size: 12px; }
.tag-remove { background: none; border: none; cursor: pointer; color: #B35400; font-size: 14px; padding: 0; }
.field-hint { font-size: 11px; color: #767676; margin-top: 4px; font-family: 'Inter', sans-serif; }

.page-footer { padding: 16px 24px; font-family: 'Inter', sans-serif; font-size: 14px; color: #fff; flex-shrink: 0; text-align: center; }
</style>
