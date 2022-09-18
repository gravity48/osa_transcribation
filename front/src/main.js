import {createApp} from 'vue'
import App from './App.vue'
import routers from './router.js'
import store from './store'

import Datepicker from '@vuepic/vue-datepicker';
import '@vuepic/vue-datepicker/dist/main.css';

import moment from 'moment';

let app =createApp(App);

// eslint-disable-next-line vue/multi-word-component-names
app.component('Datepicker', Datepicker);
app.use(store).use(routers);
app.mount('#app');
