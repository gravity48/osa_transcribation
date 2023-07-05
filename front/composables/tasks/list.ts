import {Ref, ssrRef, useAsync, useContext} from "@nuxtjs/composition-api";
import {Task} from "~/types/types";

export  const TasksList = () => {
  const {$axios} = useContext();

  const tasks: Ref<Array<Task>> = useAsync(()=> $axios.get('api/v1/tasks/tasks/').then(r => r.data));

  const addTask = () =>{
    $axios.post('api/v1/tasks/tasks/').then(r => {
      tasks.value.push(r.data);
    })
  }
  const removeTask = async (id: number) =>{
    await $axios.delete(`api/v1/tasks/tasks/${id}`);
  }
  return {
    tasks,
    addTask,
    removeTask
  }
}
