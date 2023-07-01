import { GetterTree, ActionTree, MutationTree } from 'vuex'
import {Connections} from "~/types/types";


export const state = () => ({
  con_list: [] as Array<Connections>
})

export type RootState = ReturnType<typeof state>

export const mutations: MutationTree<RootState> = {
  setConnections(state: RootState, connections: Array<Connections>){
    state.con_list = connections;
  },
  addConnection(state: RootState, connection: Connections){
    state.con_list.push(connection);
  }
}

export const actions: ActionTree<RootState, RootState> = {
  async fetchConnections({commit, state}){
    if (state.con_list.length === 0) {
      const {data} = await this.$axios.get('api/v1/connections/connections/')
      commit('setConnections', data);
    }
  },
  async addConnections({commit, state}){
    const {data} = await this.$axios.post('api/v1/connections/connections/')
    commit('addConnection', data);
  }
}

export const getters: GetterTree<RootState, RootState> = {
  connections: s => s.con_list
}
