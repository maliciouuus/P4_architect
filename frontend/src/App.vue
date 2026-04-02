<!--
  Composant racine de l'application Vue.js.

  Ce composant est le point d'entrée du rendu — il est monté dans le div#app
  de index.html. Il contient uniquement le <router-view> qui affiche la page
  correspondant à la route active, et les styles CSS globaux utilisés
  par toutes les pages (variables de design, boutons, champs, alertes).

  La navbar et la sidebar ne sont pas ici : chaque vue gère son propre header
  pour s'adapter à son contexte (guest vs authentifié, mobile vs desktop).
-->
<template>
  <div id="app">
    <!-- La vue active (Home, Login, Register, Dashboard, Download) est rendue ici -->
    <router-view />
  </div>
</template>

<!--
  Styles globaux — disponibles dans tous les composants enfants.
  On utilise des variables CSS (:root) pour centraliser les tokens de design
  extraits du Figma : gradient, couleurs, rayons, typographie.
-->
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Inter:wght@400;600&display=swap');

*, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

:root {
  /* Gradient */
  --gradient: linear-gradient(180deg, #FFB88C 0%, #DE6262 100%);

  /* Colors */
  --dark: #2C2C2C;
  --cream: #F3EEEA;
  --white: #FFFFFF;
  --text: #1E1E1E;
  --text-secondary: #757575;
  --text-placeholder: #B3B3B3;

  /* Orange palette */
  --orange: #FF812D;
  --orange-outline-stroke: #FFA569;
  --orange-outline-text: #E17F29;
  --orange-link-text: #D7630A;
  --orange-link-stroke: #D7630B;

  /* Panel (Mon espace) */
  --panel-bg: #FFF7F3;
  --panel-bar: #FFEDE2;
  --panel-bar-stroke: #D8601B;

  /* Tabs */
  --tab-bg: rgba(255, 192, 145, 0.16);
  --tab-active: #E77A6E;
  --tab-stroke: #D7630B;

  /* File rows */
  --file-row-bg: rgba(255, 192, 145, 0.05);
  --file-row-stroke: #D7630B;

  /* Sidebar */
  --sidebar-item-active-bg: rgba(255,255,255,0.4);
  --sidebar-item-active-text: #803900;

  /* Misc */
  --radius-card: 16px;
  --radius-btn: 8px;
  --radius-input: 8px;
  --radius-tab: 24px;
}

body {
  font-family: 'DM Sans', sans-serif;
  color: var(--text);
  min-height: 100vh;
}

/* ─── Buttons ─────────────────────────────────────── */
.btn-dark {
  background: var(--dark);
  color: var(--cream);
  border: none;
  border-radius: var(--radius-btn);
  padding: 8px 12px;
  font-family: 'DM Sans', sans-serif;
  font-size: 16px;
  font-weight: 400;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: background .15s;
}
.btn-dark:hover { background: #3a3a3a; }

.btn-orange-solid {
  background: var(--orange);
  color: #fff;
  border: none;
  border-radius: var(--radius-btn);
  padding: 12px;
  font-family: 'DM Sans', sans-serif;
  font-size: 16px;
  cursor: pointer;
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  transition: background .15s;
}
.btn-orange-solid:hover { background: #e6721e; }
.btn-orange-solid:disabled {
  background: transparent;
  border: 1px solid #B6A69C;
  color: #AEA49A;
  cursor: not-allowed;
}

.btn-orange-outline {
  background: transparent;
  color: var(--orange-outline-text);
  border: 1px solid var(--orange-outline-stroke);
  border-radius: var(--radius-btn);
  padding: 8px 12px;
  font-family: 'DM Sans', sans-serif;
  font-size: 16px;
  cursor: pointer;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  transition: background .15s;
  white-space: nowrap;
}
.btn-orange-outline:hover { background: rgba(255,129,45,.08); }

.btn-ghost-orange {
  background: transparent;
  color: var(--orange-outline-text);
  border: none;
  font-family: 'DM Sans', sans-serif;
  font-size: 16px;
  cursor: pointer;
  text-align: center;
  width: 100%;
  padding: 12px;
}

/* ─── Card ────────────────────────────────────────── */
.card {
  background: var(--white);
  border-radius: var(--radius-card);
  padding: 24px;
}

/* ─── Form fields ─────────────────────────────────── */
.field { display: flex; flex-direction: column; gap: 8px; }
.field label {
  font-family: 'Inter', sans-serif;
  font-size: 16px;
  color: var(--text);
}
.field input, .field select {
  background: var(--white);
  border: 1px solid #D9D9D9;
  border-radius: var(--radius-input);
  padding: 12px 16px;
  font-family: 'DM Sans', sans-serif;
  font-size: 16px;
  color: var(--text);
  outline: none;
  width: 100%;
  transition: border-color .15s;
}
.field input::placeholder { color: var(--text-placeholder); }
.field input:focus, .field select:focus { border-color: var(--orange); }

/* ─── Alerts ──────────────────────────────────────── */
.alert {
  padding: 10px 14px;
  border-radius: 8px;
  font-size: 14px;
  font-family: 'Inter', sans-serif;
}
.alert-error { background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; }
.alert-success { background: #f0fdf4; color: #15803d; border: 1px solid #bbf7d0; }
</style>
