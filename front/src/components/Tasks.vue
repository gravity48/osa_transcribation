<template>
  <h1>Задачи</h1>
  <div class="task-table">
    <ul>
      <li>
        <div class="task-header"><p>#</p>
          <p>Название обработчика</p>
          <p>Название подключения</p>
          <p>Тип задачи</p>
          <p>Модель</p>
          <p>Обработано записей</p>
          <button type="button" class="add-task-button" @click="add_task">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor"
                 class="bi bi-clipboard2-plus" viewBox="0 0 16 16">
              <path
                  d="M9.5 0a.5.5 0 0 1 .5.5.5.5 0 0 0 .5.5.5.5 0 0 1 .5.5V2a.5.5 0 0 1-.5.5h-5A.5.5 0 0 1 5 2v-.5a.5.5 0 0 1 .5-.5.5.5 0 0 0 .5-.5.5.5 0 0 1 .5-.5h3Z"/>
              <path
                  d="M3 2.5a.5.5 0 0 1 .5-.5H4a.5.5 0 0 0 0-1h-.5A1.5 1.5 0 0 0 2 2.5v12A1.5 1.5 0 0 0 3.5 16h9a1.5 1.5 0 0 0 1.5-1.5v-12A1.5 1.5 0 0 0 12.5 1H12a.5.5 0 0 0 0 1h.5a.5.5 0 0 1 .5.5v12a.5.5 0 0 1-.5.5h-9a.5.5 0 0 1-.5-.5v-12Z"/>
              <path d="M8.5 6.5a.5.5 0 0 0-1 0V8H6a.5.5 0 0 0 0 1h1.5v1.5a.5.5 0 0 0 1 0V9H10a.5.5 0 0 0 0-1H8.5V6.5Z"/>
            </svg>
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
          <p><span v-for="current_model in task.model" :key="current_model.id">{{ current_model.name }} &nbsp;</span></p>
          <p>{{ task.record_processed }}</p>
          <button type="button" class="task-settings-detail" @click="show_task_settings(task.id)">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-gear"
                 viewBox="0 0 16 16">
              <path
                  d="M8 4.754a3.246 3.246 0 1 0 0 6.492 3.246 3.246 0 0 0 0-6.492zM5.754 8a2.246 2.246 0 1 1 4.492 0 2.246 2.246 0 0 1-4.492 0z"/>
              <path
                  d="M9.796 1.343c-.527-1.79-3.065-1.79-3.592 0l-.094.319a.873.873 0 0 1-1.255.52l-.292-.16c-1.64-.892-3.433.902-2.54 2.541l.159.292a.873.873 0 0 1-.52 1.255l-.319.094c-1.79.527-1.79 3.065 0 3.592l.319.094a.873.873 0 0 1 .52 1.255l-.16.292c-.892 1.64.901 3.434 2.541 2.54l.292-.159a.873.873 0 0 1 1.255.52l.094.319c.527 1.79 3.065 1.79 3.592 0l.094-.319a.873.873 0 0 1 1.255-.52l.292.16c1.64.893 3.434-.902 2.54-2.541l-.159-.292a.873.873 0 0 1 .52-1.255l.319-.094c1.79-.527 1.79-3.065 0-3.592l-.319-.094a.873.873 0 0 1-.52-1.255l.16-.292c.893-1.64-.902-3.433-2.541-2.54l-.292.159a.873.873 0 0 1-1.255-.52l-.094-.319zm-2.633.283c.246-.835 1.428-.835 1.674 0l.094.319a1.873 1.873 0 0 0 2.693 1.115l.291-.16c.764-.415 1.6.42 1.184 1.185l-.159.292a1.873 1.873 0 0 0 1.116 2.692l.318.094c.835.246.835 1.428 0 1.674l-.319.094a1.873 1.873 0 0 0-1.115 2.693l.16.291c.415.764-.42 1.6-1.185 1.184l-.291-.159a1.873 1.873 0 0 0-2.693 1.116l-.094.318c-.246.835-1.428.835-1.674 0l-.094-.319a1.873 1.873 0 0 0-2.692-1.115l-.292.16c-.764.415-1.6-.42-1.184-1.185l.159-.291A1.873 1.873 0 0 0 1.945 8.93l-.319-.094c-.835-.246-.835-1.428 0-1.674l.319-.094A1.873 1.873 0 0 0 3.06 4.377l-.16-.292c-.415-.764.42-1.6 1.185-1.184l.292.159a1.873 1.873 0 0 0 2.692-1.115l.094-.319z"/>
            </svg>
          </button>
          <button type="button" class="show-task-detail">
            <div></div>
            <div></div>
          </button>
          <button type="button" v-if="task.status !== 'stopped'" @click="stop_task(task.id)">
            <svg xmlns="http://www.w3.org/2000/svg" fill="currentColor" class="bi bi-stop" viewBox="0 0 16 16">
              <path
                  d="M3.5 5A1.5 1.5 0 0 1 5 3.5h6A1.5 1.5 0 0 1 12.5 5v6a1.5 1.5 0 0 1-1.5 1.5H5A1.5 1.5 0 0 1 3.5 11V5zM5 4.5a.5.5 0 0 0-.5.5v6a.5.5 0 0 0 .5.5h6a.5.5 0 0 0 .5-.5V5a.5.5 0 0 0-.5-.5H5z"/>
            </svg>
          </button>
          <button type="button" v-if="task.status === 'stopped'" @click="play_task(task.id)">
            <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-play-circle"
                 viewBox="0 0 16 16">
              <path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/>
              <path
                  d="M6.271 5.055a.5.5 0 0 1 .52.038l3.5 2.5a.5.5 0 0 1 0 .814l-3.5 2.5A.5.5 0 0 1 6 10.5v-5a.5.5 0 0 1 .271-.445z"/>
            </svg>
          </button>
        </div>
        <div class="task-detail-panel">
          <button type="button" class="delete-task-btn" :data-item="task.id" @click="del_task(task.id)">
            <div>
              <div></div>
            </div>
          </button>
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
            <Datepicker id="period-to" format="dd/MM/yyyy" v-model="task_settings.period_from"
                        :maxDate="task_settings.period_to" locale="ru"/>
            <span>по</span>
            <Datepicker id="period-from" format="dd/MM/yyyy" v-model="task_settings.period_to"
                        :minDate="task_settings.period_from" locale="ru"/>
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
        <div class="form-option">
          <label for="task-type"> <span class="input-header">Список ключевых слов</span> <br> <span class="input-detail"> Введите ключевые слова, в каждой строчке новое слово</span></label>
          <textarea v-model="task_settings.options.keywords"></textarea>
        </div>
      </div>
    </div>
    <div class="column">
      <div class="col-content">
        <div class="form-option">
          <label for="model-id"><span class="input-header">Лингафонная модель </span> <br> <span class="input-detail">Выберите из списка модель обработки голоса в зависимости от языка </span>
          </label>
          <v-select multiple v-model="task_settings.model" label="name" :options="input_form.models"></v-select>
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
            <input id='time-process' type="number" v-model="task_settings.options.speech_time"
                   placeholder="Time process">
          </div>
          <div class="form-option">
            <label for="process-count"><span class="input-header">Процент распознавания</span><br><span
                class="input-detail">Процент при котором распознанное слово будет приниматься в результат <br> распознавания (указывется от 1 до 100)</span>
            </label>
            <input id='time-process' type="number" v-model="task_settings.options.recognize_percent"
                   placeholder="Time process">
          </div>
        </div>
      </div>
    </div>
    <div id="modal-close">
      <button class="modal-close-btn" @click="show_modal = false; this.show_tasks();">
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
import moment from 'moment';

