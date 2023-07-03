import { GetterTree, ActionTree, MutationTree } from 'vuex'
import {Connections} from "~/types/types";


export const state = () => ({
  con_list: [] as Array<Connections>,
  con_detail: {} as Connections | Object
})

export type RootState = ReturnType<typeof state>

export const mutations: MutationTree<RootState> = {
  setConnections(state: RootState, connections: Array<Connections>){
    state.con_list = connections;
  },
  addConnection(state: RootState, connection: Connections){
    state.con_list.push(connection);
  },
  removeConnection(state: RootState, id: number){
    const index = state.con_list.findIndex(item => item.id === id);
    state.con_list.splice(index, 1);
  },
  setDetailConnection(state: RootState, connection: Connections){
    state.con_detail = connection;
  }
}

export const actions: ActionTree<RootState, RootState> = {
  async fetchConnections({commit, state}){
    if (state.con_list.length === 0) {
      const {data} = await this.$axios.get('api/v1/connections/connections/')
      commit('setConnections', data);
    }
  },
  async addConnections({commit}){
    const {data} = await this.$axios.post('api/v1/connections/connections/')
    commit('addConnection', data);
  },
  async removeConnection({commit, state}, id: number){
    if (state.con_list.length !== 0 &&  state.con_list.find(con => con.id === id)) {
      await this.$axios.delete('api/v1/connections/connections/' + id);
      commit('removeConnection', id);
    }
  },
  async retrieveConnection({commit, state}, id:number){
      const {data} = await this.$axios.get(`api/v1/connections/connections/${id}/`)
      commit('setDetailConnection', data);
    }
}

export const getters: GetterTree<RootState, RootState> = {
  connections: s => s.con_list,
  con_detail: s => s.con_detail,
}
