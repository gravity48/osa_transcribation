import api from "@/services/api";

const API_URL = 'tasks/'


class TaskService{
    show_tasks(){
        return api.get(API_URL)
    }
    add_task(){
        return api.post(API_URL)
    }
    del_task(id){
        return api.delete(API_URL + id + '/')
    }
    get_tasks_type(){
        return api.get('tasks_type/')
    }
    get_models_list(){
        return api.get('models/')
    }
}

export default new TaskService();