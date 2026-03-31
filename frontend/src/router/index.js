/**
 * Configuration du routeur Vue Router.
 *
 * Définit les routes de l'application et les gardes de navigation
 * pour protéger les pages réservées aux utilisateurs connectés.
 */

import { createRouter, createWebHistory } from 'vue-router'

import { useAuthStore } from '../stores/auth'

const routes = [
  {
    // Page d'accueil — gradient avec tagline et icône d'upload
    path: '/',
    component: () => import('../views/HomeView.vue'),
    meta: { guest: true },
  },
  {
    // Page de connexion
    path: '/login',
    component: () => import('../views/LoginView.vue'),
    meta: { guest: true },
  },
  {
    // Page de création de compte
    path: '/register',
    component: () => import('../views/RegisterView.vue'),
    meta: { guest: true },
  },
  {
    // Tableau de bord — liste des fichiers et upload (connecté uniquement)
    path: '/dashboard',
    component: () => import('../views/DashboardView.vue'),
    meta: { requiresAuth: true },
  },
  {
    // Page publique de téléchargement — accessible sans compte
    path: '/download/:token',
    component: () => import('../views/DownloadView.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

/**
 * Garde de navigation globale.
 *
 * Avant chaque changement de page :
 * 1. Si un token existe en localStorage mais que le store est vide,
 *    on restaure la session en chargeant le profil depuis l'API.
 * 2. Les pages marquées requiresAuth redirigent vers /login si non connecté.
 * 3. Les pages marquées guest redirigent vers /dashboard si déjà connecté
 *    (pour éviter d'afficher la page de login à quelqu'un déjà connecté).
 */
router.beforeEach(async (to) => {
  const auth = useAuthStore()

  // Restauration de session si un token existe mais que le profil n'est pas chargé
  if (!auth.user && localStorage.getItem('access_token')) {
    await auth.fetchMe()
  }

  if (to.meta.requiresAuth && !auth.isAuthenticated) return '/login'
  if (to.meta.guest && auth.isAuthenticated && to.path !== '/download') return '/dashboard'
})

export default router
