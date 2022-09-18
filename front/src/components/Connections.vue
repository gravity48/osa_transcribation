<template>
  <h1>Connections</h1>
  <div id="table-div">
    <table>
      <thead>
      <tr>
        <th class="counter">#</th>
        <th>Alias</th>
        <th>DB System</th>
        <th>IP</th>
        <th>DB Name</th>
        <th>Status</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="(connection, index) in connections_list" :key="connection.id">
        <td class="counter">{{ index + 1 }}</td>
        <td>{{ connection.alias }}</td>
        <td>{{ connection.db_system }}</td>
        <td>{{ connection.ip }}</td>
        <td>{{ connection.db_name }}</td>
        <td>{{ connection.db_status }}</td>
        <td></td>
        <div class="button_group">
          <button type="button" @click="refresh_connections">Refresh</button>
          <button type="button" @click="delete_connections(connection.id)">Del</button>
        </div>
      </tr>
      </tbody>
    </table>
  </div>
  <div class="modal-settings">
    <form>
      <input v-model="connection_form.alias" type="text" placeholder="Alias">
      <select v-model="connection_form.db_system">
        <option v-for="db_system in db_systems" :value="db_system.id" :key="db_system.id">{{ db_system.name }}
        </option>
      </select>
      <input v-model="connection_form.ip" type="text" placeholder="Ip">
      <input v-model="connection_form.port" type="text" placeholder="Port">
      <input v-model="connection_form.db_login" type="text" placeholder="Login">
      <input v-model="connection_form.db_password" type="text" placeholder="Password">
      <input v-model="connection_form.db_name" type="text" placeholder="DB Name">
      <button type="button" @click="set_connections">Commit</button>
    </form>
  </div>
</template>

<script>
import ViewService from "@/services/view-service";
import $ from 'jquery';
import event_list from "@/assets/js/comp";

export default {
  name: "ConnectionsView",
  data() {
    return {
      connection_form:{
        alias: '',
        db_system: '',
        ip: '',
        port: '',
        db_login: '',
        db_password: '',
        db_name: ''
      },
      'connections_list': '',
      'db_systems': '',
    }
  },
  mounted() {
    this.show_connections();
  },
  props:{
    show_modal: Boolean,
  },
  methods: {
    show_connections() {
      ViewService.get_connections().then(response => {
        this.connections_list = response.data;
      });
      ViewService.get_db_systems().then(response => {
        this.db_systems = response.data;
        this.connection_form.db_system = this.db_systems[0]['id'];
      });
    },
    set_connections() {
      ViewService.add_connections(this.connection_form).then(response => {
        this.show_connections();
      });
    },
    refresh_connections(e) {
      let data = {
        'event': 'refresh',
        'id': e.currentTarget.getAttribute('data-item'),
      }
      ViewService.refresh_connections(data).then();
    },
    delete_connections(id) {
      ViewService.delete_connections(id).then(response => {
        this.show_connections();
      });
    },
  }
}
</script>

<style scoped>
@import "../assets/css/main";

table {
  width: 100%;
}

table .counter {
  max-width: 10px;
  word-wrap: break-word;
}

form {
  display: flex;
  flex-wrap: wrap;
  justify-content: flex-start;
}

input, select, form > button {
  height: 26px;
  width: calc(50% - 12px);
}

input {
  display: block;
  margin: 5px;
  box-sizing: border-box;
}

input:focus {
  border: 3px solid #555;
}

select {
  margin: 5px;
}

form > button {
  margin: 5px;
}

form > button:hover {
  cursor: pointer;
}

#table-div {
  overflow: auto;
}




</style>