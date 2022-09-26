import api from "@/services/api";

const API_URL = 'tasks/'


class TaskService {
    show_tasks() {
        return api.get(API_URL)
    }

    add_task() {
        return api.post(API_URL)
    }

    del_task(id) {
        return api.delete(API_URL + id + '/')
    }

    update_task(id, data){
        return api.put(API_URL + id + '/', data)
    }

    get_tasks_type() {
        return api.get('tasks_type/')
    }

    get_models_list() {
        return api.get('models/')
    }

    get_connections_list() {
        return api.get('connections/', {
            params: {
                db_status: 1,
            },
        })
    }
}

export default new TaskService();