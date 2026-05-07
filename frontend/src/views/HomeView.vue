<template>
  <div class="gradient-page">
    <header class="guest-header">
      <span class="brand">DataShare</span>
      <router-link v-if="auth.isAuthenticated" to="/dashboard" class="btn-dark">
        Mon espace
      </router-link>
      <router-link v-else to="/login" class="btn-dark">
        Se connecter
      </router-link>
    </header>

    <!-- Vue landing -->
    <div v-if="!showUpload" class="hero">
      <h1 class="tagline">Tu veux partager un fichier ?</h1>
      <button class="icon-btn" @click="handleUploadClick" aria-label="Partager un fichier">
        <div class="icon-ring-outer">
          <div class="icon-ring-inner">
            <svg width="48" height="48" viewBox="0 0 48 48" fill="none">
              <path d="M8 32a12 12 0 0 1 0-24h1A14 14 0 0 1 39 16h1a10 10 0 0 1 0 20H8z"
                stroke="#FFEDEC" stroke-width="4" fill="none"/>
              <path d="M24 22v12M20 26l4-4 4 4"
                stroke="#FFEDEC" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
          </div>
        </div>
      </button>
    </div>

    <!-- Vue upload anonyme (US07) -->
    <div v-else class="hero">
      <div class="card upload-card">
        <h1 class="upload-title">Ajouter un fichier</h1>

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
        <button type="button" class="drop-zone" @click="fileInput.click()"
          @dragover.prevent="dragging=true" @dragleave.prevent="dragging=false"
          @drop.prevent="onDrop" :class="{dragging}"
          aria-label="Sélectionner un fichier à envoyer">
          <svg aria-hidden="true" width="32" height="32" viewBox="0 0 24 24" fill="none" stroke="#767676" stroke-width="1.5">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
            <polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/>
          </svg>
          <p>Glissez un fichier ou <strong>cliquez ici</strong></p>
        </button>
        <input ref="fileInput" type="file" hidden aria-label="Sélectionner un fichier" @change="onFileChange" />

        <!-- Champs -->
        <div class="upload-fields">
          <div class="field">
            <label for="anon-password">Mot de passe</label>
            <input id="anon-password" type="password" v-model="password"
              placeholder="Optionnel — min. 6 caractères" aria-required="false" />
          </div>
          <div class="field">
            <label for="anon-expiry">Expiration</label>
            <select id="anon-expiry" v-model="expiryHours">
              <option :value="24">Une journée</option>
              <option :value="72">3 jours</option>
              <option :value="168">Une semaine</option>
            </select>
          </div>
        </div>

        <!-- Barre de progression -->
        <div v-if="progress !== null" class="progress-wrap">
          <div class="progress-bar" :style="{ width: progress + '%' }"></div>
        </div>

        <!-- Erreur -->
        <div v-if="uploadError" role="alert" class="alert alert-error">{{ uploadError }}</div>

        <!-- Lien après upload -->
        <template v-if="shareUrl">
          <p class="success-text">Fichier partagé ! Copiez le lien ci-dessous :</p>
          <div class="share-box" @click="copyLink">
            <span class="share-url">{{ shareUrl }}</span>
          </div>
          <button class="btn-orange-outline" style="width:100%;justify-content:center" @click="copyLink">
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6">
              <rect x="9" y="9" width="13" height="13" rx="2"/>
              <path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/>
            </svg>
            {{ copied ? '✓ Copié !' : 'Copier le lien' }}
          </button>
          <button class="btn-ghost" @click="reset">Envoyer un autre fichier</button>
        </template>

        <button v-if="!shareUrl"
          class="btn-orange-solid"
          :disabled="!selectedFile || uploading"
          @click="doUpload">
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6">
            <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
            <polyline points="17 8 12 3 7 8"/>
            <line x1="12" y1="3" x2="12" y2="15"/>
          </svg>
          {{ uploading ? 'Envoi…' : 'Téléverser' }}
        </button>
      </div>
    </div>

    <footer class="page-footer">Copyright DataShare® 2025</footer>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import api from '../api/client'

const auth = useAuthStore()
const router = useRouter()

