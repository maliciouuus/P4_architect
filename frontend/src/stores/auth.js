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
   * Connecte un utilisateur avec son nom d'utilisateur et mot de passe.
   * Stocke les tokens JWT dans localStorage et charge le profil.
   */
  async function login(username, password) {
    const { data } = await api.post('/auth/login/', { username, password })
    localStorage.setItem('access_token', data.access)
    localStorage.setItem('refresh_token', data.refresh)
    // On charge le profil immédiatement pour renseigner `user`
    await fetchMe()
  }

  /**
   * Inscrit un nouvel utilisateur puis le connecte automatiquement.
   * Le login après inscription évite de redemander les identifiants.
   */
  async function register(username, email, password, password2) {
    await api.post('/auth/register/', { username, email, password, password2 })
    await login(username, password)
  }

  /**
   * Récupère le profil de l'utilisateur connecté depuis l'API.
   * Appelé au démarrage de l'app si un token existe en localStorage,
   * pour restaurer la session sans redemander la connexion.
   */
  async function fetchMe() {
    try {
      const { data } = await api.get('/auth/me/')
      user.value = data
    } catch {
      // Si le token est invalide ou expiré, on repart de zéro
      user.value = null
    }
  }

  /**
   * Déconnecte l'utilisateur côté client.
   * On supprime les tokens et on vide l'état — le router redirige vers /login.
   */
  function logout() {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    user.value = null
  }

  return { user, isAuthenticated, login, register, fetchMe, logout }
})
