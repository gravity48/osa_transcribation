import {onBeforeMount, Ref, ssrRef, useAsync, useContext, useFetch, watch} from "@nuxtjs/composition-api";
import {Task} from "~/types/types";


export const taskDetail = (pk: string) => {
  let timeout: ReturnType<typeof setTimeout>;
  const {$axios} = useContext();
  const task: Ref<Task> = ssrRef({
    id: -1,
    alias: '',
    db: '',
    options: {}
  });

  useAsync(async () => {
    task.value = await $axios.get(`api/v1/tasks/tasks/${pk}`).then(r => r.data);
  }, pk);

  const watchTask = (newTask: Task, oldTask: Task) =>{
    if (newTask.id === oldTask.id){
      clearTimeout(timeout);
      setTimeout(()=> {
        $axios.put(`api/v1/tasks/tasks/${pk}/`, newTask).catch(err => console.log(err));
      }, 1000);
    }
  }

  return {
    task,
    watchTask,
  }
}
