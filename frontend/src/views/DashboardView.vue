<template>
  <div class="dashboard-layout">

    <!-- Sidebar desktop (fixe) -->
    <aside class="sidebar">
      <div class="sidebar-brand">DataShare</div>
      <nav class="sidebar-nav">
        <button class="sidebar-item active">Mes fichiers</button>
      </nav>
      <div class="sidebar-footer">Copyright DataShare© 2025</div>
    </aside>

    <!-- Sidebar mobile (overlay coulissant) -->
    <transition name="slide">
      <div v-if="sidebarOpen" class="mobile-sidebar">
        <div class="mobile-sidebar-header">
          <button class="close-btn" @click="sidebarOpen = false" aria-label="Fermer le menu">✕</button>
          <span class="mobile-brand">DataShare</span>
        </div>
        <nav class="mobile-sidebar-nav">
          <button class="mobile-sidebar-item active" @click="sidebarOpen = false">Mes fichiers</button>
        </nav>
        <div class="mobile-sidebar-footer">Copyright DataShare® 2025</div>
      </div>
    </transition>
    <div v-if="sidebarOpen" class="sidebar-backdrop" @click="sidebarOpen = false"></div>

    <!-- Main panel -->
    <div class="main-panel">

      <!-- Header mobile -->
      <div class="mobile-header">
        <button class="hamburger" @click="sidebarOpen = true" aria-label="Menu">
          <span></span><span></span><span></span>
        </button>
        <div class="mobile-user">
          <div class="avatar">{{ initials }}</div>
          <span class="username">{{ auth.user?.username }}</span>
        </div>
      </div>

      <!-- Action bar desktop -->
      <div class="action-bar">
        <div class="action-bar-inner">
          <div class="action-bar-btns">
            <button class="btn-dark" @click="$router.push('/upload')">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><line x1="12" y1="3" x2="12" y2="15"/></svg>
              Ajouter des fichiers
            </button>
            <button class="btn-dark" @click="handleLogout">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><path d="M9 21H5a2 2 0 0 1-2-2V5a2 2 0 0 1 2-2h4"/><polyline points="16 17 21 12 16 7"/><line x1="21" y1="12" x2="9" y2="12"/></svg>
              Déconnexion
            </button>
          </div>
        </div>
      </div>

      <!-- Content -->
      <div class="panel-content">
        <h1 class="section-title">Mes fichiers</h1>

        <div class="tabs-wrap">
          <div class="tabs" role="tablist" aria-label="Filtrer les fichiers">
            <button v-for="t in tabs" :key="t.key" class="tab"
              role="tab"
              :aria-selected="currentTab === t.key"
              :class="{ active: currentTab === t.key }"
              @click="currentTab = t.key">{{ t.label }}</button>
          </div>
        </div>

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
              <div v-if="file.tags && file.tags.length" class="tags-row">
                <span v-for="tag in file.tags" :key="tag" class="tag-chip">{{ tag }}</span>
              </div>
            </div>

            <div class="file-actions">
              <svg v-if="!file.is_expired && file.is_password_protected"
                class="lock-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" aria-hidden="true">
                <rect x="3" y="11" width="18" height="11" rx="2" ry="2"/>
                <path d="M7 11V7a5 5 0 0 1 10 0v4"/>
              </svg>

              <!-- Desktop : boutons texte -->
              <template v-if="!file.is_expired">
                <button class="btn-orange-outline btn-sm desktop-only" @click="confirmDelete(file)">
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><polyline points="3 6 5 6 21 6"/><path d="M19 6l-1 14H6L5 6"/><path d="M10 11v6M14 11v6"/><path d="M9 6V4h6v2"/></svg>
                  Supprimer
                </button>
                <button class="btn-orange-outline btn-sm desktop-only" @click="openLink(file.share_url)">
                  Accéder
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6"><line x1="5" y1="12" x2="19" y2="12"/><polyline points="12 5 19 12 12 19"/></svg>
                </button>

                <!-- Mobile : bouton "..." -->
                <div class="menu-wrap mobile-only">
                  <button class="dots-btn" @click="toggleMenu(file.id)" aria-label="Actions">
                    <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor">
                      <circle cx="12" cy="5" r="1.5"/><circle cx="12" cy="12" r="1.5"/><circle cx="12" cy="19" r="1.5"/>
                    </svg>
                  </button>
                  <div v-if="openMenuId === file.id" class="dropdown" role="menu">
                    <button @click="openLink(file.share_url); openMenuId = null">Accéder au lien</button>
                    <button class="danger" @click="confirmDelete(file); openMenuId = null">Supprimer</button>
                  </div>
                </div>
              </template>
            </div>
          </div>
        </div>
      </div>

      <!-- FAB mobile : ajouter un fichier -->
      <button class="fab mobile-only" @click="$router.push('/upload')" aria-label="Ajouter un fichier">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="12" y1="5" x2="12" y2="19"/><line x1="5" y1="12" x2="19" y2="12"/>
        </svg>
      </button>
    </div>

    <!-- Modale suppression -->
    <div v-if="fileToDelete" class="modal-overlay" @click.self="fileToDelete = null"
      @keydown="trapFocus"
      role="dialog" aria-modal="true" aria-labelledby="delete-modal-title">
      <div class="card delete-modal">
        <h3 id="delete-modal-title">Supprimer le fichier ?</h3>
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
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'
import { useFilesStore } from '../stores/files'

