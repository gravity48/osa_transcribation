import {GetterTree, ActionTree, MutationTree} from 'vuex'
import {ConnectionSystem, ConnectionStatus} from "~/types/types";

class SelectClass{
  name: string
  code: number
  constructor(name: string, code: number) {
    this.name = name;
    this.code = code;
  }

}

export const state = () => ({
  conn_system: [] as Array<SelectClass>,
  conn_status: [] as Array<SelectClass>,
  fetch_data: false as boolean
})

export type RootState = ReturnType<typeof state>

export const getters: GetterTree<RootState, RootState> = {
  conn_system: state => state.conn_system,
  conn_status: state => state.conn_system,
}

export const mutations: MutationTree<RootState> = {
  setConnSystem(state: RootState, conn_systems: Array<ConnectionSystem>){
    state.conn_system = conn_systems.map(item => new SelectClass(item.name, item.id));
  },
  setConnStatus(state: RootState, conn_status: Array<ConnectionStatus>){
    state.conn_status = conn_status.map(item => new SelectClass(item.status_name, item.id));
  },
  setGetAllFetchData(state: RootState){
    state.fetch_data = true;
  }
}

export const actions: ActionTree<RootState, RootState> = {
  async fetch({state, commit}) {
    if (!state.fetch_data){
      let responses = await Promise.all([
        this.$axios.get('api/v1/connections/status/'),
        this.$axios.get('api/v1/connections/systems/'),
      ]);
      commit('setConnStatus', responses[0].data);
      commit('setConnSystem', responses[1].data);
    }
  },
}
