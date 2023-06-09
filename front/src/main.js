import {createSSRApp} from 'vue'
import App from './App.vue'
import routers from './router.js'
import store from './store'

import Datepicker from '@vuepic/vue-datepicker';
import Notifications from '@kyvg/vue3-notification'
import '@vuepic/vue-datepicker/dist/main.css';

let app =createSSRApp(App);

// eslint-disable-next-line vue/multi-word-component-names
app.component('Datepicker', Datepicker);

app.use(Notifications);
app.use(store).use(routers);
app.mount('#app');
