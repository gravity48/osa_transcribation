<template>
  <h1>TaskView</h1>
  <div class="task-table">
    <ul>
      <li>
        <div class="task-header"><p>#</p>
          <p>Alias</p>
          <p>Alias DB</p>
          <p>Task Type</p>
          <p>Model</p>
          <p>Process Count</p>
          <button type="button" class="add-task-button" @click="add_task">
            <BootstrapIcon
                icon="clipboard2-plus"
                size="2x"/>
          </button>
        </div>
      </li>
      <li v-for="(task, index) in tasks" :key="task.id">
        <div class="progress-bar"></div>
        <div class="task-header">
          <p>{{ index + 1 }}</p>
          <p>{{ task.alias }}</p>
          <p>{{ filter_alias(task.db) }}</p>
          <p>{{ filter_name(task.task_type) }}</p>
          <p>{{filter_name(task.model)}}</p>
          <p>{{ task.thread_count }}</p>
          <button type="button" class="task-settings-detail" @click="show_task_settings(task.id)">
            <BootstrapIcon
                icon="gear"
                size="2x"/>
          </button>
          <button type="button" class="show-task-detail">
            <div></div>
            <div></div>
          </button>
          <button type="button" class="delete-task-btn" :data-item="task.id" @click="del_task(task.id)">
            <div>
              <div></div>
            </div>
          </button>
        </div>
        <div class="task-detail-panel">
          <h3>Task {{ task.alias }}</h3>
          <div class="task-detail--properties">
            <p><span>From: </span>{{ filtered_date(task.period_from) }}</p>
            <p><span>To: </span> {{ filtered_date(task.period_to) }}</p>
          </div>
        </div>
      </li>
    </ul>
  </div>
  <div class="modal-settings" :class="{modal_settings_show: show_modal === true}">
    <div class="column">
      <div class="col-content">
        <div class="form-option">
          <label for="alias"><span class="input-header">Название обработчика</span> <br> <span class="input-detail">Название будет отбражаться в общем списке</span></label>
          <input type="text" id="alias" v-model="task_settings.alias" placeholder="Alias">
        </div>
        <div class="form-option">
          <label for="period-to"><span class="input-header">Фильтр по дате</span><br> <span class="input-detail">Период, за который необходимо произвести пердварительную обработку записей</span>
          </label>
          <div class="date-time-string"><span>С</span>
            <Datepicker id="period-to" format="dd/MM/yyyy" v-model="task_settings.period_from" :maxDate="task_settings.period_to" locale="ru"/>
            <span>по</span>
            <Datepicker id="period-from"  format="dd/MM/yyyy" v-model="task_settings.period_to" :minDate="task_settings.period_from" locale="ru"/>
          </div>
        </div>
        <div class="form-option">
          <label for="db_alias"><span class="input-header">База данных</span> <br> <span class="input-detail"> Выберите из списка базу данных для обработки</span></label>
          <v-select v-model="task_settings.db" label="alias" :options="input_form.connections"></v-select>
        </div>
        <div class="form-option">
          <label for="task-type"> <span class="input-header">Задача обработчика</span> <br> <span class="input-detail"> Выберите из списка цель для обработки данных </span></label>
          <v-select label="name" v-model="task_settings.task_type" :options="input_form.tasks_type"></v-select>
        </div>
      </div>
    </div>
    <div class="column">
      <div class="col-content">
        <div class="form-option">
          <label for="model-id"><span class="input-header">Лингафонная модель </span> <br> <span class="input-detail">Выберите из списка модель обработки голоса в зависимости от языка </span>
          </label>
          <v-select v-model="task_settings.model" label="name" :options="input_form.models"></v-select>
        </div>
        <div class="advanced-settings">
          <p class="advanced-settings-header">Расширенная настройка</p>
          <div class="form-option">
            <label for="time-process"><span class="input-header">Количество процессов</span> <br> <span
                class="input-detail">Паралельная обработка ускоряет процесс транскрибации, но <br> большое количество фоновых процессов может повлиять на <br> производительность</span></label>
            <input id="process-count" type="number" v-model="task_settings.thread_count" placeholder="Process count">
          </div>
          <div class="form-option">
            <label for="process-count"><span class="input-header">Таймаут процесса</span><br><span class="input-detail">Время в секундах, перед автоматическим завершением процесса</span>
            </label>
            <input id='time-process' type="number" v-model="task_settings.time_processing" placeholder="Time process">
          </div>
          <div class="form-option">
            <label for="process-count"><span class="input-header">Время активной речи</span><br><span
                class="input-detail">Продолжительность времени в секундах, при которой сеанс может <br> нести информативную нагрузку</span>
            </label>
            <input id='time-process' type="number" v-model="task_settings.options.speech_time" placeholder="Time process">
          </div>
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
import moment from 'moment';
import $ from 'jquery';
import TaskService from "@/services/task-service";
import ViewService from "@/services/view-service";
import axios from "axios";
import BootstrapIcon from '@dvuckovic/vue3-bootstrap-icons';
import vSelect from "vue-select";
import 'vue-select/dist/vue-select.css';

