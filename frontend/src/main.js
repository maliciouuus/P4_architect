/**
 * Point d'entrée de l'application Vue.js.
 *
 * Instancie l'application, enregistre les plugins (Pinia pour le state
 * management, Vue Router pour la navigation) et monte l'app dans le DOM.
 */

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

const app = createApp(App)

// Pinia — gestionnaire d'état global (stores auth et files)
app.use(createPinia())

// Vue Router — gestion des routes et gardes de navigation
app.use(router)

// Montage dans le div#app de index.html
app.mount('#app')