const store = useFilesStore()
const auth = useAuthStore()
const router = useRouter()

const currentTab = ref('all')
const tabs = [
  { key: 'all',     label: 'Tous' },
  { key: 'active',  label: 'Actifs' },
  { key: 'expired', label: 'Expiré' },
]

const filteredFiles = computed(() => {
  if (currentTab.value === 'active')  return store.files.filter(f => !f.is_expired)
  if (currentTab.value === 'expired') return store.files.filter(f => f.is_expired)
  return store.files
})

const sidebarOpen = ref(false)
const fileToDelete = ref(null)
const openMenuId = ref(null)

const initials = computed(() => {
  const name = auth.user?.username || ''
  return name.slice(0, 2).toUpperCase()
})

onMounted(() => store.fetchFiles())

function handleLogout() { auth.logout(); router.push('/login') }
function openLink(url) { window.open(url, '_blank') }
function confirmDelete(file) { fileToDelete.value = file }
function toggleMenu(id) { openMenuId.value = openMenuId.value === id ? null : id }

async function doDelete() {
  await store.deleteFile(fileToDelete.value.id)
  fileToDelete.value = null
}

// Piège de focus dans la modale — WCAG 2.1 critère 2.4.3
function trapFocus(e) {
  const modal = document.querySelector('[role="dialog"]')
  if (!modal) return
  const focusable = modal.querySelectorAll('button, [href], input, select, [tabindex]:not([tabindex="-1"])')
  const first = focusable[0]
  const last = focusable[focusable.length - 1]
  if (e.key === 'Tab') {
    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault(); last.focus()
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault(); first.focus()
    }
  }
  if (e.key === 'Escape') fileToDelete.value = null
}

function expiryLabel(file) {
  const diff = Math.ceil((new Date(file.expires_at) - new Date()) / (1000 * 60 * 60 * 24))
  if (diff <= 0) return 'Expiré'
  if (diff === 1) return 'Expire demain'
  return `Expire dans ${diff} jours`
}
</script>

<style scoped>
.dashboard-layout { display: flex; min-height: 100vh; }