export default {
  name: "TasksView",
  components: {
    BootstrapIcon,
    vSelect,
  },
  props: {},
  data() {
    return {
      loader: null,
      show_modal: false,
      tasks: [],
      task_settings: {
        options:{

        }
      },
      input_form: {
        models: [],
        tasks_type: [],
        connections: [],
      }
    }
  },
  mounted() {
    this.show_tasks();
    this.init_input_form();
  },
  methods: {
    init_input_form() {
      axios.all([TaskService.get_models_list(), TaskService.get_tasks_type(), TaskService.get_connections_list()]).then(axios.spread((...responses) => {
        this.input_form.models = responses[0].data;
        this.input_form.tasks_type = responses[1].data;
        this.input_form.connections = responses[2].data;
      })).catch(errors => {
        console.log(errors);
      });
    },
    show_tasks() {
      TaskService.show_tasks().then(response => {
        this.tasks = response.data;
      });
    },
    add_task() {
      TaskService.add_task().then(response => {
        this.show_tasks();
      }).catch(error => {
        console.log(error);
      });
    },
    del_task(id) {
      TaskService.del_task(id).then(response => {
        this.show_tasks();
      });
    },
    show_task_settings(id) {
      this.task_settings = this.tasks.filter((task) => task.id === id)[0];
      this.show_modal = true;
    },
    filtered_date(value) {
      if (value) {
        return moment(String(value)).format('DD/MM/YYYY hh:mm')
      }
    },
    filter_alias(value){
      if(value){
        return value.alias;
      }
      else{
        return null;
      }
    },
    filter_name(value){
      if(value){
        return value.name;
      }
      return null;
    }
  },
  computed:{
    connections_options(){
      let options = [];
      for (const connect of this.input_form.connections){
        options.push( connect.alias);
      }
      return options;
    }
  },
  watch:{
    task_settings: {
      handler(newValue, oldValue){
        TaskService.update_task(newValue.id, newValue).then(response => {
          newValue = response.data;
        }).catch(error => {
        });
      },
      deep: true,
    }
  }
}
</script>

<style scoped>
@import "../assets/css/main";
@import "../assets/css/select";

.add-task-button{
  margin: 0 30px;
  width: 30px;
  height: 30px;
}

.add-task-button svg{
  width: 100%;
  height: 100%;
}
.task-detail--properties {
  column-count: 3;
  width: 100%;
}

.task-detail--properties p {
  margin: 0;
  text-align: left;
}

.task-detail--properties p > span {
  font-weight: 600;
}

table {
  width: 100%;
}

form {
  display: flex;
  flex-wrap: wrap;
}

form input, form select, #date-input, form button {
  width: calc(100% - 6px);
  margin: 3px;
  height: 38px;
  box-sizing: border-box;
}

.task-table ul li:not(:first-child):hover {
  cursor: pointer;
  background: rgba(85, 85, 85, 0.2);
}

.task-header {
  display: flex;
  width: 100%;
}

.task-detail-panel {
  display: flex;
  width: 100%;
  flex-wrap: wrap;
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.2s ease-out;
}


.task-detail-panel h3 {
  width: 100%;
}

.task-table ul li:not(:first-child) {
  position: relative;
  display: flex;
  flex-wrap: wrap;
  padding: 15px;
  margin-bottom: 10px;
  border: 1px solid black;
  border-radius: 4px;
  transition: background 0.2s ease-out;
}

.task-table ul li .progress-bar {
  position: absolute;
  top: 0;
  left: 0;
  width: 10%;
  height: 62px;
  background-color: rgba(0, 128, 0, 0.3);
  transition: width 0.5s;
  /* animation:  progress-bar-animation 5s linear infinite;*/
}

@keyframes progress-bar-animation {
  to {
    width: 100%;
  }
}

ul {
  list-style-type: none;
  padding: 0;
}

.task-table ul li:first-child {
  margin-bottom: 0;
  padding: 15px;
}

.task-table ul li .task-header p {
  flex-basis: 17%;
  margin: 0;
  line-height: 30px;
}

.task-table ul li .task-header p:first-child {
  flex-basis: 5%;
}

.task-header button {
  background-color: transparent;
  border: none;
  padding: 0;
}

.show-task-detail {
  width: 30px;
  height: 30px;
  position: relative;
  transition: transform .2s ease-out;
}

.show-task-detail > div {
  position: absolute;
  left: 7.5px;
  top: calc(50% - 3px);
  height: 15px;
  width: 15px;
  border: 2px solid black;
  border-top: none;
  border-left: none;
  transform: rotate(45deg) translate(-9px, -50%);
  transform-origin: center;
}

.show-task-detail > div:first-child {
  top: calc(50% + 3px);
}

.show-task-detail.active {
  transform: rotate(180deg);
}

.task-settings-detail {
  width: 30px;
  height: 30px;
}

.task-settings-detail svg {
  width: 100%;
  height: 100%;
  transition: transform .2s ease-out;
  transform-origin: center;
}

.task-settings-detail svg:hover {
  transform: rotate(45deg);
}

.delete-task-btn {
  position: relative;
  width: 30px;
  height: 30px;
}

.delete-task-btn:before, .delete-task-btn:after {
  content: '';
  position: absolute;
  left: 0;
  top: calc(50% - 1px);
  width: 100%;
  height: 2px;
  background-color: red;
  transform: rotate(45deg);

}

.delete-task-btn:after {
  transform: rotate(-45deg);
}

.dp__theme_light {
  display: inline-block;
}




.date-time-string {
  display: flex;
  align-items: center;

}

.task-table .task-header button {
  cursor: pointer;

}
</style>