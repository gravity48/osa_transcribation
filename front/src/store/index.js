import { createStore } from 'vuex'

export default createStore({
    state: {
        user: {
            refresh: null,
            access: null,
        },
        isAuthenticate: null,
        activeTab: null,
    },
    mutations: {
        setAuthenticate(state, AuthBoolean){
            state.isAuthenticate = AuthBoolean
        },
        setActiveTab(state, RouterPath){
            state.activeTab = RouterPath;
        },
    },
    actions: {},
    getters: {},
})