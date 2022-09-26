import api from "@/services/api";

class ViewService{
    users_api(){
        return api.get('user/');
    }
    get_connections(){
        return api.get('connections/');
    }
    get_db_systems(){
        return api.get('database_system/');
    }
    add_connections(){
        return api.post('connections/')
    }
    refresh_connections(data){
        return api.post('connections/', data)
    }
    delete_connections(id){
        return api.delete('connections/' + id +'/')
    }
    update_connections(id, data){
        return api.put('connections/' + id + '/', data)
    }
    get_alias(){
        return api.get('connections/alias/')
    }
}
export default new ViewService();