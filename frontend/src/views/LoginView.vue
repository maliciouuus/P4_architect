<template>
  <div class="gradient-page">
    <header class="guest-header">
      <span class="brand">DataShare</span>
      <router-link to="/login" class="btn-dark">Se connecter</router-link>
    </header>

    <div class="page-body">
      <div class="card auth-card">
        <h1 class="card-title">Connexion</h1>

        <div v-if="error" class="alert alert-error">{{ error }}</div>

        <form @submit.prevent="handleLogin" class="form-stack">
          <div class="field">
            <label>Email</label>
            <input v-model="username" type="text" placeholder="Saisissez votre email..."
              required autocomplete="username" />
          </div>
          <div class="field">
            <label>Mot de passe</label>
            <input v-model="password" type="password" placeholder="Saisissez votre mot de passe..."
              required autocomplete="current-password" />
          </div>
          <button type="button" class="btn-ghost-orange" @click="$router.push('/register')">
            Créer un compte
          </button>
          <button class="btn-orange-solid" :disabled="loading">
            {{ loading ? 'Connexion…' : 'Connexion' }}
          </button>
        </form>
      </div>
    </div>

    <footer class="page-footer">Copyright DataShare© 2025</footer>
  </div>
</template>

<script setup>
/**
 * Page de connexion — affiche un formulaire email/mot de passe sur fond gradient.
 *
 * En cas d'erreur (identifiants incorrects), un message est affiché
 * sous le formulaire sans recharger la page.
 */
import { ref } from 'vue'
import { useRouter } from 'vue-router'

import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const router = useRouter()

// Champs du formulaire liés au template via v-model
const username = ref('')
const password = ref('')

// Contrôle l'état du bouton et le texte "Connexion…" pendant l'appel API
const loading = ref(false)

// Message d'erreur affiché si la connexion échoue
const error = ref('')

/**
 * Soumet le formulaire de connexion.
 * En cas de succès, redirige vers le dashboard.
 * En cas d'échec (401), affiche un message générique sans préciser
 * si c'est l'identifiant ou le mot de passe qui est erroné (sécurité).
 */
async function handleLogin() {
  error.value = ''
  loading.value = true
  try {
    await auth.login(username.value, password.value)
    router.push('/dashboard')
  } catch {
    error.value = 'Identifiants incorrects.'
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
