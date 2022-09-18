import {createRouter, createWebHistory} from 'vue-router'
import Login from './components/Login.vue'
import Home from './components/Home.vue'
import Connections from "@/components/Connections";
import Tasks from "@/components/Tasks";
import App from './App.vue'

const routes = [
    {path: '/login', name: 'login', component: Login},
    {
        path: '/home',
        name: 'Home',
        component: Home,
        children: [{path: 'connections', name: 'Connections', component: Connections},
            {path: 'task',name: 'Tasks',component: Tasks}]
    },
    {path: '/', name: 'App', component: App},

]

const router = createRouter({
    history: createWebHistory(),
    routes,
})

export default router