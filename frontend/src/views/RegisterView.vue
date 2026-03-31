<template>
  <div class="gradient-page">
    <header class="guest-header">
      <span class="brand">DataShare</span>
      <router-link to="/login" class="btn-dark">Se connecter</router-link>
    </header>

    <div class="page-body">
      <div class="card auth-card">
        <h1 class="card-title">Créer un compte</h1>

        <div v-if="error" class="alert alert-error">{{ error }}</div>

        <form @submit.prevent="handleRegister" class="form-stack">
          <div class="field">
            <label>Email</label>
            <input v-model="email" type="email" placeholder="Saisissez votre email..."
              required autocomplete="email" />
          </div>
          <div class="field">
            <label>Mot de passe</label>
            <input v-model="password" type="password" placeholder="Saisissez votre mot de passe..."
              required autocomplete="new-password" />
          </div>
          <div class="field">
            <label>Vérification du mot de passe</label>
            <input v-model="password2" type="password" placeholder="Saisissez le à nouveau..."
              required autocomplete="new-password" />
          </div>
          <button type="button" class="btn-ghost-orange" @click="$router.push('/login')">
            J'ai déjà un compte
          </button>
          <button class="btn-orange-solid" :disabled="loading">
            {{ loading ? 'Création…' : 'Créer mon compte' }}
          </button>
        </form>
      </div>
    </div>

    <footer class="page-footer">Copyright DataShare© 2025</footer>
  </div>
</template>

<script setup>
/**
 * Page d'inscription — permet de créer un compte puis connecte automatiquement.
 *
 * La confirmation du mot de passe est vérifiée côté client avant l'appel API
 * pour éviter un aller-retour réseau inutile sur l'erreur la plus courante.
 * Les erreurs de validation Django (mot de passe trop faible, doublon) sont
 * récupérées depuis la réponse 400 et affichées directement à l'utilisateur.
 */
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const router = useRouter()

// Champs du formulaire
const email = ref('')
const password = ref('')
const password2 = ref('')

// État de chargement et message d'erreur
const loading = ref(false)
const error = ref('')

/**
 * Soumet le formulaire d'inscription.
 * Le nom d'utilisateur est dérivé de la partie locale de l'email
 * (avant le @) pour simplifier le formulaire côté utilisateur.
 * En cas de succès, l'utilisateur est automatiquement connecté.
 */
async function handleRegister() {
  error.value = ''

  // Vérification locale avant d'appeler l'API
  if (password.value !== password2.value) {
    error.value = 'Les mots de passe ne correspondent pas.'
    return
  }

  loading.value = true
  try {
    // On dérive le username de l'email pour simplifier le formulaire
    const username = email.value.split('@')[0]
    await auth.register(username, email.value, password.value, password2.value)
    router.push('/dashboard')
  } catch (e) {
    // On extrait le premier message d'erreur retourné par Django
    const data = e.response?.data
    error.value = data
      ? Object.values(data).flat()[0]
      : 'Erreur lors de la création du compte.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.gradient-page { min-height: 100vh; background: var(--gradient); display: flex; flex-direction: column; }
.guest-header { display: flex; align-items: center; justify-content: space-between; padding: 16px; height: 72px; flex-shrink: 0; }
.brand { font-family: 'DM Sans', sans-serif; font-size: 32px; font-weight: 700; color: #000; }
.page-body { flex: 1; display: flex; align-items: center; justify-content: center; padding: 24px 16px; }
.auth-card { width: 100%; max-width: 440px; }
.card-title { font-family: 'DM Sans', sans-serif; font-size: 28px; font-weight: 700; margin-bottom: 24px; text-align: center; }
.form-stack { display: flex; flex-direction: column; gap: 16px; }
.page-footer { padding: 16px 24px; font-family: 'Inter', sans-serif; font-size: 16px; color: #fff; flex-shrink: 0; }
</style>
