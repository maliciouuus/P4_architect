/**
 * Store Pinia pour l'authentification.
 *
 * Gère l'état de connexion de l'utilisateur, les tokens JWT,
 * et expose les actions login / register / logout / fetchMe.
 */

import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

import api from '../api/client'

export const useAuthStore = defineStore('auth', () => {
  // L'utilisateur connecté — null si personne n'est connecté
  const user = ref(null)

  // Propriété calculée : vrai dès qu'on a un objet utilisateur en mémoire
  const isAuthenticated = computed(() => !!user.value)

  /**
   * Connecte un utilisateur avec son email et mot de passe.
   * NestJS retourne { access_token, user } — pas de refresh token (JWT 7 jours).
   * Le token est stocké dans localStorage et le profil chargé immédiatement.
   */
  async function login(email, password) {
    // NestJS attend { email, password } — sans trailing slash contrairement à Django
    const { data } = await api.post('/auth/login', { email, password })
    // NestJS retourne access_token (pas access/refresh comme Django SimpleJWT)
    localStorage.setItem('access_token', data.access_token)
    await fetchMe()
  }

  /**
   * Inscrit un nouvel utilisateur puis le connecte automatiquement.
   * password2 est ignoré par NestJS (whitelist: true dans ValidationPipe)
   * mais on le garde pour ne pas modifier la vue RegisterView.
   */
  async function register(username, email, password, password2) {
    await api.post('/auth/register', { username, email, password })
    // On connecte avec l'email — NestJS utilise l'email comme identifiant de connexion
    await login(email, password)
  }

  /**
   * Récupère le profil de l'utilisateur connecté depuis l'API.
   * Appelé au démarrage de l'app si un token existe en localStorage,
   * pour restaurer la session sans redemander la connexion.
   */
  async function fetchMe() {
    try {
      const { data } = await api.get('/auth/me')
      user.value = data
    } catch {
      user.value = null
    }
  }

  /**
   * Déconnecte l'utilisateur côté client.
   * NestJS est stateless (JWT) — il suffit de supprimer le token local.
   */
  function logout() {
    localStorage.removeItem('access_token')
    user.value = null
  }

  return { user, isAuthenticated, login, register, fetchMe, logout }
})
