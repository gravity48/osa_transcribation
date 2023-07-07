import {GetterTree, ActionTree, MutationTree} from 'vuex'
import {ConnectionSystem, ConnectionStatus, TaskStatus, RecognizeServer} from "~/types/types";

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
  task_status: [] as Array<TaskStatus>,
  recognize_servers: [] as Array<RecognizeServer>
})

export type RootState = ReturnType<typeof state>

export const getters: GetterTree<RootState, RootState> = {
  conn_system: state => state.conn_system,
  conn_status: state => state.conn_system,
  task_status: state => state.task_status,
  recognize_servers: state => state.recognize_servers,

}

export const mutations: MutationTree<RootState> = {
  setConnSystem(state: RootState, conn_systems: Array<ConnectionSystem>){
    state.conn_system = conn_systems.map(item => new SelectClass(item.name, item.id));
  },
  setConnStatus(state: RootState, conn_status: Array<ConnectionStatus>){
    state.conn_status = conn_status.map(item => new SelectClass(item.status_name, item.id));
  },
  setTaskStatus(state: RootState, tasks_status: Array<TaskStatus>){
    state.task_status = tasks_status;
  },
  setRecognizeServer(state: RootState, recognize_server: Array<RecognizeServer>){
    state.recognize_servers = recognize_server;
  },

}

export const actions: ActionTree<RootState, RootState> = {
  async nuxtServerInit({commit}){
    let responses = await Promise.all([
      this.$axios.get('api/v1/connections/status/'),
      this.$axios.get('api/v1/connections/systems/'),
      this.$axios.get('api/v1/tasks/status/'),
      this.$axios.get('api/v1/tasks/servers/')
    ]);
    commit('setConnStatus', responses[0].data);
    commit('setConnSystem', responses[1].data);
    commit('setTaskStatus', responses[2].data);
    commit('setRecognizeServer', responses[3].data);
  },
}
