<template>
  <div id="task-detail-content" class="flex justify-content-around">
    <div class="required-params">
      <div class="input-grp">
        <InputText placeholder="Alias" v-model="task.alias"/>
      </div>
      <div class="input-grp">
        <Dropdown
          v-model="task.db"
          :options="connections"
          optionValue="id"
          optionLabel="alias"
          placeholder="Соединение"
        />
      </div>
      <div class="input-grp">
        <p>Число процессов</p>
        <InputNumber
          inputId="withoutgrouping"
          v-model="task.thread_count"
          placeholder="Thread Count"
        />
      </div>
      <div class="input-grp">
        <p>Сервера распознавания</p>
        <MultiSelect
          v-model="task.model"
          display="chip"
          :options="recognize_servers"
          optionLabel="name"
          optionValue="id"
          placeholder="Выберите сервер распознавания"
        />
      </div>
      <div class="input-grp">
        <p>Период от</p>
        <Calendar
          v-model="task.period_from"
          showTime
          showIcon
          hourFormat="24"
        />
        <p>Период до</p>
        <Calendar
          v-model="task.period_to"
          showTime
          showIcon
          hourFormat="24"
        />
      </div>
    </div>
    <div class="non-required-params">

    </div>
  </div>
</template>


<script setup lang="ts">
import InputText from 'primevue/inputtext';
import Dropdown from "primevue/dropdown/Dropdown";
import InputNumber from 'primevue/inputnumber';
import MultiSelect from 'primevue/multiselect';
import Calendar from 'primevue/calendar';


import {taskDetail} from "~/composables/tasks/detail";
import {computed, useAsync, useContext, watch} from "@nuxtjs/composition-api";
import {Connections} from "~/types/types";

const {route, store} = useContext();

const {task, watchTask} = taskDetail(route.value.params.id);

const connections = computed(() => store.getters['connections/connections'].filter((item: Connections) => item.db_status === 'Active'));

const recognize_servers = computed(() => store.getters['recognize_servers']);

useAsync(() => {
  store.dispatch('connections/fetchConnections');
})

watch(task, watchTask, {deep: true});

</script>

<script lang="ts">
export default {
  name: "TaskDetail",
  middleware: ['auth']
}
</script>

<style scoped>

#task-detail-content {
  margin: 0 5%;
  padding: 20px 0;
}

#task-detail-content > div {
  border: 1px solid black;
  border-radius: 25px;
  padding: 20px;
}

.input-grp {
  margin: 20px 0;
}


</style>
