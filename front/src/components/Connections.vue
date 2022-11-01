<template>
  <h1>Подключения</h1>
  <div id="table-div">
    <ul>
      <li>
        <div class="connection-header">
          <p>#</p>
          <p>Название подключения</p>
          <p>СУБД</p>
          <p>IP адрес</p>
          <p>Название БД</p>
          <p>Статус</p>
          <div class="button_group">
            <button></button>
            <button @click="add_connections">
              <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                   class="bi bi-clipboard2-plus" viewBox="0 0 16 16">
                <path
                    d="M9.5 0a.5.5 0 0 1 .5.5.5.5 0 0 0 .5.5.5.5 0 0 1 .5.5V2a.5.5 0 0 1-.5.5h-5A.5.5 0 0 1 5 2v-.5a.5.5 0 0 1 .5-.5.5.5 0 0 0 .5-.5.5.5 0 0 1 .5-.5h3Z"/>
                <path
                    d="M3 2.5a.5.5 0 0 1 .5-.5H4a.5.5 0 0 0 0-1h-.5A1.5 1.5 0 0 0 2 2.5v12A1.5 1.5 0 0 0 3.5 16h9a1.5 1.5 0 0 0 1.5-1.5v-12A1.5 1.5 0 0 0 12.5 1H12a.5.5 0 0 0 0 1h.5a.5.5 0 0 1 .5.5v12a.5.5 0 0 1-.5.5h-9a.5.5 0 0 1-.5-.5v-12Z"/>
                <path
                    d="M8.5 6.5a.5.5 0 0 0-1 0V8H6a.5.5 0 0 0 0 1h1.5v1.5a.5.5 0 0 0 1 0V9H10a.5.5 0 0 0 0-1H8.5V6.5Z"/>
              </svg>
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
          <button class="transform-rotate transform-rotate-45" @click="refresh_connections(connection.id)">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                 class="bi bi-arrow-repeat" viewBox="0 0 16 16">
              <path
                  d="M11.534 7h3.932a.25.25 0 0 1 .192.41l-1.966 2.36a.25.25 0 0 1-.384 0l-1.966-2.36a.25.25 0 0 1 .192-.41zm-11 2h3.932a.25.25 0 0 0 .192-.41L2.692 6.23a.25.25 0 0 0-.384 0L.342 8.59A.25.25 0 0 0 .534 9z"/>
              <path fill-rule="evenodd"
                    d="M8 3c-1.552 0-2.94.707-3.857 1.818a.5.5 0 1 1-.771-.636A6.002 6.002 0 0 1 13.917 7H12.9A5.002 5.002 0 0 0 8 3zM3.1 9a5.002 5.002 0 0 0 8.757 2.182.5.5 0 1 1 .771.636A6.002 6.002 0 0 1 2.083 9H3.1z"/>
            </svg>
          </button>
          <button class="transform-rotate transform-rotate-45" @click="show_connection_settings(connection.id)">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-gear"
                 viewBox="0 0 16 16">
              <path
                  d="M8 4.754a3.246 3.246 0 1 0 0 6.492 3.246 3.246 0 0 0 0-6.492zM5.754 8a2.246 2.246 0 1 1 4.492 0 2.246 2.246 0 0 1-4.492 0z"/>
              <path
                  d="M9.796 1.343c-.527-1.79-3.065-1.79-3.592 0l-.094.319a.873.873 0 0 1-1.255.52l-.292-.16c-1.64-.892-3.433.902-2.54 2.541l.159.292a.873.873 0 0 1-.52 1.255l-.319.094c-1.79.527-1.79 3.065 0 3.592l.319.094a.873.873 0 0 1 .52 1.255l-.16.292c-.892 1.64.901 3.434 2.541 2.54l.292-.159a.873.873 0 0 1 1.255.52l.094.319c.527 1.79 3.065 1.79 3.592 0l.094-.319a.873.873 0 0 1 1.255-.52l.292.16c1.64.893 3.434-.902 2.54-2.541l-.159-.292a.873.873 0 0 1 .52-1.255l.319-.094c1.79-.527 1.79-3.065 0-3.592l-.319-.094a.873.873 0 0 1-.52-1.255l.16-.292c.893-1.64-.902-3.433-2.541-2.54l-.292.159a.873.873 0 0 1-1.255-.52l-.094-.319zm-2.633.283c.246-.835 1.428-.835 1.674 0l.094.319a1.873 1.873 0 0 0 2.693 1.115l.291-.16c.764-.415 1.6.42 1.184 1.185l-.159.292a1.873 1.873 0 0 0 1.116 2.692l.318.094c.835.246.835 1.428 0 1.674l-.319.094a1.873 1.873 0 0 0-1.115 2.693l.16.291c.415.764-.42 1.6-1.185 1.184l-.291-.159a1.873 1.873 0 0 0-2.693 1.116l-.094.318c-.246.835-1.428.835-1.674 0l-.094-.319a1.873 1.873 0 0 0-2.692-1.115l-.292.16c-.764.415-1.6-.42-1.184-1.185l.159-.291A1.873 1.873 0 0 0 1.945 8.93l-.319-.094c-.835-.246-.835-1.428 0-1.674l.319-.094A1.873 1.873 0 0 0 3.06 4.377l-.16-.292c-.415-.764.42-1.6 1.185-1.184l.292.159a1.873 1.873 0 0 0 2.692-1.115l.094-.319z"/>
            </svg>
          </button>
          <button @click="delete_connections(connection.id)">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x-lg"
                 viewBox="0 0 16 16">
              <path
                  d="M2.146 2.854a.5.5 0 1 1 .708-.708L8 7.293l5.146-5.147a.5.5 0 0 1 .708.708L8.707 8l5.147 5.146a.5.5 0 0 1-.708.708L8 8.707l-5.146 5.147a.5.5 0 0 1-.708-.708L7.293 8 2.146 2.854Z"/>
            </svg>
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
          <label for="db_login"><span class="input-header">Логин</span><br><span
              class="input-detail">Логин базы данных</span></label>
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
        <div class="form-option">
          <label for="db_name"><span class="input-header">Неотбор</span> <br><span class="input-detail">Фильтрация по записям мз неотбора (имя собеседника/имя источника не пусто)</span></label>
          <div class="checkbox-with-label">
            <input class="checkbox-with-label" v-model="connection_form.options.selection" type="checkbox"><span
               v-if="connection_form.options.selection">Только неотбор</span><span
               v-else>Все записи</span>
          </div>
        </div>
      </div>
    </div>
    <div id="modal-close">
      <button class="modal-close-btn" @click="show_modal = false; this.get_connections();">
        <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-x"
             viewBox="0 0 16 16">
          <path
              d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"/>
        </svg>
      </button>
    </div>
  </div>

