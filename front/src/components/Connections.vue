<template>
  <h1>Connections</h1>
  <div id="table-div">
    <ul>
      <li>
        <div class="connection-header">
          <p>#</p>
          <p>Alias</p>
          <p>DB System</p>
          <p>IP</p>
          <p>DB Name</p>
          <p>Status</p>
          <div class="button_group">
            <button></button>
            <button @click="add_connections">
              <BootstrapIcon icon="clipboard2-plus"
                             size="2x"/>
            </button>
            <button></button>
          </div>
        </div>
      </li>
      <li v-for="(connection, index) in connections_list" :key="connection.id">
        <p>{{ index + 1 }}</p>
        <p>{{ connection.alias }}</p>
        <p>{{ filter_name(connection.db_system) }}</p>
        <p>{{ connection.ip }}</p>
        <p>{{ connection.db_name }}</p>
        <p>{{ connection.db_status }}</p>
        <div id='repeat-ico' class="button_group">
          <button class="transform-rotate transform-rotate-45">
            <BootstrapIcon icon="arrow-repeat" size="2x"/>
          </button>
          <button class="transform-rotate transform-rotate-45" @click="show_connection_settings(connection.id)">
            <BootstrapIcon icon="gear" size="2x"/>
          </button>
          <button @click="delete_connections(connection.id)">
            <BootstrapIcon icon="x-lg" size="2x"/>
          </button>
        </div>
      </li>
    </ul>
  </div>
  <div class="modal-settings" :class="{modal_settings_show: show_modal === true}">
    <div class="column">
      <div class="col-content">
        <div class="form-option">
          <label for="alias"><span class="input-header">Название подключения</span> <br> <span class="input-detail">Подключение будет отбражаться в общем списке</span></label>
          <input v-model="connection_form.alias" type="text" placeholder="Alias">
        </div>
        <div class="form-option">
          <label for="db_systems"><span class="input-header">СУБД</span><br> <span class="input-detail">Выберите целевую СУБД</span></label>
          <v-select v-model="connection_form.db_system" label="name" :options="db_systems"></v-select>
        </div>
        <div class="form-option">
          <label for="ip"><span class="input-header">IP</span> <br> <span class="input-detail">Введите IP адрес сервера БД</span>
          </label>
          <input v-model="connection_form.ip" type="text">
        </div>
        <div class="form-option">
          <label for="port"><span class="input-header">Порт</span><br> <span class="input-detail">Введите порт сервера БД</span></label>
          <input v-model="connection_form.port" type="text">
        </div>
      </div>
    </div>
    <div class="column">
      <div class="col-content">
        <div class="form-option">
          <label for="db_login"><span class="input-header">Логин</span><br><span class="input-detail">Логин базы данных</span></label>
          <input v-model="connection_form.db_login" type="text">
        </div>
        <div class="form-option">
          <label for="db_password"><span class="input-header">Пароль</span><br><span class="input-detail">Пароль базы данных</span></label>
          <input v-model="connection_form.db_password" type="password">
        </div>
        <div class="form-option">
          <label for="db_name"><span class="input-header">База данных</span> <br><span class="input-detail">Имя (путь) к базе данных (схеме)</span></label>
          <input v-model="connection_form.db_name" type="text">
        </div>
        <div class="form-option">
          <label for="db_name"><span class="input-header">Пост</span> <br><span class="input-detail">Фильтрация по полю пост в базе данных спрут</span></label>
          <input v-model="connection_form.options.post" type="text">
        </div>
      </div>
    </div>
    <div id="modal-close">
      <button class="modal-close-btn" @click="show_modal = false">
        <BootstrapIcon icon="x" size="2x"></BootstrapIcon>
      </button>
    </div>
  </div>
</template>

<script>
import ViewService from "@/services/view-service";
import BootstrapIcon from '@dvuckovic/vue3-bootstrap-icons';
import axios from "axios";
import vSelect from "vue-select";
import $ from 'jquery';


export default {
  name: "ConnectionsView",
  components: {
    BootstrapIcon,
    vSelect,
  },
  data() {
    return {
      connection_form: {
        options: {},
      },
      show_modal: false,
      connections_list: [],
      db_systems: [],
    }
  },
  mounted() {
    this.get_connections();
    this.get_db_systems();
  },
  methods: {
    get_db_systems() {
      ViewService.get_db_systems().then(response => {
        this.db_systems = response.data;
      }).catch(error => {
        console.log(error);
      });
    },
    show_connection_settings(id) {
      this.connection_form = this.connections_list.filter((cnnct) => cnnct.id === id)[0];
      this.show_modal = true;
    },
    get_connections() {
      ViewService.get_connections().then(response => {
        this.connections_list = response.data;
      });
    },
    add_connections() {
      ViewService.add_connections().then(response => {
        this.get_connections();
      });
    },
    refresh_connections(e) {
      let data = {
        'event': 'refresh',
        'id': e.currentTarget.getAttribute('data-item'),
      }
      ViewService.refresh_connections(data).then(response => {
        console.log(response.data);
      });
    },
    delete_connections(id) {
      ViewService.delete_connections(id).then(response => {
        this.get_connections();
      });
    },
    filter_name(value){
      if(value){
        return value.name;
      }
      return null;
    }
  },
  watch: {
    connection_form:{
      handler(newValue, oldValue){
        ViewService.update_connections(newValue.id, newValue).then(response => {
          console.log(response);
        }).catch(error => {
          console.log(error);
        })
      },
      deep: true
    }
  }
}
</script>

<style scoped>
@import "../assets/css/main";

#table-div ul {
  list-style-type: none;
  padding: 0;
  margin-top: 10px;
  margin-bottom: 0;
}

#table-div ul li {
  display: flex;
  width: 100%;
}


#table-div ul li:not(:first-child){
  border: black 1px solid;
  margin: 5px 0;
  border-radius: 4px;
}

#table-div ul li:not(:first-child):hover{
  cursor: pointer;
  background: rgba(85, 85, 85, 0.2);
}

#table-div ul li p:first-child {
  width: 5%;
}

#table-div ul li p {
  width: 20%;
}

#table-div ul li .button_group {
  flex-basis: 10%;
}

.button_group {
  display: flex;
  justify-content: center;
  align-items: center;
}

.button_group button:last-child{
  color: red;
}
#table-div ul li .button_group button {
  background-color: transparent;
  border: none;
  padding: 0;
  width: 30px;
  margin: 0 3px;
  height: 30px;
  cursor: pointer;
}

#table-div ul li .button_group button svg {
  width: 100%;
  height: 100%;
  margin-bottom: 0;
}

.transform-rotate svg {
  transform: rotate(0deg);
  transition: transform .2s ease-out;
  transform-origin: center;
}

button.transform-rotate:hover.transform-rotate-45 svg {
  transform: rotate(45deg);
}

.connection-header {
  display: flex;
  width: 100%;
}

.connection-header p {
  width: 20%;
}

.connection-header p:first-child {
  width: 5%;
}


</style>