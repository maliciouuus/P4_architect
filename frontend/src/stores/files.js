/**
 * Store Pinia pour la gestion des fichiers partagés.
 *
 * Centralise la liste des fichiers de l'utilisateur connecté
 * et expose les actions fetch / upload / delete.
 */

import { defineStore } from 'pinia'
import { ref } from 'vue'

import api from '../api/client'

export const useFilesStore = defineStore('files', () => {
  // Liste des fichiers chargés depuis l'API
  const files = ref([])

  // Vrai pendant le chargement initial de la liste
  const loading = ref(false)

  // Message d'erreur en cas d'échec du chargement
  const error = ref(null)

  /**
   * Charge la liste des fichiers de l'utilisateur connecté.
   * Réinitialise l'erreur à chaque appel pour ne pas afficher
   * une ancienne erreur après un rechargement réussi.
   */
  async function fetchFiles() {
    loading.value = true
    error.value = null
    try {
      const { data } = await api.get('/files/')
      files.value = data
    } catch {
      error.value = 'Impossible de charger les fichiers.'
    } finally {
      loading.value = false
    }
  }

  /**
   * Uploade un fichier vers l'API avec options de protection et d'expiration.
   *
   * @param {File} file - Le fichier à envoyer
   * @param {object} options
   * @param {string} options.password - Mot de passe optionnel (vide = pas de protection)
   * @param {number} options.expiryHours - Durée de validité du lien en heures
   * @param {function} options.onProgress - Callback appelé avec le pourcentage d'avancement
   * @returns {object} Les métadonnées du fichier créé (dont share_url)
   */
  async function uploadFile(file, { password = '', expiryHours = 24, onProgress } = {}) {
    const form = new FormData()
    form.append('file', file)
    if (password) form.append('password', password)
    form.append('expiry_hours', expiryHours)

    const { data } = await api.post('/files/upload/', form, {
      headers: { 'Content-Type': 'multipart/form-data' },
      onUploadProgress: (e) => {
        // On calcule le pourcentage et on appelle le callback si fourni
        if (onProgress) onProgress(Math.round((e.loaded * 100) / e.total))
      },
    })

    // On ajoute le nouveau fichier en tête de liste sans recharger toute la liste
    files.value.unshift(data)
    return data
  }

  /**
   * Supprime un fichier par son identifiant et le retire de la liste locale.
   * La liste locale est mise à jour immédiatement sans attendre un rechargement.
   */
  async function deleteFile(id) {
    await api.delete(`/files/${id}/delete/`)
    files.value = files.value.filter((f) => f.id !== id)
  }

  return { files, loading, error, fetchFiles, uploadFile, deleteFile }
})