</template>

<script>
import ViewService from "@/services/view-service";
import vSelect from "vue-select";


export default {
  name: "ConnectionsView",
  components: {
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
      field_transaction: {
        'ip': 'IP адрес сервера',
        'alias': 'Название подключения',
        'db_system': 'СУБД',
        'port': 'Порт',
        'db_login': 'Логин БД',
        'db_password': 'Пароль БД',
        'db_name': 'База данных',
        'transcribing_server': 'Сервер транскирибации',
      }
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
      for (const [item, connection] of Object.entries(this.connections_list)) {
        if (connection.id === id) {
          this.connection_form = this.connections_list[item]
          break;
        }
      }
      //this.connection_form = this.connections_list.filter((cnnct) => cnnct.id === id)[0];
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
    refresh_connections(id) {
      ViewService.refresh_connections(id).then(response => {
        this.get_connections();
        this.$notify({
          type: 'success',
          title: this.connections_list.filter((cnnct) => cnnct.id === id)[0].alias,
          text: 'Соединение установлено',
          duration: 5000,
        });
      }).catch(error => {
        this.get_connections();
        for (const [key, value] of Object.entries(error.response.data)) {
          this.$notify({
            type: 'error',
            duration: 5000,
            title: this.field_transaction[key],
            text: value,
          })
        }
      });
    },
    delete_connections(id) {
      ViewService.delete_connections(id).then(response => {
        this.get_connections();
      });
    },
    filter_name(value) {
      if (value) {
        return value.name;
      }
      return null;
    },
  },
  watch: {
    connection_form: {
      async handler(newValue, oldValue) {
        await ViewService.update_connections(newValue.id, newValue).then(response => {
        }).catch(error => {
          for (const [key, value] of Object.entries(error.response.data.errors)) {
            this.$notify({
              type: 'error',
              title: this.field_transaction[key],
              text: value,
              duration: 5000,
            });
          }
          this.connection_form = error.response.data.data;
        })
      },
      deep: true
    }
  }
}
</script>

<style scoped>
@import "../assets/css/main";
@import "bootstrap-icons/font/bootstrap-icons.css";

.checkbox-with-label {
  display: flex;
}

.checkbox-with-label > input {
  height: 17px;
  width: 17px;
}
.checkbox-with-label > span{
  display: block;
  margin: 3px 4px;
}

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


#table-div ul li:not(:first-child) {
  border: black 1px solid;
  margin: 5px 0;
  border-radius: 4px;
}

#table-div ul li:not(:first-child):hover {
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

.button_group button:last-child {
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