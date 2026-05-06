/**
 * Client HTTP centralisé pour toutes les requêtes vers l'API NestJS.
 *
 * Utilise Axios avec deux intercepteurs :
 * - Requête : injecte le token JWT dans chaque appel si disponible
 * - Réponse : redirige vers /login si le token est invalide ou expiré (401)
 *
 * NestJS émet des tokens JWT avec une durée de 7 jours (pas de refresh token).
 * Si un 401 est reçu, le token a expiré — on déconnecte proprement.
 */

import axios from 'axios'

// L'URL de base pointe vers le proxy Vite configuré dans vite.config.js
// qui redirige les appels /api/* vers NestJS sur :8000
const api = axios.create({
  baseURL: '/api',
})

// Intercepteur de requête — injecte le token JWT dans l'en-tête Authorization
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Intercepteur de réponse — déconnecte l'utilisateur si le token est invalide
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Si NestJS répond 401, le token est expiré ou absent — on nettoie et redirige
    if (error.response?.status === 401) {
      localStorage.removeItem('access_token')
      // Redirige seulement si on n'est pas déjà sur la page de login
      if (!window.location.pathname.startsWith('/login')) {
        window.location.href = '/login'
      }
    }
    return Promise.reject(error)
  },
)

export default api
