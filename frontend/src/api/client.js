/**
 * Client HTTP centralisé pour toutes les requêtes vers l'API Django.
 *
 * On utilise Axios avec deux intercepteurs :
 * - Requête : injecte le token JWT dans chaque appel si disponible
 * - Réponse : tente un refresh automatique si le token est expiré (401)
 */

import axios from 'axios'

// L'URL de base pointe vers le proxy Vite qui redirige vers Django :8000
const api = axios.create({
  baseURL: '/api',
})

// Intercepteur de requête — ajoute le header Authorization si on a un token
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// Intercepteur de réponse — gère le renouvellement automatique du token expiré
api.interceptors.response.use(
  // Si la réponse est OK, on la passe sans modification
  (response) => response,

  async (error) => {
    const originalRequest = error.config

    // On tente un refresh uniquement sur une erreur 401 et si on n'a pas déjà réessayé
    // (le flag _retry évite une boucle infinie si le refresh échoue aussi)
    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true
      const refresh = localStorage.getItem('refresh_token')

      if (refresh) {
        try {
          // On appelle directement axios pour éviter que l'intercepteur
          // ne s'applique à nouveau sur cette requête de refresh
          const { data } = await axios.post('/api/auth/token/refresh/', { refresh })
          localStorage.setItem('access_token', data.access)
          originalRequest.headers.Authorization = `Bearer ${data.access}`
          // On relance la requête originale avec le nouveau token
          return api(originalRequest)
        } catch {
          // Le refresh a échoué (token révoqué ou expiré) — on déconnecte
          localStorage.removeItem('access_token')
          localStorage.removeItem('refresh_token')
          window.location.href = '/login'
        }
      }
    }

    return Promise.reject(error)
  },
)

export default api