import TaskService from "@/services/task-service";
import axios from "axios";
import vSelect from "vue-select";
import 'vue-select/dist/vue-select.css';


export default {
  name: "TasksView",
  components: {
    vSelect,
  },
  props: {},
  data() {
    return {
      loader: null,
      show_modal: false,
      tasks: [],
      task_settings: {
        options: {}
      },
      input_form: {
        models: [],
        tasks_type: [],
        connections: [],
      },
      field_translation: {
        'alias': 'Название обработчика',
        'thread_count': 'Количество процессов',
        'db': 'База данных',
        'model': 'Лингафонная модель',
        'task_type': 'Задача обработчика',
        'period_from': 'Период До',
        'period_to': 'Период После',
        'time_processing': 'Таймаут процесса',
        'transcribing_server': 'Сервер транскирибации',
      }
    }
  },
  mounted() {
    this.show_tasks();
    this.init_input_form();
    setInterval(this.status_tasks, 2000);
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
    play_task(id) {
      TaskService.play_task(id).then(response => {
        console.log(response);
        this.$notify({
          title: this.tasks.filter((task) => task.id === id)[0].alias,
          type: 'success',
          text: 'Запуск обработчика',
          duration: 5000,
        });
        this.show_tasks();
      }).catch(error => {
        for (const [key, value] of Object.entries(error.response.data)) {
          this.$notify({
            title: this.field_translation[key],
            text: value,
            type: 'error',
            duration: 5000,
          });
          this.show_tasks();
        }
      })
    },
    stop_task(id) {
      TaskService.stop_task(id).then(response => {
        this.$notify({
          title: this.tasks.filter((task) => task.id === id)[0].alias,
          type: 'success',
          text: 'Обработчик остановлен',
          duration: 5000,
        });
        this.show_tasks();
      }).catch(error => {
        this.$notify({
          title: 'Сервер транскрибации',
          text: 'Сервер транскрибации недоступен',
          type: 'error',
          duration: 5000,
        });
        this.show_tasks();
      })

    },
    status_tasks() {
      if (this.running_task.length) {
        let data = {
          'task_run': this.running_task,
        }
        TaskService.status_task(data).then(response => {
          for (const [key, value] of Object.entries(response.data)) {
            if (value.is_running !== false) {
              let key_int = parseInt(key)
              this.tasks.filter((task) => task['id'] === key_int)[0].record_processed = value.record_processed;
            }
          }
        });
      }
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
    filter_alias(value) {
      if (value) {
        return value.alias;
      } else {
        return null;
      }
    },
    filter_name(value) {
      if (value) {
        return value.name;
      }
      return null;
    }
  },
  computed: {
    connections_options() {
      let options = [];
      for (const connect of this.input_form.connections) {
        options.push(connect.alias);
      }
      return options;
    },
    running_task() {
      return this.tasks.filter((task) => task.status !== 'stopped');
    }
  },
  watch: {
    task_settings: {
      handler(newValue, oldValue) {
        TaskService.update_task(newValue.id, newValue).then(response => {
        }).catch(error => {
          console.log(error);
          this.task_settings = error.response.data.data;
          for (const [key, value] of Object.entries(error.response.data.errors)) {
            this.$notify({
              type: 'error',
              title: this.field_translation[key],
              text: value,
              duration: 5000
            });
          }
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

textarea{
  width: 100%;
  height: 100px;
}

.task-header button {
  width: 30px;
  height: 30px;
}

.task-header button svg {
  width: 100%;
  height: 100%;
}

.add-task-button {
  margin: 0 30px;
  width: 30px;
  height: 30px;
}

.add-task-button svg {
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
  position: relative;
  display: flex;
  width: 100%;
  flex-wrap: wrap;
  max-height: 0;
  overflow: hidden;
  transition: max-height 0.2s ease-out;
  padding: 5px 0;
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
  position: absolute;
  width: 23px;
  height: 23px;
  left: calc(100% - 39px);
  background-color: transparent;
  border: none;
  top: 24px
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

.delete-task-btn:hover {
  cursor: pointer;
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