//import './assets/main.css'
import PortalVue from 'portal-vue'
import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createBootstrap } from 'bootstrap-vue-next'
import Vue3EasyDataTable from 'vue3-easy-data-table'
// Import Bootstrap and BootstrapVue CSS files (order is important)
import 'bootstrap/dist/css/bootstrap.css'
import 'bootstrap-icons/font/bootstrap-icons.css'
import 'bootstrap-vue-next/dist/bootstrap-vue-next.css'
import 'vue3-easy-data-table/dist/style.css';

import App from './App.vue'
import router from './router'

const app = createApp(App)
// Make BootstrapVue available throughout your project
app.use(createBootstrap()) // Important
app.use(PortalVue)
app.component('EasyDataTable', Vue3EasyDataTable);
app.use(createPinia())
app.use(router)

app.mount('#app')
