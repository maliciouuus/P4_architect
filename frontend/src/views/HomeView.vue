<template>
  <div class="gradient-page">
    <header class="guest-header">
      <span class="brand">DataShare</span>
      <router-link to="/login" class="btn-dark">Se connecter</router-link>
    </header>

    <div class="hero">
      <p class="tagline">Tu veux partager un fichier ?</p>
      <button class="icon-btn" @click="$router.push('/login')">
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

    <footer class="page-footer">Copyright DataShare© 2025</footer>
  </div>
</template>

<!--
  Page d'accueil — visible uniquement par les utilisateurs non connectés.

  Affiche le gradient de marque avec la tagline et l'icône d'upload cliquable.
  Cliquer sur l'icône ou le bouton "Se connecter" redirige vers /login.
  Cette page sert de vitrine avant toute interaction avec l'application.
-->
<script setup>
// Pas de logique JS nécessaire ici — la navigation est gérée directement
// via les directives @click="$router.push('/login')" dans le template.
</script>

<style scoped>
.gradient-page { min-height: 100vh; background: var(--gradient); display: flex; flex-direction: column; }
.guest-header { display: flex; align-items: center; justify-content: space-between; padding: 16px; height: 72px; flex-shrink: 0; }
.brand { font-family: 'DM Sans', sans-serif; font-size: 32px; font-weight: 700; color: #000; }
.hero { flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 24px; padding: 24px; }
.tagline { font-family: 'DM Sans', sans-serif; font-size: 30px; font-weight: 300; color: #000; text-align: center; max-width: 320px; }
.icon-btn { background: none; border: none; cursor: pointer; padding: 0; }
.icon-ring-outer { width: 144px; height: 144px; background: rgba(46,24,13,.15); border-radius: 50%; display: flex; align-items: center; justify-content: center; }
.icon-ring-inner { width: 96px; height: 96px; background: #0F0118; border-radius: 50%; display: flex; align-items: center; justify-content: center; }
.page-footer { padding: 16px 24px; font-family: 'Inter', sans-serif; font-size: 16px; color: #fff; flex-shrink: 0; }
</style>
