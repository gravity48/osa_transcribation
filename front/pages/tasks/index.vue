<template>
  <div class="flex flex-column">
    <div class="col-10 flex align-items-center justify-content-end">
      <div id="add-task"  @click.prevent="addTask">
        <p><i class="pi pi-plus"></i>Добавить задачу</p>
      </div>
    </div>
    <div id="task-content">
      <ul>
        <li v-for="task in tasks">
          <div>
            {{ task.alias }}
          </div>
          <div class="task-control flex justify-content-center align-items-center">
            <i class="pi pi-cog" @click.prevent="taskDetail(task.id)"></i>
            <i class="pi pi-times" @click.prevent="removeTask(task.id)"></i>
          </div>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup lang="ts">
import {TasksList} from "~/composables/tasks/list";
import {useRouter} from "@nuxtjs/composition-api";

let router = useRouter();
const {tasks, addTask, removeTask} = TasksList();

const taskDetail= (id: number) => {
  router.push(`tasks/${id}`);
}

</script>

<script lang="ts">
export default {
  middleware: ['auth']
}
</script>

<style scoped>

#add-task {
  cursor: pointer;
  padding: 5px;
  border: solid black 1px;
  border-radius: 40px;
}

#add-task:hover, ul li:hover {
  background-color: #e9ecef;
}

#task-content ul {
  padding: 0 20px;
}

#task-content ul li {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border: 1px solid black;
  border-radius: 25px;
  padding: 10px 25px;
  margin: 10px 0;
}

ul li div:last-child i {
  display: block;
  font-size: 1.4em;
  cursor: pointer;
  margin: 0 5px;
}
ul li div:last-child p{
  user-select: none;
  padding-right: 10px;
}
</style>