const showUpload = ref(false)
const fileInput = ref(null)
const selectedFile = ref(null)
const dragging = ref(false)
const password = ref('')
const expiryHours = ref(24)
const uploading = ref(false)
const progress = ref(null)
const uploadError = ref('')
const shareUrl = ref('')
const copied = ref(false)

function handleUploadClick() {
  if (auth.isAuthenticated) {
    router.push('/dashboard')
  } else {
    showUpload.value = true
  }
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

async function doUpload() {
  if (!selectedFile.value) return
  if (password.value && password.value.length < 6) {
    uploadError.value = 'Le mot de passe doit faire au moins 6 caractères.'
    return
  }

  uploadError.value = ''
  uploading.value = true
  progress.value = 0

  const form = new FormData()
  form.append('file', selectedFile.value)
  if (password.value) form.append('password', password.value)
  form.append('expiry_hours', expiryHours.value)

  try {
    const { data } = await api.post('/files/upload/anonymous', form, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress: (e) => {
        progress.value = Math.round((e.loaded * 100) / e.total)
      },
    })
    shareUrl.value = data.share_url
    selectedFile.value = null
    password.value = ''
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

.hero { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 24px; padding: 24px; }
.tagline { font-family: 'DM Sans', sans-serif; font-size: 30px; font-weight: 300; color: #000; text-align: center; max-width: 320px; }

.icon-btn { background: none; border: none; cursor: pointer; padding: 0; }
.icon-ring-outer { width: 144px; height: 144px; background: rgba(46,24,13,.15); border-radius: 50%; display: flex; align-items: center; justify-content: center; transition: transform .15s; }
.icon-btn:hover .icon-ring-outer { transform: scale(1.05); }
.icon-ring-inner { width: 96px; height: 96px; background: #0F0118; border-radius: 50%; display: flex; align-items: center; justify-content: center; }

/* Upload card */
.upload-card { width: 100%; max-width: 480px; display: flex; flex-direction: column; gap: 16px; padding: 24px 32px; }
.upload-title { font-family: 'DM Sans', sans-serif; font-size: 28px; font-weight: 700; text-align: center; }

.drop-zone { border: 2px dashed #D9D9D9; border-radius: 8px; padding: 24px; text-align: center; cursor: pointer; display: flex; flex-direction: column; align-items: center; gap: 8px; color: #595959; background: #fff; font-family: 'DM Sans', sans-serif; transition: border-color .2s; }
.drop-zone.dragging { border-color: var(--orange); }

.selected-file-row { display: flex; align-items: center; justify-content: space-between; padding: 8px; gap: 16px; background: var(--panel-bg, #fafafa); border-radius: 8px; }
.selected-file-left { display: flex; align-items: center; gap: 12px; flex: 1; min-width: 0; }
.file-icon { width: 24px; height: 24px; flex-shrink: 0; color: #555; }
.sel-name { font-family: 'Inter', sans-serif; font-size: 14px; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 220px; }
.sel-size { font-family: 'DM Sans', sans-serif; font-size: 13px; color: #767676; }

.upload-fields { display: flex; flex-direction: column; gap: 12px; }
.btn-sm { padding: 6px 12px; font-size: 13px; }

.progress-wrap { height: 6px; background: #F0E8E8; border-radius: 3px; overflow: hidden; }
.progress-bar { height: 100%; background: var(--orange); border-radius: 3px; transition: width .1s; }

.success-text { font-family: 'Inter', sans-serif; font-size: 15px; text-align: center; }
.share-box { background: rgba(255,129,45,.06); border: 1px solid rgba(255,129,45,.4); border-radius: 8px; padding: 10px 16px; cursor: pointer; word-break: break-all; }
.share-url { font-family: 'Inter', sans-serif; font-size: 14px; color: #B35400; }

.btn-ghost { background: none; border: none; cursor: pointer; font-family: 'DM Sans', sans-serif; font-size: 14px; color: #767676; text-decoration: underline; padding: 4px 0; align-self: center; }

.page-footer { padding: 16px 24px; font-family: 'Inter', sans-serif; font-size: 16px; color: #fff; flex-shrink: 0; }
</style>