/* ─── Sidebar desktop ─── */
.sidebar { width: 259px; flex-shrink: 0; background: var(--gradient); border-right: 2px solid #623519; display: flex; flex-direction: column; }
.sidebar-brand { font-family: 'DM Sans', sans-serif; font-size: 32px; font-weight: 700; color: #1E1E1E; padding: 16px 24px; height: 72px; display: flex; align-items: center; }
.sidebar-nav { flex: 1; padding: 24px; }
.sidebar-item { width: 100%; background: rgba(0,0,0,0.12); border: none; border-radius: 12px; padding: 8px 16px; font-family: 'DM Sans', sans-serif; font-size: 16px; font-weight: 600; color: #1E1E1E; cursor: pointer; text-align: left; }
.sidebar-footer { padding: 16px 24px; font-size: 13px; color: #fff; }

/* ─── Sidebar mobile (overlay) ─── */
.mobile-sidebar {
  position: fixed; top: 0; left: 0; bottom: 0; width: 260px;
  background: var(--gradient);
  z-index: 200; display: flex; flex-direction: column;
  box-shadow: 4px 0 24px rgba(0,0,0,.2);
}
.mobile-sidebar-header { display: flex; align-items: center; gap: 12px; padding: 16px 20px; height: 64px; }
.close-btn { background: none; border: none; font-size: 20px; cursor: pointer; color: #1E1E1E; line-height: 1; }
.mobile-brand { font-family: 'DM Sans', sans-serif; font-size: 22px; font-weight: 700; color: #1E1E1E; }
.mobile-sidebar-nav { flex: 1; padding: 16px; }
.mobile-sidebar-item { width: 100%; background: rgba(0,0,0,0.12); border: none; border-radius: 12px; padding: 10px 16px; font-family: 'DM Sans', sans-serif; font-size: 16px; font-weight: 600; color: #1E1E1E; cursor: pointer; text-align: left; }
.mobile-sidebar-footer { padding: 16px 20px; font-size: 12px; color: #fff; }
.sidebar-backdrop { position: fixed; inset: 0; background: rgba(0,0,0,.4); z-index: 199; }

/* Slide transition */
.slide-enter-active, .slide-leave-active { transition: transform .25s ease; }
.slide-enter-from, .slide-leave-to { transform: translateX(-100%); }

/* ─── Main panel ─── */
.main-panel { flex: 1; background: var(--panel-bg); display: flex; flex-direction: column; min-width: 0; position: relative; }

/* ─── Mobile header ─── */
.mobile-header {
  display: none;
  align-items: center; justify-content: space-between;
  padding: 0 16px; height: 56px;
  background: var(--panel-bar);
  border-bottom: 1px solid var(--panel-bar-stroke);
}
.hamburger { background: none; border: none; cursor: pointer; display: flex; flex-direction: column; gap: 5px; padding: 4px; }
.hamburger span { display: block; width: 22px; height: 2px; background: #333; border-radius: 2px; }
.mobile-user { display: flex; align-items: center; gap: 8px; }
.avatar { width: 32px; height: 32px; border-radius: 50%; background: #2C2C2C; color: #F3EEEA; font-family: 'DM Sans', sans-serif; font-size: 13px; font-weight: 700; display: flex; align-items: center; justify-content: center; }
.username { font-family: 'DM Sans', sans-serif; font-size: 14px; font-weight: 600; }

/* ─── Action bar desktop ─── */
.action-bar { background: var(--panel-bar); border-bottom: 1px solid var(--panel-bar-stroke); height: 64px; display: flex; align-items: center; }
.action-bar-inner { width: 100%; padding: 0 24px; display: flex; align-items: center; justify-content: flex-end; }
.action-bar-btns { display: flex; align-items: center; gap: 16px; }

/* ─── Content ─── */
.panel-content { padding: 24px; }
.section-title { font-family: 'DM Sans', sans-serif; font-size: 28px; font-weight: 700; margin-bottom: 16px; }
.tabs-wrap { margin-bottom: 16px; }
.tabs { display: inline-flex; background: var(--tab-bg); border: 1px solid var(--tab-stroke); border-radius: var(--radius-tab); overflow: hidden; }
.tab { padding: 8px 16px; font-family: 'DM Sans', sans-serif; font-size: 15px; border: none; background: transparent; color: #555; cursor: pointer; transition: background .15s, color .15s; }
.tab.active { background: #7A2E00; color: #fff; border-radius: var(--radius-tab); } /* #7A2E00 = 8.6:1 sur blanc ✅ */

/* ─── File list ─── */
.state-msg { color: var(--text-secondary); padding: 40px 0; text-align: center; }
.file-list { display: flex; flex-direction: column; gap: 8px; }
.file-row { display: flex; align-items: center; gap: 12px; background: var(--file-row-bg); border: 1px solid var(--file-row-stroke); border-radius: var(--radius-btn); padding: 10px 14px; }
.file-icon { width: 22px; height: 22px; flex-shrink: 0; color: #767676; }
.file-info { flex: 1; min-width: 0; }
.file-name { font-family: 'DM Sans', sans-serif; font-size: 15px; font-weight: 600; display: block; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.file-expiry { font-family: 'DM Sans', sans-serif; font-size: 13px; color: #767676; display: block; margin-top: 2px; }
.file-expiry.expired { color: #C52020; }
.file-actions { display: flex; align-items: center; gap: 6px; flex-shrink: 0; }
.lock-icon { width: 15px; height: 15px; color: #767676; }
.btn-sm { padding: 7px 12px; font-size: 13px; }

/* Tags */
.tags-row { display: flex; flex-wrap: wrap; gap: 4px; margin-top: 4px; }
.tag-chip { background: #FFF3EB; border: 1px solid #B35400; color: #B35400; border-radius: 99px; padding: 1px 9px; font-size: 11px; font-family: 'Inter', sans-serif; }

/* Dots menu */
.menu-wrap { position: relative; }
.dots-btn { background: #f0ece8; border: none; border-radius: 8px; width: 32px; height: 32px; cursor: pointer; display: flex; align-items: center; justify-content: center; color: #555; }
.dropdown { position: absolute; right: 0; top: 36px; background: #fff; border: 1px solid #e0dbd5; border-radius: 10px; box-shadow: 0 4px 16px rgba(0,0,0,.12); min-width: 150px; z-index: 50; overflow: hidden; }
.dropdown button { width: 100%; padding: 12px 16px; background: none; border: none; text-align: left; font-family: 'DM Sans', sans-serif; font-size: 14px; cursor: pointer; }
.dropdown button:hover { background: #f8f5f2; }
.dropdown button.danger { color: #C52020; }

/* FAB mobile */
.fab { position: fixed; bottom: 24px; right: 24px; width: 56px; height: 56px; border-radius: 50%; background: var(--orange, #FF812D); border: none; cursor: pointer; color: #fff; display: flex; align-items: center; justify-content: center; box-shadow: 0 4px 16px rgba(255,129,45,.5); z-index: 100; }

/* Delete modal */
.modal-overlay { position: fixed; inset: 0; background: rgba(0,0,0,.35); display: flex; align-items: center; justify-content: center; z-index: 300; padding: 24px; }
.delete-modal { max-width: 360px; width: 100%; }
.delete-modal h3 { font-size: 20px; font-weight: 700; margin-bottom: 8px; }
.delete-modal p { color: var(--text-secondary); margin-bottom: 20px; font-size: 14px; }
.modal-actions { display: flex; gap: 12px; justify-content: flex-end; }

/* ─── Responsive ─── */
.desktop-only { display: inline-flex; }
.mobile-only  { display: none; }

@media (max-width: 767px) {
  .sidebar       { display: none; }
  .action-bar    { display: none; }
  .mobile-header { display: flex; }
  .desktop-only  { display: none !important; }
  .mobile-only   { display: flex; }

  /* Fond warm cream du système */
  .main-panel { background: var(--panel-bg); }

  /* Header : fond panel-bar du système, sans bordure visible */
  .mobile-header {
    background: var(--panel-bg);
    border-bottom: none;
    padding: 0 20px;
    height: 56px;
  }
  .hamburger span { background: var(--text); }
  .username { font-size: 15px; font-weight: 700; color: var(--text); }
  .avatar {
    width: 34px; height: 34px;
    background: var(--tab-active);
    font-size: 13px;
  }

  /* Contenu */
  .panel-content { padding: 20px 16px 80px; }
  .section-title { font-size: 26px; font-weight: 800; margin-bottom: 16px; color: var(--text); }

  /* Tabs — pill style, pas de conteneur */
  .tabs-wrap { margin-bottom: 14px; }
  .tabs {
    background: transparent;
    border: none;
    gap: 2px;
  }
  .tab {
    padding: 7px 18px;
    font-size: 14px;
    font-weight: 600;
    color: var(--text-secondary);
    border-radius: 99px;
    border: none;
    background: transparent;
  }
  .tab.active {
    background: var(--tab-active);
    color: #1E1E1E;  /* texte foncé sur fond saumon — ratio 7:1 ✅ */
    border-radius: 99px;
    font-weight: 700;
  }

  /* File rows — fond tab-bg du système (saumon léger) */
  .file-list { gap: 10px; }
  .file-row {
    background: var(--tab-bg);
    border: none;
    border-radius: 12px;
    padding: 12px 14px;
    gap: 12px;
  }
  .file-icon { color: var(--tab-active); }
  .file-name { font-size: 14px; font-weight: 700; color: var(--text); }
  .file-expiry { font-size: 12px; color: var(--text-secondary); margin-top: 2px; }
  .file-expiry.expired { color: #C52020; font-weight: 600; }
  .lock-icon { color: var(--text-secondary); }

  /* Dots button */
  .dots-btn {
    background: rgba(255,192,145,0.25);
    border-radius: 8px;
    width: 30px; height: 30px;
    color: var(--text);
  }
}
</style>
